def naive_string_match(text: str, pattern: str):
    """
    Naive pattern matching: O((n - m + 1) * m)
    Returns list of starting indices.
    """
    n = len(text)
    m = len(pattern)
    occurrences = []

    if m == 0 or m > n:
        return occurrences

    for i in range(n - m + 1):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            occurrences.append(i)

    return occurrences


def rabin_karp(text: str, pattern: str, d: int = 256, q: int = 101):
    """
    Rabin–Karp pattern matching using rolling hash.
    d = alphabet size, q = prime modulus.
    Returns list of starting indices.
    """
    n = len(text)
    m = len(pattern)
    occurrences = []

    if m == 0 or m > n:
        return occurrences

    p = 0  # hash for pattern
    t = 0  # hash for current text window
    h = 1

    # h = pow(d, m-1) % q
    for _ in range(m - 1):
        h = (h * d) % q

    # Initial hash values for pattern and first text window
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    # Slide pattern over text one by one
    for s in range(n - m + 1):
        # If hash values match, check characters one by one
        if p == t:
            if text[s:s + m] == pattern:
                occurrences.append(s)

        # Compute hash of next window
        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q
            if t < 0:
                t += q

    return occurrences


def _compute_lps(pattern: str):
    """
    Build the LPS (longest proper prefix which is also suffix) array for KMP.
    """
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str):
    """
    Knuth–Morris–Pratt (KMP) pattern matching.
    Returns list of starting indices.
    """
    n = len(text)
    m = len(pattern)
    occurrences = []

    if m == 0 or m > n:
        return occurrences

    lps = _compute_lps(pattern)

    i = 0  # index for text
    j = 0  # index for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            # full match found at i - j
            occurrences.append(i - j)
            j = lps[j - 1]  # continue searching

        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return occurrences
