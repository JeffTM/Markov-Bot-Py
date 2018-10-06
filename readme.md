# Markov Bot Py
By Jeffrey Matthews, 2018

Markov Bot Py is my Python implementation of a semi-random text generator based on Markov chains.
It consists of 3 main modules:
1.	Tokenizer – Contains functions for tokenizing string input
2.	MarkovBot.py - Contains the MarkovBot class
3.	Formatter.py - Contains functions for formatting a list of tokens into human readable text

## General usage:
In general, the programmer should first tokenize the input text with one of the Tokenizer functions.
Then the programmer should pass those tokens to the MarkovBot class through build or the constructor.
Finally, the programmer should call walk on the MarkovBot class and pass the output tokens to a Formatter function.

## Documentation:
The source code of the 3 main modules is documented entirely with Python docstrings.
They are fully compatible with the help function. Just remember to import each module!

## Extensibility:
The source code of the 3 main modules is intended to be fully modifiable and extensible by the programmer.
Programmers are encouraged to experiment with their own tokenizer and formatter functions.

## Samples:
Two sample programs are provided:
Sample_TUI.py is a sample terminal based program
Sample_GUI.py is a sample GUI program. It uses the breezypythongui module by Ken Lambert
