import pygame
import sys

# --- CONFIGURATION (Based on your "Scope" section) ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)   # Player
GREEN = (34, 139, 34)   # Platforms
YELLOW = (255, 215, 0)  # Coins
RED = (220, 20, 60)     # Enemies
PURPLE = (148, 0, 211)  # Exit
BLACK = (0, 0, 0)

# Physics Constants (Mechanics: Gravity/Jumping)
GRAVITY = 0.8
JUMP_STRENGTH = -16
PLAYER_SPEED = 5
ENEMY_SPEED = 2

# --- CLASSES ---

class Player(pygame.sprite):
    def __init__(self, x, y):
        super().__init__()
        # Simple rectangle for the player
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False
        self.score = 0

    def update(self, keys, platforms):
        dx = 0
        dy = 0

        # Input Handling (Left/Right)
        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
        
        # Jump Mechanic
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

        # Apply Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # --- Collision Detection ---
        
        # X-Axis Collision
        self.rect.x += dx
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if dx > 0: # Moving right
                self.rect.right = platform.rect.left
            elif dx < 0: # Moving left
                self.rect.left = platform.rect.right

        # Y-Axis Collision
        self.rect.y += dy
        self.on_ground = False # Assume in air until proven otherwise
        hits = pygame.sprite.spritecollide(self, platforms, False)
        for platform in hits:
            if self.vel_y > 0: # Falling down
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
            elif self.vel_y < 0: # Jumping up into something
                self.rect.top = platform.rect.bottom
                self.vel_y = 0

        # Screen boundaries
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel_y = 0
            self.on_ground = True

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.start_x = x
        self.max_dist = distance
        self.direction = 1 # 1 is right, -1 is left

    def update(self):
        # "Patrolling enemies" logic
        self.rect.x += ENEMY_SPEED * self.direction
        
        # Reverse direction if moved too far
        if self.rect.x > self.start_x + self.max_dist:
            self.direction = -1
        elif self.rect.x < self.start_x:
            self.direction = 1

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15)) # Smaller size
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x + 15, y + 15) # Center inside a tile

class ExitBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- MAIN GAME SETUP ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Pygame Platformer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    exits = pygame.sprite.Group()

    # Level Layout (String Map)
    # P = Player, # = Wall, C = Coin, E = Enemy, X = Exit
    level_map = [
        "                        ",
        "                        ",
        "                        ",
        "          C             ",
        "        ###       X     ",
        "   C           #####    ",
        "  ###                   ",
        "         E              ",
        "       #####            ",
        "                        ",
        " P    C       E         ",
        "########################",
    ]

    # Level Parsing
    tile_size = 34 # Approximate size to fit screen
    player = None

    for row_index, row in enumerate(level_map):
        for col_index, char in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size
            
            if char == "#":
                p = Platform(x, y, tile_size, tile_size)
                platforms.add(p)
                all_sprites.add(p)
            elif char == "P":
                player = Player(x, y)
                all_sprites.add(player)
            elif char == "C":
                c = Coin(x, y)
                coins.add(c)
                all_sprites.add(c)
            elif char == "E":
                e = Enemy(x, y, 100) # Patrol distance of 100 pixels
                enemies.add(e)
                all_sprites.add(e)
            elif char == "X":
                exit_gate = ExitBlock(x, y)
                exits.add(exit_gate)
                all_sprites.add(exit_gate)

    running = True
    game_over = False
    win = False

    # --- GAME LOOP ---
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over and not win:
            keys = pygame.key.get_pressed()
            
            # 2. Update
            player.update(keys, platforms)
            enemies.update()

            # Coin Collection
            hits = pygame.sprite.spritecollide(player, coins, True) # True removes the coin
            for coin in hits:
                player.score += 10
            
            # Enemy Collision (Simple restart logic)
            if pygame.sprite.spritecollide(player, enemies, False):
                game_over = True
                print("Hit an enemy!")

            # Exit Collision
            if pygame.sprite.spritecollide(player, exits, False):
                win = True

        # 3. Draw
        screen.fill(BLACK) # Clear screen
        
        all_sprites.draw(screen)

        # UI Text
        score_text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if game_over:
            end_text = font.render("GAME OVER! Restart to try again.", True, RED)
            screen.blit(end_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
        
        if win:
            win_text = font.render("YOU WIN! Level Complete.", True, YELLOW)
            screen.blit(win_text, (SCREEN_WIDTH//2 - 130, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()