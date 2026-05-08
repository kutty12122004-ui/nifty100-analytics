from sqlalchemy import Column, Integer, String, Float
from .database import Base

class ProfitLoss(Base):
    __tablename__ = "profit_loss"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, index=True)
    year = Column(Integer)
    net_profit = Column(Float)
    opm_percentage = Column(Float)

class BalanceSheet(Base):
    __tablename__ = "balance_sheet"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, index=True)
    year = Column(Integer)
    borrowings = Column(Float)
    debt_to_equity = Column(Float)