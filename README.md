# Ecotaxa Webscraping

## Description

This repository contains scripts and tools developed as part of web scraping and API interaction with the Ecotaxa platform. The primary goal is to automate the extraction of plancton and other microorganism data, specifically focusing on images metadata, to facilitate research and analysis work.

Ecotaxa is a web application dedicated to the visual exploration and management of planktonic data. Accessing this rich platform programmatically requires understanding of the Ecotaxa API, authentication mechanisms, and data extraction techniques. This project aims to encapsulate these aspects into a user-friendly set of scripts.

---

## Getting Started

### Prerequisites

- Required Python libraries: `requests`, `beautifulsoup4`, `selenium`, `json`, `csv`, `tqdm`, `os`.

### Usage

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/PlanktoScope/Ecotaxa-webscraping.git

2. Navigate to the cloned directory:
   ```bash
   cd ecotaxa-webscraping

3. Webscarping using Ecotaxa API (specify: project ID & own Ecotaxa credentials):
    ```bash
    ecotaxa_api_history.py

4. Webscarping using Selenium (specify: project ID & own Ecotaxa credentials):
    ```bash
    ecotaxa_scraping_v3.py

---

## License
This project is licensed under the [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0).

Copyright [Wassim Chakroun](http://www.linkedin.com/in/wassim-chakroun/) and PlanktoScope project contributors.
