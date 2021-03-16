README
===========================
Two Dice Pig Game
===========================

Description
===========================
The application is a python script game for the game called two dice pig game, which is a variation of the [Pig game](https://en.wikipedia.org/wiki/Pig_(dice_game)). It is run from the terminal with a python interpreter.
The game is a two-player game, where the players play against one another. The game can also be played as a single-player game when the computer does the opposing player's role.

Game automatically either creates, or updates a HighScore.txt file in the application folder, this is to keep track of played games.


Installation
===========================
These instructions have been made for the windows. Linux and Mac commands may differ.

We assume that the user has access to and has installed, python, Graphviz and make and is familiar with how to use them.

For playing, there are no other preparations than unzipping the files.

For testing purposes, all needed packages are stated in the requirements.txt file,
The makefile has commands that automate the installation of said packages and for creating the virtual environment.

make venv
make install


Usage
===========================
To play the game or to run the tests, navigate to the folder named application with terminal and use the command:

python main.py

To run the tests and to create documentation, we have provided makefile with commands to automate them, these are to be used in the application folder:

make tests 	(this will run coverage, lint and flake8)
make coverage	(generates also coverage reports)
make lint
make flake8
make doc		(generates documentation)


Documentation
===========================
Documentations folder contains auto-generated documentation for this application, including UML-diagrams and coverage reports.


Construction of the application
===========================
Here is a brief explanation for application's classes.

*main*
Starts the game.


*shell*
Contains the interaction from the player(s). This is where all the doing is done.


*game*
It is a crossroads and handles the data flow from the shell to other parts of the application. It is responsible for tracking some details of the data relevant to the current round that is being played. Parts of the computers playing interaction is provided from here.


*dice*
Holds values for the die and its methods.


*dice_hand*
Resposible for managing throw values and keeping track of the current round score.


*player*
Holds the players name and score, together with methods needed to change these.


*intelligence*
Has the computer's decision making for how to play the game.
There is two strategies for computer to follow;

- level one is based on random yes/no decision.
- with level two, computer saves the round score when it is either, enough to win the game, or when it is over 14.


*histogram*
Responsible for played game statistics.


Authors
===========================
Meron Habtemichael, Aki Sirki�, Nahom Teclemicael.


License
===========================
This is stated in the LICENSE.md
