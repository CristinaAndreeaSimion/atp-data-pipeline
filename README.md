# 🎾 ATP Weekly Top 50 Player Report – Serverless Data Pipeline

![Python](https://img.shields.io/badge/python-3.13-blue)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-FF9900)
![pandas](https://img.shields.io/badge/pandas-2.0+-1572B6)

O soluție **serverless** care procesează automat datele ATP (2000–2025) și generează săptămânal un raport Top 50 jucători, folosind AWS Lambda, S3, EventBridge și CloudWatch.

✅ Rulează automat în fiecare **luni la 06:00 UTC**  
✅ Zero cost în afara execuției Lambda  
✅ Scalabil și ușor de întreținut

---

## 📊 Exemplu output

| player_name     | total_wins | grand_slam_wins | atp1000_wins | atp500_wins | first_win   | last_win    |
|-----------------|------------|------------------|--------------|-------------|-------------|-------------|
| Djokovic N.     | 142        | 24               | 41           | 12          | 2006-04-10  | 2025-02-16  |
| Nadal R.        | 131        | 22               | 26           | 15          | 2003-06-24  | 2024-01-20  |

📁 [Vezi fișierul complet (`sample_output/atp-top-50-08-11-2025.csv`)](sample_output/atp-top-50-08-11-2025.csv)

---

## 🧠 Ce face pipeline-ul?

1. **Descarcă** datasetul ATP (2000–2025) de pe Kaggle folosind `kagglehub`  
2. **Încarcă** CSV-ul într-un bucket S3 (`s3://atp-analysis-cristina-simion/atp_tennis.csv`)  
3. **Rulează** o funcție Lambda (Python + pandas):
   - calculează victorii totale și pe categorii (GS, ATP1000, ATP500)
   - identifică prima/ultima victorie per jucător
   - sortează și selectează **Top 50**
4. **Salvează** raportul în `s3://.../results/atp-top-50-DD-MM-YYYY.csv`
5. **Declanșat automat** cu EventBridge (`cron(0 6 ? * MON *)`)

---

## 🛠 Tehnologii

| Componentă | Rol |
|-----------|-----|
| **AWS Lambda** | Execuție serverless a logicii Python |
| **Amazon S3** | Stocare input/output |
| **EventBridge** | Planificare săptămânală (luni, 06:00 UTC) |
| **CloudWatch** | Logging & troubleshooting |
| **IAM Role** | Permisii minime: `s3:GetObject`, `PutObject`, `ListBucket` |
| **Python** | `pandas` (procesare), `boto3` (S3), `kagglehub` (download) |

---

## ⚙️ Configurare locală (pentru test)

> 🔁 Datele de intrare nu sunt incluse în acest repo din motive de dimensiune și licență. Pipeline-ul le descarcă automat de pe Kaggle la fiecare execuție.

Pentru test local:
1. Instalează dependințele:
   ```bash
   pip install -r requirements.txt

   