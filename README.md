# DeepTrip 🌍✈️

## 📑 Table of Contents
- [Project Overview](#project-overview)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
  - [Logical Architecture](#logical-architecture)
- [Technical Stack](#technical-stack)
- [Database Design](#database-design)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Deployment](#deployment)
- [Module Documentation](#module-documentation)
- [API Reference](#api-reference)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [Contact](#contact)

---

## 🌐 Project Overview
**DeepTrip** is an intelligent travel assistant system that integrates AI planning, multi-resource aggregation, and full-process service capabilities.  

It addresses pain points of traditional travel platforms such as:
- ❌ Fragmented information
- ❌ Inefficient planning
- ❌ Delayed responses  

By leveraging:
- 🧠 **Natural Language Processing (NLP)**
- 🎯 **Recommendation algorithms**
- 📱 **Cross-terminal adaptation**

The system connects **travelers**, **merchants**, and **administrators** to provide a **closed-loop service** covering:
- Pre-trip planning 📅  
- In-trip assistance 🗺️  
- Post-trip feedback ⭐  

➡️ Result: Enhanced **user experience** and improved **operational efficiency**.

---

## 🌟 Core Features

### 👤 For Travelers
- 🧭 **AI-Powered Planning**: Personalized itineraries based on preferences (budget, style, diet).  
- 💬 **Natural Language Interaction**: Chat with AI assistant to ask or adjust plans.  
- 🏨 **One-Click Booking**: Reserve hotels, attractions, restaurants.  
- 🌦️ **Real-Time Updates**: Weather alerts, crowd forecasts, dynamic changes.  
- 📔 **Travel Journal**: Auto-organize trip photos & notes, easy sharing.  

### 🏪 For Merchants
- 📝 **Simplified Onboarding**: Submit business info via portal.  
- 📦 **Order Management**: Real-time tracking, inventory control.  
- ⭐ **User Feedback**: View ratings & reviews.  
- 🎯 **Targeted Promotion**: Reach potential customers via recommendations.  

### 🔧 For Administrators
- 📊 **Dashboard Analytics**: Active users, bookings, merchant count.  
- ✅ **Merchant Review**: Approve/reject applications.  
- 📑 **Data Reporting**: Generate custom reports.  
- ⚙️ **System Config**: Permissions, moderation, service integration.  

---

## 🏗️ System Architecture

### 🧩 Logical Architecture
DeepTrip adopts a **microservices-based architecture** with clear separation of concerns for scalability & maintainability.

```plaintext
┌─────────────────────────────────────────────────────────────────┐
│                        Client Layer                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │  Web App    │  │ Mobile App  │  │  Merchant Portal        │  │
│  │ (Vue 3 + TS)│  │ (Flutter)   │  │ (Vue 3 + TS)            │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                        API Gateway Layer                         │
│  (Routing, Auth, Rate Limit, Logging)                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                     Microservice Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ User Service│  │ Travel Svc  │  │ Booking Svc │  │ AI Svc  │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Merchant Svc│  │ Admin Svc   │  │ Feedback Svc│             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                      Data & Integration Layer                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │ MySQL 8.0   │  │ Redis 7+    │  │ Third-Party APIs        │  │
│  │ (Core Data) │  │ (Cache)     │  │ - Amap (Maps)           │  │
│  └─────────────┘  └─────────────┘  │ - Alipay/WeChat Pay     │  │
│                                    │ - HeWeather              │  │
│                                    └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘

```

## ⚙️ Technical Stack 

| **Layer**          | **Technology Stack** |
|---------------------|-----------------------|
| 🎨 **Frontend**  | Web: Vue 3, TypeScript, Pinia, Vite <br> Mobile: Flutter 3.19+, Dart 3.3+ |
| 🐍 **Backend**  | Framework: FastAPI (Python 3.10+) <br> Microservices: Spring Cloud <br> API: RESTful |
| 🤖 **AI & Algorithm**  | NLP: Hugging Face Transformers <br> Recommendation: Collaborative Filtering |
| 💾 **Data Storage**  | Database: MySQL 8.0 <br> Cache: Redis 7+ <br> Message Queue: RabbitMQ/Kafka |
| 🛠️ **DevOps**  | Containerization: Docker <br> Orchestration: Kubernetes <br> CI/CD: GitHub Actions |
| 🔐 **Security**  | Authentication: JWT <br> Encryption: SSL/TLS, AES <br> Permission: RBAC |

---

## 🗄️ Database Design 
The database is divided into three core modules with normalized tables to avoid redundancy:

- **User Service Module**
  - `TRAVELLER`: User profile, preferences, and authentication.
  - `PATHLIST`: Travel itineraries created by users.
  - `AIMESSAGE`: Chat history between users and the AI assistant.

- **Merchant Service Module**
  - `MERCHANT`: Merchant account and authentication.
  - `MERCHANTINFO`: Business details (address, opening hours, menu/room types).

- **System Management Module**
  - `BOOK`: Booking records (user, merchant, status).
  - `COMMENT`: User reviews and ratings.
  - `ADMIN`: Administrator accounts and permissions.

📑 For detailed schemas, check the **Database Design Document**.

---

## 🚀 Quick Start 

### 📋 Prerequisites 
- Python 3.10+ (for backend/AI services)
- Node.js 16+ (for frontend)
- Flutter 3.19+ (for mobile app)
- MySQL 8.0
- Redis 7+
- Docker & Docker Compose (optional, for containerized deployment)

### ⚡ Installation 

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/DeepTrip.git
cd DeepTrip
```

#### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt

cp .env.example .env
# Edit .env to set database credentials, API keys, etc.

python scripts/init_db.py

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup (Web App)
```bash
cd frontend/user-web
npm install
npm run dev
```

#### 4. Mobile App Setup (Flutter)
```bash
cd mobile
flutter pub get
flutter run
```

### 🚢 Deployment 
For production deployment, use **Docker Compose**:
```bash
docker-compose up -d --build
docker-compose ps
```

## 📚 Module Documentation 

DeepTrip is divided into several core modules. Each module is designed to be independent, extensible, and easy to integrate.  

### 👤 1. User Service 
- **Description**: Handles user authentication, profile management, and preference storage.  
- **Key Features**:
  - User registration & login  
  - OAuth2 authentication  
  - Profile editing (interests, travel preferences, history)  
  - Secure session management  

### 🤖 2. AI Assistant Service 
- **Description**: Core AI engine responsible for itinerary generation, Q&A, and real-time travel insights.  
- **Key Features**:
  - AI-powered trip plan generation (single or multiple options)  
  - Natural language Q&A for travel-related queries  
  - Real-time data integration (maps, weather, traffic)  
  - Dynamic re-planning in case of disruptions  

### 🏨 3. Booking Service 
- **Description**: Provides reservation and booking functionalities for hotels, restaurants, and attractions.  
- **Key Features**:
  - Hotel and restaurant booking  
  - Attraction/ticket booking  
  - Review and rating system integration  
  - Secure payment gateway support  

### 🏪 4. Merchant Service 
- **Description**: Enables local merchants to onboard their businesses and interact with users.  
- **Key Features**:
  - Merchant data upload & verification  
  - Business profile management  
  - Viewing user feedback and ratings  
  - Recommendation engine integration  

### 🛠️ 5. Admin Service 
- **Description**: Platform management and analytics tools for administrators.  
- **Key Features**:
  - Merchant approval & data management  
  - User activity monitoring  
  - System-wide configuration settings  
  - Data analytics on popular routes, bookings, and merchant activity  

---

Made with ❤️ by the **DeepTrip Team**
