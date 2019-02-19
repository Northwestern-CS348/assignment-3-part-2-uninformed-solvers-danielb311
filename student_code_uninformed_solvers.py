from solver import *

class Queue:
    def __init__(self, initialContents = []):
        self.theQueue = initialContents[:]

    def __str__(self):
        return "The queue contains: " + str(self.theQueue)

    def isEmpty(self):
        return len(self.theQueue) == 0

    def push(self, elt):
        self.theQueue.append(elt)

    def pop(self):
        x = self.theQueue[0]
        del self.theQueue[0]
        return x

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.gm.getGameState() == self.victoryCondition:
            return True
            
        possibleMoves = self.gm.getMovables()

        if len(possibleMoves) == 0:
            self.currentState = self.currentState.parent
            self.solveOneStep()
        else:
            allMovesVisited = True
            for move in possibleMoves:
                self.gm.makeMove(move)

                currentGameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)

                if not self.visited.get(currentGameState, False):
                    if not currentGameState in self.currentState.children:
                        self.currentState.children.append(currentGameState)
                        currentGameState.parent = self.currentState

                self.gm.reverseMove(move)

            for child in self.currentState.children:
                move = child.requiredMovable
                self.gm.makeMove(move)

                if self.visited.get(child, False):
                    self.gm.reverseMove(move)
                    continue

                self.visited[child] = True
                self.currentState = child
                allMovesVisited = False
                break;

            if allMovesVisited:
                self.currentState = self.currentState.parent
                self.solveOneStep()
        
        if self.gm.getGameState() == self.victoryCondition:
            return True

        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = Queue()

    def getToTopOfTree(self):
        while True:
            if not self.currentState.parent:
                return
            
            lastMoveDone = self.currentState.requiredMovable
            self.gm.reverseMove(lastMoveDone)
            self.currentState = self.currentState.parent

    def findGameStateInTree(self, nextGameState):
        #go up the tree
        self.getToTopOfTree()
        
        #go down the tree
        while nextGameState.depth != self.currentState.depth:
            movableNodeThroughTheTree = nextGameState

            #move the movableNodeThroughTheTree up to one level below the currentState
            #then, guide currentState down to movableNodeThroughTheTree using the correct child
            while (self.currentState.depth + 1) != movableNodeThroughTheTree.depth:
                movableNodeThroughTheTree = movableNodeThroughTheTree.parent

            for child in self.currentState.children:
                if child.requiredMovable == movableNodeThroughTheTree.requiredMovable:
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child
                    break

        return

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        if self.queue.isEmpty():
            possibleMoves = self.gm.getMovables()
            for move in possibleMoves:
                self.gm.makeMove(move)
                currentGameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)

                if not self.visited.get(currentGameState, False):
                    if not currentGameState in self.currentState.children:
                        self.currentState.children.append(currentGameState)
                        currentGameState.parent = self.currentState
                        self.visited[currentGameState] = True
                        self.queue.push(currentGameState)

                self.gm.reverseMove(move)
        
        nextGameState = self.queue.pop()
        
        ###need to change self.gm so that it matches what I just popped from the queue
        self.findGameStateInTree(nextGameState)

        if self.gm.getGameState() == self.victoryCondition:
            return True

        possibleMoves = self.gm.getMovables()

        for move in possibleMoves:
            self.gm.makeMove(move)
            currentGameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)

            if not self.visited.get(currentGameState, False):
                if not currentGameState in self.currentState.children:
                    self.currentState.children.append(currentGameState)
                    currentGameState.parent = self.currentState
                    
                    self.visited[currentGameState] = True
                    self.queue.push(currentGameState)
                    
            self.gm.reverseMove(move)