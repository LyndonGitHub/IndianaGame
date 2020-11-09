import pygame 
from pygame.locals import *
import os
import random
import sys
import math
import time

"""
                        Variables & Constants
"""
WHIPX = 75 # x position for whip
WHIPY = 515 # y position for whip
playerX = 150 # where player stands
playerY = 400 # # player on floor
playerW = 100 # body width 
playerH = 50 # body height
playerhealth=100 # health 
waitTime = 1 # timing for user events
missleX = 1500 # start pos for missile 
score = 0 # game score
coinH = 200 # coin height
outOfScreen = 1500 # start point for projectiles
damage = 10 # health reduction val 

"""
                        Screen Settings and Init
"""
pygame.init() 
screenWidth = 1450 
screenHeight = 550
win = pygame.display.set_mode((screenWidth,screenHeight)) # SCREEM 
pygame.display.set_caption("Mr Jones' Time Travel" ) # TITLE 

"""
                        Sounds & Fonts
"""
# game name for splash screen
gametitle = "Mr Jones' Timetravel"
# sound files 
jumpsound = pygame.mixer.Sound('come_on_lo.wav')
hurtsound = pygame.mixer.Sound('hit sound.wav')
coinsound = pygame.mixer.Sound('smb_coin.wav')
intromusic = 'intro.wav'
mainmusic = 'mario.wav'
overmusic = 'game_over_music.wav'
fonts = {
    
    'font': [pygame.font.SysFont("Algerian",48),
            pygame.font.SysFont("Bradley Hand ITC", 30),
            pygame.font.SysFont("Algerian",22),
            pygame.font.SysFont("Algerian",14)
                ],
}

# fonts
menuFont = fonts['font'][0]
instFont = fonts['font'][1]
scoreFont= fonts['font'][2]
healthFont= fonts['font'][3]

"""
                        Colors
RBG colours
"""
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PALEGREEN = (152, 251, 152, 255)
BISQUE = (238,213,183)
"""
                        Reset Game
Funciton resets variables after user chooses to play game again
"""
def resetGame():
    global bg       
    global thorn_img
    global spike_img
    global static_img
    global playerhealth
    global score

    bg = textures['backgrounds'][0]
    thorn_img = textures['thorn'][0]
    spike_img = textures['spike'][0]
    static_img = textures['static'][0]
    playerhealth=100
    score = 0


"""
                        Textures
stores player, background and object images
"""
textures = {
    'indy': [pygame.image.load(os.path.join('playerImages','run1.png')).convert_alpha(),
              pygame.image.load(os.path.join('playerImages','run1.png')).convert_alpha(),
              pygame.image.load(os.path.join('playerImages','run2.png')).convert_alpha(),
              pygame.image.load(os.path.join('playerImages','run2.png')).convert_alpha(),
             
              ],

    'backgrounds': [pygame.image.load(os.path.join('backgroundImages','junglebg.png')).convert_alpha(),
                    pygame.image.load(os.path.join('backgroundImages','egyptbg.png')).convert_alpha(),
                    pygame.image.load(os.path.join('backgroundImages','fantasybg.png')).convert_alpha(),
                    pygame.image.load(os.path.join('backgroundImages','bkd_tint_2.png')).convert_alpha(),
                    pygame.image.load(os.path.join('backgroundImages','0.arrow_y.png')).convert_alpha(),

                ],

    'spike': [pygame.image.load(os.path.join('objectImages','spikeG.png')).convert_alpha(),
                    pygame.image.load(os.path.join('objectImages','spikeY.png')).convert_alpha(),
                    pygame.image.load(os.path.join('objectImages','spikeP.png')).convert_alpha(),],

    'thorn': [pygame.image.load(os.path.join('objectImages','thornG.png')).convert_alpha(),
                    pygame.image.load(os.path.join('objectImages','thornY.png')).convert_alpha(),
                    pygame.image.load(os.path.join('objectImages','thornP.png')).convert_alpha(),
                ],

    'rewards': [pygame.image.load(os.path.join('objectImages','coin.png')).convert_alpha(),
                ],

    'static': [pygame.image.load(os.path.join('objectImages','staticG.png')).convert_alpha(),
                    pygame.image.load(os.path.join('objectImages','staticY.png')).convert_alpha(),
                    pygame.image.load(os.path.join('objectImages','staticP.png')).convert_alpha(),
                ],
    
     'indyJump': [pygame.image.load(os.path.join('playerImages','jump.png'))],

     'indyHover' : [pygame.image.load(os.path.join('playerImages','hover.png')),
            pygame.image.load(os.path.join('playerImages','whip.png'))],
      
}

bg = textures['backgrounds'][0] # background
thorn_img = textures['thorn'][0] # moving obj 
static_img =  textures['static'][0] # static
spike_img = textures['spike'][0] # bounce
# start menu background images
bkd = textures['backgrounds'][3] # start screen background
arrow =textures['backgrounds'][4] # image for arrow
coin_img = textures['rewards'] [0] # coin 
player_img = textures['indy'] [0] # player image running 


# continously move image 
background1 = 0 # x position of screen
background2 = bg.get_width() 
clock = pygame.time.Clock() # timer 
# storing sprites
all_sprites = pygame.sprite.Group()
movobs=pygame.sprite.Group()
coinobj=pygame.sprite.Group()
bounceobj=pygame.sprite.Group()
statobj=pygame.sprite.Group()




"""    
                        Menus and Splash Screens

"""
# define splash screen function - time limit 3 seconds
def Splash():
    start_time = pygame.time.get_ticks()    
    while pygame.time.get_ticks() < start_time+3000: # wait 3 seconds 
        win.fill(BLACK)        # backgorund
        title = menuFont.render(gametitle, True, BISQUE)
        win.blit(title, (screenWidth/3, screenHeight/3))
        pygame.display.update()
        # set the timer
        clock.tick(3000)
# define instruction screen function:        
def Instruct():    
    while True:              
            win.fill(BISQUE)
            # labels
            win.blit(textures['indyHover'][0],(8*screenWidth/10, screenHeight/3))
            instructions0 = instFont.render('Instructions:', True, BLACK)
            instructions1 = instFont.render('Press                  to jump', True, BLACK)
            instructions2 = instFont.render('... hold [SPACE] to hover !', True, BLACK)
            instructions3 = instFont.render('When ready, hit [ENTER] to begin game ---------------------------------> ', True, BLACK)
            # draw label      
            win.blit(instructions0, (1*screenWidth/10, 2*screenHeight/10))
            win.blit(instructions1, (1*screenWidth/10, 3*screenHeight/10))
            # use arrow icon image
            win.blit(arrow, (2*screenWidth/11,3*screenHeight/10))
            win.blit(instructions2, (1*screenWidth/10, 4*screenHeight/10))
            win.blit(instructions3, (1*screenWidth/10, 5*screenHeight/10)) 
            # if user quits quit game                    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # enter game whenever user is ready
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # play main game music
                        pygame.mixer.music.load(mainmusic)
                        pygame.mixer.music.play(-1)
                        return True
            pygame.display.update()
    
     
# define start screen function
def startScreen():
        # play menu music
        pygame.mixer.music.load(intromusic)
        pygame.mixer.music.play(-1)
        global running
        # set a variable to zero to toggle between options
        point = 0
        running = True
        while True:              
            win.blit(bkd, (0, 0))
            instructions0 = scoreFont.render('Up/Down to select option and hit [ENTER] !', True, WHITE)
            win.blit(instructions0, (1*screenWidth/10, 6*screenHeight/10))
            if point == 0:
                start = menuFont.render('START GAME', True, GREEN)
                quitt =  menuFont.render('QUIT GAME', True, BLACK)
            # select option followed by colour alternation
            elif point == 1:
                start = menuFont.render('START GAME', True, BLACK)
                quitt =  menuFont.render('QUIT GAME', True, GREEN)
            # print two options on screen
            win.blit(start, (screenWidth/10, screenHeight/10))            
            win.blit(quitt, (screenWidth/10, 3*screenHeight/10))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    os._exit(0)
                    quit()
                if event.type == pygame.KEYDOWN:
                    # change class variable from zero to one to change colours
                    if event.key == pygame.K_DOWN:
                        point += 1
                    elif event.key == pygame.K_UP:
                        point -= 1
                    elif event.key == pygame.K_RETURN:
                        if point == 0 :
                                pygame.mixer.music.stop()
                                Instruct() # show instruction screen
                                return True
                        elif point == 1:
                            running = False
                            pygame.quit()
                            os._exit(0)
                            quit()                
            pygame.display.update()

"""
                    Reading High Score
reads int from file to save highest score
"""
# functions for end of game & scoring
def updateFile():
    f = open('scores.txt','r') # open file
    file = f.readlines()
    last = int(file[0]) # take single int in file
    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()
        return score              
    return last

# end of game function - time limit 5 seconds
def GameOver():
    start_time = pygame.time.get_ticks()  
    pygame.mixer.music.load(overmusic)
    pygame.mixer.music.play(-1)
    while pygame.time.get_ticks() < start_time+5000:
        win.fill(BISQUE)      
        title = menuFont.render("Game Over...", True, BLACK)
        scoring = menuFont.render("Your Score : " + str(score), True, BLACK)
        highScore = menuFont.render("High Score: " + str(updateFile()), True, BLACK)
        win.blit(title, (screenWidth//3, screenHeight//2))
        win.blit(highScore, (screenWidth//3, screenHeight//3))
        # added current highscore
        win.blit(scoring, (screenWidth//3, screenHeight//4))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    os._exit(0)
                    quit()
        pygame.display.update()
        clock.tick(5000)

    resetGame() # reset values
    startScreen()# play start menu

def mainMusic():
    pygame.mixer.music.load(mainmusic)
    pygame.mixer.music.play(-1)

"""

                        Redraw window
function redraws window on each while True loop call
"""
def redrawWindow():
    x = random.randint(1, 10) # randomise calls for objects
    y = random.randint(1, 10) # randomise calls for objects
    win.blit(bg, (background1, 0))  # draws our first bg image
    win.blit(bg, (background2, 0))  # draws the second bg image
    runner.draw(win) # draw player
    all_sprites.draw(win) # draw sprites
    scoretext=scoreFont.render("Score: {0}".format(score),1,BLACK) # update score
    scoretextRect= scoretext.get_rect() 
    scoretextRect.center = (90,70) # score position 
    win.blit(scoretext,scoretextRect)
    healthbar(playerhealth)
    all_sprites.update()
    pygame.display.update() # update screen


"""
                        Runtime Events
"""
pygame.time.set_timer(USEREVENT+waitTime, 2000)# MAKE BG GO FASTER
running = True# call event and increase speed every half second 
speed = 50 # init game speed

"""
                        Player Setup
"""
class player(object):

    jumpList = [20,20,20,20,20] # sequence for player jump
# -1,-3,-5,-7,-9,-11,-13,-15,-17,-19,-20
    fallList =  [-30,-30,-30,-30,-30] # player fall sequence

    def __init__(self,x,y, width, height):
        
        # position
        self.x = x # player x pos
        self.y = y # player y pos 
        self.w = width # player width
        self.h = height # player height
        # Player hovering variabels 
        self.hover = False
        self.hoverCount = 0
        # Player Jump Variables
        self.jumping = False 
        self.jumpCount = 0
        self.switchAnimiation = 0 # run counter 
        self.jumpSequence = len(self.jumpList) # counter for jump
        # for collition, get player rect for position
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # fall sequence
        self.fallCount = 0
        self.falling = False
        self.fallSequence = len(self.fallList)
        
# function draws player on surface provided
    def draw(self, win):
        # if player is jumping 
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 2# decrement player y
            win.blit(textures['indyJump'][0],(self.x,self.y))
            self.jumpCount += 1 # switch image
            # checking jump sequence index isn't too great
            if self.jumpCount >= self.jumpSequence: # jump sequence 
                self.falling = True 
                self.jumpCount = 0 
                self.jumping = False
                self.runCount = 0
        # player hover
        elif self.hover:
            self.y = self.y # keep y pos
            win.blit(textures['indyHover'][0],(self.x,self.y)) # draw
            win.blit(textures['indyHover'][1],(self.x+WHIPX,self.y-WHIPY)) # draw
            self.hoverCount += 1
            # jump release
            if self.hoverCount > 1:
                self.falling = True
                self.hover = False
                self.hoverCount= 0
            # else:
            #     self.falling = True

        # player fall 
        elif self.falling:
            self.y -= self.fallList[self.fallCount] # decrement player y
            win.blit(textures['indyHover'][0],(self.x,self.y)) # draw
            self.fallCount += 1
            if self.fallCount >= self.fallSequence: # greater than array index
                self.falling = True
                self.fallCount = 0
            # player hits ground 
            if self.y >= playerY:
                self.fallCount = 0
                self.y = playerY
                self.falling = False
                 
            if self.falling:
                self.jumping = False
                self.hover = False
                self.hoverCount = 0

        else:
            self.y = playerY
            # player running
            if self.switchAnimiation > 3:  # switch between animation sequence
                    self.switchAnimiation = 0
            win.blit(textures['indy'][self.switchAnimiation],(self.x,self.y)) # draw
            self.switchAnimiation += 1
        self.rect.x = self.x # update rect for position
        self.rect.y = self.y# update rect for position

"""
                        Projectiles
"""
#class for moving obstacles
class MovingObs(pygame.sprite.Sprite):
    #functions draw thorn projectiles on screen and make them move
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = thorn_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        #self.rect.bottom = HEIGHT - 50
        self.rect.y =  playerY
        self.rect.x = missleX
        self.speedx = random.randrange(5, 30)
        
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
           self.rect.x = missleX
           self.rect.y = random.randrange(150, 300)
           self.speedx = random.randrange(5, 30)
           pygame.display.update()


"""
                    Coins
"""
#class for poweups
class Coins(pygame.sprite.Sprite):
    #funtions to display and place the powerups on screen
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
       
        self.score=0
        self.image = coin_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = coinH
        self.rect.x = outOfScreen
        self.speedx = 10
     
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
           self.rect.x = outOfScreen
        #    self.rect.y= 300
        #    self.speedx = 10
        #    pygame.display.update()

"""
                    Static Object
"""
#class for static obstacles
class StatObs(pygame.sprite.Sprite):
    #function to display and place the obstacles on screen
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = static_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y=  450
        self.rect.x = outOfScreen
        self.speedx = 10
       
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
           self.rect.x = outOfScreen
           self.rect.y = 450
        #    self.speedx = 10
           pygame.display.update()

"""
                    Bounce
"""
#class for bouncing obstacles
class Bounce(pygame.sprite.Sprite):
    #function to display and make the objects bounce on screen
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = spike_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = 300
        self.rect.x = outOfScreen
        self.vx = -10
        self.vy = -5

    def update(self):
        newX=self.rect.x+self.vx 
        newY=self.rect.y+self.vy
       #limiting the traversal path
        if newY<0 or newY>450:
            self.vy=-self.vy
        else:
            self.rect.x=newX
            self.rect.y=newY
            pygame.display.update()

"""
                    health
function to display the health bar and health percentage on screen
Bar colour changes based on player health
also prints health in digit form to screen 
"""
def healthbar(playerhealth):
    if playerhealth>75:
        ph_color=GREEN
    elif playerhealth>50:
        ph_color=YELLOW
    else:
        ph_color=RED
    pygame.draw.rect(win, ph_color, (35, 30, playerhealth, 25))
    health=healthFont.render(str(playerhealth)+'%',True,BLACK)
    win.blit(health,(65,35)) # position 

"""
                        Deploy obstacles
Uses random ints to choose which obstalces to send and how many times
Makes all objects fairly probably at coming
"""
def deploy(x,y):
    if x == 1:
        # range for number of items to add to sprite group 
        for i in range(1,2):
            m = MovingObs()
            all_sprites.add(m)
            movobs.add(m)
    if x == 2:
        for i in range(5,10):
            b = Bounce()
            all_sprites.add(b)
            bounceobj.add(b)

    if x == 3:
        for i in range(1,2):
            s = StatObs()
            all_sprites.add(s)
            statobj.add(s)
    if y == 10 or y == 1:
        c = Coins()
        all_sprites.add(c)
        coinobj.add(c)

"""
                    Change World
function changes game setting for stage
changes images and spirtes and object speeds
"""
def changeWorld(x,val):
    # x is change, val is which level to change to 
    if x == True:
        global bg    
        global thorn_img
        global spike_img
        global static_img
        global speed
        bg = textures['backgrounds'][val]
        thorn_img = textures['thorn'][val]
        spike_img = textures['spike'][val]
        static_img = textures['static'][val]
        statiClass.speedx += 10
        bounceClass.vx -=5
        thornsClass.speedx += 10


"""
                    Run Game
"""
Splash() # splash screen with game title
startScreen() # start menu 

# change speed for each class when level changes
thornsClass = MovingObs()
bounceClass = Bounce()
statiClass = StatObs()

runner = player(playerX,playerY,playerW,playerH) # init player

while running: 
    redrawWindow()
    x = random.randint(1, 10) # rand ints for selecting objects
    y = random.randint(1, 10) # rand ints for selecting objects
    clock.tick(speed)
    background1 -= 3 # move background by x 
    background2 -= 3 # move background by x
###############################################################
#                       Collision Dection                     #
###############################################################
    hits = pygame.sprite.spritecollide(runner, movobs, True) # collide with thorns
    collect= pygame.sprite.spritecollide(runner, coinobj, True) # collide with coins
    bouncehit= pygame.sprite.spritecollide(runner, bounceobj, True) # collide with bouncing 
    stathit= pygame.sprite.spritecollide(runner, statobj, True) # collide with static object
# if checks if collision is made
# play sound and adjust variables 
    if hits:
        hurtsound.play()
        playerhealth=playerhealth-damage

    if collect:
        # play coin sound
        coinsound.play()
        score += 5

    if bouncehit:
        hurtsound.play()
        playerhealth=playerhealth-damage
        
    if stathit:
        hurtsound.play()
        playerhealth=playerhealth-damage
    # player dead
    if playerhealth==0:
        running = False
        GameOver()

###############################################################
#                       Background                            #
###############################################################
    # moves background until background is off the screen
    if background1 < bg.get_width() * -1:  # If our bg is at the -width then reset its position
        background1 = bg.get_width()
    
    if background2 < bg.get_width() * -1:
        background2 = bg.get_width()
    # send projectiles 
    for event in pygame.event.get():
        # triggered by userevent
        if event.type == USEREVENT+waitTime:
            deploy(x,y)

        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):  # See if the user clicks the red x 
            running = False    # End the loop
            pygame.quit()  # Quit the game
            os._exit(0)
            quit()

###############################################################
#                       Controls                              #
###############################################################
    # checks only one is pressed
    keys = pygame.key.get_pressed()
    # jump mechanims
    if keys[pygame.K_UP]:
        # only jump is not jumped and player is on ground 
        if not(runner.jumping) and  runner.y == playerY :
            # play jump sound
            jumpsound.play()
            runner.jumping = True

    # hover using space
    if keys[pygame.K_SPACE]:
        # # if in air or falling to ground
        if runner.jumping or runner.falling:

            runner.hover = True
    # cahnge to jungle world
    if score == 15:
        changeWorld(True,1)
    # cahnge to fantasy
    if score == 30:
        changeWorld(True,2)
    
    pygame.display.flip()
    clock.tick(speed)