import pygame
from pygame.locals import *
import sys
import os


def move(rect, movement):
    isCollide = 0
    rect.y += movement

    if rect.y < 0:
        rect.y = 0
        isCollide = 1
    if rect.bottom > WIN_SIZE[1]:
        rect.bottom = WIN_SIZE[1]
        isCollide = 1

    return isCollide


def move_ball(ball: Rect, movement: list, players: tuple):
    ball.x += movement[0]
    ball.x += ((VEL) - abs(movement[1])
               ) / 2 if movement[0] > 0 else (-(VEL / 2) - abs(movement[1])) / 2

    for player in players:
        if ball.colliderect(player):
            if movement[0] < 0:
                ball.left = player.right
            if movement[0] > 0:
                ball.right = player.left
            movement[0] = -VEL if movement[0] > 0 else VEL
            movement[1] = VEL * ((ball.centery - player.centery) /
                                 (player.height / 2))

    if move(ball, movement[1]):
        movement[1] = -movement[1]


def check_score(
        ball: Rect, ball_movement: int, player, enemy, player_score: int,
        enemy_score: int):
    if ball.right < 0 or ball.left > WIN_SIZE[0]:
        if ball.right < 0:
            enemy_score += 1
        elif ball.left > WIN_SIZE[0]:
            player_score += 1
        player.centery = enemy.centery = WIN_SIZE[1] / 2
        ball.center = (WIN_SIZE[0] / 2, 50)
        ball_movement = [VEL / 4] * 2

    return ball_movement, player_score, enemy_score

def check_winner(display, player_score, enemy_score):
    if SCORE_TO_WIN in (player_score, enemy_score):
        if player_score == SCORE_TO_WIN:
            winner_text = WINNER_FONT.render("You Win!", 0, GOLD)
        else:
            winner_text = WINNER_FONT.render("You Lose!", 0, RED)
        display.blit(
            winner_text,
            [(win_i / 2) - (text_i / 2) for win_i,
            text_i in zip(WIN_SIZE, winner_text.get_size())])
        pygame.display.update()

        startTm = pygame.time.get_ticks()
        while pygame.time.get_ticks() - startTm < 3_000:
            for event in pygame.event.get():
                if event.type == QUIT or (
                        event.type == KEYDOWN and event.key == K_ESCAPE):
                    sys.exit()
            pygame.time.wait(10)
        main()

def main():
    clock = pygame.time.Clock()

    player = Rect(10, (WIN_SIZE[1] / 2) - 50, 7, 100)
    player_score = 0
    enemy = Rect(WIN_SIZE[0] - 10 - 7, (WIN_SIZE[1] / 2) - 50, 7, 100)
    enemy_score = 0

    ball = Rect(0, 0, 20, 20)
    ball.center = (WIN_SIZE[0] / 2, 50)
    ball_movement = [VEL / 5] * 2

    display = pygame.display.set_mode(WIN_SIZE)

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or (
                    event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

        # Key action
        player_movement = 0
        keys = pygame.key.get_pressed()
        if keys[K_w]:
            player_movement -= VEL
        if keys[K_s]:
            player_movement += VEL
        move(player, player_movement)
        # Moving enemy
        enemy_movement = 0
        if enemy.centery < ball.centery - VEL * 0.9:
            enemy_movement += VEL * 0.9
        elif enemy.centery > ball.centery + VEL * 0.9:
            enemy_movement -= VEL * 0.9
        move(enemy, enemy_movement)
        # Moving ball
        move_ball(ball, ball_movement, (player, enemy))
        # Checking score
        ball_movement, player_score, enemy_score = check_score(
            ball, ball_movement, player, enemy, player_score, enemy_score)

        display.fill(BLACK)

        pygame.draw.rect(display, WHITE, player, 0, 3)
        pygame.draw.rect(display, WHITE, enemy, 0, 3)

        player_score_text = SCORE_FONT.render(str(player_score), 0, WHITE)
        enemy_score_text = SCORE_FONT.render(str(enemy_score), 0, WHITE)
        display.blit(player_score_text, (30, 30))
        display.blit(
            enemy_score_text,
            (WIN_SIZE[0] - 30 - enemy_score_text.get_width(),
             30))

        # Winner check
        check_winner(display, player_score, enemy_score)
        # Draw ball
        pygame.draw.circle(display, WHITE, ball.center, ball.width / 2)

        pygame.display.update()

        clock.tick(60)


pygame.init()

BLACK = Color('black')
RED = Color('red')
GOLD = Color('gold')
WHITE = Color('white')

SCORE_FONT = pygame.font.Font(os.path.join('assets', 'pixel_font.ttf'), 40)
WINNER_FONT = pygame.font.Font(os.path.join('assets', 'pixel_font.ttf'), 96)

WIN_SIZE = (800, 600)

VEL = 10
SCORE_TO_WIN = 3

if __name__ == '__main__':
    main()