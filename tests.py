'''
File: tests.py
Date: 2023-03-22
Author: Juan Manuel de las Heras Arroyo

Description:
This file is a script to test the project Battleships.
It imports the main module "battleships" and simulates a battleship game
setup so it can make out of band automated calls to the game functions to
assest the correct function and report any error.
It produces 2 report files. one for the player side and other for the Computer
side, with the result of all the performed tests.
'''
import time
from run.py import *

class Tests:
    ''' Performs automated tests and stores and verifies results
    It can perform the same tasks on two battle_zones playing one agains
    the other.
    Since the same firing is performed on both the player and the computer
    the Grid and the radar should show exactly the same info when displayed.
    Arguments description:
        battle_zone_1 = Mandatory battle zone for all tests (normaly the player)
        battle_zone_2 = Only needed for fire_shot tests (normaly the computer)
        display= specifies which battle field to display (0=None)
        wait= False --> Do not wait between results
        wait=True   --> request user to press ENTER after each test
        wait= [number] --> Waits [number] seconds after each test'''

    def __init__(self, battle_zone_1, battle_zone_2=None , display=1, wait =True):
        self.battle_zone_1=battle_zone_1
        self.battle_zone_2=battle_zone_2
        self.display=display
        self.wait=wait
        self.test_results1=[]
        self.test_results2=[]
        self.test_number=0
        self.test_errors=0

    def receive_shot(self, coordinates, expected_result, test_name="Generic Test"):
        self.test_number+=1
        (result, ship) = self.battle_zone_1.receive_shot(coordinates=coordinates)
        if result!=expected_result: self.test_errors+=1
        test_info_1={"test_receive_shot":{
                        "Test_number"       :self.test_number,
                        "Name"              : test_name,
                        "Result"            :"OK" if result==expected_result else "Fail",
                        "Coordinates"       :coordinates,
                        "Expected_result"   : expected_result,
                        "Actual_result"     : result,
                        "Ship"              : ship if ship else "None"}}
        self.test_results1.append(test_info_1)
        if self.battle_zone_2:
            (result, ship) = self.battle_zone_2.receive_shot(coordinates=coordinates)
            if result!=expected_result: self.test_errors+=1
            test_info_2={"test_receive_shot":{
                            "Test_number"       :self.test_number,
                            "Name"              : test_name,
                            "Result"            :"OK" if result==expected_result else "Fail",
                            "Coordinates"       :coordinates,
                            "Expected_result"   : expected_result,
                            "Actual_result"     : result,
                            "Ship"              : ship if ship else "None"}}
            self.test_results2.append(test_info_2)

    def fire_shot(self, coordinates, expected_result, test_name="Generic Test"):
        self.test_number+=1
        # Fire from zone_1 to Zone_2
        (result, ship) = self.battle_zone_1.fire_shot(coordinates=coordinates, battle_zone=self.battle_zone_2 )
        if result!=expected_result: self.test_errors+=1
        test_info_1={"fire_shot":{
                        "Test_number"       :self.test_number,
                        "Name"              : test_name,
                        "Result"            :"OK" if result==expected_result else "Fail",
                        "Coordinates"       :coordinates,
                        "Expected_result"   : expected_result,
                        "Actual_result"     : result,
                        "Ship"              : ship if ship else "None"}}
        self.test_results1.append(test_info_1)
        if self.battle_zone_2:
            # Fire from zone_2 to Zone_1
            (result, ship) = self.battle_zone_2.fire_shot(coordinates=coordinates, battle_zone=self.battle_zone_1 )
            if result!=expected_result: self.test_errors+=1
            test_info_2={"fire_shot":{
                            "Test_number"       :self.test_number,
                            "Name"              : test_name,
                            "Result"            :"OK" if result==expected_result else "Fail",
                            "Coordinates"       :coordinates,
                            "Expected_result"   : expected_result,
                            "Actual_result"     : result,
                            "Ship"              : ship if ship else "None"}}
            self.test_results2.append(test_info_2)


        if self.display:
            if self.display&1:
                display_battle_zone(self.battle_zone_1) # Display battle zone
                print (f"\n{test_info_1}")
            if self.display&2:
                display_battle_zone(self.battle_zone_2) # Display battle zone
                print (f"\n{test_info_2}")

        if type(self.wait) in [int, float]:
            time.sleep(self.wait)
        elif type(self.wait) ==bool and self.wait:
            input("Press enter to continue")
        return


def main(args):
#Testing computer side
# '''Automates the load of randomly located ships into a battle_zone.'''
#    computer_battle_zone = battle_zone(columns=10, rows=10)
#    for ship_class in COMPUTER_SHIPS:
#        result = RESULT_UNKNOWN
#        while result != RESULT_MISS:
#            result=computer_battle_zone.new_ship(ship_class)
#        #print(f"{__name__}.main({args}), Computer ship {ship_class} placed")
#    display_battle_zone(computer_battle_zone)


    # PREPARE THE TEST SCENARIO
    COLS = 10
    ROWS = 10

    # Player side
    player_battle_zone = battle_zone(columns=COLS, rows=ROWS, name="player")   # Prepare a battle zone
    # load new ships to the player board
    player_battle_zone.new_ship(Patrol_Boat,    coordinates=( 2, 2), position=VERTICAL)
    player_battle_zone.new_ship(Submarine,      coordinates=(COLS, 7), position=VERTICAL)
    player_battle_zone.new_ship(Destroyer,      coordinates=( 6, 7), position=VERTICAL)
    player_battle_zone.new_ship(Battleship,     coordinates=( 5, 5), position=HORIZONTAL)
    player_battle_zone.new_ship(Carrier,        coordinates=( 2, 1), position=HORIZONTAL)
    display_battle_zone(player_battle_zone) # display board

    # Computer side
    computer_battle_zone = battle_zone(columns=COLS, rows=ROWS, name="Computer")   # Prepare a battle zone
    computer_battle_zone.new_ship(Patrol_Boat,    coordinates=( 2, 2), position=VERTICAL)
    computer_battle_zone.new_ship(Submarine,      coordinates=(COLS, 7), position=VERTICAL)
    computer_battle_zone.new_ship(Destroyer,      coordinates=( 6, 7), position=VERTICAL)
    computer_battle_zone.new_ship(Battleship,     coordinates=( 5, 5), position=HORIZONTAL)
    computer_battle_zone.new_ship(Carrier,        coordinates=( 2, 1), position=HORIZONTAL)
    display_battle_zone(player_battle_zone)

    # Prepare the Test object
    tests=Tests(player_battle_zone, computer_battle_zone, display=0, wait=None)
    # RUN receive_shot TESTS
    tests.receive_shot(coordinates=( 0, 1),     expected_result=RESULT_COLUMN_ERROR,    test_name="COLUMN ERROR (too low)")
    tests.receive_shot(coordinates=(COLS+1, 1), expected_result=RESULT_COLUMN_ERROR,    test_name="COLUMN ERROR (too high)")
    tests.receive_shot(coordinates=( 1, 0),     expected_result=RESULT_ROW_ERROR,       test_name="ROW ERROR (too low)")
    tests.receive_shot(coordinates=( 1, ROWS+1),expected_result=RESULT_ROW_ERROR,       test_name="ROW ERROR (too high)")
    tests.receive_shot(coordinates=( 0, 0),     expected_result=RESULT_COLUMN_ERROR,    test_name="ROW/COLUMN ERROR")

    # RUN fire_shot TESTS
    tests.fire_shot(coordinates=( 1, 1),        expected_result=RESULT_MISS,            test_name="MISS (top-left)")
    tests.fire_shot(coordinates=( 1, 1),        expected_result=RESULT_DUPLICATED,      test_name="Duplicated shot")
    tests.fire_shot(coordinates=(COLS, 1),      expected_result=RESULT_MISS,            test_name="MISS (top-right)")
    tests.fire_shot(coordinates=( 1, ROWS),     expected_result=RESULT_MISS,            test_name="MISS (bottom-left)")
    tests.fire_shot(coordinates=(COLS,ROWS),    expected_result=RESULT_MISS,            test_name="MISS (bottom-right)")
    tests.fire_shot(coordinates=( 4, 5),        expected_result=RESULT_MISS,            test_name="MISS Battleship (left)")
    tests.fire_shot(coordinates=( 9, 5),        expected_result=RESULT_MISS,            test_name="MISS Battleship (right)")
    tests.fire_shot(coordinates=( 5, 4),        expected_result=RESULT_MISS,            test_name="MISS Battleship (up)")
    tests.fire_shot(coordinates=( 5, 6),        expected_result=RESULT_MISS,            test_name="MISS Battleship (dow)")

    tests.fire_shot(coordinates=( 0, 0),        expected_result=RESULT_COLUMN_ERROR,    test_name="ROW/COLUMN ERROR")
    tests.fire_shot(coordinates=( 1, ROWS+1),   expected_result=RESULT_ROW_ERROR,       test_name="ROW ERROR (too high)")
    tests.fire_shot(coordinates=(COLS+1, 1),    expected_result=RESULT_COLUMN_ERROR,    test_name="COLUMN ERROR (too high)")
    tests.fire_shot(coordinates=( 1, 2),        expected_result=RESULT_MISS,            test_name="MISS Patrol_Boat (left)")

    tests.fire_shot(coordinates=( 2, 2),        expected_result=RESULT_HIT,             test_name="HIT unit 1 Patrol_Boat")
    tests.fire_shot(coordinates=( 2, 3),        expected_result=RESULT_SUNK,            test_name="HIT unit 2 Patrol_Boat, SUNK")

    tests.fire_shot(coordinates=( 6, 7),        expected_result=RESULT_HIT,             test_name="HIT unit 1 Destroyer")
    tests.fire_shot(coordinates=( 6, 8),        expected_result=RESULT_HIT,             test_name="HIT unit 2 Destroyer")
    tests.fire_shot(coordinates=( 6, 9),        expected_result=RESULT_SUNK,            test_name="HIT unit 3 Destroyer, SUNK")

    tests.fire_shot(coordinates=( 2, 1),        expected_result=RESULT_HIT,             test_name="HIT unit 1 Carrier")
    tests.fire_shot(coordinates=( 3, 1),        expected_result=RESULT_HIT,             test_name="HIT unit 2 Carrier")
    tests.fire_shot(coordinates=( 4, 1),        expected_result=RESULT_HIT,             test_name="HIT unit 3 Carrier")
    tests.fire_shot(coordinates=( 5, 1),        expected_result=RESULT_HIT,             test_name="HIT unit 4 Carrier")
    tests.fire_shot(coordinates=( 6, 1),        expected_result=RESULT_SUNK,            test_name="HIT unit 5 Carrier, SUNK")

    tests.fire_shot(coordinates=(COLS, 7),      expected_result=RESULT_HIT,             test_name="HIT unit 5 Submarine")
    tests.fire_shot(coordinates=(COLS, 8),      expected_result=RESULT_HIT,             test_name="HIT unit 5 Submarine")
    tests.fire_shot(coordinates=(COLS, 9),      expected_result=RESULT_SUNK,            test_name="HIT unit 5 Submarine, SUNK")

    tests.fire_shot(coordinates=( 5, 5),        expected_result=RESULT_HIT,             test_name="HIT unit 1 Battleship")
    tests.fire_shot(coordinates=( 5, 5),        expected_result=RESULT_DUPLICATED,      test_name="Duplicated shot")
    tests.fire_shot(coordinates=( 6, 5),        expected_result=RESULT_HIT,             test_name="HIT unit 2 Battleship")
    tests.fire_shot(coordinates=( 7, 5),        expected_result=RESULT_HIT,             test_name="HIT unit 3 Battleship")
    tests.fire_shot(coordinates=( 8, 5),        expected_result=RESULT_SUNK,            test_name="HIT unit 4 Battleship, SUNK")

    # Display final boards
    display_battle_zone(player_battle_zone) # Display player battle zone
    display_battle_zone(computer_battle_zone) # Display computer battle zone
    # Redisplay to process explosions
    display_battle_zone(player_battle_zone) # Display player battle zone
    display_battle_zone(computer_battle_zone) # Display computer battle zone

    # Print totals to screen

    print(f"Totals:  Tests= {tests.test_number}, Errors={tests.test_errors}")
    #import json
    with open("results1.txt", mode='w') as f:
        for test_info in tests.test_results1:
            print(f"{test_info}", file=f)

    with open("results2.txt", mode='w') as f:
        for test_info in tests.test_results2:
            print(f"{test_info}", file=f)

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

'''
Some data for testing
grid_example = [
    [0x018, 0x0C0, 0x0A0, 0x0A0, 0x0A0, 0x0E0, 0x010, 0x010, 0x010, 0x018],
    [0x018, 0x1C3, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010],
    [0x010, 0x1E3, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010],
    [0x010, 0x010, 0x010, 0x010, 0x018, 0x010, 0x010, 0x010, 0x010, 0x010],
    [0x010, 0x010, 0x010, 0x018, 0x0C3, 0x0A3, 0x0A3, 0x0E3, 0x018, 0x010],
    [0x010, 0x010, 0x010, 0x010, 0x018, 0x010, 0x010, 0x010, 0x010, 0x010],
    [0x010, 0x010, 0x010, 0x010, 0x010, 0x1C0, 0x010, 0x010, 0x010, 0x1C0],
    [0x010, 0x010, 0x010, 0x010, 0x010, 0x1A0, 0x010, 0x010, 0x010, 0x1A0],
    [0x010, 0x010, 0x010, 0x010, 0x010, 0x1E0, 0x010, 0x010, 0x010, 0x1E0],
    [0x018, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010, 0x010, 0x018]]


DISPLAY GRID and RADAR EXAMPLE
==============================

    1  2  3  4  5  6  7  8  9 10     1  2  3  4  5  6  7  8  9 10
 A  X  ◄███████████►  .  .  .  X  A  .  .  .  .  .  .  .  .  .  .
 B  X   ▲ .  .  .  .  .  .  .  .  B  X ▐█▌ .  .  .  .  .  .  .  .
 C  .   ▼ .  .  .  .  .  .  .  .  C  . ▐█▌ .  .  .  .  .  .  .  .
 D  .  .  .  .  X  .  .  .  .  .  D  .  .  .  .  .  .  .  .  .  .
 E  .  .  .  X  ◄████████►  X  .  E  .  .  .  .  .  .  .  .  .  .
 F  .  .  .  .  X  .  .  .  .  .  F  .  .  .  .  .  .  .  .  .  .
 G  .  .  .  .  .   ▲ .  .  .   ▲ G  .  .  .  .  .  .  .  .  .  .
 H  .  .  .  .  .   █ .  .  .   █ H  .  .  .  .  .  .  .  .  .  .
 I  .  .  .  .  .   ▼ .  .  .   ▼ I  .  .  .  .  .  .  .  .  .  .
 J  X  .  .  .  .  .  .  .  .  X  J  .  .  .  .  .  .  .  .  .  .

'''
