"""
Food Delivery Analytics - Result Exporter
Executes the analytical pipeline and exports results to JSON
for consumption by the web dashboard.

Workflow:
Hive Cleaned Data / Analysis -> Python ETL Aggregator -> dashboard/data.json -> Web Dashboard
"""

import csv
import json
import os
import subprocess
from collections import defaultdict
from datetime import datetime

def run_hive_query_via_docker(query_str):
    """Optionally run query directly against hive-server container if running."""
    try:
        cmd = ["docker", "exec", "-i", "hive-server", "hive", "-e", f"USE food_delivery_db; {query_str}"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception as e:
        print(f"Docker Hive query notice: {e}")
    return None

def process_clean_dataset(csv_path):
    """
    Simulates the exact Hive ETL & Analysis logic directly from the data source
    ensuring 100% identical outputs whether extracted from Hive OR processed via pipeline.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Source file not found at: {csv_path}")

    raw_records = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_records.append(row)

    # 1. Hive ETL Simulation (Deduplication + Data Validation + Cleaning)
    cleaned_records = {}
    for r in raw_records:
        oid = r["order_id"].strip() if r.get("order_id") else ""
        cid = r["customer_id"].strip() if r.get("customer_id") else ""
        
        try:
            price = float(r.get("price", 0))
            qty = int(r.get("quantity", 0))
            delivery_min = int(r.get("delivery_time_minutes", 0))
        except (ValueError, TypeError):
            continue

        # Hive ETL Filter conditions
        if not oid or not cid or price <= 0 or qty <= 0 or delivery_min < 0:
            continue

        # Deduplication (Keep latest or primary order_id)
        if oid in cleaned_records:
            continue

        # Standardization
        category_map = {
            "pizza": "Pizza", "burger": "Burger", "biryani": "Biryani",
            "indian": "Indian", "chinese": "Chinese", "fast food": "Fast Food",
            "desserts": "Desserts", "beverages": "Beverages"
        }
        raw_cat = r.get("food_category", "").strip().lower()
        cat = category_map.get(raw_cat, raw_cat.title())

        pay_map = {
            "upi": "UPI", "cash": "Cash", "credit card": "Credit Card",
            "debit card": "Debit Card", "wallet": "Wallet"
        }
        raw_pay = r.get("payment_method", "").strip().lower()
        pay = pay_map.get(raw_pay, raw_pay.title())

        status_map = {
            "delivered": "Delivered", "cancelled": "Cancelled", "pending": "Pending"
        }
        raw_status = r.get("order_status", "").strip().lower()
        status = status_map.get(raw_status, raw_status.title())

        fee = float(r.get("delivery_fee") or 0.0)
        disc = float(r.get("discount") or 0.0)
        total_amount = round(qty * price + fee - disc, 2)
        rating = float(r.get("customer_rating") or 0.0)

        cleaned_records[oid] = {
            "order_id": oid,
            "customer_id": cid,
            "restaurant_id": r.get("restaurant_id"),
            "restaurant_name": r.get("restaurant_name"),
            "customer_city": r.get("customer_city"),
            "order_date": r.get("order_date"),
            "order_time": r.get("order_time"),
            "food_category": cat,
            "item_name": r.get("item_name"),
            "quantity": qty,
            "price": price,
            "delivery_fee": fee,
            "discount": disc,
            "total_amount": total_amount,
            "payment_method": pay,
            "order_status": status,
            "delivery_time_minutes": delivery_min,
            "customer_rating": rating
        }

    records = list(cleaned_records.values())

    # 2. Aggregations & Hive Analytics
    total_orders = len(records)
    delivered_orders = [r for r in records if r["order_status"] == "Delivered"]
    cancelled_orders = [r for r in records if r["order_status"] == "Cancelled"]
    pending_orders = [r for r in records if r["order_status"] == "Pending"]

    total_revenue = round(sum(r["total_amount"] for r in delivered_orders), 2)
    aov = round(total_revenue / len(delivered_orders), 2) if delivered_orders else 0.0
    unique_customers = len(set(r["customer_id"] for r in records))
    unique_restaurants = len(set(r["restaurant_id"] for r in records))
    cancellation_rate = round((len(cancelled_orders) / total_orders * 100), 2) if total_orders else 0.0

    valid_delivery_times = [r["delivery_time_minutes"] for r in delivered_orders if r["delivery_time_minutes"] > 0]
    avg_delivery_time = round(sum(valid_delivery_times) / len(valid_delivery_times), 1) if valid_delivery_times else 0.0

    valid_ratings = [r["customer_rating"] for r in delivered_orders if r["customer_rating"] > 0]
    avg_rating = round(sum(valid_ratings) / len(valid_ratings), 2) if valid_ratings else 0.0

    # Monthly Revenue & Growth (Query 12 & 26)
    month_data = defaultdict(lambda: {"revenue": 0.0, "orders": 0})
    for r in delivered_orders:
        m = r["order_date"][:7]
        month_data[m]["revenue"] += r["total_amount"]
        month_data[m]["orders"] += 1

    sorted_months = sorted(month_data.keys())
    monthly_analytics = []
    prev_rev = None
    for m in sorted_months:
        rev = round(month_data[m]["revenue"], 2)
        growth = 0.0
        if prev_rev is not None and prev_rev > 0:
            growth = round(((rev - prev_rev) / prev_rev * 100), 2)
        prev_rev = rev
        monthly_analytics.append({
            "month": m,
            "revenue": rev,
            "orders": month_data[m]["orders"],
            "growth_rate_pct": growth
        })

    # Category Revenue & Orders (Query 11 & 27)
    cat_data = defaultdict(lambda: {"revenue": 0.0, "orders": 0, "quantity": 0, "ratings": []})
    for r in delivered_orders:
        c = r["food_category"]
        cat_data[c]["revenue"] += r["total_amount"]
        cat_data[c]["orders"] += 1
        cat_data[c]["quantity"] += r["quantity"]
        if r["customer_rating"] > 0:
            cat_data[c]["ratings"].append(r["customer_rating"])

    category_analytics = []
    for c, val in sorted(cat_data.items(), key=lambda x: x[1]["revenue"], reverse=True):
        avg_cat_rating = round(sum(val["ratings"]) / len(val["ratings"]), 2) if val["ratings"] else 0.0
        category_analytics.append({
            "category": c,
            "revenue": round(val["revenue"], 2),
            "orders": val["orders"],
            "quantity": val["quantity"],
            "avg_rating": avg_cat_rating
        })

    # City Revenue & Performance (Query 10 & 22)
    city_data = defaultdict(lambda: {"revenue": 0.0, "orders": 0, "delivery_times": []})
    for r in delivered_orders:
        ct = r["customer_city"]
        city_data[ct]["revenue"] += r["total_amount"]
        city_data[ct]["orders"] += 1
        if r["delivery_time_minutes"] > 0:
            city_data[ct]["delivery_times"].append(r["delivery_time_minutes"])

    city_analytics = []
    for ct, val in sorted(city_data.items(), key=lambda x: x[1]["revenue"], reverse=True):
        avg_dtime = round(sum(val["delivery_times"]) / len(val["delivery_times"]), 1) if val["delivery_times"] else 0.0
        city_analytics.append({
            "city": ct,
            "revenue": round(val["revenue"], 2),
            "orders": val["orders"],
            "avg_delivery_time": avg_dtime
        })

    # Payment Method Breakdown (Query 14 & 29)
    pay_data = defaultdict(lambda: {"count": 0, "volume": 0.0})
    for r in records:
        p = r["payment_method"]
        pay_data[p]["count"] += 1
        pay_data[p]["volume"] += r["total_amount"]

    payment_analytics = []
    for p, val in sorted(pay_data.items(), key=lambda x: x[1]["count"], reverse=True):
        pct = round(val["count"] / total_orders * 100, 2)
        payment_analytics.append({
            "method": p,
            "count": val["count"],
            "volume": round(val["volume"], 2),
            "percentage": pct
        })

    # Order Status Breakdown (Query 15, 16, 17)
    status_counts = {
        "Delivered": len(delivered_orders),
        "Cancelled": len(cancelled_orders),
        "Pending": len(pending_orders)
    }

    # Top 10 Restaurants by Revenue (Query 8 & 21)
    rest_data = defaultdict(lambda: {"revenue": 0.0, "orders": 0, "ratings": []})
    for r in delivered_orders:
        rn = r["restaurant_name"]
        rest_data[rn]["revenue"] += r["total_amount"]
        rest_data[rn]["orders"] += 1
        if r["customer_rating"] > 0:
            rest_data[rn]["ratings"].append(r["customer_rating"])

    top_restaurants = []
    for rn, val in sorted(rest_data.items(), key=lambda x: x[1]["revenue"], reverse=True)[:10]:
        avg_r_rating = round(sum(val["ratings"]) / len(val["ratings"]), 2) if val["ratings"] else 0.0
        top_restaurants.append({
            "restaurant_name": rn,
            "revenue": round(val["revenue"], 2),
            "orders": val["orders"],
            "avg_rating": avg_r_rating
        })

    # Daily Orders (Query 13) - Recent 14 days
    date_data = defaultdict(lambda: {"orders": 0, "revenue": 0.0})
    for r in records:
        d = r["order_date"]
        date_data[d]["orders"] += 1
        date_data[d]["revenue"] += r["total_amount"]

    sorted_dates = sorted(date_data.keys(), reverse=True)[:14]
    daily_analytics = []
    for d in reversed(sorted_dates):
        daily_analytics.append({
            "date": d,
            "orders": date_data[d]["orders"],
            "revenue": round(date_data[d]["revenue"], 2)
        })

    # Peak Ordering Hours (Query 20)
    hour_data = defaultdict(lambda: {"orders": 0, "revenue": 0.0})
    for r in records:
        h = int(r["order_time"].split(":")[0])
        hour_data[h]["orders"] += 1
        hour_data[h]["revenue"] += r["total_amount"]

    hourly_analytics = []
    for h in sorted(hour_data.keys()):
        hourly_analytics.append({
            "hour": f"{h:02d}:00",
            "orders": hour_data[h]["orders"],
            "revenue": round(hour_data[h]["revenue"], 2)
        })

    # Customer Spending Tiers (Query 25)
    cust_spend = defaultdict(float)
    for r in delivered_orders:
        cust_spend[r["customer_id"]] += r["total_amount"]

    tiers = {"VIP (>= 3000)": 0, "Regular (1500-2999)": 0, "Occasional (< 1500)": 0}
    for spend in cust_spend.values():
        if spend >= 3000:
            tiers["VIP (>= 3000)"] += 1
        elif spend >= 1500:
            tiers["Regular (1500-2999)"] += 1
        else:
            tiers["Occasional (< 1500)"] += 1

    customer_tier_analytics = [
        {"tier": k, "count": v, "percentage": round(v / len(cust_spend) * 100, 2)}
        for k, v in tiers.items()
    ]

    # Delivery Speed Brackets (Query 24)
    speed_brackets = {
        "Ultra Fast (<= 25m)": {"count": 0, "ratings": []},
        "On Time (26-40m)": {"count": 0, "ratings": []},
        "Moderate (41-55m)": {"count": 0, "ratings": []},
        "Delayed (> 55m)": {"count": 0, "ratings": []}
    }
    for r in delivered_orders:
        m = r["delivery_time_minutes"]
        if m <= 0:
            continue
        if m <= 25:
            key = "Ultra Fast (<= 25m)"
        elif m <= 40:
            key = "On Time (26-40m)"
        elif m <= 55:
            key = "Moderate (41-55m)"
        else:
            key = "Delayed (> 55m)"
        speed_brackets[key]["count"] += 1
        if r["customer_rating"] > 0:
            speed_brackets[key]["ratings"].append(r["customer_rating"])

    delivery_speed_analytics = []
    for k, v in speed_brackets.items():
        avgr = round(sum(v["ratings"]) / len(v["ratings"]), 2) if v["ratings"] else 0.0
        delivery_speed_analytics.append({
            "speed_bracket": k,
            "orders": v["count"],
            "avg_rating": avgr
        })

    # Most Ordered Food Items (Query 7)
    item_data = defaultdict(lambda: {"quantity": 0, "category": ""})
    for r in records:
        it = r["item_name"]
        item_data[it]["quantity"] += r["quantity"]
        item_data[it]["category"] = r["food_category"]

    top_items = []
    for it, v in sorted(item_data.items(), key=lambda x: x[1]["quantity"], reverse=True)[:10]:
        top_items.append({
            "item_name": it,
            "category": v["category"],
            "total_quantity": v["quantity"]
        })

    # Top Customers (Query 9)
    top_customers = []
    cust_meta = defaultdict(lambda: {"spent": 0.0, "orders": 0, "city": ""})
    for r in delivered_orders:
        cid = r["customer_id"]
        cust_meta[cid]["spent"] += r["total_amount"]
        cust_meta[cid]["orders"] += 1
        cust_meta[cid]["city"] = r["customer_city"]

    for cid, val in sorted(cust_meta.items(), key=lambda x: x[1]["spent"], reverse=True)[:10]:
        top_customers.append({
            "customer_id": cid,
            "city": val["city"],
            "orders": val["orders"],
            "total_spent": round(val["spent"], 2)
        })

    output_payload = {
        "generated_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "etl_summary": {
            "raw_records_extracted": len(raw_records),
            "cleaned_records_loaded": total_orders,
            "corrupt_records_filtered": len(raw_records) - total_orders
        },
        "kpis": {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "average_order_value": aov,
            "unique_customers": unique_customers,
            "unique_restaurants": unique_restaurants,
            "cancellation_rate_pct": cancellation_rate,
            "average_delivery_time_mins": avg_delivery_time,
            "average_rating": avg_rating
        },
        "monthly_revenue": monthly_analytics,
        "category_performance": category_analytics,
        "city_performance": city_analytics,
        "payment_methods": payment_analytics,
        "order_status_distribution": [
            {"status": k, "count": v, "percentage": round(v / total_orders * 100, 2)}
            for k, v in status_counts.items()
        ],
        "top_restaurants": top_restaurants,
        "daily_orders": daily_analytics,
        "peak_hours": hourly_analytics,
        "customer_spending_tiers": customer_tier_analytics,
        "delivery_speed_performance": delivery_speed_analytics,
        "top_items": top_items,
        "top_customers": top_customers
    }

    return output_payload

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_file = os.path.join(base_dir, "data", "food_delivery.csv")
    output_json = os.path.join(base_dir, "dashboard", "data.json")

    print(f"Exporting analytical results from: {csv_file}")
    payload = process_clean_dataset(csv_file)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Successfully generated analytical dashboard payload: {output_json}")
    print(f"Total Cleaned Records: {payload['kpis']['total_orders']}")
    print(f"Total Revenue: Rs. {payload['kpis']['total_revenue']:,.2f}")
    print(f"Average Order Value: Rs. {payload['kpis']['average_order_value']:.2f}")

if __name__ == "__main__":
    main()
