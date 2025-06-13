# 📊 s3lens-etl-project

AWS Lambda ETL pipeline with S3, RDS (optional), Athena, and QuickSight visualization.

---

## 🛠 Tech Stack
- **AWS S3** – Raw and cleaned data storage
- **AWS Lambda (Python)** – Serverless transformation pipeline
- **Amazon RDS (MySQL)** – Optional data persistence layer
- **Amazon Athena** – SQL querying over cleaned data in S3
- **Amazon QuickSight** – Business Intelligence visualizations

---

## 📂 Project Structure

```bash
├── input/                   # Raw input CSVs (orders, products, customers)
├── main-code/              # Lambda function script for ETL
├── output_cleaned_files/   # Final transformed files
├── athena_queries/         # Athena SQL queries for analysis
├── quicksight_screenshots/ # Visual proofs of dashboards
├── README.md               # You’re here!
