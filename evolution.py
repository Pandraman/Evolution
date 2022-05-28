import pygame,random,math

WIDTH,HEIGHT = 1080,720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
W,H = 512,512

class Food:

    def __init__(self,x,y):
        self.x = x
        self.y = y
    def draw(self):
        pygame.draw.circle(WIN,(0,255,0),(int(self.x),int(self.y)),5)

class Agent:
    def __init__(self,x,y,speed,reproductive_urge,energy,sense_radius):
        self.x = x
        self.y = y
        self.speed = speed
        self.reproductive_urge = reproductive_urge
        self.energy = energy
        self.sense_radius = sense_radius
        self.food_eaten = 0
        self.dir = 0
        self.turnspeed = 0.1
        self.split = False
        self.SPLIT = True
        self.done = False
    def draw(self):
        pygame.draw.circle(WIN,(self.speed*30,0,200-self.speed*30),(int(self.x),int(self.y)),5)
    def move(self,FOODS,AGENTS):
        if self.done == False:
            self.x += self.speed*math.cos(self.dir)
            self.y += self.speed*math.sin(self.dir)
            self.energy -= self.speed/2
            # If Food is near agent, eat it
            for food in FOODS:
                # get dist
                dist = math.sqrt((food.x-self.x)**2+(food.y-self.y)**2)
                if dist < 10:
                    self.food_eaten += 1
                    FOODS.remove(food)
                    self.energy += 25

                elif dist < self.sense_radius:
                    self.dir += self.turnspeed*(math.atan2(food.y-self.y,food.x-self.x)-self.dir)
                else:
                    self.dir += self.turnspeed*(random.random()-0.5)/4
                # if on edge: end
            if self.x < 0 or self.x > W or self.y < 0 or self.y > H:
                self.done = True
                if self.food_eaten == 0:
                    AGENTS.remove(self)
            if self.energy < 0:
                AGENTS.remove(self)
            if self.food_eaten == 2:
                if self.SPLIT == True:
                    self.split = True
                    self.food_eaten = 0
                

FOODS = []
FD = 50
for i in range(FD):
    x = random.randint(0,W)
    y = random.randint(0,H)
    FOODS.append(Food(x,y))

AGENTS = []
AG = 10
for i in range(AG):
    x = random.randint(0,W)
    y = random.randint(0,H)
    AGENTS.append(Agent(x,y,0.5,0.5,100,50))

SP = False
gen = 0
GENS = []
AD = 0
AVG_SPEED = []
AVG = 0
S = False
m = 400
while True:

    

    Keys = pygame.key.get_pressed()
    
    if Keys[pygame.K_LEFT]:
        m -= 1
    if Keys[pygame.K_RIGHT]:
        m += 1



    pygame.draw.rect(WIN,(255,255,255),(-50,-50,562,562),0,20)
    for i in range(len(FOODS)-1):
        FOODS[i].draw()
    AD = 0
    while AD < len(AGENTS)-1:
        AVG = 0
        for i in range(len(AGENTS)-1):
            if len(AGENTS)-1 > 0:
                try:
                    AVG += AGENTS[i].speed
                    if S: AGENTS[i].draw()
                    AGENTS[i].move(FOODS,AGENTS)
                    if AGENTS[i].done == True: AD += 1
                    if AGENTS[i].split == True:
                        AGENTS.append(Agent(AGENTS[i].x,AGENTS[i].y,AGENTS[i].speed+(random.random()-.5)*.1,AGENTS[i].reproductive_urge,AGENTS[i].energy,AGENTS[i].sense_radius))
                        AGENTS[i].split = False
                except: pass
    if AD == len(AGENTS)-1:
        
        if not SP:
            GENS.append(len(AGENTS))
            if len(AGENTS)-1 > 0: AVG_SPEED.append(AVG/(len(AGENTS)-1))
            gen += 1
            SP = True
            for ag in AGENTS:
                ag.done = False
                ag.energy = 100
                ag.food_eaten = 0
                ag.x = random.randint(0,W)
                ag.y = random.randint(0,H)
                FOODS = []
                for i in range(FD):
                    x = random.randint(0,W)
                    y = random.randint(0,H)
                    FOODS.append(Food(x,y))
    else:
        SP = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    for x in range(10,100,10):
        pygame.draw.line(WIN,(150,150,150),(W*1.3,H*.4-x),(WIDTH,H*.4-x),2)
    pygame.draw.line(WIN,(255,255,255),(W*1.3,H*.4),(WIDTH,H*.4),2)
    pygame.draw.line(WIN,(255,255,255),(W*1.3,H*.4),(W*1.3,H*.2),2)
    for G in range(len(GENS)-1):
        
        if len(GENS)-1 > 0:
            if G > 0:
                pygame.draw.line(WIN,(255,255,255),(W*1.3+(G-1)*2,H*.4-GENS[G-1]),(W*1.3+G*2,H*.4-GENS[G]),2)
                pygame.draw.line(WIN,(255,255,0),(W*1.3+(G-1)*2,H*1.2-AVG_SPEED[G-1]*50),(W*1.3+G*2,H*1.2-AVG_SPEED[G]*50),2)
    if len(GENS) > (WIDTH-W*1.3)/2+3:
        GENS.pop(0)
        AVG_SPEED.pop(0)

    pygame.display.update()
    WIN.fill((46,51,54))