FROM python:3.9.16-slim-buster

WORKDIR /docker_stock_crawler
 
COPY . .
# ADD . .

RUN pip install -r requirements.txt

CMD ["python", "stockCrawler.py"]


