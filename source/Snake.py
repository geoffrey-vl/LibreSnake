#instal in /usr/lib/libreoffice/share/Scripts/python if not embedded

import uno
import random
from com.sun.star.beans import PropertyValue
from com.sun.star.awt.MessageBoxType import MESSAGEBOX, INFOBOX, WARNINGBOX, ERRORBOX, QUERYBOX
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK, BUTTONS_OK_CANCEL, BUTTONS_YES_NO, BUTTONS_YES_NO_CANCEL, BUTTONS_RETRY_CANCEL, BUTTONS_ABORT_IGNORE_RETRY
from com.sun.star.awt.MessageBoxResults import OK, YES, NO, CANCEL, RETRY
from threading import Thread
from time import sleep

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


model = XSCRIPTCONTEXT.getDocument()
sheet = model.Sheets.getByIndex(0)
parentwin = model.CurrentController.Frame.ContainerWindow

def PaintCell(coordX=0, coordY=0, color="000000"):
    # The context variable is of type XScriptContext and is available to
    # all BeanShell scripts executed by the Script Framework
    cell = sheet.getCellByPosition(coordX, coordY)
    cell.CellBackColor = int(color, 16)

def PaintCells(coordXMin=0, coordYMin=0, coordXMax=0, coordYMax=0, color="000000"):
    # The context variable is of type XScriptContext and is available to
    # all BeanShell scripts executed by the Script Framework
    cells = sheet.getCellRangeByPosition(coordXMin, coordYMin, coordXMax, coordYMax)
    cells.CellBackColor = int(color, 16)

def InitWorld():
    PaintCells(0, 0, 64, 0, "000000")
    PaintCells(0, 32, 64, 32, "000000")
    PaintCells(0, 1, 0, 31, "000000")
    PaintCells(64, 1, 64, 31, "000000")
    PaintCells(1, 1, 63, 31, "FFFFFF")

def EndGame(msg="Score: 0! Retry?"):
    box = parentwin.getToolkit().createMessageBox(parentwin, MESSAGEBOX, BUTTONS_RETRY_CANCEL, "GameOver", msg)
    return box.execute()

def Loop(*args):
    while True:
        InitWorld()
        snakePoints = [Point(25,12)]
        targetPoint = Point(random.randint(1, 63), random.randint(1, 31))
        gamespeed = 0.25
        targetsEaten = 0

        direction = "RIGHT"

        PaintCell(snakePoints[0].x, snakePoints[0].y, "000000")
        PaintCell(targetPoint.x, targetPoint.y, "FF00FF")
        sleep(gamespeed)

        #the looping funtion
        while True:
            #cache current pos
            newHead = Point(snakePoints[0].x, snakePoints[0].y)

            #get keystroke
            key = model.getCurrentSelection().getString()
            
            #only change direction upon valid keystroke
            if key == "UP" and direction != "DOWN":
                direction = "UP"
            elif key == "DOWN" and direction != "UP":
                direction = "DOWN"
            elif key == "LEFT" and direction != "RIGHT":
                direction = "LEFT"
            elif key == "RIGHT" and direction != "LEFT":
                direction = "RIGHT"

            #change pos according to direction
            if direction == "UP":
                newHead.y-=1
            elif direction == "DOWN":
                newHead.y+=1
            elif direction == "LEFT":
                newHead.x-=1
            elif direction == "RIGHT":
                newHead.x+=1

            #check if we just ate a target
            if newHead.x==targetPoint.x and newHead.y==targetPoint.y:
                targetsEaten+=1
                #generate new location for target
                while True:
                    targetPoint = Point(random.randint(1, 63), random.randint(1, 31))
                    isGoodToUse = True
                    for snakePoint in snakePoints:
                        if targetPoint.x==snakePoint.x and targetPoint.y==snakePoint.y:
                            isGoodToUse = False
                            break
                    if isGoodToUse:
                        break

                PaintCell(targetPoint.x, targetPoint.y, "FF00FF")
            else:
                #remove previous location
                pointToBlank = snakePoints.pop()
                PaintCell(pointToBlank.x, pointToBlank.y, "FFFFFF")
                del pointToBlank

            #check crash into walls
            if newHead.x<=0 or newHead.y<=0 or newHead.x>=64 or newHead.y>=32:
                PaintCell(newHead.x, newHead.y, "FF0000")
                break
            
            #check if crash into ourselves
            detectedCrash = False
            for snakePoint in snakePoints:
                if newHead.x==snakePoint.x and newHead.y==snakePoint.y:
                    detectedCrash = True
                    break
            if detectedCrash:
                PaintCell(newHead.x, newHead.y, "FF0000")
                break
            
            snakePoints.insert(0, newHead)
            PaintCell(newHead.x, newHead.y, "000000")
            sleep(gamespeed)
        result = EndGame("Score: " + str(targetsEaten) + "!")
        if result != RETRY:
            break
    InitWorld()

def StartEngine(*args):
    thread = Thread(target = Loop)
    thread.start()
    #thread.join()