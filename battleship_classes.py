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
