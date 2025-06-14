import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timezone, timedelta


class RankingsScraper:
    atp_rankings_url = "https://tennisabstract.com/reports/atpRankings.html"
    wta_rankings_url = "https://tennisabstract.com/reports/wtaRankings.html"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
    
    def scrape_rankings(self, url):
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', {'id': 'reportable'})
            
            if not table:
                raise ValueError(f"Could not find rankings table on {url}")
            
            rows = table.find_all('tr')[1:]  # Skip header row
            
            rankings_data = []
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    rank = cells[0].get_text(strip=True)
                    player_cell = cells[1]
                    player_name = player_cell.get_text(strip=True)
                    player_link = player_cell.find('a')
                    player_url = player_link.get('href') if player_link else None
                    country = cells[2].get_text(strip=True)
                    birthdate = cells[3].get_text(strip=True)
                    
                    rankings_data.append({
                        'rank': rank,
                        'player': player_name,
                        'country': country,
                        'birthdate': birthdate,
                        'player_url': player_url
                    })
            
            return pd.DataFrame(rankings_data)
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def scrape_atp_rankings(self):
        return self.scrape_rankings(self.atp_rankings_url)
    
    def scrape_wta_rankings(self):
        return self.scrape_rankings(self.wta_rankings_url)
    
    def save_rankings(self, df, tour_type, timestamp=None):
        if df is None or df.empty:
            print(f"No data to save for {tour_type}")
            return
        
        if timestamp is None:
            jst = timezone(timedelta(hours=9), 'JST')
            timestamp = datetime.now(jst)
        
        date_str = timestamp.strftime("%Y-%m-%d")
        
        # Save with timestamp
        timestamped_path = f'./data/{tour_type.lower()}-rankings-{date_str}.csv'
        df.to_csv(timestamped_path, index=False)
        print(f"Saved {tour_type} rankings to {timestamped_path}")
        
        # Save as latest
        latest_path = f'./latest/{tour_type.lower()}-rankings.csv'
        df.to_csv(latest_path, index=False)
        print(f"Saved {tour_type} rankings to {latest_path}")


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