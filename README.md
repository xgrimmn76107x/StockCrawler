# StockCrawler

## Project Init Run

FirstRun with your stocks
```
python .\stockCrawler.py --initOrFill init --choosenStock 2330 2454 --startDate 2023-01-01 --endDate now --saveFileName testStock --queryType listed
```

then run the TWII
```
python .\stockCrawler.py --initOrFill init --choosenStock 2330 2454 --startDate 2023-01-01 --endDate now --saveFileName testStock --queryType TWII
```

## Fill missing stocks

```
python .\stockCrawler.py --initOrFill fill --choosenStock 2330 2454 --saveFileName testStock
```
