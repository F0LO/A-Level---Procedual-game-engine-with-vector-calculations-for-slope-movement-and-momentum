#By mark fisk, written in OOP and some procedual.
#Trello(to do list)link -> https://trello.com/b/HY7PTQrJ/going-the-distance-cs
import pygame,sys
import random
from math import sqrt
from pygame.locals import *
import multiprocessing
#Gotta love those imports yanno
#setting up color variables (colours tho cos im british :P )
ORANGE=pygame.color.THECOLORS["orange"]
GREY=pygame.color.THECOLORS["grey"]
CLOCK=pygame.time.Clock()#game speed
SCREEN_WIDTH=1200
SCREEN_HEIGHT=600

import tkinter as tk
from tkinter.ttk import *
import time
#from PIL import ImageTK,Image

def Main_Menu():
#tkinter stuff
    menu = tk.Tk()
    menu.title("Going the Distance")
    menu.geometry("800x500")

    #background stuff
    backgroundIMG = tk.PhotoImage(file = "Menu Art.png")
    Lbackground = tk.Label(menu, image = backgroundIMG)
    Lbackground.place(x=0, y=0, relwidth = 1, relheight=1)

    #events
    def close_program():
        menu.destroy()

    def controls_window():
        Controls = tk.Toplevel(menu)
        Controls.title("Controls")
        Controls.geometry("500x500")
        ControlsIMG = tk.PhotoImage(file = "Control Scheme.png")
        LControls = tk.Label(Controls, image = ControlsIMG)
        LControls.place(x=0, y=0, relwidth = 1, relheight=1)
        Controls.mainloop()

    def Start_Game():
        t1 = time.perf_counter()
        main()#game loop thing
        t2 = time.perf_counter()
        print("That Track Took: ",t2-t1)
        pass

    #Buttons
    Bstart_game = tk.Button(menu, text = "Start Game", width = 25 , height = 5, command = Start_Game)
    Bstart_game.grid(row = 0, column = 1, padx = 10, pady = 10)

    Bcontrols = tk.Button(menu, text = "Controls", width = 25, height = 5, command = controls_window)
    Bcontrols.grid(row = 1, column = 1, padx = 10, pady = 10)

    Bleaderboard = tk.Button(menu, text = "Leaderboard", width = 25, height = 5)
    Bleaderboard.grid(row = 2, column = 1, padx = 10, pady = 10)

    Bquit = tk.Button(menu, text = "Quit", width = 25, height = 5, command = close_program)
    Bquit.grid(row = 3, column = 1, padx = 10, pady = 10)

    menu.mainloop() 


def collide(point,rect):
    collided=0
    if point[0]>=rect[0] and point[0]<rect[0]+rect[2] and point[1]>=rect[1] and point[1]<rect[1]+rect[3]:
        #check if rectangles gonna overlap
        collided=1
    return collided

#looked at C# unity game engine for 2d platformers, IDA disassembler & resource extractors kinda nice for disassembling game files :)  
def rect_collision(rect1,rect2):
    collision=0
    point1=(rect1[0],rect1[1])
    point2=(rect1[0]+rect1[2],rect1[1])#treat everything like a rectangle
    point3=(rect1[0],rect1[1]+rect1[3])
    point4=(rect1[0]+rect1[2],rect1[1]+rect1[3]) 
    if collide(point1,rect2) or collide(point2,rect2) \
    or collide(point3,rect2) or collide(point4,rect2):
       collision=1
    return collision


def Slope_Manager(slope,player):
    desired_y_pos=player.pos[1]
    increment=slope.increment
    print(slope.pos[1])
    
    if slope.slant>0: #slope going up
       if player.pos[0]+player.width<=slope.end[0]+1:
          y_offset=((player.pos[0]+player.width)-slope.start[0])*increment
          top=slope.start[1]+y_offset
          if player.pos[1]+player.height>=top:
             print(desired_y_pos) 
             desired_y_pos=top-player.height
             player.velocity[1]=0
             player.on_ground=True
             player.on_slope=True
             if player.right and player.velocity[0]<10: 
                player.on_slope=False
             player.vector[0]=slope.vector[0] #this block is why i hate vectors sooo much
             player.vector[1]=slope.vector[1]
       elif player.pos[0]<=slope.pos[0]+slope.width \
       and player.pos[1]+player.height-player.velocity[1]<=slope.end[1] \
       or  player.pos[0]<=slope.pos[0]+slope.width and player.velocity[0]>=0:
           if player.pos[1]+player.height>=slope.end[1]:
              desired_y_pos=slope.end[1]-player.height
              player.velocity[1]=0
              player.on_ground=True
              player.on_slope=True
              player.vector[0]=slope.vector[0]
              player.vector[1]=0 
              if player.left:
                 player.vector[1]=slope.vector[1]
       else:
          player.pos[0]=slope.pos[0]+slope.width

          
    elif slope.slant<0: #slope going down
       if player.pos[0]>=slope.start[0]:
          y_offset=(player.pos[0]-slope.start[0])*increment
          top=slope.start[1]+y_offset
          if player.pos[1]+player.height>=top:
             desired_y_pos=top-player.height
             player.velocity[1]=0
             player.on_ground=True
             player.on_slope=True
             if player.left and player.velocity[0]>-10:
                player.on_slope=False           
             player.vector[0]=slope.vector[0]
             player.vector[1]=slope.vector[1]             
       elif player.pos[0]<=slope.start[0] \
       and player.pos[1]+player.height-player.velocity[1]<=slope.start[1] \
       or player.pos[0]<=slope.start[0]and player.velocity[0]<=0:
          if player.pos[1]+player.height>=slope.start[1]:
             desired_y_pos=slope.start[1]-player.height
             player.velocity[1]=0
             player.on_ground=True
             player.on_slope=True
             player.vector[0]=slope.vector[0]
             player.vector[1]=0 
             if player.right:
                player.vector[1]=slope.vector[1]
       else:
          player.pos[0]=slope.pos[0]-player.width

    return desired_y_pos

def slope_respond(slope,player):
    #range of angle from 45 to -45
    top = None
    desired_y_pos=player.pos[1]
    if slope.slant < 0:
        if player.pos[0]>=slope.pos[0]:
            x = player.pos[0] - slope.pos[0]
            top = slope.pos[1]+x-1
    if slope.slant > 0:
        if player.pos[0]+player.width<=(slope.pos[0]+slope.width):
            x = (slope.pos[0]+slope.width) - ( player.pos[0]+player.width)  #sort this as approaching a negative slope teleports to the top 
            top = slope.pos[1]+x-1
    if top:
        if player.pos[1]+player.height > top:
           desired_y_pos=top-player.height
    return desired_y_pos


   
class Tile:

  def __init__(self,pos):
      self.pos=pos
      self.image=pygame.Surface((200,50)).convert()
      self.image.fill(GREY)
      self.width=self.image.get_width()
      self.height=self.image.get_height()
      self.rect=[self.pos[0],self.pos[1],self.width,self.height]
      pygame.draw.rect(self.image,ORANGE,[0,0,self.width, self.height],4)# for the aesthetic
      
  def draw(self,surface,camera):
      #blit only if we are on screen
      if self.pos[0]+self.width>=camera.screen.left and self.pos[0]<=camera.screen.right  \
      and self.pos[1]+self.height>=camera.screen.top and self.pos[1]<=camera.screen.bottom:
          
          surface.blit(self.image,(self.pos[0]-camera.screen.x,self.pos[1]-camera.screen.y))


class Slope(Tile):#list of premade slopes
   slopes=[ ( ((0,200),(200,0),(200,200)),1), ( ((0,200),(200,0),(200,200)),-1),
            ( ((0,200),(200,50),(200,200)),1),( ((0,200),(200,50),(200,200)),-1),               #easiest way to do slopes, restricted to 
            ( ((50,200),(200,0),(200,200)),1),( ((50,200),(200,0),(200,200)),-1),               #10 slopes though
            ( ((0,200),(150,0),(200,0),(200,200)),1),( ((0,200),(150,0),(200,0),(200,200)),-1) ]

   def __init__(self,pos,index=0,slant=1):
      self.pos=pos
      self.slant=slant  #1 for up slope right, -1 for down slope right
      self.image=pygame.Surface((200,200)).convert()
      self.alpha_color=self.image.get_at((0,0))
      self.image.set_colorkey(self.alpha_color)
      self.color=GREY
      self.width=self.image.get_width()
      self.height=self.image.get_height()
      self.points=Slope.slopes[index][0]
      pygame.draw.polygon(self.image,self.color,self.points,0)
      self.rect=[self.pos[0],self.pos[1],self.width,self.height]
      if self.slant<0:
         self.image=pygame.transform.flip(self.image,1,0)
      self.get_ends()
      self.get_normalized_vector()
      self.increment=(self.end[1]-self.start[1])/(self.end[0]-self.start[0])

   def get_ends(self):
       start=0
       end=0
       
       if self.slant>0:      
          for y in range(self.height):
              if self.image.get_at((0,y))!=self.alpha_color:
                 start=[0,y]
                 break
          if not start:     
             for x in range(self.width):
                 if self.image.get_at((x,self.height-1))!=self.alpha_color:
                    start=[x,self.height-1]
                    break
          for x in range(self.width):
              if self.image.get_at((x,0))!=self.alpha_color:
                 end=[x,0]
                 break               
          if not end:     
             for y in range(self.height):
                 if self.image.get_at((self.width-1,y))!=self.alpha_color:
                    end=[self.width-1,y]
                    break            
       elif self.slant<0:
          for x in range(self.width-1,-1,-1):
              if self.image.get_at((x,0))!=self.alpha_color:
                 start=[x,0]
                 break
          if not start:
             for y in range(self.height):
                 if self.image.get_at((0,y))!=self.alpha_color:
                    start=[0,y]
                    break
          for y in range(self.height):
              if self.image.get_at((self.width-1,y))!=self.alpha_color:
                 end=[self.width-1,y]
                 break
          if not end:
             for x in range(self.width-1,-1,-1):
                 if self.image.get_at((x,self.height-1))!=self.alpha_color:
                    end=[x,self.height-1]
                    break
                  
       if start and end:
          self.start=start
          self.end=end
          self._start=[start[0],start[1]]
          self._end=[end[0],end[1]]
          self.update()

   def update(self):
       self.start[0]=self.pos[0]+self._start[0]
       self.start[1]=self.pos[1]+self._start[1]
       self.end[0]=self.pos[0]+self._end[0]
       self.end[1]=self.pos[1]+self._end[1]
       self.rect[0]=self.pos[0]
       self.rect[1]=self.pos[1]

   def get_normalized_vector(self):
       vector=[self.end[0]-self.start[0],self.end[1]-self.start[1]]
       magnitude=sqrt(vector[0]**2+vector[1]**2)                     
       vector[0]=vector[0]/magnitude
       vector[1]=vector[1]/magnitude
       self.vector=vector
       
class Platform(Tile):

  def __init__(self,pos):
      self.pos=pos
      self.image=pygame.Surface((200,50)).convert()
      self.image.fill(GREY)
      self.width=self.image.get_width()
      self.height=self.image.get_height()
      self.rect=[self.pos[0],self.pos[1],self.width,self.height]
        
class Camera:
    
  def __init__(self,target,level_end=2000):  
      self.target=target
      self.level_end=level_end
      self.screen=pygame.Rect((0,0,SCREEN_WIDTH,SCREEN_HEIGHT))
    
  def update(self):
      if self.target.pos[0]>self.screen.centerx:
         if self.screen.right<self.level_end[0]:
            dx=self.target.pos[0]-self.screen.centerx
            self.screen.move_ip(dx,0)
            if self.screen.right>self.level_end[0]:
               self.screen.right=self.level_end[0]
      elif self.target.pos[0]<self.screen.centerx:
         if self.screen.left>0:
            dx=self.target.pos[0]-self.screen.centerx       #simple camera movement based on the sprite 0,0 and the center of the screen
            self.screen.move_ip(dx,0)
            if self.screen.left<0:
               self.screen.left=0
      if self.target.pos[1]>self.screen.centery:
         if self.screen.bottom<self.level_end[1]:
            dy=self.target.pos[1]-self.screen.centery
            self.screen.move_ip(0,dy)
            if self.screen.bottom>self.level_end[1]:
               self.screen.bottom=self.level_end[1]
      elif self.target.pos[1]<self.screen.centery:
         if self.screen.top>0:
            dy=self.target.pos[1]-self.screen.centery
            self.screen.move_ip(0,dy)
            if self.screen.top<0:
               self.screen.top=0
            
class Player:
   
   def __init__(self,pos):
      print(pos)    
      self.pos=pos
      #self.image=pygame.Surface((50,50)).convert()  -test sprite
      self.image=pygame.image.load("Rmariocar.png") # sort out image sizing for better looking collision
      self.width=self.image.get_width()
      self.height=self.image.get_height()
      #self.image.fill(ORANGE) -test sprite fill
      self.move_speed=10
      self.vector=[0,0]
      self.velocity=[0,0]
      self.temp_xvel=0 # for velocity on the slopes
      self.gravity=0.7
      self.friction=0.3
      self.fall_through=0
      self.on_ground=False
      self.on_slope=False
      self.left=self.right=self.down=self.running=False
      self.rect=[self.pos[0],self.pos[1],self.width,self.height]#setup player rectangle for collision stuff
      
   def controls(self):
       for event in pygame.event.get():    
           if event.type == QUIT:
               pygame.quit()
               sys.exit()
               
           if event.type == KEYDOWN:
              if event.key == K_RIGHT:
                 self.right=True
                 if self.right == True:
                     self.image = pygame.image.load("Rmariocar.png")
              elif event.key == K_LEFT:
                 self.left=True
                 if self.left == True:
                     self.image = pygame.image.load("Lmariocar.png")
              if event.key == K_DOWN:
                 self.down=True
              if event.key == K_SPACE:
                 self.running=True                               
              if event.key == K_UP:
                 if self.on_ground:
                    if self.down:
                       self.fall_through=3
                       self.velocity[1]=5
                    else:
                       self.velocity[1] -= 12
                       self.gravity=0.3
                    self.on_ground=False
           elif event.type == KEYUP:
                if event.key == K_UP:
                   self.gravity=0.7
                if event.key == K_RIGHT:
                   self.right=False
                elif event.key == K_LEFT:
                   self.left=False
                if event.key == K_DOWN:
                   self.down=False
                if event.key == K_SPACE:
                   self.running=False                               
   

   def move_rect(self):
       self.rect[0]=self.pos[0]
       self.rect[1]=self.pos[1]

   def collision_handler(self,level):
       self.move_rect()
       for tile in level.tiles:
           if rect_collision(self.rect,tile.rect):
                 if self.velocity[1]>0:
                    if self.pos[1]+self.height-self.velocity[1]<=tile.pos[1]:
                       self.pos[1]=tile.pos[1]-self.height
                       self.velocity[1]=0
                       self.on_ground=True
                       break
                 elif self.velocity[1]<0:
                   if self.pos[1]-self.velocity[1]>=tile.pos[1]+tile.height:  
                      self.pos[1]=tile.pos[1]+tile.height
                      self.velocity[1]=0
                 if self.velocity[0]>0:
                    if self.pos[0]+self.width-self.velocity[0]<=tile.pos[0]:
                       self.pos[0]=tile.pos[0]-self.width
                       self.velocity[0]=0
                 elif self.velocity[0]<0:
                    if self.pos[0]-self.velocity[0]>=tile.pos[0]+tile.width:   
                       self.pos[0]=tile.pos[0]+tile.width
                       self.velocity[0]=0
                 self.move_rect()
               
       for slope in level.slopes:
           if rect_collision(self.rect,slope.rect):
              desired_y_pos=Slope_Manager(slope,self)  
              self.pos[1]=desired_y_pos
              self.move_rect()
                          
       if not self.fall_through: 
          for platform in level.platforms:
              if rect_collision(self.rect,platform.rect):
                 if self.velocity[1]>=0:
                    if self.pos[1]+self.height-self.velocity[1]<=platform.pos[1]:
                       self.pos[1]=platform.pos[1]-self.height
                       self.velocity[1]=0
                       self.on_ground=True
                       break

   def walk_control(self,level): 
       
       if self.right:
          if self.velocity[0]==0:
             self.velocity[0]+=5
             print(self.velocity)
          elif self.velocity[0]<0:
             self.velocity[0]+=1.3
             if self.velocity[0]>0:
                 self.velocity[0]=0
          else:
             self.velocity[0]+=0.2
             if self.velocity[0]>20:
                self.velocity[0]=20
          if self.running:
             self.velocity[0]+=10
             
       elif self.left:
          if self.velocity[0]==0:
             self.velocity[0]-=5
             print(self.velocity)
          elif self.velocity[0]>0:
             self.velocity[0]-=1.3
             if self.velocity[0]<0:
                 self.velocity[0]=0                               
          else:
             self.velocity[0]-=0.2
             if self.velocity[0]<-20:
                self.velocity[0]=-20
          if self.running:
             self.velocity[0]-=10
                             
       if self.velocity[0]>0 and not self.right:
          self.velocity[0]-=self.friction
          if self.velocity[0]<0:
             self.velocity[0]=0
             
       elif self.velocity[0]<0 and not self.left:
          self.velocity[0]+=self.friction
          if self.velocity[0]>0:
             self.velocity[0]=0
             
       if self.on_slope:
          self.temp_xvel=(self.velocity[0]*self.vector[0])
          self.pos[0]+=self.temp_xvel
       else:   
          self.pos[0]+=self.velocity[0]
       
       if self.pos[0]<0:
          self.pos[0]=0
       elif self.pos[0]+self.width>level.end[0]:
          self.pos[0]=level.end[0]-self.width

   
   def jump_control(self,floor_pos=1400):
       self.velocity[1]+=self.gravity
       if self.velocity[1]>100:
          self.velocity[1]=100
       if self.on_slope :
          if self.on_ground:
             self.velocity[1]=(self.velocity[0]*self.vector[1])
          self.on_slope=False
       self.on_ground=False
       self.pos[1]+=self.velocity[1]
       if self.pos[1]+self.height>floor_pos:
          self.pos[1]=floor_pos-self.height
          self.velocity[1]=0
          self.on_ground=True
       if self.fall_through>0:
          self.fall_through-=1

   def update(self,level):
       self.controls()
       self.walk_control(level)
       self.jump_control(floor_pos=level.end[1])
       self.collision_handler(level)
       
   def draw(self,surface,camera):
       surface.blit(self.image,(self.pos[0]-camera.screen.x,self.pos[1]-camera.screen.y))


class Level:
                       
   def __init__(self):
       self.objects=[]
       self.slopes=[]
       self.platforms=[]
       self.tiles=[]
       self.end=None
       self.start_pos=None
       
   def make_level(self,level): # checks each letter then makes a surface 
       x=0
       y=200 # scale 200
       self.end=[len(level[0])*200,len(level)*200+200]
       for string in level:
           for char in string:
               if char!=" ":
                  if char=="a": # start position
                     self.start_pos=[x,y]
                  elif char=="p": # can pass through the bottom, to get to higher levels
                     p=Platform((x,y))
                     self.objects.append(p)
                     self.platforms.append(p)
                  elif char=="t": # solid platforms
                     t=Tile((x,y))
                     self.objects.append(t)
                     self.tiles.append(t)
                # elif char =="e":          # will implement later
                #    self.finish_pos =[x,y]
                #setup kill plain for failing jumps
                #append kill plain co-ords to check player x,y against
                  else:
                     char=int(char)
                     print(char)
                     s=Slope((x,y),index=char,slant=Slope.slopes[char][1])#numbers correspond to pre-defined slopes
                     self.slopes.append(s)
                     self.objects.append(s)
               x+=200
           x=0
           y+=200

def Build_Random_Row():
    list_pos = 0
    Generation = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "]
    for i in Generation:
        Ran_num = random.random()
        if Ran_num < 0.7:
            pass
        else:
            Ran_num = random.random()
            if Ran_num < 0.6:
                Generation[list_pos] = "t"
            else:
                Ran_num = random.randint(1,6)
                Generation[list_pos] = str(Ran_num)
        list_pos += 1
    Gen_string = "".join(Generation)
    return Gen_string
       
def main():

   pygame.init()

   #Open Pygame window
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),)
   
   #Title
   pygame.display.set_caption("Going the distance")

   #build level rng
   Row_Generation = Build_Random_Row()
   _level=["a                                                  ",
           Row_Generation,
           "tttttttttt   tttttttt   tttttttttttt t t ttttttt   "]

   level=Level() #intiate level
   level.make_level(_level) #enter template
   player=Player(level.start_pos)
   camera=Camera(player,level_end=level.end)

   #game refreshing area
   while True:
       
       CLOCK.tick(50)
    
       player.update(level)
       camera.update()
       screen.fill(ORANGE)

       for obj in level.objects:
           obj.draw(screen,camera)
       player.draw(screen,camera)
       pygame.display.flip()
   

   
       
if __name__=='__main__':
    Main_Menu()
    
