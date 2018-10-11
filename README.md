# AmazonScraping
This spider crawl title, brand, price, price with discount of products on amazon.com.
Made pipeline to calculate price discount in % and add that to a returned item as separate field. 
Made scraper to be able to receive command line argument - make screenshot of the page if argument is supplied and save screenshot in .png


### Installation
****``$ pip install -r requirements.txt****``


##### Installation of Splash 
1. Install Docker.
2. Pull the image:

    ****``$ sudo docker pull scrapinghub/splash``****
3. Start the container:
    
    ****``$ sudo docker run -p 8050:8050 -p 5023:5023 scrapinghub/splash``****
4. Splash is now available at 0.0.0.0 at ports 8050 (http) and 5023 (telnet).

### Run
- if arguments is supplied, spider take screenshot of webpage.

    ****```scrapy crawl amazon_spider -a screenshot=True```****
- Else

    ****```scrapy crawl amazon_spider```****
