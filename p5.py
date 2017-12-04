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
from multiprocessing import Process, Array,Pool
import multiprocessing as mp
from functools import partial
import timeit


def time_results() :
    """Write any code needed to compare the timing of the sequential and parallel versions
    with a variety of string lengths."""
    def alg (T, P):
        time1 = timeit.timeit(lambda: p_naive_string_matcher(T,P), number =1000)
        return time1
    def alg2 (T, P):
        time2 = timeit.timeit(lambda: naive_string_matcher(T,P), number =1000)
        return time2
    if __name__ == "__main__":
        # string with numbers
        num = alg(A,B)
        num1 = alg2(A,B)
        #tounge-twister
        tongue_twisters = alg(C,D)
        tongue_twisters1 = alg2(C,D)
        #tounge-twister
        tongue twisters3 = alg(E,F)
        tongue twister4 = alg2(E,F)
        #short-stories
        short_stories = alg(G, H)
        short_stories1 = alg2(G, H)
        
        print('{:^15} {:^35} {:^20}'.format("String Length","Sequential Time","Parallel Time"))
        print('{:^15} {:^35} {:^20}'.format(len(A), num, num1))
        print('{:^15} {:^35} {:^20}'.format(len(A), tongue_twisters, tongue_twisters1))
        print('{:^15} {:^35} {:^20}'.format(len(A), tongue_twisters3, tongue_twisters4))
        print('{:^15} {:^35} {:^20}'.format(len(A), short_stories, short_stories1))

        

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

A = "001111010101101001100011010111101101011101101110010010101010111110111101100001011011000010111111011110011000011111000100100101001011101110101101111010100110010100101110010000111111100100110111010110100110011011101001010010101000010100111110"
B = "110011"

C = "I wish to wish the wish you wish to wish, but if you wish the wish the witch wishes, I won't wish the wish you wish to wish."
D = "wish"

E = "One-one was a race horse.Two-two was one too.One-one won one race.Two-two won one too."
F - "one"

G = """The sun did not shine.
It was too wet to play.
So she sat in the house
All that cold, cold, wet day.

She just sat in a chair
All alone, by herself.
As she watched the paint dry
On her brand new bookshelf.

Too wet to go out
And too cold to play ball.
As she sat in the house,
And did nothing at all.

And then
Something went BUMP!
How that bump made her jump!

She looked!
Then she saw him step in on that mat!
She looked!
And she saw him!
The Cat in the Hat!
And he said to her,
“Why do you sit there like that?”

“I know it is wet
And the sun is not sunny.
But we can have
Lots of good fun that is funny!”

“I know some good games we could play,”
Said the cat.
“I know some good tricks,”
Said the Cat in the Hat.
“A lot of good tricks.
I will show them to you.
Your mother
Will not mind at all if I do.”

She sat there and she
Did not know what to say.
Her mother was out of the house
For the day.

But her fish said, “No! No!
Make that cat go away!
Tell that Cat in the Hat
You do NOT want to play.
He should not be here.
He should not be about.
He should not be here
When your mother is out!”

“Now! Now! Have no fear.
Have no fear!” said the cat.
“My tricks are not bad,”
Said the Cat in the Hat.
“Why, we can have
Lots of good fun, if you wish,
With a game that I call
Let’s get rid of the fish!”

Then the cat chased the fish
Until she was caught.
And the fish hit the Cat in the head
With a pot.

“STOP!” Yelled the girl
“You do not have to fight
Either leave her alone or
you’re leaving!” “Alright”
Said the cat. “I’ll let the fish be.
Besides, there is something
I want you to see.”

And then he ran out.
And, then, fast as a whirl,
The Cat in the Hat
Came back in with a girl.

She was a cute girl
With eyes that shone bright.
With a sweatshirt and jeans
And teeth that shone white

Then he introduced her
With a tip of his hat.
“Here’s someone I’d like you to meet,”
Said the cat.
“She’s a sweet little girl
I will show to you now”
And the girl gave a twirl.
As the cat took a bow.

“Here’s a sweet little girl
And she wants to play
She can bring you some fun
On this cold, cold, wet day.
She is just like you are,
And I call her Thing One.
Would you like to shake hands
I’m sure you’ll have fun”

She was so bored and
She needed some fun.
So she went to shake hands
With the girl called Thing One.
And as they shook hands.
Her poor fish said, “No! No!
These two should not be
In the house! Make them go!

“They should not be here
When your mother is not!
Put them out! Put them out!”
Said the fish with the pot.

“Have no fear little fish,”
Said the Cat in the Hat.
“For she’s a good Thing.”
And he gave her a pat.
“She is tame. Oh, so tame!
She has come here to play.
She will give you some fun
On this wet, wet, wet day.”

“Now why don’t you two go and play,”
Said the cat.
“Just be on your way”
Said the Cat in the Hat.

“No! No do not go!”
Said the fish with the pot.
“Do not leave me alone
With this cat. You cannot.
Oh, I do not like cats!
They scare me, I admit!
Oh, I do not like this!
Not one little bit!”

But she went anyway,
She ran down the hall.
With Thing One, hand in hand,
They went to play dolls!
Hand in hand they went
To play dolls down the hall.

And left in the room
Was the fish and the cat.
The fish with the cat,
Well, she did not like that.
The fish was afraid
Of the Cat in the Hat.
He looked like a cat
But he smelled like a rat!

The cat said to the fish
With a gleam in his eyes.
“You know, we cats eat fish
This fact can’t be denied”
The fish shook with fear
As she attempted to run
But it’s not just Thing Ones
That want to have fun.

The cat won in the end,
The fish was no more.
“Well she didn’t put up much of a fight
What a bore.”
Then who should come back
But the girl and Thing One?
And the Cat in the Hat asked
“Did you two have fun?”

“We did” said Thing One
“But now she’s dried out
She’s no fun anymore”
Said Thing One with a pout.
“Well that’s the entire idea”
Said the Cat
“Now you’ll take her place”
Said the Cat in the Hat

“We’ll go house to house
All over the world
Taking the life force
Of each boy and girl
While their parents are gone
And it’s too wet to play
We will show up
And take them away
The best time to drain them
Is when their having fun
Then they’ll all be replaced
With Thing Twos and Thing Ones”

“Now take her outside”
Said the cat to Thing One
“Soon she’ll be nothing,
Just beams in the sun.
Then come back inside,
There’s work to be done
We’ve so much to do
We’ve only begun.”

Thing One went outside,
The girl trailing behind
Lifeless and slow
Not a thought in her mind.

Then the cat said “What fun
So much fun to be done
When the world is made up of
Thing Twos and Thing Ones
No more boring kids
Just moping about
For my Things will find fun
Of this I’ve no doubt”

Thing One came back in
In the clothes of the girl
“Are you ready to take her,
Place in this world?”
The new girl gave a nod
And the Cat said, “Then that’s that.”
And then he was gone
With a tip of his hat.

So, she sat in the chair
All alone, by herself.
As she watched the paint dry
On her brand new book shelf.
When her mother came in
She said “What did you do?”
Well, what would YOU do
If your mother asked YOU?"""
H ="the"

