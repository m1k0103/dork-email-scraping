import os
import time
from dork_email_scraping.func import make_google_search, find_emails, get_all_queries, remove_dupes
from multiprocessing import Pool, cpu_count

#the loop function to which the query is mapped to in the main functon
def do_loop(query):
    print(f"[!!] Using query: {query}")
    for i in range(0,1000,10):
        links = make_google_search(i,search_query=query)
        find_emails(links)
        print(f"[!] Searched {i} pages of {query}")
    print(f"[+] Finished searching query: {query}")


#main function
def main():
    #creates config file
    if "config.yml" not in os.listdir():
        with open("config.yml", "w+") as f:
            f.write(f"key: {input('enter api key: ')}\nse_id: {input('enter custom search engine id: ')}")
    
    #creates output folder
    if "outputs" not in os.listdir("dork_email_scraping"):
        os.mkdir("dork_email_scraping/outputs")
    
    try:
        # creates a new process for a query. much faster than one process handling all queries seperately.
        with Pool(cpu_count()) as p:
            print(f"[!] Starting execution with {cpu_count()} CPUs.")
            all_queries = get_all_queries()
            p.map(do_loop,(all_queries))
    except KeyboardInterrupt:
        print("Detecting keyboard interrupt. Removing duplicates and quitting...")
        remove_dupes()
        quit()

    remove_dupes()
    print("Duplicates removed. Quitting...")
    quit()
