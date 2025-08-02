# GEOM2018 & SPIDER GAME

I've been making games since I was a kid, originally in QBASIC on DOS,
and later in C on Linux.

In university we didn't have a CS department but we just barely had a
math department, so I did that.
I was terrible at university, but great at obsessively studying random
stuff on my own time.
Among other things, I got into algebraic geometry, and did a lot of
"research" (sketching in notebooks) on tilings of the plane using squares
and triangles.

![sketchbook](/assets/geom2018/IMG_1613.png)

Ummm, I recommend this book? Your mileage may vary:
[Tilings and Patterns, by Grünbaum and Shephard](https://archive.org/details/isbn_0716711931/mode/2up)

Eventually I thought to myself "what if you had like, a screen, right?..
but where the pixels were squares and triangles".
And so I wrote various demos to that effect.

![screenshot](/assets/geom2018/screen4.png)

Unrelatedly, over the years I occasionally sketched out ideas for a game
taking place on a grid of triangles, where your character's movement uses
a finite state machine.
(You can also say "your character's movement is like the original Prince
of Persia games, or Another World / Out of This World, or Blackthorne, etc".)

![sketchbook](/assets/geom2018/IMG_1619.png)

Eventually, the squares-and-triangles geometry stuff and the
triangular-grid-game idea came together into a game demo.
And the main character looks like a spider robot thing, because it's super
hard to draw anything when your "pixels" are squares and triangles.
So in casual conversation the demo always ended up being called "the spider
game", and the name has become official.

![screenshot](/assets/geom2018/start_0.gif)

![screenshot](/assets/geom2018/big_0.gif)

![screenshot](/assets/geom2018/jungle_1.gif)

It has a [little website](http://depths.bayersglassey.com/) where you can
[play it online](http://depths.bayersglassey.com/main.html)!

The source is [up on Github](https://github.com/bayersglassey/geom2018).

It's written in C + [SDL2](https://www.libsdl.org/) with basically no other
dependencies.

[Emscripten](https://emscripten.org/) is used to compile it for the browser.

Now, let us describe its internals.

NOTE: this was all initially a
[devlog post](https://forums.tigsource.com/index.php?topic=71325.msg1444398)
on the Indie Games Source forum.
I appreciate the site and the feedback I got there at the time!


## The graphics engine

The graphics are made out of tiny geometric shapes, each of which can be
exactly one colour, much like pixels.
However, they come in various shapes -- currently square, triangle, and
diamond -- and are positioned in a 4-dimensional space based on angles of
30 degrees, as opposed to pixels' 2d space based on angles of 90 degrees.
In the graphics engine, the tiny shapes are referred to as "prismels"
(because they're like pixels, but can be arbitrary... prisms?.. no,
polygons. Hmmmmm. It was many many years ago that I first started thinking
about all this, so I guess I have no idea why I went with the term "prismels").

Anyway, here is a motivating example... you play as this spider-looking thing:

![spider](/assets/geom2018/player_stand.png)

And here is a text representation of the "prismels" which make it up:

```
               -+---+-
              / |   | \
            +-  |   |  -+
            | \ |   | / |
           /   -+---+-   \
          |     |   |     |
          +-   / \ / \   -+---+-
          | \ |   |   | / |   | \
          |  -+---+---+-  |   |  -+
          | / |   |   | \ |   | /
          +-   \ / \ /   -+---+-
          |     |   |     |
           \   -+---+-   /
            | / |   | \ |
            +-  |   |  -+
              \ |   | /
               -+---+-
             -+       +-
            / |       | \
          +-  |       |  -+
          | \ |       | / |
         /   -+       +-   \
        |     |       |     |
        +-   /         \   -+
        | \ |           | / |
        |  -+           +-  |
        | /               \ |
        +-                 -+
```

They are all squares and triangles.
There is a third type of prismel, the diamond, which gets used less frequently
than the others.
Here are all 3 shown together:

```
   +---+     +
   |   |     |
   |   |    / \       -+---+
   |   |   |   |     /   /
   +---+   +---+   +---+-
```

Earlier I said they are positioned in a "4 dimensional" space.
What did that mean, though?
It means that the coordinates of these shapes can be expressed as 4-dimensional
vectors `(a, b, c, d)`.
Here are the 4 unit vectors I use:

```
         D  C

         + +
         | |   B
         |/ -+
         | /
         O---+ A

  O = (0, 0, 0, 0) <- The origin
  A = (1, 0, 0, 0)
  B = (0, 1, 0, 0)
  C = (0, 0, 1, 0)
  D = (0, 0, 0, 1)
```

In case that's not too clear, here are some examples of other vectors:

```
   2A = (2, 0, 0, 0):

      O---+---+


   -A = (-1, 0, 0, 0):

  +---O


   2B = (0, 2, 0, 0):

             -+
            /
         -+-
        /
      O-


   C - A = (-1, 0, 1, 0):

    +
    |
     \
      |
      O


   ...you can see why that should be C - A, if you put C and -A end-to-end:

     -A

    +---+
        |
       /  C
      |
      O
```

Why, you might ask, use these 4 dimensions instead of the usual X and Y?
The answer is that basic trigonometry will tell you that if the bottom-left
point of the following triangle is the origin `(0, 0)`, then the `(x, y)`
coordinates for its topmost point are, if I recall correctly,
`(1/2, 1 + sqrt(3))`:

```
      +
      |
     / \
    |   |
    +---+
```

...and long story short, if you want to represent such coordinates as
*integers* (which I do), you actually end up with 4 "dimensions" anyway!
The general form just becomes, if I recall correctly,
`((a + b * sqrt(3)) / 2, (c + d * sqrt(3)) / 2)`.
You see? Four variables: a, b, c, d.
But we've got gross `sqrt(3)` stuff everywhere, whereas the 4d space I
prefer to use has some nice properties when it comes to rotation, as you
will now see.

Now, one thing you might notice is that A, B, C, and D can be generated
by rotating A by multiples of 30 degrees.
If it helps you visualize this, here they are shown one after the other:

```
    A: 0 degrees:

         O---+


    B: 30 degrees:

            -+
           /
         O-


    C: 60 degrees:

           +
           |
          /
         |
         O


    D: 90 degrees:

         +
         |
         |
         |
         O
```

Let's say the function R rotates its argument by 30 degrees.
And note that `30 * 12 = 360` (that is, applying R twelve times gets you back
to where you started:
`R(R(R(R(R(R(R(R(R(R(R(R(x)))))))))))) = x for any x)`.
Then we have:

```
  R(A)      = B
  R(B)      = C
  R(C)      = D
  R(D)      = C - A   <- See the visualization of C - A earlier to see how it must be R(D)!
  R(C - A)  = D - B
  R(D - B)  = -A
  R(-A)     = -B
  R(-B)     = -C
  R(-C)     = -D
  R(-D)     = -C + A
  R(-C + A) = -D + B
  R(-D + B)  = A      <- 12 rotations got us back where we started
```

Also, we can do something cool from linear algebra: we can define vector
multiplication, and say that R is a vector instead of a function.
So for any vector x, `R * x = R(x)`.
Now we need to pick a unit vector, let's say that's A.
So A represents the identity transformation: `A * x = x`
Now since B is A rotated by 30 degrees, we have `A * R = B`, but since A
is the identity, that means `R = B`.
We can keep going with that:

```
  R^0  = A
  R^1  = B
  R^2  = C
  R^3  = D
  ...
  R^12 = A  <- 12 rotations of 60 degrees is a 360 degree rotation... i.e. no change
```

And by the way, `2A` represents a "stretch" of size 2.
That is, `2A * x` stretches x to twice its size.
So I can use vectors to stretch and rotate the graphics.
The graphics engine can also define "mappers" which stretch & rotate all
coordinates in an image, and replace each of its prismels with a shape
composed of many prismels -- and this whole transformation can be applied
repeatedly, basically generating fractals.
For instance, here is a transformation called "curvy" which... well, you'll see:

```
    "curvy":
        unit: 2 4 0 -2           <---- this is the vector it multiplies the coordinates by
        entries:
            : "vert" -> "vert"
            : "edge" -> "edge"
            : "sq"   -> "curvy_sq"     <---- this says it replaces prismel "sq" with shape "curvy_sq"
            : "tri"  -> "curvy_tri"
            : "dia"  -> "curvy_dia"
```

...this is what "curvy_sq", "curvy_tri", and "curvy_dia" look like:

![curvy shapes](/assets/geom2018/curvy.png)

...so what happens if we repeatedly apply the "curvy" transformation to some
other shape?..

Original:

![some shape](/assets/geom2018/dodeca_anim.png)

Transformed with "curvy" a couple of times:

![curvily transformed shape](/assets/geom2018/screen3.png)

Cool eh?!?!
Anyway, that's enough linear algebra and fractals for now.
Apologies?.. or you're welcome?.. but let's get back to games...

So how is all this used by the game engine?
In fact, I "wrote" most of the graphics by hand using 4d coordinates.
Let's see how the spider image is defined. Here it is again for reference:

![spider](/assets/geom2018/player_stand.png)

...and here is how it was defined using the game's graphics language.
Note, lines beginning with '#' are comments.
This is all taken more or less directly from the game's current code:

```
    "_head_sixth":
        #      _ +
        #    +    \
        #   / \  _ +
        # (+)- + _ |
        #          +
        prismels:
            : "tri" (0 0 0 0)  0 f eval: 1 + 8 + 1
            : "tri" (1 0 0 0) 11 f eval: 1 + 8 + 2
            : "sq"  (1 0 0 0)  1 f eval: 1 + 8 + 1

    "_head":
        shapes:
            : "_head_sixth" (0 0 0 0)  0 f
            : "_head_sixth" (0 0 0 0)  2 f
            : "_head_sixth" (0 0 0 0)  4 f
            : "_head_sixth" (0 0 0 0)  6 f
            : "_head_sixth" (0 0 0 0)  8 f
            : "_head_sixth" (0 0 0 0) 10 f

    "eye":
        prismels:
            : "tri" (0 0 0 0)  0 f eval: 1 + 8 + 4
            : "tri" (0 0 0 0)  2 f eval: 1 + 8 + 4
            : "tri" (0 0 0 0)  4 f eval: 1 + 8 + 4
            : "tri" (0 0 0 0)  6 f eval: 1 + 8 + 4
            : "tri" (0 0 0 0)  8 f eval: 1 + 8 + 4
            : "tri" (0 0 0 0) 10 f eval: 1 + 8 + 4

    "nose":
        prismels:
            : "sq"  (0 0 0 0) 0 f eval: 1 + 8 + 1
            : "tri" (1 0 0 0) 1 f eval: 1 + 8 + 2

    "head":
        shapes:
            : "_head" (0 0 0  0) 0 f
            : "eye"   (0 0 0  0) 0 f
            : "nose"  (1 1 0 -1) 0 f

    # Back leg
    "bleg":
        prismels:
            : "tri" (  0 -1  0  0) 11 f eval: 1 + 8 + 5
            : "sq"  (  0 -1 -1  0) 11 f eval: 1 + 8 + 3
            : "tri" (  0 -1 -1 -1)  1 f eval: 1 + 8 + 3

    # Front leg
    "fleg":
        shapes:
            # For historical reasons, "bleg" and "fleg" look exactly the same,
            # just "fleg" is usually rotated 180 degrees wherever its used...
            # However, they're separate in case we ever want to tweak one.
            : "bleg" (0 0 0 0) 0 f

    "stand":
        shapes:
            : "head"  ( 0  1  3  1)  0 f
            : "bleg"  ( 0  1  1  1)  0 f
            : "fleg"  ( 2  1  1  1)  6 t
```

...and just to be clear, that text is parsed by the game engine and used
to generate the spider image.

You can maybe see the 4d coordinates in there, e.g. `"head"  ( 0  1  3  1)  0 f`
is saying that the shape called "head" should be rendered at `B + 3C + D`,
and rotated by `R^0`, and not flipped vertically ("f" is for "false").
The "eval" bits are specifying colours, e.g. `eval: 1 + 8 + 2` is light green.
(It's a classic 4-bit palette, RGBI where the "I" is for "intensity", e.g. the
"light" in "light green".
See also: [Wikipedia article](https://en.wikipedia.org/wiki/List_of_monochrome_and_RGB_color_formats#4-bit_RGBI).
And the `+ 1` is because 0 is reserved for the "transparent colour".)

In any case, somehow after typing up enough of that stuff, we end up with a game which looks like this:

![screenshot](/assets/geom2018/start_0.gif)

You might argue this does not seem like a particularly user-friendly way
to populate a video game with graphics and animation.
And I would, to some extent agreel which is why I (recently, after already
typing up 90% of the graphics the other way) wrote a parser which can
understand "text representations" of prismels, like this:

```
    "_coin_beast_bleg_step1":
        hexpicture:
            ;;                    +
            ;;                   | |
            ;;                   |5|
            ;;                  +---+
            ;;                   | | |
            ;;                   |5|5|
            ;;                    +---+
            ;;                    |   |
            ;;                    |   |
            ;;                    |D  |
            ;;                    +---+
            ;;                    |   |
            ;;                    |   |
            ;;                    |F  |
            ;;                    +---*
```


...that shape is called "_coin_beast_bleg_step1", because it's the back leg
of a "coin beast" during frame 1 of its "stepping" animation, which looks
something like this:

![coin beast](/assets/geom2018/coin_beast.gif)

Okay, but there are some pieces missing here.
How do the animations work?.. also, as you may (or may not) be able to tell
from the gameplay clip above, the map's tiles actually form a triangular
grid -- the "prismels" and 4d coordinates and whatnot are only used for
rendering the sprites, not for the "physics".

First of all, the animations are done by specifying how many frames of
animation a "shape" (image) has, and then optionally specifying for which
frames its prismels or sub-shapes are visible.
For instance, here is the "crawl_step" shape, in which the spider takes a
step while crouching:

```
    "crawl_step":
        animation: cycle 3
        shapes:
            : "crawl_head" (-1  0  2  1)  1 f  0 (0 1)
            : "crawl_head" ( 0  0  2  1)  1 f  0 (1 1)
            : "crawl_head" ( 0  1  2  0)  1 f  0 (2 1)
            : "bleg"  (-1  1  1  1)  0 f
            : "fleg"  ( 2  1  1  2)  7 t  0 (0 1)
            : "fleg"  ( 3  1  1  2)  6 t  0 (1 1)
            : "fleg"  ( 3  1  1  1)  6 t  0 (2 1)
```

...so, `"crawl_head" (-1  0  2  1)  1 f  0 (0 1)` says to render the
"crawl_head" shape at some 4d coordinate, with a rotation of `R^1`, not
flipped (the "f" is for "false", remember), and finally "0 (0 1)" means
don't offset "crawl_head"'s animation by any frames (the "0"), and only
make it visible for 1 frame, starting on frame 0 (the "(0 1)").

Look, I enjoy writing parsers more than I enjoy writing GUIs, okay?
I'm not saying this was the best way to achieve all this.

Okay, now how is the map defined?
Well, the bottom-left part of the map in this screenshot:

![screenshot](/assets/geom2018/demo2.png)

...is defined like this:

```
                                                    + - + - +   + - +
                                                   /* * *\   \*/
                                          + - + - + - +   + - +
                                         /   /* * *\   \* * */
                    + - + - +   + - + - +   + - +   + - +   +
                   /   /             \           \* * * * */*
      + - + - + - +   +               + - + - +   +   + - + -
     /                 \                       \   \*/  */*\*
    +   + -             +                       +   +
   /   /               /                         \   \
  +       + - + - + - +                           +   +
   \     /                                       /   /
    + - +               .   + - +       + - + - +   +
                        S  /     \     /             \
      .      (+)- + - + - +       + - +     - + -     +
             /                   /     \             /*
            + - +               +       + - + - + - +
           /     \             /                  * * *
          +       + - + - + - +
           \
            +
           /
          +
         /
        +
      */
      .
```

...that file is called "start.fus", and another file, "worldmap.fus",
glues together such maps like this:

```
    submaps:
        :
            file: "data/maps/demo/start.fus"
            pos: (0 0)
            camera: (6 4)
            mapper: ("quadruple")
            palette: "data/maps/demo/pals/start.fus"
        :
            file: "data/maps/demo/start2.fus"
            pos: (7 11)
            camera: (5 4)
            mapper: ("quadruple")
            palette: "data/maps/demo/pals/start.fus"
            submaps:
                :
                    file: "data/maps/demo/start3.fus"
                    pos: (2 15)
                    camera: (5 -5)
                    mapper: ("triple")
                    tileset: "data/maps/demo/tilesets/shiny.fus"
                    submaps:

                        ...ETC...
```

Terrifying.

And in fact, there is one last major type of file (and associated
mini-language), which defines how a character moves and is controlled --
how its animations are glued together, how it responds to keypresses and
collisions, and even the logic used by its AI.

Here is a snippet from the file describing the spider's movement:

```
    collmsgs: "touch"
    on "crush": goto: dead

    collmap "stand":
        ;;   .   .
        ;;   *\*/*
        ;; . - + - .
        ;;   */*\*
        ;;  (.)  .

    collmap "crawl":
        ;;     .
        ;;     *
        ;;  (.)  .

    stand:
        rgraph: "stand"
        hitbox: collmap("stand")

        # Can't stand on nothing
        if:
            coll: any no
                ;;  (+)- +
        then:
            move: 1 0
            goto immediate: start_jump

        # Crawl
        if:
            key: isdown d
        then:
            goto delay: crawling


        # Forced jump
        if:
            key: isdown f
            coll: all no
                ;;       \*/*
                ;;        + -
                ;;       /*\*
                ;; ( )
        then:
            move: 1 0
            goto immediate: start_jump


        ...ETC...
```

...so we've got conditionals and "goto"s which send you to other animations,
and side-effects like "move: 1 0" which moves you 1 space to the right.
On the one hand, it's a pretty gross example of "not invented here" syndrome
(why not embed Lua or something?), but on the other hand, it lets us add
syntax and features which might be difficult to express in another language.

For instance, I can express hitboxes as some kind of literal.
Here is part of a conditional saying "if the following hitbox, at our
sprite's location, would not collide with the map".
(Note, the "( )" represents the sprite's location, which for the spider
is its back foot):

```
        coll: all no
            ;;       \*/*
            ;;        + -
            ;;       /*\*
            ;; ( )
```

For reference, a single triangular map tile, including its 3 points, 3 edges,
and 1 triangular face looks like this:

```
      +
     /*\
    + - +
```

...the same map tile, not including 2 of its points, 1 of its edges, or its face, looks like:

```
     .
    /
   + - .
```

The "." indicate positions where you could put an "+", that is, a point.
The "." are optional, they just make it easier to visualize the triangular grid.
