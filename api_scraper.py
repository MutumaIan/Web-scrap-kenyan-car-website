import csv
import time
import requests
from retry import retry


@retry(ConnectionError, delay=2, backoff=2, tries=5)
def fetch_car_listings(page_num: int):
    """Fetch listings from the public jiji.co.ke API for a given page."""
    url = (
        "https://jiji.co.ke/api_web/v1/listing?sort=new&slug=cars"
        f"&init_page=true&page={page_num}&webp=true&lsmid=1692735392160.."
    )
    response = requests.get(url, allow_redirects=False)
    if response.status_code == 301:
        new_url = response.headers.get("Location")
        response = requests.get(new_url)

    if response.status_code == 200:
        return response.json()
    return None


def scrape_pages(start: int = 1001, end: int = 1010, output_file: str = "car_listings_1001_1200.csv"):
    start_time = time.time()
    all_listings = []
    for page_num in range(start, end):
        listings_data = fetch_car_listings(page_num)
        if not listings_data:
            break

        for listing in listings_data['adverts_list']['adverts']:
            title = listing.get('title', '')
            price = listing.get('price_obj', {}).get('view', '')

            attrs = listing.get('attrs', [])
            transmission = ''
            condition = ''
            mileage = ''

            for attr in attrs:
                if attr.get('name') == 'Transmission':
                    transmission = attr.get('value', '')
                elif attr.get('name') == 'Condition':
                    condition = attr.get('value', '')
                elif attr.get('name') == 'Mileage':
                    mileage = attr.get('value', '')

            title_parts = title.split()
            make = title_parts[0] if title_parts else ''
            model = title_parts[1] if len(title_parts) > 1 else ''
            year = ''
            color = ''

            if len(title_parts) >= 2:
                if title_parts[-2].isnumeric() and len(title_parts[-2]) == 4:
                    year = title_parts[-2]
                    if not title_parts[-1].isnumeric():
                        color = title_parts[-1]
                elif title_parts[-1].isnumeric() and len(title_parts[-1]) == 4:
                    year = title_parts[-1]
                else:
                    if not title_parts[-1].isnumeric():
                        color = title_parts[-1]

            data = {
                'Make': make,
                'Model': model,
                'Year': year,
                'Color': color,
                'Price': price,
                'Foreign/Local': condition,
                'Engine Type': transmission,
                'Mileage': mileage
            }
            all_listings.append(data)

    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Make', 'Model', 'Year', 'Color', 'Price', 'Foreign/Local', 'Engine Type', 'Mileage']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in all_listings:
            writer.writerow(data)

    elapsed_time = time.time() - start_time
    print(f"Scraping completed in {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    scrape_pages()
