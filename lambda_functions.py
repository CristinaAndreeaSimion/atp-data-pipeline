import os
import io
import boto3
import pandas as pd
from datetime import datetime

s3 = boto3.client('s3')

INPUT_KEY = "local_test.csv"
BUCKET_NAME = "" 

def read_csv_from_s3(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(io.BytesIO(obj['Body'].read()), low_memory=False)

def compute_top50(df):
    """Calculeaza Top 50 jucatori pe baza datasetului cu coloane"""
    
    # Normalizeaza datele
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Winner'] = df['Winner'].astype(str)

    # Calcul total victorii
    wins = df.groupby('Winner').agg(
        total_wins=pd.NamedAgg(column='Winner', aggfunc='count'),
        first_win=pd.NamedAgg(column='Date', aggfunc='min'),
        last_win=pd.NamedAgg(column='Date', aggfunc='max')
    ).reset_index()

    # Filtrare dupa tipuri de turnee
    # Grand Slam-urile reale
    gs_names = ['Australian Open', 'French Open', 'Wimbledon', 'US Open']
    df['is_gs'] = df['Tournament'].isin(gs_names)
    gs = df[df['is_gs']].groupby('Winner').size().reset_index(name='grand_slam_wins')

    # ATP1000 (Masters)
    atp1000_keywords = ['Masters', 'Monte Carlo', 'Rome', 'Madrid', 'Cincinnati', 'Shanghai', 'Canada']
    df['is_1000'] = df['Tournament'].apply(lambda x: any(k in str(x) for k in atp1000_keywords))
    atp1000 = df[df['is_1000']].groupby('Winner').size().reset_index(name='atp1000_wins')

    # ATP500
    atp500_keywords = ['Rotterdam', 'Dubai', 'Rio', 'Barcelona', 'Hamburg', 'Beijing', 'Tokyo']
    df['is_500'] = df['Tournament'].apply(lambda x: any(k in str(x) for k in atp500_keywords))
    atp500 = df[df['is_500']].groupby('Winner').size().reset_index(name='atp500_wins')

    # Join intre tabele
    result = wins.merge(gs, on='Winner', how='left')
    result = result.merge(atp1000, on='Winner', how='left')
    result = result.merge(atp500, on='Winner', how='left')

    # Completeaza valorile lipsa cu 0
    for col in ['grand_slam_wins', 'atp1000_wins', 'atp500_wins']:
        result[col] = result[col].fillna(0).astype(int)

    # Selecteaza si sorteaza top 50
    result = result.rename(columns={'Winner': 'player_name'})
    result = result.sort_values(by='total_wins', ascending=False).head(50)

    # Formateaza datele
    result['first_win'] = result['first_win'].dt.date.astype(str)
    result['last_win'] = result['last_win'].dt.date.astype(str)

    # Ordine finala a coloanelor
    cols = ['player_name', 'total_wins', 'grand_slam_wins',
            'atp1000_wins', 'atp500_wins', 'first_win', 'last_win']
    return result[cols]

def write_csv_to_s3(df, bucket):
    
    now = datetime.utcnow().strftime("%d-%m-%Y")
    key = f"results/atp-top-50-{now}.csv"
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue().encode('utf-8'))
    return key

def lambda_handler(event, context):
    """Punctul principal de intrare pentru AWS Lambda"""
    print("Starting ATP Top 50 analysis...")
    df = read_csv_from_s3(BUCKET_NAME, INPUT_KEY)
    top50 = compute_top50(df)
    key = write_csv_to_s3(top50, BUCKET_NAME)
    print(f"Fisier generat: s3://{BUCKET_NAME}/{key}")
    return {"status": "success", "output_file": key}
