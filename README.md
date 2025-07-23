# Credit Card Optimizer

A full-stack application that helps users optimize their credit card usage by recommending the best card for specific purchases based on reward structures.

## Project Structure

```
credit-card-optimizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app entry
│   │   ├── models.py        # Pydantic models
│   │   ├── rewards.py       # Core logic
│   │   └── data/
│   │       └── card_rewards.json
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

## Features

- 💳 Card reward structure management
- 🎯 Best card recommendation based on purchase category
- 👛 User wallet management
- 📊 Reward calculation and comparison
- 📱 Mobile-responsive frontend interface
- 🔄 Real-time recommendations

## Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Documentation

Once the backend server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run backend tests:
```bash
cd backend
pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Mobile App Development

The frontend is designed to be built into a mobile app using React Native. Future development will include:
- Native iOS and Android apps
- Push notifications for card recommendations
- Offline support
- Card scanning capabilities 