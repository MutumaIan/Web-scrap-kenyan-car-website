# Car Listings Web Scraping and Analysis

A Python project for scraping car listings data from an ecommerce site and building a price prediction model with it.

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project scrapes car listings data from `jiji.co.ke` and demonstrates exploratory analysis and price prediction.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Use the `webscrap.py` script to run scraping or model training commands.

## Usage

### Web Scraping

Scrape using Selenium scrolling:

```bash
python webscrap.py selenium --scrolls 5 --output cars.csv
```

Scrape using the public API:

```bash
python webscrap.py api --start 1001 --end 1010 --output cars_api.csv
```

### Price prediction

After collecting CSV files, train a price prediction model:

```bash
python webscrap.py model cars.csv cars_api.csv
```

The model uses XGBoost with Optuna for hyperparameter tuning.
