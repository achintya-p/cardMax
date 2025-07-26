# Credit Card Optimizer

A full-stack application that helps users optimize their credit card usage by recommending the best card for specific purchases based on reward structures and machine learning.

## Features

- 💳 Card reward structure management
- 🎯 Best card recommendation based on purchase category
- 👛 User wallet management
- 📊 Reward calculation and comparison
- 📱 Mobile-responsive frontend interface
- 🔄 Real-time recommendations
- 🤖 ML-powered features:
  - Automatic purchase category prediction
  - Personalized recommendations based on usage patterns
  - Continuous learning from user transactions
- 💾 Transaction history tracking
- 🔒 Secure user data management

## Project Structure

```
credit-card-optimizer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app entry
│   │   ├── models.py        # Pydantic models
│   │   ├── rewards.py       # Core logic
│   │   ├── ml_models.py     # ML models
│   │   ├── auth.py         # Authentication
│   │   ├── config.py       # Settings
│   │   └── data/
│   │       └── card_rewards.json
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_ml.py
│   │   └── test_rewards.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── docker-compose.yml
└── README.md
```

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/credit-card-optimizer.git
cd credit-card-optimizer
```

2. Create environment files:
```bash
# Backend
cp backend/.env.template backend/.env
# Edit backend/.env with your settings
```

3. Start services:
```bash
docker-compose up -d
```

4. Create initial superuser:
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "your-secure-password"}'
```

5. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Manual Setup

### Backend Setup

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

3. Set up environment:
```bash
cp .env.template .env
# Edit .env with your settings
```

4. Start MongoDB and Redis:
```bash
# Install MongoDB and Redis on your system, or use Docker:
docker run -d -p 27017:27017 --name mongodb mongo
docker run -d -p 6379:6379 --name redis redis
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Development Guidelines

### Backend Development

1. **Environment Variables**:
   - Never commit `.env` files
   - Use `.env.template` as a reference
   - Update `.env.template` when adding new variables

2. **Database Migrations**:
   - MongoDB is schemaless but maintain models in `app/db/models.py`
   - Update tests when changing models

3. **Testing**:
   - Write tests for new features
   - Run tests with: `pytest`
   - Maintain test coverage

4. **ML Models**:
   - Save models to `backend/models/`
   - Version models with metadata
   - Test prediction accuracy

### API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Authentication

The API uses JWT tokens for authentication:

1. Get token:
```bash
curl -X POST http://localhost:8000/token \
  -d "username=your-email@example.com&password=your-password"
```

2. Use token:
```bash
curl -H "Authorization: Bearer your-token" http://localhost:8000/cards
```

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

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details 