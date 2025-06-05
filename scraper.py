import time
import csv
from selenium import webdriver
from bs4 import BeautifulSoup


class CarScraper:
    """Scrape car listings from jiji.co.ke using Selenium scrolling."""

    def __init__(self, url: str = "https://jiji.co.ke/cars?sort=new", driver=None):
        self.driver = driver or webdriver.Chrome()
        self.driver.get(url)
        self.data_list = []
        self.scraped_set = set()

    def scrape_listing(self, listing):
        name = listing.find('div', class_='qa-advert-list-item-title b-list-advert-base__item-title')
        price = listing.find('div', class_='qa-advert-price')
        desc_block = listing.find('div', class_='b-list-advert-base__item-attr__wrapper')
        if not name or not price or not desc_block:
            return None

        name = name.text.strip()
        price = price.text.strip()
        desc_elements = desc_block.find_all('div')
        desc = [element.text.strip() for element in desc_elements]

        name_parts = name.split()
        if len(name_parts) < 4:
            return None

        make = name_parts[0]
        model = ' '.join(name_parts[1:-3])
        year = name_parts[-2]
        color = name_parts[-1]

        foreign_local = desc[0] if desc else ""
        engine_type = desc[-1] if desc else ""

        data = {
            'Make': make,
            'Model': model,
            'Year': year,
            'Color': color,
            'Price': price,
            'Foreign/Local': foreign_local,
            'Engine Type': engine_type,
        }
        return data

    def run(self, scrolls: int = 10, output_file: str = "car_listings.csv"):
        try:
            for i in range(scrolls):
                scroll_height = 1000 * i
                self.driver.execute_script(f"window.scrollTo(0, {scroll_height});")
                time.sleep(2)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                listing_divs = soup.find_all('div', class_='b-list-advert-base__data')
                for listing in listing_divs:
                    data = self.scrape_listing(listing)
                    if data:
                        data_str = f"{data['Make']} {data['Model']} {data['Year']} {data['Color']}"
                        if data_str not in self.scraped_set:
                            self.data_list.append(data)
                            self.scraped_set.add(data_str)
        finally:
            self.driver.quit()

        with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Make', 'Model', 'Year', 'Color', 'Price', 'Foreign/Local', 'Engine Type']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for data in self.data_list:
                writer.writerow(data)
        print(f"Data exported to {output_file}")


if __name__ == "__main__":
    scraper = CarScraper()
    scraper.run()
