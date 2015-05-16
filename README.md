
# Pairing functions for Python

Pairing functions take two integers and give you one integer in return. What makes a pairing function special is that it is *invertable*; You can
reliably depair the same integer value back into it's two original values in the original order. Besides their [interesting mathematical properties](http://mathworld.wolfram.com/PairingFunction.html), pairing functions have some practical uses in software development in a very specific use case: Hiding two integer values as a single integer.

This is a python implementation of the [Cantor pairing
function](http://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function)
 and provides two functions, `pair` and `depair`.

## Install

    $ pip install pairing

## Usage

    from pairing import pair, depair

    pair(22, 33)  # 1573
    pair(33, 22)  # 1562
    depair(1573) # (22, 33)
    depair(1562) # (33, 32)



## When (not) to use this

So the pairing functions work, but why not just use two-tuples? After all,

`(22, 33)`

is certainly more explicit than some magic long integer like

`1573`

Everyone who uses this value downstream had better know how to solve the riddle! "Is that a pair of values or is the value actually 1573?". For the vast majority of problems, you
should **just stick with tuples** to represent pairs of integers.

But there may be situations where a pairing function can be useful if applied
carefully:

* You want to track pairs of integer values but the protocol, schema or API will
only accept **scalars** - single integer values, not collections. Using pairing functions in this
context should be reserved as a hack of last resort when the system can not be
modified to accommodate a collection.

* You have tuples as a result of element-wise array operations and want to store
it in a numpy `ndarray`. While numpy supports tuples, they will not give you the
best **performance** and are not a supported data type for many numpy
optimization techniques. For example, you could perform the `pair` algebra using `numexpr` to gain big speedups over any numpy manipulation and tuple data types to achieve the same effect.

    ```
    import numexpr as ne
    import numpy as np
    from pairing import depair

    a = np.random.randint(101, 103, (4, 3))
    b = np.random.randint(101, 103, (4, 3))
    paired = ne.evaluate("0.5 * (a + b) * (a + b + 1) + b")

    assert depair(paired[2, 2]) == (a[2, 2], b[2, 2])
    ```

* You have two-integer tuples as keys and want to
**serialize** the data to JSON, which does not allow collections as keys.
    ```
>>> d = {(22, 33):'foo'}
>>> json.dumps(d)
Traceback (most recent call last):
...
TypeError: keys must be a string
    ```

    Pairing functions could bypass this limitation.

    ```
>>> dc = dict(zip([pair(*x) for x in d.keys()], d.values()))
>>> dc
{1573: 'foo'}
>>> json.dumps(dc)
'{"1573": "foo"}'
    ```

    Both producer and consumer of JSON would need to agree on the details as to
which keys to pair/depair. There are many reasons why not to choose this route
(tight coupling, data fragility) but it might work in a pinch.


## Limitations

**TL;DR** Use non-negative integers that are not ridiculously large.

First off, negative values are not supported

    pair(-1, 33)  # ValueError: -1 and 33 cannot be paired

Zeros are fine

    pair(0, 33)  # 594

We can iterate through a range of integers and confirm that this works perfectly, at least for a certain range of positive integers

    for i in range(8,52,4):
        p = pair(2**i, 2**i)
        print p, "(2^{i}, 2^{i})".format(i=i)

    131584 (2^8, 2^8)
    33562624 (2^12, 2^12)
    8590065664 (2^16, 2^16)
    2199025352704 (2^20, 2^20)
    562949986975744 (2^24, 2^24)
    144115188612726784 (2^28, 2^28)
    36893488156009037824 (2^32, 2^32)
    9444732965876729380864 (2^36, 2^36)
    2417851639231457372667904 (2^40, 2^40)
    618970019642725321821650944 (2^44, 2^44)
    158456325028529238137041321984 (2^48, 2^48)


... until it doesn't. There do exist practical limits on the size of inputs
given that `long` integers are represented with arbitrary precision. With very large numbers, silent bugs can manifest in
ways that might catch you off-gaurd if you're not aware.


    values = (2**52, 2**52)                # (4503599627370496, 4503599627370496)
    encoded = pair(*values, safe=False)    # 40564819207303340847894502572032L
    depair(encoded)                        # (9007199254740992L, 0L)

That's not good. Noticed that we turned turned `safe=False` which allows these sorts of silent errors. Let's not fail silently! Using the default `safe=True` will perform a full pair-depair cycle and confirm that
the values are stable. If not, the function will raise a `ValueError` by default:


    encoded = pair(*values)
    # ValueError: 4503599627370496 and 4503599627370496 cannot be paired



## Tests

Try the test and benchmark script first:

    $ python3 test.py
    Tests pass.
    Benchmarking...
    0.47101 sec, 20000 iterations

