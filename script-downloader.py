from bs4 import BeautifulSoup
from datetime import date
import os.path
from urllib.request import Request, urlopen
import os
import csv
from time import time

path = os.path.dirname(__file__)
os.chdir(path)

headers = {'User-Agent': 'Mozilla/5.0'}


def url_fetch(i=0, headers=headers):
    url = "https://www.donedeal.ie/cars/"+make+"/"+model+"/"+fueltype+keywords+"start="+str(i*30)+"&"+yearfrom+"&"+yearto+"&"+"engine_from="+enginesizefrom+"&"+"engine_to="+enginesizeto

    req = Request(url, headers=headers)
    req = urlopen(req)
    webContent = req.read().decode('UTF-8')

    doc = BeautifulSoup(webContent, 'html.parser')
    return doc
    


# Search Logic

saved_search = str(input("Do you have a saved search?: Y/N: "))

while saved_search == "N":

    make = input("Make: ")
    model = input("Model: ")
    
    fueltype = "X"
    while fueltype != "Petrol?" and fueltype != "Diesel?":     
        fuelchoice = input("Fuel Type: A = Petrol B = Diesel: ")
        
        if fuelchoice == "A":
            fueltype = "Petrol?"  
        elif fuelchoice == "B":
            fueltype = "Diesel?"    
        else:
            print("Wrong Input")

    enginesizefrom = input("Engine Size From (in cc's, example: 1200): ")
    enginesizeto = input("Engine Size To: ")

    yearfrom = "year_from=" + str(input("Year From: "))
    yearto = "year_to=" + str(input("Year To: "))

    keyword = input("OPTIONAL: Key Words? Suggested: 335i, GTI, M3, etc. One word only. ")
    
    if keyword != "":
        keywords = "words=" + keyword + "&"
    else:
        keywords = ""


    doc = url_fetch(0)

    error = doc.find("h2", class_="styles__Header-sc-dhlpsy-2 knmJSx")
    
    if error == None:
        saved_search = None
        search_complete = True
    else: 
        print("You've made an error in your selection, perhaps the make and model are wrong? Or there's none for sale.") 
     


# Saving Logic

if saved_search == None:
    check2 = str(input("Would you like to save your search?, Y/N: "))

    texts = []
    if check2 == "Y":

        if os.path.isfile("saved-searches.csv") == True:
            with open("saved-searches.csv", "r") as f:
                for words in f.readlines():
                    if words != "\n":
                        texts.append(words)
        
                f.close()

        with open("saved-searches.csv", "a") as f:
            writer = csv.writer(f)
            search = [int(len(texts)), make, model, fueltype, enginesizefrom, yearfrom, yearto, enginesizeto, keyword]
            writer.writerow(search)



if saved_search == "Y":

    print("Select a search using the number:")

    print("_______________________________________________________________________")


    texts = []
    with open("saved-searches.csv", "r") as f:
        for words in f.readlines():
            if words != "\n":
                texts.append(words.rstrip())
    
    for searches in texts:
        print(searches.rstrip())


    selection = int(input())
    search = texts[selection]

    search = search.split(",")
    

    
    make = search[1]
    model = search[2]
    fueltype = search[3]
    enginesizefrom = search[4]
    yearfrom = search[5]
    yearto = search[6]
    if search[8] != "":
        keywords = "words=" + search[8] + "&"
    else:
        keywords = ""
    enginesizeto = search[7]


doc = url_fetch(0)

print("Please wait...")

if os.path.isdir("saved-cars") == False:
    os.mkdir("saved-cars")
    os.chdir(path + "/saved-cars")
else:
    os.chdir(path + "/saved-cars")


# This block of texts gets me the amount of ads posted for this specific car


tags = doc.find("h2", class_="styles__Details-sc-gp61km-12 bSMUto")
ads = tags.get_text() 
ads = ads.split()[0]

print(ads)



links = []
i = 0
while i <= int(ads) // 30:
    
    doc = url_fetch(i)

    rawlinks = []
    for a in doc.find_all('a', class_="Link__SLinkButton-sc-9jmsfg-0 emzqZy SearchCardstyled__CardLink-sc-19e3gpz-4 fkYVTG", href=True):
        rawlinks.append( a['href'])

    z = 0
    while z < len(rawlinks):
        links.append(rawlinks[z])
        z += 2

    i += 1

# CSV LOGIC

print(links)

i = 0

print("CSV File Name (keep the naming consistent if you want to add to the file)")

print("Cars tracked:")
print(os.listdir())

csv_file = input() + ".csv"
csv_columns = ["Make", "Model", "Year", "Mileage", "Colour", "NCT Expiry", "Price", "URL"]

start_time = time()

urls = []

with open(csv_file, 'a') as f:
    writer = csv.writer(f)
    if os.stat(csv_file).st_size == 0:
        writer.writerow(csv_columns)
    else:
        filename = open(csv_file, "r")
        file = csv.DictReader(filename)
        for col in file:
            urls.append(col["URL"])

    i = 0

    for url in links:
        
        response = urllib.request.urlopen(url)
        webContent = response.read().decode('UTF-8')

        doc = BeautifulSoup(webContent, 'html.parser')

        keyinfo = doc.find_all("div", class_="KeyInfoList__Text-sc-sxpiwc-2 dGjCWx")
        resultsinfo = doc.find_all("div", class_="KeyInfoList__Text-sc-sxpiwc-2 dQdfES")

        price = doc.find("p", class_="Price__CurrentPrice-sc-e0e8wj-0 jsgPAs")

        keys = []
        for key in keyinfo:
            keys.append(key.text)
        
        keys.append("Price")
        keys.append("URL")


        results = []
        for result in resultsinfo:
            results.append(result.text)
        
        results.append(price.text)
        results.append(url)


        table = {}
        for z, key in enumerate(keys):
            table[key] = results[z]
            z += 1
        

        tablekey = []
        for key in table:
            tablekey.append(key)


        z = 0
        results = []    
        for result in tablekey:
            if result in csv_columns:
                results.append(table[result])
            
            z += 1

        if url not in urls:
            writer.writerow(results)
        
        i += 1

        if i % 10 == 0:
            print(str(round((i / len(links)) * 100)) + "% " + "Done")



end_time = time()


print("Parsing Time:", end_time - start_time)
print("Done!")

