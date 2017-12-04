# Programming Assignment 5
#
# Don't rename any functions, although feel free to implement any helper functions
# you find useful.
#
# 1) Implement the naive_string_matcher function as specified in its docstring.
#    This is a variation of the algorithm on page 988 of the textbook.
#    Read the docstring below carefully so you know what I've changed.
#
# 2) Implement the function print_results below.
#
# 3) Implement the p_naive_string_matcher function as specified in its docstring.
#
# 4) In the time_results function below, implement any code needed to compare the runtimes
#    of the sequential and parallel version on string of varying lengths.  You will need to
#    figure out how to generate strings of varying lengths.  Here's one approach to get a really
#    long string to use as T (long enough that you will almost certainly see a benefit to parallel
#    implementation.  The complete works of shakespeare is freely available (http://shakespeare.mit.edu/ among
#    other places).  You might just hardcode a long string by copying and pasting and surrounding with """ and """
#    to get a multiline string.
#
# 5) Answer the following questions here in a comment based on #4:
#
#    Q1: After running time_results, fill in this table in this comment for whatever P and T lengths
#        you tried (make sure you vary lengths from short to longer:
#        T-length   P-Length   Sequential   Parallel
#
#    Q2: How do the times (of both versions) vary by string length?  If T is held constant, and pattern P length varied, how does
#        that affect runtime?  If P length is held constant, and text T length varied, how does that affect runtimes?
#
#    Q3: At what lengths of P and/or T is the sequential version faster?
#
#    Q4: At what lengths of P and/or T is the parallel version faster?
#
#    Q5: Are the results consistent with the speedup you computed in Problem Set 4?  If not, what do you think caused
#        the inconsistency with the theoretical speedup?


# These are imports you will likely need.  Feel free to add any other imports that are necessary.
#E.g., you might also need Queue for getting the results back from your processes.
from multiprocessing import Process, Array
import ctypes


def time_results() :
    """Write any code needed to compare the timing of the sequential and parallel versions
    with a variety of string lengths."""
    pass

def print_results(L) :
    """Prints the list of indices for the matches."""
    print(L)

def naive_string_matcher(T, P) :
    """Naive string matcher algorithm from textbook page 988.

    Slight variation of the naive string matcher algorithm from
    textbook page 988.  Specifically, the textbook version prints the
    results.  This python function does not print the results.
    Instead, it generates and returns a list of the indices at the start
    of each match.  For example, if T="abcabcabc" and P="def", this function
    will return the empty list [] since the pattern doesn't appear in T.
    For that same T, if the pattern P="abc", then this function will return
    the list [0, 3, 6] since the pattern appears 3 times, beginning on indices
    0, 3, and 6.

    Keyword arguments:
    T -- the text string to search for patterns.
    P -- the pattern string.
    """
    L = []
    n = len(T)
    m = len(P)
    for i in range((n-m)+1):
        for j in range(m):
            if (T[i+j] != P[j]):
                break
            if j == m-1:
                L.append(str(i))
    return L


def p_naive_string_matcher(T, P) :
    """Parallel naive string matcher algorithm from Problem Set 4.

    This function implements the parallel naive string matcher algorithm that you specified in
    Problem Set 4.  You may assume in your implementation that there are 4 processor cores.
    If you want to write this more generally, you may add a parameter to the function for number
    of processes.  If you do, don't change the order of the existing parameters, and your new parameters
    must follow, and must have default values such that if the only parameters I pass are T and P, that
    you default to 4 processes.

    Like the sequential implementation from step 1 of assignment, this function should not
    print results.  Instead, have it return a list of the indices where the matches begin.
    For example, if T="abcabcabc" and P="def", this function
    will return the empty list [] since the pattern doesn't appear in T.
    For that same T, if the pattern P="abc", then this function will return
    the list [0, 3, 6] since the pattern appears 3 times, beginning on indices
    0, 3, and 6.

    You must use Process objects from the multiprocessing module and not Threads from threading because
    in the next step of the assignment, you're going to investigate performance relative to the sequential
    implementation.

    You will need to decide how to distribute the work among the processes.
    One way (not the only way) is to give all of your processes T and P, and to give each process
    a range of starting indices to check, such that you give each approximately equal sized ranges.
    Another way is to give all processes the pattern string P, but only a substring of T (of approximately
    equal size).  In this case, you'd need to figure out how to map the indices back into the original.

    You will need to decide how to get the results back from the processes.
    One way (not the only way) is to give all processes a reference to a Queue object for the results.

    If you give all processes the full T and P, then if the size of the text T is large, the savings from
    multiprocessing may be outweighed by the cost of giving each its own independent copy of T.
    You might try using an Array object to use shared memory.  Here's how to do it.  Create an array of
    characters in shared memory with: a = Array(ctypes.c_wchar, "Hello World", lock=None)
    You'll need to import ctypes
    for this to work.  You can then access individual characters with a[0], a[1], etc.
    You might do this for both T and P.  None of the processes need to change them, so there is no risk
    of a race condition.

    Keyword arguments:
    T -- the text string to search for patterns.
    P -- the pattern string.
    """
    L = [i for i in range(0, n-m+1)]
    n = len(T)
    m = len(P)
    pool = mp.Pool()
    func = partial(p_help, T,P,m)
    matches = [x for x in pool.map(func, iterable) if x is not None]
    return matches
def p_hlep(T,P,m,i):
    if P == T[i:i+m]:
        return i

Q = "001111010101101001100011010111101101011101101110010010101010111110111101100001011011000010111111011110011000011111000100100101001011101110101101111010100110010100101110010000111111100100110111010110100110011011101001010010101000010100111110"
W = "110011"
