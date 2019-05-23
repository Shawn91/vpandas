def pop_elements_index(eles, arr):
    """Get element index in arrary one by one.
    The second element's index is obtained by first remove the first element from the array.

    Examples:
        >>> print(pop_elements_index(['b', 'a'], ['b','c','a']))
        [0, 1]
    """
    arr = arr[:]  # a shallow copy
    result = []
    for e in eles:
        result.append(arr.index(e))
        arr.remove(e)
    return result

if __name__ == '__main__':
    import doctest
    doctest.testmod()