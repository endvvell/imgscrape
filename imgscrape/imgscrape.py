#!/usr/bin/env python3
import bs4, requests, os, sys

def imgScrape(url):
    userUrl = requests.get(url) #get requested page

    if userUrl.status_code == requests.codes.ok: #check if request was successful
        imgGet = bs4.BeautifulSoup(userUrl.text, "html.parser")
        imgElem = imgGet.select("img") #get elements from the parsed page

        if (len(imgElem) != 0):# #check if anything was found
            imgList = []
            for x in imgElem:
                if ("." in (x['src'])): #check if found files are suitable
                    imgList.append(x['src']) #put found items in a list
            if not imgList:
                print("Found no suitable files to be download. Website might not allow scraping.")
            else:
                print("Found following files:")
                print(";\n".join(imgList), "\n")

                if not os.path.exists("./imgFiles"): #create folder for found files
                    os.makedirs("imgFiles")
                os.chdir("./imgFiles")

                #write files to folder
                def writeFiles(IMG, URL):
                    for e in range(len(IMG)): #if webpage doesn't have a base folder: try downloading from 'relative' root
                        if (".html" in URL) or (".php" in URL):
                            URL = (str(URL).split("/"))[:-1]
                            URL = "/".join(URL) + "/"
                            
                        imgWeb = requests.get(URL + IMG[e])
                        if imgWeb.status_code == requests.codes.ok:
                            with open("img" + str(IMG[e]).replace("/", "-"), "wb") as imgSave: #open stream
                                print(IMG[e]) #progress confirmation
                                imgSave.write(imgWeb.content) #write to the stream in binary (wb)
                print("Progress:")
                try:
                    writeFiles(imgList, url)
                except:
                    print("* Issue with URL, trying with added \"/\" on the end...")
                    url = url + "/"
                    writeFiles(imgList, url)
                print("\nDone.")
        else:
            print("Found no suitable files to download. Website might not allow scraping.")
    else:
        print("Request was not successful. Error code: {}".format(userUrl.status_code))

#check if any arguments to the script were supplied
while(True):
    if len(sys.argv) > 1:
        userI = sys.argv[1]
    else:
        userI = input("Please enter a url to scrape for images: ")
        userI = userI.strip()

    #check if protocol is mentioned in the url for parser to work
    if ("https://" not in userI[:8]) and ("http://" not in userI[:7]):
            print("* Protocol not specified, assuming 'http://'")
            userI = "http://" + userI
    print("Webpage to scrape:")
    print(userI, "\n")

    # Showtime!
    try:
        imgScrape(userI)
    except:
        print("Sorry, something went wrong or the script got interrupted. Please make sure URL is spelled correctly. Try adding a trailing '/' to the end of your URL.")
    break
