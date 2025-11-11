# 🎾 ATP Weekly Top 50 Player Report – Serverless Data Pipeline

![Python](https://img.shields.io/badge/python-3.13-blue)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900)
![pandas](https://img.shields.io/badge/pandas-2.0+-1572B6)

A **serverless** solution that automatically processes ATP data (2000–2025) and generates a weekly Top 50 Players report, AWS Lambda, S3, EventBridge, and CloudWatch.

✅ Runs automatically every **Monday at 06:00 UTC** 
✅ Zero cost outside of Lambda execution 
✅ Scalable and easy to maintain

---

## 📊 Example output

| player_name     | total_wins | grand_slam_wins | atp1000_wins | atp500_wins | first_win   | last_win    |
|-----------------|------------|------------------|--------------|-------------|-------------|-------------|
| Djokovic N.     | 142        | 24               | 41           | 12          | 2006-04-10  | 2025-02-16  |
| Nadal R.        | 131        | 22               | 26           | 15          | 2003-06-24  | 2024-01-20  |


---

## 🧠 What does the pipeline do?

1. **Download** the ATP dataset (2000–2025) from Kaggle using `kagglehub` 
2. **Upload** the CSV to an S3 bucket (`s3://atp-analysis-cristina-simion/atp_tennis.csv`) 
3. **Run** a Lambda function (Python + pandas):
- calculate total and category wins (GS, ATP1000, ATP500)
- identify first/last win per player
- sort and select **Top 50**
4. **Save** the report to `s3://.../results/atp-top-50-DD-MM-YYYY.csv`
5. **Automatically triggered** with EventBridge (`cron(0 6 ? * MON *)`)
---

## 🛠 Technologies

| Component | Role |
|-----------|-----|
| **AWS Lambda** | Serverless execution of Python logic |
| **Amazon S3** | Input/output storage |
| **EventBridge** | Weekly scheduling (Monday, 06:00 UTC) |
| **CloudWatch** | Logging & troubleshooting |
| **IAM Role** | Minimum permissions: `s3:GetObject`, `PutObject`, `ListBucket` |
| **Python** | `pandas` (processing), `boto3` (S3), `kagglehub` (downloading) |

---

## 🗺 Pipeline Architecture

flowchart TD
    A["EventBridge Rule\n(Mon, 06:00 UTC)"]
    --> B["AWS Lambda\n• Download dataset from Kaggle\n• Read from S3\n• Process with pandas (Top 50)\n• Save results to S3"]
    --> C["S3 Bucket\n• Input: atp_tennis.csv\n• Output: results/*.csv"]
    --> D["CloudWatch Logs\n• Logging & monitoring\n• Troubleshooting"]

---


## ⚙️ Local setup (for testing)

> 🔁 Input data is not included in this repo due to size and licensing reasons. The pipeline automatically downloads it from Kaggle on each run.

For local testing:
1. Install dependencies:
   ```bash
   pip install -r requirements.txt

   
