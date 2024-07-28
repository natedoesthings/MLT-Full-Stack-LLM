import requests

class SecEdgar:

  def __init__(self, fileurl):
    self.fileurl = fileurl

    self.name_dict = {}
    self.ticker_dict = {}

    self.headers = {'user-agent': 'MLT NA nathanaeldtesfaye@gmail.com'}
    r = requests.get(fileurl, headers=self.headers)

    self.file_json = r.json()

    self.cik_json_to_dict()


  def cik_json_to_dict(self):
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
    
  def quarter_helper(self, quarter, month):
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


    
  def filing_helper(self, file_json, year, quarter = None):
    filings = file_json['filings']['recent']

    accessionNumbers = filings['accessionNumber']
    primaryDocuments = filings['primaryDocument']
    filingDates = filings['filingDate']
    primaryDocDescriptions = filings['primaryDocDescription']

    for i in range(len(primaryDocDescriptions)):
      if quarter:
        if primaryDocDescriptions[i] == '10-Q' and filingDates[i].split('-')[0] == year and self.quarter_helper(quarter, filingDates[i].split('-')[1]):
          accessionNumber = accessionNumbers[i].replace('-', '')
          primaryDocument = primaryDocuments[i]
          return accessionNumber, primaryDocument
      else:
        if primaryDocDescriptions[i] == '10-K' and filingDates[i].split('-')[0] == year:
          accessionNumber = accessionNumbers[i].replace('-', '')
          primaryDocument = primaryDocuments[i]
          return accessionNumber, primaryDocument
      
    
      
    
  def annual_filing(self, cik, year):
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    r = requests.get(url, headers=self.headers)

    if r.status_code == 200:

      file_json = r.json()
      accessionNumber, primaryDocument = self.filing_helper(file_json, year)

      print(f'Accession Number: {accessionNumber}')
      print(f'Primary Document: {primaryDocument}')

      url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{primaryDocument}'

      print(url)

      r = requests.get(url, headers=self.headers)
      return r.text

    else:
      print("Request failed")
      return None

  def quarterly_filing(self, cik, year, quarter):
    url = f'https://data.sec.gov/submissions/CIK{cik}.json'
    r = requests.get(url, headers=self.headers)

    if r.status_code == 200:

      file_json = r.json()
      accessionNumber, primaryDocument = self.filing_helper(file_json, year, quarter)

      url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{primaryDocument}'

      print(url)

      r = requests.get(url, headers=self.headers)
      return r.text

    else:
      print("Request failed")
      return None


se = SecEdgar('https://www.sec.gov/files/company_tickers.json')

# Test
print(se.name_to_cik('Apple Inc.'))
print(se.ticker_to_cik('AAPL'))
annualDocument = se.annual_filing('0000320193', '2018')
quarterlyDocument = se.quarterly_filing('0000320193', '2023', 'Q2')



    

