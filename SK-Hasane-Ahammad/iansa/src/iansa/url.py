
from dataclasses import dataclass, field
from typing import *

import tldextract
import validators
import functools
import urllib
import re


_IP_PATTERN = re.compile(
    r"(?:(?:\d{1,3}\.){3}\d{1,3}) | (?:\[[0-9a-fA-F:]+\])"
)


class InvalidURL(ValueError):
    """
    Initializes the InvalidURL with a message indicating the 
    provided URL is invalid.

    Args:
        url (str): The URL that is deemed invalid.
    """
    def __init__(self, url: str):
        super().__init__(
            f"Invalid URL provided: {url}"
        )


@dataclass
class URL:
    
    url: str
    parsed: urllib.parse.ParseResult = field(init=False)


    def __post_init__(self):
        if validators.url(self.url):
            self.parsed = urllib.parse.urlparse(self.url)
            return

        raise InvalidURL(self.url)


    @functools.cached_property
    def IP(self) -> List[str]:
        """
        Extracts IP addresses (both IPv4 and IPv6) from the URL.

        Example:
        >>> url = URL("https://192.168.1.1/path")
        >>> url.IP
        ['192.168.1.1']

        Returns:
            List of extracted IP addresses.
        """
        return [match.group() for match in _IP_PATTERN.finditer(self.url)]


    @functools.cached_property
    def subdomains(self) -> List[str]:
        """
        Extracts subdomains from the URL.

        Example:
        >>> url = URL("https://sub.example.domain.com")
        >>> url.subdomains
        ['sub', 'example']

        Returns:
            List of subdomains (empty list if none found).
        """
        ret = []
        hostname = self.parsed.hostname
        if hostname:
            extracted = tldextract.extract(hostname)
            if extracted.subdomain:
                ret = extracted.subdomain.split(".")

        return ret


    @functools.cached_property
    def query_params(self) -> Dict[str, List[str]]:
        """
        Parses query parameters from the URL and returns them as a
        dictionary.

        Example:
        >>> url = URL("https://example.com/path?key1=value1&key2=value2")
        >>> url.query_params
        {'key1': ['value1'], 'key2': ['value2']}

        Returns:
            Dictionary of query parameters with their values.
        """
        return urllib.parse.parse_qs(self.parsed.query)


    @functools.cached_property
    def hostname_special(self) -> List[str]:
        """
        Extracts and returns a list of special characters from the
        hostname.

        Example:
        >>> url = URL("https://my-test.domain.com")
        >>> url.hostname_special
        ['-']

        Returns:
            List of special characters found in the hostname.
        """
        return [char for char in self.parsed.hostname if not char.isalnum() and char != "."]


    @functools.cached_property
    def hostname_digits(self) -> List[int]:
        """
        Extracts and returns a list of digits found in the hostname.

        Example:
        >>> url = URL("https://abc123.domain456.com")
        >>> url.hostname_digits
        [1, 2, 3, 4, 5, 6]

        Returns:
            List of integers representing digits found in the
            hostname.
        """
        return [int(ch) for ch in self.parsed.hostname if ch.isdigit()]


    @functools.cached_property
    def len(self) -> int:
        """
        Computes the total length of the URL string.

        Example:
        >>> url = URL("https://example.com/path")
        >>> url.len
        24

        Returns:
            Integer length of the URL.
        """
        return len(self.url)


    @functools.cached_property
    def port(self) -> Optional[int]:
        """
        Extracts the port number from the URL (if specified).

        Example:
        >>> url = URL("https://example.com:8080/path")
        >>> url.port
        8080

        Returns:
            Port number as an integer, or None if not specified.
        """
        return self.parsed.port
