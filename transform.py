import os
import re
import pandas as pd

RAW_DIR = os.path.join('data', 'raw')
PROCESSED_DIR = os.path.join('data', 'processed')
OUTPUT_FILE = os.path.join(PROCESSED_DIR, 'cleaned_financials.csv')


def load_csv(filename):
    path = os.path.join(RAW_DIR, filename)
    return pd.read_csv(path, dtype=str)


def normalize_year(value):
    if pd.isna(value):
        return pd.NA

    text = str(value).strip()
    if not text or text.upper() in {'N/A', 'NA'}:
        return pd.NA

    parsed = pd.to_datetime(text, errors='coerce', infer_datetime_format=True)
    if pd.notna(parsed):
        return parsed.strftime('%b %Y')

    year_match = re.fullmatch(r'(\d{4})', text)
    if year_match:
        return f'Jan {year_match.group(1)}'

    return text


def clean_year_column(df):
    if 'Year' not in df.columns:
        return df

    df['Year'] = df['Year'].apply(normalize_year)
    return df


def replace_nulls(df):
    df = df.replace(['', ' ', 'N/A', 'NA'], pd.NA)
    return df.fillna(0)


def numeric_column(series):
    return pd.to_numeric(series.astype(str).str.replace('[,$%]', '', regex=True), errors='coerce').fillna(0)


def merge_financial_data(pl_df, bs_df, cmp_df):
    merge_keys = ['Year']
    if 'Company' in pl_df.columns and 'Company' in bs_df.columns:
        merge_keys.append('Company')

    merged = pl_df.merge(bs_df, on=merge_keys, how='outer', suffixes=('_pl', '_bs'))

    if 'Company' in cmp_df.columns and 'Company' in merged.columns:
        merged = merged.merge(cmp_df, on=['Company'], how='left')
    else:
        merged = merged.merge(cmp_df, on=merge_keys, how='left', suffixes=('', '_cmp'))

    return merged


def calculate_ratios(df):
    df['Net Profit Margin'] = numeric_column(df.get('Net Profit', 0)) / numeric_column(df.get('Sales', 0))
    debt = numeric_column(df.get('Borrowings', 0))
    equity = numeric_column(df.get('Share Capital', 0)) + numeric_column(df.get('Reserves', 0))
    df['Debt-to-Equity'] = debt / equity.replace(0, pd.NA)
    return df


def main():
    pl_df = load_csv('profitandloss.csv')
    bs_df = load_csv('balancesheet.csv')
    cmp_df = load_csv('companies.csv')

    pl_df = clean_year_column(pl_df)
    bs_df = clean_year_column(bs_df)
    cmp_df = clean_year_column(cmp_df)

    pl_df = replace_nulls(pl_df)
    bs_df = replace_nulls(bs_df)
    cmp_df = replace_nulls(cmp_df)

    financials = merge_financial_data(pl_df, bs_df, cmp_df)
    financials = calculate_ratios(financials)

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    financials.to_csv(OUTPUT_FILE, index=False)
    print(f'Saved cleaned financial data to {OUTPUT_FILE}')


if __name__ == '__main__':
    main()
