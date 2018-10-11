# AmazonScraping
This spider crawl title, brand, price, price with discount of products on amazon.com.
Made pipeline to calculate price discount in % and add that to a returned item as separate field. 
Made scraper to be able to receive command line argument - make screenshot of the page if argument is supplied and save screenshot in .png


### Installation
$ pip install -r requirements.txt

### Run
- if arguments is supplied, spider take screenshot of webpage.

    ```scrapy crawl amazon_spider -a screenshot=True```
- Else

    ```scrapy crawl amazon_spider```
