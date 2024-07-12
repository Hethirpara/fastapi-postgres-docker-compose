from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Table, MetaData, select
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional, Union

db_user = 'quotes_user'
db_password = 'quotesuser_password'
db_name = 'quotes_db'
db_host = 'localhost'
db_port = '5432'

DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

engine = create_engine(DATABASE_URL)
metadata = MetaData()

coin_data = Table(
    'coin_data', metadata,
    autoload_with=engine
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CoinData(BaseModel):
    id: str
    rank: Optional[str]
    symbol: Optional[str]
    name: Optional[str]
    supply: Optional[float]
    maxSupply: Optional[float]
    marketCapUsd: Optional[float]
    volumeUsd24Hr: Optional[float]
    priceUsd: Optional[float]
    changePercent24Hr: Optional[float]
    vwap24Hr: Optional[float]

class Pager(BaseModel):
    page_number: int = 1
    page_size: int = 10

class Filter(BaseModel):
    field_name: Optional[str] = None
    field_value: Optional[str] = None

class Sort(BaseModel):
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None

class CoinRequestBody(BaseModel):
    filter: Optional[Filter] = None
    sort: Optional[Sort] = None
    pager: Pager

@app.post("/coins", response_model=List[CoinData])
def filter_coins(request_body: CoinRequestBody, db: Session = Depends(get_db)):
    query = select([coin_data])

    # Apply filter
    if request_body.filter and request_body.filter.field_name and request_body.filter.field_value:
        filter_field_name = request_body.filter.field_name
        filter_field_value = request_body.filter.field_value
        if filter_field_name == 'name':
            query = query.where(coin_data.c.name.ilike(f"%{filter_field_value}%"))
        else:
            query = query.where(getattr(coin_data.c, filter_field_name) == filter_field_value)

    # Apply sorting
    if request_body.sort and request_body.sort.sort_by and request_body.sort.sort_order:
        if request_body.sort.sort_order.lower() == 'asc':
            query = query.order_by(getattr(coin_data.c, request_body.sort.sort_by).asc())
        elif request_body.sort.sort_order.lower() == 'desc':
            query = query.order_by(getattr(coin_data.c, request_body.sort.sort_by).desc())

    # Apply pagination after filtering and sorting
    page_offset = (request_body.pager.page_number - 1) * request_body.pager.page_size
    query = query.offset(page_offset).limit(request_body.pager.page_size)
    
    result = db.execute(query).fetchall()
    
    if not result:
        raise HTTPException(status_code=404, detail="No more records available.")
    
    return [CoinData(**dict(row)) for row in result]

