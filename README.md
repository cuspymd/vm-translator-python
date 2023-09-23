# VM Translator in Python

![GitHub last commit](https://img.shields.io/github/last-commit/cuspymd/vm-translator-python)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/cuspymd/vm-translator-python)

This repository contains a Python implementation of the VM Translator for the Hack computer, as described in Chapter 7 of the [Nand to Tetris](https://www.nand2tetris.org/) course. With this VM Translator, you can translate VM code into Hack Assembly Language code.

## Prerequisites

- Python 3.11 or higher is required to run this VM Translator. You can download the latest version of Python from the [official Python website](https://www.python.org/downloads/).

## Installation

To use this VM Translator, you can clone this repository:

```bash
git clone https://github.com/cuspymd/vm-translator-python.git
cd vm-translator-python
```

## Usage

You can translate VM code to Hack Assembly Language code using the following command:

```bash
python -m vm_translator.main input.vm
```

This will generate an input.asm file in the same directory as your input VM code (input.vm).
