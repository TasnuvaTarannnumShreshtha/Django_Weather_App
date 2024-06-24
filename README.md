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
git clone <repository-url>
cd <project-directory>
```

#### 2. Install the Dependencies mentioned in Requirements Section
```bash
pip install -r package_name
```

#### 3. Set up the Database (SQLite)
```bash
python3 manage.py migrate
```
