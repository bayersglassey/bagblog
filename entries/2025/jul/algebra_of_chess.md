# An Algebra of Chess

I've been a fan of abstract algebra, and algebraic geometry, since University.

I also enjoy reading and thinking about chess and other board games.
I like playing them too, for fun, and for purposes of experimentation.


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
And I think it's clear that we could express it in terms of this rule, if we
had a way to apply it repeatedly:

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
**If none of that terminology sounds familiar, don't worry about it. Let's
get back to chess.**

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


## The algebra of chess moves

Okay, we have an "algebra of chessboards", but at the end there, we also
introduced a way to describe chess *moves*, for instance:

    ♙ + ur♟ -> . + ur♙

Now, let's say for a moment that we're not (yet) only interested in describing
*valid* chess moves.
We want a way to describe *any* chess move, even one where you teleport your
king to the other side of the board, remove your opponent's queen, and add
two knights to your side, all in one move.
Crazy, you say?!?! Well, all I say to you is:

    ♔ + uuuuuu. + uurr♛ -> . + uuuuuu♔ + uurr. + lll♘ + rrr♘

It's not a *legal* move, but it's definitely a, um, move.
And we can describe it!

Now, can we describe a series of moves?
For example, moving a king one square up, then one square right?

    Moving a king one square up:

    ♔ -> . + u♔

    Moving a king one square right:

    ♔ -> . + r♔

    Moving a king one square up, then one square right (all in one move):

    ♔ -> . + ur♔

I would like a way of saying that one move was made, and then another move
was made; and I would like a way of saying that such a series of moves is
equivalent to a single (possibly illegal!) move.

    (♔ -> . + u♔)(♔ -> . + r♔) = (♔ -> . + ur♔)

Make sense? So, when we write two moves next to each other, that represents
the move where we do those moves, one after another.
But... does that always make sense?.. what does the following sequence of
moves result in?

    (♔ -> . + u♔)(♖ -> . + u♖) = ???

We moved a king upwards, and then we moved a rook upwards.
So uhhh... I guess that one doesn't "simplify" into a single move?
Or at least, not a move we can write with a single `->`?

For that matter, let's go back to our example of moving the king up and
then to the right.
We wrote it as an equation, as if moving your king up, and then moving your
king right, was always the same as moving your king up-and-right.
But... that's only the case if you only have one king.
Which, in standard chess, you do.
But what about moving a pawn up, and then moving a pawn up? Does it have
to be the same pawn each time?

    (♙ -> . + u♙)(♙ -> . + u♙) = (♙ -> . + u. + uu♙)  ...???

If you are lost, that's probably because **this is not a good syntax for
visualizing the board.**
So don't feel lost, don't run away from me please, stay, yes stay with me,
here I'll give you a nice picture of a chessboard:

    .......
    ..♙.♙..

    Applying the move (♙ -> . + u♙) could give us *either* of:

    ..♙....        ....♙..
    ....♙..   or   ..♙....

Now, I've been jumping ahead like crazy here with this syntax and these
rules, so in case you're wondering -- I'm not *proving* anything here about
this syntax.
I'm actually coming up with the rules for it as I go along.
I have decided, just now, that I would like for the meaning of a move like
`♙ -> . + u♙` to be "find any one piece ♙, and replace it with `. + u♙`".

But a corollary of my decision is that this equation which I gave earlier
is *not* true, according to our algebra of moves:

    (♙ -> . + u♙)(♙ -> . + u♙) = (♙ -> . + u. + uu♙)

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
let's use e.g. "%♖" to mean "when POI is a rook", "%♙" to mean "when
POI is a pawn", etc:

    Move a rook up, and then move it up again:

    %♖: (% + u. -> . + u%){2}

Make sense?.. that's all a single move.
And this "with % as" syntax isn't special; it can be stuck inside more
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
            * The meaning is: no move, or the move which consists of
              doing nothing, leaving the board exactly as it was
        * f -> g (where f and g are board fragment patterns)
        * %p: M (where p is a chess piece and M is a move)
            * The meaning is: choose a specific piece on the board.
              It is now the POI (piece of interest).
              Now move like M.
        * MN (where M and N are moves)
            * Note that nil M = M = M nil, that is, "doing nothing and
              then doing M" is the same as simply doing M, and so is
              "doing M and then doing nothing".
            * We would like for (f -> g)(h -> i) to be equivalent to
              (f -> i) in some situations when the pattern h matches the
                board fragment g.
              I'm not fully clear on the specifics of this yet, so let's
              look at it separately... see Appendix A!
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

Don't worry, if it makes your eyes glaze over, you're free to gloss over it.
But the fact that I was able to write it down makes me more confident that
our algebra is self-consistent, and we're not just waving our hands around
saying crazy things.
For instance, I reckon we could likely implement this algebra in software...
hint hint...

By the way, I have snuck in some new concepts! Did you notice?

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
[Irreversible Chess](entries/2025/jul/irreversible_chess.md)!

We could also implement a software library which can parse it, and use it
to quickly play different chess variants!

That sounds fun. Maybe we'll do that and link to it here...


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

