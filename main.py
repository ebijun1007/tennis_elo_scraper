from datetime import datetime, timedelta, timezone

import pandas as pd
from scripts.elo_scraper import EloScraper


def main():
    jst = timezone(timedelta(hours=9), 'JST')
    now = datetime.now(jst)
    elo_scraper = EloScraper()
    atp_elo_table = elo_scraper.get_html_table(elo_scraper.link_atp_elo)
    atp_yelo_table = elo_scraper.get_html_table(elo_scraper.link_atp_yelo)
    wta_elo_table = elo_scraper.get_html_table(elo_scraper.link_wta_elo)
    wta_yelo_table = elo_scraper.get_html_table(elo_scraper.link_wta_yelo)

    # convert html table to pandas dataframe
    atp_elo_df = elo_scraper.convert_html_table_to_csv(
        atp_elo_table).set_index('Player')
    atp_yelo_df = elo_scraper.convert_html_table_to_csv(
        atp_yelo_table).set_index('Player')
    wta_elo_df = elo_scraper.convert_html_table_to_csv(
        wta_elo_table).set_index('Player')
    wta_yelo_df = elo_scraper.convert_html_table_to_csv(
        wta_yelo_table).set_index('Player')

    # join elo_df and yelo_df
    atp_elo_df = atp_elo_df.join(atp_yelo_df.drop(
        columns=['Rank', 'Wins', 'Losses']))
    wta_elo_df = wta_elo_df.join(wta_yelo_df.drop(
        columns=['Rank', 'Wins', 'Losses']))

    # save dataframe to csv file
    atp_elo_df.to_csv(f'./data/atp-{now.strftime("%Y-%m-%d")}.csv')
    wta_elo_df.to_csv(f'./data/wta-{now.strftime("%Y-%m-%d")}.csv')

    # save dataframe to csv file as latest
    atp_elo_df.to_csv(f'./latest/atp.csv')
    wta_elo_df.to_csv(f'./latest/wta.csv')


if __name__ == "__main__":
    main()
