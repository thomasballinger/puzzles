"""
Maximum Sum: maximal sub-rectangle
as described at
http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=3&page=show_problem&problem=44
"""

def max_array_sum(a, verbose=False):
    """
    Returns the maximum sum of contiguous numbers in an array of integers

    >>> max_array_sum([1, 23, -4, 2, 7, 8, 2, -10, 11, -20, 7])
    40
    """
    first = last = 0
    running = a[last]
    max_sum = running
    while not (first == last == len(a) - 1):
        if verbose: print 'running total from', first, 'to', last, 'inclusive:', running
        if first > last and last < len(a) - 1:
            assert first == last + 1
            last += 1
            running += a[last]
        elif running < 0:
            running -= a[first]
            first += 1
        elif last < len(a) - 1:
            last += 1
            running += a[last]
        elif last == len(a) - 1:
            running -= a[first]
            first += 1
        else:
            raise Exception("Logic Error")
        max_sum = max(running, max_sum)
    return max_sum

def max_sub_rect(n, a, verbose=False, naive=False):
    """
    Given a side length and an array of integers, finds the maximal
    sub-rectangle sum of the square of side length n and data a

    calling this one O(n^4)

    >>> a = [ 0, -2, -7,  0, \
              9,  2, -6,  2, \
             -4,  1, -4,  1, \
             -1,  8,  0, -2];
    >>> max_sub_rect(4, a)
    15
    >>> max_sub_rect(4, a, naive=True)
    15
    """
    if verbose:
        for row in zip(*(a[i::n] for i in range(n))):
            print row

    def get_combined_row_naive(first_row, last_row):
        return [sum(a[row*n+col] for row in range(first_row, last_row+1)) for col in range(n)]

    def get_combined_row_with_cache(first_row, last_row, cache={(i, i) : a[i*n:(i+1)*n] for i in range(n)}):
        if (first_row, last_row) in cache:
            return cache[first_row, last_row]
        result = [x+y for x,y in zip(get_combined_row_with_cache(first_row, first_row), get_combined_row_with_cache(first_row+1, last_row))]
        cache[(first_row, last_row)] = result
        return result

    get_combined_row = get_combined_row_naive if naive else get_combined_row_with_cache

    max_sum = -127 * n**2
    for first_row in range(n):
        for last_row in range(first_row, n):
            array = get_combined_row(first_row, last_row)
            if verbose:
                print 'summed array for rows', first_row, 'to', last_row, 'inclusive:', array
            max_sum = max(max_array_sum(array), max_sum)
    return max_sum

def get_rand_square(n):
    import random
    return [random.randint(-127, 127) for _ in range(n**2)]

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import time
    import cProfile

    n = 100
    a = get_rand_square(n)
    def test(**kwargs):
        t0 = time.time()
        print max_sub_rect(n, a, **kwargs)
        print str(kwargs), time.time() - t0
        cProfile.run('max_sub_rect(n, a, **%r)' % kwargs)
        print('max_sub_rect(n, a, **%r)' % kwargs)
    test(naive=True)
    test(naive=False)
