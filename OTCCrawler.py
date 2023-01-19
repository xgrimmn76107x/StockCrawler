import requests
from bs4 import BeautifulSoup



url = 'https://www.tpex.org.tw/web/emergingstock/single_historical/result.php?l=zh-tw'
payload = {
    'ajax':True,
    'input_month':'111/12',
    'input_emgstk_code':'7584'
}
res = requests.post(url, data=payload)
# data = res.json()
soupget = BeautifulSoup(res.text, "html.parser")
print(soupget.prettify())