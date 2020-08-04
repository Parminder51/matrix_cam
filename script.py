import pygame, pygame.font
from random import randint
import cv2 as cv

def generate(letters):
    for i in range(len(letters)):
        letters[i] = letters[i][-1:]+letters[i][0:-1]
    return(letters)

def turn(letters, ogletters, lettersOnScreen, gray, frame, k):
    if k=='' or k=='1':
        return(turn_green(letters, ogletters, lettersOnScreen, gray))
    elif k=='0':
        return(turn_red(letters, ogletters, lettersOnScreen, gray))
    elif k=='2':
        return(turn_blue(letters, ogletters, lettersOnScreen, gray))
    else:
        return(turn_color(letters, ogletters, lettersOnScreen, frame))

def turn_green(letters, ogletters, lettersOnScreen, gray):
    for x in range(lettersOnScreen[0]):
        for y in range(lettersOnScreen[1]):
            letters[x][y] = fontObj.render(ogletters[x][y], False, (0, int(gray[y][x]), 0))
    return(letters)

def turn_red(letters, ogletters, lettersOnScreen, gray):
    for x in range(lettersOnScreen[0]):
        for y in range(lettersOnScreen[1]):
            letters[x][y] = fontObj.render(ogletters[x][y], False, (int(gray[y][x]), 0, 0))
    return(letters)

def turn_blue(letters, ogletters, lettersOnScreen, gray):
    for x in range(lettersOnScreen[0]):
        for y in range(lettersOnScreen[1]):
            letters[x][y] = fontObj.render(ogletters[x][y], False, (0, 0, int(gray[y][x])))
    return(letters)

def turn_color(letters, ogletters, lettersOnScreen, gray):
    gray = cv.resize(gray, lettersOnScreen)
    for x in range(lettersOnScreen[0]):
        for y in range(lettersOnScreen[1]):
            letters[x][y] = fontObj.render(ogletters[x][y], False, (int(gray[y][x][2]), int(gray[y][x][1]), int(gray[y][x][0])))
    return(letters)

k = input('Please tell which color you want for the background:\n(default is green if you just press enter)\n0 - red\n1 - green\n2 - blue\n3 - all colors\n')

COLOR = (0, 255, 0) #The Color of the Matrix

#url = 'http://192.168.43.162:4747/video'
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
# Pygame init
pygame.init()
clock = pygame.time.Clock()
temp = pygame.display.Info()
displLength = (temp.current_w, temp.current_h)
surface = pygame.display.set_mode(displLength, pygame.FULLSCREEN)
# Font init
pygame.font.init()
fontObj = pygame.font.Font(pygame.font.get_default_font(), 14)
sampleLetter = fontObj.render('_', False, (0, 111, 0))
letterSize = (sampleLetter.get_width(), sampleLetter.get_height())
lettersOnScreen = (int(displLength[0] / letterSize[0]), int(displLength[1] / letterSize[1]))

letters = [[0 for _ in range(lettersOnScreen[1])] for _ in range(lettersOnScreen[0])]
ogletters = [[0 for _ in range(lettersOnScreen[1])] for _ in range(lettersOnScreen[0])]
char = chr(randint(32, 126))
for x in range(lettersOnScreen[0]):
    for y in range(lettersOnScreen[1]):
        letters[x][y] = fontObj.render(char, False, COLOR)
        ogletters[x][y] = char
        char = chr(randint(32, 126))

run = True
while run:
    clock.tick(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            run = False
    for x in range(lettersOnScreen[0]):
        for y in range(lettersOnScreen[1]):
            surface.blit(letters[x][y], ((x*letterSize[0]), (y*letterSize[1])))
    pygame.display.update()
    surface.fill((0, 0, 0))
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    gray = cv.resize(gray, lettersOnScreen)
    letters = turn(letters, generate(ogletters), lettersOnScreen, gray, frame, k)
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
pygame.quit()
exit()