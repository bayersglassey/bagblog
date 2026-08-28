# Just computers, after all (UNFINISHED)

The AI craze has been largely bad for my mental health.
The amount of hype, overselling, and disinformation is staggering.
Sometimes, I try to think about it as if it wasn't literally raging outside,
destroying the job market and people's minds; I try to think of it as just
another interesting little technology, with a little niche somewhere.

What is this little niche "AI" thing?.. it's mostly just computers.
I used to like those.
Here's some thoughts.


## List of initial ideas

* A way of compressing natural language into a more computer-friendly
  representation, e.g. a stack-based language, or a predicate-based
  language like Prolog
    * Part of the intuition here is that the way LLMs currently work
      is inherently inefficient, in that the same "program" is run for
      each "forward step" (i.e. when generating each output token), yet
      many output tokens have basically no value, e.g. they're just
      little connective grammar words (to say nothing of the emojis).
* Natural language interface for Wikipedia (downloaded locally)
  ...looks like enwiki-20260501-pages-articles-multistream.xml.bz2
  ...on this page: https://dumps.wikimedia.org/enwiki/20260501/
* Natural language interface for code generation
* Understand gradient descent, and then look for a discrete equivalent
  ...e.g. look for some concept of "discrete derivative", or a calculus
  of derivatives
    * Gradient descent is an "optimization" technique... there is also
      discrete optimization, look into that:
      https://en.wikipedia.org/wiki/Discrete_optimization
      ...can we do optimization with like... data structures?..
* Mechanistic interpretability has found things like, transformer arch
  is running multiple "programs" in parallel for each forward step,
  but some of them get dampened by others.
  And some of those programs are like "lookups", some are "copiers",
  etc.
  Somehow, this system of linear algebra approximates some kind of
  other program... what if we try to write that program ourselves?
  And we try to make it produce good output for more and more examples:
  that is, the "training" process is just us, looking at more and more
  examples, and growing this spaghetti code thing.



Currently, chatbots are used as "everything machines".
You can ask them factual questions, or to generate poetry, or to
generate code, or use tools, or have a "conversation" where they are
to remember facts you provide, and give advice or opinions.
A single LLM might provide all of that functionality at the same time;
I would argue that it's essentially running many programs in parallel,
then choosing the output of one program when deciding on the next token
to output.
But how much functionality is shared between those parallel programs?..
can we not make them explicitly separate programs, and then have some
logic to choose between them?..

Let's take the ability of LLMs to apparently process and generate
grammatically correct natural language.
This seems to me to be the major "program" learned by GPT-2.
That is, GPT-2 isn't very good at math or reporting factual information,
but it *is* good at generating plausible-looking natural language text.

It does have a limited ability of returning factual information (sometimes):

    # Given this function:
    def complete(text, n=5, m=10):
        for i, resp in enumerate(generator(text, max_new_tokens=n, num_return_sequences=m)): print(f"ANSWER {i+1}: " + resp['generated_text'])

    In [59]: complete("Chinese city of")
    ANSWER 1: Chinese city of Guangdong, China
    ANSWER 2: Chinese city of Mysore has witnessed
    ANSWER 3: Chinese city of New Delhi, India Reuters
    ANSWER 4: Chinese city of San Francisco has been hit
    ANSWER 5: Chinese city of Kolkata, Pakistan
    ANSWER 6: Chinese city of Xinjiang. The official
    ANSWER 7: Chinese city of Nanjing, a Chinese
    ANSWER 8: Chinese city of Guadalajara in
    ANSWER 9: Chinese city of Zarahemar will
    ANSWER 10: Chinese city of Xinjiang, and a

    In [60]: complete("Canadian city of")
    ANSWER 1: Canadian city of Ottawa. Ottawa police say
    ANSWER 2: Canadian city of Toronto. A
    ANSWER 3: Canadian city of Toronto, Canada, has
    ANSWER 4: Canadian city of Detroit is in the midst
    ANSWER 5: Canadian city of Birmingham, Alabama, a
    ANSWER 6: Canadian city of St. Paul.
    ANSWER 7: Canadian city of Winnipeg. "
    ANSWER 8: Canadian city of Vancouver, Canada
    ANSWER 9: Canadian city of New York has banned the
    ANSWER 10: Canadian city of St. Petersburg, which

...but it's terrible at math:

    In [66]: complete("One plus one is")
    ANSWER 1: One plus one is a lot of stuff you
    ANSWER 2: One plus one is the ability to make use
    ANSWER 3: One plus one is that the main feature of
    ANSWER 4: One plus one is that this means that for
    ANSWER 5: One plus one is that you get to see
    ANSWER 6: One plus one is there's the possibility of
    ANSWER 7: One plus one is that the new camera lens
    ANSWER 8: One plus one is that you can't use
    ANSWER 9: One plus one is the fact that you can
    ANSWER 10: One plus one is the "don't ask

    In [67]: complete("1 + 1 = ")
    ANSWER 1: 1 + 1 = アップレイ
    ANSWER 2: 1 + 1 =  1, 2,
    ANSWER 3: 1 + 1 = 𝔯[1
    ANSWER 4: 1 + 1 = ??????
    ANSWER 5: 1 + 1 = 0000000000000000000000000000000000000000000000000000000000000000
    ANSWER 6: 1 + 1 = 【W+R+
    ANSWER 7: 1 + 1 = _________ __________________
    ANSWER 8: 1 + 1 = 𝑖 [ 0
    ANSWER 9: 1 + 1 =  + 1 , +
    ANSWER 10: 1 + 1 = ???? - ???? -

...but it knows how to make comma-separated lists:

    In [79]: complete("Apple, orange")
    ANSWER 1: Apple, orange, red, blue,
    ANSWER 2: Apple, orange, purple, and blue
    ANSWER 3: Apple, orange and red. I've
    ANSWER 4: Apple, orange, blue, and white
    ANSWER 5: Apple, orange, green, brown,
    ANSWER 6: Apple, orange and blue on the right
    ANSWER 7: Apple, orange and gold, and more
    ANSWER 8: Apple, orange and red (not orange
    ANSWER 9: Apple, orange and yellow light green light
    ANSWER 10: Apple, orange, blue, and yellow

...and it knows how to recognize certain grammatical constructs:

    In [80]: complete("The person whose")
    ANSWER 1: The person whose name is not listed in
    ANSWER 2: The person whose name you may not know
    ANSWER 3: The person whose opinion is the greatest should
    ANSWER 4: The person whose name is not found is
    ANSWER 5: The person whose name is in the title
    ANSWER 6: The person whose job is to make sure
    ANSWER 7: The person whose last name has been withheld
    ANSWER 8: The person whose name I have given you
    ANSWER 9: The person whose name you are referring to
    ANSWER 10: The person whose name is on the ballot

    In [81]: complete("The cat whose")
    ANSWER 1: The cat whose name I have no idea
    ANSWER 2: The cat whose name was given to him
    ANSWER 3: The cat whose life is in danger on
    ANSWER 4: The cat whose head I found was a
    ANSWER 5: The cat whose name has been associated with
    ANSWER 6: The cat whose only teeth are his own
    ANSWER 7: The cat whose head was cut off by
    ANSWER 8: The cat whose name is spelled out on
    ANSWER 9: The cat whose name had to be used
    ANSWER 10: The cat whose name I would have given

    In [82]: complete("The restaurant whose")
    ANSWER 1: The restaurant whose name is also owned by
    ANSWER 2: The restaurant whose name appears on most menus
    ANSWER 3: The restaurant whose owners are "The Che
    ANSWER 4: The restaurant whose owners are now in jail
    ANSWER 5: The restaurant whose name is now synonymous with
    ANSWER 6: The restaurant whose name appears on the front
    ANSWER 7: The restaurant whose patrons have been making their
    ANSWER 8: The restaurant whose owners said they wanted to
    ANSWER 9: The restaurant whose owner said he was trying
    ANSWER 10: The restaurant whose owner has been named as

Okay. What are some LLM use cases for which we could write little "programs"?..
First of all, different programs pay attention to different "scales" of the context.
For instance, think of parts-of-speech: some programs recognize that previous token
was an adjective, so next token should be a noun; others recognize that previous
tokens formed a comma-separated list, so next token should be a list item, comma,
the word "and", etc.

Those are just programs for generating grammatically correct text, though.
Separately, there must be programs for "reasoning", especially for in-context
reasoning.
GPT-2 has almost no ability for in-context reasoning... the best I could do was:

    # Given this:
    complete("\"Garble\" is a colour. Some colours:")

    # Often I would get lists of real colours:
    "Garble" is a colour. Some colours: blue, red, green, blue, yellow.

    # Sometimes I would get a re-statement of the "Garble" definition:
    "Garble" is a colour. Some colours: "Garble" is a colour.

    # Sometimes I would get a different fake colour definition.
    # Often this included repetition of the pattern "X is a colour. Some colours: ..."
    "Garble" is a colour. Some colours: "Faux" is a colour. Some colours
    "Garble" is a colour. Some colours: "Grape" is a colour. Some colours
    "Garble" is a colour. Some colours: "Tiered" and "Red" are non-distant colours.
    "Garble" is a colour. Some colours: The blue "Garble" is a colour. Some colours: The blue "Garble" is

    # Sometimes "garble" would show up in a later sentence:
    "Garble" is a colour. Some colours: black, red or grey. The name can be abbreviated as garble, but sometimes it is

The ability to repeat stuff, sometimes with tweaks, is interesting:

    In [140]: complete("I'm cool! I'm fresh! I'm nice! I'm here!", 20)
    ANSWER 1: I'm cool! I'm fresh! I'm nice! I'm here! There's nothing more to this place!"

    On his way, Trump said he had a "
    ANSWER 2: I'm cool! I'm fresh! I'm nice! I'm here! I'm just outta here!"

    "Hey, that's good. You're just out
    ANSWER 3: I'm cool! I'm fresh! I'm nice! I'm here! I'm the hottest!"

    And the next morning, she was in Los Angeles, in a
    ANSWER 4: I'm cool! I'm fresh! I'm nice! I'm here!

    No, I'm not.

    I'm not in this place.

    I
    ANSWER 5: I'm cool! I'm fresh! I'm nice! I'm here! I'm here!" she yelled.

    Her husband, who had been on the phone with her
    ANSWER 6: I'm cool! I'm fresh! I'm nice! I'm here! I'm here to make you happy! Make me happy! I'm here to make you happy!
    ANSWER 7: I'm cool! I'm fresh! I'm nice! I'm here! I'm good! I'm all right! I'm fine! I'm not really that bad.
    ANSWER 8: I'm cool! I'm fresh! I'm nice! I'm here! I'm here. I'm here. I'm here! I'm here! I'm here.
    ANSWER 9: I'm cool! I'm fresh! I'm nice! I'm here!


    So what's your go-to option for a "good" time?


    I
    ANSWER 10: I'm cool! I'm fresh! I'm nice! I'm here! I'm sooo good! I'm sooo good! I'm sooo good! I'm


    In [151]: complete("I made a pie.")
    ANSWER 1: I made a pie. She had to be my
    ANSWER 2: I made a pie. (And a cheesecake
    ANSWER 3: I made a pie. I'm a very big
    ANSWER 4: I made a pie. Oh, and I made
    ANSWER 5: I made a pie. (When I was younger
    ANSWER 6: I made a pie. The recipe I made was
    ANSWER 7: I made a pie. I made the
    ANSWER 8: I made a pie. I made a pie without
    ANSWER 9: I made a pie. I made it. I
    ANSWER 10: I made a pie. I was gonna make it

    In [153]: complete("I made a pie. (")
    ANSWER 1: I made a pie. (I think it was a
    ANSWER 2: I made a pie. (1) A baking sheet
    ANSWER 3: I made a pie. (No, I don't
    ANSWER 4: I made a pie. (It had been made in
    ANSWER 5: I made a pie. (I'm sorry, I
    ANSWER 6: I made a pie. (I'm proud of that
    ANSWER 7: I made a pie. (I have a lot of
    ANSWER 8: I made a pie. (It was a pie with
    ANSWER 9: I made a pie. (I'm sorry, they
    ANSWER 10: I made a pie. (Piece of pie)

    In [156]: complete("I made a pie. Not")
    ANSWER 1: I made a pie. Not on purpose, not because
    ANSWER 2: I made a pie. Not my name!
    ANSWER 3: I made a pie. Not a pie. A pie
    ANSWER 4: I made a pie. Not only did I roast the
    ANSWER 5: I made a pie. Not a crust though. We
    ANSWER 6: I made a pie. Not a pie, but a
    ANSWER 7: I made a pie. Not a pie, but a
    ANSWER 8: I made a pie. Not from a bag of dough
    ANSWER 9: I made a pie. Not one of my pies."
    ANSWER 10: I made a pie. Not only did I make a

It has very limited ability to understand text which has been transformed
in various ways, i.e. spelling & formatting matter:

    In [175]: complete("I MADE A PIE.")
    ANSWER 1: I MADE A PIE. I MADE A P
    ANSWER 2: I MADE A PIE.

    "Hey,
    ANSWER 3: I MADE A PIE. I AM THE ANCI
    ANSWER 4: I MADE A PIE.

    I told you
    ANSWER 5: I MADE A PIE.

    I MADE
    ANSWER 6: I MADE A PIE.

    DALLAS
    ANSWER 7: I MADE A PIE. I MADE A P
    ANSWER 8: I MADE A PIE.

    It had been
    ANSWER 9: I MADE A PIE. I AM SO STUP
    ANSWER 10: I MADE A PIE.

    Well, who

    In [178]: complete("I/made/a/pie")
    ANSWER 1: I/made/a/pie/the-pie/
    ANSWER 2: I/made/a/pie-in-the-
    ANSWER 3: I/made/a/pie/little_pie_
    ANSWER 4: I/made/a/pie/is/good/
    ANSWER 5: I/made/a/pie/pie/pie/
    ANSWER 6: I/made/a/pie/piecicle/
    ANSWER 7: I/made/a/pie/ My sister
    ANSWER 8: I/made/a/pie/bakery.png
    ANSWER 9: I/made/a/pie,butch/orange
    ANSWER 10: I/made/a/pie" "I

...so, GPT-2 looks like it has programs for:
* Repeating earlier stuff
* Completing various grammatical structures
* Doing some basic lookups (for "related words", which we can attempt to
  use to "look up facts" like the capital city of a country)

...but definitely limited or no programs for:
* Doing transformations before/after other programs (e.g. it can't handle
  uppercased text)
* Math

So, let's try to write some programs for:
* repetition
* structure
* built-in lookups ("related words", "facts" etc)
* text transformations
  e.g. if we detect all-caps, we can lower before calling other programs,
  then re-apply all-caps before returning.
  Later on, this could be used for "personality" etc: "you are a senior
  programmer" etc
* math
* tools

And let's not limit our programs to being "predict next token".
Let's write programs with memory, which can produce lots of text all at once.
So for instance, if a program decides to produce a list of things, another
program can't interrupt that. Rather, the program can call upon other programs
to generate list entries.
However, sometimes we do want to run multiple programs and choose the best
result among them.
We just don't want to be doing that *all the time*.

Let's limit ourselves to a particular "vocabulary".
So instead of training on the entirety of Wikipedia, let's focus on...
programming! So that we can have a natural-language interface to coding.

Some programs can simply detect things, other programs can output things.
We want programs to return probabilities rather than booleans.
Ideally, we compare the results of "detect" programs first, then choose
which "output" programs to run.

Programs can be on various scales, from low to high.
We can have a program which determines which scale of program to run next.
E.g. if previous character was ".", there's a good chance we should be
starting a fresh sentence.

Are we trying to make a chatbot, or a text-completer?
Let's start with a text-completer, so we can compare ourselves to GPT-2.
Let's start with sentence structure.

Some ideas for programs:
* Are we starting a new sentence?
  e.g. following a ".", "(", ";", ":", etc
* How long is the sentence we're currently in?
* Are we following a verb? Adjective? Noun?
* Are we partway through a hyphenated word?

Can we do some training?..
So for instance, can we process Wikipedia and find all nouns, verbs, etc?..
And do some "related words" processing?..
We could use NLTK instead, of course.
Hmmmmmmmmmmmmmmm let's try to extract sentences.
The extraction process should also output some statistics, so we can tell
e.g. how much text we *rejected* due to not looking enough like a sentence.

E.g. the Apple wikipedia entry:

    An apple is the round, edible fruit of an apple tree (Malus spp.).

    Fruit trees of the orchard or domestic apple (Malus domestica), the
    most widely grown in the genus, are cultivated worldwide.

    The tree originated in Central Asia, where its wild ancestor, Malus
    sieversii, is still found.

    Apples have been grown for thousands of years in Eurasia before they
    were introduced to North America by European colonists.

    Apples have cultural significance in many mythologies (including Norse
    and Greek) and religions (such as Christianity in Europe).

    Apples grown from seeds tend to be very different from those of their
    parents, and the resultant fruit frequently lacks desired characteristics.

    For commercial purposes, including botanical evaluation, apple cultivars
    are propagated by clonal grafting onto rootstocks.

    Apple trees grown without rootstocks tend to be larger and much slower
    to fruit after planting.

    Rootstocks are used to control the speed of growth and the size of the
    resulting tree, allowing for easier harvesting.

    There are more than 7,500 cultivars of apples.

    Different cultivars are bred for various tastes and uses, including
    cooking, eating raw, and cider or apple juice production.

    Trees and fruit are prone to fungal, bacterial, and pest problems,
    which can be controlled by a number of organic and non-organic means.

    In 2010, the fruit's genome was sequenced as part of research on
    disease control and selective breeding in apple production.

Let's say we start with a built-in list of "grammatical" words: in, a, an,
the, of, on, and, or, not, by, etc.
And some basic stemming, like "-'s", "-ing", "-ed", "-es", "-s", "-er",
"-est", "-y", "-est", etc?..
And let's recognize numbers, too?.. parse "7,500" as 7500?.. later on, we
could try to enter/exit different "modes", like in France we parse "7,500"
as 7.5, etc.
Anyway, then one thing we can do is just record how many times a given
pair of words is found in a sentence together.
And then... can we build lookup tables, from words to common word-sets they
belong to, or something?..



The assumption in the current "AI" rat race is that more powerful single
models should be produced by expensive training processes and tons of data.
The results are not decomposable: if you want to add functionality, you
can't just mix it in, at best you can start from a base model and post-train
it, but the transformer architecture is fundamentally about packing as much
behaviour into a fixed amount of space (i.e. fixed number of params/weights)
as possible. So the training process produces spaghetti, basically by design.
Instead, what if we attempt to slowly, manually, write composable programs?

One issue with current LLMs' model weights is that they encode both data and
behaviour, mixed together.
If we could separate those, then it might be possible to reuse the same
"code" for e.g. the "producing grammatical structures" behaviour, while
separately being able to e.g. generate a list of known concepts.
That kind of "list of known concepts" is presumably related to the "concept
maps" people can extract from LLM layers, but currently I don't think they
are easily exported, modified, etc separately from the "logic" which makes
use of them.



How many "programs" can LLMs currently make use of at once?..
So e.g. if we ask an LLM to list the capital cities of Canada before 1980
ordered by size of province population while capitalizing every second
letter and also making it all rhyme, at some point those various programs
will start to step on each others toes... like, some of those programs
will be reusing the same weights as each other, and so they won't be able
to run simultaneously. Or something.
