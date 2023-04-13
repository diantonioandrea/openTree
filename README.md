# openTree

Genealogy utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary).

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **openTree**.

1. Compilation
	* pyinstaller: compilation of **openTree**.
2. Usage
	* [CLIbrary](https://github.com/diantonioandrea/CLIbrary): interface, inputs and outputs.
	* bcrypt: profile password-protection.
	* requests: update system.

As a one-liner:

	python3 -m pip install --upgrade pyinstaller CLIbrary bcrypt requests

### Compiling and installing from source

**openTree** can be compiled[^1] by:

	make PLATFORM

where PLATFORM must be replaced by:

* windows
* unix (linux and macOS)

based on the platform on which **openTree** will be compiled. This will also produce a release package under ./release/openTree-PLATFORM.zip.    
**openTree** can be then installed[^2] by:

	./openTree install

or

	.\openTree.exe install

on Windows.

[^1]: The Makefile for the Windows version is written for [NMAKE](https://learn.microsoft.com/en-gb/cpp/build/reference/nmake-reference?view=msvc-170).
[^2]: This is the only way to install **openTree**.

## Commands

**openTree** supports its own help through **CLIbrary**'s help system.  
By:

	help

you'll obtain the list of available commands.
