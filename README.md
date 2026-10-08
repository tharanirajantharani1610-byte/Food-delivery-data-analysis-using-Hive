# Food Delivery Data Analysis Using Apache Hive with Docker

> **Academic Big Data Engineering & Analytics Project**  
> **Environment:** 100% Docker Desktop (Windows / macOS / Linux) &bull; **Zero Local Hadoop Installation**

---

## 1. Abstract
The rapid expansion of on-demand food delivery platforms has led to exponential growth in order transaction records, customer engagement metrics, and logistics telemetry. Analyzing these massive volumes of semi-structured and structured data requires robust, distributed Big Data infrastructure. This project presents an enterprise-grade Big Data solution titled **"Food Delivery Data Analysis Using Apache Hive with Docker"**. Utilizing **Docker Desktop** as the exclusive runtime environment, the architecture orchestrates **Apache Hive (HiveServer2 & Metastore)**, a **PostgreSQL Metastore database**, and underlying **Hadoop HDFS (NameNode & DataNode)** microservices without requiring any manual Hadoop configuration on the host Windows machine. 

A realistic food delivery dataset comprising 5,200+ orders across 8 major Indian metropolises, 8 cuisine categories, and diverse payment gateways is ingested. An automated **Extract, Transform, Load (ETL)** pipeline cleanses invalid records, handles NULL values, standardizes categories, calculates order financials, and deduplicates records into an optimized columnar **ORC (Optimized Row Columnar)** format with Snappy compression. A suite of **30 analytical HiveQL queries** extracts operational, geographic, and financial intelligence. The extracted insights are converted via Python and visualized through a high-performance, dark-themed **Web Analytics Dashboard**.

---

## 2. Introduction
Modern food delivery ecosystems (e.g., Swiggy, Zomato, DoorDash, Uber Eats) process millions of food orders daily. Extracting actionable insights—such as peak ordering hours, high-revenue culinary categories, cancellation patterns, and delivery speed benchmarks—demands distributed SQL query engines capable of scaling to petabytes. 

**Apache Hive** provides an SQL abstraction layer (HiveQL) over distributed storage engines (HDFS). However, configuring Hadoop, Winutils, Java paths, and Metastore daemons natively on Windows is notoriously error-prone. This project eliminates host environment friction by deploying a fully encapsulated, multi-container Docker cluster using **Docker Compose**.

---

## 3. Problem Statement
Traditional relational databases (RDBMS) struggle with horizontal scalability, schema evolution, and cost-effective analytical processing of large-scale delivery logs. Conversely, setting up distributed Big Data frameworks like Hadoop and Hive directly on local development machines poses significant barriers:
1. Complex dependency trees (Java, Hadoop binaries, native Windows DLLs, Winutils).
2. Metastore database initialization and JDBC connection failures.
3. Lack of portability between development, staging, and evaluation environments.

**Solution:** Implement an isolated, declarative, multi-container Big Data stack managed via Docker Compose that provides instant reproducibility, automated volume persistence, and seamless execution of Big Data ETL and analytical queries.

---

## 4. Project Objectives
* **Zero Host Installation:** Run Apache Hive, Hive Metastore, PostgreSQL, and HDFS entirely within Docker containers.
* **Realistic Data Ingestion:** Process a 5,000+ record delivery dataset featuring real-world anomalies (inconsistent casing, negative numbers, missing fields, duplicates).
* **Robust Hive ETL Pipeline:** Implement HiveQL data transformation logic to deduplicate, validate, sanitize, and compute derived financial fields (`total_amount = quantity * price + delivery_fee - discount`).
* **Advanced HiveQL Analytics:** Execute 30 specialized analytical queries covering executive KPIs, geographic revenue, logistics performance, and customer segmentation.
* **Result Serialization & Visualization:** Export analytical outputs to structured JSON via Python and present them on an interactive, responsive web dashboard built with HTML5, CSS3, and Chart.js.

---

## 5. Scope of the Project
* **Functional Scope:**
  * Extraction of transactional food delivery logs.
  * Schema-on-read staging in Hive raw tables.
  * In-database HiveQL ETL transformations.
  * Partition-aware columnar storage using Apache ORC format.
  * Business intelligence aggregation and metric computation.
  * Modern frontend dashboard visualization with dynamic charts and KPI cards.
* **Non-Functional Scope:** High data integrity, deterministic ETL reproducibility, zero host machine configuration pollution.

---

## 6. System Architecture

```
+-----------------------------------------------------------------------------------------------+
|                                    WINDOWS HOST SYSTEM                                        |
|  [data/food_delivery.csv]  <-- Host Bind Mount -->  [hive/*.sql Scripts]                      |
+----------------------------------------|------------------------------------------------------+
                                         | Docker Virtual Volume Binds
                                         v
+-----------------------------------------------------------------------------------------------+
|                                DOCKER DESKTOP VIRTUAL NETWORK                                 |
|                                                                                               |
|   +-----------------------+              +-----------------------+                            |
|   |   HDFS NameNode       | <==========> |   HDFS DataNode       |   (Storage Layer)          |
|   |   Port: 50070         |              |   Port: 50075         |                            |
|   +-----------▲-----------+              +-----------------------+                            |
|               |                                                                               |
|   +-----------┴-----------+              +-------------------------------+                    |
|   |   Hive Metastore      | <==========> |   hive-metastore-postgresql   |   (Catalog Layer)  |
|   |   Port: 9083          |              |   Port: 5432 (Postgres 9/11)  |                    |
|   +-----------▲-----------+              +-------------------------------+                    |
|               |                                                                               |
|   +-----------┴----------------------------------------------------------+                    |
|   |   hive-server (HiveServer2 & Hive Interactive CLI Engine)            |   (Compute Layer)  |
|   |   Ports: 10000 (JDBC/Thrift), 10002 (Web UI)                         |                    |
|   |   Mounted: /opt/data & /opt/hive-scripts                             |                    |
|   +----------------------------------------------------------------------+                    |
+-----------------------------------------------------------------------------------------------+
                                         |
                                         v
                        [scripts/export_results.py]
                                         |
                                         v
                        [dashboard/data.json]
                                         |
                                         v
               [dashboard/index.html & Chart.js Web Dashboard]
```

### Architectural Clarification: Hadoop & HDFS in Docker
* **No Host Hadoop:** You do **not** install Hadoop or configure environment variables (`HADOOP_HOME`, `HADOOP_CONF_DIR`) on Windows.
* **Internal Docker Subsystem:** Apache Hive requires a distributed filesystem for table data. In this project, HDFS NameNode (`namenode`) and DataNode (`datanode`) run as autonomous background services **inside Docker**.
* **Zero Host HDFS Configuration:** All filesystem coordination is handled via Docker Compose networking (`hive-network`).

---

## 7. Technologies Used

| Technology | Layer / Purpose | Version |
| :--- | :--- | :--- |
| **Docker Desktop** | Containerization runtime & service orchestration | 20+ / 29+ |
| **Docker Compose** | Multi-container declarative specification | v2.x / v5.x |
| **Apache Hive** | Distributed SQL Data Warehousing & ETL Engine | 2.3.2 |
| **PostgreSQL** | Relational catalog for Hive Metastore | 2.3.0 |
| **Hadoop HDFS** | Containerized distributed storage backing Hive | 2.7.4 |
| **Python** | Dataset synthesis, pipeline execution, result JSON exporter | 3.10+ / 3.13+ |
| **HiveQL** | SQL dialect for schema definition, ETL & analytical queries | ANSI HiveQL |
| **HTML5 & CSS3** | Custom cybernetic glassmorphism dashboard UI | Semantic / Vanilla |
| **JavaScript (ES6+)** | Dynamic data binding, DOM manipulation, async fetch | Native ES6 |
| **Chart.js** | Interactive data visualization library | 4.x CDN |

---

## 8. Hardware & Software Requirements

### Hardware Requirements
* **Processor:** Intel Core i5 / AMD Ryzen 5 or higher (x86_64 / ARM64 with virtualization support enabled).
* **RAM:** Minimum 8 GB (16 GB recommended for running multi-container Docker workloads).
* **Storage:** 10 GB free disk space.

### Software Requirements
* **Operating System:** Windows 10/11 (64-bit) with WSL 2 enabled, or macOS / Linux.
* **Container Runtime:** Docker Desktop installed and running.
* **Scripting Runtime:** Python 3.8+ (standard library only; no external package dependencies required).
* **Browser:** Modern web browser (Chrome, Edge, Firefox).

---

## 9. Project Directory Structure

```text
FoodDeliveryHiveProject/
│
├── docker-compose.yml       # Multi-container Docker configuration
│
├── data/                    # Dataset directory (mounted to /opt/data)
│   └── food_delivery.csv    # 5,200+ transactional records with edge cases
│
├── hive/                    # HiveQL scripts (mounted to /opt/hive-scripts)
│   ├── database.sql         # Database creation script (food_delivery_db)
│   ├── tables.sql           # Raw staging and cleaned ORC tables
│   ├── etl.sql              # Extract, Transform, Validate, and Load pipeline
│   └── analysis.sql         # 30 Comprehensive analytical queries
│
├── scripts/                 # Automation scripts
│   ├── generate_data.py     # Realistic synthetic dataset generator
│   └── export_results.py    # Analytical calculation & JSON exporter
│
├── dashboard/               # Frontend interactive visualization
│   ├── index.html           # Dashboard layout & executive KPI cards
│   ├── style.css            # Custom dark cybernetic glassmorphism styling
│   ├── script.js            # Chart.js rendering & data binding logic
│   └── data.json            # Structured analytical JSON payload
│
└── README.md                # Comprehensive documentation
```

---

## 10. Dataset Specifications

The dataset in `data/food_delivery.csv` contains 5,200+ realistic records with the following schema:

| Column | Data Type | Description |
| :--- | :--- | :--- |
| `order_id` | STRING | Unique alphanumeric order identifier (`ORD_00001`) |
| `customer_id` | STRING | Unique customer identifier (`CUST_0142`) |
| `restaurant_id` | STRING | Unique restaurant identifier (`REST_109`) |
| `restaurant_name` | STRING | Restaurant brand name (e.g., Domino's Pizza, Paradise Biryani) |
| `customer_city` | STRING | Customer location (Mumbai, Delhi, Bangalore, Hyderabad, etc.) |
| `order_date` | STRING | Date of purchase (`YYYY-MM-DD`) |
| `order_time` | STRING | Time of purchase (`HH:MM:SS`) |
| `food_category` | STRING | Food classification (Pizza, Burger, Biryani, Indian, etc.) |
| `item_name` | STRING | Specific menu dish (e.g., Margherita Pizza, Butter Chicken) |
| `quantity` | INT | Number of units ordered |
| `price` | DOUBLE | Unit price of the item |
| `delivery_fee` | DOUBLE | Delivery surcharge |
| `discount` | DOUBLE | Applied promotional discount |
| `payment_method` | STRING | Gateway used (UPI, Cash, Credit Card, Debit Card, Wallet) |
| `order_status` | STRING | Fulfillment status (Delivered, Cancelled, Pending) |
| `delivery_time_minutes`| INT | Elapsed transit duration (minutes) |
| `customer_rating` | DOUBLE | Rating provided (1.0 to 5.0 stars) |

*Intentional Dirty Data Injected:* ~3.5% anomalous records (missing customer IDs, negative prices, zero quantities, mixed casing, and 40 duplicate order IDs) to rigorously demonstrate the Hive ETL transformation.

---

## 11. Complete Hive ETL Pipeline

### Extract
Ingests the raw CSV directly from host-mounted `/opt/data/food_delivery.csv` into the staging table `food_delivery_raw`:
```sql
LOAD DATA LOCAL INPATH '/opt/data/food_delivery.csv' OVERWRITE INTO TABLE food_delivery_raw;
```

### Transform
* **Deduplication:** Utilizes `ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY order_date DESC)` to eliminate duplicate orders.
* **Data Validation:** Enforces `price > 0`, `quantity > 0`, and `delivery_time_minutes >= 0`.
* **Null Handling:** Cleans blank/NULL identifiers; substitutes default values using `COALESCE`.
* **Standardization:** Normalizes casing for food categories (`CASE WHEN LOWER(...) ...`), payment gateways, and delivery statuses.
* **Derived Financial Metric:** Computes total order value:
  $$\text{total\_amount} = (\text{quantity} \times \text{price}) + \text{delivery\_fee} - \text{discount}$$

### Load
Populates the cleansed dataset into `food_delivery_cleaned`, stored in Snappy-compressed **ORC format** for columnar scan acceleration.

---

## 12. 30 HiveQL Analytical Queries Overview

The file `hive/analysis.sql` contains the complete queries matching the schema:
1. **Total Orders:** Count of all processed records.
2. **Total Revenue:** Gross revenue from delivered orders.
3. **Average Order Value (AOV):** Mean transaction ticket size.
4. **Unique Customers:** Distinct active user accounts.
5. **Unique Restaurants:** Count of distinct restaurant partners.
6. **Most Popular Food Category:** Top category by order volume.
7. **Most Ordered Food Item:** Menu dish with highest unit sales.
8. **Top 10 Restaurants:** Highest grossing restaurant brands.
9. **Top 10 Customers:** Highest spenders across all cities.
10. **Revenue by City:** Geographic breakdown of orders and delivery speeds.
11. **Revenue by Food Category:** Cuisine profitability comparison.
12. **Monthly Revenue:** Month-over-month sales progression.
13. **Daily Order Count:** Daily demand trends.
14. **Orders by Payment Method:** Transaction volume and gateway shares.
15. **Delivered Orders Count:** Total successfully delivered orders.
16. **Cancelled Orders Count:** Total aborted transactions.
17. **Cancellation Rate (%):** Overall platform churn rate.
18. **Average Delivery Time:** Mean delivery duration in minutes.
19. **Average Customer Rating:** Mean platform satisfaction score.
20. **Peak Ordering Hour:** Hourly traffic distribution (lunch vs dinner).
21. **Best-Rated Restaurants:** Top rated establishments with &ge;30 orders.
22. **Highest Revenue City:** Prime geographical market.
23. **Discount Analysis:** Orders categorized by discount brackets.
24. **Delivery Performance:** Delivery speed brackets vs customer satisfaction.
25. **Customer Spending Analysis:** Customer segmentation (VIP, Regular, Occasional).
26. **Monthly Growth Rate:** Month-over-month revenue percentage growth using `LAG()`.
27. **Food Category Performance:** Quantity vs revenue matrix by cuisine.
28. **Restaurant Order vs Revenue:** Average revenue generated per restaurant order.
29. **Payment Method Analysis:** Ticket size variance across payment methods.
30. **Executive Business Summary:** Multi-metric single-row executive summary.

---

## 13. Step-by-Step Windows Execution Guide

### Prerequisites
1. Ensure **Docker Desktop** is running on Windows (look for the whale icon in the system tray).
2. Open **PowerShell** or **Command Prompt** in this project directory:
   ```powershell
   cd "c:\Users\Tharani Rajan\OneDrive\Desktop\Food delivery data analysis using Hive"
   ```

### Step 1: Generate the Dataset
```powershell
python scripts/generate_data.py
```
*(Creates 5,200+ records in `data/food_delivery.csv`)*

### Step 2: Launch the Docker Hive Cluster
```powershell
docker compose up -d
```

Verify that all 5 containers are running:
```powershell
docker compose ps
```
*Expected services:* `hive-server`, `hive-metastore`, `hive-metastore-postgresql`, `namenode`, `datanode`.

### Step 3: Execute Hive Database & Table Setup
Run the SQL scripts inside the container using volume mounts:
```powershell
# 1. Create Database
docker exec -i hive-server hive -f /opt/hive-scripts/database.sql

# 2. Create Raw Staging & Cleaned Production Tables
docker exec -i hive-server hive -f /opt/hive-scripts/tables.sql

# 3. Execute Complete ETL Pipeline
docker exec -i hive-server hive -f /opt/hive-scripts/etl.sql
```

### Step 4: Run HiveQL Analytical Queries
```powershell
docker exec -i hive-server hive -f /opt/hive-scripts/analysis.sql
```

*Optional: Access the interactive Hive CLI terminal:*
```powershell
docker exec -it hive-server hive
```
Inside the interactive prompt, you can run any HiveQL query directly:
```sql
USE food_delivery_db;
SELECT customer_city, count(*), sum(total_amount) FROM food_delivery_cleaned GROUP BY customer_city;
exit;
```

### Step 5: Export Results for Web Dashboard
```powershell
python scripts/export_results.py
```
*(Generates `dashboard/data.json`)*

### Step 6: Launch Web Dashboard
Open `dashboard/index.html` in your browser, or start a lightweight local web server:
```powershell
python -m http.server 8080 --directory dashboard
```
Then navigate to: **`http://localhost:8080`**

### Step 7: Stop the Docker Cluster
When you are finished:
```powershell
docker compose down
```

---

## 14. Comprehensive Troubleshooting Matrix

| Problem | Root Cause | Solution | Exact Windows Command |
| :--- | :--- | :--- | :--- |
| **Docker not running** | Docker Desktop application is closed | Launch Docker Desktop from the Start menu | `Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"` |
| **Docker daemon error** | WSL 2 backend or Docker service stopped | Ensure Docker service is active in Windows Services | `Restart-Service *docker*` |
| **Port already in use (5432 / 10000)** | Local PostgreSQL or another service running on port 5432 or 10000 | Stop conflicting local service or change host port mapping in `docker-compose.yml` | `Get-Process -Id (Get-NetTCPConnection -LocalPort 5432).OwningProcess` |
| **Container keeps restarting** | Precondition dependency waiting for database or NameNode | Wait 30 seconds for initial healthcheck handshake | `docker compose logs -f hive-server` |
| **Table does not exist** | Script executed without specifying database context | Ensure `USE food_delivery_db;` precedes queries | `docker exec -i hive-server hive -e "USE food_delivery_db; SHOW TABLES;"` |
| **CSV file not found** | Host volume mount path misconfigured or CSV not generated | Run `python scripts/generate_data.py` to recreate `data/food_delivery.csv` | `docker exec -it hive-server ls -la /opt/data` |
| **Hive command not found** | Executing `hive` outside the container on Windows host | Prepend `docker exec -i hive-server` to run inside container | `docker exec -it hive-server hive` |

---

## 15. Advantages & Practical Applications
1. **100% Platform Portability:** No local installation of Hadoop, Winutils, or Java prevents system bloat and "works on my machine" conflicts.
2. **Columnar Storage Optimization:** ORC format with Snappy compression yields up to 75% storage savings and faster aggregation scans compared to raw text CSV.
3. **Decoupled Architecture:** Storage (HDFS), Metadata (PostgreSQL), Compute (HiveServer2), and Visualization (Web UI) operate as independent, maintainable layers.
4. **Actionable Business Intelligence:** Provides real-time metrics on delivery bottlenecks, high-churn customer segments, and revenue-maximizing menu items.

---

## 16. Conclusion
This project successfully demonstrates the design, deployment, and end-to-end execution of a complete Big Data Analytics pipeline using **Apache Hive with Docker**. By eliminating manual Windows Hadoop configuration, the system achieves enterprise-grade reliability and provides rich business intelligence across 5,000+ delivery transactions.
