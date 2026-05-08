import pandas as pd
import os
import numpy as np

RAW_DIR = 'data/raw'
PROCESSED_DIR = 'data/processed'


def get_numeric_series(df, column_name):
    if column_name in df.columns:
        return pd.to_numeric(df[column_name], errors='coerce').fillna(0)
    return pd.Series(0, index=df.index, dtype=float)


def transform_data():
    try:
        print("🚀 Starting Transformation...")
        
        # 1. Load Files (Skipping the top junk rows)
        # Based on your output, we likely need to skip 1 or 2 rows to hit the real headers
        df_pl = pd.read_csv(f'{RAW_DIR}/profit_loss.csv', skiprows=1)
        df_bs = pd.read_csv(f'{RAW_DIR}/balance_sheet.csv', skiprows=1)

        # 2. Standardize Columns (Lowercase + Underscores)
        df_pl.columns = [col.strip().lower().replace(' ', '_') for col in df_pl.columns]
        df_bs.columns = [col.strip().lower().replace(' ', '_') for col in df_bs.columns]

        # 3. P&L Calculations
        print("📊 Calculating P&L Metrics...")
        sales = get_numeric_series(df_pl, 'sales')
        net_profit = get_numeric_series(df_pl, 'net_profit')
        
        # Calculate OPM using NumPy to prevent division errors
        df_pl['opm_percentage'] = np.where(sales != 0, (net_profit / sales) * 100, 0)
        df_pl['opm_percentage'] = df_pl['opm_percentage'].astype(float).round(2)

        # 4. Balance Sheet Calculations
        print("📊 Calculating Balance Sheet Metrics...")
        
        borrowings = get_numeric_series(df_bs, 'borrowings')
        reserves = get_numeric_series(df_bs, 'reserves')
        share_capital = get_numeric_series(df_bs, 'share_capital')
        
        # If share_capital is missing but equity_capital exists, use that instead
        if share_capital.eq(0).all() and 'equity_capital' in df_bs.columns:
            share_capital = get_numeric_series(df_bs, 'equity_capital')

        total_equity = share_capital + reserves

        # Safe division for Debt-to-Equity using np.where
        df_bs['debt_to_equity'] = np.where(
            total_equity != 0,
            borrowings / total_equity,
            0
        )
        df_bs['debt_to_equity'] = df_bs['debt_to_equity'].astype(float).round(2)

        # 5. Save Files
        os.makedirs(PROCESSED_DIR, exist_ok=True)
        df_pl.to_csv(f'{PROCESSED_DIR}/cleaned_pl.csv', index=False)
        df_bs.to_csv(f'{PROCESSED_DIR}/cleaned_bs.csv', index=False)
        
        print("🎉 Success! Processed files saved.")
        print(f"📌 Columns in BS: {list(df_bs.columns)}")

    except Exception as e:
        # This will now catch and print the specific line if it fails
        print(f"❌ Transformation Error: {e}")

if __name__ == "__main__":
    transform_data()