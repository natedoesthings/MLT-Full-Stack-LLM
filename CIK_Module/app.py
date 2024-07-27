import requests

class SecEdgar:

  def __init__(self, fileurl):
    self.fileurl = fileurl

    self.name_dict = {}
    self.ticker_dict = {}

    headers = {'user-agent': 'MLT NA nathanaeldtesfaye@gmail.com'}
    r = requests.get(fileurl, headers=headers)

    self.filejson = r.json()

    print(r.text)
    print(self.filejson)

    self.cik_json_to_dict()


  def cik_json_to_dict(self):

    for _, entry in self.filejson.items():
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


# se = SecEdgar('https://www.sec.gov/files/company_tickers.json')

# # Test
# print(se.name_to_cik('Apple Inc.'))
# print(se.ticker_to_cik('AAPL'))

def rewrite_accessionNumber(asscessionNumber):
  return asscessionNumber.replace('-', '')


def annual_filing(cik, year):
  url = f'https://data.sec.gov/submissions/CIK{cik}.json'
  headers = {'user-agent': 'MLT NA nathanaeldtesfaye@gmail.com'}

  r = requests.get(url, headers=headers)


  if r.status_code == 200:

    accessionNumber = None
    primaryDocument = None

    filejson = r.json()
    filings = filejson['filings']['recent']

    accessionNumbers = filings['accessionNumber']
    primaryDocuments = filings['primaryDocument']
    forms = filings['form']
 
    for i in range(len(forms)):
      if forms[i] == '10-K' and accessionNumbers[i].split('-')[1] == year[2:]:
        accessionNumber = accessionNumbers[i]
        primaryDocument = primaryDocuments[i]
        break
    
    accessionNumber = accessionNumber.replace('-', '')

    print(f'Accession Number: {accessionNumber}')
    print(f'Primary Document: {primaryDocument}')

    url = f'https://www.sec.gov/Archives/edgar/data/{cik}/{accessionNumber}/{primaryDocument}'

    print(url)
      
    r = requests.get(url, headers=headers)
    return r.text

  else:
    print("Request failed")
    return None
    
      
# Test
annual_filing('0000320193', '2018')
