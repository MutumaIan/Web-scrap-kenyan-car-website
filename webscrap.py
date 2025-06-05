import argparse
from scraper import CarScraper
from api_scraper import scrape_pages
from model import load_dataset, train_model


def main():
    parser = argparse.ArgumentParser(description="Car listings scraping and modeling")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_selenium = subparsers.add_parser("selenium", help="Scrape using selenium")
    parser_selenium.add_argument("--scrolls", type=int, default=10)
    parser_selenium.add_argument("--output", default="car_listings.csv")

    parser_api = subparsers.add_parser("api", help="Scrape using API pages")
    parser_api.add_argument("--start", type=int, default=1001)
    parser_api.add_argument("--end", type=int, default=1010)
    parser_api.add_argument("--output", default="car_listings_1001_1200.csv")

    parser_model = subparsers.add_parser("model", help="Train price prediction model")
    parser_model.add_argument("csv", nargs="+", help="CSV files with listings")

    args = parser.parse_args()

    if args.command == "selenium":
        scraper = CarScraper()
        scraper.run(scrolls=args.scrolls, output_file=args.output)
    elif args.command == "api":
        scrape_pages(start=args.start, end=args.end, output_file=args.output)
    elif args.command == "model":
        df = load_dataset(args.csv)
        train_model(df)


if __name__ == "__main__":
    main()
