
from dataclasses import dataclass, fields

from . import utils
from . import url


@dataclass(slots=False)
class Features:

    url: str 
    len: int = 0
    
    num_digits : int = 0
    num_special: int = 0
    num_subdom : int = 0
    num_query_params: int = 0

    has_ip  : bool = False
    has_port: bool = False
    https   : bool = False

    entropy: float = 0.0


    @staticmethod
    def _randomness(s: str, alpha: float = 0.4, beta: float = 0.3, gamma: float = 0.3) -> float:
        """
        Computes a randomness score for a given string based on
        Shannon entropy, consonant-vowel ratio, and unique character
        ratio.

        Args:
            s (str): The input string (typically the hostname).
            alpha (float): Weight for Shannon entropy.
            beta (float): Weight for consonant-vowel ratio.
            gamma (float): Weight for unique character ratio.

        Example:
        >>> Features._randomness("example.com")
        1.933772647454919

        Returns:
            float: A randomness score representing the
            unpredictability of the string.
        """
        entropy = utils.shannon_entropy(s)
        vc_ratio = utils.vowel_consonant_ratio(s)
        unique_ratio  = len(set(s)) / len(s)

        return alpha * entropy + beta * vc_ratio + gamma * unique_ratio


    def _extract(self, url: url.URL) -> None:
        """
        Extracts and computes various features from a given `URL`
        object.

        Args:
            url (url.URL): A parsed URL object.
        """
        self.len = url.len

        self.num_digits  = len(url.hostname_digits)
        self.num_special = len(url.hostname_special)
        self.num_subdom  = len(url.subdomains)
        self.num_query_params = len(url.query_params)

        self.has_ip   = bool(url.IP)
        self.has_port = bool(url.port)
        self.entropy  = self._randomness(url.parsed.hostname)


    def __post_init__(self):
        self._extract(
            url.URL(self.url)
        )

    
    @classmethod
    def schema(cls) -> str:
        """
        Returns a comma-separated string of the class attributes.
        """
        return ",".join(
            field.name for field in fields(cls)
        )
    

    def __str__(self) -> str:
        """
        Returns a comma-separated string representation of the feature
        values.

        Example:
        >>> features = Features("https://example.com")
        >>> str(features)
        "https://example.com,23,4,2,1,2,0,1,1.8"

        Returns:
            str: A comma-separated string of feature values.
        """
        return ",".join(
            str(int(value)) if isinstance(value, bool) else str(value)
            for value in (
                getattr(self, field.name) for field in fields(self)
            )
        )
