import pygame,sys,random
from pygame.math import Vector2
pygame.init()


no_cells = 40
cell_size = 20
#screen
sc = pygame.display.set_mode((cell_size*no_cells,cell_size*no_cells))
clk=pygame.time.Clock()
fruitpic = pygame.image.load("temp/fruit.png").convert_alpha()
game_font = pygame.font.Font('temp/Radikal W03 Regular.ttf',25)


screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update,150)


#fruit for snake to consume
class FRUIT:
    def __init__(self):
        #create x-y position
        self.x=random.randint(0,no_cells-1)
        self.y=random.randint(0,no_cells-1)
        self.pos =Vector2(self.x,self.y)

    
    def draw_fruit(self):
        #draw a square as frutis
        fruit_rec=pygame.Rect(int(self.pos.x)*cell_size,int(self.pos.y*cell_size),cell_size,cell_size)
        sc.blit(fruitpic,fruit_rec)
        #pygame.draw.rect(sc,pygame.Color("black"),fruit_rec)

    def randomize(self):
        self.x=random.randint(0,no_cells-5)
        self.y=random.randint(0,no_cells-5)
        self.pos =Vector2(self.x,self.y)


class SNAKE:
    def __init__(self):
        self.body =[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.newblock=False

        self.head_up = pygame.image.load("temp/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("temp/head_down.png").convert_alpha()
        self.head_left = pygame.image.load("temp/head_left.png").convert_alpha()
        self.head_right = pygame.image.load("temp/head_right.png").convert_alpha()
        self.tail_down = pygame.image.load("temp/tail_down.png").convert_alpha()
        self.tail_left = pygame.image.load("temp/tail_left.png").convert_alpha()
        self.tail_right = pygame.image.load("temp/tail_right.png").convert_alpha()
        self.tail_up = pygame.image.load("temp/tail_up.png").convert_alpha()
        self.body_vertical = pygame.image.load("temp/body_vertical.png").convert_alpha()
        self.body_tr = pygame.image.load("temp/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("temp/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("temp/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("temp/body_bl.png").convert_alpha()
        self.body_horizontal = pygame.image.load("temp/body_horizontal.png").convert_alpha()

        self.eat_sound= pygame.mixer.Sound("temp/crunch.mp3")
        
        
    def reset(self):
        self.body =[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        


    def update_head(self):
        head_change=self.body[1]-self.body[0]
        if head_change==Vector2(1,0): self.head=self.head_left
        if head_change==Vector2(-1,0): self.head=self.head_right
        if head_change==Vector2(0,-1): self.head=self.head_down
        if head_change==Vector2(0,1): self.head=self.head_up

    def update_tail(self):
        tail_change=self.body[-2]-self.body[-1]
        if tail_change==Vector2(1,0): self.tail=self.tail_left
        if tail_change==Vector2(-1,0): self.tail=self.tail_right
        if tail_change==Vector2(0,-1): self.tail=self.tail_down
        if tail_change==Vector2(0,1): self.tail=self.tail_up



    def draw_snake(self):
        self.update_head()
        self.update_tail()
        
        for index,block in enumerate(self.body):
            #create rectangle
            x_pos=int(block.x * cell_size)
            y_pos=int(block.y * cell_size)
            snake_rec=pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            #check head direction

            #initial position
            #head
            if index==0:
                sc.blit(self.head,snake_rec)
            #tail
            elif index == len(self.body)-1:
                sc.blit(self.tail,snake_rec)
            else:
                #up or down
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if previous_block.x==next_block.x:
                    sc.blit(self.body_vertical,snake_rec)
                elif previous_block.y==next_block.y:
                    sc.blit(self.body_horizontal,snake_rec)
                else:
                    #corners
                    if previous_block.x==-1 and next_block.y ==-1 or previous_block.y==-1 and next_block.x==-1:
                        sc.blit(self.body_tl,snake_rec)
                    elif previous_block.x==-1 and next_block.y ==1 or previous_block.y==1 and next_block.x==-1:
                        sc.blit(self.body_bl,snake_rec)
                    elif previous_block.x==1 and next_block.y ==-1 or previous_block.y==-1 and next_block.x==1:
                        sc.blit(self.body_tr,snake_rec)
                    elif previous_block.x==1 and next_block.y ==1 or previous_block.y==1 and next_block.x==1:
                        sc.blit(self.body_br,snake_rec)
    

    def play_sound(self):
        self.eat_sound.play()


            
    
    def move_snake(self):
        if self.newblock==True:
            #tail is also added as a part of snake
            body_copied= self.body[:]
            body_copied.insert(0,body_copied[0]+self.direction)
            self.body = body_copied[:]
            self.newblock=False
        else:
            #tail is deleted so that it seems like snake is moving
            body_copied= self.body[:-1]
            #new pos is inserted in list of vectors
            body_copied.insert(0,body_copied[0]+self.direction)
            self.body = body_copied[:]
    
    def elongate(self):
        self.newblock=True
        

class GAME:
    def __init__(self):
        self.snake= SNAKE()
        self.fruit = FRUIT()


    def update(self):
        self.snake.move_snake()
        self.eat()
        self.check_dead()
    
    def scoreboard(self):
        score=str(len(self.snake.body)-3)
        score_disp = game_font.render(score,True,(56,74,12))
        scorex=int(cell_size*no_cells -60)
        scorey=int(cell_size*no_cells -30)
        score_rect=score_disp.get_rect(center=(scorex,scorey))
        fruit_rect=fruitpic.get_rect(midright=(score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(fruit_rect.left,fruit_rect.top,fruit_rect.width+score_rect.width,fruit_rect.height)

        pygame.draw.rect(sc,pygame.Color("gold"),bg_rect)
        pygame.draw.rect(sc,(56,74,12),bg_rect,2)
        sc.blit(score_disp,score_rect)
        sc.blit(fruitpic,fruit_rect)


    def draw(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.scoreboard()

    def eat(self):

        if self.fruit.pos == self.snake.body[0]:
            #chagne fruit pos
            self.fruit.randomize()
            #elongate snake
            self.snake.elongate()
            self.snake.play_sound()
        
        for block in self.snake.body[1:]:
            if block==self.fruit.pos:
                self.fruit.randomize()

    def check_dead(self):
        #snake outside screen
        if not 0<=self.snake.body[0].x < no_cells or not 0<=self.snake.body[0].y < no_cells :
            self.game_over()
        #snake hits itself
        for block in self.snake.body[1:]:
            if block==self.snake.body[0]:
                self.game_over()

    
    def draw_grass(self):
        grass_color =(167,209,61)
        for row in range(no_cells):
            if row%2==0:
                for i in range(no_cells):
                    if i%2==0:
                        grass_rec=pygame.Rect(cell_size*i,cell_size*row,cell_size,cell_size)
                        pygame.draw.rect(sc,grass_color,grass_rec)
            else:
                for i in range(no_cells):
                    if i%2!=0:
                        grass_rec=pygame.Rect(cell_size*i,cell_size*row,cell_size,cell_size)
                        pygame.draw.rect(sc,grass_color,grass_rec)
                
    
    def game_over(self):
        self.snake.reset()





game=GAME()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==screen_update:
            game.update()
        if event.type == pygame.KEYDOWN:
            #up key should not be pressed when down key is pressed
            if event.key==pygame.K_UP:
                if game.snake.direction.y!=1:
                    game.snake.direction = Vector2(0,-1)
            if event.key==pygame.K_DOWN:
                if game.snake.direction.y!=-1:
                    game.snake.direction = Vector2(0,1)
            if event.key==pygame.K_LEFT:
                if game.snake.direction.x!=1:
                    game.snake.direction = Vector2(-1,0)
            if event.key==pygame.K_RIGHT:
                if game.snake.direction.x!=-1:
                    game.snake.direction = Vector2(1,0)
            
        
    #background surface color
    sc.fill((175,215,70))
    game.draw()
    pygame.display.update()
    clk.tick(150)