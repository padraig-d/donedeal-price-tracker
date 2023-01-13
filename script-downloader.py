from bs4 import BeautifulSoup
from datetime import date
import os.path
import urllib.request
import os
import csv

path = os.path.dirname(__file__)
os.chdir(path)


# Search Logic

saved_checker = ""

print("Do you have a saved search?: Y/N")

check = str(input())

if check == "N":
    saved_checker = False
elif check == "Y":
    saved_checker = True

i = 0

if saved_checker == 0:

    while i < 1: 

        print("Make")
        make = input()

        print("Model")
        model = input()

        print("Fuel Type: A = Petrol B = Diesel")
        fueltype = "X"

        while fueltype != "Petrol?" and fueltype != "Diesel?":
            fuelchoice = input()
            if fuelchoice == "A":
                fueltype = "Petrol?"
            elif fuelchoice == "B":
                fueltype = "Diesel?"
            else:
                print("Wrong Input")

        print("Engine Size From:")
        enginesizefrom = input()

        print("Engine Size To:")
        enginesizeto = input()

        print("Year From")
        yearfrom = "year_from=" + str(input())

        print("Year To")
        yearto = "year_to=" + str(input())

        print("OPTIONAL: Key Words? Suggested: 335i, GTI, M3, etc. One word only.")
        keyword = input()

        if keyword != "":
            keywords = "words=" + keyword + "&"
        else:
            keywords = ""

        url = "https://www.donedeal.ie/cars/"+make+"/"+model+"/"+fueltype+keywords+"start="+str(i*30)+"&"+yearfrom+"&"+yearto+"&"+"engine_from="+enginesizefrom+"&"+"engine_to="+enginesizeto


        response = urllib.request.urlopen(url)
        webContent = response.read().decode('UTF-8')


        doc = BeautifulSoup(webContent, 'html.parser')

        fourohfour = doc.find("h2", class_="styles__Header-sc-dhlpsy-2 knmJSx")

        if fourohfour == None:
            i += 1
        else: 
            print("You've made an error in your selection, perhaps the make and model are wrong?") 
     


    if i == 1:
        print("DONE")

    print("Would you like to save your search?: Y/N")

    saving_checker = ""
    check2 = str(input())
    if check2 == "Y":
        saving_checker = True
    elif check2 == "N":
        saving_checker = False
    

    texts = []
    if saving_checker == True:

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

i = 0


texts = []
if saved_checker == True:

    print("Select a search using the number:")


    print("---------------------------------------------------------")

    with open("saved-searches.csv", "r") as f:
        for words in f.readlines():
            if words != "\n":
                texts.append(words)
    
    for searches in texts:
        print(searches.rstrip())

    selection = input()

    i = 0

    while i < len(texts):
        text = texts[i].split(",")

        if selection == text[0]:
            search = texts[i].rstrip()
            i += 20000

        i += 1

    search = search.split(",")
    
    
    print(search)
    
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

i = 0


url = "https://www.donedeal.ie/cars/"+make+"/"+model+"/"+fueltype+keywords+"start="+str(i*30)+"&"+yearfrom+"&"+yearto+"&"+"engine_from="+enginesizefrom+"&"+"engine_to="+enginesizeto

print(url)

response = urllib.request.urlopen(url)
webContent = response.read().decode('UTF-8')
    
doc = BeautifulSoup(webContent, 'html.parser')


if os.path.isdir("saved-cars") == False:
    os.mkdir("saved-cars")
else:
    os.chdir(path + "/saved-cars")


# This block of texts gets me the amount of ads posted for this specific car

tags = doc.find("h2", class_="styles__Details-sc-gp61km-12 bSMUto")
rawads = tags.get_text() 

z = 0
ads = []

while z < len(rawads):
    if ord(rawads[z]) <= ord("9") and ord("0") <= ord(rawads[z]):
       ads.append(rawads[z])
       z += 1 
    else:
        z +=1

ads = "".join(ads) # Gets me exact number of ads for this car

links = []
while i <= int(ads) // 30:
    
    response = urllib.request.urlopen(url)
    webContent = response.read().decode('UTF-8')
    
    doc = BeautifulSoup(webContent, 'html.parser')

    rawlinks = []
    for a in doc.find_all('a', class_="Link__SLinkButton-sc-9jmsfg-0 emzqZy", href=True):
        rawlinks.append( a['href'])

    z = 0
    while z < len(rawlinks):
        links.append(rawlinks[z])
        z += 2

    i += 1

# CSV LOGIC

i = 0

print("CSV File Name (keep the naming consistent if you want to add to the file")

print("Cars tracked:")
print(os.listdir())


csv_file = input() + ".csv"
csv_columns = ["Make", "Model", "Year", "Mileage", "Colour", "NCT Expiry", "Price", "URL"]

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



    while i < len(links):
        url = links[i]

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

        z = 0 
        table = {}
        while z < len(keys):
            table[keys[z]] = results[z]
            z += 1
        
        # print("Processing...")
        # print(table["Make"])
        # print(table["Model"])
        # print(table["Year"])
        # print(table["Mileage"])
        # print(table["NCT Expiry"] + " NCT EXPIRY")
        # print(table["Colour"] + " COLOUR")
        # print(table["Price"])
        # print(table["URL"])

        tablekey = []
        for key in table:
            tablekey.append(key)


        z = 0
        results = []    
        while z < len(tablekey):
            if tablekey[z] in csv_columns:
                results.append(table[tablekey[z]])
            
            z += 1

        if url not in urls:
            writer.writerow(results)

        print("Processing...")

        i += 1

print("Done.")

