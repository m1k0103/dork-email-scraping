#intext:@"yahoo|gmail|hotmail".com filetype:txt site:.uk
#intext:@"yahoo|gmail|hotmail".com ext:csv | ext:txt


def init():
    #creates config file
    with open("config.yml", "w+") as f:
        f.write(f"key: {input('enter api key: ')}")
        pass



# initial testing shows that google uses dynamic pages.
# will most likely have to use selenium
# will take much longer with using *ugh* selenium 