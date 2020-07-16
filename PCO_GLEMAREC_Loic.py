#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
PCO project - space invaders - GLEM Loïc
'''

try:  # import as appropriate for 2.x vs. 3.x
   import tkinter as tk
except:
   import Tkinter as tk

class Bullet(object):
    def __init__(self, shooter):
        self.radius = 5
        self.color = "red"
        self.speed = 8
        self.id = None
        self.shooter = shooter
        
    def install_in(self, canvas):
        lx = canvas.coords(self.shooter.id)[0] + 6
        ly = 555
        self.id = canvas.create_oval(lx, ly, lx + self.radius*2, ly + self.radius*2, fill=self.color)
        
    def move_in(self, canvas):
        canvas.move(self.id, 0, -self.speed)


class Defender(object):
    def __init__(self): 
        self.width = 20
        self.height = 20
        self.move_delta = 20 
        self.id = None 
        self.max_fired_bullets = 8 
        self.fired_bullets = []
        
    def install_in(self, canvas):
        lx = 400 + self.width/2
        ly = 600 - self.height - 10
        self.id = canvas.create_rectangle(lx, ly, lx + self.width, ly + self.height, fill="white")
    
    def move_in(self,canvas, dx): 
        canvas.move(self.id, dx, 0)
    
    def fire(self, canvas):
        if len(self.fired_bullets) < self.max_fired_bullets:
            self.fired_bullets.append(Bullet(self))
            self.fired_bullets[-1].install_in(canvas)

class Alien(object):
    def __init__(self):
        self.id = None
       
    def install_in(self, canvas, x, y, image, tag):
        self.id = canvas.create_image(x, y, image=image, tags=tag, anchor='nw')
        
    def move_in(self, canvas, dx, dy):
        canvas.move(self.id, dx, dy)

class Fleet(object):
    def __init__(self):
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        self.aliens_fleet = []
        self.image = tk.PhotoImage(file='alien.gif')
        label = tk.Label(image=self.image)
        label.image = self.image
        self.once = True
        
    def install_in(self, canvas):
        x = 0
        y = 0
        for _ in range(self.aliens_lines):
            for _ in range(self.aliens_columns):
                self.aliens_fleet.append(Alien())
                self.aliens_fleet[-1].install_in(canvas, x, y, self.image, "alien")
                x += self.image.width() + self.aliens_inner_gap
            y += self.image.height() + self.aliens_inner_gap
            x = 0
        
    def move_in(self, canvas):
        all_aliens = canvas.bbox("alien")
        canvas.move("alien", self.alien_x_delta, 0)
        try:
            if all_aliens[2] > 800 and self.once: #Sorti droite
                self.alien_x_delta = -self.alien_x_delta
                canvas.move("alien", 0, self.alien_y_delta)
                self.once = False
            if all_aliens[0] < 0 and not self.once: #Sorti gauche
                self.alien_x_delta = -self.alien_x_delta
                canvas.move("alien", 0, self.alien_y_delta)
                self.once = True
        except:
            #On a tout touché
            canvas.quit()
        
    def manage_touched_aliens_by(self, canvas, defender):
        #Test si il y a une touche
        for b in defender.fired_bullets:
            bullet_collision = canvas.find_overlapping(canvas.coords(b.id)[0], canvas.coords(b.id)[1], canvas.coords(b.id)[2], canvas.coords(b.id)[3])
            if len(bullet_collision) > 1:
                for a in self.aliens_fleet:
                    if a.id == bullet_collision[0]:
                        canvas.delete(a.id)
                        canvas.delete(b.id)
                        defender.fired_bullets.remove(b)

class Game(object):
    
    def __init__(self, frame):
        width=800
        height=600
        self.frame=frame
        self.canvas=tk.Canvas(self.frame,width=width, height=height,bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.defender=Defender()
        self.fleet = Fleet()
        
    def start(self):
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.frame.winfo_toplevel().bind("<Key>", self.keypress)
        
    def keypress(self, event):
        x = 0
        if event.keysym == 'Left': 
            x = -30
        elif event.keysym == 'Right': 
            x = 30
        elif event.keysym == 'space':
            self.defender.fire(self.canvas)
        self.defender.move_in(self.canvas, x)

    def start_animation(self):
        self.start()
        self.canvas.after(0, self.animation)
    
    def animation(self):
        for b in self.defender.fired_bullets:
            b.move_in(self.canvas)
           
            #le projectile sort de l'ecran
            if self.canvas.coords(b.id)[1] < 0:
                self.defender.fired_bullets.remove(b)
                self.canvas.delete(b.id)
            
        self.fleet.move_in(self.canvas)
        
        all_aliens = self.canvas.bbox("alien")
        try:
            if all_aliens[3] > self.canvas.coords(self.defender.id)[1]:
                self.canvas.quit()
        except:
            None
        
        #Teste si les projectles touchent
        self.fleet.manage_touched_aliens_by(self.canvas, self.defender)

        self.canvas.after(100, self.animation)
                
class SpaceInvaders(object): 
    ''' Main Game class '''

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Invaders")
        width=800
        height=600
        self.frame=tk.Frame(self.root,width=width, height=height,bg="green")
        self.frame.pack()
        self.game = Game(self.frame)
        
    def play(self): 
        self.game.start_animation()
        self.root.mainloop()  
                
jeu=SpaceInvaders()
jeu.play()


# In[ ]:




