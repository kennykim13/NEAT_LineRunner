__author__ = 'Kenny'
import pygame
import neat
import sys
import os
import math
import random
import time
from pygame.locals import *


pygame.init()
pygame.font.init()

# Setting Variables, initializing, and loading images
Window_Size = [591,600]
white = [255, 255, 255]
TITLE_FONT = pygame.font.SysFont("pixelmix_bold", 40)
dino_img = [(pygame.image.load("run1.png")),(pygame.image.load("run2.png"))]
cactus_img = [pygame.image.load("CACTUS1.png"),pygame.image.load("CACTUS2.png"),pygame.image.load("CACTUS3.png"),pygame.image.load("CACTUS4.png")]
floor_img = pygame.image.load("floor-1.png")
cloud_img = pygame.image.load("1x-cloud.png")
low_img = [pygame.image.load("low1.png"), pygame.image.load("low2.png")]
bird_img = [pygame.image.load("enemy1.png"), pygame.image.load("enemy2.png")]
dead_img = pygame.image.load("death.png")
generation = 0

class Dino:
    IMAGE = dino_img #Represents Dino Images
    JUMP_VALUE = 10   #Represnets the max height the dino will jump
    velocity = 1
    max_height = 250

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = self.IMAGE[0]
        self.image_count = 0
        self.dino_rect = pygame.Rect(self.x,self.y, self.image.get_width(),self.image.get_height())
        self.onGround = False

    def jump(self):
        self.velocity = -1


    def fall(self):
        self.velocity = 10
        self.y += self.JUMP_VALUE* self.velocity
        self.dino_rect.y += self.JUMP_VALUE* self.velocity

    def move(self, y, ground_rect_1, ground_rect_2):
        self.y += self.velocity*1.1
        self.dino_rect.y += self.velocity*1.1
        self.x += 2
        self.dino_rect.x += 2
        if y > 330:
            self.velocity = 40
            self.y = 330
            self.dino_rect.y = 330

        if groundCollide(self.dino_rect, ground_rect_1, ground_rect_2):
            self.y = 330
            self.dino_rect.y = 330
            self.velocity= 0
        else:
            # Add gravity
            self.velocity -= 1
            self.y += self.velocity
            self.dino_rect.y += self.velocity
        # Cap gravity
        if self.velocity >= 40 or y <= self.max_height:
            self.velocity = 40
            self.y = self.max_height
            self.dino_rect.y = self.max_height
            self.fall()



    def draw(self, win):
        self.image_count += 1
        if self.image_count < 2:
            self.image = self.IMAGE[1]
        elif self.image_count > 2:
            self.image = self.IMAGE[0]
            self.image_count = 0
        #pygame.draw.rect(win,(0,0,0),(self.dino_rect.x,self.dino_rect.y, self.dino_rect.width,self.dino_rect.height),1)
        win.blit(self.image, self.dino_rect)


class Ground:
    velocity = 5
    width = floor_img.get_width()
    image = floor_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width
        self.ground_rect_1 = pygame.Rect(self.x1,self.y, self.image.get_width(),self.image.get_height())
        self.ground_rect_2 = pygame.Rect(self.x2,self.y, self.image.get_width(),self.image.get_height())

    def move(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
            self.ground_rect_1.x = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width
            self.ground_rect_2.x = self.x1 + self.width

    def draw(self, window):
        window.blit(self.image, (self.x1, self.y))
        window.blit(self.image, (self.x2, self.y))

def groundCollide(dino_rect, ground_rect_1, ground_rect_2):
    if dino_rect.colliderect(ground_rect_1) or dino_rect.colliderect(ground_rect_2):
        return True
    else:
        return False


class Cloud:
    velocity = 5
    image = cloud_img

    def __init__(self):
        self.x = random.randrange(0, 591)
        self.y = random.randrange(self.image.get_height(), 125)

    def move(self):
        self.x -= self.velocity

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def off_screen(self):
        self.x = 591
        self.y = random.randrange(self.image.get_height(), 125)


    def randomVel(self):
        self.velocity = random.randrange(3,7)

class Cactus:
    velocity = 5
    gap = 100
    image = cactus_img[random.randrange(0,4)]

    def __init__(self):
        self.x = 591
        self.y = 375.0 - 44
        self.cacti_rect = pygame.Rect(self.x,self.y, self.image.get_width(),self.image.get_height())

    def move(self):
        self.x -= self.velocity
        self.cacti_rect.x  -= self.velocity

    def draw(self, window):
        #pygame.draw.rect(window,(0,0,0),(self.cacti_rect.x,self.cacti_rect.y, self.cacti_rect.width,self.cacti_rect.height),1)
        window.blit(self.image, (self.x, self.y))

    def off_screen(self):
        if (self.x + self.image.get_width()) < 0:
            self.x = random.randrange(591, 1000)
            self.y = 375.0 - 44
            self.image = cactus_img[random.randrange(0,4)]
            self.cacti_rect.x = self.x
            self.cacti_rect.y = self.y

    def randomVel(self):
        self.velocity = random.randrange(3,7)

def draw_win(win, rexys, ground, clouds, cactus, score, generation):
    win.fill(white)
    text = TITLE_FONT.render("Score: " + str(round(score * 100)), 0, (0,0,0))
    win.blit(text, (550 - text.get_width(),10))
    generation_text = TITLE_FONT.render("Generation: " + str(generation), 0, (0,0,0))
    win.blit(generation_text,(400 - generation_text.get_width(), 50))
    ground.draw(win)
    for rexy in rexys:
        rexy.draw(win)
    for cacti in cactus:
        #print("cacti X", cacti.x, " cacti Y:",cacti.y)
        cacti.draw(win)
    for cloud in clouds:
        cloud.draw(win)

    pygame.display.update()

def show_end_screen(screen):
    title = TITLE_FONT.render("You died...", True, (0, 0, 0))
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        screen.blit(title, (230, 100))
        pygame.display.update()
    pygame.quit()

def distance_formula(x2y2, x1y1):
    delta_x = (x2y2[0]-x1y1[0])**2
    delta_y = (x2y2[1]-x1y1[1])**2
    answer = math.sqrt(delta_x + delta_y)
    return answer

def main(genomes, config):
    ground = Ground(375.0)
    clouds = ([Cloud(),Cloud(), Cloud()])
    cactus = [Cactus()]
    window = pygame.display.set_mode(Window_Size)
    clock = pygame.time.Clock()
    score = 0
    global generation
    isJump = False
    jumpCount = 8

    rexys = []
    networks = []
    genome = []
    generation += 1
    for _, ge in genomes:
        network = neat.nn.FeedForwardNetwork.create(ge, config)
        networks.append(network)
        rexys.append(Dino(random.randrange(0,50), 330))
        ge.fitness = 0
        genome.append(ge)

    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        ground.move()

        if len(rexys) <= 0:
            break
        if len(cactus) <= 1:
            cactus.append(Cactus())

        for cacti in cactus:
            cacti.move()
            cacti.off_screen()

            if (cacti.x + cacti.image.get_width()) < 0:
                cacti.off_screen()
                cactus.remove(cacti)

            for x,rexy in enumerate(rexys):
                rexy.move(rexy.y, ground.ground_rect_1, ground.ground_rect_2)
                genome[x].fitness += 0.05
                output = networks[x].activate(
                    (
                    rexy.y, distance_formula((rexy.x,rexy.y),(cacti.cacti_rect.x,cacti.cacti_rect.y))
                    )
                )
                if output[0] > 0.5:
                    rexy.jump()
                if rexy.dino_rect.colliderect(cacti.cacti_rect):
                    rexy.image = dead_img
                    genome[x].fitness -= 3
                    rexys.pop(x)
                    networks.pop(x)
                    genome.pop(x)

        for cloud in clouds:
            cloud.move()
            cloud.off_screen()
            cloud.randomVel()
        score += 1.101
        draw_win(window, rexys, ground, clouds, cactus, score, generation)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "configuration.txt")
    run(config_path)