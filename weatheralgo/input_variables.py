import pytz


URL_DENVER = "https://www.weather.gov/wrh/timeseries?site=KDEN&hours=3"
XML_URL_DENVER = 'https://forecast.weather.gov/MapClick.php?lat=39.8589&lon=-104.6733&FcstType=digitalDWML'
TIMEZONE_DENVER = pytz.timezone("America/Denver")

SCRAPING_HOURS = (8, 23)  # Hours to consider for trading (6 AM to 4 PM)
TRADE_EXECUTION_HOURS = (9, 15)
MARKET_DENVER = 'KXHIGHDEN'
LR_LENGTH = 5




class SeriesSelector:

    def __init__(self):
        self.all_markets = {
            'DENVER': {
                'SERIES': 'KXHIGHDEN',
                'TIMEZONE': 'America/Denver',
                'URL': "https://www.weather.gov/wrh/timeseries?site=KDEN&hours=3",
                'XML_URL': 'https://forecast.weather.gov/MapClick.php?lat=39.8589&lon=-104.6733&FcstType=digitalDWML',
            },
            'CHICAGO': {
                'SERIES': 'KXHIGHCHI',
                'TIMEZONE': 'America/Chicago',
                'URL': 'https://www.weather.gov/wrh/timeseries?site=KMDW&hours=3',
                'XML_URL': 'https://forecast.weather.gov/MapClick.php?lat=41.7842&lon=-87.7553&FcstType=digitalDWML',
            },
            'MIAMI': {
                'SERIES': 'KXHIGHMIA',
                'TIMEZONE': 'America/Miami',
                'URL': 'https://www.weather.gov/wrh/timeseries?site=KMIA&hours=3',
                'XML_URL': 'https://forecast.weather.gov/MapClick.php?lat=25.7934&lon=-80.2901&FcstType=digitalDWML',
            },
            'AUSTIN': {
                'SERIES': 'KXHIGHAUS',
                'TIMEZONE': 'America/Austin',
                'URL': 'https://www.weather.gov/wrh/timeseries?site=KAUS&hours=3',
                'XML_URL': 'https://forecast.weather.gov/MapClick.php?lat=30.1945&lon=-97.6699&FcstType=digitalDWML',
            },
            'PHILADELPHIA': {
                'SERIES': 'KXHIGHPHIL',
                'TIMEZONE': 'America/Philadelphia',
                'URL': 'https://www.weather.gov/wrh/timeseries?site=KPHL&hours=3',
                'XML_URL': 'https://forecast.weather.gov/MapClick.php?lat=39.8721&lon=-75.2407&FcstType=digitalDWML',
            },
            'LOS ANGELES': {
                'SERIES': 'KXHIGHLAX',
                'TIMEZONE': 'America/Los_Angeles',
                'URL': 'https://www.weather.gov/wrh/timeseries?site=KLAX&hours=3',
                'XML_URL': 'https://forecast.weather.gov/MapClick.php?lat=33.9425&lon=-118.409&FcstType=digitalDWML',
            }
        }
        self.city = None  # Initialize city
        self.lr_length = None
        self.scraping_hours = None
        self.trade_execution_hours = None

    def user_input(self):
        while True:
            self.city = input("City (DENVER, CHICAGO, MIAMI, AUSTIN, PHILADELPHIA, LOS ANGELES): ").upper() # .upper() for case-insensitivity
            if self.city in self.all_markets:  # Validate city input
                print(f"Selected City: {self.city}")
                self.market = self.all_markets[self.city]
                break # Exit loop if city is valid
            else:
                print("Invalid city. Please choose from the list.")

        while True:  # Loop for lr_length input
            try:
                self.lr_length = int(input('Linear Regression Length: '))
                print(f"LR Length: {self.lr_length}")
                break  # Exit loop if input is valid
            except ValueError:
                print("Invalid input. Please enter an integer.")

        while True: # Loop for scraping_hours input
            try:
                self.scraping_hours_str = input('Scraping Hours (e.g., 8,17): ') #Get string input first
                self.scraping_hours = tuple(map(int, self.scraping_hours_str.split(','))) #Split and convert to tuple of ints
                print(f"Scraping Hours: {self.scraping_hours}")
                break
            except ValueError:
                print("Invalid input. Please enter comma-separated integers.")

        while True: # Loop for trade_execution_hours input
            try:
                self.trade_execution_hours_str = input('Trading Execution Hours (e.g., 9,16): ')
                self.trade_execution_hours = tuple(map(int, self.trade_execution_hours_str.split(',')))
                print(f"Trading Execution Hours: {self.trade_execution_hours}")
                break
            except ValueError:
                print("Invalid input. Please enter comma-separated integers.")
                    
                