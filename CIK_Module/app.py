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
    
  # Private Helper Method to determine if a month is in a quarter
  def __quarter_helper(self, quarter, month):
    quarter = quarter.lower()

    if quarter == 'q1':
      return month == '03' or month == '04' or month == '05'
    elif quarter == 'q2':
      return month == '06' or month == '07' or month == '08'
    elif quarter == 'q3':
      return month == '09' or month == '10' or month == '11'
    elif quarter == 'q4':
      return month == '12' or month == '01' or month == '02'
    else:
      return False


  # Private Helper Method to get the filing information needed based on user input
  # Returns the accession number and primary document
  def __filing_helper(self, file_json, year, quarter = None):
    filings = file_json['filings']['recent']

    accessionNumbers = filings['accessionNumber']
    primaryDocuments = filings['primaryDocument']
    filingDates = filings['filingDate']
    primaryDocDescriptions = filings['primaryDocDescription']

    for i in range(len(primaryDocDescriptions)):
      if quarter:
        if primaryDocDescriptions[i] == '10-Q' and filingDates[i].split('-')[0] == year and self.__quarter_helper(quarter, filingDates[i].split('-')[1]):
          accessionNumber = accessionNumbers[i].replace('-', '')
          primaryDocument = primaryDocuments[i]
          return accessionNumber, primaryDocument
      else:
        if primaryDocDescriptions[i] == '10-K' and filingDates[i].split('-')[0] == year:
          accessionNumber = accessionNumbers[i].replace('-', '')
          primaryDocument = primaryDocuments[i]
          return accessionNumber, primaryDocument
      
  # Private Helper method that returns the html text of the filing
  def __file_report(self, cik, year, quarter = None):
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    r = requests.get(url, headers=self.headers)

    if r.status_code == 200:

      file_json = r.json()
      accessionNumber, primaryDocument = self.__filing_helper(file_json, year, quarter)
      url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{primaryDocument}'

      print(url)

      r = requests.get(url, headers=self.headers)
      return r.text

    else:
      print("Request failed")
      return None
  
  # Method to get the annual filing of a company
  def annual_filing(self, cik, year):
    return self.__file_report(cik, year)

  # Method to get the quarterly filing of a company
  def quarterly_filing(self, cik, year, quarter):
    return self.__file_report(cik, year, quarter)


if __name__ == '__main__':
  se = SecEdgar('https://www.sec.gov/files/company_tickers.json')

  # Test
  print(se.name_to_cik('Apple Inc.'))
  print(se.ticker_to_cik('AAPL'))
  annualDocument = se.annual_filing('0000320193', '2018')
  quarterlyDocument = se.quarterly_filing('0000320193', '2023', 'Q2')



    

