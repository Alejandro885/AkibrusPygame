import pygame

pygame.init()

clockfps = pygame.time.Clock()
fps = 60

#creating the game window
bottom_panel = 100
screen_width = 647
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')


#define the fonts
font = pygame.font.SysFont('Times New Roman', 24)

#define colors
red = (255, 0, 0)
green = (0, 255, 0)

#loading the game images and background themes
background_img = pygame.image.load('mistyBackground.jpg').convert_alpha()
#creating panel image
panel_img = pygame.image.load('panelFuturistic.jpg').convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#function for background
def draw_bg():
    screen.blit(background_img, (0, 0))


#function for drawing panel
def draw_panel():
    #draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #show knight stats
    draw_text(f'{knight.name} HP: {knight.health}', font, red, 29, screen_height - bottom_panel + 12)
    for count, i in enumerate(raider_list):
        #show name and health
        draw_text(f'{i.name} HP: {i.health}', font, red, 470, (screen_height - bottom_panel + 8) + count * 42)



# creating fighter classes
class Fighter:
    def __init__(self, x, y, name, max_health, strength, potions):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        #0:idle, 1:attack, 2:damage taken, 3:death
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        # loading idle images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'{self.name}/{i}.png.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # loading attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'{self.name}/attack/{i}.png.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        #will handle animation
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has past since last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if animation reached limit, then loop
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self):
        screen.blit(self.image, self.rect)


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        #constantly update health
        self.health = health
        #calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


knight = Fighter(140, 270, 'knight', 30, 10, 3)
raider1 = Fighter(490, 270, 'raider', 20, 6, 1)
raider2 = Fighter(590, 270, 'raider', 20, 6, 1)

raider_list = []
raider_list.append(raider1)
raider_list.append(raider2)

knight_health_bar = HealthBar(30, screen_height - bottom_panel + 45, knight.health, knight.max_health)
raider1_health_bar = HealthBar(470, screen_height - bottom_panel + 33, raider1.health, raider1.max_health)
raider2_health_bar = HealthBar(470, screen_height - bottom_panel + 75, raider2.health, raider2.max_health)

run = True
while run:

    clockfps.tick(fps)
    #put background image in
    draw_bg()

    #put the panel in
    draw_panel()
    knight_health_bar.draw(knight.health)
    raider1_health_bar.draw(raider1.health)
    raider2_health_bar.draw(raider2.health)

    #draw fighters onto screen
    knight.update()
    knight.draw()
    for raider in raider_list:
        raider.update()
        raider.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
