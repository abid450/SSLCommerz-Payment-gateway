# 💳 SSLCommerz Payment Gateway Integration

A production-ready **SSLCommerz Payment Gateway** integration built with **Django**, **Celery**, **Redis**, and **Django REST Framework**. This project provides a complete payment solution with email confirmation, transaction tracking, and secure payment processing.

---

## 🏷️ Badges

![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.15-FF1709?logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-5.6-37814A?logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?logo=redis&logoColor=white)
![SSLCommerz](https://img.shields.io/badge/SSLCommerz-3.0-FF6B00)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24-2496ED?logo=docker&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?logo=github&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ✅ **SSLCommerz Integration** | Complete SSLCommerz payment gateway integration |
| ✅ **Multiple Payment Methods** | bKash, Nagad, Rocket, Credit/Debit Card, COD |
| ✅ **Transaction Management** | Track all payments with unique transaction ID |
| ✅ **Email Confirmation** | Automatic email confirmation via Celery |
| ✅ **Async Processing** | Background tasks with Celery + Redis |
| ✅ **IPN Handling** | Instant Payment Notification for real-time updates |
| ✅ **Validation** | Full validation with Django REST Framework serializers |
| ✅ **Responsive Design** | Mobile-friendly checkout page |
| ✅ **Security** | CSRF protection, secure payment processing |
| ✅ **API Ready** | Complete REST API for payment integration |
| ✅ **Environment Config** | All sensitive data in `.env` file |

---

## 🛠️ Tech Stack

| Technology | Badge | Purpose |
|------------|-------|---------|
| **Django 6.0** | ![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white) | Web Framework |
| **Django REST Framework** | ![DRF](https://img.shields.io/badge/DRF-3.15-FF1709?logo=django&logoColor=white) | API Development |
| **Celery** | ![Celery](https://img.shields.io/badge/Celery-5.6-37814A?logo=celery&logoColor=white) | Background Task Queue |
| **Redis** | ![Redis](https://img.shields.io/badge/Redis-7.0-DC382D?logo=redis&logoColor=white) | Message Broker & Cache |
| **SSLCommerz** | ![SSLCommerz](https://img.shields.io/badge/SSLCommerz-3.0-FF6B00) | Payment Gateway |
| **PostgreSQL** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white) | Database |
| **Gmail SMTP** | ![Gmail](https://img.shields.io/badge/Gmail-SMTP-EA4335?logo=gmail&logoColor=white) | Email Sending |
| **Docker** | ![Docker](https://img.shields.io/badge/Docker-24-2496ED?logo=docker&logoColor=white) | Containerization |
| **Python 3.10+** | ![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white) | Programming Language |
| **Git** | ![Git](https://img.shields.io/badge/Git-2.40-F05032?logo=git&logoColor=white) | Version Control |

---

## 📁 Project Structure

sl/
├── 📄 manage.py
├── 📄 .env
├── 📄 requirements.txt
├── 📄 README.md
├── 📁 sl/
│ ├── 📄 init.py
│ ├── 📄 celery.py
│ ├── 📄 settings.py
│ ├── 📄 urls.py
│ └── 📄 wsgi.py
├── 📁 Payment/
│ ├── 📄 init.py
│ ├── 📄 admin.py
│ ├── 📄 apps.py
│ ├── 📄 models.py
│ ├── 📄 serializers.py
│ ├── 📄 services.py
│ ├── 📄 tasks.py
│ ├── 📄 urls.py
│ └── 📄 views.py
├── 📁 static/
│ └── 📁 images/
│ ├── 🖼️ bkash.jpg
│ ├── 🖼️ nagad.webp
│ ├── 🖼️ rk.webp
│ └── 🖼️ devit.webp
├── 📁 templates/
│ └── 📁 payment/
│ ├── 📄 checkout.html
│ ├── 📄 success.html
│ ├── 📄 failed.html
│ └── 📄 cancelled.html
├── 📁 logs/
└── 📁 frontend/


---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- Redis Server
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/sslcommerz-payment.git
cd sslcommerz-payment


# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate

Step 7: Start Redis Server

redis-server --port 6376

Step 8: Start Celery Worker

# Windows
celery -A sl worker --loglevel=info -P eventlet

# Mac/Linux
celery -A sl worker --loglevel=info

Step 9: Start Celery Beat (for periodic tasks)

celery -A sl beat --loglevel=info

📡 API Endpoints

Method	Endpoint	Description
POST	/payment/api/initiate/	Initiate payment
GET	/payment/api/status/<tran_id>/	Check payment status
POST	/payment/api/<id>/retry/	Retry failed payment
POST	/payment/api/<id>/refund/	Refund payment (admin)
GET	/payment/checkout/	Checkout page
GET	/payment/success/	Payment success page
GET	/payment/failed/	Payment failed page
POST	/payment/ipn/	IPN webhook

Test API with Postman
POST /payment/api/initiate/
Content-Type: application/json

{
    "amount": "500.00",
    "customer_name": "Test Customer",
    "customer_email": "test@example.com",
    "customer_phone": "01712345678",
    "payment_method": "bkash"
}

📊 Database Models
PaymentTransaction
Field	Type	Description
tran_id	CharField	Unique transaction ID
amount	DecimalField	Payment amount
status	CharField	initiated/pending/completed/failed
payment_method	CharField	bkash/nagad/card/cod
customer_name	CharField	Customer full name
customer_email	EmailField	Customer email
customer_phone	CharField	Customer phone
paid_at	DateTimeField	Payment completion time
