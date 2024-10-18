import pygame
import sys

pygame.init()

w_width = 1000
w_height = 500
screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Arbegna")

clock = pygame.time.Clock()
bg_img = pygame.image.load("./images/bg.png")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))
walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('soldier/standing.png')
moveRight = [pygame.image.load(f'enemy/R{i}.png') for i in range(1, 10)]
moveLeft = [pygame.image.load(f'enemy/L{i}.png') for i in range(1, 10)]
font = pygame.font.SysFont("helvetica", 30, True)
score = 0
bulletsound = pygame.mixer.Sound("sounds/Bulletsound.mp3")
hitsound = pygame.mixer.Sound("sounds/hit_local.mp3")
hurtsound = pygame.mixer.Sound("sounds/oyne.mp3")
music = pygame.mixer.music.load("sounds/Ethiopian_Patriotic.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

class Player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)
        self.health = 5
        self.damage_taken = 0

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        self.draw_health_bar(screen)
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 20, 50, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, 50 * (self.health / 5), 10))

    def reset(self):
        self.x = 210
        self.y = 435
        self.health = 5
        self.damage_taken = 0

class Projectile():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Enemy():
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel = 3
        self.path = [x, end]
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)
        self.health = 10
        self.visible = True
        
    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 27:
                self.walkCount = 0
            if self.vel > 0:
                screen.blit(moveRight[self.walkCount // 3], (self.x, self.y))
            else:
                screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
            self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
            self.hit = pygame.Rect(self.hitbox)
            pygame.draw.rect(screen, "grey", (self.hitbox[0], self.hitbox[1] + 3, 50, 10), 0)
            pygame.draw.rect(screen, "green", (self.hitbox[0], self.hitbox[1] + 3, 50 - (5.5 + (9 - self.health)), 10), 0)
                 
    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width + 20:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - 20:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
    
    def touch(self):
        hitsound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

def draw_splash_screen():
    screen.fill((0, 0, 0))
    splash_text = font.render("Welcome to Arbegna!", True, (255, 255, 255))
    screen.blit(splash_text, (w_width // 2 - splash_text.get_width() // 2, w_height // 2 - splash_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(3000)  # Show splash for 3 seconds

def draw_main_menu():
    screen.fill((0, 0, 0))
    title = font.render("Arbegna", True, (255, 255, 255))
    start_text = font.render("Press ENTER to Start", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

    screen.blit(title, (w_width // 2 - title.get_width() // 2, 50))
    screen.blit(start_text, (w_width // 2 - start_text.get_width() // 2, 150))
    screen.blit(quit_text, (w_width // 2 - quit_text.get_width() // 2, 200))

    pygame.display.update()

def draw_game_over(score):
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

    screen.blit(game_over_text, (w_width // 2 - game_over_text.get_width() // 2, 50))
    screen.blit(score_text, (w_width // 2 - score_text.get_width() // 2, 150))
    screen.blit(restart_text, (w_width // 2 - restart_text.get_width() // 2, 200))
    screen.blit(quit_text, (w_width // 2 - quit_text.get_width() // 2, 250))

    pygame.display.update()

def DrawInGameloop():
    screen.blit(bg_img, (0, 0))
    clock.tick(25)
    text = font.render("Score: " + str(score), 4, "white")
    screen.blit(text, (0, 10))
    soldier.draw(screen)
    for enemy_inst in enemies:
        enemy_inst.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.flip()

soldier = Player(210, 435, 64, 64)
bullets = []
enemies = []
shoot = 0

enemy_spawn_time = 5000  
last_spawn_time = pygame.time.get_ticks()
spawn_rate_multiplier = 1  
next_double_time = pygame.time.get_ticks() + 30000 

# Game State Control
current_state = "splash"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Splash Screen
    if current_state == "splash":
        draw_splash_screen()
        current_state = "menu"

    # Main Menu
    elif current_state == "menu":
        draw_main_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            current_state = "game"
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    # Game Loop
    elif current_state == "game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(bullets) < 5:
                        bullet = Projectile(soldier.x + 25, soldier.y + 25, 6, (0, 0, 0), 1)
                        bullets.append(bullet)
                        bulletsound.play()
                if event.key == pygame.K_r:
                    soldier.reset()
                    enemies.clear()
                    bullets.clear()
                    score = 0
                    current_state = "game"

        # Spawn enemies at intervals
        if pygame.time.get_ticks() - last_spawn_time > enemy_spawn_time:
            new_enemy = Enemy(900, 440, 64, 64, 900)
            enemies.append(new_enemy)
            last_spawn_time = pygame.time.get_ticks()

        DrawInGameloop()

        for bullet in bullets:
            if bullet.x < w_width and bullet.x > 0:
                bullet.x += bullet.vel
            else:
                bullets.remove(bullet)

        for enemy_inst in enemies:
            if enemy_inst.visible:
                enemy_inst.draw(screen)
                if enemy_inst.hit.colliderect(soldier.hit):
                    soldier.health -= 1
                    hurtsound.play()
                    if soldier.health <= 0:
                        current_state = "game_over"
            for bullet in bullets:
                if bullet.hit.colliderect(enemy_inst.hit):
                    enemy_inst.touch()
                    bullets.remove(bullet)
                    score += 1

    # Game Over
    elif current_state == "game_over":
        draw_game_over(score)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            soldier.reset()
            enemies.clear()
            bullets.clear()
            score = 0
            current_state = "game"
        elif keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    clock.tick(30)

pygame.quit()
