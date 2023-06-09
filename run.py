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
from battleships_classes import *    # import battleships classes

# **** Define Players arsenal
PLAYER_SHIPS = [Carrier, Battleship, Destroyer, Submarine, Patrol_Boat]
COMPUTER_SHIPS = [Carrier, Battleship, Destroyer, Submarine, Patrol_Boat]

def display_status(battle_zone):
    ''' calculates the statistics about the ships for the player and the
    computer and outputs them to the console.
    '''
    player_status_header = f"{battle_zone.name} Status".center(battle_zone.columns*3)+C_NORMAL
    computer_status_header = f"Enemy Status".center(battle_zone.columns*3)+C_NORMAL
    print (f" {C_STATUS_HEADER_ROW} {player_status_header}   {C_STATUS_HEADER_ROW}{computer_status_header}")
    #prepare the enemy battleship list
    enemy_units_hit=0
    enemy_battleships_sunk=[]
    for shot in battle_zone.fired_shots:
        if battle_zone.fired_shots[shot][0] == RESULT_HIT: # found a hit
            enemy_units_hit+=1
        elif battle_zone.fired_shots[shot][0] == RESULT_SUNK: # found a SUNK
            #add the battleship designation to the sunk list
            enemy_battleships_sunk.append(battle_zone.fired_shots[shot][1])


    for index in range(len(battle_zone.ships)):
        # Prepare the player status line
        ship=battle_zone.ships[index]
        designation=ship.designation
        if ship.sunk:
            status=f"{C_STATUS_SUNK} SUNK {C_STATUS_PANEL}"
        elif not ship.hits:
            status=f"{C_STATUS_OK} 100% {C_STATUS_PANEL}"
        else:
            status=f"{C_STATUS_HIT} {100-ship.hits*100//ship.size:3}% {C_STATUS_PANEL}"
        player_status_line= f"{C_STATUS_DESIGNATION}{designation.ljust(15)} {status}"+"".ljust(battle_zone.columns*3-22)
        # Prepare the Enemy status line
        if len(enemy_battleships_sunk)>index:
            designation=enemy_battleships_sunk[index]
            status=f"{C_STATUS_SUNK} SUNK {C_STATUS_PANEL}"
            computer_status_line=f"{C_STATUS_DESIGNATION}{designation.ljust(15)} {status}"+"".ljust(battle_zone.columns*3-22)
        else:
            computer_status_line=f"{C_STATUS_PANEL}"+"".ljust(battle_zone.columns*3)

        print (f" {C_STATUS_PANEL} {player_status_line}{C_NORMAL}   {C_STATUS_PANEL}{computer_status_line}{C_NORMAL}")


def display_grids(battle_zone):
    ''' Translates the internal representation in the battle_zone object to the
    display representation and outputs the information to the console.
    Once the information is presented, calls tu update explosions.
    Note: Remember that grid is a python bidimentional array and starts
        at grid[0][0]
    '''
    battle_zone.update_grids()   # Update the grid and radar with any new information
    # Draws the Grid Header
    grid=battle_zone.grid
    radar=battle_zone.radar
    grid_header_row =f"{C_GRID_HEADER_ROW }  " + "".join([f"{x:3}" for x in range(1,battle_zone.columns+1)])+" "+C_NORMAL
    radar_header_row=f"{C_RADAR_HEADER_ROW}  " + "".join([f"{x:3}" for x in range(1,battle_zone.columns+1)])+" "+ C_NORMAL
    print(grid_header_row+radar_header_row)
    # Draws Grid elements
    for row in range(battle_zone.rows):
        grid_row =f"{C_GRID_HEADER_COL} {chr(65 + row) } " # initializes grid row
        radar_row=f"{C_RADAR_HEADER_COL} {chr(65 + row)} "    # initializes radar row
        for col in range(battle_zone.columns):
            #Calculate grid column
            element = grid[row][col]
            try: # avoids the game to break if there is color or caracter set errors.
                 #   (this is in case the set is loaded from a config file)
                graph_element=Game_Colors[element & COLOR_MASK] + board_elements[element & ELEMENT_MASK ]
                grid_row+= graph_element
            except Exception  as e:
                grid_row+= "???"
            # calculate Radar column
            element = radar[row][col]
            try: # avoids the game to break if there is color or caracter set errors.
                 #   (this is in case the set is loaded from a config file)
                graph_element=Game_Colors[element & COLOR_MASK] + board_elements[element & ELEMENT_MASK ]
                radar_row+= graph_element
            except Exception  as e:
                radar_row+= "???"
                print(f"display_battle_zone(): Error: {e}\n Pos({row}, {col})={hex(element)}, Game_Colors({hex(element & COLOR_MASK)}) , board_elements({hex(element & ELEMENT_MASK)})")

        print(grid_row + C_NORMAL + radar_row +C_NORMAL)   # OUTPUTS THE FULL ROW TO THE CONSOLE

    battle_zone.update_explosions() # Update explosion for next display loop


def display_battle_zone(battle_zone):
    '''Presents the full game screen to the console calling all the functions
    that create each individual segment of the screen
    '''
    display_title(battle_zone)
    display_status(battle_zone)
    display_grids(battle_zone)


def translate_coordinates(location):
    ''' Translate the player coordinate string str_row_letter+str_column_number
    to internal representation tuple (int_column, int_row).
    '''
    row=-1  # Set coordinates to error
    col=-1
    if not (ord('A')  <= ord(location[0]) <= ord('J')):   # Bad row
        print(f"Sorry, the coordinates {location} are invalid, valid rows are from A to J")
    elif not location[1:].isnumeric():    # bad column
        print(f"Sorry, the coordinates {location} are invalid, valid columns are from 1 to 10")
    else:
        row =  ord(location[0]) - ord('@')
        col =  int(location[1:])
    return (col, row)

def get_new_ship_location(ship_class):
    ''' Requests to the user the new ship location , validates the input and
    returns one of the following options as tuple (coordinate, position)
    where coordinates is a tuple in the format (int_column, int_raw)
    and the position either HORIZONTAL or VERTICAL constants.
        - A tuple with valid translated numeric coordinates and position
        - The tuple ((None, None),BNone) signaling a request for automation
        - The tuple ((-1, -1),-1) signaling that there was an input error
        '''
    coordinates=(-1, -1)    # Set coordinates to error
    position=-1
    print(f"Please type in the location and position of the new {ship_class.__name__}")
    print("(use Leters A-J for row, 1-10 for column and V/H for vertial or Horizontal")
    print("just press [RETURN] and an automatic random location will be generated")
    print(" Examples: 'VA1' HB8 , VD10, HH3, etc.: ",end='')
    location =input ().upper()
    if not location:    # Empty string
        coordinates=(None, None)    # Set coordinates to automatic
        position=None               # Set position to automatic
    elif len(location)<3: # Invalid location
        print(f"Sorry, the location {location} is invalid")
    elif location[0] not in ['V','H']: # Invalid Position
        print(f"Sorry, the location {location} is invalid, valid possitions are only  V or H")
    else:
        position = HORIZONTAL if location[0]=='H' else VERTICAL
        coordinates=translate_coordinates(location[1:])

    return coordinates, position

def get_coordinates():
    ''' Requests to the user the firing coordinates, validates the input and
    returns one of the following options as tuple (column, row):
        - A tuple with valid translated numeric coordinates
        - The tuple (None, None) signaling a request for automation
        - The tuple (-1, -1) signaling that there was an input error
        '''
    coordinates=(-1, -1)    # Set coordinates to error
    print(f"Please type in the coordinates to fire")
    print("(use Leters A-J for row, 1-10 for column ")
    print("just press [RETURN] and an automatic random coordinates will be generated")
    print(" Examples: 'A1' B8 , D10, H3, etc.: ",end='')
    location =input().upper()
    if not location:    # Empty string
        coordinates=(None, None)    # Set coordinates to automatic
    elif len(location)<2: # Invalid coordinates
        print(f"Sorry, the coordinates {location} are invalid")
    else:
        coordinates=translate_coordinates(location)

    return coordinates


def battleships_game(columns=10,rows=10, name="Player"):
    ''' Main Battleship game function.
    It prepares the player and the computer boards and alternatively
    yields the turn to fire to both.
    The end of the game is decided when one player has sunk all his ships.
    The winner is the player who still has some ships afloat.
    '''
    # Prepare Computer  battle zone
    computer_battle_zone = battle_zone(columns=columns, rows=rows, name="Computer")
    for ship_class in COMPUTER_SHIPS:
        result = RESULT_UNKNOWN
        while result != RESULT_MISS:
            result=computer_battle_zone.new_ship(ship_class)
    # Prepare Player battle zone
    player_battle_zone = battle_zone(columns=columns, rows=rows, name=name)
    for ship_class in PLAYER_SHIPS:
        result = RESULT_UNKNOWN
        while result != RESULT_MISS:
            display_battle_zone(player_battle_zone) # Display battle zone
            # Get new ship location  input from player
            coordinates, possition =get_new_ship_location(ship_class)
            if not possition:
                #Attempt to generate automatic location
                while result != RESULT_MISS:    # ship colision avoidance loop
                    result=player_battle_zone.new_ship(ship_class)
            else:
                if possition==-1 or coordinates[0]==-1 or coordinates[1]==-1:
                    # The location could not be validated
                    delay(3) # delay to let the player read the screen

    while True: # Game loop
        if sum([ship.sunk for ship in player_battle_zone.ships]) == len(player_battle_zone.ships):
            # All the player's ships are sunk. End of the game
            winner = computer_battle_zone
            break    # end the game, The Computer wins
        while True:  # Player's turn loop
            display_battle_zone(player_battle_zone) # Display battle zone
            coordinates=get_coordinates()
            if coordinates[0]==None:
                # Automated coordinate generation
                result=(RESULT_COLUMN_ERROR, None)
                while result[0] in [RESULT_COLUMN_ERROR, RESULT_ROW_ERROR, RESULT_DUPLICATED]:
                    coordinates = player_battle_zone.random_coordinates()
                    result=player_battle_zone.fire_shot(coordinates=coordinates, battle_zone=computer_battle_zone)
                break   # end the Player's turn
            else:
                result=player_battle_zone.fire_shot(coordinates=coordinates, battle_zone=computer_battle_zone)
                if result[0] in [RESULT_COLUMN_ERROR, RESULT_ROW_ERROR]:
                    print("Sorry, the coordinates are incorrect, Please try again ")
                    delay(2)
                elif result[0]==RESULT_DUPLICATED:
                    print("Sorry, the coordinates are duplicated, Please try again ")
                    delay(2)
                else:
                    break
        # Draw screen with updated information
        display_battle_zone(player_battle_zone) # Display battle zone
        if sum([ship.sunk for ship in computer_battle_zone.ships]) == len(computer_battle_zone.ships):
            # All the Computer's  ships are sunk. End of the game
            winner = player_battle_zone
            break    # end the game # The player wins
        input("The computer will fire now, Press [return] to continue")
        #delay(1)
        while True: # compuer's turn loop
            coordinates = computer_battle_zone.random_coordinates()
            result=computer_battle_zone.fire_shot(coordinates=coordinates, battle_zone=player_battle_zone )
            if result[0] not in [RESULT_COLUMN_ERROR, RESULT_ROW_ERROR, RESULT_DUPLICATED]:
                break # end the Computer's turn

    return winner

def game_over_message(message):
    ''' Presents the final screen to the console with the winner message
    and waits for the player to press [Enter].
    '''
    row=10
    screen_width=70
    press_enter_msg="Press [Enter] to continue"
    if len(message) < len(press_enter_msg):
        message=message.center(len(press_enter_msg))

    line1=("*"*(len(message)+6)+" ")
    line2=("**" + " "*(len(message)+2) +"** ")
    column=(screen_width-len(line1))//2
    print(CURPOS.format(row,  column)+line1)
    print(CURPOS.format(row+1,column)+line1)
    print(CURPOS.format(row+2,column)+line2,)
    print(CURPOS.format(row+3,column)+("** "+message+" ** "))
    print(CURPOS.format(row+4,column)+line2)
    print(CURPOS.format(row+5,column)+line2)
    print(CURPOS.format(row+6,column)+"** "+"Press [Enter] to continue".center(len(message))+" ** ")
    print(CURPOS.format(row+7,column)+line2)
    print(CURPOS.format(row+8,  column)+line1)
    print(CURPOS.format(row+9,column)+line1)
    input()



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

def display_title(battle_zone=None):
    ''' Clears the terminal and presents the game title at the top of the
    screen.
    '''
    print(CLRSCR,end='')        # Clear screen
    print(CURPOS.format(1,1),end='')  # Positions the cursor to row=1, col=1
    if battle_zone:
        columns=battle_zone.columns
    else:
        columns=10
    print(C_TITLE+"".center(columns*2*3+6)+C_NORMAL)
    print(C_TITLE+"BATTLESHIPS".center(columns*2*3+6)+C_NORMAL)

def main(args):
    ''' Presents the main menu and directs the control to the
    selected option.
    '''
    columns=10
    rows=10
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


