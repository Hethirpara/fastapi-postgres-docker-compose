import requests
from sqlalchemy import create_engine, Table, Column, MetaData, VARCHAR, Numeric

# PostgreSQL database connection details
db_user = 'quotes_user'
db_password = 'quotesuser_password'
db_name = 'quotes_db'
db_host = 'localhost'
db_port = '5432'

# SQLAlchemy engine creation
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Define metadata and table schema
metadata = MetaData()

# Define the table structure
coin_data = Table(
    'coin_data', metadata,
    Column('id', VARCHAR, primary_key=True),
    Column('rank', VARCHAR),
    Column('symbol', VARCHAR),
    Column('name', VARCHAR),
    Column('supply', Numeric),
    Column('maxSupply', Numeric),
    Column('marketCapUsd', Numeric),
    Column('volumeUsd24Hr', Numeric),
    Column('priceUsd', Numeric),
    Column('changePercent24Hr', Numeric),
    Column('vwap24Hr', Numeric)
)

# Create the table in PostgreSQL
metadata.create_all(engine)
print("Table 'coin_data' created successfully.")

# API endpoint
url = "https://api.coincap.io/v2/assets"

# Make GET request to API
response = requests.get(url)
responseData = response.json()

# Extract data from JSON response
data_to_insert = []
for item in responseData['data']:
    data_to_insert.append({
        'id': item['id'],
        'rank': item['rank'],
        'symbol': item['symbol'],
        'name': item['name'],
        'supply': item['supply'],
        'maxSupply': item['maxSupply'],
        'marketCapUsd': item['marketCapUsd'],
        'volumeUsd24Hr': item['volumeUsd24Hr'],
        'priceUsd': item['priceUsd'],
        'changePercent24Hr': item['changePercent24Hr'],
        'vwap24Hr': item['vwap24Hr']
    })

# Insert data into PostgreSQL table
with engine.connect() as connection:
    for row in data_to_insert:
        ins = coin_data.insert().values(row)
        connection.execute(ins)

print("Data inserted into 'coin_data' table successfully.")
