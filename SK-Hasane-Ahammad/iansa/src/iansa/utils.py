
import collections
import numpy
import math
import re


def shannon_entropy(s: str) -> float:
    """
    Computes the Shannon entropy of a given string, which 
    quantifies the randomness of character distribution.

    Example:
    >>> shannon_entropy("hello")
    1.9219280948873623

    Args:
        s (str): The input string.

    Returns:
        float: The Shannon entropy value, representing the 
        randomness of the string. 
    """

    if not s:
        return 0.0

    freq = numpy.array(list(collections.Counter(s).values()))
    probs = freq / freq.sum()
    return -numpy.sum(probs * numpy.log2(probs))


def vowel_consonant_ratio(s: str) -> float:
    """
    Computes the ratio of consonants to vowels in a given string.

    Example:
    >>> vowel_consonant_ratio("hello")
    1.5

    Args:
        s (str): The input string.

    Returns:
        float: The ratio of consonants to vowels. 
         - If there are no vowels but at least one consonant, 
           returns `inf`. 

         - If the string is empty or has no vowels/consonants, 
           returns `0.0`.
    """
    if not s:
        return 0.0
    
    vowels = re.findall(r'[aeiouAEIOU]', s)
    consonants = re.findall(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]', s)

    v_count = len(vowels)
    c_count = len(consonants)
    if v_count == 0:
        if c_count > 0:
            return float("inf")
        return 0.0

    return c_count / v_count

# vowel to non-vowel chars
