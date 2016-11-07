import datetime
import requests
import csv
import urllib2
import json
from BeautifulSoup import BeautifulSoup

record = ("")

def findTable(soup, tableName):
	table = soup.find("table", {"id" : lambda L: L and L.endswith(tableName)})
	for row in table.findAll('tr')[1:]:
	    col = row.findAll('td')

	    componentes = col[0].text
	    cemgramas = col[1].text
	    recomendado = col[2].text
	    
	    if tableName == "Vitaminas":
	    	habitual = ""
	    else:
	    	habitual = col[3].text
	    
	    global record
	    record += ",".join((foodName, componentes, cemgramas, recomendado, habitual)) + "\n"
	return

alphabet = "abcdefghijklmnopqrstuvwxyz"

for letter in alphabet: 
	print letter + " - " + str(datetime.datetime.now())
	url = 'http://www.insa.pt/sites/INSA/Portugues/AreasCientificas/AlimentNutricao/AplicacoesOnline/TabelaAlimentos/PesquisaOnline/Paginas/ListaAlfabetica.aspx' + "?valorPes=" + letter
	response = requests.get(url)
	html = response.content

	soup = BeautifulSoup(html)

	table = soup.find('table', attrs={'class': 'tblPesquisas'}) #catch food table

	list_of_food = [] #food table

	for row in table.findAll('tr'): #each line
	    for cell in row.findAll('td'): #each column/cell
	        for link in cell.findAll('a'): #each reference with link
				foodRecord = (link['href'], link.contents[0])
				food = ",".join(foodRecord)
				list_of_food.append(food)

	#parse food link
	for food in list_of_food:
		url = food.split(',')[0]
		foodName = food.split(',')[1]

		response = requests.get(url)
		
		html = response.content
		soup = BeautifulSoup(html)

		findTable(soup, 'Energia')
		findTable(soup, 'Macroconstituintes')
		findTable(soup, 'AcidosGordos')
		findTable(soup, 'Colesterol')
		findTable(soup, 'Vitaminas')
		findTable(soup, 'Minerais')
	#	findTable(soup, 'Langual')

print "saving csv"
with open('listing.csv', 'w') as f:
    f.write(record.encode('utf-8'))
