
<br />
<div align="center">
  <h1 align="center">GMapHunter</h1>

  <p align="center">
    High-Performance Lead Generator for Google Maps
    <br />
    <br />
    <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
    <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"></a>
    <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres"></a>
    <a href="https://github.com/features/actions"><img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions"></a>
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

> **Struggling with the 120-result limit on Google Maps? GMapHunter shatters that barrier.**

GMapHunter is a sophisticated lead generation tool engineered to extract comprehensive business data from Google Maps with 100% coverage. Unlike standard searches that cap results, GMapHunter utilizes a smart **Grid Search Algorithm** to subdivide target cities into micro-zones (2km²), effectively bypassing limitations and harvesting thousands of high-value leads (e.g., Dentists, Restaurants, Clinics) in a single run.

Built for scale and resilience, it leverages advanced TLS fingerprinting to emulate legitimate user behavior, ensuring continuous operation without IP bans. Whether you are building a B2B database or analyzing market density, GMapHunter delivers raw, actionable data.

<!-- KEY FEATURES -->
## Key Features

*   **📍 Precision Grid Search**: Automatically generates a coordinate grid over a target city to perform granular searches, ensuring no business is missed.
*   **🛡️ Advanced Anti-Detect**: Powered by `curl_cffi`, matching real browser TLS fingerprints (Chrome/Safari) to bypass bot protections effortlessly.
*   **🐳 Docker Native**: Fully containerized application. Deploy anywhere with a single command, keeping your host system clean.
*   **💾 Smart Data Persistence**: Uses PostgreSQL with UPSERT logic to handle millions of records while preventing duplicates automatically.
*   **📊 Business-Ready Exports**: Clean, structured Excel export functionality via Pandas, ready for your CRM or sales pipeline.
*   **🤖 CI/CD Automation**: Integrated with GitHub Actions for scheduled, completely autonomous data scraping tasks.

<!-- ARCHITECTURE -->
## Architecture

The system follows a streamlined Data Pipeline architecture:

1.  **Grid Generation**: `gmap_url_creator.py` calculates a grid of coordinates based on the target city's viewport.
2.  **Data Ingestion**: `gmap_data_fetcher.py` sends requests using TLS fingerprinting.
3.  **Parsers**: Raw HTML/JSON is parsed to extract metadata (Name, Phone, Website, Address, Rating).
4.  **Storage Layer**: Validated data is pushed to PostgreSQL (NeonDB). Duplicates are rejected or updated.
5.  **Analytics/Export**: `export_to_excel.py` pulls from the DB and generates formatted reports.

### Visuals
<div align="center">
  <img src="assets/terminal_run.png" alt="Terminal Run" width="800">
  <p><em>Real-time grid processing and data extraction</em></p>
</div>

<div align="center">
  <img src="assets/excel_output_censored.png" alt="Excel Output" width="800">
  <p><em>Cleaned and structured dataset ready for use</em></p>
</div>

<!-- INSTALLATION & USAGE -->
## Installation & Usage

This project is optimized for Docker. No local Python environment setup is required.

### Prerequisites

*   Docker & Docker Compose

### 🚀 Quick Start

1.  **Clone the repository**
    ```sh
    git clone https://github.com/oguzcankaraman/GMapHunter.git
    cd GMapHunter
    ```

2.  **Configure Environment**
    Create a `.env` file with your database credentials:
    ```env
    DATABASE_URL=postgresql://user:password@host:port/dbname
    ```

3.  **Run with Docker**
    ```sh
    # Build and run the scraper container
    docker-compose up --build
    ```

4.  **Export Data**
    ```sh
    # Execute the export script inside the container
    docker-compose run scraper python export_to_excel.py
    ```

<div align="center">
  <img src="assets/github_actions_success.png" alt="CI/CD Pipeline" width="600">
  <p><em>Automated nightly builds and scrapers via GitHub Actions</em></p>
</div>

<!-- DISCLAIMER -->
## ⚠️ Disclaimer

This project is for **educational and research purposes only**.

*   Respect Google Maps' Terms of Service.
*   Do not use this tool for spamming or harassment.
*   The author is not responsible for any misuse of this software or any consequences resulting from its use.
