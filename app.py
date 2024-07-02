from flask import Flask, jsonify, render_template
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import logging
import yagmail

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

# Configuration
WEBSITES = [
    {"url": "https://www.linkedin.com/", "title": "Linkedin"},
    # {"url": "https://www.example.com.pk/", "title": "Example Site"}
]
CHECK_INTERVAL = 2  # seconds
ALERT_INTERVAL_FIRST = 15  # seconds for the first alert
ALERT_INTERVAL_SUBSEQUENT = 1800  # seconds (30 minutes)
ALERT_EMAILS = ["any-email@example.com", "another-email@example.com"]
EMAIL_USER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"  # Replace with your app password

website_status = {site['url']: {"status": "unknown", "alert_sent": False, "last_down_time": None, "last_alert_sent_time": None} for site in WEBSITES}

logging.basicConfig(level=logging.INFO)

def send_email_alert(website):
    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)
    subject = f"Website Down Alert: {website['url']}"
    body = f"The website {website['url']} ({website['title']}) is down as of {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}."

    try:
        yag.send(to=ALERT_EMAILS, subject=subject, contents=body)
        logging.info(f"Email alert sent successfully for {website['url']}.")
        website_status[website['url']]['alert_sent'] = True
        website_status[website['url']]['last_alert_sent_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logging.error(f"Failed to send email alert for {website['url']}: {e}")
    finally:
        yag.close()

def check_website():
    for website in WEBSITES:
        url = website['url']
        try:
            response = requests.get(url, timeout=10)
            logging.info(f"Checked {url}, status code: {response.status_code}")
            if response.status_code == 200:
                website_status[url]['status'] = "up"
                website_status[url]['title'] = website['title']
                website_status[url]['alert_sent'] = False
                website_status[url]['last_down_time'] = None
            else:
                handle_down_website(website)
        except requests.RequestException as e:
            logging.error(f"Error checking {url}: {e}")
            handle_down_website(website)

def handle_down_website(website):
    url = website['url']
    now = datetime.now()

    if website_status[url]['last_down_time'] is None:
        # First time the website is detected as down
        website_status[url]['last_down_time'] = now
    else:
        time_since_last_alert = (now - website_status[url]['last_alert_sent_time']).total_seconds() if website_status[url]['last_alert_sent_time'] else float('inf')

        if (now - website_status[url]['last_down_time']).total_seconds() > ALERT_INTERVAL_FIRST and not website_status[url]['alert_sent']:
            send_email_alert(website)
            website_status[url]['alert_sent'] = True
            website_status[url]['last_alert_sent_time'] = now
        elif time_since_last_alert > ALERT_INTERVAL_SUBSEQUENT and website_status[url]['alert_sent']:
            send_email_alert(website)
            website_status[url]['last_alert_sent_time'] = now

    website_status[url]['status'] = "down"

scheduler.add_job(check_website, 'interval', seconds=CHECK_INTERVAL)

@app.route('/')
def index():
    return render_template('index.html', websites=WEBSITES, website_status=website_status)

@app.route('/status')
def status():
    return jsonify(website_status)

if __name__ == "__main__":
    app.run(debug=True)
