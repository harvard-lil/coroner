import re
import requests
from urlparse import urlparse, urljoin
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
    r.history = r.history[1:]
    for i in r.history:
        chain.append((i.url, i.status_code))

    chain.append((r.url, r.status_code))

    return {'chain': chain, 'resonse_text': r.text}

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

    address_chain = get_chain(address).chain
    print address_chain

    # get url. track number of redirects and responses.
    # if we end up with a 404, a bad malformed url, or
    # a slow or dead response, return false

    bogus_address_chain = get_chain(get_bogus_address(address)).chain
    print bogus_address_chain

    #if address_chain == bogus_address_chain:
    #    print "It appears as if we've found a soft 404"
    #    return

    #vect = TfidfVectorizer(min_df=1)
    #tfidf = vect.fit_transform([address.content, bogus address.content])
    #pairwise_similarity = tfidf * tfidf.T


if __name__ == "__main__":
    #main('http://cyber.law.harvard.edu/asdfsv23adf/avdd4')
    #main('http://feedly.com/asdfsv23vs3adf/vsdsds')
    main('http://ssnat.com/avsd/d')