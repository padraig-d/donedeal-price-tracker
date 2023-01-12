from bs4 import BeautifulSoup
from datetime import date
import os.path
import urllib.request
import os
import csv

os.chdir('C:/Users/Patrick#/Desktop/donedeal-script/downloaded-pages')


# Search Logic

# i = 0
# while i < 1: 

    # print("Where would you like to save the data? Input a valid directory")
    # directory = "r" + str(input())

#     print("Make")
#     make = input()

#     print("Model")
#     model = input()

#     print("Fuel Type: A = Petrol B = Diesel")
#     fueltype = "X"

#     while fueltype != "Petrol?" and fueltype != "Diesel?":
#         fuelchoice = input()
#         if fuelchoice == "A":
#             fueltype = "Petrol?"
#         elif fuelchoice == "B":
#             fueltype = "Diesel?"
#         else:
#             print("Wrong Input")

#     print("Engine Size")
#     enginesize = input()

#     print("OPTIONAL: Year From, Leave Blank If No")
#     yearfrom = "year_from=" + str(input())

#     print("OPTIONAL: Year To, Leave Blank If No")
#     yearto = "year_to=" + str(input())

#     print("OPTIONAL: Key Words? Suggested: 335i, GTI, M3, etc. One word only.")
#     keyword = input()

#     if keyword != "":
#         keywords = "words=" + keyword + "&"
#     else:
#         keywords = ""


#     if yearfrom != "" and yearto == "":
#          url = "https://www.donedeal.ie/cars/"+make+"/"+model+"?"+keywords+fueltype+"start="+str(i*30)+"&"+yearfrom+"&"+"engine_from="+enginesize
#     elif yearto != "" and yearfrom == "":
#         url = "https://www.donedeal.ie/cars/"+make+"/"+model+"?"+keywords+fueltype+"start="+str(i*30)+"&"+yearto+"&"+"engine_from="+enginesize
#     elif yearfrom != "" and yearto != "":
#         url = "https://www.donedeal.ie/cars/"+make+"/"+model+"?"+keywords+fueltype+"start="+str(i*30)+"&"+yearfrom+"&"+yearto+"&"+"engine_from="+enginesize


#     i += 1


#     response = urllib.request.urlopen(url)
#     webContent = response.read().decode('UTF-8')


#     doc = BeautifulSoup(webContent, 'html.parser')

#     fourohfour = doc.find("h2", class_="styles__Header-sc-dhlpsy-2 knmJSx")

#     if fourohfour == None:
#         i += 1
#     else: 
#         print("You've made an error in your selection, perhaps the make and model are wrong?")      


# if i == 1:
#     print("DONE")

i = 0



make = "BMW/"
model = "3-Series/"
fueltype = "Petrol?"
enginesize = "2000"
yearfrom = "year_from=2002"
yearto = "year_to=2010"

# URL LOGIC --- This will be taken out when program is finished.

name_of_file = "websitehtml_"
completeName = name_of_file+str(i)+".html"
url = "https://www.donedeal.ie/cars/"+make+model+fueltype+"start="+str(i*30)+"&"+"engine_from="+enginesize

if yearfrom != "" and yearto == "":
    url = "https://www.donedeal.ie/cars/"+make+model+fueltype+"start="+str(i*30)+"&"+yearfrom+"&"+"engine_from="+enginesize
elif yearto != "" and yearfrom == "":
    url = "https://www.donedeal.ie/cars/"+make+model+fueltype+"start="+str(i*30)+"&"+yearto+"&"+"engine_from="+enginesize
elif yearfrom != "" and yearto != "":
    url = "https://www.donedeal.ie/cars/"+make+model+fueltype+"start="+str(i*30)+"&"+yearfrom+"&"+yearto+"&"+"engine_from="+enginesize

# Sample URL
# https://www.donedeal.ie/cars/BMW/3-Series/Diesel?start=30&engine_from=2000
#                             /Make/Model  /Fuel  /Page     /Engine


response = urllib.request.urlopen(url)
webContent = response.read().decode('UTF-8')
    
doc = BeautifulSoup(webContent, 'html.parser')

# os.chdir(directory)
# os.mkdir("saved-cars")
# os.chdir("/saved-cars")





# ------------------------------------------------------------ This is reduntant.

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

    completeName = name_of_file+str(i)+".html"
    
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

csv_file = input() + ".csv"
csv_columns = ["Make", "Model", "Year", "Mileage", "Colour", "NCT Expiry", "Price", "URL"]

urls = []

with open(csv_file, 'a') as f:
    writer = csv.writer(f)
    if os.stat(csv_file).st_size == 0:
        writer.writerow(csv_columns)
        print("File is empty")
    else:
        print("File is not empty")
        filename = open("test.csv", "r")
        file = csv.DictReader(filename)
        for col in file:
            urls.append(col["URL"])



    while i < 10: # CHANGE LATER -----> len(links)
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



## NOTES

## What's left to do.

## CSV - MANDATORY

        # If time feautres aren't implemented, maybe have a column which says when the search was ran on?
        # This is so that at least we can have a historical price trend.

## Time features? 
        
        # Would be useful, but I need to phone a friend for that one.
        # If that is implemented, then implement a checker to see if an ad has been sold, if it has, we can 
        # mark when it was last seen. 

## SAVED LINKS SECTION

        # 