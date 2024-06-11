# Parsing your own text

+ [1. Parsing with HOPS](#1-parsing-with-hops)
+ [2. Parsing with UDPipe](#2-parsing-with-udpipe)
+ [3. Querying the results with GREW][#3-querying-the-results-with-grew]

In this tutorial, we're going to parse an historical text with the HOPS
parser, an extract from the *Grandes Chroniques*, a medieval French text.
The source data can be found in the [data](../data) folder.

You'll need a local copy of our Git repository for this script to work,
so start off with:
```console
cd ~
git clone https://github.com/ILR-Stuttgart/from-parser-to-query.git
```

## 1. Parsing with HOPS

If you've installed the HOPS Parser (see [day2-install.md](day2-install.md))
locally, we can parse this short text on more or less any standard computer.

### 1.1. Install an Old French model

We *could* use the modern French model that we downloaded before, but since
this is a medieval text, it's better to use the Old French model. (A list 
of French models for the HOPS parser can be found in the [parser's GitHub
repository](https://github.com/hopsparser/hopsparser)).

To install the model, run the following commands:
```console
wget https://zenodo.org/record/7708976/files/UD_Old_French-SRCMF-2.9-flaubert_base_cased.tar.xz
tar -xf UD_Old_French-SRCMF-2.9-flaubert_base_cased.tar.xz
```

### 1.2. Parse the text in CONLLU format

HOPS parser accepts both plain text and CONLLU input formats. To parse
CONLLU input, we'll use the `grchron-gold.conllu` file. You'll see that
this file contains annotation already, but this isn't necessary, and 
the syntactic and morphological information will in any case be re-written
by the parser.

To parse the text in CONLLU format, we first activate the Python 
virtual environment for the parser and then run it:
```console
cd ~
source hopsparser/bin/activate
hopsparser parse UD_Old_French-SRCMF-2.9-flaubert_base_cased from-parser-to-query/data/grchron-gold.conllu out.conllu
```
If you can't run HOPS, we've uploaded the output [in the data folder](../data/grchron-hops.conllu).

Bonus: since this input file contains gold annotation, we can get an initial
idea of how well our parser performed by running a simple diff on the files:
```console
diff from-parser-to-query/data/grchron-gold.conllu from-parser-to-query/data/grchron-hops.conllu
```

### 1.3. Parse the text in plain text format

We can also use the plain text file `grchon.txt` as input to the parser.
The file must be tokenized into words and sentences: words are separated by a space,
and sentences are on seperate lines.
In the current file, the tokenization first needs to be slightly modified,
splitting punctuation such as commas from the previous word and splitting
tokens ending with an apostrophe from the following word. We'll do this 
with `sed`:
```console
sed -E 's/([.,])/ \1/g' from-parser-to-query/data/grchron.txt > grchron.txt
sed -i "s/'/' /g" grchron.txt
```
(Note for Mac users: in the second command, replace `sed -i` with `sed -i ''`.)

Now, we can parse with the HOPS parser by adding the `--raw` argument to the
command line:
```console
hopsparser parse --raw UD_Old_French-SRCMF-2.9-flaubert_base_cased grchron.txt out.conllu
```

You'll see here that the result is a lot simpler because this parser and model
combination only generates a universal part-of-speech tag (UPOS) and the
dependency relations. It doesn't lemmatize, so there are no lemmas.

### 1.4. A quick note on training the HOPS Parser

If you have pre-annotated gold data, it's relatively simple to train
the HOPS parser and create your own language model. We're not going to cover
this in depth in this tutorial, but please refer to the Day 2 slides
from the workshop and feel free to contact us if you'd be interested
in learning more about this.

## 2. Parsing with UDPipe

The UDPipe parser has an online interface, so provided the language
you want to parse is supported and your file is not too big, it's a
great alternative to HOPS.
Unlike HOPS, it's able to tokenize plain text files, so you can upload
the [grchron.txt](../data/grchon.txt) file from our repository without
using the `sed` commands to finalize the tokenization.

1. Go to the UDPipe website [https://lindat.mff.cuni.cz/services/udpipe/](https://lindat.mff.cuni.cz/services/udpipe/).
1. Select the UD 2.12 model trained on the Old French corpus `old french-srcmf-ud-2.12-230717`.
1. Select the actions "Tag and Lemmatize", and "Parse".
1. Under "Advanced options", select
    + **UDPipe version**: UDPipe2
    + **Input**: Tokenize plain text
    + **Tokenizer**: Normalize spaces & Presegmented input
1. Select "Input File" > "Load File" and select `grchon.txt` from the `data` folder of this repository
1. Click process input.

On the screen, you'll obtain the text parsed in CONLLU format. This parser
adds a second set of part-of-speech tags, some morphological features, and 
generates sentence IDs.

If the parser doesn't work for some reason, the results are in the
[grchron-udpipe.conllu](../data/grchron-udpipe.conllu) file.

## 3. Querying the results with GREW

We suggest two options for working with the parsed data:
1. Use the online Arborator GREW interface [https://arboratorgrew.elizia.net/#/](https://arboratorgrew.elizia.net/#/)
1. Use GREW Match from the command line.

Arborator GREW has an intuitive graphical interface and we discuss how to
use it live in the workshop, so in this tutorial we'll focus on the
command-line interface.

### 3.1. Write the GREW query

Let's take a look at our results with a basic query to get an idea of
how good the parse is. For example, let's see if every sentence is headed
by a verb.

First of all, we need to write a GREW query to identify sentences which
aren't headed by a verb. You can check using the corpora on the [GREW match online interface](https://universal.grew.fr/) 
that the query is syntactically correct and returns the sort of result we
want before trying it out on our parsed files. The correct query, in this case,
is:
```grew
pattern {
    * -[root]-> V; % node V is the root
    V [upos<>VERB] % V is not a verb.
}
```

### 3.2. Run GREW match

Assuming you've successfully installed GREW match (see [day2-install.md](day2-install.md)),
we can run this query from the command line.
First, we create an empty text file (let's call it `query.txt`) and
save our query in it.
Next, we run GREW match on the output of the HOPS parser with the following commands:
```console
cd ~
eval $(opam env)
grew grep -request query.txt -i from-parser-to-query/data/grchron-hops.conllu
```

By default, results are printed to the terminal in `.json` format, which, to be
perfectly honest, is not very helpful at all, other than to confirm that
this structure is found. So we've developed a simple Python script to convert this
output into a more usable form, similar to the concordances available on the
GREW match website.

To see the query results in a more helpful form, try the following:
```console
cd ~
eval $(opam env)
grew grep -request query.txt -i from-parser-to-query/data/grchron-hops.conllu > query.json
python3 from-parser-to-query/scripts/json2tsv.py --conllu from-parser-to-query/data/grchron-hops.conllu --json query.json --pivot V
```
(If GREW match doesn't run on your computer, the files [query.txt](query.txt),
[query.json](query.json) and [query.tsv](query.tsv) are included in this
Git repository.)

This generates a file `query.tsv` which can be opened in a text editor or a spreadsheet editor.
We can quickly see from this file that:
+ "sentences" 118, 140, 148 and 185 contain no main verb, so the parse is correct;
+ sentences 129 and 212 have a nominal head because in UD, the attribute rather than the copula is the head of the clause, so the parse is correct here too;
+ sentence 123 has been annotated correctly with *est* as the root; however, the verb must have been given the wrong `upos` tag by the parser (probably `AUX`).
+ sentence 203 is a copula construction but the **verb** *estoit* has been identified as the head and must have been give the wrong `upos` tag too. The parse here is incorrect.

From the examples above, it's clear that copula constructions
seem to cause problems for the parser, which is useful information. 
When using this corpus, we might be particularly cautious in dealing with 
sentences headed by the verb *être* "to be", which is usually either a
copula or an auxiliary, neither of which should usually appear as a root.

