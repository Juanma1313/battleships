'''
File: ansi_commands.py
Date: 2023-03-22
Author: Juan Manuel de las Heras Arroyo

Description:
   Define constants elements to construct ANSI commands to set front and
background colors, stiles for a standard ANSI console output.
ANSI command construction:
  [ES] + [S] +";" + [TC] + ";" + [BC] + "m" '''
#    - [ES] Escape sequence
#ESCSEQ = '\x1b['    # Escape in hexadecimal
#ESCSEQ = "\u001b["  # in Unicode
ESCSEQ = "\033["     # in Octal  (Prefered)
#    - [S] Style
S_NORMAL    ='0'
S_BOLD      ='1'
S_LIGHT     ='2'
S_ITALIZED  ='3'
S_UNDERLINED='4'
S_BLINK     ='5'
#    - [TC] Text Color
TC_BLACK    ='30'
TC_RED      ='31'
TC_GREEN    ='32'
TC_YELLOW   ='33'
TC_BLUE     ='34'
TC_PURPLE   ='35'
TC_CYAN     ='36'
TC_WHITE    ='37'
#    - [BC] Background Color
BC_BLACK    ='40'
BC_RED      ='41'
BC_GREEN    ='42'
BC_YELLOW   ='43'
BC_BLUE     ='44'
BC_PURPLE   ='45'
BC_CYAN     ='46'
BC_WHITE    ='47'

#CLRSCR = ESCSEQ + "2J"      # Clear screen command
CLRSCR =  "\033c"       # Clear screen command

CURPOS = "\033[{};{}f"  # Cursor positioning command
                    # Note: Be aware of the format to include Row and Collumn




