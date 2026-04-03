
 Personal Finance Tracker

Apersonal finance management application built with FastAPI (backend) and React (frontend).
##  Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

##  Installation

### 1. Clone the repository

git clone https://github.com/kidistsa/personal-finance-tracker.git

cd personal-finance-tracker
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run the backend
uvicorn app.main:app --reload --port 9000
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env.development
# Edit .env.development with your backend URL

# Run the frontend
npm run dev
