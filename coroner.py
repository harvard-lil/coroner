import re
import requests
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Thanks Django.
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def get_chain(address):
    # from url, build a list of respone urls and status codes
    # return the chain and the response text

    r = requests.get(address)

    chain = []
    body = ''

    if r.history:

        chain.append(('', r.history[0].status_code))
        r.history = r.history[1:]
        for i in r.history:
            chain.append((i.url, i.status_code))

        chain.append(('', r.status_code))

        body = str(BeautifulSoup(r.text).body)

    return {'chain': chain, 'resonse_body': body}

def get_bogus_address(address):
    # From an address, build one that looks similar.
    # if our address looks like http://name.tld/some/path, build
    # an address that looks like http://name.tld/some/randopath

    bogus_path_elemnt = 'lnkl08008asdvsjiberish00ojsd00lknklads0-lkls0'

    return urljoin(address, bogus_path_elemnt)


def main(address):

    # Help the user a bit
    parsed_url = urlparse(address)
    if not parsed_url.scheme:
        address = "http://%s" % address

    # Check for a malformed address
    if not re.match(regex, address):
        return False

    chain_and_doc = get_chain(address)
    print chain_and_doc['chain']

    bogus_address_chain_and_doc = get_chain(get_bogus_address(address))
    print bogus_address_chain_and_doc['chain']

    #print chain_and_doc['resonse_body']
    #print bogus_address_chain_and_doc['resonse_body']

    documents = (chain_and_doc['resonse_body'], bogus_address_chain_and_doc['resonse_body'])
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    similarity_measure = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    print similarity_measure

    if chain_and_doc == bogus_address_chain_and_doc and similarity_measure[0][1] > .95:
        print 'It appears as if we have been served a soft 404'

if __name__ == "__main__":
    #main('http://cyber.law.harvard.edu/asdfsv23adf/avdd4')
    #main('http://feedly.com/asdfsv23vs3adf/vsdsds')
    main('http://engadget.com/asdfsv23vs3adf/vsdsds')
    #main('http://ssnat.com/avsd/d')