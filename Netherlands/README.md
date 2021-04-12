## TripAdvisor scraper for whole Netherlands   
A TripAdvisor scraper app, that will help you to scrape all the details about restaurants in the Netherlands.
The details include Name, Location, Rating, No.of reviews, Cuisine type, Website of the restaurant, Email, Phone number, etc.   
The python packages used to scrape are **BeautifulSoup and Selenium**. 
Selenium is used to scrape the website and email information of the restaurant and BeauitfulSoup is used to scrape the rest of the details.  
Firstly, run "extracting_All_citylinks.py" to have citylinks.csv as output.
Then, run "TripAdvisor_v2.py" to scrape all of restaurants in Netherlands. This file takes citylinks.csv as input and gives two excel files as output.  
Restaurant_TripAdvisor_Netherlands.csv is the concatenation of those outputs which include 17000 restaurants.
