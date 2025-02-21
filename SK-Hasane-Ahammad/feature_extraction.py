from urllib.parse import urlparse, urlencode
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import ipaddress
import requests
import urllib
import whois
import re

# -- loading the data --

# load phishing URLs
data0 = pd.read_csv("dataset/PhishTank-verified_online.csv")
print(data0.head())
print(data0.shape)

# choose 5000 phishing URLs randomly
phishurl = data0.sample(n = 5000, random_state = 12).copy()
phishurl = phishurl.reset_index(drop=True)
print(phishurl.head())
print(phishurl.shape)

# load legitimate URLs
data1 = pd.read_csv("dataset/Benign_list_big_final.csv")
data1.columns = ['URLs']
print(data1.head())
print(data1.shape)

# choose 5000 legitimate URLs randomly
legiurl = data1.sample(n = 5000, random_state = 12).copy()
legiurl = legiurl.reset_index(drop=True)
print(legiurl.head())
print(legiurl.shape)

# -- feature extraction --

## autor falou que essa func eh inutil
def getDomain(url):
    domain = urlparse(url).netloc

    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")

    return domain

def havingIP(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0

    return ip

def haveAtSign(url):
    if "@" in url:
        at = 1
    else:
        at = 0

    return at

## talvez usar sigmoide ou similar aqui seja melhor
def getLength(url):
    if len(url) < 54:
        length = 0
    else:
        length = 1

    return length

# returns the number of '/' in url
def getDepth(url):
    s = urlparse(url).path.split('/')
    depth = 0

    for j in range(len(s)):
        if len(s[j]) != 0:
            depth = depth + 1

    return depth

## isso funciona mesmo?
## poderia ser
## if pos > 7:
##     return 1
## return 0
def redirection(url):
    pos = url.rfind('//')

    if pos > 6:
        if pos > 7:     ## se (pos > 7), retorna 1
            return 1
        else:           ## se (pos == 7), retorna 0
            return 0
    else:               ## se (pos <= 6), retorna 0
        return 0

## deveria ser scheme em vez de netloc.
## o autor nao sabe o que esta fazendo!!!
def httpDomain(url):
    domain = urlparse(url).netloc

    if 'https' in domain:
        return 1
    else:
        return 0

#listing shortening services
shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

# check for shortening services in URL
def tinyURL(url):
    match=re.search(shortening_services,url)

    if match:
        return 1
    else:
        return 0

def prefixSuffix(url):
    if '-' in urlparse(url).netloc:
        return 1
    else:
        return 0

## sigmoide
## nem tudo precisa ser exatamente 0 ou 1
""" data.alexa.com nao esta online
def web_traffic(url):
    try:
        url = urllib.parse.quote(url)
        rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return 1

    if rank < 100000:
        return 1
    else:
        return 0
"""

## :(
def domainAge(domain_name):
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date
    if (isinstance(creation_date,str) or isinstance(expiration_date,str)):
        try:
            creation_date = datetime.strptime(creation_date,'%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        return 1
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        if ((ageofdomain/30) < 6):
            age = 1
        else:
            age = 0
    return age

def domainEnd(domain_name):
    expiration_date = domain_name.expiration_date
    if isinstance(expiration_date,str):
        try:
            expiration_date = datetime.strptime(expiration_date,"%Y-%m-%d")
        except:
            return 1
    if (expiration_date is None):
        return 1
    elif (type(expiration_date) is list):
        return 1
    else:
        today = datetime.now()
        end = abs((expiration_date - today).days)
        if ((end/30) < 6):
            end = 0
        else:
            end = 1
    return end

def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1

def mouseOver(response):
    if response == "" :
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0

def rightClick(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1

def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1

def featureExtraction(url,label):
    features = []
    #Address bar based features (10)
    features.append(getDomain(url))
    features.append(havingIP(url))
    features.append(haveAtSign(url))
    features.append(getLength(url))
    features.append(getDepth(url))
    features.append(redirection(url))
    features.append(httpDomain(url))
    features.append(tinyURL(url))
    features.append(prefixSuffix(url))

    #Domain based features (4)
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
    except:
        dns = 1

    features.append(dns)
    #features.append(web_traffic(url))
    features.append(1 if dns == 1 else domainAge(domain_name))
    features.append(1 if dns == 1 else domainEnd(domain_name))

    # HTML & Javascript based features (4)
    try:
        response = requests.get(url, timeout=2)
    except:
        response = ""
    features.append(iframe(response))
    features.append(mouseOver(response))
    features.append(rightClick(response))
    features.append(forwarding(response))
    features.append(label)

    return features

# extract features from legitimate URLs
print(legiurl.shape)
legi_features = []
label = 0

for i in range(0, 5000):
    url = legiurl['URLs'][i]
    legi_features.append(featureExtraction(url,label))

feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection', 
                 'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record',
                 'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards', 'Label']

legitimate = pd.DataFrame(legi_features, columns= feature_names)
print(legitimate.head())
legitimate.to_csv('legitimate.csv', index= False)

# extract features from phishing URLs
print(phishurl.shape)
phish_features = []
label = 1

for i in range(0, 5000):
    url = phishurl['url'][i]
    phish_features.append(featureExtraction(url,label))

feature_names = ['Domain', 'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth','Redirection',
                 'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record',
                 'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over','Right_Click', 'Web_Forwards', 'Label']

phishing = pd.DataFrame(phish_features, columns= feature_names)
print(phishing.head())
phishing.to_csv('phishing.csv', index= False)

urldata = pd.concat([legitimate, phishing]).reset_index(drop=True)
print(urldata.head())
print(urldata.tail())
print(urldata.shape)
urldata.to_csv('urldata.csv', index=False)
