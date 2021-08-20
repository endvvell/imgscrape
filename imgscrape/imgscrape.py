#!/usr/bin/env python3
import bs4, requests, os, sys

from requests.api import request

def imgScrape(url):
    userUrl = requests.get(url) # get requested page

    if userUrl.status_code == 200: # check if request was successful
        imgGet = bs4.BeautifulSoup(userUrl.text, "html.parser")
        imgElem = imgGet.find_all("img",{"src":True}) # get elements from the parsed page

        if (len(imgElem) != 0): # check if anything was found
            imgList = []
            for x in imgElem:
                if ("." in (x['src'])): # check if found files are suitable
                    imgList.append(x['src']) # put found items in a list
            if not imgList:
                print("Found some image files, but none of suitable format. Website might be blocking scraping attempts.")
            else:
                print("Found following files:")
                print(";\n".join(imgList), "\n")

                if not os.path.exists("./imgFiles"): # create folder for found files
                    os.makedirs("imgFiles")
                os.chdir("./imgFiles")
#
                # find and write files to folder
                def writeFiles(IMG, URL):
                    # trying to guess full path to image
                    def tryingFunc(PATH):
                        imgWeb = requests.get(PATH)
                        print(f"Trying : {PATH}", end=" - ")
                        if imgWeb.status_code == 200:
                            with open("img" + str(PATH).replace("/", "-"), "wb") as imgSave: #open stream
                                print(f"{imgWeb} - Success") # progress confirmation
                                imgSave.write(imgWeb.content) # write to the stream in binary (wb)
                        elif imgWeb.status_code == 404: # re-trying assuming domain to be base
                            print(f"{imgWeb} - Failed (Wrong Path)")
                            rURL = (str(URL).split("/",3))[:-1]
                            rURL = "/".join(rURL) + "/"
                            imgWeb = requests.get(rURL + IMG[e])
                            print(f"*Again : {rURL + IMG[e]}", end=" - ")
                            if imgWeb.status_code == 200:
                                with open("img" + str(PATH).replace("/", "-"), "wb") as imgSave:
                                    print(f"{imgWeb} - Success\n")
                                    imgSave.write(imgWeb.content)
                            elif imgWeb.status_code == 404:
                                print(f"{imgWeb} - Failed (Wrong Path)\n")
                            else:
                                print(f"{imgWeb} - Failed\n")
                        else: # all attempts failed - proceeding to next
                            print(f"{imgWeb} - Failed")
#
                    for e in range(len(IMG)):
                        if (str(IMG[e]).startswith("http")):
                            tryingFunc(IMG[e])
                        elif (".html" in URL) or (".php" in URL):
                            URL = (str(URL).split("/"))[:-1]
                            URL = "/".join(URL) + "/"
                        elif (str(IMG[e]).startswith(".")):
                            IMG[e] = str(IMG[e])[1:]
                            tryingFunc(URL + IMG[e])
                        else:
                            tryingFunc(URL + IMG[e])
#                            
                print("Progress:")
                try:
                    writeFiles(imgList, url)
                except:
                    print("* Issue with URL, trying with added trailing \"/\"...")
                    url = url + "/"
                    writeFiles(imgList, url)
                print("\nDone.\n")
        else:
            print("Found no files to download. Website might be blocking scraping attempts.")
    elif (userUrl.status_code == 403):
        print(f"Request was not successful - Error code: {userUrl.status_code} - Forbidden")
    else:
        print(f"Request was not successful - Error code: {userUrl.status_code}")


while(True):
    if len(sys.argv) > 1:
        userI = sys.argv[1]
    else:
        userI = input("Please enter a url to scrape for images: ")
        userI = userI.strip()

    # check if protocol is mentioned in the url for parser to work
    if ("https://" not in userI[:8]) and ("http://" not in userI[:7]):
            print("* Protocol not specified, assuming 'http://'")
            userI = "http://" + userI
    if (userI.endswith("/")):
        userI = userI[:-1]
    print("\nWebpage to scrape:")
    print(userI, "\n")

    # Showtime!
    try:
        imgScrape(userI)  
    except:
        print("Sorry, something went wrong or the script got interrupted. Please make sure URL is spelled correctly.")
    break
