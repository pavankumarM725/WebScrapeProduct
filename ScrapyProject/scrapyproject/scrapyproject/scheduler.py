import schedule
import time
import subprocess

def run_spider():
    subprocess.run(["scrapy", "crawl", "amazon"])

# Schedule the spider to run daily at a specific time (e.g., 8:00 AM)
schedule.every().day.at("08:00").do(run_spider)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute if it's time to run the spider


