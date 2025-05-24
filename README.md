# Financial Portfolio Tracker

A full-stack application for tracking and visualizing financial portfolios using Python, Django, React, and Snowflake.

## Tech Stack

- Backend: Python, Django, Django REST Framework
- Frontend: React, Tailwind CSS
- Database: Snowflake
- Cloud: Azure Functions, Azure SQL
- Data Visualization: Chart.js

## Project Structure

```
python-react-snowflake/
├── backend/           # Django backend
├── frontend/         # React frontend
└── azure/           # Azure Functions
```

## Setup Instructions

### Backend Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:
```bash
cd backend
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
# Django
SECRET_KEY=your_secret_key
DEBUG=True

# Snowflake
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_WAREHOUSE=your_warehouse

# Azure
AZURE_STORAGE_CONNECTION_STRING=your_connection_string
```

## License

MIT 