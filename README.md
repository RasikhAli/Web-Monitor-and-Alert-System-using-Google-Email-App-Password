# Web Monitor and Alert System using Google Email App Password
A Flask-based web application that monitors website uptime and sends email alerts using Google Email App Password. This tool regularly checks the status of specified websites and notifies via email when any site goes down.

## Features
- Monitor multiple websites for uptime.
- Send email alerts when a website is down.
- Configurable check intervals and alert intervals.
- Uses Google Email App Password for sending alerts.

## Requirements
- Python 3.x
- Flask
- Requests
- APScheduler
- Yagmail
- Logging

## Installation
1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/web-monitor-alert-system.git
    cd web-monitor-alert-system
    ```

2. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configuration:**
    Edit the configuration settings in `app.py` to match your requirements, including websites to monitor, email settings, etc.

## Usage
1. **Run the Flask application:**
    ```bash
    python app.py
    ```

2. **Access the web interface:**
    Open your web browser and navigate to `http://127.0.0.1:5000/`.

## How to Generate Google Email App Password
To send email alerts, you need to generate a Google Email App Password. Follow these steps:

1. **Enable Two-Factor Authentication:**
    - Go to your Google Account: [https://myaccount.google.com/](https://myaccount.google.com/)
    - Click on "Security" in the left-hand menu.
    - Under "Signing in to Google," click on "2-Step Verification" and follow the steps to set it up.

2. **Generate App Password:**
    - After enabling 2-Step Verification, return to the "Security" section.
    - Under "Signing in to Google," click on "App Passwords."
    - You might need to sign in again.
    - At the bottom of the screen, click on "Select app" and choose "Other (Custom name)".
    - Enter a custom name (e.g., "Web Monitor") and click "Generate."
    - Google will display a 16-character app password. Copy this password.

3. **Update Email Settings in the Code:**
    - In `app.py`, update the `EMAIL_USER` and `EMAIL_PASSWORD` variables with your email and the generated app password.

    ```python
    EMAIL_USER = "your-email@gmail.com"
    EMAIL_PASSWORD = "your-app-password"  # Replace with the 16-character app password
    ```

## Example Configuration
Here's an example configuration in `app.py`:

```python
WEBSITES = [
    {"url": "https://www.linkedin.com/", "title": "Linkedin"},
    {"url": "https://www.youtube.com/", "title": "Youtube"}
]
CHECK_INTERVAL = 2  # seconds
ALERT_INTERVAL_FIRST = 15  # seconds for the first alert
ALERT_INTERVAL_SUBSEQUENT = 1800  # seconds (30 minutes)
ALERT_EMAILS = ["any-email@example.com", "another-email@example.com"]
EMAIL_USER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"  # Replace with your app password
