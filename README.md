# Local Test Setup

### Clone

```bash
git clone https://github.com/Infinity080/job-finder.git
cd job-finder
```

### BACKEND

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cd backend/job_finder_backend/
python manage.py migrate
python manage.py runserver
```

### FRONTEND

```bash
cd frontend/job-finder-frontend/
npm install
npm start
```
