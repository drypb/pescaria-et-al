
import utils


def _randomness(s: str, alpha: float = 0.5, beta: float = 0.1, gamma: float = 0.4) -> float:
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

    return alpha * entropy + gamma * unique_ratio


if __name__ == "__main__":
    print(_randomness("a28ad1#@1c51AM"))
    print(_randomness("www.google.com"))
    #print(utils.shannon_entropy("a28ad1#@1c51AM"))
    #print(utils.shannon_entropy("www.google.com"))
