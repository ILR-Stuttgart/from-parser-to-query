# Installing tools for the workshop

## Introduction

This guide allows you to install all the command-line tools you
need for the workshop. Windows users will need to install CygWin.
+ Python 3
+ HOPS Parser \(Grobol et Crabbé 2021\)
+ GREW \(Guillaume 2021\)

Instructions are provided for [Linux](#linux-ubuntudebian), [Mac OS](#mac)
and [Windows (via CygWin)](#windows)

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

## Mac

1. Install [XCode](https://developer.apple.com/xcode/)
1. Install [brew](https://brew.sh/)

Test brew by opening a terminal and typing:
```console
brew help
```
To install Python 3, pip and Python virtual environments, and `wget` using brew:
```console
brew install python virtualenv wget
```

Test your installation by running:
```console
python3 --version
pip --version
```

### HOPS Parser and models

Follow the Linux/Ubuntu instructions above (not tested).

### GREW

To install GREW, follow the instructions on the [grew.fr](https://grew.fr/usage/install)
website. Here's a summary of the commands:
```console
brew install aspcud
brew install opam
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

## References

+ Bonfante, Guillaume, Bruno Guillaume, and Guy Perrier. 2018. 'Application of Graph Rewriting to Natural Language Processing', volume 1 of *Logic, Linguistics and Computer Science Set*. ISTE Wiley. [https://www.wiley.com/en-fr/Application+of+Graph+Rewriting+to+Natural+Language+Processing-p-9781119522348](https://www.wiley.com/en-fr/Application+of+Graph+Rewriting+to+Natural+Language+Processing-p-9781119522348)
+ Grobol, Loïc, and Benoît Crabbé. 2021. ‘Analyse en dépendances du français avec des plongements contextualisés’. In *Actes de la 28ème conférence sur le traitement automatique des langues naturelles*. [https://hal.archives-ouvertes.fr/hal-03223424](https://hal.archives-ouvertes.fr/hal-03223424).
+ Guillaume, Bruno. 'Graph Matching and Graph Rewriting: GREW tools for corpus exploration, maintenance and conversion'. *Demonstrations – 16th Conference of the European Chapter of the Association for Computational Linguistics (EACL)* [https://hal.inria.fr/hal-03177701](https://hal.inria.fr/hal-03177701).
