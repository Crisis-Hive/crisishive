# Crisis Hive

Real-time crisis monitoring and reporting platform. Crisis Hive lets people report ongoing crises with location data and media, and helps communities coordinate a response.

## Features

- **User accounts** — sign up / log in via Django Allauth
- **Crisis feed** — real-time feed of reported incidents
- **Location tagging** — attach geographic location to each report
- **Media uploads** — attach photos/videos to reports (stored via Cloudinary)
- **Community** — community-driven interaction around reports
- **Response coordination** — organize and track responses to active crises

## Tech Stack

- **Backend:** Django 5
- **Database:** PostgreSQL (via `dj-database-url` + `psycopg2`)
- **Auth:** django-allauth
- **Static files:** WhiteNoise
- **Media storage:** Cloudinary
- **Deployment:** Gunicorn (Heroku-style `Procfile`)

## Project Structure

```
crisishive/
├── accounts/     # user auth & profiles
├── community/    # community interactions
├── crisishive/   # project settings
├── feed/         # crisis reports feed
├── location/     # location tagging
├── media/        # media upload handling
├── response/     # crisis response coordination
├── static/       # static assets
├── templates/    # HTML templates
└── manage.py
```

## Getting Started

### Prerequisites

- Python 3.x
- PostgreSQL

### Installation

```bash
git clone https://github.com/Crisis-Hive/crisishive.git
cd crisishive

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```


### Run locally

```bash
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

## License

Add your license here.
