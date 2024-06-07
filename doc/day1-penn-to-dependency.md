# Converting Penn to dependency format

## Introduction

This is a very brief tutorial to help you install and run a state-of-the-art
constituency to dependency convertor on an open-access corpus of
historical English. *It does not create a usable corpus, it is simply a
proof of concept.* However, it illustrates that the approach we advocate,
conversion to dependency and then training a dependency parser, is a
feasible method for obtaining a parser for languages like English where
the majority of gold corpus data is in Penn constituency format.

The convertor was developed and customized for the Icelandic IcePaHC
corpus, but can with a little knowledge of Python be adapted to produce
good results for other Penn corpora.

## Background

The *Icelandic Parsed Historical Corpus* (IcePaHC, Wallenberg et al., 2011)
is a diachronic corpus of the Icelandic language and was annotated using
the Penn constituency format. You can read more about it [on the wiki](https://linguist.is/wiki/index.php?title=Icelandic_Parsed_Historical_Corpus_(IcePaHC)).

It was automatically converted to Universal Dependencies by 
Þórunn Arnardóttir and colleagues (Arnardóttir et al., 2020, 2023) and
this new version is included in the current UD corpora distributed at
[https://universaldependencies.org/](https://universaldependencies.org/).

Arnardóttir et al. (2020) document the conversion process, and the
conversion tool is available under an Apache 2.0 license [on GitHub](https://github.com/thorunna/UDConverter).

## Installation

You'll need `git` installed on your machine, [see instructions here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
Python should be installed too, [see instructions here](install.md).

Clone both the convertor and the corpus with the following commands:
```console
git clone https://github.com/thorunna/UDConverter.git
git clone https://github.com/beatrice57/pceec2.git
```

Next, create a Python virtual environment and install the dependencies
for the convertor:
```console
python3 -m venv udconverter
source udconverter/bin/activate
pip install -r UDConverter/requirements.txt
```

Test the installation
```console
python3 UDConverter/scripts/convert.py -h
```

## A quick hack

In order to get the converter to run on non-IcePaHC files,
we need to quickly hack the code to disable the lookup of morphological
features which aren't present in ICEPAHC (causes a Python `KeyError`).
Use `sed` for this unsubtle manipulation, and thanks to Achim Stein
for the tip.
```console
sed -i 's/= Icepahc_feats/= 0 #Icepahc_feats/g' UDConverter/scripts/lib/features.py
```

## Converting a file

To convert a single file from the PCEEC2, here `allen.psd`, type the
following:
```console
cd UDConverter/scripts
python3 convert.py -N -i ~/pceec2/data/parsed/allen.psd --post_process --output
```

The conversion ends rather ungracefully with a Python error, but the file
is correctly saved to `UDConverter/CoNLLU/icepahc`. There's clearly
a lot of fine-tuning required - most obviously the `METADATA` and `CODE`
nodes in the PCEEC2 are not handled - but the core of the conversion
is there and can form the basis of parser training data for English
historical texts.

## References

+ Arnardóttir, Þórunn, Hinrik Hafsteinsson, Einar Freyr Sigurðsson, Kristín Bjarnadóttir, Anton Karl Ingason, Hildur Jónsdóttir, and Steinþór Steingrímsson. 2020. ‘A Universal Dependencies Conversion Pipeline for a Penn-Format Constituency Treebank’. In *Proceedings of the Fourth Workshop on Universal Dependencies (UDW 2020)*, edited by Marie-Catherine de Marneffe, Miryam de Lhoneux, Joakim Nivre, and Sebastian Schuster, 16–25. Barcelona, Spain (Online): Association for Computational Linguistics. [https://aclanthology.org/2020.udw-1.3](https://aclanthology.org/2020.udw-1.3).
+ Arnardóttir, Þórunn, Hinrik Hafsteinsson, Atli Jasonarson, Anton Ingason, and Steinþór Steingrímsson. 2023. ‘Evaluating a Universal Dependencies Conversion Pipeline for Icelandic’. In *Proceedings of the 24th Nordic Conference on Computational Linguistics (NoDaLiDa)*, edited by Tanel Alumäe and Mark Fishel, 698–704. Tórshavn, Faroe Islands: University of Tartu Library. [https://aclanthology.org/2023.nodalida-1.69](https://aclanthology.org/2023.nodalida-1.69).
+ Wallenberg, Joel C., Anton Karl Ingason, Einar Freyr Sigurðsson, and Eiríkur Rögnvaldsson. 2011. *Icelandic Parsed Historical Corpus (IcePaHC)*. Version 0.9. [http://www.linguist.is/icelandic_treebank](http://www.linguist.is/icelandic_treebank).


