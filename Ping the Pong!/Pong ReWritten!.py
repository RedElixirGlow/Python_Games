import pygame, sys, random

class Block(pygame.sprite.Sprite):
    def __init__(self,path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
class Player(Block):
    def __init__(self,path, pos_x, pos_y, speed):
        super().__init__(path, pos_x, pos_y)
        self.speed = speed
        self.movement = 0
    def screen_constraint(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constraint()
class Ball(Block):
    def __init__(self,path, pos_x, pos_y, speed_x, speed_y, paddles):
        super().__init__(path, pos_x, pos_y)
        self.speed_x = speed_x * random.choice((-1,1))
        self.speed_y = speed_y * random.choice((-1,1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0
    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(border_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles,False):
            pygame.mixer.Sound.play(player_sound)
            collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1,1))
        self.speed_y *= random.choice((-1,1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width/2,screen_height/2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if current_time - self.score_time >= 2100:
            self.active = True

        time_counter = basic_font.render(str(countdown_number),True,accent_colour)
        time_counter_rect = time_counter.get_rect(center = (screen_width/2, screen_height/2 + 50))
        pygame.draw.rect(screen,background_colour,time_counter_rect)
        screen.blit(time_counter,time_counter_rect)
class Enemy(Block):
    def __init__(self, path, pos_x, pos_y, speed):
        super().__init__(path,pos_x,pos_y)
        self.speed = speed

    def update(self,ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.x:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
class WinLose():
    def __int__(self, player_score, enemy_score, message_win, message_lose):
        self.player_score = player_score
        self.enemy_score = enemy_score
        self.message_win = message_win
        self.message_lose = message_lose
        message_win = basic_font.render(str("Well Done!"),True,accent_colour)
        message_lose = basic_font.render(str("Game Over!"),True,accent_colour)
        if enemy_score == 5 and player_score < 5:
            message_lose_rect = message_lose.get_rect(midleft = (screen_width/2+20,screen_height/2))
            screen.blit(message_lose, message_lose_rect)
        if player_score == 5 and enemy_score < 5:
            message_win_rect = message_win.get_rect(midleft = (screen_width/2+20,screen_height/2))
            screen.blit(message_win, message_win_rect)
class GameManager():
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.enemy_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.enemy_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def win_lose(self):
        # self.player_score = player_score
        # self.enemy_score = enemy_score
        # self.message_win = message_win
        # self.message_lose = message_lose
        message_win = basic_font.render(str("Well Done!"),True,accent_colour)
        message_lose = basic_font.render(str("Game Over!"),True,accent_colour)
        if self.enemy_score == 5:
            # message_lose_rect = message_lose.get_rect(midleft = (screen_width/5,screen_height/2))
            # screen.blit(message_lose, message_lose_rect)
            screen.draw.text("Game Over! :(", center = (screen_width/2,screen_height/2), fontsize = 30)
        if self.player_score == 5:
            # message_win_rect = message_win.get_rect(midleft = (screen_width/2,screen_height/2))
            # screen.blit(message_win, message_win_rect)
            screen.draw.text("Well Done! :D",  center = (screen_width/2,screen_height/2), fontsize = 30)
        # if self.player_score == 5 or self.enemy_score == 5:
        #     screen.draw

    def draw_score(self):
        self.win_lose()
        player_score = basic_font.render(str(self.player_score),True,accent_colour)
        enemy_score = basic_font.render(str(self.enemy_score),True,accent_colour)

        player_score_rect = player_score.get_rect(midleft = (screen_width/2+20,screen_height/25))
        enemy_score_rect = enemy_score.get_rect(midleft = (screen_width/2-40,screen_height/25))

        screen.blit(player_score,player_score_rect)
        screen.blit(enemy_score,enemy_score_rect)


# Setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong the ReWritten Game")

# Global variables (font, colours and sounds)
background_colour = pygame.Color('grey36')
accent_colour = pygame.Color('indianred2')
basic_font = pygame.font.Font("freesansbold.ttf",32)
border_sound = pygame.mixer.Sound("borderPong.ogg")
player_sound = pygame.mixer.Sound("playerPong.ogg")
enemy_sound = pygame.mixer.Sound("opponentPong.ogg")
score_sound = pygame.mixer.Sound("score.ogg")
middle_strip = pygame.Rect(screen_width/2 - 2, 0, 4, screen_height)

# Game objects
player = Player("Paddle.png",screen_width - 20, screen_height/2, 5)
enemy = Enemy("Paddle.png", 20, screen_width/2,5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(enemy)

ball = Ball("Ball.png",screen_width/2,screen_height/2,4,4,paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite,paddle_group)
# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

    screen.fill(background_colour)
    pygame.draw.rect(screen,accent_colour,middle_strip)

    # Running the game
    game_manager.run_game()

    # Rendering
    pygame.display.flip()
    clock.tick(120)