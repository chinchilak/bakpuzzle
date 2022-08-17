# pip install pygame
import pygame
from pygame.locals import *
import random
import json

with open("./puzzle.json", "r") as jf:
    puzzles = json.load(jf)

id = random.randint(0,len(puzzles))

SWIDTH  = 1920
SHEIGHT = 1080
SSCALE  = 1

pygame.init()
font = pygame.font.Font("./bak_std.ttf", 96)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SWIDTH * SSCALE, SHEIGHT * SSCALE))
pygame.display.set_caption("Chest " + str(id))
background = pygame.image.load("./chest.png").convert()
background = pygame.transform.scale(background, (SWIDTH * SSCALE, SHEIGHT * SSCALE))

class Button():
    def __init__(self, text, x, y):
        self.rect = pygame.Rect(x, y, 0, 0)
        self.updateText(text)
        self.clicked = False 

    def updateText(self, text):
        self.text = text
        self.render = font.render(self.text, True, (255,255,255))
        self.text_width = self.render.get_width()
        self.text_height = self.render.get_height()
        self.box = pygame.Surface((self.text_width, self.text_height))
        self.rect = self.render.get_rect(topleft = self.rect.topleft)
        
def check_list_match(list1:list,list2:list):
    for x in set(list1 + list2):
        if list1.count(x) != list2.count(x):
            return False
    return True

def rand_letter_from_list(inputlist:list,solution:str):
    sol = list(solution)
    res = []
    check = True
    while check:
        for each in inputlist:
            res.append(random.choice(each))
        for x in set(res + sol):
            if res.count(x) != sol.count(x):
                check = False
                break
    return res

letters = rand_letter_from_list(puzzles[id]["Sources"],puzzles[id]["Solution"])
solution = list(puzzles[id]["Solution"])

# global lst
lst = [0] * len(letters)
res = []
sol = letters
w = []
h = []
sw = 80
sh = 80
for i,v in enumerate(letters):
    q    = 0.05
    vq   = 0.23 + (i * q)
    hq   = 0.45
    swss = SWIDTH * SSCALE
    shss = SHEIGHT * SSCALE
    lst[i] = puzzles[id]["Sources"][i].find(letters[i])
    res.append(Button(puzzles[id]["Sources"][i][lst[i]], swss * vq, shss * hq))
    w.append(swss * vq)
    h.append(shss * hq)

def get_center_pos_rect_args(fontobject:object,rectobject:object):
    leaver = fontobject.get_rect()
    leaver.center = rectobject.center
    return leaver


leaver = pygame.Rect(1540,910, 162, 72)
leave = font.render("Leave", True, (0,0,0))
sriddle = puzzles[id]["Text"]

rrr = []
rrw = []
rrh = []
for i,v in enumerate(sriddle):
    rrr.append(v)
    rrw.append(260)
    rrh.append(600 + 60 * i)

nlst = list(zip(rrr,rrw,rrh))

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                # print(pygame.mouse.get_pos())
                for i,v in enumerate(lst):
                    if pygame.Rect(w[i], h[i], sw, sh).collidepoint(event.pos):
                        if lst[i] == len(puzzles[id]["Sources"][i]) - 1:
                            lst[i] = 0
                        else:
                            lst[i] += 1
                        res[i].updateText(puzzles[id]["Sources"][i][lst[i]])
                        sol[i] = (puzzles[id]["Sources"][i][lst[i]])
            if leaver.collidepoint(event.pos):
                game_running = False
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False

    screen.fill((0,0,0))
    screen.blit(background, (0,0))

    for i,v in enumerate(letters):
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(w[i], h[i], sw, sh), 1)
        screen.blit(font.render(sol[i], True, (0,0,0)), (w[i] + sw/3, h[i] + sh/5))
        
    screen.blit(leave, get_center_pos_rect_args(leave, leaver))
    for i in nlst:
        screen.blit(font.render(i[0], True, (0,0,0)), (i[1],i[2]))
    
    if check_list_match(sol,solution):
        text = font.render("The chest has opened!", True, (255,255,255))
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(text.get_rect(center=screen.get_rect().center)))
        screen.blit(text, text.get_rect(center=screen.get_rect().center))

    pygame.display.update()

pygame.quit()

        