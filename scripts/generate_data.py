"""
Food Delivery Dataset Generator
Generates realistic food delivery dataset with at least 5,000 records,
including intentional dirty data (NULLs, duplicates, invalid records)
to demonstrate Big Data ETL cleaning in Apache Hive.
"""

import csv
import os
import random
from datetime import datetime, timedelta

def generate_dataset(output_path="../data/food_delivery.csv", num_records=5200):
    random.seed(42)
    
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    cities = [
        "Mumbai", "Delhi", "Bangalore", "Hyderabad", 
        "Chennai", "Kolkata", "Pune", "Ahmedabad"
    ]
    
    restaurants_by_category = {
        "Pizza": [
            ("REST_101", "Domino's Pizza"),
            ("REST_102", "Pizza Hut"),
            ("REST_103", "Ovenstory Pizza"),
            ("REST_104", "La Pino'z Pizza")
        ],
        "Burger": [
            ("REST_105", "Burger King"),
            ("REST_106", "McDonald's"),
            ("REST_107", "Wendy's"),
            ("REST_108", "The Burger Club")
        ],
        "Biryani": [
            ("REST_109", "Paradise Biryani"),
            ("REST_110", "Behrouz Biryani"),
            ("REST_111", "Bawarchi"),
            ("REST_112", "Meghana Foods")
        ],
        "Indian": [
            ("REST_113", "Punjab Grill"),
            ("REST_114", "Barbeque Nation"),
            ("REST_115", "Haldiram's"),
            ("REST_116", "Saravanaa Bhavan")
        ],
        "Chinese": [
            ("REST_117", "Mainland China"),
            ("REST_118", "Wow! Momo"),
            ("REST_119", "Wok Express"),
            ("REST_120", "Berco's")
        ],
        "Fast Food": [
            ("REST_121", "Subway"),
            ("REST_122", "KFC"),
            ("REST_123", "Taco Bell"),
            ("REST_124", "Faasos")
        ],
        "Desserts": [
            ("REST_125", "Baskin Robbins"),
            ("REST_126", "Theobroma"),
            ("REST_127", "Naturals Ice Cream"),
            ("REST_128", "Belgian Waffle Co")
        ],
        "Beverages": [
            ("REST_129", "Starbucks"),
            ("REST_130", "Chaayos"),
            ("REST_131", "Cafe Coffee Day"),
            ("REST_132", "Chai Point")
        ]
    }
    
    items_by_category = {
        "Pizza": [
            ("Margherita Pizza", 249.00),
            ("Pepperoni Feast", 499.00),
            ("Farmhouse Supreme", 399.00),
            ("Paneer Tikka Pizza", 349.00),
            ("Cheese Burst Pizza", 429.00)
        ],
        "Burger": [
            ("Crispy Veg Burger", 129.00),
            ("Double Whopper", 299.00),
            ("Classic Chicken Burger", 199.00),
            ("Fiery Paneer Burger", 179.00),
            ("Smoky BBQ Burger", 249.00)
        ],
        "Biryani": [
            ("Hyderabadi Chicken Biryani", 320.00),
            ("Mutton Dum Biryani", 450.00),
            ("Veg Dum Biryani", 240.00),
            ("Kolkata Special Biryani", 350.00),
            ("Paneer Biryani", 260.00)
        ],
        "Indian": [
            ("Paneer Butter Masala", 280.00),
            ("Butter Chicken", 360.00),
            ("Dal Makhani", 220.00),
            ("Garlic Naan Combo", 160.00),
            ("Kadhai Paneer", 270.00)
        ],
        "Chinese": [
            ("Veg Hakka Noodles", 180.00),
            ("Chicken Fried Rice", 230.00),
            ("Chilli Chicken Gravy", 270.00),
            ("Schezwan Veg Momos", 150.00),
            ("Manchurian Gravy", 210.00)
        ],
        "Fast Food": [
            ("Crispy Chicken Bucket", 480.00),
            ("Veggie Delight Sub", 190.00),
            ("Cheesy French Fries", 120.00),
            ("Chicken Zinger Meal", 299.00),
            ("Paneer Wrap", 160.00)
        ],
        "Desserts": [
            ("Chocolate Truffle Pastry", 140.00),
            ("Red Velvet Jar Cake", 175.00),
            ("Belgian Chocolate Waffle", 160.00),
            ("Gulab Jamun (2 pcs)", 80.00),
            ("Nutella Brownie", 130.00)
        ],
        "Beverages": [
            ("Cold Coffee with Ice Cream", 150.00),
            ("Caffe Latte", 220.00),
            ("Masala Chai (Flask)", 110.00),
            ("Mango Smoothie", 160.00),
            ("Iced Green Tea", 130.00)
        ]
    }
    
    payment_methods = ["UPI", "Cash", "Credit Card", "Debit Card", "Wallet"]
    payment_weights = [0.45, 0.20, 0.18, 0.10, 0.07]
    
    statuses = ["Delivered", "Cancelled", "Pending"]
    status_weights = [0.85, 0.10, 0.05]
    
    customers = [f"CUST_{i:04d}" for i in range(1, 801)]
    
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    delta_days = (end_date - start_date).days
    
    records = []
    
    for i in range(1, num_records + 1):
        order_id = f"ORD_{i:05d}"
        customer_id = random.choice(customers)
        city = random.choice(cities)
        
        category = random.choice(list(restaurants_by_category.keys()))
        rest_id, rest_name = random.choice(restaurants_by_category[category])
        item_name, base_price = random.choice(items_by_category[category])
        
        random_days = random.randint(0, delta_days)
        order_dt = start_date + timedelta(days=random_days)
        order_date_str = order_dt.strftime("%Y-%m-%d")
        
        # Peak hours weighting (lunch 12-15, dinner 19-23)
        peak_rand = random.random()
        if peak_rand < 0.40:
            hour = random.choice([19, 20, 21, 22])
        elif peak_rand < 0.70:
            hour = random.choice([12, 13, 14])
        else:
            hour = random.randint(8, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        order_time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        
        quantity = random.choices([1, 2, 3, 4, 5], weights=[0.55, 0.25, 0.12, 0.05, 0.03])[0]
        delivery_fee = round(random.choice([0.0, 20.0, 30.0, 40.0, 50.0]), 2)
        
        # Discounts
        discount_chance = random.random()
        if discount_chance < 0.35:
            discount = 0.0
        elif discount_chance < 0.75:
            discount = round(random.uniform(20.0, 75.0), 2)
        else:
            discount = round(random.uniform(75.0, 150.0), 2)
            
        payment_method = random.choices(payment_methods, weights=payment_weights)[0]
        order_status = random.choices(statuses, weights=status_weights)[0]
        
        if order_status == "Delivered":
            delivery_time = random.randint(18, 65)
            rating = round(random.choices(
                [5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.0],
                weights=[0.35, 0.28, 0.18, 0.08, 0.05, 0.03, 0.02, 0.01]
            )[0], 1)
        elif order_status == "Cancelled":
            delivery_time = 0
            rating = 0.0
        else: # Pending
            delivery_time = random.randint(20, 45)
            rating = 0.0
            
        record = {
            "order_id": order_id,
            "customer_id": customer_id,
            "restaurant_id": rest_id,
            "restaurant_name": rest_name,
            "customer_city": city,
            "order_date": order_date_str,
            "order_time": order_time_str,
            "food_category": category,
            "item_name": item_name,
            "quantity": quantity,
            "price": base_price,
            "delivery_fee": delivery_fee,
            "discount": discount,
            "payment_method": payment_method,
            "order_status": order_status,
            "delivery_time_minutes": delivery_time,
            "customer_rating": rating
        }
        
        # ----------------------------------------------------------------------
        # Inject intentional dirty/corrupt data (~3.5% of records) for ETL demo
        # ----------------------------------------------------------------------
        dirty_flag = random.random()
        if dirty_flag < 0.006:
            # Missing customer_id
            record["customer_id"] = ""
        elif dirty_flag < 0.012:
            # Negative or zero price
            record["price"] = -50.00
        elif dirty_flag < 0.018:
            # Negative or zero quantity
            record["quantity"] = 0
        elif dirty_flag < 0.024:
            # Lowercase / dirty category
            record["food_category"] = record["food_category"].lower()
        elif dirty_flag < 0.030:
            # Inconsistent payment method
            record["payment_method"] = record["payment_method"].lower()
        elif dirty_flag < 0.035:
            # Missing rating for delivered order
            record["customer_rating"] = ""
            
        records.append(record)
        
    # Inject 40 explicit duplicate records to verify deduplication
    duplicate_samples = random.sample(records[:500], 40)
    for dup in duplicate_samples:
        records.append(dict(dup))
        
    headers = [
        "order_id", "customer_id", "restaurant_id", "restaurant_name",
        "customer_city", "order_date", "order_time", "food_category",
        "item_name", "quantity", "price", "delivery_fee", "discount",
        "payment_method", "order_status", "delivery_time_minutes",
        "customer_rating"
    ]
    
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)
        
    print(f"Successfully generated {len(records)} records in {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(current_dir, "..", "data", "food_delivery.csv")
    generate_dataset(output_path=target_file, num_records=5200)
