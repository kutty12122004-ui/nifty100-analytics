import pandas as pd
from sqlalchemy import create_engine
import os

# Update 'your_password' with the password you set during PostgreSQL installation
DB_URL = "postgresql://postgres:password@localhost:5432/nifty100_db"
PROCESSED_DIR = 'data/processed'

def load_data():
    try:
        print("🔌 Connecting to PostgreSQL...")
        engine = create_engine(DB_URL)
        
        # Load the cleaned files from the Silver Layer
        df_pl = pd.read_csv(f'{PROCESSED_DIR}/cleaned_pl.csv')
        df_bs = pd.read_csv(f'{PROCESSED_DIR}/cleaned_bs.csv')
        
        # Load into SQL
        print("📤 Loading into 'profit_loss' table...")
        df_pl.to_sql('profit_loss', engine, if_exists='replace', index=False)
        
        print("📤 Loading into 'balance_sheet' table...")
        df_bs.to_sql('balance_sheet', engine, if_exists='replace', index=False)
        
        print("🎉 Stream B ETL Pipeline Complete!")
        
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("💡 Tip: Check if your PostgreSQL password is correct in the DB_URL.")

if __name__ == "__main__":
    load_data()