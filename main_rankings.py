from scripts.rankings_scraper import RankingsScraper


def main():
    scraper = RankingsScraper()
    
    print("Scraping ATP rankings...")
    atp_df = scraper.scrape_atp_rankings()
    scraper.save_rankings(atp_df, 'ATP')
    
    print("Scraping WTA rankings...")
    wta_df = scraper.scrape_wta_rankings()
    scraper.save_rankings(wta_df, 'WTA')
    
    print("Rankings scraping completed!")


if __name__ == "__main__":
    main()