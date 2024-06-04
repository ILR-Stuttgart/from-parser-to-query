# Installing tools for the workshop

## Introduction

This guide allows you to install all the command-line tools you
need for the workshop. Windows users will need to install CygWin.
+ Python 3
+ HOPS Parser \(REF\)
+ GREW \(REF\)

## Linux \(Ubuntu/Debian\)

### Python 3

Python 3 is installed by default.

### HOPS Parser and models

WARNING: this is a very large download. You will need a fast internet
connection and 6GB of free disk space.

First, create a virtual environment called `hopsparser` in your home
directory and activate it.
```console
cd ~
python3 -m venv hopsparser
source hopsparser/bin/activate
```
Next, install the [HOPS parser](https://github.com/hopsparser/hopsparser)
within the virtual environment using pip.
```console
pip install hopsparser
```
We'll be using the modern French model trained on the Sequoia corpus
with Camembert word embeddings. To install the model, run the following:
```console
wget https://zenodo.org/record/7703346/files/UD_French-Sequoia-flaubert.tar.xz
tar -xf UD_French-Sequoia-flaubert.tar.xz
```

To test the installation, copy the file [test.txt](../doc/from-parser-to-query/test.txt)
to your home directory and run the following command:
```console
hopsparser parse --raw UD_French-Sequoia-flaubert test.txt out.conll
```

### GREW

To install GREW, follow the instructions on the [grew.fr](https://grew.fr/usage/install)
website. Here's a summary of the commands:
```console
sudo apt install opam
sudo apt install wget m4 unzip librsvg2-bin curl bubblewrap
opam init
opam switch create 5.1.1
eval $(opam env)
opam remote add grew "http://opam.grew.fr"
opam install re # not listed on website but necessary
opam install grew
```

To test the GREW installation:
```console
eval $(opam env)
grew version
```
This currently returns an error message and then the version number;
but this is fine!

