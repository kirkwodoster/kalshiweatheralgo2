#from nws_scrape_2nd import check_ema_downtrend
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from selenium.webdriver.common.by import By
from datetime import datetime
import xml.etree.ElementTree as ET
import logging
import uuid

from weatheralgo.clients import client
from weatheralgo import util_functions
from weatheralgo import scrape_functions





def trade_execution(market: str, temperatures: list):
    try:
        highest_temp = np.array(temperatures).max()
        highest_temp = int(highest_temp)
        market_ticker = util_functions.order_pipeline(highest_temp=highest_temp, market=market)
        if market_ticker:
            return 'Market Ticker'
        balance = client.get_balance()['balance'] > 100
        if balance:          
            logging.info('order_pipeline worked')
            order_id = str(uuid.uuid4())
            client.create_order(ticker=market_ticker, client_order_id=order_id)
            logging.info(f'Order Submitted {market_ticker}')
            util_functions.trade_to_csv(order_id=order_id, ticker=market_ticker)
            logging.info('Trade Saved')
            return True
        else:
            return False
    
    except Exception as e:
        logging.info(f'trade_execution : {e}')
    
def if_temp_reaches_max(current_temp: int, market: str):
    try:
        market_temp_max = list(util_functions.weather_config(market).items())[-1][1]
        if current_temp >= market_temp_max:
            market_ticker = util_functions.order_pipeline(highest_temp=current_temp, market=market)
            order_id = str(uuid.uuid4())
            client.create_order(ticker=market_ticker, client_order_id=order_id)
            logging.info(f"Max temp reached and bet made {current_temp}")
            util_functions.trade_to_csv(order_id=order_id, ticker=market_ticker)
            logging.info('Trade Saved')
            
            return True
    except Exception as e:
        logging.info(f'if_temp_reaches_max : {e}')
    
    
def trade_criteria_met(temperatures, lr_length, timezone, xml_url):
    
    try:
        current_time = datetime.now(timezone).hour
        hour_max_temp = scrape_functions.xml_scrape(xml_url, timezone)[1]

        start_scrape = hour_max_temp - 1 >= current_time
        length = len(temperatures) >= lr_length

        if start_scrape and length:
            x = np.arange(0, lr_length).reshape(-1,1)
            temp_length = temperatures[-lr_length:]
            regressor = LinearRegression().fit(x, temp_length)
            slope = regressor.coef_
            if slope <= 0:
                return True
    except Exception as e:
        logging.error(f"Error in trade_criteria_met: {e}")
        
    