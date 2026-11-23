# Product Sales Management System

A Python application for product inventory and sales management, built with PostgreSQL. The project provides product registration, inventory control, sales processing, and database migration management.

## Features

- **Product Management:** Register, list, update, and delete products.
- **Inventory Management:** Track product stock and automatically update quantities after sales.
- **Sales Management:** Register sales and calculate transaction values.
- **Database Management:** PostgreSQL integration using Psycopg2.
- **Database Migrations:** Automatically execute pending migrations.
- **Seed Data:** Populate the database with initial product records.
- **Environment Configuration:** Manage database credentials through environment variables.
- **Automated Tests:** Validate application behavior using Pytest.
- **Code Quality:** Code formatting and static analysis with Ruff.

## Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| PostgreSQL | Relational database |
| Psycopg2 | PostgreSQL connection |
| Pydantic | Data validation |
| Python-dotenv | Environment configuration |
| Pytest | Automated testing |
| Ruff | Code formatting and linting |
| Git | Version control |

## Project Structure

```text
product_sales/
│
├── database/
│   ├── migrations/
│   ├── schemas.sql
│   ├── conection.py
│   ├── db_setup.py
│   ├── migration_runner.py
│   └── seed_runner.py
│
├── src/
│   ├── cli/
│   ├── interfaces/
│   ├── models/
│   ├── services/
│   └── setup/
│
├── test/
│
├── .env.example
├── .gitignore
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## Requirements

Before running the application, make sure you have:

- Python 3.10 or higher.
- PostgreSQL installed and running.
- Git installed.

## Installation

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd product_sales
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux:**

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password
```

Replace the values with your PostgreSQL configuration.

**Important:** Never commit your `.env` file or expose database credentials.

## Database Initialization

The application automatically performs the following initialization steps when executed:

1. Creates the database if it does not exist.
2. Establishes a PostgreSQL connection.
3. Executes pending database migrations.
4. Inserts initial product data through the seed process.
5. Starts the application CLI.

## Running the Application

Execute:

```bash
python main.py
```

## Running Tests

Execute the test suite:

```bash
pytest -v
```

To generate a coverage report:

```bash
pytest --cov=src --cov-report=term-missing
```

## Code Quality

Check code formatting:

```bash
ruff format --check .
```

Automatically format the project:

```bash
ruff format .
```

Run static analysis:

```bash
ruff check .
```

Automatically fix supported issues:

```bash
ruff check . --fix
```

## Environment Variables

| Variable | Description |
|---|---|
| DB_HOST | PostgreSQL server address |
| DB_PORT | PostgreSQL server port |
| DB_NAME | Database name |
| DB_USER | Database username |
| DB_PASSWORD | Database password |

## Project Goals

This project was developed to practice and demonstrate:

- Python application architecture.
- Object-oriented programming.
- Separation of responsibilities.
- PostgreSQL database integration.
- SQL queries and relational modeling.
- Inventory and sales transaction management.
- Automated testing and code quality.

## Future Improvements

- Improve application configuration and setup automation.
- Implement additional sales reports.
- Improve error handling and logging.
- Expand automated test coverage.
- Develop a graphical user interface.

## Author

**Fábio**

Python Developer | Backend Development | PostgreSQL

---

*This project is part of my continuous learning journey in Python backend development.*
