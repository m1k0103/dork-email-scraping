import os
import time
from dork_email_scraping.func import make_google_search, find_emails, get_all_queries, remove_dupes


#main function
def main():

    #creates config file
    if "config.yml" not in os.listdir():
        with open("config.yml", "w+") as f:
            f.write(f"key: {input('enter api key: ')}\nse_id: {input('enter custom search engine id: ')}")
    
    #creates output folder
    if "outputs" not in os.listdir("dork_email_scraping"):
        os.mkdir("dork_email_scraping/outputs")
    
    # runs the main loop
    for query in get_all_queries():
        print(f"[!!!] Using query: {query}")
        for i in range(0,1000,10):
            links = make_google_search(i, search_query=query)
            find_emails(links)
            print(f"[!] Current searched pages: {i+10}")
            time.sleep(5)
            print("__Sleeping 5 seconds__")

    remove_dupes()
