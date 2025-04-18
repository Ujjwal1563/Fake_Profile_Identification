# Fake Profile Identification Project

This project aims to detect fake profiles across social networks using **Machine Learning models** such as **SVM, ANN, XGBoost**, and **Graph-based methods**. The system includes a **FastAPI backend** and a **React frontend** to generate and visualize results.

## 🚀 Features
- Fake profile detection using machine learning models
- Graph-based visualization of user networks
- Synthetic data generation for testing
- REST API with FastAPI
- Modern UI built with React & Tailwind CSS

## 📌 Tech Stack
- **Frontend:** React, Tailwind CSS
- **Backend:** FastAPI, NetworkX, Scikit-Learn, Matplotlib
- **Database:** SQLite / PostgreSQL (optional)

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Ujjwal1563/Fake_Profile_Identification.git
cd fake-profile-identification
```

### 2️⃣ Install Backend Dependencies
```bash
cd backend
pip install fastapi uvicorn matplotlib networkx numpy pandas tensorflow scikit-learn xgboost
```

### 3️⃣ Start the Backend Server
```bash
uvicorn main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

---

### 4️⃣ Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### 5️⃣ Start the Frontend Server
```bash
npm run dev
```

The React app will be available at: `http://localhost:3000`

---

## 📜 License
This project is licensed under the MIT License.

---

## 💡 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 🔗 Contact
For any queries, reach out via [your email or GitHub profile].

