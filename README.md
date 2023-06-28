# openTree

Genealogy utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary).[^1]  

**openTree** is an easy-to-use genealogy utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary). It allows users to *easily store, search, and visualize their family trees and track their family's history*.

[^1]: **openTree** has been archived and should serve just as a fun project and a [CLIbrary](https://github.com/diantonioandrea/CLIbrary) example.

## Installation

### Prerequisites

There are some Python modules that need to be installed in order to compile and use **openTree**.

1. Compilation
	* pyinstaller: compilation of **openTree**.
2. Usage
	* [CLIbrary](https://github.com/diantonioandrea/CLIbrary): interface, inputs and outputs.
	* bcrypt: profile password-protection.
	* requests: Update notification.

As a one-liner:

	python3 -m pip install --upgrade pyinstaller CLIbrary bcrypt requests

### Compiling and installing from source

**openTree** can be compiled[^2] by:

	make PLATFORM

where PLATFORM must be replaced by:

* windows
* unix (Linux and macOS)

based on the platform on which **openTree** will be compiled.  
**openTree** can be then installed[^3] by:

	./openTree install

or

	.\openTree.exe install

on Windows.

[^2]: The Makefile for the Windows version is written for [NMAKE](https://learn.microsoft.com/en-gb/cpp/build/reference/nmake-reference?view=msvc-170).
[^3]: This is the only way to install **openTree**.

## Commands

**openTree** supports its own help through **CLIbrary**'s help system.  
By:

	help

you'll obtain the list of available commands.
