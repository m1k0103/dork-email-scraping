import os
import yaml
import requests
import re
import pandas as pd
from urllib.parse import urlparse


# removes duplicates from output file and creates a new file called {filename}_clean
def remove_dupes():
    with open(f"dork_email_scraping/outputs/output.txt", "r") as f:
        unique = set(f.readlines())
        with open(f"dork_email_scraping/outputs/clean_output.txt", "w") as new_f:
            new_f.writelines(set(unique))


# gets secrets from config file
def get_secrets():
    with open("config.yml") as f:
        contents = yaml.safe_load(f)
        return contents["key"], contents["se_id"]


# function which returns the urls that come from the page of a google search
def make_google_search(start,search_query):

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
        print("[+] No more search results found. Quitting...")
        quit()
    
    print(f"found {len(links)} links")
    return links


#writes an array of emails a "out.txt" file
def write_emails(email_list):
    with open("dork_email_scraping/outputs/output.txt", "a") as out:
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
            print(f"[!] Timeout to {url}")
            continue
        except requests.exceptions.ConnectionError:
            print(f"[!] Connection error to {url}")

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
            print(f"[-] No emails found in url {url}")

        else:
            print(f"[+] Found {len(emails)} in url {url}")
            write_emails(emails)
    return


def get_all_queries():
    with open("dork_email_scraping/dork_queries.txt", "r") as f:
        return list(f.readlines())