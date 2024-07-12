from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Table, MetaData, select, func
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional

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
    filter: Optional[Filter]
    sort: Optional[Sort]
    pager: Pager

@app.post("/coins", response_model=dict)
def filter_coins(request_body: CoinRequestBody, db: Session = Depends(get_db)):
    try:
        query = select([coin_data])

        # Apply filter if provided
        if request_body.filter and request_body.filter.field_name and request_body.filter.field_value:
            filter_field_name = request_body.filter.field_name
            filter_field_value = request_body.filter.field_value
            query = query.where(getattr(coin_data.c, filter_field_name) == filter_field_value)

        # Apply sorting if provided
        if request_body.sort and request_body.sort.sort_by and request_body.sort.sort_order:
            sort_by = request_body.sort.sort_by
            sort_order = request_body.sort.sort_order.lower()
            if sort_order == 'asc':
                query = query.order_by(getattr(coin_data.c, sort_by).asc())
            elif sort_order == 'desc':
                query = query.order_by(getattr(coin_data.c, sort_by).desc())
            else:
                raise HTTPException(status_code=400, detail="Invalid sort_order. Use 'asc' or 'desc'.")

        # Count total records using a separate query
        total_records_query = select([func.count()]).select_from(query.subquery())
        total_records = db.execute(total_records_query).scalar()

        # Apply pagination after filtering and sorting
        page_offset = (request_body.pager.page_number - 1) * request_body.pager.page_size
        query = query.offset(page_offset).limit(request_body.pager.page_size)

        result = db.execute(query).fetchall()

        if not result:
            raise HTTPException(status_code=404, detail="No more records available.")

        return {
            "payload": {
                "data": [CoinData(**dict(row)) for row in result],
                "pager": {
                    "page_number": request_body.pager.page_number,
                    "page_size": request_body.pager.page_size,
                    "total_records": total_records
                }
            },
            "message": ""
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
