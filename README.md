# Personal Restaurant Recommendation System

A personalized restaurant suggestion system that learns from your dining preferences to help you decide where to eat.

## Motivation
Deciding where to eat is tough when you're overwhelmed by endless Google Maps or Yelp results. This system learns your preferences and provides realistic suggestions tailored to you.

---

## Features
- **User authentication** with secure password hashing
- **Personalized ML model** per user predicting restaurant preference
- **Smart data collection** storing restaurant metadata, user interactions, and cuisine preferences
- **Statistics dashboard** to display your activity
- **Rate limiting** to protect API budget and server load
- **Production-ready deployment** on Render with database-based model storage

---

## Technologies
- **Backend**: Python (Flask)
- **Database**: SQLite (development), PostgreSQL (production)
- **ML**: scikit-learn (Logistic Regression, StandardScaler, cross-validation)
- **Visualization**: Matplotlib (Testing)
- **Frontend**: HTML/CSS, JavaScript, Jinja2
- **API**: Google Places (New) API
- **Deployment**: Render, gunicorn

---

## How It Works

### Making Suggestions
1. User provides location access and preferred drive distance
2. Google API fetches 20 nearby restaurants based on parameters
3. System extracts restaurant features and removes identifiable info
4. User's cuisine acceptance ratio is calculated and added to dataset
5. Cleaned data is passed through user's unique ML model
6. Returns top 5 predicted matches + 5 random restaurants (for exploration)

### Cold Start (New Users)
- System fetches 30 restaurants from provided location
- User rates all 30 restaurants to build initial preference profile
- This creates baseline data for model training (minimum 50 interactions recommended)
- After sufficient ratings, personalized ML predictions begin

### Data Storage
- User accepts/rejects restaurants
- Decision saved in user interaction table
- Restaurant and cuisine data upserted into respective tables

### Model Retraining
- Triggers after 50 new interactions
- Joins restaurant and interaction data
- Calculates cuisine acceptance ratios
- Splits into train/test sets with proper scaling
- Trains new logistic regression model
- Saves model and test results to database

---

## Key Technical Achievements

### ML Model Performance
- **77% cross-validation accuracy** after 762 user interactions
- **5-fold CV consistency**: Low variance across different data splits
- **No overfitting**: Train-test gap <5%

### Feature Engineering Insights
Feature importance reveals behavioral patterns:
- **Opening status (1.464)** - Most important: learned to prioritize open restaurants
- **Cuisine preference (1.368)** - Second: historical cuisine preference strongly influences decisions
- **Dine-in availability (0.011)** - Least important: minimal impact on choices

**Key insight**: The model adapts to testing behavior. I initially focused only on cuisine type, then began testing during closing hours. The model learned to prioritize opening status, showing strong adaptability to changing decision patterns.

### Per-User Model Architecture
- One model per user (fully personalized recommendations)
- Each user's model trained only on their interaction data
- **Why not global model?** User A loves Italian, User B hates Italian → different models learn different patterns. Global model would average everyone's preferences (bad recommendations for all).
- **Why cuisine_ratio works across users**: Feature already captures individuality (user1 chinese=50/55 acceptance, user2 chinese=1/10)

### Production-Grade Security
- **Password hashing** with `werkzeug.security` 
- **Session management** with encrypted Flask sessions
- **Rate limiting** (10 requests/hour for expensive endpoints)

---

## Challenges & Solutions

### Challenge 1: Finding the Right Model
- **Linear regression** - negative accuracy (wrong model type)
- **Logistic regression** - 71.67% accuracy (better fit)
- **Random forest** - 76% accuracy but overfitting detected
- **Final: Logistic regression with more data** - ~77% CV accuracy

**Learning**: More data + simpler model beats complex model with less data.

### Challenge 2: Cold-Start Problem
**Problem**: New users have 0 interactions, can't train model

**Solution: Initial Rating Collection**
- User rates 30 restaurants on first use
- Builds baseline preference data
- Enables model training once sufficient data collected (50+ interactions)
- Progressive improvement as more data accumulates

### Challenge 3: Cloud Deployment
**Problem**: Models saved to files disappear on Render restart

**Solution: Database-Based Model Storage**
- Local dev: File-based storage (fast iteration)
- Production: Database storage (survives restarts)
- Uses `pickle.dumps()` to serialize model to bytes, then store in database
- In-memory cache reduces database queries (first load ~50ms, subsequent ~0.1ms)

### Challenge 4: Feature Encoding
**Problem**: How to represent cuisine types (strings) as numerical features?

**Solution: Custom Frequency Encoding**
- Formula: `cuisine_ratio = accepted / shown`
- Example: User accepted 7/10 Italian restaurants, Italian encoded as 0.7
- Single numerical feature (no dimensionality explosion)
- Updates dynamically as user interacts

---

## Architecture Decisions & Trade-offs

### Per-User Models vs Global Model
**Chosen: Per-User**
- **Pros**: Fully personalized, learns individual preferences
- **Cons**: Need 50+ interactions per user, more models to store
- **Good for**: Recommendation systems with diverse user preferences

**Rejected: Global**
- **Pros**: Works for new users immediately, only one model
- **Cons**: Not personalized, averages everyone's preferences (bad for all)

### PostgreSQL vs Redis for Rate Limiting
**Chosen: PostgreSQL**
- **Pros**: No new services, persistent, free on Render
- **Cons**: Slightly slower than Redis (negligible for this scale)

**Why not Redis?**
- Requires separate service, costs extra on Render
- Over-engineering for current scale—can swap later if needed

---

## Results
- **~77% cross-validation accuracy** after 762 user interactions
- **Feature importance insights**:
  - Initially cuisine-driven (I only looked at cuisine type)
  - Opening status then dominated once testing during closing hours
  - **Result**: Model performs well and adapts, but takes time before results show
- **Fully personalized** recommendations per user

---

## Future Improvements
- Display restaurant images
- Show AI-generated descriptions from Google API
- Allow manual location selection (not just current location)
- Prevent duplicate restaurant names in results
- Provide direct map links to restaurants
- Use AI to categorize restaurants with unspecified cuisines
- Stricter retrain conditions with overfitting checks
- Expand statistics page (add feature importance visualizations)

---

## What I Learned

### Technical Skills
- **Cross-validation** is more reliable than single train/test split
- **Password hashing**: Can't manually compare hashes
- **Model performance improves with data**: 75.4% to 77.4% with 70 more interactions

### Software Engineering
- **Redirect vs Render**: Redirect after POST prevents duplicate submissions
- **Separation of concerns**: Database layer, ML layer, API layer, app layer
- **Error handling**: Wrap database operations in try/except with rollback
- **Start simple, iterate**: MVP with core features, deploy, then add complexity

---

## Model Performance Tracking

| Metric | Value |
|--------|-------|
| CV Mean Accuracy | 77.4% |
| CV Std | ±4.0% |
| Training Interactions | 762 |
| Features | 9 |
| Train-Test Gap | <5% |

**Feature Importance** (Logistic Regression Coefficients):
1. `open`: 1.464 (most important)
2. `cuisine_ratio`: 1.368
3. `dine_in`: 0.011 (least important)

---

## Setup & Installation

**Note**: These are placeholder instructions

### Prerequisites
- Python 3.8+
- PostgreSQL 
- Google Places API key

### Local Development
```bash
# Clone repository
git clone [repo-url]
cd restaurant-recommendation-ml

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python setup_database.py

# Run development server
python app.py
```

### Environment Variables
```
GOOGLE_API_KEY=your_api_key_here
FLASK_SECRET_KEY=random_secret_key
DATABASE_URL=postgresql://user:password@host:port/database
```

---
