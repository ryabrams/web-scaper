# 🔎 Web Scraper

A simple web scraper that crawls a website and exports URL, Page Title, and Directory information to CSV, built with Flask for GitHub Codespaces.

## Setup
1. Clone or fork this repository.
2. Open in GitHub Codespaces:
   - Click "Code" > "Codespaces" > "Create codespace on main".
3. The Codespace will install dependencies automatically via `devcontainer.json`.

## Usage
1. Run the app: `python app.py`.
2. Forward port 5000 in the Codespace UI (make it public).
3. Access the forwarded URL (e.g., `https://<username>-<random>-5000.app.github.dev/`).
4. Enter your website URL and click "Run Scraper".
5. Monitor the job status:
   - Spinner: Job running.
   - Green ✔: Success (download link appears).
   - Red ✘: Failure.
6. Download the CSV or commit results to the repo.

## Features
- Crawls all pages within the specified domain.
- Respects robots.txt and rate-limits (1 request/second).
- Extracts URL, Page Title, and Directory.
- Saves results to CSV locally and offers download via Flask.
- Logs job history (date, time, success/fail) in SQLite.
- Real-time status with spinner, checkmark, or cross.

## GitHub Codespaces Setup
This project is configured for GitHub Codespaces:
1. Open the repo in Codespaces via "Code" > "Codespaces" > "Create codespace on main".
2. Dependencies install automatically (`requirements.txt`).
3. Run `python app.py` in the terminal.
4. Forward port 5000 (labeled "Flask App") and make it public.
5. Access the app at the provided URL.

The `.devcontainer/devcontainer.json` configures:
- Python 3.9 environment.
- Port 5000 forwarding.
- VS Code Python extensions.

## File Structure
web-scraper/
│
├── .devcontainer/
│   └── devcontainer.json     # Codespaces configuration
│
├── static/
│   └── style.css             # CSS for UI (spinner, checkmark, cross)
│
├── templates/
│   └── index.html            # Flask template with form and status UI
│
├── scraper.py                # Web scraping logic
├── app.py                    # Flask app with routes and status
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore                # Git ignore rules


## Codespace Notes
- Port 5000 is forwarded automatically via `devcontainer.json`.
- Files (CSV, SQLite DB) persist only during the Codespace session unless committed:
  ```bash
  git add .
  git commit -m "Add scrape results"

## License
This project is licensed under the MIT License.
