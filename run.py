'''
File: battleships.py
Date: 2023-03-22
Author: Juan Manuel de las Heras Arroyo

Description:
This file contains the main entry point for the Battleships game application.
It holds also all the console-user interaction and the main game logic.
'''
from time import sleep as delay     # delay in seconds to allow player to read screens

from battleships_colors import *    # import available color commands

def get_grid_size(name, cols, rows):
    '''Requests the user the size of the board in columns and rows.
    the format for the user is str_columns_number+'x'str_rows_number
    returns a tuple in the form (int_columns, int_rows)
    '''
    while True:
        display_title()
        print(f"\n\n\nThe current battle_zone size is a grid of {cols}x{rows}.")
        print(f"If you want to change this setting, type the new size like '11x11'".center(66))
        print(f"o just press [Enter] to continue with the current size".center(66))
        print(f"(sizes available are from 8x8 up to 12x10)".center(66))
        print (" "*33, end='')
        size =input()
        if size:
            player_name=None
            try:
                t_cols,t_rows=size.split("x")
                if not (8 <= int(t_cols) <= 12):
                    # value out of range
                    print (f"\n Sorry, {t_cols} columns is not valid".center(66))
                elif not (8 <= int(t_rows) <= 10):
                    print (f"\n Sorry, {t_rows} rows is not valid".center(66))
                else:
                    cols=int(t_cols)
                    rows=int(t_rows)
                    break
            except Exception as e:
                print (f"\n Sorry, {size} is not valid".center(66))
            delay(2)  # waits for 2 secconds so the user can read the message, and then continues
            #input("Press [Enter] to try again".center(66))

        else:
            break

    return cols,rows

def get_player_name(name=None):
    player_name=None
    while not player_name:
        display_title()
        print("\n\n\nWrite your name and press [ENTER] to start.".center(66))
        print("(15 leters max.)".center(66))
        print (" "*33, end='')
        player_name=input()
        if not player_name and name:
            # User pressed enter but there was a previous name defined
            player_name=name
            break
        if len(player_name)>15:
            player_name=None

    return player_name

def main_menu(name=""):
    ''' Presents the main menu on the console, validates the user input
    and returns the selected option
    '''
    option=None
    while True:
        display_title()
        print(f"\n\n\nHello {name}, Welcome to a new game of Battleships ".center(66))
        print(C_UNDERLINE+ "MAIN MENU".center(66)+C_NORMAL)
        print("\n\t1.- Change Player Name")
        print("\n\t2.- Change Battleship zone size")
        print("\n\t3.- Start the game")
        print("\n")
        #print("\n\t4.- Let the computer play alone")
        print("\n\t5.- Exit")
        print ("\nSelect an option".center(66) )
        print (" "*33, end='')
        t_option=input()
        if not t_option: continue
        try:
            option=int(t_option)
            if not 1 <= option <= 5:
                print (f"\n Sorry, option {t_option} out of range ".center(66))
            else:
                break
        except Exception as e:
            print (f"\n Sorry, option {option} is not valid".center(66))
        delay(2)  # waits for 2 secconds so the user can read the message, and then continues

    return option

def display_title():
    ''' Clears the terminal and presents the game title at the top of the
    screen.
    '''
    global columns
    print(CLRSCR,end='')        # Clear screen
    print(CURPOS.format(1,1),end='')  # Positions the cursor to row=1, col=1
    print(C_TITLE+"".center(columns*2*3+6)+C_NORMAL)
    print(C_TITLE+"BATTLESHIPS".center(columns*2*3+6)+C_NORMAL)

# GLOBAL VARIABLES
player_name=None
columns=10
rows=10

def main(args):
    ''' Presents the main menu and directs the control to the
    selected option.
    '''
    global player_name,columns,rows

    player_name=get_player_name()
    while True:
        option=main_menu(player_name)
        if   option == 1: # Change Name
            player_name=get_player_name(player_name)
        elif option == 2: # Change battle_zone size
            (columns,rows) = get_grid_size(player_name, columns, rows)
        elif option == 3: # player against ther computer
            winner=battleships_game(columns=columns, rows=rows, name=player_name)
            if winner.name==player_name:
                message="Congratulations, You gave won"
            else:
                message="I'm sorry, you've lost the game"
            game_over_message(message)

        elif option == 4: # Computer against computer
            pass
        elif option == 5: # Exit
            break
        else:   # Option not available
            # this should never happen
            pass

    return 0


if __name__ == '__main__':
    # it only executes main() if its the main module, otherwise acts as an import.
    import sys
    sys.exit(main(sys.argv))


