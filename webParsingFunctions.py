import bs4 as bs 
from urllib.request import Request, urlopen
from urllib.parse import quote

# need to use special header so that
# website will accept request
def getSoup(url):
	# site = 'https://dictionary.goo.ne.jp/jn/'
	hdr = {'User-Agent': 'Mozilla/5.0'}
	req = Request(url, headers=hdr)
	page = urlopen(req)
	soup = bs.BeautifulSoup(page, 'lxml')

	return soup

def getDefinitionPage(url):
	return "https://dictionary.goo.ne.jp" + url 
def getSearchResults(word):
	percentEncoding = quote(word)
	wordUrl = 'https://dictionary.goo.ne.jp/srch/jn/' + percentEncoding + '/m0u/'
	return getSoup(wordUrl)

