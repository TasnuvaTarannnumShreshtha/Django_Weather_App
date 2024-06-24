# Weather App
## Introduction
This Django-based weather application provides temperature forecasts for the coolest 10 districts in Bangladesh based on average temperatures at 2 PM for the next 7 days, utilizing the [Open-Meteo](https://open-meteo.com/en/docs) API for weather data retrieval. Additionally, it compares the 2 PM temperatures of your current location and a destination specified for travel on a given date, helping users decide whether to travel there.
## Getting Started
### Requirements

- **Python Version**: Python 3.12.3 
- **Django Version**: Django 5.0.6 
- **Celery**: Celery 5.4.0
- **Redis**: Redis 7.2.5

### Setting Up the Project
#### 1. Clone the Repository

```bash
git clone https://github.com/shreshtha-strativ/Weather-App.git
cd weather_app
```

#### 2. Install the Dependencies mentioned in Requirements Section
```bash
pip install -r package_name
```

#### 3. Set up the Database (SQLite)
```bash
python3 manage.py migrate
```

#### 4. Starting Services
Since the project uses Celery with Redis and Celery Beat, these services need to be started separately in seperate terminals
##### 1. Start Redis Server
```bash
redis-server
```
##### 2. Start Celery Worker
```bash
celery -A weather_app worker --loglevel=info
```
##### 3. Start Celery Beat
```bash
celery -A weather_app beat --loglevel=info
```
#### 5. Running the Django Server
Finally, start your Django development server in another terminal session
```bash
python3 manage.py runserver
```

### Accessing the Application
After running the django server you can visit [http://localhost:8000](http://localhost:8000) to access it through a web browser


