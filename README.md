# FastAPI App with Docker and PostgreSQL

This repository has a FastAPI app with Docker and PostgreSQL. It filters, sorts, and paginates coin data.

## How It Works

- **Filtering:** Choose data by different fields.
- **Sorting:** Arrange data by fields in ascending or descending order.
- **Pagination:** Get data in parts for better performance.

## Tech Used

- **FastAPI:** Python web framework.
- **Docker:** Containers for easy deployment.
- **PostgreSQL:** Database for coin data.
- **SQLAlchemy:** Maps Python objects to database rows.
- **Pydantic:** Validates and manages data.

## Setup

### Before You Start

- Docker must be installed.
- PostgreSQL should be running locally or remotely.

### Starting the App

1. **Clone the repo:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>

   docker-compose build

    docker-compose up -d

    Open http://localhost:8000/docs in your browser to use the API with Swagger UI.

    
This markdown code snippet can be directly used in your `README.md` file on GitHub to provide clear instructions and documentation for your FastAPI application with Docker and PostgreSQL.



