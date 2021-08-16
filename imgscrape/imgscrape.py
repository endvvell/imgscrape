#!/usr/bin/env python3
import bs4, requests, os, re

def imgScrape(url):
    userUrl = requests.get(url) #get requested page

    if userUrl.status_code == requests.codes.ok: #check if request was successful
        imgGet = bs4.BeautifulSoup(userUrl.text, "html.parser")
        imgElem = imgGet.select("img") #get elements from the parsed page

        imgList = []
        for x in imgElem: #put found items in a list
            imgList.append(x['src'])
        print("Found following files:")
        print(";\n".join(imgList), "\n")

        if not os.path.exists("./imgFiles"): #create folder for found files
            os.makedirs("imgFiles")
        os.chdir("./imgFiles")

        print("Progress:")
        for x in range(len(imgList)): #write files to folder 
            imgWeb = requests.get(url + imgList[x])
            if imgWeb.status_code == requests.codes.ok:
                with open("img" + str(imgList[x]).replace("/", "-"), "wb") as imgSave: #open stream
                    print(imgList[x]) #progress confirmation
                    imgSave.write(imgWeb.content) #write to the stream in binary (wb)
        print("\nDone.")
    else:
        print("Request was not successful.")


while(True):
    userI = input("Please enter a url to scrape for images: ")

    #check if protocol is mentioned in the url for parser to work
    if ("https://" not in userI[:8]) and ("http://" not in userI[:7]):
            print("* Protocol not specified, assuming 'http://'")
            userI = "http://" + userI
    if "/" not in userI[-1]:
        slashYN = input("* Trailing slash not mentioned at the end of the URL, should '/' be appended to the end of URL? [Y/N]: ")
        resY = re.findall(r"(^Y(?:\s)*?$)|(^Y.s(?:\s)*?$)", slashYN, re.I)
        resN = re.findall(r"(^N(?:\s)*?$)|(^No(?:\s)*?$)", slashYN, re.I)
        if resY:
            print("Adding '/' to the end of URL\n")
            userI = userI + "/"
        elif resN:
            print("Ok, leaving URL as", userI, "\n")
        else:
            print("\n*** Sorry, not sure what you meant, assume 'No'. Leaving URL as", userI, "***\n")
    print("Webpage to scrape:")
    print(userI, "\n")

    # Showtime!
    try:
        imgScrape(userI)
    except:
        print("Sorry, something went wrong or the script got interrupted. Please make sure URL is spelled correctly. Try adding a trailing '/' to the end of your URL.")
    break
