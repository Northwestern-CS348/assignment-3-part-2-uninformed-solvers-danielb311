from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        onPeg1 = ()
        onPeg2 = ()
        onPeg3 = ()

        currentDisk = 1
        while(True):
            currentDiskFound = False
            for fact in self.kb.facts:
                if fact.statement.predicate == "on":
                    disk = fact.statement.terms[0].term.element
                    peg = fact.statement.terms[1].term.element
                    diskNumber = int(disk[-1])
                    pegNumber = int(peg[-1])

                    if diskNumber == currentDisk:
                        currentDiskFound = True

                        if pegNumber == 1:
                            onPeg1 += tuple([diskNumber])
                        elif pegNumber == 2:
                            onPeg2 += tuple([diskNumber])
                        elif pegNumber == 3:
                            onPeg3 += tuple([diskNumber])

                        currentDisk += 1
                        break #breaks out of the for loop

            if not currentDiskFound:
                return (onPeg1, onPeg2, onPeg3)
                

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        movingDisk = movable_statement.terms[0].term.element
        oldPeg = movable_statement.terms[1].term.element
        newPeg = movable_statement.terms[2].term.element

        oldOn = parse_input("fact: (on " + movingDisk + " " + oldPeg + ")")

        oldUnderMovingDisk = parse_input("fact: (above " + movingDisk + " ?x)")
        oldUnderMovingDiskAsk = self.kb.kb_ask(oldUnderMovingDisk)

        oldDiskUnderMovingDisk = None
        oldOrdering = None

        if oldUnderMovingDiskAsk:
            oldDiskUnderMovingDisk = oldUnderMovingDiskAsk.list_of_bindings[0][1][0].statement.terms[1].term.element
            oldOrdering = parse_input("fact: (above " + movingDisk + " " + oldDiskUnderMovingDisk + ")")

        
        oldTopOldPeg = parse_input("fact: (top " + movingDisk + " " + oldPeg + ")")
        
        newOn = parse_input("fact: (on " + movingDisk + " " + newPeg + ")")
        
        newUnderMovingDisk = parse_input("fact: (top ?x " + newPeg + ")")
        newUnderMovingDiskAsk = self.kb.kb_ask(newUnderMovingDisk)

        newDiskUnderMovingDisk = None
        newOrdering = None
        removeEmptyNewPeg = None

        if newUnderMovingDiskAsk:
            newDiskUnderMovingDisk = newUnderMovingDiskAsk.list_of_bindings[0][1][0].statement.terms[0].term.element
            oldTopNewPeg = parse_input("fact: (top " + newDiskUnderMovingDisk + " " + newPeg + ")")
            newOrdering = parse_input("fact: (above " + movingDisk + " " + newDiskUnderMovingDisk + ")")
        else:
            removeEmptyNewPeg = parse_input("fact: (empty " + newPeg + ")")
        
        newTopOldPeg = None
        if oldOrdering:
            newTopOldPeg = parse_input("fact: (top " + oldDiskUnderMovingDisk + " " + oldPeg + ")") 
        else:
            newTopOldPeg = parse_input("fact: (empty " + oldPeg + ")")

        newTopNewPeg = parse_input("fact: (top " + movingDisk + " " + newPeg + ")")
        self.kb.kb_retract(oldOn)
        if oldOrdering:
            self.kb.kb_retract(oldOrdering)

        self.kb.kb_retract(oldTopOldPeg)
        if newUnderMovingDiskAsk:
            self.kb.kb_retract(oldTopNewPeg)

        if removeEmptyNewPeg:
            self.kb.kb_retract(removeEmptyNewPeg)

        self.kb.kb_assert(newOn)
        self.kb.kb_assert(newOrdering)
        self.kb.kb_assert(newTopOldPeg)
        self.kb.kb_assert(newTopNewPeg)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        row1 = ()
        row2 = ()
        row3 = ()
        for currRow in range(1,4):
            for currCol in range(1,4):
                tileFound = False
                for fact in self.kb.facts:
                    if fact.statement.predicate == "located":
                        tile = fact.statement.terms[0].term.element
                        column = fact.statement.terms[1].term.element
                        row = fact.statement.terms[2].term.element

                        tileNumber = int(tile[-1])
                        columnNumber = int(column[-1])
                        rowNumber = int(row[-1])

                        if rowNumber == currRow and columnNumber == currCol:
                            tileFound = True
                            if rowNumber == 1:
                                row1 += tuple([tileNumber])
                            elif rowNumber == 2:
                                row2 += tuple([tileNumber])
                            elif rowNumber == 3:
                                row3 += tuple([tileNumber])
                            
                            break

                if not tileFound:
                    if currRow == 1:
                        row1 += tuple([-1])
                    elif currRow == 2:
                        row2 += tuple([-1])
                    elif currRow == 3:
                        row3 += tuple([-1])


        return (row1, row2, row3)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        movingTile = movable_statement.terms[0].term.element
        oldColumn = movable_statement.terms[1].term.element
        oldRow = movable_statement.terms[2].term.element
        newColumn = movable_statement.terms[3].term.element
        newRow = movable_statement.terms[4].term.element

        empty = parse_input("fact: (empty ?x ?y)")
        emptyFact = self.kb.kb_ask(empty).list_of_bindings[0][1][0]

        oldEmptyColumn = emptyFact.statement.terms[0].term.element #should equal newColumn
        oldEmptyRow = emptyFact.statement.terms[1].term.element #should equal newRow
        newEmptyRow = oldRow
        newEmptyColumn = oldColumn

        oldOn = parse_input("fact: (located " + movingTile + " " + oldColumn + " " + oldRow + ")")
        oldEmpty = parse_input("fact: (empty " + oldEmptyColumn + " " + oldEmptyRow + ")")
        newOn = parse_input("fact: (located " + movingTile + " " + newColumn + " " + newRow + ")")
        newEmpty = parse_input("fact: (empty " + newEmptyColumn + " " + newEmptyRow + ")")
        
        self.kb.kb_retract(oldOn)
        self.kb.kb_retract(oldEmpty)

        self.kb.kb_assert(newOn)
        self.kb.kb_assert(newEmpty)

        #assert all new movable statements
        # for fact in self.kb.facts:
        #     if fact.statement.predicate == "located":
        #         tile = fact.statement.terms[0].term.element
        #         column = fact.statement.terms[1].term.element
        #         row = fact.statement.terms[2].term.element

        #         tileNumber = int(tile[-1])
        #         columnNumber = int(column[-1])
        #         rowNumber = int(row[-1])

        #         if (columnNumber + 1 == newEmptyColumn) or (columnNumber - 1 == newEmptyColumn):
        #             if (rowNumber + 1 == newEmptyRow) or (rowNumber - 1 == newEmptyRow):
        #                 #tile found is adjacent to empty spot so can move there
        #                 newMovable = parse_input("fact: (movable " + tile + " " + columnNumber + " " + rowNumber + " " + newEmptyColumn + " " + newEmptyRow + ")")
        #                 self.kb.kb_assert(newMovable)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
