# An Algebra of Chess

I've been a fan of abstract algebra, and algebraic geometry, since University.

I also enjoy reading and thinking about chess and other board games.
I like playing them too, for fun, and for purposes of experimentation.

Hey look, it's an algebraic expression showing a pawn taking another pawn:

    ♙ + ur♟ -> . + ur♙

If that piques your interest, read on.


## What is an algebra?

I think a halfway decent description of "an algebra" is: a set of rules for
replacing parts of something you've written down.

So for instance, let's say you've written this down on a piece of paper:

    x + 1 - 1

One of the rules of "regular algebra" (the one with numbers, you know the one)
says that you're allowed to erase the `1 - 1` there and replace it with `0`:

    x + 0

And then another rule says, you can replace `x + 0` with `x`:

    x

But then *another* rule says, you can replace `x` with `x * 1` (x times 1):

    x * 1

And another rule says, you can replace `1` with `20 / 20` (20 divided by 20):

    x * 20 / 20

Notice how, at one point, we had x all by itself.
And there is a kind of game we can play, where we have an equation, and we
try to "solve for x":

    3x + 4 = 5

    3x = 1

    x = 1/3

But our goal of solving for x isn't one of the rules of algebra; it's just
something we layer on top.
Algebra doesn't tell us that we *have* to solve for x; in fact, it says it's
totally fine if we introduce a new variable, e.g. like this:

    3x + 4 = 5

    3x + 4 + 7y = 5 + 7y

In fact, there are many goals we could layer on top of algebra.
For instance, we could have a game with multiple players, and an equation
written down, and the players take turns applying rules of algebra to it.
Maybe the players are trying to work together to solve for a variable?..
or maybe each player is trying to solve for a different variable?..
or maybe there are a whole bunch of players, and they're allowed to form
alliances, and each player has a goal which they keep secret from the other
players?..
But in any case, the rules of algebra tell us what changes the players
are allowed to make to the equation when they "move".

Just let that idea float around in your mind for a minute: algebra is just
some rules, without a goal.
The rules have to do with what's allowed to be written down on a piece of
paper, and how people are allowed to make changes to it.

And I think, when you open your mind to that idea, you can start to see
a connection between algebra and board games.
Writing an algebraic expression on a piece of paper is like putting pieces
down on a board.
Some of a board game's rule are an algebra describing how the board is
allowed to change, or how the pieces move around on it.
Other rules describe the players, their goals, the order in which they take
turns, etc; but let's forget about those rules for now, and focus on the
algebra of the board.

We'll focus on chess for now, and build an algebra in two layers, one
building upon the other:
* an algebra of chess positions
* an algebra of chess moves


## An algebra of chess positions

### Some motivation: visualizing chess rules

Here is a chess board:

    ♜♞♝♚♛♝♞♜
    ♟♟♟♟♟♟♟♟
    ........
    ........
    ........
    ........
    ♙♙♙♙♙♙♙♙
    ♖♘♗♔♕♗♘♖

And here is a valid move:

    ♜♞♝♚♛♝♞♜
    ♟♟♟♟♟♟♟♟
    ........
    ........
    ........
    .....♙..
    ♙♙♙♙♙.♙♙
    ♖♘♗♔♕♗♘♖

And here is the rule of chess algebra which says it was valid:

    .
    ♙

    ...can be replaced with:

    ♙
    .

Make sense? Now here is another rule of chess algebra, saying that a pawn
may take an enemy pawn diagonally:

     ♟
    ♙

    ...can be replaced with:

     ♙
    .

These rules can be applied anywhere on the board, similar to how the rule
"`x + 0` can be replaced with `x`" can be applied anywhere within an
expression or equation.

Now, here is another rule:

    .
    .
    .
    ♖

    ...can be replaced with any of:

    .   .   ♖
    .   ♖   .
    ♖   .   .    ...etc
    .   .   .

An interesting question here is, how can we express this rule without using
"etc"?.. that is, how do we express a potentially infinite rule (if you want
to support chessboards of any size, which I think we should, as a matter of
principle) in a finite way?
And I think it's clear that we could express it in terms of the following rule,
if we had a way to apply it repeatedly:

    .
    ♖

    ...can be replaced with:

    ♖
    .

Make sense? The rule that a rook can travel forward over as many empty squares
as it wants, should in some sense be equivalent to repeatedly applying the
rule that a rook can travel forward one empty square at a time.

But before we talk any further about rules, we should talk first about the
little before & after pictures we've been using to describe them, that is,
when we say "this can be replaced with that," what are "this" and "that"?..
let's call them "board fragments"!


### The concept of "board fragments"

Let's gear up like proper mathematicians and start coming up with some syntax.
We're going to come up with a way to describe fragments of chess boards as
algebraic expressions.
In fact, we're going to come up with an "algebra of chess positions".
Here we go!..

Here is a "board fragment":

    .♛.
    ....
     .♔♙

...it has some empty squares (shown as "."), and some squares with pieces
on them.
It has no edge: it's like a small cut-out from a full chessboard.

Let's also say that all board fragments have a centre.
So, the following diagram could be for many different board fragments,
depending on where we say its "centre" is:

     .
    .♖.
     .

The centre is always at the *corners* of the board's grid of squares.
So for instance, here are two different board fragments, drawn with the
grid visible, and the centre indicated with "@":

      +-+
      | |
    +-+-+-+
    | |♖| |
    +-+-+-+
      | |
      @-+

    ...is different from:

      +-+
      | |
    +-+-@-+
    | |♖| |
    +-+-+-+
      | |
      +-+

Now let's come up with an easier way to describe board fragments without
having to draw them out.

The symbol `.` will mean the board fragment consisting of an empty square,
with the centre at the square's bottom-left corner.
The symbols `♟`, `♙`, `♚`, `♔`, etc are like `.`, but with the indicated
piece sitting on the square.

    The board fragment ".":

    +-+
    | |
    @-+

    The board fragment "♟":

    +-+
    |♟|
    @-+

The symbol `0` will mean the empty board fragment, which consists of...
nothing. No empty squares, no squares with pieces on them, just a "centre"
floating in a void.

    The empty board fragment, "0":

    @


### The concept of "movements"

There are also "movements". These are ways of moving a board fragment around
relative to its centre.
Imagine putting your finger on a chessboard (or a little cut-out fragment of
a chessboard) and sliding it around: you could slide it to the left, to the
right... and all the pieces sitting on it would slide around with it.
That's a "movement".

The basic movements are `u`, `d`, `l`, and `r`, meaning movements of a board
fragment 1 square up, down, left, and right relative to its centre.
You could also think of these movements as moving the centre relative to the
rest of the board fragment, but trust me for now that it's more useful to
think of sliding the board relative to the centre.

Given a board fragment f and movement m, we can apply m to f, resulting in
another board fragment.
We show application by concatenation, that is, writing things next to each
other, e.g. `m f` or just `mf`.

For instance, `u.` is the board fragment consisting of `.` slid upwards by
one square's width relative to the centre.

    The board fragment "u.":

    +-+
    | |
    +-+

    @

    The board fragment "l♝":

    +-+
    |♝|
    +-@

    The board fragment "r♟":

      +-+
      |♟|
    @ +-+

There is also the "identity movement", `1`, which means no movement at all.
That is, for any board fragment f, `1f = f`.

Movements can be combined with each other; for instance, `ur` means a movement
of one square to the right, followed by a movement of one square up.
That's a diagonal movement!.. and note that `ur = ru`, that is, it doesn't
matter whether we move up or right "first": a movement is only defined by
where it ends up.

    The board fragment "ru." (i.e. "." moved up and to the right):

      +-+
      | |
      +-+

    @

    The board fragment "rr♟" (i.e. "♟" moved to the right twice):

        +-+
        |♟|
    @   +-+

As a shorthand, instead of `rr`, we can write `r²`, and for `rrr`, we can
write `r³`, etc.
And since it's difficult to type superscripts like "²" and "³", let's say
that for any integer i, `m^i` means "do movement m, i times".
So, `m^2 = m² = mm`, etc.
Note that `m^1 = m`, that is, "do m once" is the same as m itself.
What about `m^0`?.. "do m zero times"?.. that's the same as the identity
movement, 1, which means "do nothing"!
We can also say that `r⁻¹ = l`, and `l⁻¹ = r`.
That is, moving to the right once is like moving to the left "negative one time".
And similarly, `r⁻² = l²`, etc.


### Gluing board fragments together

So far, we've made board fragments consisting of a single square.
Now we need a way to describe board fragments with multiple squares.
So let's add an operator, `+`, which takes two board fragments and glues
them together, keeping their centres lined up.
But you're never allowed to glue squares or pieces on top of each other!..
Here are some illustrations:

    The board fragment ". + r.":

    +-+-+
    | | |
    @-+-+

    The board fragment "♟ + r♜":

    +-+-+
    |♟|♜|
    @-+-+

    The board fragment ". + rru♘" (notice, board fragments don't need to
    be connected - they can have squares floating off by themselves):

        +-+
        |♘|
    +-+ +-+
    | |
    @-+

By the way, remember how we said that the symbol for the "empty fragment"
is `0`?.. we chose the symbols `0` and `+` on purpose, because `f + 0 = f`
for any board fragment f, just like with the number 0 and addition.
And `f + g = g + f`, for board fragments as well as numbers!
We could have chosen different symbols for chess algebra, but if you're
used to algebra with numbers, it's handy to use familiar symbols which
follow similar rules.
In fact, if you think about applying movements as being a "multiplication",
then you may notice certain rules of multiplication are true for chess
algebra as well, like `m(f + g) = mf + mg`.

Everything making sense?.. here's a bigger example of this "glue operator":

    Here are the board fragments "♘", "u.", "ur.", and "uur♚":

                              +-+
                              |♚|
           +-+       +-+      +-+
           | |       | |
    +-+    +-+       +-+
    |♘|
    @-+    @       @        @

    ...and here is their "sum", "♘ + u. + ur. + uur♚":

      +-+
      |♚|
    +-+-+
    | | |
    +-+-+
    |♘|
    @-+

    ...and we can apply movements to entire boards!
    So, here is that sum moved once to the right, i.e. "r(♘ + u. + ur. + uur♚)":

        +-+
        |♚|
      +-+-+
      | | |
      +-+-+
      |♘|
    @ +-+

We now have the power to build an entire chessboard out of algebra!
Look, I'll prove it...

    This board fragment (with the centre at the bottom-left corner)...

    ♜♞♝♚♛♝♞♜
    ♟♟♟♟♟♟♟♟
    ........
    ........
    ........
    ........
    ♙♙♙♙♙♙♙♙
    ♖♘♗♔♕♗♘♖

    ...can be written as:

    uuuuuuu(♜ + r(♞ + r(♝ + r(♚ + r(♛ + r(♝ + r(♞ + r♜))))))) +
     uuuuuu(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r♟))))))) +
      uuuuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
       uuuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
        uuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
         uu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
          u(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r♙))))))) +
           (♖ + r(♘ + r(♗ + r(♔ + r(♕ + r(♗ + r(♘ + r♖)))))))

Wheee!

And if you don't think that looks very nice, then let's add a couple of
operators to make it easier to build up board fragments.
Let's say, for any fragments f and g, `fg = f + rg`, and `f;g = f + ug`.
We can use these operators to build up horizontal (with `fg`) and vertical
(with `f;g`) lines of pieces:

    The board fragment "♖..;♙♗♙;.♙.", that is,
    "(♖ + r. + rr.) + u(♙ + r♗ + rr♙) + uu(. + r♙ + rr.)":

    .♙.
    ♙♗♙
    ♖..

    The board fragment "...;♙0♙;r♞", that is,
    "(. + r. + rr.) + u(♙ + rr♙) + uur♞":

     ♞
    ♙ ♙
    ...

Also, because this is an algebra, we can use variables, write equations,
define functions, etc.
For instance, if `x = ♙;.;♟`, then `xxx` is two lines of 3 pawns opposing
each other:

    ♟♟♟
    ...
    ♙♙♙


### A few more movements: rotation, flipping, colour reversal

Let's finish up our algebra of positions with operators for rotating and
flipping the board, and reversing the colours of chess pieces.

Let's define an operator `R`, which means a 90 degree clockwise rotation
of a board fragment.
This a "movement", like u, d, l, and r: imagine putting your fingers on
a chess board, and rotating it clockwise, along with all its pieces:

    The board fragment "r♟ + rd.":

          +-+
          |♟|
        @ +-+
          | |
          +-+

    The board fragment "R(r♟ + rd.)", i.e. "r♟ + rd. rotated around the
    centre by 90 degrees counter-clockwise":

      +-+-+
      |♟| |
      +-+-+

        @

    The board fragment "R²(r♟ + rd.)", i.e. "r♟ + rd. rotated around the
    centre by 180 degrees counter-clockwise":

    +-+
    | |
    +-+ @
    |♟|
    +-+

And how about `F`, which is a horizontal flip around the centre?..

    The board fragment "♖♟.":

          +-+-+-+
          |♖|♟| |
          @-+-+-+

    The board fragment "F(♖♟.)", i.e. "♖♟. flipped
    horizontally":

    +-+-+-+
    | |♟|♖|
    +-+-+-@

    The board fragment "RF(♖♟.)",
    i.e. "F(♖♟.) rotated 90 degrees counter-clockwise",
    i.e. "♖♟. flipped horizontally and then rotated 90 degrees
    counter-clockwise":

        +-@
        |♖|
        +-+
        |♟|
        +-+
        | |
        +-+

And how about `C`, which reverses the colours of the pieces?..

    The board fragment "♙ + r. + rr♗ + ur♟ + urr♞":

      +-+-+
      |♟|♜|
    +-+-+-+
    |♙| |♗|
    @-+-+-+

    The board fragment "C(♙ + r. + rr♗ + ur♟ + urr♞)":

      +-+-+
      |♙|♖|
    +-+-+-+
    |♟| |♝|
    @-+-+-+

We can combine these operators together, for instance `CRr` is the operator
which moves a board fragment right, then rotates it 90 degrees
counter-clockwise, then reverses the colours of all the pieces.

The "movement" operators, including colour reversal, all distrubute over the
glue operator, `+` - that is to say, for any movement m and board fragments
f and g, `m(f + g) = mf + mg`.
It may be helpful to see an example:

    The board fragment "♖ + r♟ + rr.":

          +-+-+-+
          |♖|♟| |
          @-+-+-+

    The board fragment "r(♖ + r♟ + rr.)":

            +-+-+-+
            |♖|♟| |
          @ +-+-+-+

    The board fragments "r♖", "rr♟", and "rrr.":

            +-+       +-+         +-+
            |♖|       |♟|         | |
          @ +-+   @   +-+   @     +-+

    The board fragment "r♖ + rr♟ + rrr.", which can be seen to be the
    same as "r(♖ + r♟ + rr.)" above:

            +-+-+-+
            |♖|♟| |
          @ +-+-+-+

As a final example, let's combine everything we've seen so far to reproduce
the initial position of the standard chessboard:

    bottom_right = 0♗♘♖;♙♙♙♙;....;....
    bottom = dddd(bottom_right + F(bottom_right) + l♔♕)
    full_board = bottom + RRC(bottom)

Powerful stuff. Soon, we'll extend this algebra so that we can express chess
moves in it. But first, a side note...


## Side note: abstract algebra, group theory, ring theory

This section is going to be all about algebra itself, we won't add anything
to our algebra of chess.
If that bores you, feel free to skip it!

Anyway, the operators we've described so far follow certain rules...
If the variables f, g, h are board fragments, and m, n are movements, then:
* `f + g = g + f`
* `f + 0 = f = 0 + f`
* `1m = m = m1`
* there is an inverse movement m⁻¹, such that `m(m⁻¹) = 1 = (m⁻¹)m`
* `m(f + g) = mf + mg`
* `mn = nm` (if m and n are both one of u, d, l, r)

All of these rules correspond to rules about numbers, addition, and
multiplication.

In abstract algebra, common rules are given names, for instance:
* "associativity", e.g. `(x + y) + z = x + (y + z)`
* "commutativity", e.g. `x + y = y + x` or `xy = yx`
* "identity", e.g. `x + 0 = x` or `1x = x`
* "inverse", e.g. `x + -x = 0` or `x(x⁻¹) = 1`
* "distributivity", e.g. `x(y + z) = xy + xz`

We can therefore quickly build up a new algebra using common rules.
Furthermore, there are names for specific groups of rules, for instance:
* a "group" is an invertible associative operator with an identity element,
  for instance `+` and `0`, or multiplication and `1`
* an "abelian group" is a group whose operator is commutative
* a "ring" is two groups, one of whose operators distributes over the other,
  for instance `+` and multiplication

One more rule of groups, which is rather subtle, is that whenever two things
exist (call them `x` and `y`), then `x + y` also exists.
This means that you don't actually need to decide up front what all the
things are... you don't have to say, "`+` is an operator which works on
numbers", you can just say, "`+` is a group with an identity element we'll
call 0, and some other element we'll call A", and immediately you know that
`A + A` also exists, and so does `A + A + A`, and so on.
And if you don't want to have to write `A + A + A + ...etc, 15 times`, you
could maybe just say that `15A` means 15 As added together.
And now, maybe A is the same as 1, in which case you have rediscovered
numbers!.. but maybe you also say that something else exists, let's call it
B. And so now, since A and B both exist, so does `A + B`. And so does
`2A + 3B`. And so on...
And if you have ever heard of "imaginary numbers", then perhaps this looks
a bit familiar!.. because the imaginary numbers are precisely an abelian
ring with 0 and `+` forming one group, 1 and multiplication forming the
other, and also something called `i`.
And since `i` exists, so does `i + i` or `2i`, and so does `i + i + i` or `3i`,
and so does `2 + 3i`, etc etc.

Now, what if we also declare that `4A = 0`?.. then how many different things
can we have?.. for instance, do we still have a `5A`?.. let's do some algebra:

    5A

    = 4A + A

    = 0 + A

    = A

Ah ha! So really, the only things we have are 0, A, 2A, and 3A. Every other
"sum of As" turns out to be one of those four things.
In fact, to be precise, for all integers n, `nA = (n % 4)A`, where `%` is the
"modulo" operation on integers, i.e. `n % 4` means "the remainder after
dividing n by 4".

An interesting thing about abelian groups is that they form grids.
If you recall, an "abelian" group is one where the operator is commutative,
meaning `x + y = y + x` for any two things x and y.
So, let's say that besides 0, we have two things called A and B.
By the rule of commutativity, it's therefore true that `2A + B = B + 2A`,
and `30A + 50B = 50B + 30A`, and in general `nA + mB = mB + nA` for any
positive integers n and m.
Now, if we draw a diagram where A means "move up", and B means "move right",
we get a grid:

    3A  +---+--[Y]--+
        |   |   |   |
    2A  +---+---+---+
        |   |   |   |
     A  +---+---+---+
        |   |   |   |
     0 [X]--+---+---+

        0   B  2B  3B

    Starting at zero, i.e. the [X] in the bottom-left corner, moving twice
    to the right and then 3 times upwards is the same as moving 3 times
    upwards and then twice to the right.
    That is, both of those movements take you to the [Y] in the top-right.
    In other words, 2B + 3A = 3A + 2B.

Why does this matter?.. because it means that you can actually create entire
mathematical structures (e.g. number systems, number-like systems,
geometries... and even games!) using algebra.
You don't need to start with a structure and then make up an algebra to
describe it, you can go the other way as well.
In our case, instead of describing "board fragments", and then defining `+`
in terms of gluing them together, and u, d, l, r in terms of sliding them
around, we could have just put on our mathematician hats and said something
like:
* let "board fragments" be a set of elements closed under an associative
  operator, `+`, with an identity element, 0 (the "empty board fragment")
* the following are also board fragments: .♟♚♛♝♞♜♙♔♕♗♘♖
* let "movements" be a set closed under an associative invertible operator,
  shown by concatenation, with an identity element, 1
* the following are also movements: uldrRFC (with u being the inverse of d,
  l being the inverse of r, and C being its own inverse)
* concatenation distributes over `+`, and has an abelian subgroup with kernel
  udlr
* (we leave out the definitions of R, F, and C for now, for brevity...)

...and already, we would be able to express any position in chess.
For instance, the initial position can be expressed like this:

    uuuuuuu(♜ + r(♞ + r(♝ + r(♚ + r(♛ + r(♝ + r(♞ + r♜))))))) +
     uuuuuu(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r♟))))))) +
      uuuuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
       uuuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
        uuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
         uu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
          u(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r♙))))))) +
           (♖ + r(♘ + r(♗ + r(♔ + r(♕ + r(♗ + r(♘ + r♖)))))))

...but the interesting thing is that we don't need to translate this into
a chessboard! We can just leave it as an algebraic expression, and define
all the moves of chess using algebra (as we'll see in the next section), and
play chess with it.
If we were to modify the rules of our algebra in various ways, we could
come up with algebras for other games as well - checkers, othello, chess
variants... even games with boards not based on square grids!

I'll stop there on the subject of abstract algebra itself for now.
If you're interested to learn more, you could do worse than by starting here:
* https://en.wikipedia.org/wiki/Abstract_algebra
* https://en.wikipedia.org/wiki/Group_theory
* https://en.wikipedia.org/wiki/Ring_theory
* https://en.wikipedia.org/wiki/Algebraic_geometry


## An algebra of chess moves

### Introducing the arrow operator

Okay! Earlier, we said that this was a valid chess move:

    .
    ♙

    ...can be replaced with:

    ♙
    .

Now let's express that move with our chess algebra, using a new operator,
`->`, which says that one board fragment can be replaced with another.
We're going to call this a "rule":

    The rule "♙;. can be replaced with .;♙":

    ♙;. -> .;♙

And now, let's do this one, where a pawn takes an enemy pawn diagonally:

     ♟
    ♙ 

    ...can be replaced with:

     ♙
    . 

Ready?! Ready?! Now watch this!!

    ♙;r♟ -> .;r♙

Now, this operator in no way limits us to only describing *valid* chess moves.
We can use it to describe *any* chess move, even one where you teleport your
king to the other side of the board, remove your opponent's queen, and add
two knights to your side, all in one move:

    ♔ + uuuuuu. + uurr♛ -> . + uuuuuu♔ + uurr. + lll♘ + rrr♘

It's not a *legal* move, but it's definitely a, um, move.
And we can describe it!

Now, can we describe a series of moves?
For example, moving a king one square up, then one square right?

    Moving a king one square up:

    ♔;. -> .;♔

    Moving a king one square right:

    ♔. -> .♔

    Moving a king one square up and to the right (all in one move):

    ♔;r. -> .;r♔

Let's show "doing one move, and then another" by simply putting two moves
next to each other:

    Moving a king one square up, then one square right:

    (♔;. -> .;♔)(♔. -> .♔)

One question we might ask is: when (if ever) can a series of moves which
follow each other be "simplified" into a single move?..

    Here is an equation, saying that moving a king one square up, then one
    square right, all in one move, is the same as (equal to) moving a king
    one square up and to the right, all in one move.
    Is this equation actually correct, I wonder?..

    (♔;. -> .;♔)(♔. -> .♔) = (♔;r. -> .;r♔)

    Here is another equation; on the left side, it describes moving a king
    upwards, and then moving a rook upwards.
    Does this expression "simplify"?.. doesn't seem like it!..

    (♔;. -> .;♔)(♖;. -> .;♖) = ???

Let's focus on the example of moving the king up and then to the right.
We showed an equation above, which claimed that moving your king up, and
then moving your king right, was the same as moving your king up-and-right.
But... that's only the case if you only have one king.
Which - in standard chess, at least - is indeed the case.
But what about moving a pawn up, and then moving a pawn up? Does it have
to be the same pawn each time?

    (♙;. -> .;♙)(♙;. -> .;♙) = (♙;.;. -> .;.;♙)  ...???

Let's pause for a moment and try to define "rules" more precisely.
I would like for the meaning of a rule like `♙;. -> .;♙` to be something
like "find any one piece ♙ with an empty square above it, and move the piece
onto the empty square".
But since there might be many pieces ♙ with empty squares above them, there
could be many possible positions resulting from this rule.
So, the way we will be interpreting rules is, "what are all the positions
which could result from making this move".

A bit more formally, let us say: a rule is something which can be applied to
a board fragment, and produces a set of board fragments.
A "set"!.. let's pause for another moment, and talk about set theory.


### Side note: set theory

I suppose you don't *really* need to read this section, but it might be
handy for understanding the concept of a "set of board fragments".

Set theory is a branch of mathematics focusing on "sets", in the sense of
"collections of things".
For instance, if you have a set of numbers, perhaps it consists of the
numbers 1 and 2. Or perhaps it consists of all the even numbers.
Already, you can see that a set can be finite, or infinite.
The defining characteristic of a set is that, given anything, you can say
whether that thing is in the set or not.
For instance, 20 is in the set of even numbers, but 21 is not.

The usual syntax for sets uses curly brackets, for instance `{1, 2, 3}`
is the set consisting of 1, 2, and 3.
There is exactly one empty set, `{}`, which also has its own symbol, `∅`.

Importantly, sets don't need to contain just numbers.
For instance, you can have a set containing other sets: `{∅}` is the set
containing just the empty set, `{∅, {∅}}` is the set containing just the
empty set and the set containing just the empty set, etc.

Set theory is interesting, because it has become the underpinning of almost
all of modern mathematics.
Almost every other branch of mathematics can be, and generally is, expressed
with it.

I'll stop there for now, but if you want to know more, you might try starting
here:
* https://en.wikipedia.org/wiki/Set_theory
* https://en.wikipedia.org/wiki/Foundations_of_mathematics


### The concept of "rules"

In any case, we were going to try to define "rules", before we got
sidetracked by set theory.
So, again, let's say a rule is something which can be applied to a board
fragment, and produces a *set* of board fragments.

(If we wish to use mathematical jargon, we may say "a rule is a function
from board fragments to sets of board fragments".)

What syntax shall we use for sets of board fragments?..
We could use the usual syntax for sets, with curly brackets `{...}`, but it
doesn't work very well with our chess algebra syntax.
For instance, here's a set of three board fragments: `{♙;., ♘..;..♚, 0}`.
I find that... not so readable. So let's use a new operator instead, `|`.
The meaning of `♙;. | ♘..;..♚ | 0` is the set consisting of those 3 board
fragments.
(If you read the "side note" earlier about abstract algebra, then you may
believe me if I tell you that `|` is an associative commutative operator
with identity element `∅`...)

How do we express a set with exactly one member?.. so for instance, is
`♙;.` a board fragment, or the set containing just that board fragment?..
In fact, I'm going to abuse our syntax a bit, and say that our operators
all accept board fragments *or* sets of board fragments.
To "abuse syntax" means, in the mathematical biz, to use the same syntax
for two different things, with the understanding that it will be obvious
what is meant in context.
In order for this abuse of syntax to work out nicely in our case, our
operators will all distribute over `|`, for instance `u(f | g) = uf | ug`,
`.(♙|♟). = .♙. | .♟.`, `(f -> g)(h | i) = (f -> g)h | (f -> g)i`, etc.
If a situation comes up where I need to make the distinction explicit, I'll
say e.g. "the set ♙;." or "the board fragment ♙;.".

If you are feeling lost, I apologize, and here is a picture describing the
meaning of "rules" in our chess algebra!

    Applying this rule ("a pawn can move forward into an empty square"):

    .        ♙
    ♙   ->   .

    ...to this board fragment (two pawns, with empty squares in front of them):

    ...
    ♙.♙

    ...produces this set of board fragments (one pawn could move forward, or
    the other could move forward):

    ♙..         ..♙
    ..♙   and   ♙..

...and we can express that example in chess algebra as:

    (♙;. -> .;♙)(♙.♙;...) = (..♙;♙..) | (♙..;..♙)

Make sense?.. here is another example:

    Applying this rule ("a pawn can move forward into an empty square"):

    .        ♙
    ♙   ->   .

    ...to this board fragment (two pawns, blocked by enemy pawns):

    ♟.♟
    ♙.♙

    ...produces the empty set!
    That is, neither pawn is able to move forwards.

...and we can express that example in chess algebra as:

    (♙;. -> .;♙)(♙.♙;♟.♟) = ∅

...isn't that fantastic?!


## Combining rules

Let's go back to this rule, which I mentioned wayyy earlier:

    .
    .
    .
    ♖

    ...can be replaced with any of:

    .   .   ♖
    .   ♖   .
    ♖   .   .
    .   .   .

...and I said we should be able to express it in terms of this rule:

    .
    ♖

    ...can be replaced with:

    ♖
    .

Well, here's how we write that last rule:

    ♖;. -> .;♖

And now the question is, how do we use that rule to express:

    ♖;.;.;. -> .;♖;.;. | .;.;♖;. | .;.;.;♖

Well, if `♖;. -> .;♖` is a rook moving one square up, then I would like for
something like `(♖;. -> .;♖)(♖;. -> .;♖)` to mean a rook moving two squares
up.
So, let's say concatenation of rules is an operator, whose meaning is "and
then":

    Move a rook one square up, and then move a rook one square up:

    (♖;. -> .;♖)(♖;. -> .;♖)

    Move a rook one square up, and then move a rook one square up, and then
    move a rook one square up:

    (♖;. -> .;♖)(♖;. -> .;♖)(♖;. -> .;♖)

...that's going to get tedious... let's use "²", "³", "^i", etc to indicate
the number of times a rule should be repeated. So:

    Move a rook one square up, and then move a rook one square up:

    (♖;. -> .;♖)²

    Move a rook one square up, and then move a rook one square up, and then
    move a rook one square up:

    (♖;. -> .;♖)³

But what about a rook moving one square up, and then *optionally* moving
another square up?.. let's use `?` as a suffix meaning "optionally":

    Move a rook up, and then optionally move a rook up:

    (♖;. -> .;♖)(♖;. -> .;♖)?

    Move a rook up, and then optionally move a rook up, and then optionally
    move a rook up:

    (♖;. -> .;♖)(♖;. -> .;♖)?(♖;. -> .;♖)?

...but what if we want to support chessboards of unlimited size?.. can we
introduce a symbol meaning "one or more times"?.. sure, let's use `+` as a
suffix for that:

    Move a rook up, and then optionally move a rook up, and then optionally
    move a rook up, and then... etc, forever:

    (♖;. -> .;♖)+

Programmers, wake up. Did your ears twitch just now? Did your nostrils
widen, and did you think to yourself "smells like regular expressions"?
Yes. Yesssss, that is exactly where we're going with this.

If you've never heard of a "regular expression", you could do worse than to
begin here:
* https://en.wikipedia.org/wiki/Regular_expression

In any case, I'm going to steal some syntax from regular expressions, and
lay it out for you here:

    The syntax of repeated rules!

    Finite repetition:

    R^2 = R² = RR

    ...and in general, for any positive integer i,
    R^i = "R repeated i times"

    Finite optional repetition:

    R{2, 4} = RR | RRR | RRRR = "R repeated between 2 and 4 times"

    ...and in general, for any positive integers i and j,
    R{i, j} = "R repeated between i and j times"

    Infinite optional repetition:

    R{2, ∞} = RR | RRR | RRRR | RRRRR | ... = "R repeated at least 2 times"

    ...and in general, for any positive integer i,
    R{i, ∞} = "R repeated at least i times"

    And finally, some handy shorthands:

    R? = R{0, 1}
    R* = R{0, ∞}
    R+ = R{1, ∞}

Alrighty! Now are we done? Can we describe rook movement like this?

    Move a rook up, one or more times:

    (♖;. -> .;♖)+

Not quite! Because there's nothing yet to guarantee that we are moving the
*same* rook up each time.
Consider:

    If we apply this rule (move a rook up, then move a rook up):

    (♖;. -> .;♖)(♖;. -> .;♖)

    ...to this board fragment:

    ...
    ...
    ♖.♖

    ...then these are the possible resulting board fragments:

    ♖..         ...         ..♖
    ...   and   ♖.♖   and   ...
    ..♖         ...         ♖..

...right?! Because these are the possible series of moves:
* move left rook, move left rook
* move left rook, move right rook
* move right rook, move left rook
* move right rook, move right rook

...and the middle two of those series produce the same board fragment in the
end (the one with both rooks on the same horizontal rank).
So, 3 possible resulting board fragments.

So, how do we specify that multiple rules apply to "the same piece"?..


### Pieces of interest

Let's introduce the idea of a "piece of interest" (POI for short).
We'll use the symbol `%` to represent the POI; and so, `%` becomes a board
fragment, just like `.` or `♙`.
Now, we can write:

    Move the POI up, and then move the POI up:

    (%;. -> .;%)²

Ah ha! Now let's add a way to specify, or choose, the POI.
Here, then, is some new syntax: "%♖: ..." will mean "choose some rook as
the POI, and then...".
In general, if p is a piece, and R is a rule, then `%p: R` is a rule.

Now, can we finally move a rook two squares up?.. yes we can!

    Pick a rook, move it up, then move it up again:

    %♖: (%;. -> .;%)²

Make sense?..
And this "%♖: ..." syntax isn't special; it can be stuck inside more
complicated combinations of moves, for instance:

    Move a single rook up twice, then move a single pawn up twice:

    (%♖: (%;. -> .;%)²)(%♙: (%;. -> .;%)²)

And now. Finally. Can we describe how a rook moves?..

    Pick a rook, and move it up one or more times:

    %♖: (%;. -> .;%)+

Boom, now we're cooking with chess algebra.


### Reusing rules in multiple directions

Several chess pieces (rook, bishop, knight, king, queen) have movement rules
which we could define in one direction, then rotate 4 times to get the
complete movement rule.
We can make use of the rotation operator, `R`, to achieve this.
Let's continue with our example of the rook:

    rook_move_u = (%;. -> .;%)+

    rook_move = %♖: (rook_move_u | R rook_move_u | R² rook_move_u | R³ rook_move_u)

Also, if you are familiar with regular expressions, the following definition
of a rook's ability to take a pawn may make some sense:

    rook_move_u = (%;. -> .;%)+

    rook_take_u = (%;. -> .;%)* (%;♟ -> .;%)

    rook_move_or_take_u = rook_move_u | rook_take_u

    rook_move_or_take = %♖: rook_move_or_take_u | R rook_move_or_take_u | R² rook_move_or_take_u | R³ rook_move_or_take_u

We can make our lives a bit easier by allowing ourselves to define functions;
for instance, the definition of rook_move_or_take becomes much shorter if we
use a function to abstract away the concept of making the same move in any of
the 4 cardinal directions...

    in_any_direction(M) = M | R M | R² M | R³ M

    rook_move_or_take = %♖: in_any_direction(rook_move_or_take_u)

Also, you may have noticed that according to our definition above, rooks can
only take enemy pawns.
How can we easily extend that to all enemy pieces?..

    enemy_pieces = ♟ | ♚ | ♛ | ♝ | ♞ | ♜

    rook_take_u = (%;. -> .;%)* (%;(enemy_pieces) -> .;%)

...notice how we've replaced "♟" with "enemy_pieces" in the rule "rook_take_u".
And, since we said that all our operators distribute over `|`, this means that:

    rook_take_u = (%;. -> .;%)* (%;(enemy_pieces) -> .;%)

                = (%;. -> .;%)* (%;(♟|♚|♛|♝|♞|♜) -> .;%)

                = (%;. -> .;%)* (
                    (%;♟ -> .;%) |
                    (%;♚ -> .;%) |
                    (%;♛ -> .;%) |
                    (%;♝ -> .;%) |
                    (%;♞ -> .;%) |
                    (%;♜ -> .;%)
                  )

...do you believe me?


## Extending chess algebra

So far, we've seen how to describe simple piece movements.
But what about castling?.. what about pawn promotion?.. what about pawns
being allowed to move two squares on their first move?.. what about "en
passant"?..
We can describe all of this, and more.

For instance, let's introduce a board fragment `#`, which means "off the board".
That is, whereas `.` means a square of the board, onto which a piece could be
placed, `#` means somewhere off the board, where a piece cannot be placed.
Now we can define some of the stranger pawn behaviour:

    Pawns may move twice from their starting position:

    #;0;♙;.;. -> #;0;.;.;♙

    Pawns may turn into a queen upon reaching the opposite rank:

    ♙;.;# -> .;♕;#

What about castling?.. we can describe the basic "swapping king with rook"
move easily enough:

    (#♖..♔ -> #.♔♖.) | (♔...♖# -> .♖♔..#)

...but what about the condition that the king not be in, or pass through,
check?..
For that, we need to be able to detect check; and we need to be able to
express a rule which only applies when some condition is met.
Let's introduce some syntax!
If A is a condition (something which can be true or false) and B and C
are rules, then let's say `if A then B else C` is a rule.
And as a shorthand let's have C default to ∅, that is,
`(if A then B) = (if A then B else ∅)`.

So now, what are conditions?
Actually, we've already seen some... in rules of the form `f -> g`, we're
using the board fragment f as a sort of condition.
But it's a bit more complicated than that...

TODO: introduce "matching", "finding", and "replacing"?..


## What can we do with it?

We could simply gaze at it in wonder!

Or we could use it to express other games, like checkers or Othello!
Even ones with boards which aren't a square grid, like Chinese checkers!
Or we could express chess variants, like
[Irreversible Chess](/entries/2025/jul/irreversible_chess.md)!

We could also implement a software library which can parse it, and use it
to quickly play different chess variants!
That sounds fun. Maybe we'll do that and
[link to it here](algchess.py)...


================================================================

    ♜♞♝♚♛♝♞♜
    ♟♟♟♟♟♟♟♟
    ........
    ........
    ........
    ........
    ♙♙♙♙♙♙♙♙
    ♖♘♗♔♕♗♘♖

