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
from battleships_colors import *    # import available color commands
from random import randrange        # import random number generators


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

# *** Element/State Colors ***
Game_Colors={
    WATER | NORMAL  : C_WATER_NORMAL,
    WATER | SPLASH  : C_WATER_SPLASH,
    WATER | MISS    : C_WATER_MISS,
    SHIP | NORMAL   : C_SHIP_NORMAL,
    SHIP | EXPLODE  : C_SHIP_EXPLODE,
    SHIP | SUNK     : C_SHIP_SUNK}


# *** Coordinate check constants
RESULT_COLUMN_ERROR =-1
RESULT_ROW_ERROR    =-2
RESULT_MISS         = DEFAULT
RESULT_HIT          = 1
RESULT_SUNK         = 2
RESULT_DUPLICATED   = 3
RESULT_UNKNOWN      = 10

# *** Ships classes
class Ship():
    ''' Base class for all batleships in the battle_zone
    Instances of this class represent a generic ship in the game.
    '''
    def __init__(self, coordinates, position=HORIZONTAL, size=2):
        ''' Requires coordenates to set the location in the grid'''

        self.sunk=False
        self.designation=__class__.__name__
        self.coordinates=coordinates
        self.position=position
        self.size=size
        self.hits=0
        if size >=2:
            self.units=[0]*size
            self.units[0]=position | SHIP | BOW
            self.units[-1]=position | SHIP | STERN
            for i in range(1,size-1):
                self.units[i]=position | SHIP | DECK

    @property
    def column(self):
        ''' Returns the left most column number where the ship is in the grid.
        Column range always start with 1
        '''
        return self.coordinates[0]

    @property
    def row(self):
        ''' Returns the upper most row number where the ship is in the grid.
        Row range always start with 1
        Rows are ste numerically, the UI is in charge to translate from letters
        to numbers
        '''
        return self.coordinates[1]

    def check_coordinates(self,coordinates):
        '''Test if a part of the ship is in the coordinates
        '''
        result = RESULT_MISS
        if self.position==HORIZONTAL:
            if (self.column <= coordinates[0] < self.column+self.size) and (self.row==coordinates[1]):
                #print(f"{__class__.__name__}.check_coordinates(coordinates={coordinates}), Horizontal Hit detected")
                result=RESULT_HIT
        else:
            if (self.row <= coordinates[1] < self.row+self.size) and (self.column==coordinates[0]):
                #print(f"{__class__.__name__}.check_coordinates(coordinates={coordinates}), Vertical Hit detected")
                result=RESULT_HIT
        #print(f"{__class__.__name__}.check_coordinates(coordinates={coordinates}), ship={self.designation}, result={result}")
        return result

    def receive_shot(self, coordinates):
        result=self.check_coordinates(coordinates)
        if result==RESULT_HIT:
            self.hits+=1
            if self.position==HORIZONTAL:
                 # get the damaged unit from delta column
                unit=coordinates[0]-self.column
            else:
                 # get the damaged unit from delta row
                unit=coordinates[1]-self.row    # get the damaged unit

            self.units[unit]|=EXPLODE    # Sets the unit on fire

            #if sum([(unit & EXPLODE)//EXPLODE for unit in self.units])==self.size:
            if self.hits>=self.size:
                ## All units are exploded or sunk
                self.sunk=True
                result=RESULT_SUNK  # Sip is sunk
        return result


class Patrol_Boat(Ship):
    ''' Ship subclass to define a Patrol_Boat '''
    size = 2
    def __init__(self, coordinates, position=HORIZONTAL):
        super().__init__(coordinates, position,size=2)
        self.designation=__class__.__name__

class Submarine(Ship):
    ''' Ship subclass to define a Submarine '''
    size = 3
    def __init__(self, coordinates, position=HORIZONTAL):
        super().__init__(coordinates, position,size=3)
        self.designation=__class__.__name__

class Destroyer(Ship):
    ''' Ship subclass to define a Destroyer '''
    size = 3
    def __init__(self, coordinates, position=HORIZONTAL):
        super().__init__(coordinates, position,size=3)
        self.designation=__class__.__name__

class Battleship(Ship):
    ''' Ship subclass to define a Battleship '''
    size = 4
    def __init__(self, coordinates, position=HORIZONTAL):
        super().__init__(coordinates, position,size=4)
        self.designation=__class__.__name__

class Carrier(Ship):
    ''' Ship subclass to define a Carrier '''
    size = 5
    def __init__(self, coordinates, position=HORIZONTAL):
        super().__init__(coordinates, position,size=5)
        self.designation=__class__.__name__

class battle_zone():
    ''' Mantains the information of the status of a player's board.
    battle_zone.grid: holds the symbolic representation of the state of all
        the player ships and enemy fired shots.
    battle_zone.radar: Contains the symbolic representation of the shots that
    the player has fired.
    '''
    def __init__(self, columns=10, rows=10, name="Computer"):
        self.ships=[]
        self.fired_shots={}
        self.received_shots={} # dictionary to store received shots
                     # {(column, row):coordinate:result, ship, element}
        self.name=name
        self.columns=columns
        self.rows=rows
        # Create the bidimentional array for the grid
        self.grid=[ [WATER for x in range(columns)] for x in range(rows)]
        # Create the bidimentional array for the radar
        self.radar=[ [WATER for x in range(columns)] for x in range(rows)]

    def update_grids(self):
        ''' updates the information of the two dimensional grid to represent
        the current batle state performing the following tasks:
        - Iterates throughout all the ships and sets them in the grid with
            internal representation
        - Iterates throughout all the enemy gunshots and sets them in the grid
            with internal representation
        - Iterates throughout all the player gunshots and sets them in the
            radar with internal representation.
        Note: it is important to remember that grid is a python bidimentional
        array and starts at grid[row=0][column=0] unlike the game coordenates
        that start at (column=1,row=1), note also the matrix transposition
        on columns and rows between Python arrays and the game screen'''
        # Loop throughout all the ships to represent them on the grid
        for ship in self.ships:
            #print(f"Column={ship.column}, Row={ship.row}, Size={ship.size}, Units={ship.units}")
            for i in range(ship.size):
                # Calculate the coordenates for each ship element
                (column, row)  = (ship.column-1, ship.row+i-1) if ship.position==VERTICAL else (ship.column+i-1, ship.row-1)
                # Place each ship unit on the grid
                self.grid[row][column]=ship.units[i]

        # Loop throughout all the received shots to represent them on the grid
        for shot in self.received_shots:
            if self.received_shots[shot][2] in [MISS, EXPLODE, SUNK, SPLASH]:
                # update explosion state to grid cell.
                column = shot[0]-1
                row    = shot[1]-1
                self.grid[row][column]&= ~STATE_MASK # delete explosion state in grid
                self.grid[row][column]|=self.received_shots[shot][2] # Set new state
        # Loop throughout all the fired  shots to represent them on the radar
        for shot in self.fired_shots:
            if self.fired_shots[shot][2] in [MISS, EXPLODE, SUNK, SPLASH]:
                # update explosion state to grid cell.
                column = shot[0]-1
                row    = shot[1]-1
                self.radar[row][column]&= ~STATE_MASK # delete explosion state in radar
                if self.fired_shots[shot][2] in [EXPLODE, SUNK]:
                     # ship was hit by this shot
                     element = RADAR | SHIP
                else:
                     # water was hit by this shot
                     element=self.radar[row][column]
                self.radar[row][column]= element # define radar element
                self.radar[row][column]|=self.fired_shots[shot][2] # Set new state

    def update_explosions(self):
        '''Scans the fired and received shots to replace SPLASH and EXPLODE with
        MISS and SUNK for the next display loop.
        '''
        # Updates exploding Received shots for display in Radar
        for shot in self.received_shots:
            if self.received_shots[shot][2]==EXPLODE:
                # change explosion with sunk
                self.received_shots[shot][2]=SUNK
            if self.received_shots[shot][2]==SPLASH:
                # change explosion and splash to sunk and miss .
                self.received_shots[shot][2]=MISS
        # Updates exploding Fired shots for display in Radar
        for shot in self.fired_shots:
            if self.fired_shots[shot][2]==EXPLODE:
                # change explosion with sunk
                self.fired_shots[shot][2]=SUNK
            if self.fired_shots[shot][2]==SPLASH:
                # change explosion and splash to sunk and miss .
                self.fired_shots[shot][2]=MISS

    def check_coordinates(self,coordinates):
        ''' Returns the result of a hipotetical fire solution.
        It can also be used to validate coordinates and detect collissions
        '''
        result = RESULT_UNKNOWN
        ship=None
        # Validates coordinates
        column=coordinates[0]
        row = coordinates[1]
        if not (1 <= column <= self.columns):
            #print(f"{__class__.__name__}.check_coordinates(coordinates={coordinates}), Column error")
            result = RESULT_COLUMN_ERROR
        elif not (1 <= row <= self.rows):
            #print(f"{__class__.__name__}.check_coordinates(coordinates={coordinates}), Row error")
            result = RESULT_ROW_ERROR
        elif len(self.ships)==0:  # There are no ships yet
            result = RESULT_MISS
        else:   # There are ships defined, then checks for ship collission
            for ship in self.ships:
                result= ship.check_coordinates(coordinates)
                if result != RESULT_MISS:
                    #print(f"{__class__.__name__}.check_coordinates(coordinates={coordinates}), Collition detected, Result={result}")
                    break
            else: # No ship found
                ship=None

        #print(f"{__class__.__name__}.check_coordinates(coordinates={coordinates}), Result={result}, Ship={ship}")
        return result, ship

    def validate_ship(self, ship):
        ''' tests that the ship coordinates and boundaries are correct and there is no collission
        with an existing ship
        '''
        #print(f"{__class__.__name__}.validate_ship({ship}),  coordinates={ship.coordinates}, position={ship.position}")
        result=RESULT_UNKNOWN
        for i in range(ship.size):
            if ship.position == VERTICAL:
                result, other_ship =self.check_coordinates([ship.column, ship.row+i])
            else:
                result, other_ship=self.check_coordinates([ship.column+i, ship.row])
            if result!=RESULT_MISS:
                #print(f"{__class__.__name__}.validate_chip({ship}), Collition detected at element[{i}], Result={result}, ship={other_ship}")
                break
        return result

    def new_ship(self, ship_class, coordinates=None, position=None):
        ''' Adds a new ship object to the player battle_zone
        If provided, It verifyes coordinates and boundaries and check for collissions.
        if not provided, generates random position and coordenates
        '''
        #print(f"{__class__.__name__}.new_ship({ship_class}),  coordinates={ship.coordinates}, position={ship.position}")
        if position == None:
            position=self.random_position
        if not coordinates: # if not provided define random coordinates for the ship
            coordinates=self.random_coordinates(ship_class.size, position)
        ship=ship_class(coordinates=coordinates, position=position)
        result = self.validate_ship(ship)
        if result == RESULT_MISS:
            self.ships+=[ship]
        #print(f"{__class__.__name__}.new_ship({ship_class}),  ship={ship}, coordinates={ship.coordinates}, position={ship.position}")
        return result

    def random_coordinates(self, size=None, position=None):
        ''' Returns random coordenates for fire solutions or new ship placement.
            if size and possition are defined, coordenates accomodate to ship size
            and position
        '''
        if not size:    # Requested a generic coordinate for fire solution.
            result= (randrange(1, self.columns+1), randrange(1, self.rows+1))
        else:           # Requested coordinates for new ship
            if position==VERTICAL:    # The ships position is vertical, limit the column coordinate
                result= (randrange(1, self.columns), randrange(1, self.rows-size+2))
            else:                     # The ships position is horizontal, limit the raw coordinate
                result= (randrange(1, self.columns-size+2), randrange(1, self.rows))
        return result

    @property
    def random_position(self):
        '''Returns randomly HORIZONTAL or VERTICAL position
        '''
        return HORIZONTAL if randrange(0, 2)==0 else VERTICAL


    def receive_shot(self, coordinates):
        ''' performs all the computation needed to evaluate a received shot
        from the enemy.
        If a ship unit is hit, it marks it as explosion and returns the result
        and de ship designation in a tuple.
        If a water unit is hit, it marks it as splash and returns the result
        and None in a tuple.
        Every shot is stored in the received_shots list for further processing.
        '''
        result = RESULT_UNKNOWN
        designation=None    # Variable to Stores name of the ship
        if coordinates in self.received_shots:
            result=RESULT_DUPLICATED
        else:
            (result, ship) = self.check_coordinates(coordinates)
            if result not in [RESULT_COLUMN_ERROR, RESULT_ROW_ERROR]:
                # The coordenates are valid, store received shot
                if ship:
                    # There is a new hit on a ship
                    result=ship.receive_shot(coordinates)
                    designation=ship.designation
                    #self.received_shots.update({coordinates:[result,ship,EXPLODE]})
                    explosion=EXPLODE
                else:
                    # There is a miss, prepare splash
                    explosion=SPLASH

                self.received_shots.update({coordinates:[result,designation, explosion]})

        #print(f"{__class__.__name__}.receive_shot({coordinates}),  ship={designation}, result={result}")
        return result, designation

    def fire_shot(self, coordinates, battle_zone ):
        ''' performs all the computation needed to evaluate a fired shot
        to the enemy and it will call the receive_shot function of the enemy's
        battle_zone instance which is in charge of the data updating.
        If an enemy ship unit is hit, it returns EXPLODE and the ship
        designation in a tuple.
        If an enemy water unit is hit, it returns SPlASH and None in a tuple.
        Every shot is stored in the fired_shots list for further processing.
        '''
        result = RESULT_UNKNOWN
        designation=None
        if coordinates in self.fired_shots:
            result=RESULT_DUPLICATED
        else:
            (result, designation)=battle_zone.receive_shot(coordinates)
            if result not in [RESULT_COLUMN_ERROR, RESULT_ROW_ERROR]:
                # The coordenates are valid, store fired shot
                if designation: # There is a ship in the fired coordenates
                    # There is a new hit on a ship
                    explosion=EXPLODE
                else:
                    # There is a miss, prepare splash
                    explosion=SPLASH
                self.fired_shots.update({coordinates:[result, designation, explosion]})
        #print(f"{__class__.__name__}.fire_shot({coordinates}),  ship={designation}, result={result}")
        return result, designation

