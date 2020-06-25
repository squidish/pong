import pygame
import pandas as pd
import sys
import getopt

#Draw the main scenario
WIDTH = 1200
HEIGHT = 600
BORDER = 20 
VELOCITY = 1

#Objects
class Ball: 
    
    RADIUS = 10

    def __init__(self,x,y,vx,vy):
       self.x = x
       self.y = y
       self.vx = vx
       self.vy = vy

    def show(self,colour):
           global screen
           pygame.draw.circle(screen,colour, (self.x,self.y), self.RADIUS)

    def update(self, paddle):
         global bgColor, fgColour

         newx = self.x + self.vx
         newy = self.y + self.vy
     
         if newx < BORDER +self.RADIUS:
              self.vx = -self.vx
         elif newy < BORDER+self.RADIUS or newy > HEIGHT-BORDER-self.RADIUS:
              self.vy = -self.vy
         elif newx == WIDTH-paddle.WIDTH and (newy <= paddle.y + (paddle.HEIGHT/2)) and (newy >= paddle.y - (paddle.HEIGHT/2)) : 
              self.vx = -self.vx
         else:
           self.show(bgColour)
           self.x = self.x + self.vx
           self.y = self.y + self.vy
           self.show(fgColour)

class Paddle:
      
   WIDTH = 20
   HEIGHT = 100

   def __init__(self,y):
      self.y = y

   def show(self,colour):
      global screen
      pygame.draw.rect(screen,colour, pygame.Rect((WIDTH-self.WIDTH,self.y-(self.HEIGHT/2)),(self.WIDTH,self.HEIGHT)))

   def update(self,NewY):
      self.show(pygame.Color("black"))
      self.y = NewY
      self.show(pygame.Color("white"))

   def update_manual(self):
      self.show(pygame.Color("black"))
      self.y = pygame.mouse.get_pos()[1]
      self.show(pygame.Color("white"))

#------------------MAIN SCRIPT BEGINS HERE--------------------------------------------

try:
  opts, args = getopt.getopt(sys.argv[1:], "",["ai","record"])
except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

auto = False
record = False
for o, a in opts:
    if(o == "--ai"):
      auto = True
    if(o == "--record"):
      record = True

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#create initial setup
ballplay  = Ball(40,HEIGHT//2,-VELOCITY,VELOCITY)
paddleplay = Paddle(400)

#draw the scenario
fgColour = pygame.Color("white")
bgColour = pygame.Color("black")
pygame.draw.rect(screen,fgColour, pygame.Rect((0,0),(WIDTH,BORDER)))
pygame.draw.rect(screen,fgColour, pygame.Rect(0,0,BORDER,HEIGHT))
pygame.draw.rect(screen,fgColour, pygame.Rect(0,HEIGHT-BORDER,WIDTH,BORDER))

ballplay.show(fgColour)
paddleplay.show(fgColour)


if(record and auto):
   sample = open("game_ai.csv","w")
   sample.write("x,y,vx,vy,paddle.y \n")
elif(record and not auto):
   sample = open("game.csv","w")
   sample.write("x,y,vx,vy,paddle.y \n")


if(auto):
   pong = pd.read_csv("game.csv")
   pong = pong.drop_duplicates()
   X = pong.drop(columns = ['paddle'])
   y = pong['paddle']
   from sklearn.neighbors import KNeighborsRegressor
   clf = KNeighborsRegressor(n_neighbors=3)
   clf = clf.fit(X,y)
   df = pd.DataFrame(columns = ['x','y','vx','vy'])


#main game loop
while True:
   e = pygame.event.poll()
   if e.type == pygame.QUIT or ballplay.x > WIDTH:
      break
   pygame.display.flip()
   if (auto): 
      toPredict = df.append({'x' : ballplay.x , 'y' : ballplay.y, 'vx' : ballplay.vx , 'vy' : ballplay.vy }, ignore_index = True)
      shouldMove = clf.predict(toPredict)
      paddleplay.update(shouldMove)
   else:
      paddleplay.update_manual()
   #paddleplay.update_manual()
   ballplay.update(paddleplay)
   if (record):
      sample.write(str(ballplay.x) + "," + str(ballplay.y) + "," +str(ballplay.vx) + "," + str(ballplay.vy) + "," + str(paddleplay.y) + "\n")

#if leave the main game loop then...
pygame.quit()
