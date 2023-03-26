'''
File: battleships_classes.py
Date: 2023-03-22
Author: Juan Manuel de las Heras Arroyo

Description:
This file contains the definition of the ships classes used in the Battleships
project.
It also defines all the constats used to describe all the ships and game board
elements internally and to be displayed at the console.
'''

# *** Grid Elements Constants ***
DEFAULT         = 0

# --- Possition ---
HORIZONTAL      = DEFAULT   # 0
VERTICAL        = 0x100 # 0b_1_0000_0000
RADAR           = 0x200 #0b_10_0000_0000
# --- Ship ---
SHIP            = 0x80  # 0b_0_1000_0000
DECK            = 0x20  # 0b_0_0010_0000
BOW             = 0x40  # 0b_0_0100_0000
STERN           = 0x60  # 0b_0_0110_0000

# --- Water ---
WATER           = 0x10  # 0b_0_0001_0000
SPLASH          = 0x04  # 0b_0_0000_0100
MISS            = 0x08  # 0b_0_0000_1100
# --- State ---
NORMAL          = DEFAULT
EXPLODE         = 0x01  # 0b_0_0000_0001
SUNK            = 0x03  # 0b_0_0000_0011

ELEMENT_MASK    = RADAR | HORIZONTAL | VERTICAL | SHIP | DECK | BOW | STERN | WATER | MISS | SPLASH
#ELEMENT_MASK    = 0x1FC # 0b_1_1111_1100
COLOR_MASK      = SHIP | WATER | NORMAL | EXPLODE | SUNK | MISS | SPLASH
#COLOR_MASK      = 0x09F # 0b_0_1001_1111
STATE_MASK      = NORMAL | EXPLODE | SUNK | MISS | SPLASH

