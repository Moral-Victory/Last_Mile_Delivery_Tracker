# Last-Mile Delivery Tracker - Phase 1

This project implements **Phase 1: Database Schema & Authentication (Core Infrastructure)** of the delivery tracker platform.

## Features
- **FastAPI Backend**: Built with FastAPI serving local JSON database storage and static files.
- **Role-Based Users**: Support for `admin`, `customer`, and `agent` roles.
- **JWT Authentication**: Safe logins using signed JWT tokens to verify identity sessions.
- **Local JSON Database (`database.json`)**: Persistent JSON document registry seeding default credentials, zones, and pricing.

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Python 3.10+ installed

### Install Dependencies
Run the following command to install the required packages:
```bash
pip install -r requirements.txt
```

### Start Backend API Server
Run the FastAPI development server:
```bash
python main.py
```
Open **[http://localhost:3000](http://localhost:3000)** in your browser to interact with the authentication dashboard.

---

## 👥 Seed Profiles for Testing
Use these credentials on the login screen to sign in as different roles:
- **Admin**: `admin@aislop.delivery` / `admin123`
- **Customer**: `customer@aislop.delivery` / `customer123`
- **Rider Agent**: `agent1@aislop.delivery` / `agent123`

---

## 🧬 API Documentation

### Authentication Endpoints

#### 1. Login (`POST /api/auth/login`)
- **Request Body**:
  ```json
  {
    "email": "customer@aislop.delivery",
    "password": "customer123"
  }
  ```
- **Response**:
  ```json
  {
    "token": "eyJhbGciOi...",
    "user": {
      "id": "usr_customer1",
      "email": "customer@aislop.delivery",
      "role": "customer",
      "name": "Premium Customer"
    }
  }
  ```

#### 2. Register Customer (`POST /api/auth/register`)
- **Request Body**:
  ```json
  {
    "email": "newuser@domain.com",
    "password": "password123",
    "name": "New Customer",
    "role": "customer"
  }
  ```

#### 3. Session Check (`GET /api/auth/me`)
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
  ```json
  {
    "authenticated": true,
    "user": { ... }
  }
  ```
