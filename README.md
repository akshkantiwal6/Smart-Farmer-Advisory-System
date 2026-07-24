# 🌾 Smart Farmer AI Market Intelligence Platform

An AI-powered agricultural market intelligence platform that helps farmers analyze historical crop prices, predict future prices using Machine Learning, and make informed selling decisions.

## 🌐 Live Demo

https://smart-farmer-advisory-system.streamlit.app/

---

# 📌 Features

- 🤖 AI-based Crop Price Prediction
- 📈 Historical Price Trend Analysis
- 📅 Seasonal Price Analysis
- 📊 Market Stability Analysis
- 💡 Smart BUY / SELL / MONITOR Recommendation
- 🗄️ SQLite Database Integration
- ☁️ Automatic Asset Download from Hugging Face
- 📱 Interactive Streamlit Dashboard
- 📥 Government Market Data Support

---

# 🖥️ Dashboard Preview

> Add screenshots here after deployment.

Example:

```
screenshots/dashboard.png
screenshots/prediction.png
screenshots/analytics.png
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Development |
| Streamlit | Web Application |
| SQLite | Database |
| Scikit-learn | Machine Learning |
| Random Forest | Price Prediction Model |
| Pandas | Data Processing |
| Plotly | Interactive Charts |
| Hugging Face | Model & Database Hosting |
| GitHub | Version Control |

---

# 📂 Project Structure

```
Smart-Farmer-Advisory-System/
│
├── analytics/
├── database/
├── ml/
├── streamlit_app/
├── download_assets.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🧠 Machine Learning

Model Used:

- Random Forest Regressor

Input Features:

- Commodity
- State
- District
- Market
- Variety
- Grade
- Date

Prediction:

- Future Modal Price

---

# 📊 Analytics

The dashboard provides:

- Historical Price Trends
- Seasonal Analysis
- Market Stability Score
- Current vs Predicted Price
- AI Recommendation Engine

---

# 📦 Dataset

Source:

**AGMARKNET (Government of India Agricultural Market Data)**

The project uses cleaned historical agricultural market data for analysis and prediction.

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/akshkantiwal6/Smart-Farmer-Advisory-System.git
```

Move into the project

```bash
cd Smart-Farmer-Advisory-System
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run streamlit_app/app.py
```

---

# 🎯 Future Improvements

- Weather-based prediction
- Mobile application
- Multi-language support
- SMS alerts for farmers
- Advanced forecasting models (XGBoost, LSTM)
- State-wise market comparison
- PDF report generation

---

# 👨‍💻 Developer

**Aksh Kantiwal**

B.Tech CSE (Artificial Intelligence)

---

# 📜 License

This project is developed for educational and research purposes.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.