from fake_useragent import UserAgent
import logging
import numpy as np
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from weatheralgo import trade_functions
from weatheralgo import scrape_functions
from weatheralgo.input_variables import MARKET_DENVER, LR_LENGTH, SCRAPE_INTERVAL, TIMEZONE_DENVER, XML_URL_DENVER, URL_DENVER
from weatheralgo import util_functions


# Initialize Selenium WebDriver
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-data")
    chrome_options.add_argument("--headless")
    ua = UserAgent()
    chrome_options.add_argument(f"user-agent={ua.random}")
    return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


class seriesSelector:
    def __init__(self, )

# Main function to scrape and process data
def scrape_dynamic_table(driver, url=URL_DENVER, timezone= TIMEZONE_DENVER):
    

    util_functions.logging_settings()
    temperatures = []
    dates = []
    
    restart_threshold = 50  # Restart WebDriver every 50 iterations
    loop_counter = 0

    logging.info('Loading Scrape Dynamic Table')

    while True:
        begin_scraping = scrape_functions.begin_scrape(timezone=TIMEZONE_DENVER)
        trade_made_today = util_functions.trade_today(market=MARKET_DENVER, timezone=TIMEZONE_DENVER)
        logging.info('While Loop')
        time.sleep(3)
        try:
            logging.info(f'being_scraping is {begin_scraping}')
            logging.info(f'trade_made_today is {trade_made_today}')
            if begin_scraping and not trade_made_today:
                logging.info('Begin Scrape')
                logging.info('No Trade Made Today')
                
                scrape_temp = scrape_functions.scrape_temperature(driver=driver, url=URL_DENVER, timezone=TIMEZONE_DENVER)
                current_date = scrape_temp[0]
                current_temp = scrape_temp[1]
                logging.info(f'Dates length {len(dates)}')
                
                if len(dates) == 0 or (len(dates) > 0 and dates[-1] != current_date):
                    
                    dates.append(current_date)
                    temperatures.append(current_temp)
                    
                    logging.info(f"Date: {dates}")
                    logging.info(f"Date: {temperatures}")

                    #checks to see if currentc temp is at max of available markets then makes bet
                
                    current_temp_is_max = trade_functions.if_temp_reaches_max(current_temp=current_temp, market = MARKET_DENVER)
                    if current_temp_is_max:
                        logging.info('Max Temperature Reached')
                       
                        temperatures = []
                        dates = []
   
                    trade_criteria = trade_functions.trade_criteria_met(temperatures=temperatures, 
                                                              lr_length=LR_LENGTH,
                                                              timezone=TIMEZONE_DENVER, 
                                                              xml_url=XML_URL_DENVER)
                    if trade_criteria:
                        
                        trade_execute = trade_functions.trade_execution(temperatures=temperatures,market=MARKET_DENVER)
                        if trade_execute:
                            logging.info('Trade Criteria True')
                           
                            temperatures = []
                            dates = []
                
                else:
                    # rand = randint(5, 10)
                    # time.sleep(rand)
                    logging.info('to_append is False')
            elif trade_made_today:
                temperatures = []
                dates = []
            else:
                continue
          
        except Exception as e:
            logging.error(f"in main loop: {e}")

            loop_counter += 1
            if loop_counter >= restart_threshold:
                logging.info("Restarting WebDriver to prevent stale sessions...")
                driver.quit()
                driver = initialize_driver()
                loop_counter = 0  # Reset counter

            time.sleep(3)




# # Entry point
# if __name__ == "__main__":

#     driver = initialize_driver()

#     try:
#         scrape_dynamic_table(driver)
 
#     except KeyboardInterrupt:
#         logging.info("Script interrupted by user.")
#     finally:
#         driver.quit()
#         logging.info("WebDriver closed.")
        
