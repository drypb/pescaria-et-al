from urllib.parse import urlparse
import sys

def valid(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def main():
    with open(sys.argv[1], 'r') as file:
        for url in file:
            if not valid(url):
                print(url + ' is invalid !')

if __name__ == "__main__":
    main()
