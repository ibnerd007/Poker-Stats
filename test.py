# side-scroller-demo.py

from tkinter import *

def init(data):
    data.scrollX = 0  # amount view is scrolled to the right
    data.scrollMargin = 50 # closest player may come to either canvas edge
    data.playerX = data.scrollMargin # player's left edge
    data.playerY = 0  # player's bottom edge (distance above the base line)
    data.playerWidth = 10
    data.playerHeight = 20
    data.walls = 5
    data.wallPoints = [0]*data.walls
    data.wallWidth = 20
    data.wallHeight = 40
    data.wallSpacing = 90 # wall left edges are at 90, 180, 270,...
    data.currentWallHit = -1 # start out not hitting a wall

def getPlayerBounds(data):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = (data.playerX, data.height/2 - data.playerY)
    (x1, y0) = (x0 + data.playerWidth, y1 - data.playerHeight)
    return (x0, y0, x1, y1)

def getWallBounds(wall, data):
    # returns absolute bounds, not taking scrollX into account
    (x0, y1) = ((1+wall) * data.wallSpacing, data.height/2)
    (x1, y0) = (x0 + data.wallWidth, y1 - data.wallHeight)
    return (x0, y0, x1, y1)

def getWallHit(data):
    # return wall that player is currently hitting
    # note: this should be optimized to only check the walls that are visible
    # or even just directly compute the wall without a loop
    playerBounds = getPlayerBounds(data)
    for wall in range(data.walls):
        wallBounds = getWallBounds(wall, data)
        if (boundsIntersect(playerBounds, wallBounds) == True):
            return wall
    return -1

def boundsIntersect(boundsA, boundsB):
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

def movePlayer(dx, dy, data):
    data.playerX += dx
    data.playerY += dy
    # scroll to make player visible as needed
    if (data.playerX < data.scrollX + data.scrollMargin):
        data.scrollX = data.playerX - data.scrollMargin
    if (data.playerX > data.scrollX + data.width - data.scrollMargin):
        data.scrollX = data.playerX - data.width + data.scrollMargin
    # and check for a new wall hit
    wall = getWallHit(data)
    if (wall != data.currentWallHit):
        data.currentWallHit = wall
        if (wall >= 0):
            data.wallPoints[wall] += 1

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if (event.keysym == "Left"):    movePlayer(-5, 0, data)
    elif (event.keysym == "Right"): movePlayer(+5, 0, data)
    elif (event.keysym == "Up"):    movePlayer(0, +5, data)
    elif (event.keysym == "Down"):  movePlayer(0, -5, data)

def timerFired(data):
    pass

def redrawAll(canvas, data):
    # draw the base line
    lineY = data.height/2
    lineHeight = 5
    canvas.create_rectangle(0, lineY, data.width, lineY+lineHeight,fill="black")

    # draw the walls
    # (Note: should optimize to only consider walls that can be visible now!)
    sx = data.scrollX
    for wall in range(data.walls):
        (x0, y0, x1, y1) = getWallBounds(wall, data)
        fill = "orange" if (wall == data.currentWallHit) else "pink"
        canvas.create_rectangle(x0-sx, y0, x1-sx, y1, fill=fill)
        (cx, cy) = ((x0+x1)/2 - sx, (y0 + y1)/2)
        canvas.create_text(cx, cy, text=str(data.wallPoints[wall]))
        cy = lineY + 5
        canvas.create_text(cx, cy, text=str(wall), anchor=N)

    # draw the player
    (x0, y0, x1, y1) = getPlayerBounds(data)
    canvas.create_oval(x0 - sx, y0, x1 - sx, y1, fill="cyan")

    # draw the instructions
    msg = "Use arrows to move, hit walls to score"
    canvas.create_text(data.width/2, 20, text=msg)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run()