# Rottentomatoes-Web-Scraper
A web scraper to extract movies data from [www.rottentomatoes.com](https://www.rottentomatoes.com/). 

This project contains an interaction with the target website to click on a button and load more movies before calling the movies scraper.  
  
The first step is to find the exact location of the element to be clicked. This is done through the element CSS locator, that can be found by clicking on *Copy* --> *Copy selector*.

![alt text](https://github.com/mariadancianu/Rottentomatoes-Web-Scraper/blob/main/load_more_button_css_selector_copy.png)

## Output dataset 
![alt text](https://github.com/mariadancianu/Rottentomatoes-Web-Scraper/blob/main/rottentomatoes_output_example.png)

## Technologies 

Python version: 3.11. 

Python libraries:
- BeautifulSoup
- selenium
- pandas
- time

## Learning points 
- inspect the structure of the html page from which to scrape the data and identify the required elements
- getting familiar with the selenium library 
- extract URLs from the main page, open them and extract additional information from these pages 
- using a crawling delay to avoid performance issues for the scraped website 
- **interact with the website by clicking on a button** to load more movies 

## Status
Project is: *done*. 

## Warnings
The websites structure changes in time and a Web Scraper that was previously working perfectly can break due to these updates. The code must be maintained and updated by running periodical tests. Small adjustments are usually required since the websites changes are small and incremental. I will try to update the code periodically but keep in mind that any errors are part of the Web Scraping process.

## Contact 
Created by mary_0094@hotmail.it, feel free to get in touch! :woman_technologist:
