import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import csv
import datetime
import sqlite3
import time
from io import StringIO

class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.visited = set()
        self.results = []
        self.robot_parser = RobotFileParser()
        self.robot_parser.set_url(urljoin(self.base_url, '/robots.txt'))
        try:
            self.robot_parser.read()
        except:
            print("Could not read robots.txt")
        self.rate_limit = 1  # seconds between requests
        
    def can_fetch(self, url):
        return self.robot_parser.can_fetch('*', url)

    def get_directory(self, url):
        path = urlparse(url).path
        if path == '' or path == '/':
            return '/'
        parts = path.strip('/').split('/')
        return f"/{parts[0]}/" if parts else '/'

    def scrape_page(self, url):
        if url in self.visited or not url.startswith(self.base_url):
            return
        if not self.can_fetch(url):
            print(f"Blocked by robots.txt: {url}")
            return
            
        try:
            time.sleep(self.rate_limit)  # Rate limiting
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            self.visited.add(url)
            title = soup.title.string.strip() if soup.title else 'No Title'
            directory = self.get_directory(url)
            
            self.results.append({
                'URL': url,
                'Page Title': title,
                'Directory': directory
            })
            
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                if absolute_url.startswith(self.base_url) and absolute_url not in self.visited:
                    self.scrape_page(absolute_url)
                    
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    def save_to_csv(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scrape_results_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['URL', 'Page Title', 'Directory'])
            writer.writeheader()
            writer.writerows(self.results)
        return filename

    def get_csv_string(self):
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=['URL', 'Page Title', 'Directory'])
        writer.writeheader()
        writer.writerows(self.results)
        return output.getvalue()

    def run(self):
        self.scrape_page(self.base_url)
        return self.save_to_csv()

def log_job(status, filename):
    conn = sqlite3.connect('scraper_jobs.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs 
                 (datetime TEXT, status TEXT, filename TEXT)''')
    c.execute('INSERT INTO jobs VALUES (?, ?, ?)', 
              (datetime.datetime.now().isoformat(), status, filename))
    conn.commit()
    conn.close()

def get_job_logs():
    conn = sqlite3.connect('scraper_jobs.db')
    c = conn.cursor()
    c.execute('SELECT datetime, status, filename FROM jobs ORDER BY datetime DESC')
    logs = c.fetchall()
    conn.close()
    return logs
