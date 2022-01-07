from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class': 'table table-striped table-hover table-hover-solid-row table-simple history-data'})
row = table.find_all('td')

row_length = len(row)

#initiating a tuple
tanggal_temp = []
harga_temp = []

for i in range(0, row_length):

    #scrapping process
    
    #get tanggal
    if i in range (0, row_length, 4):
        tanggal = tanggal_temp.append(row[i].get_text())
    
    #get harga 
    if i in range (2, row_length, 4):
        harga = harga_temp.append(row[i].get_text())

tanggal_temp = tanggal_temp[::-1]
harga_temp = harga_temp[::-1]

#change into dataframe
df = pd.DataFrame()
df['Tanggal'] = tanggal_temp
df['Harga'] = harga_temp

#insert data wrangling here
df['Harga'] = df['Harga'].str.replace(",","")
df['Harga'] = df['Harga'].str.replace("IDR","")
df['Harga'] = df['Harga'].astype('float64')
df['Tanggal'] = df['Tanggal'].astype('datetime64')

df = df.set_index('Tanggal')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Harga"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)