"""
Web Scraper to extract movies data from "www.rottentomatoes.com/browse/movies_at_home/".

Author: Maria Dancianu
"""

from bs4 import BeautifulSoup
import pandas as pd 
from time import sleep 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")


def get_homepage_url_soup(url, 
                          load_more_data=True,
                          num_load_more_data_clicks=4, 
                          crawling_delay=5):
    """Opens the website and returns a BeautifulSoup object.
    
    Args:
      homepage_url: string
          URL of the website to be scraped. 
      load_more_data: boolean, optional, Default=True
          Boolean variable to indicate whether to click on the 'LOAD
          MORE' button to extract more movies. 
      num_load_more_data_clicks: int, optional, Default = 1
          Number of clicks on the "LOAD MORE" button. 
      crawling_delay: int, optional, Default = 5  
          Waiting time, in seconds, before crawling the website page. 
          This is required to avoid causing performance issues to the 
          website. 
      
    Returns: 
      soup: BeautifulSoup object
          BeautifulSoup object representing the page to be scraped. 
    """
    
    sleep(crawling_delay)
    
    browser = webdriver.Chrome(options=options)
    browser.get(url)
   
    if load_more_data:
        print("Loading more data")
        
        load_more_button_css_selector = '#main-page-content > div.discovery > div.discovery__actions > button'
            
        for i in range(0, num_load_more_data_clicks):
            sleep(crawling_delay)
            print("Click on 'LOAD MORE' button")
            
            element = browser.find_element(By.CSS_SELECTOR, load_more_button_css_selector)
            
            browser.execute_script("arguments[0].click();", element)

    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    return soup


def get_url_soup(url, crawling_delay=5):
    """Opens the website and returns a BeautifulSoup object.
    
    Args:
      homepage_url: string
          URL of the website to be scraped. 
      crawling_delay: int, optional, Default = 5  
          Waiting time, in seconds, before crawling the website page. 
          This is required to avoid causing performance issues to the 
          website. 
      
    Returns: 
      soup: BeautifulSoup object
          BeautifulSoup object representing the page to be scraped. 
    """
    
    sleep(crawling_delay)
    
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    return soup


def get_movie_data(movie_soup):
    """Extracts the data of a single movie. 
    
    Args:
      movie_soup: BeautifulSoup object
          BeautifulSoup object of one single movie. 
          
    Returns:
       output_dict: dictionary 
          Dictionary with the movie data. 
    """
    
    movie_title = movie_soup.find("h1", slot='title').string
    
    movie_info = movie_soup.findAll('li', attrs={'class': 'info-item'})
    
    # by default we keep None if one element is not found 
    output_dictionary = {
        'Title': movie_title,
        'Genre': None,
        'Original Language': None,
        'Director': None,
        'Producer': None, 
        'Writer': None, 
        'Release Date (Theaters)': None,
        'Release Date (Streaming)': None, 
        'Runtime': None, 
        'Distributor': None
    }

    for info in movie_info:
        movie_info_label = info.findAll('b', attrs={'data-qa': 'movie-info-item-label'})
        movie_info_label = movie_info_label[0].text

        movie_info_label = movie_info_label.replace(":", "")

        if movie_info_label in output_dictionary.keys():
            movie_info_value = info.findAll('span', attrs={'data-qa': 'movie-info-item-value'})

            # avoids for instance having \xa0 in the text (Unicode character representing non-breaking space)
            # common when parsing HTML files using BeautifulSoup 
            movie_info_value = movie_info_value[0].get_text(strip=True)
            
            if movie_info_label == 'Genre':
                movie_info_value = movie_info_value.split(",")
                movie_info_value = [s.replace('\n', '') for s in movie_info_value]
                movie_info_value = [s.rstrip() for s in movie_info_value]
                movie_info_value = [s.lstrip() for s in movie_info_value]
            
            output_dictionary[movie_info_label] = movie_info_value

    return output_dictionary


def MoviesDataScraper():
    """Extracts movies data.
    
    Returns:
        None but saves a csv with the extracted data.
    """
    
    all_movies_list = []
    
    root_url = 'https://www.rottentomatoes.com/'
    homepage_url = "https://www.rottentomatoes.com/browse/movies_at_home/"
    
    soup = get_homepage_url_soup(homepage_url)
    
    all_movies = soup.findAll('tile-dynamic')
     
    print(f'Found {len(all_movies)} movies to be scraped!')
    
    for movie in all_movies:
        movie_urls = movie.findAll('a', href=True)
         
        # skip the movie is no URL is found 
        if len(movie_urls) == 0:
            continue 

        movie_url = movie_urls[0]['href'][1:]
        movie_url = f'{root_url}{movie_url}'
        
        movie_soup = get_url_soup(movie_url)
        
        movie_output_dict = get_movie_data(movie_soup)
        
        all_movies_list.append(movie_output_dict)

    results_df = pd.DataFrame(all_movies_list)  
    
    results_df.to_csv("rottentomatoes_movies.csv")
    

if __name__ == '__main__':
    MoviesDataScraper()
