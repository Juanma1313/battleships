
if __name__ == '__main__':
    # it only executes main() if its the main module, otherwise acts as an import.
    import sys
    #from battleships import *
    import battleships
    sys.exit(battleships.main(sys.argv))


