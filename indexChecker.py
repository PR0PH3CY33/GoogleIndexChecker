
try:
    import sys

    import requests

    import xml.etree.ElementTree as ET

except ImportError as ie:

    print(ie)

    sys.exit()

def getSitemapUrls(sitemapUrl):

    response = requests.get(sitemapUrl)

    if(response.status_code == 200):

        xmlContent = (response.content)

        root = ET.fromstring(xmlContent)
        
        urls = []

        for url in root.findall(".//loc"):

            urls.append(url.text)

        return urls
        
    else:

        print("Couldn't fetch the sitemap")

        sys.exit()


def getIndexationStatus(apiKey, apiEndpointUrl, url):

    payload = {
    
        "url": url
    
    }

    headers = {
    
        "Content-Type": "application/json"
    
    }
    
    try:
        
        response = requests.post(apiEndpointUrl, json=payload, headers=headers)
    
        result = response.json()
    
        if(result["testStatus"]["status"] == "COMPLETE"):

            print(str(url) + " is indexed by Google")

        else:

            print(str(url) + " is NOT indexed by Google")

    except Exception as e:
        
        print(e)

        sys.exit()
 

sitemapUrl = "https://thelinuxbible.com/sitemap.xml"

urls = getSitemapUrls(sitemapUrl)

if(len(urls) == 0):
    
    print("No URLs were found in the sitemap")

else:
 
    for url in urls:

        apiKey = "AIzaSyAiKH2ZnzYW09upSVVb2kh41cCIgDcHTuA"

        apiEndpointUrl = "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key=" + str(apiKey)

        indexationStatus = getIndexationStatus(apiKey, apiEndpointUrl, url)
