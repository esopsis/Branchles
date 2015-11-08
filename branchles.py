import pygame, sys
from pygame.locals import *
pygame.init()

""" branchles.py
by Eric J.Parfitt (ejparfitt@gmail.com)

This program starts with a set of twigs, and draws branches from the tips
of twigs going aroind the "tree" clockwise.  If a branch would collide
with another branch, both branches on that node are not added.

Version: 1.0 alpha
"""

WIDTH = 700
HEIGHT = 800
FPS = 4

windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

branchLength = 10
directionNum = 6
newBranches = []

clock = pygame.time.Clock()

class Branch:
    """Creates a branch object.
   
    Keyword arguments:
    xCo -- the x coordinate of a branch's origin
    yCo -- the y coordinate of a branch's origin
    direction -- the direction of a branch, can be between 0 and 5
    budX -- the x coordinate of a branch's tip, or bud
    budY -- the y coordinate of a branch's tip, or bud
   
    """
    
    def __init__(self, myXCo, myYCo, myDirection):
        self.xCo = myXCo
        self.yCo = myYCo
        self.direction = myDirection
        self.budX = self.findBudX()
        self.budY = self.findBudY()
        
    def findBudX(self):
        directionsX = {0 : 0, 1 : 1, 2 : 1, 3 : 0, 4 : -1, 5 : -1}
        return self.xCo + directionsX[self.direction]
    
    def findBudY(self):
        directionsY = {0 : 1, 1 : 1, 2 : -1, 3 : -1, 4 : -1, 5 : 1}
        return self.yCo + directionsY[self.direction]
    
    def draw(self, color):
        pygame.draw.line(windowSurface, color, 
                [self.xCo * branchLength + WIDTH / 2, 
                self.yCo * branchLength + HEIGHT / 2], 
                [self.budX * branchLength + WIDTH / 2, 
                self.budY * branchLength + HEIGHT / 2])
        pygame.display.flip()

def incBranch(direction):
    if(direction + 1 < directionNum):
        return direction + 1
    return 0

def decBranch(direction):
    if(direction >= 1):
        return direction - 1
    return directionNum - 1

# sets up initial branches
oldBranches = [Branch(0, 1, 3), Branch(0, 0, 0)]

windowSurface.fill(WHITE)
allBranches = []
allBranches.extend(oldBranches)
for branch in oldBranches:
    branch.draw(BLACK)
pygame.display.flip()

def sprout():
    """Create new branches at the tips of the last generation of branches."""
    global newBranches
    global oldBranches
    global allBranches
    newBranches = []
    for branch in oldBranches:
        branchA = Branch(branch.budX, 
                branch.budY,incBranch(branch.direction))
        branchB = Branch(branch.budX, branch.budY,
                decBranch(branch.direction))
        for branch2 in allBranches:
            if ((branchA.budX == branch2.budX and branchA.budY == branch2.budY)
                    or (branchB.budX == branch2.budX and
                    branchB.budY == branch2.budY)):
                break
        
        else:
            clock.tick(FPS)
            branchA.draw(BLACK)
            checkQuit()
            clock.tick(FPS)
            branchB.draw(BLACK)
            allBranches.extend([branchA, branchB])
            newBranches.extend([branchA, branchB])
    oldBranches = []
    oldBranches.extend(newBranches)

def checkQuit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
   
while(True):
    sprout()
    checkQuit()
