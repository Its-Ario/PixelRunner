import pygame
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        
        playerWalk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        playerWalk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        
        self.playerWalk = [playerWalk1, playerWalk2]
        self.playerJump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
        self.playerState = 0
        
        self.image = self.playerWalk[self.playerState]
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0
        
        self.jumpSound = pygame.mixer.Sound("audio/jump.mp3")
        self.jumpSound.set_volume(0.5)
        
    def update(self) -> None:
        self.playerInput()
        self.applyGravity()
        self.animationState()
        
    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jumpSound.play()
            self.gravity = -20
            
    def animationState(self):
        if self.rect.bottom < 300:
            self.image = self.playerJump
        else:
            self.playerState += .1
            if self.playerState >= len(self.playerWalk): self.playerState = 0
            self.image = self.playerWalk[int(self.playerState)]
            
    def applyGravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        
        if type == 'snail':
            snailFrame1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snailFrame2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snailFrame1, snailFrame2]
            y_pos = 300
        else:
            flyFrame1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            flyFrame2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [flyFrame1, flyFrame2]
            y_pos = 210
            
        self.animationState = 0     
        self.image = self.frames[self.animationState]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100), y_pos))
    
    def animation_state(self):
        self.animationState += .1
        if self.animationState >= len(self.frames): self.animationState = 0
        self.image = self.frames[int(self.animationState)]
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    
pygame.init()

screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
mainFont = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False
game_over = False
startTime = 0
bgMusic = pygame.mixer.Sound("audio/music.wav")
bgMusic.set_volume(0.7)
bgMusic.play(-1)

def mainMenu():
    screen.fill((94,129,162))
    titleFont = pygame.font.Font("font/Pixeltype.ttf", 72)
    titleSurface = titleFont.render("Pixel Runner", False, (0,0,0))
    titleRect = titleSurface.get_rect(center=(400,75))
    
    instructSurface = mainFont.render("Press Space or Click on The Player to Start", False, (255,0,0))
    instructRect = instructSurface.get_rect(center=(400,350))
    
    playerStand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
    playerStand = pygame.transform.scale2x(playerStand)
    playerStandRect = playerStand.get_rect(center=(400,200))
    
    keys = pygame.mouse.get_pressed()
    if playerStandRect.collidepoint(pygame.mouse.get_pos()):
        if keys[0] == True:
            return True
    
    screen.blit(playerStand, playerStandRect)
    screen.blit(titleSurface, titleRect)
    screen.blit(instructSurface, instructRect)

def gameOver():
    gameoverFont = pygame.font.Font("font/Pixeltype.ttf", 72)
    gameoverSurface = gameoverFont.render("Game Over!", False, (255,0,0))
    gameoverRect = gameoverSurface.get_rect(center=(400,150))
    screen.blit(gameoverSurface, gameoverRect)
    
    restartSurface = mainFont.render("Press Space To Restart!", False, (0,0,0))
    restartRect = restartSurface.get_rect(center=(400,375))
    screen.blit(restartSurface, restartRect)
    
def collisions(player, enemies: list):
    if enemies:
        for enemy in enemies:
            if player.colliderect(enemy):
                enemyRects.clear()
                return True, False
    return False, True

def collisionSprite():
    if pygame.sprite.spritecollide(player.sprite,enemyGroup,False):
        enemyGroup.empty()
        return True, False
    return False, True

def enemyMovement(enemies: list):
    if enemies:
        for enemy in enemies:
            enemy.x -= 5
            
            if enemy.bottom == 300:
                screen.blit(snailSurface, enemy)
            else:
                screen.blit(flySurface, enemy)
        return [enemy for enemy in enemies if enemy.x > -100]
    return [] 

def displayScore(start_time):
    time = (pygame.time.get_ticks() - start_time) // 1000
    scoreSurface = mainFont.render(f"Score: {time}", False, (64,64,64))
    scoreRect = scoreSurface.get_rect(center=(100,50))
    screen.blit(scoreSurface, scoreRect)
    
def playerAnimation():
    global playerSurf, playerState
    
    if playerRect.bottom < 300:
        playerSurf = playerJump
    else:
        playerState += .1
        if playerState >= len(playerWalk): playerState = 0
        playerSurf = playerWalk[int(playerState)]

# * Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

enemyGroup = pygame.sprite.Group()

# * Statics

skySurface = pygame.image.load("graphics/Sky.png").convert()
skySurface2 = pygame.image.load("graphics/Sky2.png").convert()
sky1_x = 0
sky2_x = 800

groundSurface = pygame.image.load("graphics/ground.png").convert()
groundSurface2 = pygame.image.load("graphics/ground.png").convert()
ground1_x = 0
ground2_x = 800

# scoreSurface  = mainFont.render('0', False, (64,64,64))
# scoreRect = scoreSurface.get_rect(center=(400,50))

# * Enemies

snailFrame1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snailFrame2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snailState = 0
snailFrames = [snailFrame1, snailFrame2]
snailSurface = snailFrames[snailState]

flyFrame1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
flyFrame2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
flyState = 0
flyFrames = [flyFrame1, flyFrame2]
flySurface = flyFrames[flyState]

enemyRects = []

playerWalk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
playerWalk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
playerWalk = [playerWalk1, playerWalk2]
playerJump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
playerState = 0
playerSurf = playerWalk[playerState]
playerRect = playerSurf.get_rect(midbottom=(80, 300))
playerGravity = 0

# * Timers
enemyTimer = pygame.USEREVENT + 1
pygame.time.set_timer(enemyTimer, 1500)

snailAnimationTimer = pygame.USEREVENT + 2
pygame.time.set_timer(snailAnimationTimer, 500)

flyAnimationTimer = pygame.USEREVENT + 3
pygame.time.set_timer(flyAnimationTimer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playerRect.collidepoint(event.pos):
                    if playerRect.bottom == 300:
                        playerGravity = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if playerRect.bottom == 300:
                        playerGravity = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    game_over = False
                    startTime = pygame.time.get_ticks()
        if game_active:
            if event.type == enemyTimer:
                enemyGroup.add(Enemy(choice(['fly', 'snail','snail','snail'])))
                # if randint(0,2):
                #     enemyRects.append(snailSurface.get_rect(bottomright=(randint(900,1100), 300)))
                # else:
                #     enemyRects.append(snailSurface.get_rect(bottomright=(randint(900,1100), 210)))
            if event.type == snailAnimationTimer:
                if snailState == 0: snailState = 1
                else: snailState = 0
                snailSurface = snailFrames[snailState]
            if event.type == flyAnimationTimer:
                if flyState == 0: flyState = 1
                else: flyState = 0
                flySurface = flyFrames[flyState]
                
    if game_over:
        gameoverFont = pygame.font.Font("font/Pixeltype.ttf", 72)
        gameoverSurface = gameoverFont.render("Game Over!", False, (255,0,0))
        gameoverRect = gameoverSurface.get_rect(center=(400,150))
        screen.blit(gameoverSurface, gameoverRect)
        
        restartSurface = mainFont.render("Press Space To Restart!", False, (0,0,0))
        restartRect = restartSurface.get_rect(center=(400,375))
        screen.blit(restartSurface, restartRect)
    elif game_active:
        # * Ground
        ground1_x -= 5
        ground2_x -= 5
        
        screen.blit(groundSurface, (ground1_x,300))
        screen.blit(groundSurface2, (ground2_x,300))
        
        if ground1_x == -800:
            ground1_x = 800
        elif ground2_x == -800:
            ground2_x = 800
        
        # * Sky
        sky1_x -= 5
        sky2_x -= 5
        
        screen.blit(skySurface, (sky1_x,0))
        screen.blit(skySurface2, (sky2_x,0))
        
        if sky1_x == -800:
            sky1_x = 800
        elif sky2_x == -800:
            sky2_x = 800
        
        # pygame.draw.rect(screen, "#c0e8ec", scoreRect)
        # screen.blit(scoreSurface, scoreRect)
        displayScore(startTime)
        
        # snailRect.x -= 5
        # if snailRect.right <= 0: snailRect.left = 800
        # screen.blit(snailSurface, snailRect)
        
        # Player
        # playerGravity += 1
        # playerRect.y += playerGravity
        # if playerRect.bottom >= 300:
        #     playerRect.bottom = 300
        # playerAnimation()
        # screen.blit(playerSurf, playerRect)
        
        player.draw(screen)
        player.update()
        
        enemyGroup.draw(screen)
        enemyGroup.update()
        
        # # * Enemy Movement
        # enemyRects = enemyMovement(enemyRects)
        
        # * Collision
        game_over, game_active = collisionSprite()
            
    else:
        if mainMenu():
            game_active = True
        
    pygame.display.update()
    clock.tick(60)