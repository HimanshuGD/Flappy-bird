import pygame
import sys
import random
from pygame import mixer

pygame.init()

width = 1270
height = 720
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
fps = 60

message = pygame.image.load("images/message.png").convert_alpha()
background = pygame.image.load("images/background.png").convert_alpha()
bird = pygame.image.load("images/bird.png").convert_alpha()
pipe = pygame.image.load("images/pipe.png").convert_alpha()
rotatedPipe = pygame.image.load("images/rotated_pipe.png").convert_alpha()
point = pygame.mixer.Sound("sounds/point.wav")
hit = pygame.mixer.Sound("sounds/hit.wav")
die = pygame.mixer.Sound("sounds/die.mp3")
wing = pygame.mixer.Sound("sounds/wing.mp3")
pygame.display.set_caption("Flappy Bird")

mixer.music.load("sounds/middle.mp3")
mixer.music.play(-1)

def welcomescreen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key == pygame.K_UP):
                return
            else:
                screen.blit(message, (0,0))
                pygame.display.update()

class Game:
    def __init__(self):
        self.gameOn = True
        self.birdX = 100
        self.birdY = 100
        self.pipesX = [width, width+200, width+400,width+600,width+800,width+1000,width+1200]
        self.lowerPipeY = [self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe(),self.randomPipe()]
        self.upperPipeY = [self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe(),self.randomRotatedPipe()]
        self.gravity = 0
        self.pipeVel = 0
        self.flap = 0
        self.score = 0
        self.rotateAngle = 0
        self.isGameOver = False
        self.playSound = True

#   def welcomescreen(self):
#       while True:
#          for event in pygame.event.get():
#                 if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#                    pygame.quit()
#                 elif event.type==pygame.KEYDOWN and (event.key==pygame.K_SPACE or event.key == pygame.K_UP):
#                    return
#                else:
#                    screen.blit(message, (0, 0))
#                    pygame.display.update()
#                    clock.tick(fps)

    def movingPipe(self):
        for i in range(0,7):
            self.pipesX[i] += -self.pipeVel

        for i in range(0,7):
            if self.pipesX[i] < -50:
                self.pipesX[i] = width + 100
                self.lowerPipeY[i] = self.randomPipe()
                self.upperPipeY[i] = self.randomRotatedPipe()
    
    def randomPipe(self):
        return random.randrange(int(height/2)+50, height-200)

    def randomRotatedPipe(self):
        return random.randrange(-int(height/2)+100, -100)

    def flapping(self):
        self.birdY += self.gravity
        if self.isGameOver == False:
            self.flap -= 1
            self.birdY -= self.flap

    def isCollision(self):
        for i in range(0,7):
            if (self.birdX >= self.pipesX[i] and self.birdX <= (self.pipesX[i] + pipe.get_width()) and ((self.birdY + bird.get_height()-15) >= self.lowerPipeY[i] or (self.birdY) <= self.upperPipeY[i] + rotatedPipe.get_height() - 15)):
                return True
            elif(self.birdX == self.pipesX[i] and (self.birdY <= self.lowerPipeY[i] and self.birdY >= self.upperPipeY[i])):
                if(self.isGameOver == False):
                    self.score += 1
                    pygame.mixer.Sound.play(point)

        if self.birdY + bird.get_height() >= height:
            self.gravity = 0
            return True

        elif self.birdY <= 0:
            return True

        return False

    def gameOver(self):
        if self.isCollision():
            self.isGameOver = True
            self.screenText("Game Over!", (255,255,255), 450, 300, 84, "Fixedsys", bold = True)
            self.screenText("Press Enter To Play Again", (255,255,255), 400, 600, 48, "Fixedsys", bold=True)
            self.pipeVel = 0
            self.flap = 0
            self.rotateAngle = -90
            if self.playSound:
                pygame.mixer.Sound.play(hit)
                pygame.mixer.Sound.play(die)
                self.playSound = False

    def screenText(self, text, color, x,y, size, style, bold = False):
        font = pygame.font.SysFont(style, size, bold = bold)
        screen_text = font.render(text, True, color)
        screen.blit(screen_text, (x,y))

    def mainGame(self):
        while self.gameOn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        #pygame.mixer.Sound.play(wing)

                        if(self.isGameOver == False):
                            self.pipeVel = 5
                            self.gravity = 10
                            self.flap = 20
                            self.rotateAngle = 15
                            pygame.mixer.Sound.play(wing)

                    if event.key == pygame.K_RETURN:
                        newGame = Game()
                        newGame.mainGame()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.rotateAngle = 0
            screen.blit(background, (0,0))
            for i in range(0,7):
                screen.blit(pipe, (self.pipesX[i], self.lowerPipeY[i]))
                screen.blit(rotatedPipe, (self.pipesX[i], self.upperPipeY[i]))
            screen.blit(pygame.transform.rotozoom(bird, self.rotateAngle, 1), (self.birdX, self.birdY))

            self.movingPipe()
            self.flapping()
            self.gameOver()
            self.screenText(str(self.score), (255,255,255), 600, 50, 68, "Fixedsys", bold=True)
            pygame.display.update()
            clock.tick(fps)

while True:
    welcomescreen()
    flappyBird = Game()
    flappyBird.mainGame()
