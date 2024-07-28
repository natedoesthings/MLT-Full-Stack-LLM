import requests

class SecEdgar:

  def __init__(self, fileurl):
    self.fileurl = fileurl

    self.name_dict = {}
    self.ticker_dict = {}

    self.headers = {'user-agent': 'MLT NA nathanaeldtesfaye@gmail.com'}
    r = requests.get(fileurl, headers=self.headers)

    self.file_json = r.json()

    self.__cik_json_to_dict()

  # Private method to convert the json file to a dictionary
  def __cik_json_to_dict(self):
    for _, entry in self.file_json.items():
        name = entry['title']
        ticker = entry['ticker']
        cik = entry['cik_str']

        if name and cik:
          self.name_dict[name] = (cik, name, ticker)
        if ticker and cik:
          self.ticker_dict[ticker] = (cik, name, ticker)

  
  def name_to_cik(self, name):
    if name in self.name_dict:
      return self.name_dict[name]
    
    else:
      print("Name not in dictionary")
      return None
  
  def ticker_to_cik(self, ticker):
    if ticker in self.ticker_dict:
      return self.ticker_dict[ticker]
    
    else:
      print("Ticker not in dictionary")
      return None
    


if __name__ == '__main__':
  se = SecEdgar('https://www.sec.gov/files/company_tickers.json')

  # Test
  print(se.name_to_cik('Apple Inc.'))
  print(se.ticker_to_cik('AAPL'))



    

