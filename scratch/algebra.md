
Some unused stuff from "An algebra of board game positions"

==============================================================

Now let's talk about "abstract algebra", which is the study of "algebras"
in general, not necessarily the "regular" one based on numbers.
In an algebra, there are rules which tell you what kinds of thing are
allowed to be written on the piece of paper.
For instance, in the "regular algebra" of numbers, you can write this:

    (x + 1)

...but never this:

    (x + 1

...nor this:

    )x + 1(

...and this rule, that parentheses must come in matching open/close pairs,
is one which is shared by all algebras.
Other rules are also always shared, having to do with variables, equality,
and replacement.
That is, if `x = something`, then you can always replace `x` with `something`.
But the details of values like `0` or `34`, and operators like `+` and `-`,
can be very different in different algebras.

The rules for what can be written down in an algebra are usually given by
naming different kinds of thing, and then saying how to build 
For instance, we could make a small algebra based on numbers, where:

    A digit is one of: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
    A number is: 0, or a series of digits not starting with 0
    A variable is: a lowercase letter between a and z
    An expression is: a number, a variable, or (E1 + E2)
        ...where E1 and E2 are expressions

    You are allowed to write an expression on the paper.

With these rules, we could write (for example) any of the following things on
our piece of paper:

    23

    q

    (1 + 2)

    ((x + 1) + 42)

    (a + (b + c))

However, with these rules, we couldn't write any of the following things on
our piece of paper:

    (100 - 50)

    (1 + 2) = 3

    1 + 2

    (x + y + z)

...because our rules don't mention `-` or `=`, and they only say we can use `+` when
it has exactly 2 expressions on either side and parentheses around the whole
thing.
The rules of "regular algebra" of course let you write down many more things,
not to mention allow you to change them in various ways, for instance turning
`(x + y) + z` into `x + (y + z)`!
In abstract algebra, we can't take such things for granted.

Now, let's talk about algebraic geometry.
If "regular algebra" can be used to talk about numbers, algebraic geometry can be
used to talk about geometry: things like points, lines, circles, etc.
If you've ever learned about vector algebra, then you may already know that you
can use algebra to talk about points and lines.
For instance, the vector `<1, 2>` can represent a point, or an "arrow" pointing in
a certain direction.

Here is a diagram showing three points, A, B, and C.

    2|  C
    1|
    0|A   B
     +-----
      0 1 2

These points could also be written as vectors:

    A = <0, 0>
    B = <2, 0>
    C = <1, 2>

And we can also use vectors as "arrows", or *movements* if you like, which
move points around.
Here are some steps in vector algebra showing how to "move" C by `<3, -2>`,
resulting in a new point called "D":

    D = C + <3, -2>

    D = <1, 2> + <3, -2>

    D = <4, 0>

    2|  C
    1|
    0|A   B   D
     +---------
      0 1 2 3 4

