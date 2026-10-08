/**
 * Food Delivery Big Data Analytics Dashboard
 * Chart.js Integration & Data Binding Logic
 */

let charts = {};

// Fallback dataset in case opened via file:// protocol directly
const fallbackData = {
  kpis: {
    total_orders: 5114,
    total_revenue: 1776410.97,
    average_order_value: 411.49,
    unique_customers: 800,
    unique_restaurants: 32,
    cancellation_rate_pct: 9.84,
    average_delivery_time_mins: 34.6,
    average_rating: 4.32
  },
  monthly_revenue: [
    { month: "2024-01", revenue: 148520.50, orders: 362 },
    { month: "2024-02", revenue: 142110.20, orders: 345 },
    { month: "2024-03", revenue: 153400.80, orders: 374 },
    { month: "2024-04", revenue: 149230.10, orders: 358 },
    { month: "2024-05", revenue: 158940.00, orders: 382 },
    { month: "2024-06", revenue: 146890.30, orders: 351 },
    { month: "2024-07", revenue: 152120.40, orders: 368 },
    { month: "2024-08", revenue: 144500.60, orders: 349 },
    { month: "2024-09", revenue: 150240.70, orders: 361 },
    { month: "2024-10", revenue: 161820.90, orders: 390 },
    { month: "2024-11", revenue: 159450.40, orders: 385 },
    { month: "2024-12", revenue: 169177.07, orders: 405 }
  ],
  category_performance: [
    { category: "Pizza", revenue: 312450.00, orders: 742 },
    { category: "Biryani", revenue: 298120.00, orders: 698 },
    { category: "Indian", revenue: 275340.00, orders: 680 },
    { category: "Burger", revenue: 234150.00, orders: 654 },
    { category: "Fast Food", revenue: 221800.00, orders: 641 },
    { category: "Chinese", revenue: 215400.00, orders: 620 },
    { category: "Desserts", revenue: 112400.00, orders: 554 },
    { category: "Beverages", revenue: 106750.97, orders: 525 }
  ],
  city_performance: [
    { city: "Mumbai", revenue: 268400.00, orders: 660, avg_delivery_time: 36.2 },
    { city: "Delhi", revenue: 254100.00, orders: 635, avg_delivery_time: 38.4 },
    { city: "Bangalore", revenue: 245200.00, orders: 610, avg_delivery_time: 33.1 },
    { city: "Hyderabad", revenue: 238900.00, orders: 595, avg_delivery_time: 31.8 },
    { city: "Pune", revenue: 204500.00, orders: 512, avg_delivery_time: 32.5 },
    { city: "Chennai", revenue: 198300.00, orders: 495, avg_delivery_time: 35.0 },
    { city: "Kolkata", revenue: 189400.00, orders: 480, avg_delivery_time: 37.6 },
    { city: "Ahmedabad", revenue: 177610.97, orders: 443, avg_delivery_time: 32.0 }
  ],
  payment_methods: [
    { method: "UPI", count: 2301, volume: 805400.00, percentage: 45.0 },
    { method: "Cash", count: 1022, volume: 351200.00, percentage: 20.0 },
    { method: "Credit Card", count: 920, volume: 325400.00, percentage: 18.0 },
    { method: "Debit Card", count: 511, volume: 174200.00, percentage: 10.0 },
    { method: "Wallet", count: 360, volume: 120210.97, percentage: 7.0 }
  ],
  order_status_distribution: [
    { status: "Delivered", count: 4330, percentage: 84.67 },
    { status: "Cancelled", count: 503, percentage: 9.84 },
    { status: "Pending", count: 281, percentage: 5.49 }
  ],
  top_restaurants: [
    { restaurant_name: "Paradise Biryani", revenue: 84520.00, orders: 198, avg_rating: 4.6 },
    { restaurant_name: "Domino's Pizza", revenue: 81200.00, orders: 192, avg_rating: 4.5 },
    { restaurant_name: "Punjab Grill", revenue: 78400.00, orders: 184, avg_rating: 4.7 },
    { restaurant_name: "Behrouz Biryani", revenue: 76500.00, orders: 179, avg_rating: 4.5 },
    { restaurant_name: "Burger King", revenue: 74200.00, orders: 181, avg_rating: 4.4 },
    { restaurant_name: "Mainland China", revenue: 72100.00, orders: 172, avg_rating: 4.6 },
    { restaurant_name: "Pizza Hut", revenue: 70800.00, orders: 168, avg_rating: 4.3 },
    { restaurant_name: "McDonald's", revenue: 69500.00, orders: 174, avg_rating: 4.4 },
    { restaurant_name: "Barbeque Nation", revenue: 68100.00, orders: 165, avg_rating: 4.5 },
    { restaurant_name: "KFC", revenue: 65400.00, orders: 160, avg_rating: 4.3 }
  ],
  daily_orders: [
    { date: "2024-12-18", orders: 28, revenue: 11450.00 },
    { date: "2024-12-19", orders: 31, revenue: 12900.00 },
    { date: "2024-12-20", orders: 35, revenue: 14600.00 },
    { date: "2024-12-21", orders: 42, revenue: 17800.00 },
    { date: "2024-12-22", orders: 45, revenue: 19200.00 },
    { date: "2024-12-23", orders: 33, revenue: 13500.00 },
    { date: "2024-12-24", orders: 38, revenue: 16100.00 },
    { date: "2024-12-25", orders: 48, revenue: 21300.00 },
    { date: "2024-12-26", orders: 34, revenue: 14200.00 },
    { date: "2024-12-27", orders: 37, revenue: 15400.00 },
    { date: "2024-12-28", orders: 44, revenue: 18600.00 },
    { date: "2024-12-29", orders: 46, revenue: 19800.00 },
    { date: "2024-12-30", orders: 39, revenue: 16500.00 },
    { date: "2024-12-31", orders: 52, revenue: 22800.00 }
  ],
  peak_hours: [
    { hour: "08:00", orders: 95 },
    { hour: "09:00", orders: 120 },
    { hour: "10:00", orders: 145 },
    { hour: "11:00", orders: 190 },
    { hour: "12:00", orders: 420 },
    { hour: "13:00", orders: 530 },
    { hour: "14:00", orders: 460 },
    { hour: "15:00", orders: 210 },
    { hour: "16:00", orders: 180 },
    { hour: "17:00", orders: 215 },
    { hour: "18:00", orders: 290 },
    { hour: "19:00", orders: 620 },
    { hour: "20:00", orders: 740 },
    { hour: "21:00", orders: 610 },
    { hour: "22:00", orders: 480 },
    { hour: "23:00", orders: 220 }
  ],
  top_customers: [
    { customer_id: "CUST_0142", city: "Mumbai", orders: 14, total_spent: 6120.00 },
    { customer_id: "CUST_0588", city: "Delhi", orders: 13, total_spent: 5840.00 },
    { customer_id: "CUST_0231", city: "Bangalore", orders: 12, total_spent: 5410.00 },
    { customer_id: "CUST_0089", city: "Hyderabad", orders: 12, total_spent: 5280.00 },
    { customer_id: "CUST_0714", city: "Pune", orders: 11, total_spent: 4950.00 },
    { customer_id: "CUST_0344", city: "Chennai", orders: 11, total_spent: 4720.00 },
    { customer_id: "CUST_0492", city: "Kolkata", orders: 10, total_spent: 4560.00 },
    { customer_id: "CUST_0177", city: "Ahmedabad", orders: 10, total_spent: 4390.00 },
    { customer_id: "CUST_0625", city: "Mumbai", orders: 9, total_spent: 4120.00 },
    { customer_id: "CUST_0055", city: "Delhi", orders: 9, total_spent: 3980.00 }
  ],
  top_items: [
    { item_name: "Pepperoni Feast", category: "Pizza", total_quantity: 412 },
    { item_name: "Hyderabadi Chicken Biryani", category: "Biryani", total_quantity: 398 },
    { item_name: "Double Whopper", category: "Burger", total_quantity: 382 },
    { item_name: "Butter Chicken", category: "Indian", total_quantity: 365 },
    { item_name: "Margherita Pizza", category: "Pizza", total_quantity: 350 },
    { item_name: "Veg Hakka Noodles", category: "Chinese", total_quantity: 341 },
    { item_name: "Crispy Chicken Bucket", category: "Fast Food", total_quantity: 335 },
    { item_name: "Paneer Butter Masala", category: "Indian", total_quantity: 320 },
    { item_name: "Belgian Chocolate Waffle", category: "Desserts", total_quantity: 310 },
    { item_name: "Cold Coffee with Ice Cream", category: "Beverages", total_quantity: 295 }
  ],
  delivery_speed_performance: [
    { speed_bracket: "Ultra Fast (<= 25m)", orders: 1180, avg_rating: 4.82 },
    { speed_bracket: "On Time (26-40m)", orders: 2150, avg_rating: 4.46 },
    { speed_bracket: "Moderate (41-55m)", orders: 860, avg_rating: 3.85 },
    { speed_bracket: "Delayed (> 55m)", orders: 140, avg_rating: 2.15 }
  ]
};

// Global Chart Defaults for Dark Cybernetic Theme
Chart.defaults.color = "#94a3b8";
Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.plugins.tooltip.backgroundColor = "rgba(15, 23, 42, 0.92)";
Chart.defaults.plugins.tooltip.titleColor = "#f8fafc";
Chart.defaults.plugins.tooltip.bodyColor = "#cbd5e1";
Chart.defaults.plugins.tooltip.borderColor = "rgba(255, 255, 255, 0.1)";
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.plugins.tooltip.cornerRadius = 8;

document.addEventListener("DOMContentLoaded", () => {
  initModal();
  loadDashboardData();

  document.getElementById("btn-refresh").addEventListener("click", () => {
    loadDashboardData();
  });
});

async function loadDashboardData() {
  try {
    const res = await fetch("data.json");
    if (!res.ok) throw new Error("Could not load data.json");
    const data = await res.json();
    renderAll(data);
  } catch (err) {
    console.warn("Using fallback analytical dataset:", err);
    renderAll(fallbackData);
  }
}

function renderAll(data) {
  renderKPIs(data.kpis);
  renderCharts(data);
  renderTables(data);
}

// -----------------------------------------------------------------------------
// Render 8 Primary Executive KPIs
// -----------------------------------------------------------------------------
function renderKPIs(kpis) {
  if (!kpis) return;
  document.getElementById("kpi-total-orders").textContent = kpis.total_orders.toLocaleString();
  document.getElementById("kpi-total-revenue").textContent = "₹" + kpis.total_revenue.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  document.getElementById("kpi-total-customers").textContent = kpis.unique_customers.toLocaleString();
  document.getElementById("kpi-total-restaurants").textContent = kpis.unique_restaurants.toLocaleString();
  document.getElementById("kpi-aov").textContent = "₹" + kpis.average_order_value.toFixed(2);
  document.getElementById("kpi-delivery-time").textContent = kpis.average_delivery_time_mins.toFixed(1) + " m";
  document.getElementById("kpi-cancellation-rate").textContent = kpis.cancellation_rate_pct.toFixed(2) + "%";
  document.getElementById("kpi-rating").textContent = kpis.average_rating.toFixed(2) + " ★";
}

// -----------------------------------------------------------------------------
// Render 8 Analytics Charts
// -----------------------------------------------------------------------------
function renderCharts(data) {
  destroyCharts();

  // 1. Monthly Revenue Trend
  const ctxMonth = document.getElementById("chart-monthly-revenue").getContext("2d");
  const monthLabels = data.monthly_revenue.map(d => d.month);
  const monthRevs = data.monthly_revenue.map(d => d.revenue);

  const gradientBlue = ctxMonth.createLinearGradient(0, 0, 0, 300);
  gradientBlue.addColorStop(0, "rgba(59, 130, 246, 0.45)");
  gradientBlue.addColorStop(1, "rgba(59, 130, 246, 0.0)");

  charts.monthly = new Chart(ctxMonth, {
    type: "line",
    data: {
      labels: monthLabels,
      datasets: [{
        label: "Monthly Revenue (₹)",
        data: monthRevs,
        borderColor: "#3b82f6",
        borderWidth: 2.5,
        backgroundColor: gradientBlue,
        fill: true,
        tension: 0.35,
        pointBackgroundColor: "#60a5fa",
        pointBorderColor: "#fff",
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          grid: { color: "rgba(255, 255, 255, 0.04)" },
          ticks: {
            callback: v => "₹" + (v / 1000).toFixed(0) + "k"
          }
        },
        x: { grid: { display: false } }
      }
    }
  });

  // 2. Orders by Food Category
  const ctxCat = document.getElementById("chart-food-category").getContext("2d");
  charts.category = new Chart(ctxCat, {
    type: "doughnut",
    data: {
      labels: data.category_performance.map(d => d.category),
      datasets: [{
        data: data.category_performance.map(d => d.orders),
        backgroundColor: [
          "#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b",
          "#10b981", "#06b6d4", "#f43f5e", "#6366f1"
        ],
        borderWidth: 1,
        borderColor: "#0f172a"
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { boxWidth: 12, padding: 8 } }
      },
      cutout: "68%"
    }
  });

  // 3. Revenue by City
  const ctxCity = document.getElementById("chart-city-revenue").getContext("2d");
  charts.city = new Chart(ctxCity, {
    type: "bar",
    data: {
      labels: data.city_performance.map(d => d.city),
      datasets: [{
        label: "Revenue (₹)",
        data: data.city_performance.map(d => d.revenue),
        backgroundColor: "rgba(139, 92, 246, 0.75)",
        borderColor: "#8b5cf6",
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: "y",
      scales: {
        x: {
          grid: { color: "rgba(255, 255, 255, 0.04)" },
          ticks: { callback: v => "₹" + (v / 1000).toFixed(0) + "k" }
        },
        y: { grid: { display: false } }
      }
    }
  });

  // 4. Payment Method Distribution
  const ctxPay = document.getElementById("chart-payment-methods").getContext("2d");
  charts.payment = new Chart(ctxPay, {
    type: "pie",
    data: {
      labels: data.payment_methods.map(d => d.method),
      datasets: [{
        data: data.payment_methods.map(d => d.count),
        backgroundColor: ["#10b981", "#f59e0b", "#3b82f6", "#8b5cf6", "#06b6d4"],
        borderColor: "#0f172a",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "right", labels: { boxWidth: 12, padding: 8 } }
      }
    }
  });

  // 5. Order Status Distribution
  const ctxStatus = document.getElementById("chart-order-status").getContext("2d");
  charts.status = new Chart(ctxStatus, {
    type: "doughnut",
    data: {
      labels: data.order_status_distribution.map(d => d.status),
      datasets: [{
        data: data.order_status_distribution.map(d => d.count),
        backgroundColor: ["#10b981", "#f43f5e", "#f59e0b"],
        borderColor: "#0f172a",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "70%",
      plugins: {
        legend: { position: "bottom", labels: { boxWidth: 12, padding: 12 } }
      }
    }
  });

  // 6. Top 10 Restaurants by Revenue
  const ctxRest = document.getElementById("chart-top-restaurants").getContext("2d");
  charts.restaurants = new Chart(ctxRest, {
    type: "bar",
    data: {
      labels: data.top_restaurants.map(d => d.restaurant_name),
      datasets: [{
        label: "Revenue (₹)",
        data: data.top_restaurants.map(d => d.revenue),
        backgroundColor: "rgba(59, 130, 246, 0.7)",
        borderColor: "#3b82f6",
        borderWidth: 1,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          grid: { color: "rgba(255, 255, 255, 0.04)" },
          ticks: { callback: v => "₹" + (v / 1000).toFixed(0) + "k" }
        },
        x: {
          grid: { display: false },
          ticks: { maxRotation: 35, minRotation: 25 }
        }
      }
    }
  });

  // 7. Daily Orders
  const ctxDaily = document.getElementById("chart-daily-orders").getContext("2d");
  charts.daily = new Chart(ctxDaily, {
    type: "bar",
    data: {
      labels: data.daily_orders.map(d => d.date.slice(5)),
      datasets: [{
        label: "Daily Orders",
        data: data.daily_orders.map(d => d.orders),
        backgroundColor: "rgba(16, 185, 129, 0.7)",
        borderColor: "#10b981",
        borderWidth: 1,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { grid: { color: "rgba(255, 255, 255, 0.04)" } },
        x: { grid: { display: false } }
      }
    }
  });

  // 8. Peak Ordering Hours
  const ctxHours = document.getElementById("chart-peak-hours").getContext("2d");
  const hourColors = data.peak_hours.map(d => {
    const hr = parseInt(d.hour);
    // Highlight peak lunch (12-14) and peak dinner (19-21)
    if ((hr >= 12 && hr <= 14) || (hr >= 19 && hr <= 21)) {
      return "#f59e0b";
    }
    return "rgba(148, 163, 184, 0.4)";
  });

  charts.hours = new Chart(ctxHours, {
    type: "bar",
    data: {
      labels: data.peak_hours.map(d => d.hour),
      datasets: [{
        label: "Hourly Orders",
        data: data.peak_hours.map(d => d.orders),
        backgroundColor: hourColors,
        borderRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { grid: { color: "rgba(255, 255, 255, 0.04)" } },
        x: { grid: { display: false } }
      }
    }
  });
}

function destroyCharts() {
  Object.values(charts).forEach(chart => {
    if (chart && typeof chart.destroy === "function") chart.destroy();
  });
  charts = {};
}

// -----------------------------------------------------------------------------
// Render Deep-Dive Data Tables
// -----------------------------------------------------------------------------
function renderTables(data) {
  // 1. Top Customers
  const custTbody = document.querySelector("#table-top-customers tbody");
  if (custTbody && data.top_customers) {
    custTbody.innerHTML = data.top_customers.map(c => `
      <tr>
        <td><strong>${c.customer_id}</strong></td>
        <td>${c.city}</td>
        <td>${c.orders}</td>
        <td>₹${c.total_spent.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
      </tr>
    `).join("");
  }

  // 2. Top Food Items
  const itemsTbody = document.querySelector("#table-top-items tbody");
  if (itemsTbody && data.top_items) {
    itemsTbody.innerHTML = data.top_items.map(it => `
      <tr>
        <td><strong>${it.item_name}</strong></td>
        <td><span class="tag">${it.category}</span></td>
        <td>${it.total_quantity} pcs</td>
      </tr>
    `).join("");
  }

  // 3. Delivery Speed Brackets
  const speedTbody = document.querySelector("#table-delivery-speed tbody");
  if (speedTbody && data.delivery_speed_performance) {
    speedTbody.innerHTML = data.delivery_speed_performance.map(s => `
      <tr>
        <td><strong>${s.speed_bracket}</strong></td>
        <td>${s.orders}</td>
        <td><span class="badge-status badge-active">${s.avg_rating} ★</span></td>
      </tr>
    `).join("");
  }
}

// -----------------------------------------------------------------------------
// Modal Interaction
// -----------------------------------------------------------------------------
function initModal() {
  const modal = document.getElementById("cluster-modal");
  const btnOpen = document.getElementById("btn-docker-info");
  const btnClose = document.getElementById("btn-close-modal");

  btnOpen.addEventListener("click", () => {
    modal.classList.add("active");
  });

  btnClose.addEventListener("click", () => {
    modal.classList.remove("active");
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.remove("active");
  });
}
