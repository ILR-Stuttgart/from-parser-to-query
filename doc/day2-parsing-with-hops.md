# Parsing your own text

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
repository](https://github.com/hopsparser/hopsparser).

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

## 2. Parsing with UD-Pipe

TODO

## 3. Querying the results with GREW (command line)

Let's take a look at our results with a basic query to get an idea of
how good the parse is. For example, let's see if every sentence is headed
by a verb.

### 3.1. Write the GREW query

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

This generates a file `query.tsv` which can be opened in a text editor or a spreadsheet editor.
We can quickly see from this file that:
+ "sentences" 118, 140, 148 and 185 are actually verb-less, so the parse is correct;
+ sentences 129 and 212 do have a main verb, but this hasn't been identified as the root, so the parse is wrong;
+ sentences 123 and 203 have been annotated correctly with the main verb as the root so the parse is correct; however, the verb must have been given the wrong `upos` tag by the parser (probably `AUX`).

The last instance is a classic case of the kind of parser error that doesn't matter
very much if you are aware of it. We could simply modify our query to exclude
both `VERB` and `AUX` tags when looking for sentences without verbs, even though
according to the UD guidelines, `AUX` should never be the root of a clause anyway.
