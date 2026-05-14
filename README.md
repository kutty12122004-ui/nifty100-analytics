#  Nifty 100 Financial Intelligence System

A comprehensive financial analytics platform for India's top 100 publicly listed companies.

##  Features

###  Data Engineering
- ETL Pipeline (Extract, Transform, Load)
- PostgreSQL/SQLite Data Warehouse
- Star Schema Design with Dimension & Fact Tables

### REST API
- 7+ Production-ready endpoints
- Company financial data
- Top performers ranking
- Sector-wise analysis

###  Web Dashboard
- Interactive company dashboard
- Search and filter companies
- Responsive mobile design
- Real-time data visualization

##  Tech Stack

| Category | Technology |
|----------|-----------|
| Backend | Django 6.0, Python 3.11 |
| Database | PostgreSQL / SQLite |
| API | Django REST Framework |
| Frontend | HTML5, Tailwind CSS, Chart.js |
| ETL | Pandas, NumPy |
| Version Control | Git, GitHub |

##  API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API information |
| `/api/health/` | GET | Health check |
| `/api/companies/` | GET | List all companies |
| `/api/companies/{symbol}/` | GET | Company details |
| `/api/companies/{symbol}/financials/` | GET | Historical financials |
| `/api/top-performers/` | GET | Top 15 performers |
| `/api/sector-analysis/` | GET | Sector-wise analysis |

##  Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/kutty12122004-ui/nifty100-analytics.git
cd nifty100-analytics

# Install dependencies
pip install django pandas

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
