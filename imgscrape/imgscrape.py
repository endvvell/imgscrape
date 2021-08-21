#!/usr/bin/env python3
import bs4, requests, os, sys, re

def imgScrape(url):
# get requested page
    userUrl = requests.get(url)
    if userUrl.status_code == 200:   # check if request was successful
        imgGet = bs4.BeautifulSoup(userUrl.text, "html.parser")
        imgElem = imgGet.find_all("img",{"src":True})   # get elements from the parsed page

# check if anything was found
        if (len(imgElem) != 0):
            imgList = []
            for x in imgElem:   # check if found files are of suitable format
                if ("." in (x['src'])):
                    imgList.append(x['src'])   # put found items in a list
            if not imgList:
                print("Found some image files, but none of suitable format. Website might be blocking scraping attempts.")
            else:
                print("Found following files:")
                print(";\n".join(imgList), "\n")

# create folder for found files
                if not os.path.exists("./imgFiles"):
                    os.makedirs("imgFiles")
                os.chdir("./imgFiles")

# find and write files to folder - function
                def fwFiles(IMGS, URL):
    # trying to find correct path to image
                    def tryingFunc(PATH):
        # write binary image data to file - function
                        def writeFunc(PATH):
                                with open("img" + str(PATH).replace("/", "-"), "wb") as imgSave:    #open stream
                                    print(f"{imgWeb} - Success")    # progress confirmation
                                    imgSave.write(imgWeb.content)   # write to the stream in binary (wb)
                                    
                        imgWeb = requests.get(PATH)
                        print(f"Trying : {PATH}", end=" - ")
                        if imgWeb.status_code == 200:
                            writeFunc(PATH)
                        elif imgWeb.status_code == 404: # re-trying assuming domain to be root
                            print(f"{imgWeb} - Failed (Wrong Path)")
                            rURL = (str(URL).split("/",3))[:-1]
                            rURL = "/".join(rURL)
                            try:    # in case previously added trailing "/" was removed from URL by the code above and image path doesn't start with "/"
                                imgWeb = requests.get(rURL + IMGS[e])
                            except:
                                rURL = rURL + "/"
                                imgWeb = requests.get(rURL + IMGS[e])
                            print(f"*Again : {rURL + IMGS[e]}", end=" - ")
                            if imgWeb.status_code == 200:
                                writeFunc(PATH)
                            else:
                                print(f"{imgWeb} - Failed\n")
                        else:
                            print(f"{imgWeb} - Failed\n")

                    for e in range(len(IMGS)):  # additional filters for the code above
                        slashDupe = re.findall(r"(/{2,})", IMGS[e]) #   if the image is on sub-domain: remove preceding slashes
                        if (str(IMGS[e]).startswith("http")):
                            tryingFunc(IMGS[e])
                        elif (".html" in URL) or (".php" in URL):
                            URL = (str(URL).split("/"))
                            URL = "/".join(URL) + "/"
                            if (str(IMGS[e]).startswith(".")):
                                IMGS[e] = str(IMGS[e])[1:]
                                tryingFunc(URL + IMGS[e])
                        elif (str(IMGS[e]).startswith(".")):
                            IMGS[e] = str(IMGS[e])[1:]
                            tryingFunc(URL + IMGS[e])
                        elif len(slashDupe) > 0:
                            if str(IMGS[e]).startswith(slashDupe[0]):
                                imglen = len(IMGS[e]) - len(slashDupe[0])
                                IMGS[e] = IMGS[e][-imglen:]
                                tryingFunc(("http://" + IMGS[e]))
                        else:
                            tryingFunc(URL + IMGS[e])

                print("Progress:")
                try:
                    fwFiles(imgList, url)
                except:
                    print("* Issue with image URL, trying with added \"/\"...")
                    url = url + "/"
                    fwFiles(imgList, url)
                print("\nDone.\n")
        else:
            print("Found no files to download. Website might be blocking scraping attempts.")
    elif (userUrl.status_code == 403):
        print(f"Request was not successful - Error code: {userUrl.status_code} - Forbidden")
    else:
        print(f"Request was not successful - Error code: {userUrl.status_code}")


# get user input, adjust if needed
while(True):
    if len(sys.argv) > 1:   #adding ability to pass URL as an argument to the script
        userI = sys.argv[1]
    else:
        userI = input("Please enter a URL to scrape for images: ")
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
