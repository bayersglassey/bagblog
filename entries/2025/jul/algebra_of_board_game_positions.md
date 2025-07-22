# An algebra of board game positions

I've been a fan of abstract algebra, and algebraic geometry, since University.

I also enjoy reading and thinking about chess and other board games.
I like playing them too, for fun, and for purposes of experimentation.

## What is algebra?

I think a halfway decent description of "an algebra" is: a set of rules for
replacing parts of something you've written down.

So for instance, let's say you've written this down on a piece of paper:

    x + 1 - 1

One of the rules of "regular algebra" (the one with numbers, you know the one)
says that you're allowed to erase the `1 - 1` there and replace it with `0`:

    x + 0

And then another rule says, you can replace `x + 0` with `x`:

    x

But then *another* rule says, you can replace `x` with `x * 1`:

    x * 1

And another rule says, you can replace `1` with `20 / 20`:

    x * 20 / 20

Right? Notice how at one point, we had x all by itself.
And sometimes, we're playing a game with algebra where we want to do that,
like when we have an equation, and we're trying to "solve for x":

    3x + 4 = 5

But our goal of solving for x isn't one of the rules of algebra; it's just
something we layer on top.
Algebra doesn't tell us that we *have* to solve for x; in fact, it says it's
totally fine if we do this:

    3x + 4 - 7y = 5 - 7y

We could turn this into a sort of multiplayer game, where there's an equation
written down, and players take turns applying rules of algebra to it, one at
a time.
Maybe the players are trying to work together to solve for a variable?..
Maybe there are 3 players, each trying to solve for a different variable?..
Maybe there are a whole bunch of players, and they're allowed to form alliances,
and each player has a secret goal which they keep secret from the other players?..
But in any case, the rules of algebra tell us that every time a player makes
a "move", they are only allowed to change the equation in certain ways.

Just let that idea float around in your mind for a minute: algebra is just
some rules, without a goal.
The rules have to do with what's allowed to be written down on a piece of
paper, and how people are allowed to make changes to it.

And I think, when you open your mind to that fact, you can start to see
a connection between algebra and board games.
In algebra, when we write something down on a piece of paper, that piece
of paper is like the board in chess.
Let's say that algebra and chess are both games, and the paper and board
are called the game's "state".
Some of the game rules are an algebra describing how the state is allowed
to change.
When a player takes their turn, they do so by changing the game's state
according to the rules of the game's algebra.
Other game rules describe the players, their goals, the order in which
they take turns, etc; but let's forget about those rules for now, and
focus on the algebra.


## The algebra of chessboard fragments

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
that `x + 0` can be replaced with `x` can be applied anywhere within an
expression or equation.

Now, here is another rule:

    .
    .
    .
    ♖

    ...can be replaced with any of:

    .   .   ♖
    .   ♖   .
    ♖   .   .
    .   .   .

An interesting question here is, "how can we express this rule more simply"?
And I think it's clear that we could express it in terms of this rule:

    .
    ♖

    ...can be replaced with:

    ♖
    .

Now, let's gear up like proper mathematicians and start coming up with some
syntax here.
We're going to come up with a way to describe fragments of chess boards as
algebraic expressions.
In fact, we're going to come up with an "algebra of chessboard fragments".
Let's say that all board fragments have a center.
The "empty board fragment" is indicated by 0, and consists of no squares or
pieces.
The symbol `.` is the board fragment consisting of an empty square, and the
center of this board fragment is the square's bottom-left corner.
The symbols `♟`, `♙`, `♚`, `♔`, etc are the board fragments consisting of
squares with the indicated piece on them, and the centers of these board
fragments are their squares' bottom-left corners.

There are also "movements".
The basic movements are `u`, `d`, `l`, and `r`, meaning movements of 1 square
up, down, left, and right.
There is also the "identity movement", `1`, which means not moving at all.
Given a board fragment f and movement m, we can apply m to f, resulting in
another board fragment.
For instance, `u.` is the board fragment consisting of an empty square, but
where the fragment's center is one square's width down from the square's
bottom-left corner.
Movements can be combined with each other; for instance, `ur` means a movement
of one square to the right, followed by a movement of one square up.
That's a diagonal movement!.. and note that `ur` = `ru`, that is, it doesn't
matter whether we move up or right "first": a movement is only defined by
where it ends up.

Here's an illustration of some board fragments, with "@" showing the center:

    The empty board fragment, "0":

    @

    The board fragment ".":

    +-+
    | |
    @-+

    The board fragment "r.":

      +-+
      | |
    @ +-+

    The board fragment "ru.":

      +-+
      | |
      +-+

    @

    The board fragment "l.":

    +-+
    | |
    +-@

    The board fragment "♟":

    +-+
    |♟|
    @-+

    The board fragment "r♟":

      +-+
      |♟|
    @ +-+

Making sense so far?..

There is also an operator, `+`, which takes two board fragments and glues
them together, keeping their centers lined up.
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

I hope it's clear that we could build up a picture of a chessboard this way;
that is, we can express any chess position using this algebra.
Next, we'll see how to express valid chess moves.

By the way, for any movement m, it's the case that 1m = m = m1, and m0 = 0.
It's also the case that every movement has an inverse movement n, such that
mn = 1.
You can write "m⁻¹" for "the inverse of m".
Also, for any board fragment f, it's the case that f + 0 = f.
Also, for any movement m, and board fragments f and g, it's the case that
m(f + g) = mf + mg!..
In abstract algebra, we would say that the movements form a "group", and so
do the board fragments, and together, the movements and board fragments form
a "ring". Just like addition and multiplication of numbers! Ooooh fancy.
Also, I'll tell you a secret: we are doing algebraic geometry here, where
"board fragments" are sets, "squares" are points (as in, the kinds of points
which can form a line or a shape), 0 is the empty set, and `+` is set union.

Okay! Earlier, we said that this was a valid chess move:

    .
    ♙

    ...can be replaced with:

    ♙
    .

Now let's express that move with our chess algebra:

    ♙ + u. -> . + u♙

Right?! Right?! Awww man, look at it, that's so cool!..

And now, let's do this one, where a pawn takes an enemy pawn diagonally:

     ♟
    ♙ 

    ...can be replaced with:

     ♙
    . 

Ready?! Ready?! Now watch this!!

    ♙ + ur♟ -> . + ur♙

Phew! Okay, let's take a break.


====================================================================

    ♜♞♝♚♛♝♞♜
    ♟♟♟♟♟♟♟♟
    ........
    ........
    ........
    ........
    ♙♙♙♙♙♙♙♙
    ♖♘♗♔♕♗♘♖

