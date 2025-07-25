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

Right? Notice how at one point, we had x all by itself.
And sometimes, we're playing a game with algebra where we want to do that,
like when we have an equation, and we're trying to "solve for x":

    3x + 4 = 5

But our goal of solving for x isn't one of the rules of algebra; it's just
something we layer on top.
Algebra doesn't tell us that we *have* to solve for x; in fact, it says it's
totally fine if we introduce a new variable, e.g. like this:

    3x + 4 = 5 + 7y - 7y

We could turn this into a sort of multiplayer game, where there's an equation
written down, and players take turns applying rules of algebra to it, one at
a time.
Maybe the players are trying to work together to solve for a variable?..
Maybe each player is trying to solve for a different variable?..
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
    ♖   .   .
    .   .   .

An interesting question here is, "how can we express this rule more simply"?
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
Keep that in mind!

Now, let's gear up like proper mathematicians and start coming up with some
syntax here.
We're going to come up with a way to describe fragments of chess boards as
algebraic expressions.
In fact, we're going to come up with an "algebra of chessboard fragments".
Here we go!..

Here is a "board fragment":

    .♛.
    ....
     .♔♙

...it has some empty squares, and some squares with pieces on them.
It has no edge: it's like a small cut-out from a full chessboard.
The full chessboard is also a board fragment, though; and so is the "empty
board fragment", which consists of... nothing. No squares, no pieces.

Let's also say that all board fragments have a center.
So, the following diagram could be for many different board fragments,
depending on where we say its "center" is:

     .
    .♖.
     .

The center is always at the *corners* of the board's grid of squares.
So for instance, here are two different board fragments, drawn with the
grid visible, and the center indicated with "@":

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

The symbol `0` will mean the empty board fragment.

The symbol `.` will mean the board fragment consisting of an empty square,
with this board fragment's center at the square's bottom-left corner.
The symbols `♟`, `♙`, `♚`, `♔`, etc are like `.`, but with the indicated
piece sitting on the square.

There are also "movements". These are ways of moving a board fragment around
relative to its center.
Imagine putting your finger on a chessboard (or a little cut-out fragment of
a chessboard) and sliding it around: you could slide it to the left, to the
right...

The basic movements are `u`, `d`, `l`, and `r`, meaning movements of the board
fragment 1 square up, down, left, and right relative to its center.
You could also think of these movements as moving the center relative to the
rest of the board fragment, but trust me for now that it's more useful to
think of sliding the board relative to the center.

There is also the "identity movement", `1`, which means no movement at all.

Given a board fragment f and movement m, we can apply m to f, resulting in
another board fragment.
For instance, `u.` is the board fragment consisting of `.` slid upwards by
one square's width relative to the center.

Movements can be combined with each other; for instance, `ur` means a movement
of one square to the right, followed by a movement of one square up.
That's a diagonal movement!.. and note that `ur = ru`, that is, it doesn't
matter whether we move up or right "first": a movement is only defined by
where it ends up.

Here's an illustration of some board fragments, with "@" showing the center:

    The empty board fragment, "0":

    @

    The board fragment ".":

    +-+
    | |
    @-+

    The board fragment "r." (i.e. "." moved to the right):

      +-+
      | |
    @ +-+

    The board fragment "ru." (i.e. "." moved up and to the right):

      +-+
      | |
      +-+

    @

    The board fragment "l." (i.e. "." moved to the left):

    +-+
    | |
    +-@

    The board fragment "♟":

    +-+
    |♟|
    @-+

    The board fragment "r♟" (i.e. "♟" moved to the right):

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

Making sense?.. here's a bigger example of this "glue operator":

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

I hope it's clear that we could build up a picture of a chessboard this way;
that is, we can express any chess position using this algebra.
In fact, I'll prove it to you:

    This board fragment (with the center at the bottom-left corner)...

    ♜♞♝♚♛♝♞♜
    ♟♟♟♟♟♟♟♟
    ........
    ........
    ........
    ........
    ♙♙♙♙♙♙♙♙
    ♖♘♗♔♕♗♘♖

    ...can be written as:

    uuuuuuu(♜ + r(♞ + r(♝ + r(♚ + r(♛ + r(♝ + r(♞ + r(♜)))))) +
     uuuuuu(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r(♟ + r♟))))))) +
      uuuuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
       uuuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
        uuu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
         uu(. + r(. + r(. + r(. + r(. + r(. + r(. + r.))))))) +
          u(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r(♙ + r♙))))))) +
           (♖ + r(♘ + r(♗ + r(♔ + r(♕ + r(♗ + r(♘ + r♖)))))))

Right?.. Do you see?.. Do you see???

Next, we'll see how to express valid chess moves.


## A note on abstract algebra

By the way, for any movement m, it's the case that `1m = m = m1`, and `m0 = 0`.
It's also the case that every movement has an inverse movement n, such that
`mn = 1`.
You can write `m⁻¹` for "the inverse of m".
Also, for any board fragment f, it's the case that `f + 0 = f`.
Also, for any movement m, and board fragments f and g, it's the case that
`m(f + g) = mf + mg`!..
In abstract algebra, we would say that the movements form a "group", and so
do the board fragments, and together, the movements and board fragments form
a "ring". Just like addition and multiplication of numbers! Ooooh fancy.
Also, I'll tell you a secret: we are doing algebraic geometry here, where
"board fragments" are sets, "squares" are points (as in, the kinds of points
which can form a line or a shape), `0` is the empty set, and `+` is set union.

**If none of this terminology sounds familiar or makes sense, don't worry about
it. Let's get back to chess.**

But you may or may not be interested in the following:
* https://en.wikipedia.org/wiki/Abstract_algebra
* https://en.wikipedia.org/wiki/Group_theory
* https://en.wikipedia.org/wiki/Ring_theory
* https://en.wikipedia.org/wiki/Algebraic_geometry


## The algebra of chess moves

Okay! Earlier, we said that this was a valid chess move:

    .
    ♙

    ...can be replaced with:

    ♙
    .

Now let's express that move with our chess algebra, using a new operator,
`->`, which says that one board fragment can be changed into another:

    ♙ + u. -> . + u♙

And now, let's do this one, where a pawn takes an enemy pawn diagonally:

     ♟
    ♙ 

    ...can be replaced with:

     ♙
    . 

Ready?! Ready?! Now watch this!!

    ♙ + ur♟ -> . + ur♙

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

    ♔ + u. -> . + u♔

    Moving a king one square right:

    ♔ + r. -> . + r♔

    Moving a king one square up and to the right (all in one move):

    ♔ + ur. -> . + ur♔

I would like a way of saying that one move was (or can be) made, and then
another move was (or can be) made.
Let's show "doing one move, and then another" by simply putting two moves
next to each other:

    Moving a king one square up, then one square right:

    (♔ + u. -> . + u♔)(♔ + r. -> . + r♔)


One question we might ask is: when (if ever) can a series of moves which
follow each other be "simplified" into a single move?..

    Here is an equation, saying that moving a king one square up, then one
    square right, all in one move, is the same as (equal to) moving a king
    one square up and to the right, all in one move.
    Is this equation actually correct, I wonder?..

    (♔ + u. -> . + u♔)(♔ + r. -> . + r♔) = (♔ + ur. -> . + ur♔)

    Here is another equation; on the left side, it describes moving a king
    upwards, and then moving a rook upwards.
    Does this expression "simplify"?.. doesn't seem like it!..

    (♔ + u. -> . + u♔)(♖ + u. -> . + u♖) = ???

Let's focus on the example of moving the king up and then to the right.
We showed an equation above, which claimed that moving your king up, and
then moving your king right, was the same as moving your king up-and-right.
But... that's only the case if you only have one king.
Which - in standard chess, at least - is indeed the case.
But what about moving a pawn up, and then moving a pawn up? Does it have
to be the same pawn each time?

    (♙ + u. -> . + u♙)(♙ + u. -> . + u♙) = (♙ + u. + uu. -> . + u. + uu♙)  ...???

If you are lost, that's probably because **this is not a good syntax for
visualizing the board.**
So don't feel lost, don't run away from me please, stay, yes stay with me,
here I'll give you a nice picture of a chessboard:

    .......
    ..♙.♙..

    I'm going to argue that applying the move (♙ -> . + u♙) could give us
    *either* of:

    ..♙....        ....♙..
    ....♙..   or   ..♙....

Now, I've been jumping ahead like crazy here with this syntax and these
rules, so in case you're wondering -- I'm not *proving* anything here about
this syntax.
I'm actually coming up with the rules for it as I go along.
I have decided, just now, that I would like for the meaning of a move like
`♙ + u. -> . + u♙` to be "find any one piece ♙ with an empty square above it,
and move the piece onto the empty square".

But this means that the following equation is *not* correct:

    (♙ + u. -> . + u♙)(♙ + u. -> . + u♙) = (♙ + u. + uu. -> . + u. + uu♙)

...that is, to tell someone "move some pawn up, and then move some pawn up",
is not the same as to tell someone "move some pawn up twice".

Let's ponder that for a moment... just savour the idea for a second...
Okay, now I'm going to jump around again.

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

Well, here's how we write that last rule, as a "move":

    ♖ + u. -> . + u♖

And now the question is, how do we use that rule to express (and I'm going
to add some new syntax here, watch me now) this rule:

    ♖ + u. + uu. + uuu. -> (. + u♖ + uu. + uuu.) | (. + u. + uu♖ + uuu.) | (. + u. + uu. + uuu♖)

See what I did there? I added `|` to mean "any of".
So like, `x -> y | z` means "the move where board fragment x becomes either
board fragment y, or board fragment z".

And I would *like* to express the rook's movement as something like:

    (♖ + u. -> . + u♖)(♖ + u. -> . + u♖)(♖ + u. -> . + u♖)

...or better yet, forget about limiting the rook to moving forward by
only 3 squares, what we really want is something more like:

    (♖ + u. -> . + u♖)+

...where the `+` at the end means "do this movement 1 or more times".
Programmers, wake up. Did your ears twitch just now? Did your nostrils
widen, and did you think to yourself "smells like regular expressions"?
Yessss. Yesssss, that is exactly where we're going with this.

But let's go back again to the question of how to apply a rule repeatedly
to the *same piece*. For instance, consider this rule:

    Move a rook up:

    ♖ + u. -> . + u♖

Now, let's introduce some more syntax: if M is a move, then `M{2}` means
"do M, and then do M". In general, we can write `M{n}` for any integer n.
We can now write:

    Move a rook up, and then move a rook up:

    (♖ + u. -> . + u♖){2}

But how do we write the rule "move a rook up, and then move the same rook
up"?
Let's introduce the idea of a "piece of interest" (POI for short).
Idunno if that'll do quite what we want, but let's see.
Let's use the symbol `%` to represent the POI.
Now, we can write:

    Move the POI up, and then move the POI up:

    (% + u. -> . + u%){2}

And now let's add a way to specify that the POI is a specific piece...
let's use e.g. "%♖: ..." to mean "choose some rook as the POI, and then...",
and "%♙" to mean "choose some pawn as the POI, and then...", etc:

    Move a rook up, and then move it up again:

    %♖: (% + u. -> . + u%){2}

Make sense?.. that's all a single move.
And this "%♖: ..." syntax isn't special; it can be stuck inside more
complicated combinations of moves, for instance:

    Move a single rook up twice, then move a single pawn up twice:

    (%♖: (% + u. -> . + u%){2})(%♙: (% + u. -> . + u%){2})

Boom, now we're cooking with chess algebra.


## Chess algebra made rigorous

Let's take a little pause, stop adding new syntax, and just describe what
we've come up with so far. Explicitly this time, not just by piling up
example upon example.

    A basic movement is one of: 1 u d l r R
        * the meaning of R is a counter-clockwise rotation of 90 degrees
    A movement is one of:
        * a basic movement
        * nm (where n, m are movements)
            * Note that 1m = m = m1
            * If n and m do not contain any rotations R, then nm = mn
        * n⁻¹, n², or in general n^i, where n is a movement and i is an integer
            * The meaning of n⁻¹ is the inverse of n, such that nn⁻¹ = 1.
            * The meaning of n² is nn, n³ is nnn, n^4 is nnnn, etc.
                * Note that R^4 = 1, i.e. 4 90 degree rotations are equivalent
                  to no movement at all.

    A chess piece is one of: ♙ ♔ ♕ ♗ ♘ ♖ ♟ ♚ ♛ ♝ ♞ ♜
    A basic board fragment either a chess piece, or one of: 0 . % #
    A board fragment is one of:
        * a basic board fragment
        * mf (where m is a movement, and f is a board fragment)
        * f + g (where f and g are board fragments)
            * Note that f + g = g + f, and 0 + f = f = f + 0
            * Note also that m(f + g) = mf + mg, for any movement m

    A board fragment pattern is one of:
        * a board fragment
        * f | g (where f and g are board fragment patterns)
            * The meaning is, either f or g
    A move is one of:
        * nil
            * The meaning is: the empty move, i.e. the move which consists
              of doing nothing, leaving the board exactly as it was
        * f -> g (where f and g are board fragment patterns)
        * %p: M (where p is a chess piece and M is a move)
            * The meaning is: choose a specific piece on the board.
              It is now the POI (piece of interest).
              Now do M.
        * MN (where M and N are moves)
            * The meaning is, do M and then do N.
            * Note that nil M = M = M nil, that is, "doing nothing and
              then doing M" is the same as simply doing M, and so is
              "doing M and then doing nothing".
        * M | N (where M and N are moves)
            * The meaning is "do either M or N"
            * Note: I belieeeeve that f -> (g | h) is probably equivalent
              to (f -> g) | (f -> h) ...but the proof is left as an
              excercise to the reader ;)
        * M{i} (where M is a move and i is an integer)
            * The meaning is "do M i times", e.g. M{3} = MMM
                * Note that M{0} = nil
        * M{i, j} (where M is a move and i and j are integers)
            * The meaning is "do M between i and j times"
              e.g. M{2, 4} = M{2} | M{3} | M{4} = MM | MMM | MMMM
        * M*
            * The meaning is "do M zero or more times"
              i.e. M* = nil | M | MM | MMM | MMMM | ...
        * M+
            * The meaning is "do M one or more times"
              i.e. M+ = M | MM | MMM | MMMM | ...
                * Note that M* = nil | M+
        * M?
            * The meaning is "maybe do M", i.e. M? = nil | M
                * Note that M? = M{0, 1}

Didja memorize all that?!?!?!

Don't worry, if it makes your eyes glaze over, you're free to ignore it.
But the fact that I was able to write it down makes me more confident that
our algebra is self-consistent, and we're not just waving our hands around
saying crazy things.
For instance, I reckon we could likely implement this algebra in software...
hint hint...

By the way, I snuck in some new concepts! Did you notice?

For instance, there is now a board fragment `#`, which means "off the board".
That is, whereas `.` means a square of the board, onto which a piece could be
placed, `#` means somewhere off the board, where a piece cannot be placed.
We need this to define certain valid pawn moves:

    Pawns may move twice from their starting position:

    dd# + ♙ + u. + uu. -> dd# + . + u. + uu♙

    Pawns may turn into a queen upon reaching the opposite rank:

    ♙ + u# -> . + u♕

I have also added a rotation movement, R. Here is an illustration of it:

    The board fragment "r♟" (recall, @ is the board fragment's center):

          +-+
          |♟|
        @ +-+

    The board fragment "Ru♟", i.e. "u♟ rotated around the center by 90
    degrees counter-clockwise":

      +-+
      |♟|
      +-+

        @

    The board fragment "R²u♟", i.e. "u♟ rotated around the center by 180
    degrees counter-clockwise":

    +-+ @
    |♟|
    +-+

Make sense?.. this will allow us to more easily define the movement of
e.g. the rook:

    rook_move_u = (% + u. -> . + u%)+

    rook_move = %♖: (rook_move_u | R rook_move_u | R² rook_move_u | R³ rook_move_u)

Also, if you are familiar with regular expressions, the following definition
of a rook's ability to take a pawn may make some sense:

    rook_move_u = (% + u. -> . + u%)+

    rook_take_u = (% + u. -> . + u%)* (% + u♟ -> . + u%)

    rook_move_or_take_u = rook_move_u | rook_take_u

    rook_move_or_take = %♖: rook_move_or_take_u | R rook_move_or_take_u | R² rook_move_or_take_u | R³ rook_move_or_take_u

We can make our lives a bit easier by allowing ourselves to define functions;
for instance, the definition of rook_move_or_take becomes much shorter if we
use a function to abstract away the concept of making the same move in any of
the 4 cardinal directions...

    in_any_direction(M) = M | R M | R² M | R³ M

    rook_move_or_take = %♖: in_any_direction(rook_move_or_take_u)

We can also express more complicated things, like defining rules for taking
any enemy piece:

    Here are some board fragment patterns:

    unfilled = ♙ | ♔ | ♕ | ♗ | ♘ | ♖

    filled = ♟ | ♚ | ♛ | ♝ | ♞ | ♜

    Here is a rule which says that a pawn make take any enemy piece diagonally:

    pawn_takes = (♙ + ur filled -> . + ur ♙) | (♙ + ul filled -> . + ul ♙)

We can also define rules for one player, and then use functions to easily
"copy" those rules for the other player:

    Here is a function which converts a board fragment pattern or move
    into one in which the "colours" of all pieces have been swapped:

    colour_swapped(♙) = ♟
    colour_swapped(♔) = ♚
    ...etc...
    colour_swapped(f + g) = colour_swapped(f) + colour_swapped(g)
    colour_swapped(f | g) = colour_swapped(f) | colour_swapped(g)
    colour_swapped(mf) = m colour_swapped(f)
    ...etc...

    And here is a function which converts a board fragment pattern or move
    into one in which the board has been "flipped" - the colours of all pieces
    have been swapped, and the board has been rotated 180 degrees:

    flipped(f) = R² colour_swapped(f)
    flipped(f -> g) = flipped(f) -> flipped(g)
    flipped(M N) = flipped(M) flipped(N)
    ...etc...

Are you with me so far?.. yes?.. no?..

Look, even if you don't fully follow everything here, I hope you can at
least believe me that we have found a way to express chess positions and moves
using algebra.

Isn't that cool?


## What can we do with it?

We could simply gaze at it in wonder!

Or we could use it to express chess variants, like
[Irreversible Chess](/entries/2025/jul/irreversible_chess.md)!

We could also implement a software library which can parse it, and use it
to quickly play different chess variants!
That sounds fun. Maybe we'll do that and
[link to it here](algchess.py)...


## Appendix A: when do two moves simplify into one?

For any move M, it is the case that `nil M = M = M nil`.
That is, "do nothing and then do M" is the same as "do M", and the same as
"do M and then do nothing".
By two moves being "the same", I mean that they always apply to the same
board fragments, and transform them into the same board fragments.

Now, let's consider the case of a rook moving forwards one or two squares.

    Move a rook forward if there is space, then forward again if there is
    still space.

    %♖: (% + u. -> . + u%){2}

...isn't this equivalent to the following rule?..

    Move a rook forward if there is space for that, or move it forward
    twice if there is space for that.

    %♖: (% + u. -> . + u%) | (% + u. + uu. -> . + u. + uu%)

...no, I don't think they are the same... because the second rule gives
you a choice, when there are two squares of space ahead, between moving
one or two squares forward.
Whereas the first rule says, move forward if you can, and then move
forward *again* if you can.

But I believe *this* rule is equivalent to the second one above:

    %♖: (% + u. -> . + u%) (% + u. -> . + u%)?

...that is, move forward if you can, and then *maybe* move forward if
you can.
That is, once you've moved forward once, you can then choose to behave
like `nil` or `(% + u. -> . + u%)`.

Now, can we *prove* that these rules are equivalent?..
What are the basic laws or axioms of rule equivalence which we can use
to prove such theorems?..


================================================================

    ♜♞♝♚♛♝♞♜
    ♟♟♟♟♟♟♟♟
    ........
    ........
    ........
    ........
    ♙♙♙♙♙♙♙♙
    ♖♘♗♔♕♗♘♖

