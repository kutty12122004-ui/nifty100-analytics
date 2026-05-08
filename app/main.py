from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, database

app = FastAPI(title="Nifty 100 Analytics API")

@app.get("/")
def read_root():
    return {"message": "Nifty 100 API is live and connected!"}

@app.get("/financials")
def get_financials(db: Session = Depends(database.get_db)):
    try:
        # 1. Fetch the joined data
        results = db.query(
            models.ProfitLoss.company_id,
            models.ProfitLoss.year,
            models.ProfitLoss.net_profit,
            models.ProfitLoss.opm_percentage,
            models.BalanceSheet.borrowings,
            models.BalanceSheet.debt_to_equity
        ).join(
            models.BalanceSheet,
            and_(
                models.ProfitLoss.company_id == models.BalanceSheet.company_id,
                models.ProfitLoss.year == models.BalanceSheet.year
            )
        ).all()

        # 2. FIX: Convert SQLAlchemy rows to a list of dictionaries for FastAPI
        # This prevents the "dictionary update sequence element" error
        return [
            {
                "company_id": row.company_id,
                "year": row.year,
                "net_profit": row.net_profit,
                "opm_percentage": row.opm_percentage,
                "borrowings": row.borrowings,
                "debt_to_equity": row.debt_to_equity
            } 
            for row in results
        ]

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))