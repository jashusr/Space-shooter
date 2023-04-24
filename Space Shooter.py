import pygame
import random

# Initialize Pygame
pygame.init()

# Load music file
pygame.mixer.music.load("gameaudio.mp3")

name = input("Enter the name: ")

rock_speed = 1
print("Choose The Difficulty Level\n1 for Normal(Defult)\n2 for Hard")
dif = int(input("Your choose: "))
if dif==1:
    rock_speed += 0.5
    pygame.time.wait(2000)
elif dif==2:
    rock_speed += 1
    pygame.time.wait(2000)
else:
    print("Input error Difficulty level set to Defult")
    rock_speed += 0.5
    pygame.time.wait(2000)

# Set up the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
player_img = pygame.image.load("shooterjet.png")

pygame.display.set_icon(player_img)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Set up the clock
clock = pygame.time.Clock()

# Set up the font
font = pygame.font.SysFont('Times New Roman', 43)

# Set up the colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Set up the game variables
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150]
player_speed = 5
bullet_speed = 15
bullet_list = []
player_list = []
rock_list = []
score = 0
image_display_time = None
should_display_image = False
rocks_hit = 0

# Load images
bullet_img = pygame.image.load("bullet_img.png")
rock_img = pygame.image.load("rock.jpg")
bg_img = pygame.image.load('bg_img.jpg')
downbg_img = pygame.image.load('downbg_img.jpg')
blast_img = pygame.image.load('blast.png')
life_img = pygame.image.load('life.png')

# Scale images
player_img = pygame.transform.scale(player_img, (50, 50))
bullet_img = pygame.transform.scale(bullet_img, (5, 12))
rock_img = pygame.transform.scale(rock_img, (40, 40))      
blast_img = pygame.transform.scale(blast_img, (40,40))


def draw_player(player_pos):
    #Draw the player on the screen
    screen.blit(player_img, player_pos)

def move_player(keys_pressed, player_pos):
    #Move the player based on user input
    mousepos = pygame.mouse.get_pos()
    x = mousepos[0]
    player_pos[0] = x-25

def draw_bullet(bullet_list):
    #Draw the bullets on the screen
    for bullet_pos in bullet_list:
        screen.blit(bullet_img, bullet_pos)

def move_bullet(bullet_list):
    #Move the bullets up the screen
    for i, bullet_pos in enumerate(bullet_list):
        bullet_pos[1] -= bullet_speed
        if bullet_pos[1] < 0:
            bullet_list.pop(i)

def create_rock():
    #Create a rock at a random position at the top of the screen
    rock_pos = [random.randint(0, SCREEN_WIDTH - 50), 0]
    return rock_pos

def draw_rock(rock_list):
    #Draw the rocks on the screen
    for rock_pos in rock_list:
        screen.blit(rock_img, rock_pos)

def move_rock(rock_list):
    #Move the rocks down the screen
    for i, rock_pos in enumerate(rock_list):
        rock_pos[1] += rock_speed
        if rock_pos[1] > SCREEN_HEIGHT-100:
            rock_list.pop(i)

#04/10/2003 python version
#03/05/2000 python version
#included svr and srvr

# Play music file
pygame.mixer.music.play()

# Main game loop
game_over = True
while game_over:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("Game Exited")
            game_over = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                bullet_list.append([player_pos[0] + 22, player_pos[1]])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                    bullet_list.append([player_pos[0] + 22, player_pos[1]])

    # screen background
    screen.blit(bg_img,(0,0))

    # Move and draw the player
    keys_pressed = pygame.key.get_pressed()
    move_player(keys_pressed, player_pos)
    draw_player(player_pos)

    # Move and draw the bullets
    move_bullet(bullet_list)
    draw_bullet(bullet_list)

    # Move and draw the rocks
    if len(rock_list) < 5:
        rock_list.append(create_rock())
    move_rock(rock_list)
    draw_rock(rock_list)

    # Check for collisions of bullet and rocks
    for rock_pos in rock_list:
        for bullet_pos in bullet_list:
            if bullet_pos[1] < rock_pos[1] + 50 and bullet_pos[1] + 10 > rock_pos[1]:
                if bullet_pos[0] > rock_pos[0] and bullet_pos[0] < rock_pos[0] + 50:
                    bullet_list.remove(bullet_pos)
                    rock_list.remove(rock_pos)
                    blast_pos = rock_pos
                    pygame.time.wait(50)
                    score += 10
                    should_display_image = True
                    image_display_time = pygame.time.get_ticks()

    for rock_pos in rock_list:
        if rock_pos[1] + 50 > player_pos[1] and rock_pos[1] < player_pos[1] + 64:
            if rock_pos[0] + 50 > player_pos[0] and rock_pos[0] < player_pos[0] + 64:
                print("Score: ", score)
                with open("score.txt", "a") as file:
                    file.write(str(name)+ " : "+str(score) + "\n")
                game_over = False

    if should_display_image:
        screen.blit(blast_img,(blast_pos))

    # Check if it's been 2 seconds since the image was displayed
    if image_display_time is not None and pygame.time.get_ticks() - image_display_time > 500:
        image_display_time = None
        should_display_image = False               

    # Draw the score
    screen.blit(downbg_img,(0,600))
    score_text = font.render(str(score), True, GRAY)
    screen.blit(score_text, [165, 627])
    
    for rock_pos in rock_list:
            if rock_pos[1] >= SCREEN_HEIGHT-100:
                rocks_hit += 1

    if rocks_hit == 1:
        screen.blit(life_img,(411,620))
    if rocks_hit == 2:
        screen.blit(life_img,(411,620))
        screen.blit(life_img,(487,619))
    if rocks_hit == 3:
        screen.blit(life_img,(411,620))
        screen.blit(life_img,(487,619))
        screen.blit(life_img,(563,618))
    if rocks_hit == 4:
        screen.blit(life_img,(411,620))
        screen.blit(life_img,(487,619))
        screen.blit(life_img,(563,618))
        screen.blit(life_img,(639,617))
    if rocks_hit == 5:
        screen.blit(life_img,(411,620))
        screen.blit(life_img,(487,619))
        screen.blit(life_img,(563,618))
        screen.blit(life_img,(639,617))
        screen.blit(life_img,(715,616))
        pygame.time.wait(1000)
        print("Score: ", score)
        with open("score.txt", "a") as file:
            file.write(str(name)+ " : "+str(score) + "\n")
        game_over = False
    
    # Update the display
    pygame.display.update()

    # Set the frame rate
    clock.tick(60)   

# Open the file in read mode and read the contents into a list
with open("score.txt", "r") as file:
    contents = file.readlines()

# Split the contents of the list into a list of scores
scores = [int(line.split(":")[1].strip()) for line in contents]

# Find the highest score
high_score = max(scores)

pygame.mixer.music.stop()

print("The highest score is:", high_score)
# Quit Pygame
pygame.quit()

input()