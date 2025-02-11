import pygame
from sys import exit
from random import randint

def displayScore():
    currentTime = int(pygame.time.get_ticks() / 1000) - startTime
    textSurface = testFont.render(f'Score: {currentTime}', False, (64, 64, 64))
    textRect = textSurface.get_rect(center=(400, 50))
    screen.blit(textSurface, textRect)
    for cloud in clouds:
        cloud.x -= 2
        pygame.draw.rect(screen, 'Light Gray', cloud)
        if cloud.right < 0:
            cloud.x = randint(800, 1000)
    return currentTime

speed = 12

def obsMovement(obsList):
    if obsList:
        for obsRect in obsList:
            obsRect.x -= speed
            screen.blit(enemy1 if obsRect.bottom == 300 else enemy2, obsRect)

        obsList = [obs for obs in obsList if obs.x > -100]
        return obsList
    return []

def collisions(player, obsList):
    return not any(player.colliderect(obs) for obs in obsList)

class Particle:
    def __init__(self, x, y, color, speed, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.lifetime = lifetime  # How long the particle lives
        self.size = randint(2, 5)  # Random size for diversity

    def update(self):
        # Move the particle upwards or sideways
        self.y -= self.speed
        self.size = max(self.size - 0.1, 0)  # Shrink over time
        self.lifetime -= 1  # Decrease lifetime

    def is_alive(self):
        return self.lifetime > 0
    
particles = []

def create_particles(x, y):
    for _ in range(20):  # Number of particles
        color = (randint(150, 255), randint(150, 255), randint(150, 255))  # Random color
        speed = randint(1, 4)  # Random speed
        lifetime = randint(20, 50)  # How long the particle lasts
        particles.append(Particle(x, y, color, speed, lifetime))

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Speed Cube')
clock = pygame.time.Clock()
testFont = pygame.font.Font(None, 50)

gameActive = False
startTime = 0
score = 0

skySurface = pygame.Surface((800, 350))
skySurface.fill('#55b6ff')

groundSurface = pygame.Surface((800, 150))
groundSurface.fill('Dark Green')

clouds = [pygame.Rect(randint(800, 1000), randint(50, 200), 50, 30) for _ in range(3)]

enemy1 = pygame.Surface((50, 30))
enemy1.fill('Dark Red')

enemy2 = pygame.Surface((40, 20))
enemy2.fill('Black')

obsRectList = []

playerOriginal = pygame.Surface((60, 60), pygame.SRCALPHA)  # Transparent background
playerOriginal.fill('Yellow')
playerRect = playerOriginal.get_rect(midbottom=(80, 300))

obsTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obsTimer, 600)

playerGrav = 0
rotationAngle = 0
jumps = 1  # Allow one mid-air jump
speed_updated = False
jumping = False

midairJump = False  # Initialize midairJump flag

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if gameActive:
            if score % 10 == 0 and score != 0 and not speed_updated:
                speed += 0.5
                speed_updated = True
            if score % 10 != 0:
                speed_updated = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if playerRect.bottom >= 300 and not jumping:
                        playerGrav = -15  # First jump
                        rotationAngle = 0  # Reset rotation to 0 before jumping
                        jumping = True  # Start jump process
                        midairJump = False  # Reset midair jump

                    elif not midairJump and jumps > 0:  # Only allow mid-air jump once
                        playerGrav = -12
                        jumping = True  # Allow another jump
                        rotationAngle = min(rotationAngle + 10, 90)  # Increase rotation by 10 for clockwise
                        midairJump = True  # Set midair jump flag to True


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gameActive:
                gameActive = True
                startTime = int(pygame.time.get_ticks() / 1000)

        if event.type == obsTimer and gameActive:
            obsRectList.append(enemy1.get_rect(bottomright=(randint(800, 950), 300)) if randint(0, 2) 
                               else enemy2.get_rect(bottomright=(randint(800, 950), 210)))

    if gameActive:
        screen.blit(skySurface, (0, 0))
        screen.blit(groundSurface, (0, 300))

        score = displayScore()

        # Apply gravity
        playerGrav += 1
        playerRect.y += playerGrav

        if jumping:
            # Rotate cube by 10 degrees until it reaches 90 degrees (clockwise)
            if rotationAngle < 90:
                rotationAngle = min(rotationAngle + 10, 90)  # Increase rotation by 10 for clockwise

        # Stop at ground level
        if playerRect.bottom >= 300:
            playerRect.bottom = 300
            playerGrav = 0  # Stop falling
            jumping = False
            rotationAngle = 0  # Reset rotation on landing
            midairJump = False  # Reset midair jump flag

        # Rotate the player
        rotatedPlayer = pygame.transform.rotate(playerOriginal, -rotationAngle)  # Rotate clockwise
        rotatedRect = rotatedPlayer.get_rect(center=playerRect.center)  # Keep center aligned
        screen.blit(rotatedPlayer, rotatedRect)

        obsRectList = obsMovement(obsRectList)

        if not collisions(playerRect, obsRectList):
            for _ in range(10):  # Flash effect
                screen.fill((255, 255, 255))
                pygame.display.update()
                pygame.time.delay(30)
            gameActive = False

    else:
        speed = 12
        screen.fill((50, 50, 50))
        titleText = testFont.render("SPEED CUBE", False, (255, 255, 255))
        titleRect = titleText.get_rect(center=(400, 100))
        screen.blit(titleText, titleRect)

        startText = testFont.render("Press SPACE to Start", False, (255, 255, 255))
        startRect = startText.get_rect(center=(400, 300))
        screen.blit(startText, startRect)

        obsRectList.clear()
        playerRect.midbottom = (80, 300)

        scoreMess = testFont.render(f'Your Score: {score}', False, (255, 255, 255))
        scoreMessRect = scoreMess.get_rect(center=(400, 200))

        if score > 0:
            screen.blit(scoreMess, scoreMessRect)

    pygame.display.update()
    clock.tick(60)
