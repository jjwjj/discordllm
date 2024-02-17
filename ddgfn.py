from duckduckgo_search import DDGS



###############################################################################
def ddgText(searchtxt):
    resulttxt = ""

    with DDGS() as ddgs:
        results = ddgs.text(searchtxt, max_results=10, safesearch='off')
        for r in results:
            resulttxt += f"{r['title']} -- {r['body']}"

    return resulttxt



###############################################################################
def ddgNews(newstxt):
    resulttxt = ""

    with DDGS() as ddgs:
        results = ddgs.news(newstxt, max_results=10)
        for r in results:
            resulttxt += f"{r['title']} -- {r['body']}"
    
    return resulttxt

###############################################################################
def ddgAll(searchtext):
    resulttxt = ""

    resulttxt  = ddgText(searchtext)
    resulttxt += ddgNews(searchtext)

    return resulttxt




###############################################################################
def main():

    searchtext = "history of the domesticated cat"
    # "latest news about domesticated cats"

    searchweb  = ddgText(searchtext)
    searchnews = ddgNews(searchtext)

    print(searchweb)
    print(searchnews)



###############################################################################
if __name__ == '__main__':
    main()