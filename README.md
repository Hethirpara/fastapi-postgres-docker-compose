# Coin Data API

This FastAPI application allows you to manage and retrieve cryptocurrency data from a PostgreSQL database. You can filter, sort, and paginate the data using the provided endpoints. The application is also equipped with Swagger UI for easy interaction with the API.

## Features

- **Filter**: Filter data based on specific fields.
- **Sort**: Sort data by various fields in ascending or descending order.
- **Pagination**: Paginate the data to manage large datasets efficiently.

## Requirements

- Python 3.8+
- PostgreSQL
- FastAPI
- SQLAlchemy
- Pydantic

## Setup

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt

db_user = 'your_username'
db_password = 'your_password'
db_name = 'your_dbname'
db_host = 'your_hostname'
db_port = 'your_port_number'


uvicorn main:app --reload
