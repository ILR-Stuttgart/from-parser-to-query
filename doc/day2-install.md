# Installing tools for the workshop

## Introduction

This guide allows you to install all the command-line tools you
need for the workshop. Windows users will need to install CygWin.
+ Python 3
+ HOPS Parser \(REF\)
+ GREW \(REF\)

## Linux \(Ubuntu/Debian\)

The basic tools (Python, PIP, sed, wget) should be installed by default. If
in doubt, run:
```console
sudo apt install python3 python3-pip python3-virtualenv sed wget
```

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

To test the installation, copy the file [test.txt](../doc/from-parser-to-query/data/test.txt)
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
eval $(opam env)
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

## Windows

The easiest way to run our tools on Windows is to install CygWin, a 
Unix-like environment.

1. Go to [https://www.cygwin.com](https://www.cygwin.com), download and run the setup file.
1. Accept default settings until you get to the "Select Packages" window.
1. At the select packages windows, install:
	+ Archive > unzip
	+ Python > python3 python3-pip python3-virtualenc
	+ Libs > opam opam-installer
	+ Net > curl
	+ OCaml > ocaml
	+ Text > m4
	+ Web > wget
1. Once the install is complete, double-click the "CygWin64 Terminal" icon to open the terminal
1. Test the installation by running the following commands:
```console
python3 --version
pip3 --version
opam --version
```

Don't delete the setup file (`setup-x86_64.exe`) since you need to run it
to install and delete packages from the CygWin installation.

### HOPS Parser and models

Unfortunately, we were not able to install the HOPS Parser using CygWin
due to an error when compiling C++ dependencies.

### GREW

Installing GREW on CygWin is almost the same as on Linux but version
1.9.5 of the `ocamlfind` library has to be installed manually (default
version 1.9.6 fails to install). Here's a summary of the commands:

```console
opam init
eval $(opam env)
opam switch create 5.1.1
eval $(opam env)
opam remote add grew "http://opam.grew.fr"
opam install re ocamlfind.1.9.5
opam install grew
```

To test the GREW installation:
```console
eval $(opam env)
grew version
```
This currently returns an error message and then the version number;
but this is fine!
