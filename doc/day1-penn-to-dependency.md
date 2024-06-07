# Converting Penn-constituency to dependency format

## Introduction

This is a very brief tutorial to help you install and run a state-of-the-art
constituency to dependency convertor on an open-access corpus of
historical English.

The convertor was developed and customized for the Icelandic IcePaHC
corpus (Árnarsdóttir et al. 2020, 2023), but can with a little knowledge
of Python be adapted to produce good results for other Penn corpora
(e.g. Stein 2024 for the French MCVF/PPCHF corpus).

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
