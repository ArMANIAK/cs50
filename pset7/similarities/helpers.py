from nltk.tokenize import sent_tokenize


def slicer(string, n):
    # slices string into substrings of n-length
    list_str = []
    for i in range(len(string) - n + 1):
        if string[i: i + n] not in list_str:
            list_str.append(string[i: i + n])

    return list_str


def lines(a, b):
    """Return lines in both a and b"""

    # TODO
    a_list = a.split('\n')
    b_list = b.split('\n')
    result = []
    for b_line in b_list:
        if b_line in a_list and b_line not in result:
            result.append(b_line)

    return result


def sentences(a, b):
    """Return sentences in both a and b"""

    # TODO
    a_list = sent_tokenize(a)
    b_list = sent_tokenize(b)
    result = []
    for b_line in b_list:
        if b_line in a_list and b_line not in result:
            result.append(b_line)

    return result


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    # TODO
    a_list = slicer(a, n)
    b_list = slicer(b, n)
    result = []
    for b_sub in b_list:
        if b_sub in a_list and b_sub not in result:
            result.append(b_sub)

    return result
