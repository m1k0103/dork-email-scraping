import os
import yaml
import requests
import re
import time
import pandas as pd
from urllib.parse import urlparse


#intext:@"yahoo|gmail|hotmail".com filetype:txt site:.uk
#intext:@"yahoo|gmail|hotmail".com ext:csv | ext:txt



def get_secrets():
    with open("config.yml") as f:
        contents = yaml.safe_load(f)
        return contents["key"], contents["se_id"]






# function which returns  the urls that come from the first page of a google search
def make_google_search(start):
    search_query = 'intext:@"yahoo|gmail|hotmail|teamaol|outlook".com ext:csv | ext:txt | ext:log | ext:xls | ext:xlsx | ext:xlsm | ext:xlsb | ext:odf | ext:ods'

    secrets = get_secrets()

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": search_query,
        "key": secrets[0],
        "cx":secrets[1],
        "start":start
    }
    response = requests.get(url, params=params)
    results = response.json()

    links = []
    try:
        for item in results["items"]:
            links.append(item["link"])
    except KeyError:
        print("No more search results found. Quitting...")
        quit()
    
    print(f"found {len(links)} links")
    return links





#writes an array of emails a "out.txt" file
def write_emails(email_list):
    with open("output.txt", "a") as out:
        for email in email_list:
            out.write(f"{email.lower()}\n")
    return





#when provided links, it will get the contents and use regex to extract emails
def find_emails(links):
    #cycles through every url and gets raw contents of url
    for url in links:
        try:
            raw_contents = requests.get(url, timeout=5).text # timeout 5 seconds
        except requests.exceptions.Timeout:
            print(f"timeout to {url}")
            continue
        except requests.exceptions.ConnectionError:
            print(f"connection error to {url}")

        #gets file extensiuon to check if its a spreadsheet and needs to be converted to a txt file
        extension = os.path.splitext(urlparse(url).path)[1][1:]

        #converts to txt
        if extension in ["xls","xlsx","xlsm","xlsb","odf","ods"]:
            storage_options = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 GLS/100.10.9939.100"}
            try:
                raw_contents = pd.read_excel(url, storage_options=storage_options).to_string()
            except Exception as e:
                print(f"Error: {e}")
                continue

        #uses regex to find email pattern
        emails = re.findall('([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', raw_contents)
        if len(emails) == 0:
            print(f"no emails found in url {url}")

        else:
            print(f"found {len(emails)} in url {url}")
            write_emails(emails)
    return



#main function
def main():
    #creates config file
    if "config.yml" not in os.listdir():
        with open("config.yml", "w+") as f:
            f.write(f"key: {input('enter api key: ')}\nse_id: {input('enter custom search engine id: ')}")
    
    for i in range(0,1000,10):
        links = make_google_search(i)
        find_emails(links)
        print(f"current searched pages: {i+10}")
        time.sleep(5);print("sleeping 5 seconds")




main()