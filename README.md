# 📝 Flask Smart Notes API

A lightweight, fully RESTful API built with **Flask** and **SQLAlchemy** for managing personal notes with tagging, search, and filtering capabilities.

This project showcases my adaptability to Flask and serves as a backend microservice example.

---

## 🚀 Features

- Create, read, update, and delete notes
- Add tags to categorize notes
- Search notes by title/content keywords
- Filter notes by tag
- Clean RESTful structure
- Easily deployable with Docker

---

## 🔧 Tech Stack

- **Python 3.10+**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLite** (or PostgreSQL-ready)
- **Postman** (for testing)
- Optional:
  - **JWT authentication**
  - **Docker**
  - **GitHub Actions**

---

## 📦 API Endpoints

### Notes

| Method | Endpoint          | Description               |
|--------|-------------------|---------------------------|
| GET    | `/notes`          | List all notes            |
| GET    | `/notes/<id>`     | Retrieve a specific note  |
| POST   | `/notes`          | Create a new note         |
| PUT    | `/notes/<id>`     | Update a note             |
| DELETE | `/notes/<id>`     | Delete a note             |

### Tags

| Method | Endpoint      | Description           |
|--------|---------------|-----------------------|
| GET    | `/tags`       | List all unique tags  |

> Filter example: `GET /notes?tag=flask`  
> Search example: `GET /notes?search=meeting`

---

## 🧪 Example Note Payload

```json
{
  "title": "Flask Interview Prep",
  "content": "Review decorators, blueprints, and routing.",
  "tags": ["flask", "interview"]
}
```
## 🛠️ Getting Started
### Clone the project
```bash
git clone https://github.com/your-username/flask-smart-notes.git
cd flask-smart-notes
```
### Create virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Run the app
```bash
python run.py
```
#### (Optional) Run with Docker
```bash
docker build -t flask-notes .
docker run -p 5000:5000 flask-notes
```
### 🧪 Testing (Optional)
```bash
pytest
# or test via Postman collection (provided in repo)
```
## 📄 License

This project is open-source and free to use under the MIT license.

## 🙋 About Me
Mahdi Khrrousheh
Python & Cloud Engineer | AWS re/Start Graduate | Learning fast, building faster\

📧 [mahdi.khrrousheh@gmail.com](mailto:mahdi.khrrousheh@gmail.com)

🔗 [LinkedIn](https://www.linkedin.com/in/khrrousheh/) | [Portfolio](https://khrrousheh.github.io/Khrrousheh/)