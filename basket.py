# Importing Modules And Initializing Them
import pygame
import random

pygame.init()


class Basketball:
    def __init__(self):
        # Variables
        self.Height = 620
        self.Width = 500
        self.Game_Window = pygame.display.set_mode((self.Width, self.Height))
        pygame.display.set_caption("Basket Dunk")

        # Images
        self.background = pygame.image.load("images/bg.jpg")
        self.background = pygame.transform.scale(self.background, (self.Width, self.Height)).convert_alpha()
        self.board_img = pygame.image.load("images/basket.png")
        self.board_img = pygame.transform.scale(self.board_img, (20, 200)).convert_alpha()
        self.play_img = pygame.image.load("images/play.png")
        self.play_img = pygame.transform.scale(self.play_img, (150 + 75, 150)).convert_alpha()
        self.title = pygame.image.load("images/title.png")
        self.title = pygame.transform.scale(self.title, (250, 150)).convert_alpha()

        # Font
        self.font = pygame.font.SysFont("nimbusroman", 55)

        # Controlling Variables
        self.Game = True
        self.Game_Start = False
        self.Clock = pygame.time.Clock()
        self.FPS = 60

        # Other Variables
        self.Score = 0
        self.Gravity = 9.8

        self.Side = "Left"
        self.Basket_Pos = random.randint(200, self.Height // 2 + 100)

        # Ball Variables
        self.Ball_Pos = [self.Width // 2, self.Height // 2]
        self.Ball_Radius = 30
        self.Velocity = [0, 0]
        self.velocity_on_space = [-2, -7]

        # Starting Game Loop
        self.start_time = pygame.time.get_ticks()
        self.time_left = (pygame.time.get_ticks() - self.start_time) / 1000
        self.game_loop()

    def game_loop(self):
        while self.Game:

            # Fetching Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Game = False
                elif event.type == pygame.KEYDOWN:

                    # If Space Key is Pressed
                    if event.key == pygame.K_SPACE and self.Game_Start:
                        self.Velocity[1] = self.velocity_on_space[1]
                        self.Velocity[0] = self.velocity_on_space[0]

                    # To Quit Game
                    elif event.key == pygame.K_q:
                        if not self.Game_Start:
                            self.Game = False
                        self.Game_Start = False

                # Starting Game
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.Game_Start:
                    pos = event.pos

                    # Checking For Position Of Click
                    if (self.Width // 2 - self.play_img.get_width() / 2 < pos[
                        0] < self.Width // 2 - self.play_img.get_width() / 2 + 150 + 75) and (
                            self.Height // 2 - self.play_img.get_height() / 2 + 50 < pos[1] <
                            self.Height // 2 - self.play_img.get_height() / 2 + 50 + 150):
                        # Reinitializing All Variables Again
                        self.Game_Start = True
                        self.start_time = pygame.time.get_ticks()
                        self.Score = 0
                        self.Side = "Left"
                        self.Basket_Pos = random.randint(200, self.Height // 2 + 100)
                        self.Ball_Pos = [self.Width // 2, self.Height // 2]
                        self.velocity_on_space = [-2, -7]

            # Updating Screen
            self.screen()

            # Clock
            self.Clock.tick(self.FPS)

    def screen(self):

        # Setting Background

        self.Game_Window.fill((51, 255, 255))
        self.Game_Window.blit(self.background, [0, 0])

        # Checking Game is Started Or not
        if self.Game_Start:

            # Score And Basket
            self.Game_Window.blit(self.font.render(f"Score : {self.Score}", True, (255, 0, 0)), [0, 0])
            self.create_basket()

            # Drawing Ball
            self.ball = pygame.draw.circle(self.Game_Window, (255, 128, 0), self.Ball_Pos, self.Ball_Radius)

            pygame.draw.rect(self.Game_Window, (50, 50, 50), [50, 50, 400, 20])
            pygame.draw.rect(self.Game_Window, (250, 250, 250), [50, 50, (self.time_left / 10) * 400, 20])
            self.timer()
            self.update_ball_position()
        else:
            self.starting_window()

        pygame.display.update()

    # To Draw The Basket
    def create_basket(self):

        if self.Side == "Right":
            self.board = self.Game_Window.blit(self.board_img, [self.Width - 50, self.Basket_Pos - 140])
            self.basket = pygame.draw.ellipse(self.Game_Window, (255, 0, 0),
                                              [self.Width - 200, self.Basket_Pos, 150, 20], width=5)
        else:
            self.board = self.Game_Window.blit(self.board_img, [30, self.Basket_Pos - 140])

            self.basket = pygame.draw.ellipse(self.Game_Window, (255, 0, 0), [50, self.Basket_Pos, 150, 20], width=5)

    # To Update The Ball Position and checking Collisions
    def update_ball_position(self):
        collision_for_basket = [self.basket.left, self.basket.right,
                                (self.Ball_Pos[0] - self.Ball_Radius) if self.Side == "Left" else (
                                        self.Ball_Pos[0] + self.Ball_Radius)]
        collision_for_basket.sort()

        scoring = [self.basket.left + self.Ball_Radius, self.basket.right - self.Ball_Radius, self.Ball_Pos[0]]
        scoring.sort()

        # Collision With Board
        if self.ball.colliderect(self.board):

            if self.board.top + 10 > self.ball.bottom > self.board.top or \
                    self.board.bottom - 10 < self.ball.top < self.board.bottom:
                self.Velocity[1] = -self.Velocity[1]
            else:
                self.Velocity[0] = -self.Velocity[0]

        # Collision With Basket
        if (collision_for_basket[1] == ((self.Ball_Pos[0] - self.Ball_Radius) if self.Side == "Left" else (
                self.Ball_Pos[0] + self.Ball_Radius))) and (
                self.Basket_Pos < self.Ball_Pos[1] < self.Basket_Pos + 20):
            self.Velocity[0] = -self.Velocity[0]

        # Collision With Ground
        if self.Ball_Pos[1] + self.Ball_Radius >= self.Height - 1:
            self.Velocity[1] = -self.Velocity[1]
            self.Ball_Pos[1] = self.Height - self.Ball_Radius
            if 0 > self.Velocity[1] > -2:
                self.Velocity[1] = 0
                self.Ball_Pos[1] = self.Height - self.Ball_Radius

        # If It Goes Out Of Screen

        if self.Ball_Pos[0] + self.Ball_Radius < 0:
            self.Ball_Pos[0] = self.Width + self.Ball_Radius
        elif self.Ball_Pos[0] - self.Ball_Radius > self.Width:
            self.Ball_Pos[0] = - self.Ball_Radius

        # If We Score A Point
        if (scoring[1] == self.Ball_Pos[0]) and (
                self.Basket_Pos < self.Ball_Pos[1] < self.Basket_Pos + 20) and (self.Velocity[1] > 0):
            self.Basket_Pos = random.randint(200, self.Height // 2 + 100)
            if self.Side == "Right":
                self.Side = "Left"
                self.velocity_on_space[0] = -self.velocity_on_space[0]
            else:
                self.Side = "Right"
                self.velocity_on_space[0] = -self.velocity_on_space[0]
            self.start_time = pygame.time.get_ticks()
            self.Score += 1

        # Updating Position
        self.Velocity[1] += self.Gravity / 60
        self.Ball_Pos[1] += self.Velocity[1]
        self.Ball_Pos[0] += self.Velocity[0]

    # Checking For Time
    def timer(self):
        self.time_left = (pygame.time.get_ticks() - self.start_time) / 1000
        if not self.time_left < 10:
            self.Game_Start = False

    # Creating The Starting Window
    def starting_window(self):

        # Title
        self.Game_Window.blit(self.title, [self.Width // 2 - self.title.get_width() / 2, 100])

        # Button
        self.Game_Window.blit(self.play_img, (
            self.Width // 2 - self.play_img.get_width() / 2, self.Height // 2 - self.play_img.get_height() / 2 + 50))

        # Score
        score = self.font.render(f"Score: {self.Score}", True, (255, 0, 0))
        self.Game_Window.blit(score, [self.Width / 2 - score.get_width() / 2,
                                      self.Height / 2 + score.get_height() + self.play_img.get_height() / 2 + 50])


if __name__ == '__main__':
    basket = Basketball()
