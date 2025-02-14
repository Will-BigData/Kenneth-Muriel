# Kenneth-Muriel
Blackjack Game

A simple command-line Blackjack game implemented in Python.

Table of Contents

    Features
    Requirements
    Installation
    Usage
    Game Rules

Features

    Play against a dealer in a Blackjack game.
    Load and save player data from/to a CSV file.
    Support for choosing from multiple players (one at a time).
    Basic betting system with win/loss tracking.

Requirements

    Python 3.x
    Required libraries: csv, random

Installation

Navigate into the project directory:

bash

    cd blackjack-game

Usage

    Prepare a data.csv file (if you don't have the one that was provided in this package) with player information in the following format:

name,money,wins,losses
Player1,100,0,0
Player2,150,1,0

Run the game:

bash

    python blackjack.py

    Follow the prompts in the command line to play the game.

Game Rules

    Each player is dealt two cards; the goal is to get as close to 21 as possible without going over.
    Players can choose to "hit" (draw another card) or "stand" (keep their current hand).
    Aces can count as 1 or 11 points.
    The dealer must hit until reaching a value of at least 17.
    Players win if they have a higher value than the dealer without busting (going over 21).
