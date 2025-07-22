
# Irreversible Chess

## Introduction

Let's say, for sake of argument, that we dislike that when playing chess,
it's possible for the board to be in the same position multiple times in
the same game.
For instance, both players could move a piece back and forth, resulting in
an infinite loop.
Of course, competitive chess has the "three-fold rule", which says that if
the same position occurs 3 times in one game, it's a draw.
However, let's say we would prefer, for aesthetic reasons, that the rules
should *naturally* prevent any position from ever reoccurring, without
having to explicitly (hamfistedly!) specify it.

Let us therefore invent a chess variant in which it is impossible for
positions to repeat themselves.
In other words, a chess variant in which the diagram of transitions
between positions has no cycles.
An acyclic chess variant!
Let's call it "Irreversible Chess".

We will represent chess pieces using Unicode.
Since this is a plain text file, and the text might be black on white, or
white on black, or some other combination of colours entirely, we will call
the players not "white" and "black", but "filled" and "unfilled":

    8|♜♞♝♚♛♝♞♜ <- The "filled" pieces
    7|♟♟♟♟♟♟♟♟
    6|........
    5|........
    4|........
    3|........
    2|♙♙♙♙♙♙♙♙
    1|♖♘♗♔♕♗♘♖ <- The "unfilled" pieces
     +--------
      abcdefgh

We will refer to rows of the board as "ranks", and columns as "files", per
standard chess terminology; and per standard chess notation, we may refer
to squares of the board by a combination of letter and number, e.g. the
unfilled and filled kings begin the game on squares d1 and d8, respectively.

We may sometimes describe moves according to standard chess notation, e.g.
"♙d4 ♞d5" means a turn where unfilled player moves a pawn to d4, and filled
player moves their knight to d5.
An "x" means "takes", for instance "♞xc3" means "knight takes on c3".


## The basic variant

For our irreversible chess variant, we will begin with all the standard
rules of chess, but impose restrictions on the movements of the pieces,
blocking any which might be reversible.
We require that our variant be a strict subset of regular chess: that is,
every valid move in our variant must be a valid move in regular chess, but
not vice versa.

Let's begin by requiring that when any piece moves, it must end up further
"forward" than it was before - that is, further towards the other player's
side of the board.

Pawns are unaffected by this rule; the other pieces now move and take as
follows:

    King:

    XXX
    .♔.

    Knight:

    .X.X.
    X...X
    ..♘..

    Bishop:

    X.....X
    .X...X.
    ..X.X..
    ...♗...

    Rook:

    .X.
    .X.
    .X.
    .♖.

    Queen:

    X..X..X
    .X.X.X.
    ..XXX..
    ...♕...

For now, we disallow castling, since it requires horizontal movement.
(But we will reintroduce it later!..)

I submit to you that we have already arrived at an irreversible chess
variant!

This variant is already somewhat interesting: it becomes possible to
run one's king to safety, that is, running it past (or to the same rank
as) all opposing pieces, at which point it is free from check.
An interesting question might therefore be: in this chess variant, with
perfect play, should we always expect a draw by both players running
their kings past each other's pieces?..
Or, if solving that question is too difficult, we might ask what kinds
of strategies are effective in this variant.
For instance, is running one's king to safety the most effective strategy?
And if so, are there any effective counter-strategies?
Let's think of some...

Can we simply use our pawns? Let's say the unfilled king is on the run,
and we are the filled player.
If we have an unbroken pawn line, we can stop the king in his tracks:

    ♟♟♟♟♟♟♟♟
    ........
    ....♔...

In fact, we can give checkmate:

    ♟♟♟♟♟.♟♟
    .....♟..
    ....♔...

Ah ha! In one sense, it's much easier to give checkmate in this this
variant, because the king can only run towards you.

An interesting situation is this, where both kings are on the run, and
meet in the middle, blocking each other from further progress:

    ....♚...
    ........
    ....♔...

In such a situation, running the kings to safety becomes impossible.
Indeed, both kings are now completely stuck!.. and so the question
becomes whether either of the players can achieve checkmate.

In fact, one interesting question might be which squares of the board
each player is able to "attack" (i.e. take on).
Or, to ask the reverse question, which squares of the board are "safe"
for each player?
Clearly, neither player can "attack" their own home rank, since pieces
must always move forwards.
But let's consider more generally, for each piece, which squares it is
able to attack:

    Rook:

    X.......
    X.......
    X.......
    X.......
    X.......
    X.......
    X.......
    ♖.......

    Knight:

    XXXXXXXX
    XXXXXXXX
    XXXXXXXX
    XXXXXXX.
    ..X.X..X
    X.X..X..
    ...X....
    .♘......

    Bishop:

    .X.X.X.X
    X.X.X.X.
    .X.X.X.X
    X.X.X.X.
    .X.X.X..
    X.X.X...
    .X.X....
    ♖♘♗♔♕♗♘♖

    King:

    XXXXXXXX
    XXXXXXXX
    XXXXXXXX
    XXXXXXXX
    XXXXXXX.
    .XXXXX..
    ..XXX...
    ♖♘♗♔♕♗♘♖

    Queen:

    XXXXXXXX
    XXXXXXXX
    XXXXXXXX
    XXXXXXXX
    .XXXXXXX
    ..XXXXX.
    ...XXX..
    ♖♘♗♔♕♗♘♖

Clearly, the queen is the most powerful piece, as always...
The rook appears to be fairly weak, although interestingly, without it
the sides of the board would be left fairly unguarded, especially near
the home rank!

So, perhaps a good strategy is to try and immobilize the enemy king, either
with pawns or one's own king, and then come along behind with one's queen
to deliver the checkmate?..

Let's consider the pawns.
The movement of pawns in our variant is unchanged; however, I believe we may
say that they have become more powerful, because it is very difficult to
attack a diagonal chain of pawns head-on.
So for instance, the queen here cannot take all the pawns by herself - at
most, she can take one safely, or she can take 3 if she is willing to put
herself in danger (and the pawns refuse to defend themselves, or their player
is busy elsewhere on the board):

    ..♟...♟.
    ...♟.♟..
    ....♟...
    ........
    ........
    ....♕...

The following situation is even worse: the queen is one rank closer, and now
she cannot take even a single pawn safely.
Remember, she can't move horizontally!.. in order to attack the sidemost pawns,
she will need to make a diagonal movement, but the pawns have covered every
square to which she can move:

    ..♟...♟.
    ...♟.♟..
    ....♟...
    ........
    ....♕...

So, perhaps we should expect high-level play in our chess variant to have an
emphasis on pawn tactics and strategy?..

Let's consider how to assign an approximate "value" to each piece on the board.
In regular chess, when e.g. deciding whether to trade two pieces during the
early or mid game, often a system of "relative values" of the pieces is used,
for instance:

    Pawn: 1
    Knight: 3
    Bishop: 3
    Rook: 5
    Queen: 9

...meaning that for instance a knight is worth 3 pawns, or a queen 3 knights,
etc.
In our variant, we have already seen that the rook is likely "worth" much less
then in regular chess.
But... does this system of assigning values to each piece even make sense in
our variant? It is typically used to decide whether to make a trade, or to
assign a "value" to a given board position as a whole.
But consider the following fragment of a position:

    ..♔.
    .♛..

The filled queen is *past* the unfilled king, and can therefore never be used
to give check.
In fact, the queen is no longer able to take or block the king, *or* any piece
which can take or block the king, *or* any piece which can take or block any
piece which can take or block the king, *or*... etc.

The queen's value in this case should therefore be very much diminished!..
Should her value be zero?.. not quite: perhaps a position will arise later
where this queen is the only piece with a valid move, or perhaps there is an
enemy piece behind the king which the queen can take or block, for example:

    ....♚.
    ......
    ......
    ..♔...
    .♛....
    ......
    ...♖..

So this is very interesting: we might say that a piece's value drops once
it has reached the same rank as the enemy king - or rather, once there is
no longer any overlap in the squares reachable by a given piece and the
enemy king.
For instance, for the king and queen, the reachable squares form "cones"
in front of them, and if they are outside of each other's cones, then they
can never come together in check:

    ...♛.\.../.
    ../.\.\./..
    ./...\.♔...

It is left as an excercise to the reader to determine how best to quickly
determine, for other pieces, how to tell at a glance whether their is any
overlap in the squares reachable by that piece and an enemy king.

Let's consider the concepts from regular chess of opening, mid, and late game.
Do they still apply?..
Certainly, one could memorize opening sequences for our chess variant.
It seems to me that, in general, "good" openings for regular chess are in
no way guaranteed to be "good" in the variant.
For instance, often a position in regular chess is good because it threatens
certain moves; but many moves which are "safe" in regular chess are no longer
so in the variant, because pieces can no longer retreat.
That is, once a piece is committed to an attack, it can generally no longer
be recalled to safety.

The late game, in regular chess, is often defined as beginning once a certain
number (or combined value) of pieces have been removed from the board.
But in our variant, I suspect that in many games, most pieces will not be
taken, but rather "abandoned" once they are passed by the enemy king.

How about some other tenets of regular chess strategy?.. for instance, in
regular chess, the center of the board is often considered important: either
having one's pieces there, or having "control" of it, i.e. having one's pieces
"pointed at it".
In our variant, having one's pieces *in* the center of the board is risky in
that it requires having one's pieces further forward, which reduces one's
control of the *sides* of the board, potentially allowing the enemy king
to sneak there.

Well, let's stop there for now. We have come up with, I would argue, an
interesting chess variant - perhaps even one worth playing!
Let's now look at removing some of the restrictions of our variant - always
making sure we can guarantee that the game remains irreversible!


## Adding back some horizontal and backwards movement

It seems unfortunate that, in our variant, the Rook can no longer move
horizontally, and will therefore be stuck for ever on its starting file.
More generally, while the idea of running one's king past the enemy
pieces to safety is interesting, we might ask whether we could add back
a certain amount of horizontal and/or backwards movement, to bring back
some of the "fighting spirit" of regular chess.

Of course, we must be careful, if we allow horizontal or backwards
movements, to ensure that they are irreversible!..

### Castling

Castling allows horizontal movement of the king and rooks, and is
irreversible even in regular chess!

Before castling, the king and rooks look like this:

    X......X
    X......X
    ♖..♔...♖

After castling, they are in one of these positions:

    After castling king-side:

    ..X....X
    ..X....X
    .♔♖....♖

    After castling queen-side:

    X...X...
    X...X...
    ♖...♖♔..

We have therefore given each player a one-time possiblity of changing the
"lines of power" which are "shot out" from their rooks.

Even more so than in regular chess, it becomes extremely important not
to castle too early; and in fact not to move one's pieces too far away
from either side of the board, in case the enemy king happens to castle
there.
Otherwise, one can easily end up with some of one's pieces unable to
ever put the enemy king in check.
For instance, in the following example, the unfilled player has moved
their bishops and queens to the left side of the board:

    ♜♞♝.♜♚..
    ♟♟♟.♝♟.♟
    ..♛.♟♞♟.
    ...♟....
    .♙.♙....
    ♗.♕♗♙...
    ♙.♙..♙♙♙
    ♖♘.♔..♘♖

The filled king should therefore have an easy time of running down the
right side of the board.
It's almost as if the filled king can ignore everything on the left side
of this line:

    ♜♞♝.♜ \ ♚..
    ♟♟♟.♝♟ \ .♟
    ..♛.♟♞♟ ) .
    ...♟.. / ..
    .♙.♙. / ...
    ♗.♕♗ / ♙...
    ♙.♙ / ..♙♙♙
    ♖♘ / .♔..♘♖

...except of course that the unfilled knight in the bottom-right can still
pass over onto the right side of that line, and the unfilled king might
run to the left side of the line, in which case the unfilled player will
need to worry about whether to attempt to give check.

Let's consider the board to the right of that line... taken in isolation,
can we show that either player can force a win or a draw?..

       ♚..
        .♟
         .
        ..
       ...
      ♙...
     ..♙♙♙
    .♔..♘♖

We're not really considering here whether either player is allowed to spend
turns on the left side of the board (i.e. the side not shown here), just
whether there is a clear strategy to be found on the right side of the board
in isolation.

It seems clear to me that the unfilled pawn line can prevent the filled king
from running past.
That is, the unfilled pawns can be moved one at a time in such a way that
there are never any safe squares through which the king could pass them.
So for instance, unfilled player could try to press for this position:

       ♚..
        .♟
         .
        ♙♙
       ♙..
      ♙...
     .....
    .♔..♘♖

What about the filled king?.. can he at least make a safe space for himself
and hide there for ever (assuming that he has valid moves to make on the left
side of the board)?..
By themselves, the unfilled pawns and rook can't do anything to the filled
pawn.
However, the unfilled knight and king could attack it.
Let's say we come to this position:

       ♚..
        .♟
         .
        ♘♙
       ..♔
      ♙...
     ..♙♙.
    .....♖

The filled pawn is under attack from unfilled knight.
If filled pawn moves forward, however, then the unfilled pieces can never
get through (aside from the knight).

Well, that's enough of that.
My takeaway from this is that running one's knight past the enemy pawn line
may in fact be quite difficult, unless one can punch a hole through.


### Allowing pieces to take horizontally and backwards

The central rule of our variant has been that pieces can only move forwards.
However, perhaps there are cases where a piece can move horizontally or
backwards in a way which is clearly irreversible... such as when a piece is
taken!
When a piece is taken off the board, we can clearly no longer return to any
previous position in that game, since the piece was present in all previous
positions.
(Pieces can come back on the board when a pawn reaches the opposite side, but
of course in that case the *pawn* is taken off the board, so irreversibility
is still preserved.)

So, one way to extend our variant while preserving irreversibility is to say
that pieces may always *take* exactly as they do in standard chess: it is only
when *moving without taking* that they must move forwards.

For instance, the rook in this diagram may take the enemy pawn, but may
not make any other horizontal movement:

    ..........
    ..........
    ..♖....♟..
    ..........

Now, unfortunately our rooks are still relatively weak compared to
regular chess, because we cannot easily double them up on the same file
(unless an enemy piece wanders into our base).
For instance, in the following situation, we might wish to double
our rooks up on the open "c" file:

    ........
    ♙♙.♙♙♙..
    ♖.....♙♙
    .......♖
    abcdefgh

And in fact, we can give our rooks this power if we allow them to
move horizontally, but only *towards each other*.
Each such movement decreases the distance between the rooks, and is
therefore irreversible.
Once the rooks are doubled, they can no longer move horizontally,
except of course to take an enemy piece - at which point they may
again move towards each other.

Can we come up with a similar rule, allowing the queen to move
horizontally in certain situations?.. for instance, what if the queen
is always allowed to move towards the king's current file - either
horizontally, or diagonally backwards?..
But no, this would allow the queen to move back and forth between the
following two squares (A and B):

    ......B.
    ........
    ...♔A...

In any case, allowing all pieces to *take* without the need of moving
forwards, and allowing each player's rooks to move horizontally towards
each other, may bring back some of the "fighting spirit" of regular chess.


## More analysis of strategy and theory in the basic variant

Let's return to the basic variant, that is, chess but where pieces must
always move forwards, even when taking.

### Mating

Under what circumstances is it possible to mate?

The fact that the king cannot move horizontally means that bishops have
an easier time of blocking his escape.
For instance, in the following example, the king can only move directly
forwards:

    ...♝...
    ..X.X..
    .X.♔.X.

This tells us that the filled queen may give checkmate in this position,
unless another unfilled piece can take her or interpose between her and
the king:

    ...♛...
    ..XXX..
    .X.♔.X.

So, perhaps when moving one's king forwards, it's a good idea to keep bishops
and/or the queen "pointed diagonally" at the squares just ahead of the king?..
Or more generally, to use one's far-ranging pieces to draw a corridor of safety
for one's king?.. something like this:

    .....|//
    .....//|
    ....//.|
    ...//|♔|
    ../♗.|.|
    .♗...♕.♖

Well, anyway - let's think about which other pieces can give checkmate...
Basically, we just need to cover the 3 squares in front of the king, plus
the king himself:

    XXX
    .♔.

Let's say we have the king trapped against the left or right side of the
board, or against one of the rooks at the side of the board:

    ♜..
    X..
    X..
    X♔.

I suppose we now just need one piece to hit the king on the diagonal, and
another to cover his escape forwards, which can be done e.g. by the bishops:

    ♜..♝♝
    |.//.
    |//..
    |♔...

...or a bishop and a knight:

    ♜.♞.♝
    |../.
    |X/..
    |♔...

...but notice that the knight can only achieve this from that particular
square; if it tries to cover the king's escape from the square in the
following diagram, it blocks the bishop from giving check:

    ♜...♝
    |..♞.
    |X...
    |♔...

It seems to me that it's likely much easier to give checkmate using pawns...
But I suppose it's difficult to do so when one's pawns are opposed by the
enemy pawns?..

What happens in the following position?.. can either player force a draw?..

    6..♚..
    5.♟♟♟.
    4.....
    3.....
    2.♙♙♙.
    1..♔..
     abcde

Let's say one player attempts to defend, and the other to attack.
Unfilled player goes first, and is defending:

    ♙c3 ♟d4

    6..♚..
    5.♟♟..
    4...♟.
    3..♙..
    2.♙.♙.
    1..♔..
     abcde

If ♙xd4, ♟xd4 (that is, the players trade pawns on d4), then we easily arrive
at a drawn position:

    ♙xd4 ♟xd4
    ♙d3 ♟b4
    ♙b3

    6..♚..
    5.....
    4.♟.♟.
    3.♙.♙.
    2.....
    1..♔..
     abcde


### Moving bastions

In regular chess, one may move one's king to the left or right side of
the board, and then crowd various other pieces around him.
In our variant, it's relatively difficult to crowd pieces directly around
the king, since it's necessary to move pieces forward in order to get
them to a file closer to the king.
But perhaps we can create "moving bastions", where the king moves forward
along with a group of protectors?..

Who can we send with the king?
Let's say we have not castled (either because we are playing the basic
variant where castling is disallowed, or because we are playing with
castling allowed but have simply not done so yet).
We can use a chain of pawns to provide our king with a sort of corridor
within which to travel:

    ........
    ......♙.
    .....♙/♙
    ....♙/..
    ♙♙♙♙/...
    ♖♘♗♔♕♗♘♖

...however, this will require having the king sneak along just inside the
wall of pawns, where he will be vulnerable to attack from queens, bishops,
and knights outside the wall.

Perhaps it's better to attempt a slightly wider corridor, allowing the king
to travel fully protected by the pawn wall (aside from knights), and the
king-side bishop to protect the diagonal just inside the wall?..

    ........
    .....♙♙.
    ....♙//♙
    ...♙//..
    ♙♙♙//...
    ♖♘♗♔♕♗♘♖

If this is a desirable formation, then perhaps "control of the center" is
indeed a useful concept in our variant, just as in regular chess.
That is, if either player can form a pawn chain which allows the king to
make a semi-protected run for the other side of the board...

Well, let's play a brief game against ourselves, where both sides attempt
to control the center in the usual way.

    ♙d4 ♟d5
    ♘f3 ♞f6
    ♗g5

    8♜♞♝♚♛♝.♜
    7♟♟♟.♟♟♟♟
    6.....♞..
    5...♟..♗.
    4...♙....
    3.....♘..
    2♙♙♙.♙♙♙♙
    1♖♘.♔♕♗.♖
     abcdefgh

The unfilled bishop threatens the knight; unlike in regular chess, neither
of them can retreat to safety.
Perhaps it's best for filled knight to move forwards, under protection of
the pawn on d5?..

    ... ♞e4

    8♜♞♝♚♛♝.♜
    7♟♟♟.♟♟♟♟
    6........
    5...♟..♗.
    4...♙♞...
    3.....♘..
    2♙♙♙.♙♙♙♙
    1♖♘.♔♕♗.♖
     abcdefgh

Interesting - the filled knight is now threatening f2, forking the king
and rook. In regular chess, it might be possible to shuffle the king and/or
rook horizontally to escape the threat, but here that is impossible.
The rook could move forwards to escape the threat; is that useful?.. in
regular chess, moving one's rooks or queen early is generally a bad idea,
because it slows development, and allows the opponent to potentially chase
them around the middle of the board.
However, chasing around the middle of the board is less possible here, since
once an attacker has "missed" their target, they have also passed it by, and
cannot "turn back" to chase it again.
So, perhaps it makes sense to begin pushing one's rook-pawn forward, with
the rook following behind as needed to avoid attack from bishops and queens?..

I'll stop there. It's not my goal to give a rigorous analysis of this chess
variant, only to sketch some of its interesting properties...
