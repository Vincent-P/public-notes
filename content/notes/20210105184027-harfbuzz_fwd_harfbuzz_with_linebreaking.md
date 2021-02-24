+++
title = "[HarfBuzz] Fwd: Harfbuzz with linebreaking"
draft = false
+++

link
: <https://lists.freedesktop.org/archives/harfbuzz/2016-June/005623.html>

tags
: [text rendering]({{< relref "20210105204547-text_rendering" >}})

> each word has at least
> one (often many) breakpoints, but only one of them gets used per
> line.

Right.

> And the only way to know which one to use is to shape.

Well, no. You shaped already; that was the first thing you did. As Adam
told you, the only way to know which breakpoint to **use** is to run a
justification algorithm, which you need to code. You're currently
thinking about a simple first-fit algorithm, which chops the glyphs into
lines once they get to be longer than the target line length; that's
fine, although you may find that a best-fit algorithm which performs
dynamic programming over all possible breakpoints gives you a neater
paragraph.

Now, shaping determines the glyph widths for you (which is the input to
your line breaking algorithm), but it is your code which is responsible
for finding the **possible** breakpoints in the text, at the language
level, and your code which is responsible for determining the **actual**
breakpoints at the shaped-glyph level.

Here we go then. If you want to use Harfbuzz to shape lines into
paragraphs, here is what you need to do:


## Perform the first stage of the bidi algorithm to organise the text {#perform-the-first-stage-of-the-bidi-algorithm-to-organise-the-text}

into same-direction runs. (Really, don't leave this bit out, and don't
think "I'll add RTL/complex script support later", because that never
works out well and because we already have enough typesetters that only
handle Latin.) ICU does this.


## Shape the paragraph, keeping note of the connection between the glyphs {#shape-the-paragraph-keeping-note-of-the-connection-between-the-glyphs}

and the text. Harfbuzz does this.


## Find the breakpoints in the text, using language analysis on the {#find-the-breakpoints-in-the-text-using-language-analysis-on-the}

characters. ICU does this.


## Create a data structure representing the runs of Harfbuzz output {#create-a-data-structure-representing-the-runs-of-harfbuzz-output}

between the breakpoints - TeX and SILE call these runs "nnodes" - and
the potential breakpoints themselves - "penalty nodes" (for breaking
inside a "word") and "glue nodes" (for whitespace between "words").
Assign widths to the nnodes by summing the widths of the shaped glyphs
inside them. You can put each glyph into its own nnode instead of
consolidating each run into an nnode if it's conceptually easier, but it
just slows your justification algorithm down.

Here's what my data structure looks like at this stage:

N<19.71pt>(Take)G<2.6pt>N<22.06pt>(these)G<2.6pt>N<15.37pt>(five)G<2.6pt>N<40.42pt>(sentences)G<2.6pt>N<25.17pt>(which)G<2.6pt>N<2.97pt>(I)G<2.6pt>N<19.95pt>(need)G<2.6pt>N<8.47pt>(to)G<2.6pt>N<23.24pt>(break)G<2.6pt>N<16.69pt>(into)G<2.6pt>N<4.58pt>(a)G<2.6pt>N<42.68pt>(paragraph)N<2.29pt>(.)

(Each nnode also contains a list of glyph IDs and widths.) Each of the
glue nodes are potential break points; these were obtained by checking
the Unicode line break status of each character. The space character
0x20 is breakable, so it gets turned into a glue node.


## Run your justification algorithm to determine which breakpoints should {#run-your-justification-algorithm-to-determine-which-breakpoints-should}

be used. Your code does this.


## If the algorithm does not produce a tight enough paragraph, break open {#if-the-algorithm-does-not-produce-a-tight-enough-paragraph-break-open}

the nnodes by hyphenating the text, reshaping them into new nnodes, and
putting a discretionary breakpoint in the middle.

Now it looks like this:

N<19.71pt>(Take)G<2.64pt>N<22.06pt>(these)G<2.64pt>N<15.37pt>(five)G<2.64pt>N<13.99pt>(sen)D(N<3.36pt>(-)||)N<26.43pt>(tences)G<2.64pt>N<25.17pt>(which)G<2.64pt>N<2.97pt>(I)G<2.64pt>N<19.95pt>(need)G<2.64pt>N<8.47pt>(to)G<2.64pt>N<23.24pt>(break)G<2.64pt>N<16.69pt>(into)G<2.64pt>N<4.58pt>(a)G<2.64pt>N<18.43pt>(para)D(N<3.36pt>(-)||)N<24.24pt>(graph)N<2.29pt>(.)


## Run your justification algorithm again on this new node list. {#run-your-justification-algorithm-again-on-this-new-node-list-dot}

On a 100pt column, my algorithm determined that the line breaks are at
position 10 and position 22 of the node list array.


## Organise your node list into a list of lines, based on the breakpoints {#organise-your-node-list-into-a-list-of-lines-based-on-the-breakpoints}

that were fired.

I split my node list at positions 10 and 22, so my lines are:

N<19.71pt>(Take)G<2.64pt>N<22.06pt>(these)G<2.64pt>N<15.37pt>(five)G<2.64pt>N<13.99pt>(sen)D(N<3.36pt>(-)||)N<26.43pt>(tences)G<2.6pt>

N<25.17pt>(which)G<2.6pt>N<2.97pt>(I)G<2.6pt>N<19.95pt>(need)G<2.6pt>N<8.47pt>(to)G<2.6pt>N<23.24pt>(break)G<2.6pt>N<16.69pt>(into)

N<4.58pt>(a)G<2.6pt>N<18.43pt>(para)D(N<3.36pt>(-)||)N<24.24pt>(graph)N<2.29pt>(.)


## For each line in the paragraph, apply the second part of the bidi {#for-each-line-in-the-paragraph-apply-the-second-part-of-the-bidi}

algorithm (ICU does this) and reshape where necessary. This splits and
recombines ligatures correctly. (I promise; we have a test case to prove
this.)

You only need to determine line breaks once, and you only need to
reshape once per line maximum. I'm not going to argue about whether it
works or not, because you can check out the code and the test suite for
yourself: <https://github.com/simoncozens/sile>

> In fact I don’t see any other way to do it

You need to put aside the idea that there is a connection between
shaping and determining which breakpoints to use. There isn't one, and
this is the mental block which is stopping you from seeing solutions to
your problem.
