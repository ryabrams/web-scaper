from flask import Flask, render_template, request, jsonify, send_file
from scraper import WebScraper, log_job, get_job_logs
import threading
from io import BytesIO
import datetime

app = Flask(__name__)
scraper_thread = None
last_scraper = None
scraper_status = {'running': False, 'success': None, 'message': ''}

@app.route('/')
def index():
    logs = get_job_logs()
    return render_template('index.html', logs=logs)

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    global scraper_thread, last_scraper, scraper_status
    if scraper_thread and scraper_thread.is_alive():
        return jsonify({'status': 'error', 'message': 'Scraper already running'})

    base_url = request.form.get('base_url')
    if not base_url:
        return jsonify({'status': 'error', 'message': 'Please provide a base URL'})

    scraper_status = {'running': True, 'success': None, 'message': 'Scraping in progress...'}

    def scrape_task():
        global last_scraper, scraper_status
        try:
            scraper = WebScraper(base_url)
            filename = scraper.run()
            last_scraper = scraper
            log_job('success', filename)
            scraper_status = {'running': False, 'success': True, 'message': 'Scraping completed successfully'}
        except Exception as e:
            log_job('fail', str(e))
            scraper_status = {'running': False, 'success': False, 'message': f'Scraping failed: {str(e)}'}

    scraper_thread = threading.Thread(target=scrape_task)
    scraper_thread.start()
    return jsonify({'status': 'success', 'message': 'Scraper started'})

@app.route('/scraper-status')
def get_scraper_status():
    return jsonify(scraper_status)

@app.route('/download-last-csv')
def download_last_csv():
    global last_scraper
    if not last_scraper or not last_scraper.results:
        return "No recent scrape available", 404
        
    csv_data = last_scraper.get_csv_string()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return send_file(
        BytesIO(csv_data.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"scrape_results_{timestamp}.csv"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
