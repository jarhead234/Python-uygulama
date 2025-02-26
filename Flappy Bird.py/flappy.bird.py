import pygame
import random
import sys
import os
import json
import math
from pygame import mixer

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
BROWN = (139, 69, 19)
DARK_GREEN = (34, 139, 34)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Load high score
def load_high_score():
    try:
        with open('high_score.json', 'r') as f:
            return json.load(f)['high_score']
    except:
        return 0

def save_high_score(score):
    with open('high_score.json', 'w') as f:
        json.dump({'high_score': score}, f)

# Game settings
class Settings:
    def __init__(self):
        self.sound_on = True

class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.animation_count = 0
        self.angle = 0
        self.size = 32
        self.rect = pygame.Rect(self.x + 5, self.y + 5, self.size - 10, self.size - 10)
        self.body_color = (255, 220, 0)  # Parlak sarı
        self.wing_color = (255, 150, 0)  # Koyu turuncu
        self.eye_color = BLACK
        self.beak_color = (255, 140, 0)  # Turuncu

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.angle = 45

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.x = self.x + 5
        self.rect.y = self.y + 5
        self.angle = max(-90, min(45, self.angle - 3))
        self.animation_count = (self.animation_count + 1) % 30

    def draw(self):
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Gövde
        pygame.draw.circle(surface, self.body_color, (16, 16), 12)
        
        # Kanat
        wing_y = 16 + math.sin(self.animation_count * 0.3) * 3
        pygame.draw.ellipse(surface, self.wing_color, (8, wing_y - 6, 12, 8))
        
        # Göz
        pygame.draw.circle(surface, self.eye_color, (22, 13), 3)
        pygame.draw.circle(surface, WHITE, (23, 12), 1)
        
        # Gaga
        pygame.draw.polygon(surface, self.beak_color, [(24, 16), (30, 14), (30, 18)])
        
        rotated_surface = pygame.transform.rotate(surface, self.angle)
        screen.blit(rotated_surface, 
                   (self.x - rotated_surface.get_width()//2,
                    self.y - rotated_surface.get_height()//2))

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(150, SCREEN_HEIGHT - 150)
        self.x = SCREEN_WIDTH
        self.speed = PIPE_SPEED
        self.width = 50
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_height = SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2)
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - self.bottom_height, self.width, self.bottom_height)
        self.passed = False

    def update(self):
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        # Ağaç gövdeleri
        pygame.draw.rect(screen, BROWN, (self.x + self.width//3, 0, self.width//3, self.top_height))
        pygame.draw.rect(screen, BROWN, (self.x + self.width//3, SCREEN_HEIGHT - self.bottom_height, self.width//3, self.bottom_height))

class ParticleSystem:
    def __init__(self):
        self.particles = []

    def add_score_particle(self, x, y):
        self.particles.append({
            'x': x,
            'y': y,
            'timer': 30,
            'y_velocity': -2
        })

    def update(self):
        new_particles = []
        for particle in self.particles:
            particle['timer'] -= 1
            particle['y'] += particle['y_velocity']
            if particle['timer'] > 0:
                new_particles.append(particle)
        self.particles = new_particles

    def draw(self):
        for particle in self.particles:
            alpha = min(255, particle['timer'] * 8)
            text = pygame.font.Font(None, 24).render('+1', True, WHITE)
            text.set_alpha(alpha)
            screen.blit(text, (particle['x'], particle['y']))

def main():
    try:
        settings = Settings()
        bird = Bird()
        pipes = []
        score = 0
        high_score = load_high_score()
        last_pipe = pygame.time.get_ticks()
        font = pygame.font.Font(None, 36)
        particle_system = ParticleSystem()
        
        pygame.mixer.music.set_volume(0.5)

        while True:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if score > high_score:
                        save_high_score(high_score)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.flap()
                    elif event.key == pygame.K_m:
                        settings.sound_on = not settings.sound_on
                        pygame.mixer.music.set_volume(0.5 if settings.sound_on else 0.0)

            # Spawn new pipes
            if current_time - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = current_time

            # Update
            bird.update()
            for pipe in pipes:
                pipe.update()
            particle_system.update()

            # Remove off-screen pipes
            pipes = [pipe for pipe in pipes if pipe.x > -50]

            # Check collisions and scoring
            for pipe in pipes:
                if pipe.top_rect.colliderect(bird.rect) or pipe.bottom_rect.colliderect(bird.rect):
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    return score
                
                if not pipe.passed and pipe.x < bird.x:
                    score += 1
                    particle_system.add_score_particle(bird.x + 50, bird.y)
                    pipe.passed = True

            # Check if bird hits the ground or ceiling
            if bird.y < 0 or bird.y > SCREEN_HEIGHT:
                if score > high_score:
                    high_score = score
                    save_high_score(high_score)
                return score

            # Draw everything
            screen.fill(SKY_BLUE)
            bird.draw()
            for pipe in pipes:
                pipe.draw()
            particle_system.draw()

            # Draw scores
            score_text = font.render(f'Score: {score}', True, WHITE)
            high_score_text = font.render(f'High Score: {high_score}', True, WHITE)
            
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 40))

            pygame.display.flip()
            clock.tick(60)

    finally:
        if score > high_score:
            save_high_score(high_score)

def game_over_screen(score):
    font = pygame.font.Font(None, 48)
    text = font.render(f'Game Over! Score: {score}', True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
    
    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render('Press SPACE to restart', True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
    
    controls_text = restart_font.render('M: Sound On/Off', True, WHITE)
    controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

        screen.fill(SKY_BLUE)
        screen.blit(text, text_rect)
        screen.blit(restart_text, restart_rect)
        screen.blit(controls_text, controls_rect)
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        while True:
            score = main()
            if not game_over_screen(score):
                break
    finally:
        pygame.quit()
        sys.exit() 