from duckduckgo_search import DDGS, AsyncDDGS



###############################################################################
def ddgText(searchtxt):
    resulttxt = ""

    with DDGS() as ddgs:
        results = ddgs.text(searchtxt, max_results=10, safesearch='off')
        for r in results:
            resulttxt += f"{r['title']} -- {r['href']}-- {r['body']}\n\n"
            # print(f"{r}\n\n")

    return resulttxt

    # results = await AsyncDDGS().text(searchtxt, max_results=10, safesearch='off')
    # for r in results:
    #     # resulttxt += f"{r['title']} -- {r['href']}-- {r['body']}\n\n"
    #     print(f"{r}\n\n")



###############################################################################
def ddgNews(newstxt):
    resulttxt = ""

    with DDGS() as ddgs:
        results = ddgs.news(newstxt, max_results=20)
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