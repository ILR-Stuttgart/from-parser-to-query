# Querying Dependency Corpus with GREW Match

## Introduction

In this tutorial, we'll learn how to use the GREW Match query language
in a user-friendly GREW match online portal: [https://universal.grew.fr/](https://universal.grew.fr/)
The website also contains an excellent tutorial on using the query 
language.

Full documentation for the query language is found here:
[https://grew.fr/doc/request/](https://grew.fr/doc/request/).

Full documentation of the UD tagset is found here: [https://universaldependencies.org/guidelines.html](https://universaldependencies.org/guidelines.html).
The pages on POS tags and syntactic relations are particularly useful.

## Sample query: Looking for double objects in English

We're going to use the query finder to look for double object
constructions in English. We're going to use the UD GUM corpus
\(see [https://gucorpling.org/gum/](https://gucorpling.org/gum/) for further information\).
So we select the corpus `UD_English-GUM@2.13`.

### Step 1. Let's see how they're annotated

Let's begin for looking for sentences containing a typical double-object
verb, "give". We define a node, X, with the lemma *give*:
```opam
pattern { X [lemma="give"] }
```
Next, let's look for cases of *give* with an object:
```opam
pattern { 
	X [lemma="give"]; % node X has the lemma "give"
	X -[obj]-> Y % node X has an "obj" relation to node Y
}
```
In the sentence `GUM_academic_huh-29`, we see a double object construction,
*gives us a natural control over...*. Looking at the graph, the second
object is annotated, logically enough, as `iobj`.

### Step 2. Refining the query to get the right ditransitives

Our basic ditransitive query requires a verb to have a direct and an
indirect object:
```opam
pattern { 
	X -[obj]-> Y; % node X dominates node Y with an "obj" relation
	X -[iobj]-> Z % node X dominates node Z with an "iobj" relation
}
```
Looking through the results, most of these seem to be double object
constructions. Are there any indirect objects introduced by the 
preposition "to"?
```opam
pattern { 
	X -[iobj]-> Y; % some node X dominates some node Y with an "iobj" relation
	Z [form = "to"]; % node Z is the form "to"
	Y -> Z % node Y dominates node Z
}
```
No. This means that the prepositional objects are annotated differently.
We'll come to them in a minute. For now, we can use clustering on
our first query to produce a list of verb lemmas attested with 
double objects in the corpus:
+ change `Clustering 1` to `Key`
+ write `X.lemma` in the textbox.
+ rerun the search

### Step 3. Finding verbs which also take a prepositional object

How are structures with a prepositional object annotated? We need
to look for sentences with an object, then some other nominal dependent
introduced by the preposition "to":
```opam
pattern { 
	X -[obj]-> *; % some node X has an object
	Z [upos=NOUN|PRON]; % some node Z is a nominal (noun or pronoun)
	X -> Z; % node X also dominates node Z
	A [form = "to"]; % some node A is the form "to"
	Z -> A % node Z dominates node A
}
```
If we look at hit 6 (`GUM_academic_census-29 \[1/4\]`), we can see that
this relation is tagged `obl`, and the relation to *to* is tagged as
`case` So now we can refine our query to look for all verbs with an
"obl" argument introduced by *to*:
```opam
pattern { 
	X -[obj]-> *; % some node X has an object
	Z [upos=NOUN|PRON]; % some node Z is a nominal (noun or pronoun)
	X -[obl]-> Z; % node X also dominates node Z with an "obl" relation
	A [form = "to"]; % some node A is the form "to"
	Z -[case]-> A % node Z dominates node A with a "case" relation
}
```
Again, by clustering on the key, we can see that verbs like *give*
allow both structures. By clicking on *give*, we can see the matching
results.

### Step 4. Word order

Usually the prepositional object will follow the direct object in a 
sentence. But is this the case here? Let's adapt our last query
slightly to see if there are any cases where the prepositional object
precedes the verb.
```opam
pattern { 
	X -[obj]-> Y; % some node X has some object node Y
	Z [upos=NOUN|PRON]; % some node Z is a nominal (noun or pronoun)
	X -[obl]-> Z; % node X also dominates node Z with an "obl" relation
	A [form = "to"]; % some node A is the form "to"
	Z -[case]-> A; % node Z dominates node A with a "case" relation
	A << Y % the node A, i.e. the preposition *to*, occurs earlier in the sentence than the direct object
}
```
There are some cases! These are an interesting set of exceptions that
we might want to filter further, but for now, we'll just save them to a
table.

Click the `TSV` button in GREW Match, select X as the pivot (i.e. the
verb should be a keyword), and then "Download .tsv file". This gives you
a text file with your results in tabular format.
