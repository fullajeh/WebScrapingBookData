
#Jehlyen Fuller

#Simple Web Scraping Tool to Sort Book Names, and their Corresponding Prices in a Table

import pandas as pd 
from bs4 import BeautifulSoup as soup
import requests
import matplotlib.pyplot as plt

data = []
url = 'https://books.toscrape.com/' # Website We're going to Scrape
 
response = requests.get(url, timeout=10) # Send a request to the URL, and timeout if we wait more than 10 seconds.
response.raise_for_status()

if response.status_code == 200: #200 means that the server is responding to our request, allowing us to scrape data.
	print("Ready to Extract Data")
	site_data = soup(response.content, 'html.parser') #Convert the content to JSON for Python to read it easier.

	products = site_data.find_all("article", class_="product_pod") # The books are stored in article blocks with the class "product_pod"
	if products:
		print("Found products")
		for item in products:
			item_name = item.find("h3").get_text(strip=True) # This is the book's name
			item_price = item.find('p', class_="price_color").text.strip() # This is the book's price
			
			# Lets get the ratings per book
			item_rating = item.p.get("class")
			rating = item_rating[1]

			#Change the Words to Numbers
			if str(rating).lower() == "one":
				rating = 1
			elif str(rating).lower() == "two":
				rating = 2
			elif str(rating).lower() == "three":
				rating = 3
			elif str(rating).lower() == "four":
				rating = 4
			else:
				rating = 5

			# Add all of the data to the data list we made earlier
			data.append([item_name, item_price, int(rating)]) # Lets add it to our list for now, we'll make it a DataFrame later

			
			
else:

	print("Error Occurred") # If the server responds with any other code, it's likely an error and we cannot continue

print("Data Table: ", data)
book_dataframe = pd.DataFrame(data, columns=["Book Name", "Price", "Rating"]) # Convert this to a DataFrame with Columns
book_dataframe.drop_duplicates(inplace=True) # Get rid of any duplicate books
book_dataframe.dropna(inplace=True) # Get rid of any empty books (no title, or price)
book_dataframe["Price"].astype(str) # Convert the prices to string so we can alter the price formatting
book_dataframe['Price'].str.replace("Â","£", "", regex=False) # Remove the AE the list originally gives us

print(book_dataframe,'\n')

# Lets Sort the Books by Ratings

ratings = book_dataframe.sort_values(by="Rating", ascending=False)

# Print the Count of the 5 Star Rated Books
print(len(ratings[ratings['Rating'] >= 5]))

# Lets make a pie chart based on the percentages of each rating
five_stars = len(ratings[ratings['Rating'] == 5])
four_stars = len(ratings[ratings['Rating'] == 4])
three_stars = len(ratings[ratings['Rating'] == 3])
two_stars = len(ratings[ratings['Rating'] == 2])
one_star = len(ratings[ratings['Rating'] == 1])

sizes = [five_stars, four_stars, three_stars, two_stars, one_star]
categories = ['Five Star Rated Books','Four Star Rated Books','Three Star Rated Books','Two Star Rated Books','One Star Rated Books']
colors = ["#D6EAF8",  # very light pastel blue
          "#AED6F1",  # light pastel blue
          "#85C1E9",  # soft sky blue
          "#5DADE2",  # medium pastel blue
          "#3498DB"]  # deeper pastel blue
explode = (0,0,0,0,0.1) # Explode (Slightly Seperate) One Star Rated Books on the Pie Chart
plt.pie(sizes, labels=categories, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90, explode=explode)
plt.title("Book Ratings by Percentages")
plt.show()
