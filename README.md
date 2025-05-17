# Bright Money Assignment 

## 📘 Overview

A Django-based credit card management system providing RESTful APIs for credit card applications, EMI schedules, loan management, and payments. It uses MongoDB for storage and Celery for asynchronous background tasks.

---

## 🛠️ Tech Stack

- Python 3.11  
- Django 3.2.8  
- MongoDB (via Djongo)  
- Django REST Framework  
- Celery for async task handling  

---

## ✨ Features

- ✅ User registration with credit score calculation  
- ✅ Credit card loan application & eligibility check  
- ✅ EMI calculation (with principal + interest)  
- ✅ Payment handling with validations  
- ✅ Loan statement generation (past + upcoming)  
- ✅ Billing system with min due, APR, and due date  
- ✅ Daily cron via Celery for billing cycle management  

---

## ⚙️ Prerequisites

- Python 3.11  
- MongoDB instance (local or cloud)  
- Git  

---

## 🚀 Setup & Run (Single Terminal)

`````bash
# 1. Clone the repository
git clone <repository-url>
cd Django_Assign

# 2. Create and activate virtual environment
python -m venv venv

# Activate for Windows
.\venv\Scripts\Activate.ps1

# OR Activate for macOS/Linux
# source venv/bin/activate

# 3. Install dependencies
pip install setuptools wheel
pip install sqlparse==0.2.4
pip install django==3.2.8
pip install djongo==1.3.6
pip install djangorestframework==3.14.0
pip install pytz python-dotenv celery pymongo==3.12.3

# 4. Create .env in root with your MongoDB credentials:
echo "MONGODB_NAME=optimusprime
MONGODB_URL=mongodb+srv://<username>:<password>@cluster.mongodb.net/
MONGODB_USER=<username>
MONGODB_PASSWORD=<password>" > .env

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Run both Django server and Celery worker in background (macOS/Linux only):
gnome-terminal --tab -- bash -c "python manage.py runserver" &
gnome-terminal --tab -- bash -c "celery -A credit_card_system worker --loglevel=info" &

# For Windows users, open two terminals manually:
# Terminal 1: python manage.py runserver
# Terminal 2: celery -A credit_card_system worker --loglevel=info
`````

---

## 🔌 API Endpoints

### 🔹 Register User  
`POST /api/users/`
```json
{
  "aadhar_id": "123456789012",
  "name": "John Doe",
  "annual_income": 500000
}
```

### 🔹 Apply for Loan  
`POST /api/apply-loan/`
```json
{
  "unique_user_id": "user-uuid",
  "loan_type": "credit_card",
  "loan_amount": 5000,
  "interest_rate": 12,
  "term_period": 12,
  "disbursement_date": "2024-03-20"
}
```

### 🔹 Make Payment  
`POST /api/make-payment/`
```json
{
  "loan_id": "loan-uuid",
  "amount": 1000
}
```

### 🔹 View Statement  
`GET /api/get-statement/<loan_id>/`

---

## 📊 Business Logic

### ✅ Credit Score
- Range: 300–900 based on CSV balance
- ₹15,000 per score unit
- Async via Celery

### ✅ Loan Rules
- Min Score: 450
- Min Income: ₹1,50,000
- Max Loan: ₹5,000
- Interest ≥ 12%
- EMI ≤ 20% of monthly income

### ✅ EMI & Billing
- Daily interest from T+1
- Billing cycle every 30 days
- Due = billing date + 15 days
- Min Due = 3% principal + APR

---

## 🧾 Project Structure

```
Django_Assign/
├── credit_api/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tasks.py
├── credit_card_system/
│   ├── settings.py
│   ├── celery.py
│   └── urls.py
└── manage.py
```

---

## 🧪 Testing

```bash
python manage.py test
```



## ⚠️ Developer Notes

- MongoDB must be running
- Celery required for async credit score & billing
- `credit_data.csv` must be present and updated

---


Happy coding! 🚀
