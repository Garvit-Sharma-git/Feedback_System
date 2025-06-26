# 📝 Role-Based Feedback System

  

A clean, full-stack role-based feedback system built using **FastAPI**, **React**, and **TailwindCSS**. Designed for companies to manage continuous performance feedback between **managers** and **employees**, the platform supports feedback submission, acknowledgment, anonymous reviews, employee comments, and export as PDF reports.

  

---
## 🔗 Live Demo

- 🌐 **Frontend (Vercel)**: [https://feedback-system-cyan.vercel.app](https://feedback-system-cyan.vercel.app/)  
- 🛠 **Backend (Render)**: [https://feedback-system-backend-39y1.onrender.com](https://feedback-system-backend-39y1.onrender.com)

---

## 🔧 Tech Stack

  

**Frontend**

- React (Vite)

- TailwindCSS

- Axios

- React Router

- react-hot-toast

  

**Backend**

- FastAPI

- SQLAlchemy (SQLite)

- Pydantic

- CORS

- xhtml2pdf (for PDF generation)

- Docker

  

---

  

## 🌟 Features

  

- ✅ Login using email and role

- ✅ Manager can view team & give feedback

- ✅ Anonymous feedback option

- ✅ Sentiment tagging (positive/neutral/negative)

- ✅ Employees can view, acknowledge, and comment

- ✅ PDF export of feedback by manager

- ✅ Dark-themed UI with smooth UX

- ✅ Role-based access control (RBAC)

- ✅ Dockerized backend for easy deployment

  

---

  

## 🗂️ Project Structure

  
```bash 
feedback-system/

├── backend/

│ ├── app/

│ │ ├── auth.py

│ │ ├── crud.py

│ │ ├── database.py

│ │ ├── dependencies.py

│ │ ├── debug.py

│ │ ├── models.py

│ │ ├── schemas.py

│ │ └── main.py

│ └── Dockerfile

├── frontend/

│ ├── src/

│ │ ├── api/

│ │ ├── components/

│ │ ├── contexts/

│ │ ├── pages/

│ │ ├── App.jsx

│ │ └── main.jsx

│ └── index.html

└── README.md

  ```


  

---

  

## 🚀 Setup Instructions

  

### 📦 Backend

  

#### 1. Install Dependencies

  

```bash

cd  backend

pip  install  -r  requirements.txt
```

### 2.  Run  FastAPI  Server
```bash

uvicorn  app.main:app  --reload

```
Server  runs  on:  http://localhost:8000

  

### 3.  Seed  Users

```bash

curl  -X  POST  http://localhost:8000/debug/users/init
```

### 4.  Docker (Optional)

```bash

docker  build  -t  feedback-backend  .

docker  run  -p  8000:8000  feedback-backend
```

### 🌐  Frontend

### 1.  Install  Dependencies

```bash

cd  frontend

npm  install
```
### 2.  Start  React  App

```bash

npm  run  dev
```
Frontend  runs  on:  http://localhost:5173

  

### 🔐  Mock  Login  Users

#### Name  Email  Role
```bash
Alice  Manager  alice@company.com  manager

Eve  Manager  eve@company.com  manager

Bob  Employee  bob@company.com  employee

Charlie  Employee  charlie@company.com  employee

David  Employee  david@company.com  employee

Frank Employee  frank@company.com  employee

Grace Employee  grace@company.com  employee
```
  

Use  these  credentials  for  demo  purposes.

  

### 📤  Key  API  Endpoints

#### Method  Endpoint  Description
```bash
POST  /login  Login  with  email  and  role

GET  /team?manager_id=1  Get  team  members

POST  /feedback?manager_id=1  Submit  feedback

GET  /feedback/{employee_id}  Get  feedback  for  employee

GET  /feedback/manager/{manager_id}  Get  feedback  given  by  manager

POST  /feedback/{id}/acknowledge  Acknowledge  feedback

POST  /feedback/{id}/comment  Add  employee  comment  to  feedback

GET  /feedback/manager/{id}/export/pdf  Export  all  manager  feedback  as  PDF
```
  


### 📝  License

#### MIT  License

  

💡  Author

Built  with  ❤️  by  Garvit  Sharma

