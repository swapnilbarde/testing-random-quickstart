"""googlesearch is a Python library for searching Google, easily."""

#https://www.learnsteps.com/google-search-url-parameters-and-what-do-they-mean/

from time import sleep
from bs4 import BeautifulSoup
from requests import get
import urllib
from urllib.parse import urlparse
import random


def get_useragent():
    return random.choice(_useragent_list)

_useragent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'
]




def _req(term, results, lang, start, proxies, timeout):
    resp = get(
        url="https://www.google.co.in/search",
        headers={
            "User-Agent": get_useragent()
        },
        params={
            "q": term,
            "num": results + 2,  # Prevents multiple requests
            "hl": lang,
            "start": start,
            "cr":"countryIN",
            'adtest':'off',
            'source':'hp'
        },
        proxies=proxies,
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5):
    """Search the Google search engine"""

    escaped_term = urllib.parse.quote_plus(term) # make 'site:xxx.xxx.xxx ' works.

    # Proxy
    proxies = None
    if proxy:
        if proxy.startswith("https"):
            proxies = {"https": proxy}
        else:
            proxies = {"http": proxy}

    # Fetch
    start = 0
    while start < num_results:
        # Send request
        resp = _req(escaped_term, num_results - start,
                    lang, start, proxies, timeout)

        # Parse
        soup = BeautifulSoup(resp.text, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        if len(result_block) ==0:
            start += 1
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find(
                "div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    start += 1
                    if advanced:
                        yield SearchResult(link["href"], title.text, description)
                    else:
                        yield link["href"]
        sleep(sleep_interval)

        if start == 0:
            return []

def get_results(all_results_object,domain_search,to_return='all|index',pprint=False):
  results = []
  domains = []
  found_at_index = None
  

  for idx, result in enumerate(all_results_object, 1):
      results.append(result)
      domains.append(urlparse(result).netloc)

      if found_at_index is None:
        for single in domains:
          if any(subdomain in single for subdomain in domain_search):
                found_at_index = idx
      if pprint:
        print(f"{idx}. {result}")
  if to_return=='index':
    return found_at_index
  if to_return=='all':
    return (results,domains,found_at_index)
  
domain_search = ['zomato','zomato.com']
keyword = 'Best vadapav in kalyan'

top_results = search(keyword, num_results=50, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5)
output = get_results(top_results,domain_search,to_return='all')

print("Found at",output[2])