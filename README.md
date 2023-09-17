# Car Listings Web Scraping and Analysis

A Python project for scraping car listings data from an ecommerce site and building a price prediction model with it.

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is designed to scrape car listings data from the a website, perform EDA and eventually build a price prediction model from the data.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Run the web scraping script by executing `python webscrap.py`.

## Usage

### Web Scraping

To scrape car listings data from the site, you can run the `webscrap.ipynb` script. It will collect data and store it in CSV files.

### Price prediction. 

After loading the data to a csv file, it is then concatenated and used to build a price prediction model using xgboost and optuna for feature analysis. 