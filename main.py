import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithmic Rally")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Game settings
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 120
BALL_SIZE = 20
BLOCK_SIZE = 40

# Fonts
FONT = pygame.font.Font(None, 36)
LARGE_FONT = pygame.font.Font(None, 72)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 8
        self.color = WHITE

    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)

    def move(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Ball:
    def __init__(self, speed):
        self.radius = BALL_SIZE // 2
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = speed
        angle = random.uniform(-math.pi/4, math.pi/4)
        self.dx = self.speed * math.cos(angle)
        self.dy = self.speed * math.sin(angle)

    def move(self, paddle, blocks):
        self.x += self.dx
        self.y += self.dy

        if self.y - self.radius <= 0 or self.y + self.radius >= HEIGHT:
            self.dy *= -1

        if self.x - self.radius <= 0:
            self.dx *= -1

        if paddle.rect.collidepoint(self.x, self.y):
            self.dx *= -1.1  # Increase speed slightly on paddle hit
            self.dy = random.uniform(-self.speed, self.speed)

        for block in blocks[:]:
            if block.rect.collidepoint(self.x, self.y):
                if abs(block.rect.top - self.y) < 10 or abs(block.rect.bottom - self.y) < 10:
                    self.dy *= -1
                else:
                    self.dx *= -1
                return block  # Return the hit block

        return None

    def draw(self):
        pygame.draw.circle(WIN, WHITE, (int(self.x), int(self.y)), self.radius)

class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.type = random.choice(['speed', 'size', 'points'])
        self.color = YELLOW if self.type == 'speed' else (RED if self.type == 'size' else BLUE)

    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)

def draw_court():
    WIN.fill(BLACK)
    pygame.draw.line(WIN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
    pygame.draw.rect(WIN, WHITE, (0, 0, WIDTH, HEIGHT), 4)

def create_button(x, y, width, height, text, color):
    button_rect = pygame.Rect(x, y, width, height)
    return {
        'rect': button_rect,
        'text': text,
        'color': color,
        'hover_color': (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
    }

def draw_button(button, surface, font, is_hover=False):
    color = button['hover_color'] if is_hover else button['color']
    pygame.draw.rect(surface, color, button['rect'])
    text_surf = font.render(button['text'], True, WHITE)
    text_rect = text_surf.get_rect(center=button['rect'].center)
    surface.blit(text_surf, text_rect)

def show_menu():
    WIN.fill(BLACK)
    title = LARGE_FONT.render("ALGORITHMIC RALLY", True, WHITE)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    button_width, button_height = 200, 50
    button_y_start = HEIGHT // 2
    button_x = WIDTH // 2 - button_width // 2

    easy_button = create_button(button_x, button_y_start, button_width, button_height, "Easy", GREEN)
    medium_button = create_button(button_x, button_y_start + 70, button_width, button_height, "Medium", YELLOW)
    hard_button = create_button(button_x, button_y_start + 140, button_width, button_height, "Hard", RED)

    buttons = [easy_button, medium_button, hard_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for button in buttons:
                        if button['rect'].collidepoint(event.pos):
                            return button['text'].lower()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "hard"

        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            is_hover = button['rect'].collidepoint(mouse_pos)
            draw_button(button, WIN, FONT, is_hover)

        pygame.display.flip()

def game_over(score):
    text = LARGE_FONT.render(f"GAME OVER - Score: {score}", True, WHITE)
    restart = FONT.render("Press SPACE to restart", True, GRAY)
    WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height()))
    WIN.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + restart.get_height()))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
    return False

def main():
    clock = pygame.time.Clock()

    while True:
        difficulty = show_menu()
        if not difficulty:
            break

        if difficulty == "easy":
            BALL_SPEED_INIT = 3
            NUM_BLOCKS = 3
        elif difficulty == "medium":
            BALL_SPEED_INIT = 4
            NUM_BLOCKS = 5
        else:  # hard
            BALL_SPEED_INIT = 5
            NUM_BLOCKS = 7

        paddle = Paddle(WIDTH - PADDLE_WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        ball = Ball(BALL_SPEED_INIT)
        blocks = [Block(random.randint(50, WIDTH // 2 - BLOCK_SIZE),
                        random.randint(50, HEIGHT - BLOCK_SIZE)) for _ in range(NUM_BLOCKS)]
        score = 0

        running = True
        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            keys = pygame.key.get_pressed()
            paddle.move(keys)
            hit_block = ball.move(paddle, blocks)

            if hit_block:
                blocks.remove(hit_block)
                if hit_block.type == 'speed':
                    paddle.speed += 1
                elif hit_block.type == 'size':
                    paddle.rect.height = min(paddle.rect.height + 10, HEIGHT // 2)
                score += 20 if hit_block.type == 'points' else 10
                blocks.append(Block(random.randint(50, WIDTH // 2 - BLOCK_SIZE),
                                    random.randint(50, HEIGHT - BLOCK_SIZE)))

            # Check if ball is missed
            if ball.x - ball.radius >= WIDTH:
                if not game_over(score):
                    pygame.quit()
                    return
                break

            # Increase score for successful returns
            if ball.x + ball.radius <= 0:
                score += 1

            draw_court()
            paddle.draw()
            ball.draw()
            for block in blocks:
                block.draw()

            # Draw score
            score_text = FONT.render(f"Score: {score}", True, WHITE)
            WIN.blit(score_text, (10, 10))

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()