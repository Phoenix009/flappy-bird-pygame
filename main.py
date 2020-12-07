import pygame
import sys
import random
import time


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos+WIDTH, 900))

def draw_background():
    screen.blit(bg_surface, (bg_x_pos, 0))
    screen.blit(bg_surface, (bg_x_pos+WIDTH, 0))

def create_pipe():
    height = random.choice(pipe_height)
    bottom_pipe = bottom_pipe_surface.get_rect(midtop=(2*WIDTH, height))
    top_pipe = top_pipe_surface.get_rect(midbottom=(2*WIDTH, height-300))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    new_pipes = []
    for pipe in pipes:
        pipe.centerx -= 3
        if pipe.centerx < -WIDTH:continue
        new_pipes.append(pipe)
    
    return new_pipes

def draw_pipes(top_pipes, bottom_pipes):
    for top_pipe, bottom_pipe in zip(top_pipes, bottom_pipes):
        screen.blit(top_pipe_surface, top_pipe)
        screen.blit(bottom_pipe_surface, bottom_pipe)

def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe): return True
    
    if bird_rect.top <= 0 or bird_rect.bottom >= 900: return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement*-3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def display_score(game_state):
    if game_state == "MAIN_GAME":
        score_surface = game_font.render(str(score), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH//2, 50))
        screen.blit(score_surface, score_rect)
    elif game_state == "GAME_OVER":
        global high_score
        high_score = max(high_score, score)

        game_over_surface = game_font.render(f"Game Over !", True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(WIDTH//2, HEIGHT//2-150))
        screen.blit(game_over_surface, game_over_rect)


        high_score_surface = game_font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 100))
        screen.blit(high_score_surface, high_score_rect)

        score_surface = game_font.render(f"Score: {score}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(score_surface, score_rect)

        restart_surface = small_game_font.render(f"Press space to restart", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(restart_surface, restart_rect)


SCREEN_SIZE = WIDTH, HEIGHT = (576, 1024)
MAX_FPS = 120

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)
small_game_font = pygame.font.Font('04B_19.TTF', 20)


#Game Variables
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0
game_active = True

# Game Surfaces
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)
bg_x_pos = 0

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())
bird_frames = [bird_upflap, bird_midflap, bird_downflap, bird_midflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, HEIGHT//2))

bottom_pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
bottom_pipe_surface = pygame.transform.scale2x(bottom_pipe_surface)
top_pipe_surface = pygame.transform.flip(bottom_pipe_surface, False, True)

# Game Events
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
top_pipe_list = []
bottom_pipe_list = []
pipe_height = [300, 400, 600, 800]

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 100)

SCORE_UPDATE = pygame.USEREVENT + 2
pygame.time.set_timer(SCORE_UPDATE, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -7

            if event.key == pygame.K_SPACE and not game_active:
                print("-- RESTARTING --")
                game_active = True
                bird_rect.center = (100, HEIGHT//2)
                bird_movement = 0
                top_pipe_list.clear()
                bottom_pipe_list.clear()
                score = 0


        if event.type == SPAWNPIPE:
            top_pipe, bottom_pipe = create_pipe()
            top_pipe_list.append(top_pipe)
            bottom_pipe_list.append(bottom_pipe)

        if event.type == BIRDFLAP:
            bird_index += 1
            bird_index %= len(bird_frames)
            bird_surface, bird_rect = bird_animation()

        if event.type == SCORE_UPDATE and game_active:
            score += 1

    if check_collisions(top_pipe_list + bottom_pipe_list):
        game_active = False

    # Background
    draw_background()

    if game_active:
        # Bird Movement
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird_surface = rotate_bird(bird_surface)
        screen.blit(rotated_bird_surface, bird_rect)

        #Pipes
        top_pipe_list = move_pipes(top_pipe_list)
        bottom_pipe_list = move_pipes(bottom_pipe_list)
        draw_pipes(top_pipe_list, bottom_pipe_list)

        display_score("MAIN_GAME")
    else:
        display_score("GAME_OVER")


    # Floor
    draw_floor()


    bg_x_pos -= 1
    if bg_x_pos <= -WIDTH: 
        bg_x_pos = 0
    
    floor_x_pos -= 1
    if floor_x_pos <= -WIDTH: 
        floor_x_pos = 0



    pygame.display.update()
    clock.tick(MAX_FPS)

