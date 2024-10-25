# Analysis of "Pruebas Saber" Data in Colombia

This project focuses on the analysis and visualization of the results from **Pruebas Saber** in Colombia, using a frontend-backend architecture. The backend is built with **Django**, and the frontend uses **Nuxt 3** to visualize the data.

### Objective
The objective of this project is to provide a tool that:
1. Retrieves results from the **Saber 11** and **Saber Pro** exams by department or municipality.
2. Visualizes and analyzes the data through interactive charts.
3. Provides basic statistics such as **skewness**, **standard deviation**, and other relevant indicators.

---

## Project Structure

The project is divided into two parts:
1. **Backend (REST API)**: Developed with Django, which exposes the data through API endpoints.
2. **Frontend**: Developed with Nuxt 3, which consumes the API endpoints and visualizes the data in an interactive interface.

---

## Installation and Setup

### Requirements
- Python 3.x (for the backend)
- Node.js (for the frontend)
- PostgreSQL Database (optional, recommended)

### Steps

1. Clone the repository
   ```bash
   git clone https://github.com/ISCOUTB/AG-Analysis-ICFES.git
   ```
2. Navigate into it
3. Setup **backend**
   - Navigate into the folder
     ```bash
     cd backend/
     ```
   - Create a virtual environment
     ```bash
     python -m venv .venv
     ```
   - Activate it
     ```bash
     .venv/Scripts/activate # Windows
     source .venv/bin/activate # Unix based systems
     ```
     - Make sure is activated using
       ```bash
       which python
       which pip
       ```
   - Install the dependencies
     ```bash
     pip install -r requirements.txt
     ```
   - Migrations and seed db  
     See [backend/data/README.md](/backend/data/README.md) for more information. Keep in mind that this files are required.
     After done with this step, you can delete the files.
     ```bash
     python manage.py migrate
     python manage.py seed -Ft Saber11
     python manage.py seed -Ft SaberPro
     ```
   - Start the development server
     ```bash
     python manage.py runserver
     ```
4. Setup **frontend**
  - Navigate into the folder
    ```bash
    cd frontend/
    ```
  - Install the dependencies
    ```bash
    npm install
    ```
  - Apply migrations
    ```bash
    npx prisma migrate dev
    ```
  - Run the app
    ```bash
    npm run dev
    ```
---

### Considerations

- Make sure to setup both .env
  - backend: POSTGRES_HOST, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
  - frontend: DATABASE_URL, and the credentials for OAuth (Github & Google)







     
