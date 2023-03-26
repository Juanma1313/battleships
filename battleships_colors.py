'''
File: battleships.py
Date: 2023-03-22
Author: Juan Manuel de las Heras Arroyo

Description:
Thid file defines the constants to be used as text attributes for the output
to a standard ANSI console.
Since this is a specific file for the Battleships project, the names of the
constants prety much describe where and for what purpose they are bing used.
'''
from ansi_commands import *

# Text available attributes
C_NORMAL            = ESCSEQ  +S_NORMAL +'m'
C_UNDERLINE         = ESCSEQ  +S_UNDERLINED +'m'
C_TITLE             = ESCSEQ  +S_BOLD   +';'+S_UNDERLINED+';'+TC_YELLOW+';'+BC_BLACK  +'m'
C_STATUS_HEADER_ROW = ESCSEQ  +S_BOLD   +';'+S_UNDERLINED+';'+TC_BLACK +';'+BC_WHITE  +'m'
C_STATUS_DESIGNATION= ESCSEQ  +S_BOLD   +';'                 +TC_BLACK +';'+BC_GREEN  +'m'
C_STATUS_PANEL      = ESCSEQ  +S_NORMAL +';'                 +TC_BLACK +';'+BC_WHITE  +'m'

C_STATUS_OK         = ESCSEQ  +S_BOLD+';'+                 TC_BLACK +';'+BC_WHITE  +'m'
C_STATUS_HIT        = ESCSEQ  +S_BOLD+';'+                 TC_BLUE  +';'+BC_WHITE  +'m'
C_STATUS_SUNK       = ESCSEQ  +S_BOLD+';'+                 TC_RED   +';'+BC_WHITE  +'m'

C_GRID_HEADER_ROW   = ESCSEQ  +S_BOLD       +';'    +TC_YELLOW  +';'    +BC_BLUE   +'m'
C_RADAR_HEADER_ROW  = ESCSEQ  +S_BOLD       +';'    +TC_YELLOW  +';'    +BC_BLUE   +'m'
C_GRID_HEADER_COL   = ESCSEQ  +S_BOLD       +';'    +TC_YELLOW  +';'    +BC_BLUE   +'m'
C_RADAR_HEADER_COL  = ESCSEQ  +S_BOLD       +';'    +TC_YELLOW  +';'    +BC_BLUE   +'m'
C_WATER_NORMAL      = ESCSEQ  +S_NORMAL     +';'    +TC_BLUE    +';'    +BC_CYAN   +'m'
C_WATER_SPLASH      = ESCSEQ  +S_BLINK      +';'    +TC_CYAN    +';'    +BC_RED    +'m'
C_WATER_MISS        = ESCSEQ  +S_NORMAL     +';'    +TC_BLUE    +';'    +BC_CYAN   +'m'
C_SHIP_NORMAL       = ESCSEQ  +S_NORMAL     +';'    +TC_BLACK   +';'    +BC_CYAN   +'m'
C_SHIP_EXPLODE      = ESCSEQ  +S_BLINK      +';'    +TC_YELLOW  +';'    +BC_RED    +'m'
C_SHIP_SUNK         = ESCSEQ  +S_NORMAL     +';'    +TC_WHITE   +';'    +BC_CYAN  +'m'
