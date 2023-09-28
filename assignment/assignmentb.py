import requests
from bs4 import BeautifulSoup
from models import Book
from mongoengine import connect
from db import connect_to_database
from dotenv import load_dotenv
import os

load_dotenv()
# Establish the database connection
connect(
    db="TailNode",  
    host=os.environ.get('MongoURL'),
)
db_client = connect_to_database()

def scraping_book():
   
     base_url = "http://books.toscrape.com"
     page_number = 1

     while True:
      if db_client:
       # GET request to the URL
       response = requests.get(f"{base_url}/catalogue/page-{page_number}.html")

      # Check if the request was successful
      if response.status_code == 200:
      # Parse the HTML content of the page using BeautifulSoup
       soup = BeautifulSoup(response.text, "html.parser")

    
      # find all relevant tags and add their text content, save into array.
       paragraphs = soup.find_all("a" , title=True)
       img_tags = soup.find_all('img',class_='thumbnail')
       price_tags = soup.find_all('p', class_='price_color')
       availability_tags = soup.find_all('p', class_='instock availability')
       rating_tags = soup.find_all('p', class_='star-rating')

       titles = [a["title"] for a in paragraphs]
       image_urls = [img['src'] for img in img_tags]
       prices = [price_tag.text for price_tag in price_tags]
       availabilitys = [availability_tag.get_text(strip=True) for availability_tag in availability_tags]
       ratings = [rating_tag['class'][1] for rating_tag in rating_tags]
      
     #  loop over array and create instance of Book and save that instance into database.
       for i in range(len(titles)): 
        book=Book(title=titles[i],image=image_urls[i],price=prices[i],availability=availabilitys[i],rating=ratings[i])
        book.save()

        # Check if there is a "Next" button to go to the next page
       next_button = soup.find("li", class_="next")
       if next_button:
            print(f"completed scraping of pageNo. {page_number}")
            page_number += 1
            
       else:
            print("completed scraping of pageNo. 50")
            print("All data of the Books added into the database")
            break  # No more pages to scrape, exit the loop
      else:
          print("Failed to retrieve the web page. Status code:", response.status_code)


if __name__=='__main__':
   scraping_book()