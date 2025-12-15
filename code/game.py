#C:\Users\sathp\Documents\it\PWS\code

# TO DO
# - BALANCE
# - BOSS FIGHT?

import pygame, time, math, random
from pygame.locals import *
from pygame.math import Vector2
pygame.init()

########################### - screen - clock

WINDOW_W = 1100
WINDOW_H = 700

padding = 10
dummy_radius = 21

show_hitboxes = False

screen = pygame.display.set_mode([ WINDOW_W, WINDOW_H])
pygame.display.set_caption("PWS spel")
clock = pygame.time.Clock()

coins_per_drop = 10
medkits = 0

running = True

day_time = True
day_count = 0
day_duration_seconds = 30
night_duration_seconds = 25
switch_count = 0
last_ticks = pygame.time.get_ticks()

upgrade_area = pygame.Rect( 590, 140, 35, 35 )

############################ - vars - pictures

FPS = 60
YELLOW = (255, 255, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 237, 255)
GREEN = (0, 255, 0)
RED = (179, 21, 21)
GRAY = (158, 158, 158)

font32 = pygame.font.Font("freesansbold.ttf", 32)
font24 = pygame.font.Font("freesansbold.ttf", 24)
font16 = pygame.font.Font("freesansbold.ttf", 16)

bullets = []
enemies = []
objects = []
items = []

enemy_speed = 1


############################ - skins & sprites - shop texts

map1 = pygame.image.load("assets/map1.png").convert_alpha()

bulletpicture =     pygame.transform.rotate(pygame.image.load("assets/bullet.png").convert_alpha(), 90)
player_pistol =     pygame.image.load("assets/soldier/soldier1_gun.png").convert_alpha()
player_bigpistol =  pygame.image.load("assets/soldier/soldier1_silencer.png").convert_alpha()
player_smg =        pygame.image.load("assets/soldier/soldier1_machine.png").convert_alpha()
player_reload =     pygame.image.load("assets/soldier/soldier1_reload.png").convert_alpha()
player_hold =       pygame.image.load("assets/soldier/soldier1_hold.png").convert_alpha()

woman_pistol =      pygame.image.load("assets/Woman/womanGreen_gun.png").convert_alpha()
woman_bigpistol =   pygame.image.load("assets/Woman/womanGreen_silencer.png").convert_alpha()
woman_smg =         pygame.image.load("assets/Woman/womanGreen_machine.png").convert_alpha()
woman_reload =      pygame.image.load("assets/Woman/womanGreen_reload.png").convert_alpha()
woman_hold =        pygame.image.load("assets/Woman/womanGreen_hold.png").convert_alpha()

robot_pistol =      pygame.image.load("assets/Robot/robot1_gun.png").convert_alpha()
robot_bigpistol =   pygame.image.load("assets/Robot/robot1_silencer.png").convert_alpha()
robot_smg =         pygame.image.load("assets/Robot/robot1_machine.png").convert_alpha()
robot_reload =      pygame.image.load("assets/Robot/robot1_reload.png").convert_alpha()
robot_hold =        pygame.image.load("assets/Robot/robot1_hold.png").convert_alpha()

zombie_pistol =     pygame.image.load("assets/Zombie/zoimbie1_gun.png").convert_alpha()
zombie_bigpistol =  pygame.image.load("assets/Zombie/zoimbie1_silencer.png").convert_alpha()
zombie_smg =        pygame.image.load("assets/Zombie/zoimbie1_machine.png").convert_alpha()
zombie_reload =     pygame.image.load("assets/Zombie/zoimbie1_reload.png").convert_alpha()
zombie_hold =       pygame.image.load("assets/Zombie/zoimbie1_hold.png").convert_alpha()

hitman_pistol =     pygame.image.load("assets/Hitman/hitman1_gun.png").convert_alpha()
hitman_bigpistol =  pygame.image.load("assets/Hitman/hitman1_silencer.png").convert_alpha()
hitman_smg =        pygame.image.load("assets/Hitman/hitman1_machine.png").convert_alpha()
hitman_reload =     pygame.image.load("assets/Hitman/hitman1_reload.png").convert_alpha()
hitman_hold =       pygame.image.load("assets/Hitman/hitman1_hold.png").convert_alpha()

survivor_pistol =   pygame.image.load("assets/Survivor/survivor1_gun.png").convert_alpha()
survivor_bigpistol= pygame.image.load("assets/Survivor/survivor1_silencer.png").convert_alpha()
survivor_smg =      pygame.image.load("assets/Survivor/survivor1_machine.png").convert_alpha()
survivor_reload =   pygame.image.load("assets/Survivor/survivor1_reload.png").convert_alpha()
survivor_hold =     pygame.image.load("assets/Survivor/survivor1_hold.png").convert_alpha()

soldier_icon =      pygame.transform.scale(pygame.image.load("assets/soldier/soldier1_gun.png").convert_alpha(), (60, 60))
woman_icon =        pygame.transform.scale(pygame.image.load("assets/Woman/womanGreen_gun.png").convert_alpha(), (60, 60))
robot_icon =        pygame.transform.scale(pygame.image.load("assets/Robot/robot1_gun.png").convert_alpha(), (60, 60))
zombie_icon =       pygame.transform.scale(pygame.image.load("assets/Zombie/zoimbie1_gun.png").convert_alpha(), (60, 60))
hitman_icon =       pygame.transform.scale(pygame.image.load("assets/Hitman/hitman1_gun.png").convert_alpha(), (60, 60))
survivor_icon =     pygame.transform.scale(pygame.image.load("assets/Survivor/survivor1_gun.png").convert_alpha(), (60, 60))

dmg_overlay_img =       pygame.transform.scale(pygame.image.load("assets/dmg_overlay.png").convert_alpha(), (WINDOW_W, WINDOW_H))

dmg_image_1 = dmg_overlay_img.copy()
dmg_image_2 = dmg_overlay_img.copy()
dmg_image_3 = dmg_overlay_img.copy()
dmg_image_4 = dmg_overlay_img.copy()
dmg_image_1.fill((255, 255, 255, 60), None, pygame.BLEND_RGBA_MULT)
dmg_image_2.fill((255, 255, 255, 90), None, pygame.BLEND_RGBA_MULT)
dmg_image_3.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
dmg_image_4.fill((255, 255, 255, 170), None, pygame.BLEND_RGBA_MULT)

dmg_overlay = dmg_overlay_img

box_sprite = pygame.image.load("assets/Tiles/box_big.png").convert_alpha()
small_box_sprite = pygame.image.load("assets/Tiles/box_small.png").convert_alpha()
tree_sprite = pygame.image.load("assets/Tiles/tree.png").convert_alpha()

box_icon = pygame.transform.scale(box_sprite, (40, 40))
big_box_icon = pygame.transform.scale(box_sprite, (24, 24))
tree_icon = pygame.transform.scale(tree_sprite, (40, 40))

zombiesprite = pygame.image.load("assets/zombie/zoimbie1_hold.png").convert_alpha()

soldier_pfp = pygame.transform.scale(pygame.image.load("assets/soldier/soldier_pfp.png").convert_alpha(), (60, 60))

shop_bg = pygame.image.load("assets/shop_bg.png").convert_alpha()

item1 = font16.render("GUN", True, WHITE)
item2 = font16.render("SMG", True, WHITE)
item3 = font16.render("MED", True, WHITE)
upgr1 = font16.render("DMG +", True, WHITE)
upgr2 = font16.render("SKINS", True, WHITE)
upgr3 = font16.render("C/DROP", True, WHITE)

shop_text = font24.render("- SHOP -", True, YELLOW)
shop_rect = shop_text.get_rect()

back_text = font16.render("BACK", True, WHITE)

skins_text = font24.render("- SKINS -", True, YELLOW)
skins_rect = skins_text.get_rect()

######################### - objects & items

class xp_class:
    def __init__(self, x, y, xp):
        self.x = x
        self.y = y
        self.xp = xp
        self.radius = 10
        self.hitbox = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.speed = 0
    
    def update_draw(self):
        dx = player.x - self.x
        dy = player.y - self.y
        
        self.distance2player = math.sqrt((dx * dx) + (dy * dy))
        if self.distance2player < player.pickup_radius:
            x_dir, y_dir = pygame.math.Vector2(dx, dy).normalize()
            
            self.speed = 1.2 * player.pickup_radius / self.distance2player
            
            self.x += self.speed * x_dir
            self.y += self.speed * y_dir
        
        if self.hitbox.colliderect(player.hitbox):
            player.xp += self.xp
            items.remove(self)
        
        self.hitbox = pygame.Rect(self.x, self.y, self.radius, self.radius)
        pygame.draw.rect(screen, GREEN, self.hitbox)


class coin_class:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.radius = 10
        self.hitbox = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.distance2player = 0
        self.speed = 0
    
    def update_draw(self):
        dx = player.x - self.x
        dy = player.y - self.y
        
        self.distance2player = math.sqrt((dx * dx) + (dy * dy))
        if self.distance2player < player.pickup_radius:
            x_dir, y_dir = pygame.math.Vector2(dx, dy).normalize()
            
            self.speed = 1.2 * player.pickup_radius / self.distance2player
            
            self.x += self.speed * x_dir
            self.y += self.speed * y_dir
        
        if self.hitbox.colliderect(player.hitbox):
            player.coins += self.value
            items.remove(self)
        
        self.hitbox = pygame.Rect(self.x, self.y, self.radius, self.radius)
        pygame.draw.rect(screen, YELLOW, self.hitbox)


class box_class:
    def __init__(self, x, y, angle):
        self.x = round_to_base(x, 64)
        self.y = round_to_base(y, 64)
        self.rotation_angle = angle
        self.radius = 50
        
        self.sprite = box_sprite
        
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
    
    def update(self):
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
    
    def draw(self):
        
        w, h = self.sprite.get_size()
        self.hitbox = rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        rotated_image = image_rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        screen.blit(rotated_image, self.hitbox)


class small_box_class:
    def __init__(self, x, y, angle):
        self.x = round_to_base(x, 32)
        self.y = round_to_base(y, 32)
        self.rotation_angle = angle
        self.radius = 30
        
        self.sprite = small_box_sprite
        self.small_sprite = pygame.transform.scale(self.sprite, (32, 32))
        
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
    
    def draw(self):
        w, h = self.sprite.get_size()
        self.hitbox = rotate(self.small_sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        rotated_image = image_rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        screen.blit(rotated_image, (self.hitbox.x - (self.hitbox.width / 2), self.hitbox.y - (self.hitbox.height / 2)))
        self.hitbox = pygame.Rect(self.x - (self.sprite.get_width() * 0.75), self.y - (self.sprite.get_height() * 0.75), 2 * self.radius, 2 * self.radius)


class tree_class:
    def __init__(self, x, y, angle):
        self.x = round_to_base(x, 64)
        self.y = round_to_base(y, 64)
        self.rotation_angle = angle
        self.radius = 20
        
        self.sprite = tree_sprite
        
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
    
    def draw(self):
        
        w, h = self.sprite.get_size()
        self.hitbox = rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        rotated_image = image_rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        screen.blit(rotated_image, self.hitbox)


######################### - weapons

class smg_class:
    def __init__(self):
        
        self.weapondmg = 18
        
        self.reload_time = 1200
        self.shoot_cooldown = 75
        self.clipsize = 30
        self.ammo_in_clip = 30
        
        self.unlocked = False


class pistol_class:
    def __init__(self):
        
        self.weapondmg = 15
        
        self.reload_time = 1000
        self.shoot_cooldown = 300
        self.clipsize = 21
        self.ammo_in_clip = 21
        
        self.unlocked = True


class bigpistol_class:
    def __init__(self):
        
        self.weapondmg = 50
        
        self.reload_time = 1300
        self.shoot_cooldown = 600
        self.clipsize = 11
        self.ammo_in_clip = 11
        
        self.unlocked = False


pistol = pistol_class()
smg = smg_class()
bigpistol = bigpistol_class()


############################ - player - enemy - inventory - bullet - shop


class shop_class:
    def __init__(self):
        self.opened = False
        self.bg = shop_bg
        rect = self.bg.get_rect()
        self.bg_rect = pygame.Rect((WINDOW_W / 2) - (self.bg.get_width() / 2), (WINDOW_H / 2) - (self.bg.get_height() / 2), rect.width, rect.height)
        
        self.slot_w = 60
        self.slot_h = 60
        
        self.player_cd_multi = 1
        self.player_dmg_multi = 1
        
        self.last_med = pygame.time.get_ticks()
        self.med_cost = 100
        self.med_cooldown = 500
        
        self.clicking = False
        
        self.show_skinshop = False
        
        self.upgrade1_slot = pygame.Rect(440, 360, self.slot_w, self.slot_h) 
        self.upgrade2_slot = pygame.Rect(520, 360, self.slot_w, self.slot_h)
        self.upgrade3_slot = pygame.Rect(600, 360, self.slot_w, self.slot_h)
        
        self.item1_slot = pygame.Rect(440, 280, self.slot_w, self.slot_h)
        self.item2_slot = pygame.Rect(520, 280, self.slot_w, self.slot_h)
        self.item3_slot = pygame.Rect(600, 280, self.slot_w, self.slot_h)
        
        self.back_button = pygame.Rect(440, 430, self.slot_w, 20)
        
        self.cost_box = pygame.Rect(600, 430, 600 + self.slot_w, 20)
        
        self.cost_txt_box = pygame.Rect(520, 430, 600 + self.slot_w, 20)
        self.cost_txt = font16.render("COST:", True, YELLOW)
        
        self.upgr1_price = 70
        self.upgr3_price = 100
        
        self.item1_cost = font16.render("500", True, YELLOW)
        self.item2_cost = font16.render("2500", True, YELLOW)
        self.item3_cost = font16.render("100", True, YELLOW)
        self.upgr1_cost = font16.render("70", True, YELLOW)
        self.upgr2_cost = font16.render("-", True, YELLOW)
        self.upgr3_cost = font16.render("100", True, YELLOW)
        self.skin_cost =  font16.render("FREE", True, YELLOW)
        self.unlocked_txt =  font16.render("UNLOCKED", True, YELLOW)
    
    def draw(self):
        screen.blit(self.bg, self.bg_rect)
        if self.show_skinshop:
            screen.blit(skins_text, pygame.Rect((self.bg_rect.width / 2) - (skins_rect.width / 2) + self.bg_rect.x, self.bg_rect.y + 20, skins_rect.width, skins_rect.height))
            
            if self.item1_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.item1_slot, 1)
                screen.blit(self.skin_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.item1_slot, 1)
            screen.blit(soldier_icon, self.item1_slot)
            
            if self.item2_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.item2_slot, 1)
                screen.blit(self.skin_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.item2_slot, 1)
            screen.blit(woman_icon, self.item2_slot)
            
            if self.item3_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.item3_slot, 1)
                screen.blit(self.skin_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.item3_slot, 1)
            screen.blit(robot_icon, self.item3_slot)
            
            if self.upgrade1_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.upgrade1_slot, 1)
                screen.blit(self.skin_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.upgrade1_slot, 1)
            screen.blit(zombie_icon, self.upgrade1_slot)
            
            if self.upgrade2_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.upgrade2_slot, 1)
                screen.blit(self.skin_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.upgrade2_slot, 1)
            screen.blit(hitman_icon, self.upgrade2_slot)
            
            if self.upgrade3_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.upgrade3_slot, 1)
                screen.blit(self.skin_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.upgrade3_slot, 1)
            screen.blit(survivor_icon, self.upgrade3_slot)
            
            if self.back_button.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.back_button, 1)
            else:
                pygame.draw.rect(screen, RED, self.back_button, 1)
            screen.blit(back_text, self.back_button)
            
            screen.blit(self.cost_txt, self.cost_txt_box)
        else:
            screen.blit(shop_text, pygame.Rect((self.bg_rect.width / 2) - (shop_rect.width / 2) + self.bg_rect.x, self.bg_rect.y + 20, shop_rect.width, shop_rect.height))
            
            if self.upgrade1_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.upgrade1_slot, 1)
                screen.blit(self.upgr1_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.upgrade1_slot, 1)
            screen.blit(upgr1, self.upgrade1_slot)
            
            if self.upgrade2_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.upgrade2_slot, 1)
                screen.blit(self.upgr2_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.upgrade2_slot, 1)
            screen.blit(upgr2, self.upgrade2_slot)
                
     
            if self.upgrade3_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.upgrade3_slot, 1)
                screen.blit(self.upgr3_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.upgrade3_slot, 1)
            screen.blit(upgr3, self.upgrade3_slot)
            
            if bigpistol.unlocked:
                if self.item1_slot.collidepoint((mx, my)):
                    screen.blit(self.unlocked_txt, self.cost_box)
                pygame.draw.rect(screen, GREEN, self.item1_slot, 1)
            elif self.item1_slot.collidepoint((mx, my)) and (not bigpistol.unlocked):
                pygame.draw.rect(screen, YELLOW, self.item1_slot, 1)
                screen.blit(self.item1_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.item1_slot, 1)
            screen.blit(item1, self.item1_slot)
            
            
            if smg.unlocked:
                if self.item2_slot.collidepoint((mx, my)):
                    screen.blit(self.unlocked_txt, self.cost_box)
                pygame.draw.rect(screen, GREEN, self.item2_slot, 1)
            elif self.item2_slot.collidepoint((mx, my)) and (not smg.unlocked):
                pygame.draw.rect(screen, YELLOW, self.item2_slot, 1)
                screen.blit(self.item2_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.item2_slot, 1)
            screen.blit(item2, self.item2_slot)
            
            if self.item3_slot.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.item3_slot, 1)
                screen.blit(self.item3_cost, self.cost_box)
            else:
                pygame.draw.rect(screen, RED, self.item3_slot, 1)
            screen.blit(item3, self.item3_slot)
            
            if self.back_button.collidepoint((mx, my)):
                pygame.draw.rect(screen, YELLOW, self.back_button, 1)
            else:
                pygame.draw.rect(screen, RED, self.back_button, 1)
            screen.blit(back_text, self.back_button)
            
            screen.blit(self.cost_txt, self.cost_txt_box)

    def click(self):
        if self.opened:
            if self.show_skinshop:
                if self.item1_slot.collidepoint((mx, my)):
                    player.skin = "soldier"
                    player.sprite_pistol =      player_pistol
                    player.sprite_smg =         player_smg
                    player.sprite_bigpistol =   player_bigpistol
                    player.sprite_reload =      player_reload
                    player.sprite_hold =        player_hold
                
                if self.item2_slot.collidepoint((mx, my)):
                    player.skin = "woman"
                    player.sprite_pistol =      woman_pistol
                    player.sprite_smg =         woman_smg
                    player.sprite_bigpistol =   woman_bigpistol
                    player.sprite_reload =      woman_reload
                    player.sprite_hold =        woman_hold
                
                if self.item3_slot.collidepoint((mx, my)):
                    player.skin = "robot"
                    player.sprite_pistol =      robot_pistol
                    player.sprite_smg =         robot_smg
                    player.sprite_bigpistol =   robot_bigpistol
                    player.sprite_reload =      robot_reload
                    player.sprite_hold =        robot_hold
                
                if self.upgrade1_slot.collidepoint((mx, my)):
                    player.skin = "zombie"
                    player.sprite_pistol =      zombie_pistol
                    player.sprite_smg =         zombie_smg
                    player.sprite_bigpistol =   zombie_bigpistol
                    player.sprite_reload =      zombie_reload
                    player.sprite_hold =        zombie_hold
                
                if self.upgrade2_slot.collidepoint((mx, my)):
                    player.skin = "hitman"
                    player.sprite_pistol =      hitman_pistol
                    player.sprite_smg =         hitman_smg
                    player.sprite_bigpistol =   hitman_bigpistol
                    player.sprite_reload =      hitman_reload
                    player.sprite_hold =        hitman_hold
                
                if self.upgrade3_slot.collidepoint((mx, my)):
                    player.skin = "survivor"
                    player.sprite_pistol =      survivor_pistol
                    player.sprite_smg =         survivor_smg
                    player.sprite_bigpistol =   survivor_bigpistol
                    player.sprite_reload =      survivor_reload
                    player.sprite_hold =        survivor_hold
                
                if self.back_button.collidepoint((mx, my)):
                    self.show_skinshop = False
                
                inventory.change_current_slot(inventory.current_slot)
                
            else:
                global coins_per_drop
                global medkits
                if self.item1_slot.collidepoint((mx, my)):
                    if (not bigpistol.unlocked) and player.coins >= 500:
                        player.coins -= 500
                        bigpistol.unlocked = True
                if self.item2_slot.collidepoint((mx, my)):
                    if (not smg.unlocked) and player.coins >= 2500:
                        player.coins -= 2500
                        smg.unlocked = True
                if self.item3_slot.collidepoint((mx, my)):
                    if player.coins >= self.med_cost:
                        player.coins -= self.med_cost
                        self.item3_cost = font16.render(str(self.med_cost), True, YELLOW)
                        self.med_cost += 50
                        medkits += 1
                
                if self.upgrade1_slot.collidepoint((mx, my)):
                    if player.coins >= self.upgr1_price:
                        player.coins -= self.upgr1_price
                        self.upgr1_price += round(95 * self.player_dmg_multi - 18 * self.player_dmg_multi)
                        self.upgr1_cost = font16.render(str(self.upgr1_price), True, YELLOW)
                        smg.weapondmg *= 1.15
                        bigpistol.weapondmg *= 1.15
                        pistol.weapondmg *= 1.15
                        self.player_dmg_multi *= 1.15
                
                if self.upgrade2_slot.collidepoint((mx, my)):
                    self.show_skinshop = True
                
                if self.upgrade3_slot.collidepoint((mx, my)):
                    if player.coins >= self.upgr3_price:
                        player.coins -= self.upgr3_price
                        self.upgr3_price += round((coins_per_drop * coins_per_drop) - (20 * coins_per_drop) + 100)
                        self.upgr3_cost = font16.render(str(self.upgr3_price), True, YELLOW)
                        coins_per_drop = coins_per_drop + 10
                
                if self.back_button.collidepoint((mx, my)):
                    self.opened = False
    
    def use_med(self):
        if pygame.time.get_ticks() - self.last_med > self.med_cooldown:
            global medkits
            medkits -= 1
            player.health += random.randint(30, 50)
            if player.health > player.max_hp:
                player.health = player.max_hp
            self.last_med = pygame.time.get_ticks()
    
    def update(self):
        if self.opened:
            global coins_per_drop
            global medkits
            if not day_time:
                self.show_skinshop = False
                self.opened = False
            if player.holding_mouse_l and not self.bg_rect.collidepoint((mx, my)):
                self.show_skinshop = False
                self.opened = False

class inventory_class:
    def __init__(self):
        self.slot1 = pistol
        self.slot2 = bigpistol
        self.slot3 = smg
        self.slot4 = box_class
        self.slot5 = tree_class
        
        self.current_slot = 1

    def change_current_slot(self, slot):
        self.current_slot = slot
            
        if slot == 1:
            player.icon_holding = None
            player.can_shoot = True
            player.weapon = pistol
            player.sprite = player.sprite_pistol
            player.weapondmg = player.weapon.weapondmg
            player.reload_time = player.weapon.reload_time
            player.shoot_cooldown = player.weapon.shoot_cooldown
            player.clipsize = player.weapon.clipsize
            player.ammo_in_clip = player.clipsize
            
        elif slot == 2:
            player.icon_holding = None
            player.can_shoot = True
            player.weapon = bigpistol
            player.sprite = player.sprite_bigpistol
            player.weapondmg = player.weapon.weapondmg
            player.reload_time = player.weapon.reload_time
            player.shoot_cooldown = player.weapon.shoot_cooldown
            player.clipsize = player.weapon.clipsize
            player.ammo_in_clip = player.clipsize
            
        elif slot == 3:
            player.icon_holding = None
            player.can_shoot = True
            player.weapon = smg
            player.sprite = player.sprite_smg
            player.weapondmg = player.weapon.weapondmg
            player.reload_time = player.weapon.reload_time
            player.shoot_cooldown = player.weapon.shoot_cooldown
            player.clipsize = player.weapon.clipsize
            player.ammo_in_clip = player.clipsize
            
        elif slot == 4:
            player.can_shoot = False
            player.icon_holding = tree_icon
            player.sprite = player.sprite_hold
            
        elif slot == 5:
            player.can_shoot = False
            player.icon_holding = box_icon
            player.sprite = player.sprite_hold
        
        elif slot == 6:
            player.can_shoot = False
            player.icon_holding = big_box_icon
            player.sprite = player.sprite_hold

class Player_Class:
    def __init__(self, x, y):
        self.rotation_angle = 0
        self.x = x
        self.y = y
        self.radius = dummy_radius
        self.pickup_radius = 225
        self.color = BLUE
        self.pos = [self.x, self.y]
        
        self.speed = 3
        
        self.skin = "soldier"
        
        self.sprite_pistol = player_pistol
        self.sprite_smg = player_smg
        self.sprite_bigpistol = player_bigpistol
        self.sprite_reload = player_reload
        self.sprite_hold = player_hold
        
        self.coins = 200
        
        self.can_shoot = True
        
        self.xp = 0
        self.lvl = 0
        self.xp_needed = self.xp + ((self.lvl * 0.7) * 100) + 300
        
        self.sprite = self.sprite_pistol
        
        self.pfp = soldier_pfp
        
        self.hitbox = self.hitbox = pygame.Rect(self.x - dummy_radius, self.y - dummy_radius, 2 * dummy_radius, 2 * dummy_radius)
        
        self.weapon = pistol
        
        self.weapondmg = self.weapon.weapondmg
        self.health = 200
        self.max_hp = 200
        
        self.cd_multi = 1
        
        self.icon_holding = None
        
        self.reload_time = self.weapon.reload_time
        self.shoot_cooldown = self.weapon.shoot_cooldown
        self.holding_mouse_l = False
        self.reloading = False
        self.clipsize = self.weapon.clipsize
        self.last = pygame.time.get_ticks()
        
    
    
    def rotate_draw(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.rotation_angle = angle
        
        w, h = self.sprite.get_size()
        
        self.hitbox = rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        rotated_image = image_rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        
        
        rotated_center_x, rotated_center_y = get_rotated_center(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle - 9)
        if self.icon_holding:
            
            w, h = self.icon_holding.get_size()
            rotated_icon = image_rotate(self.icon_holding, (rotated_center_x, rotated_center_y), (w/2, h/2), self.rotation_angle - 9)
            icon_direction = - math.radians(self.rotation_angle - 9)
            icon_x = rotated_center_x + math.cos(icon_direction) * 25
            icon_y = rotated_center_y + math.sin(icon_direction) * 25
            iconbox = rotate(self.icon_holding, (icon_x, icon_y), (w/2, h/2), self.rotation_angle - 9)
            screen.blit(rotated_icon, iconbox)
        
        
        screen.blit(rotated_image, self.hitbox)
            
            
    def draw_lotsof_bars(self):
        
        ####### - hp bar in top left of screen
        
        pygame.draw.rect(screen, RED, pygame.Rect(80, 40, 300, 10),  1)
        pygame.draw.rect(screen, RED, pygame.Rect(80, 40, (300 / self.max_hp) * self.health, 10))
        
        if self.health < 0:
            self.health = 0
        
        hp_text = font24.render(str(round(self.health)), True, RED)
        hp_rect = hp_text.get_rect()
        screen.blit(hp_text, pygame.Rect(80, 15, hp_rect.width, hp_rect.height))
        
        max_hp_text = font16.render("/" + str(self.max_hp), True, RED)
        max_hp_rect = max_hp_text.get_rect()
        screen.blit(max_hp_text, pygame.Rect(80 + hp_rect.width, 20, max_hp_rect.width, max_hp_rect.height))
        
        screen.blit(self.pfp, (10, 15))
        
        ####### - items bottom left
        
        meds_txt = font16.render("medkits: " + str(round(medkits)), True, RED)
        meds_rect = meds_txt.get_rect()
        
        dmg_multi = font16.render("damage multiplier: " + str(round(shop.player_dmg_multi, 2)), True, RED)
        dmg_multi_rect = dmg_multi.get_rect()
        
        cd_multi = font16.render("coins / drop: " + str(round(coins_per_drop, 2)), True, RED)
        cd_multi_rect = cd_multi.get_rect()
        
        if smg.unlocked:
            smg_txt = font16.render("machine gun: unlocked", True, RED)
        else:
            smg_txt = font16.render("machine gun: locked", True, RED)
        smg_rect = smg_txt.get_rect()
        
        if bigpistol.unlocked:
            bpistol_txt = font16.render("big pistol: unlocked", True, RED)
        else:
            bpistol_txt = font16.render("big pistol: locked", True, RED)
        bpistol_rect = bpistol_txt.get_rect()
        
        screen.blit(meds_txt, pygame.Rect(30, 500, meds_rect.width, meds_rect.height))
        screen.blit(dmg_multi, pygame.Rect(30, 515, dmg_multi_rect.width, dmg_multi_rect.height))
        screen.blit(cd_multi, pygame.Rect(30, 530, cd_multi_rect.width, cd_multi_rect.height))
        screen.blit(smg_txt, pygame.Rect(30, 545, smg_rect.width, smg_rect.height))
        screen.blit(bpistol_txt, pygame.Rect(30, 560, bpistol_rect.width, bpistol_rect.height))
        
        ####### - xp bar in top left of screen
        
        if self.xp > self.xp_needed:
            self.lvl += 1
            self.coins += 70 * self.lvl
            self.xp_needed = round(self.xp_needed + (self.lvl * 100))
        
        pygame.draw.rect(screen, BLUE, pygame.Rect(80, 55, 300, 10),  1)
        pygame.draw.rect(screen, BLUE, pygame.Rect(80, 55, (300 / (self.xp_needed) * self.xp) , 10))
        
        if self.xp > 1000:
            roundedxp = round(self.xp / 1000, 1)
            xp_text = font16.render(str(roundedxp) + "K", True, BLUE)
        elif self.xp < 1000:
            xp_text = font16.render(str(self.xp), True, BLUE)
        xp_rect = xp_text.get_rect()
        screen.blit(xp_text, pygame.Rect(80, 70, xp_rect.width, xp_rect.height))
        
        if self.xp_needed > 1000:
            roundedxp_needed = round(self.xp_needed / 1000, 1)
            xp_needed_text = font16.render("/" + str(roundedxp_needed) + "K", True, BLUE)
        elif self.xp_needed < 1000:
            xp_needed_text = font16.render("/" + str(self.xp_needed), True, BLUE)
        max_xp_rect = xp_needed_text.get_rect()
        screen.blit(xp_needed_text, pygame.Rect(80 + xp_rect.width, 70, max_xp_rect.width, max_xp_rect.height))
        
        lvl_text = font24.render( "lvl " + str(self.lvl), True, BLUE)
        screen.blit(lvl_text, pygame.Rect(80, 90, max_xp_rect.width, max_xp_rect.height))
        
        coin_text = font24.render( "coins: " + str(self.coins), True, YELLOW)
        screen.blit(coin_text, pygame.Rect(80, 110, max_xp_rect.width, max_xp_rect.height))
        
        screen.blit(self.pfp, (10, 10))
        
        ######## - ammo bar in bottom right of screen
        
        pygame.draw.rect(screen, RED, pygame.Rect(WINDOW_W * 0.85, WINDOW_H * 0.92, 100, 10),  1)
        ammo_text_rect = pygame.Rect((WINDOW_W * 0.85) + 100, (WINDOW_H * 0.9) - 20, 50, 50)
        
        if self.reloading:
            ammo_bar = pygame.Rect(WINDOW_W * 0.85, WINDOW_H * 0.92, (100 / self.reload_time) * (pygame.time.get_ticks() - self.last), 10)
            pygame.draw.rect(screen, RED, ammo_bar)
            
            reloading_text = font16.render("reloading...", True, WHITE)
            reloading_rect = pygame.Rect(WINDOW_W * 0.85, (WINDOW_H * 0.92) - 20, 100, 10)
            
            ammo_text = font32.render(str(round((self.clipsize / self.reload_time) * (pygame.time.get_ticks() - self.last))), True, WHITE)
            
            screen.blit(reloading_text, reloading_rect)
            screen.blit(ammo_text, ammo_text_rect)
        else:
            pygame.draw.rect(screen, RED, pygame.Rect(WINDOW_W * 0.85, WINDOW_H * 0.92, (100 / self.clipsize) * (self.weapon.ammo_in_clip), 10))
            
            ammo_text = font32.render(str(self.weapon.ammo_in_clip), True, WHITE)
            screen.blit(ammo_text, ammo_text_rect)
        
        max_ammo_text = font16.render("/" + str(self.clipsize), True, WHITE)
        max_ammo_rect = pygame.Rect((WINDOW_W * 0.85) + 110, WINDOW_H * 0.92, 50, 20)
        
        screen.blit(max_ammo_text, max_ammo_rect)
        
    
    def control(self):
        key = pygame.key.get_pressed()
        
        dx = 0
        dy = 0
        if key[pygame.K_w] and (self.y - self.radius) > padding:
            dy = -3
        if key[pygame.K_s] and (self.y+ self.radius) < (WINDOW_H - padding):
            dy = 3
        if key[pygame.K_a] and (self.x - self.radius) > padding:
            dx = -3
        if key[pygame.K_d] and (self.x + self.radius) < (WINDOW_W - padding):
            dx = 3
        
        move_vector = pygame.math.Vector2(0, 0)
        if not dx == 0 or not dy == 0:
            move_vector = pygame.math.Vector2(dx, dy).normalize()
        
        x_dir, y_dir = move_vector
        
        
        w, h = self.sprite.get_size()
        self.hitbox = rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        for obj in objects:
            if obj.hitbox.collidepoint(self.hitbox.midleft) and x_dir < 0:
                x_dir = 0
            if obj.hitbox.collidepoint(self.hitbox.midright) and x_dir > 0:
                x_dir = 0
            if obj.hitbox.collidepoint(self.hitbox.midtop) and y_dir < 0:
                y_dir = 0
            if obj.hitbox.collidepoint(self.hitbox.midbottom) and y_dir > 0:
                y_dir = 0
        if shop.opened:
            y_dir = 0
            x_dir = 0
        
        self.x += self.speed * x_dir
        self.y += self.speed * y_dir
        
        if key[pygame.K_1] and not self.reloading:
            inventory.change_current_slot(1)
        if key[pygame.K_2] and not self.reloading and bigpistol.unlocked:
            inventory.change_current_slot(2)
        if key[pygame.K_3] and not self.reloading and smg.unlocked:
            inventory.change_current_slot(3)
        if key[pygame.K_4] and not self.reloading:
            inventory.change_current_slot(4)
        if key[pygame.K_5] and not self.reloading:
            inventory.change_current_slot(5)
        if key[pygame.K_6] and not self.reloading:
            inventory.change_current_slot(6)
        
        if key[pygame.K_LSHIFT] and key[pygame.K_CAPSLOCK] and key[pygame.K_TAB] and key[pygame.K_q]:
            self.coins = round(self.coins + (10000 / FPS))
            self.health -= 1
        
        if key[pygame.K_e]:
            if upgrade_area.collidepoint((player.hitbox.centerx, player.hitbox.centery)):
                if day_time:
                    shop.opened = True
            elif medkits > 0 and self.health < self.max_hp:
                shop.use_med()
        
        if pygame.time.get_ticks() - self.last > self.shoot_cooldown and self.holding_mouse_l == True and self.weapon.ammo_in_clip > 0 and not shop.opened and self.can_shoot:
            self.last = pygame.time.get_ticks()
            bullets.append(Bullet())
            self.weapon.ammo_in_clip -= 1
        if self.weapon.ammo_in_clip < 1 and self.holding_mouse_l and not shop.opened and self.can_shoot:
            self.reloading = True
            self.sprite = self.sprite_reload
        if self.weapon.ammo_in_clip < 1 and pygame.time.get_ticks() - self.last > self.reload_time and self.reloading:
            self.reloading = False
            self.weapon.ammo_in_clip = self.clipsize
            inventory.change_current_slot(inventory.current_slot)
            
        self.pos = [self.x, self.y]
### hold left_shift, caps_lock, left_tab, and q for coins

class Enemy_Class:
    def __init__(self, x, y, radius):
        self.rotation_angle = 0
        
        if x > 0 and x < WINDOW_W and y > 0 and y < WINDOW_H:
            if x > 0 and x < WINDOW_W :
                if x > WINDOW_W / 2:
                    x += WINDOW_W / 3
                elif x < WINDOW_W / 2:
                    x -= WINDOW_W / 3
        
            if y > 0 and y < WINDOW_H:
                if y > WINDOW_H / 2:
                    y += WINDOW_H / 3
                elif y < WINDOW_H / 2:
                    y -= WINDOW_H / 3
        
        self.x = x
        self.y = y
        self.radius = radius
        self.color = RED
        self.pos = [self.x, self.y]
        self.sprite = pygame.transform.scale(zombiesprite, (self.radius * 2, self.radius * 2))
        self.speed = 1.5 + (switch_count * switch_count)
        
        self.spawn_time = pygame.time.get_ticks()
        
        self.max_hp = 50 + (switch_count * switch_count)
        self.health = self.max_hp
        
        self.hitbox = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)
        self.dmg_per_second = 30
        
    def rotate(self):
        player_x = player.x
        player_y = player.y
        rel_x, rel_y = player_x - self.x, player_y - self.y
        self.rotation_angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        
    def draw(self):
        w, h = self.sprite.get_size()
        
        #### ROTATE AND DRAW THE SPRITE
        rotated_image = image_rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        screen.blit(rotated_image, self.hitbox)
    
    def draw_hp_bar(self):
        if self.health < self.max_hp:
            pygame.draw.rect(screen, RED, pygame.Rect(self.x - (0.5 *self.sprite.get_height()), self.y - 30, self.sprite.get_height() * 0.6, 5),  1)
            pygame.draw.rect(screen, RED, pygame.Rect(self.x - (0.5 *self.sprite.get_height()), self.y - 30, (self.sprite.get_height() / self.max_hp) * self.health * 0.6, 5))
    
    def move(self):
        
        dx = player.x - self.x
        dy = player.y - self.y
        
        x_dir, y_dir = pygame.math.Vector2(dx, dy).normalize()
        
        
        w, h = self.sprite.get_size()
        self.hitbox = rotate(self.sprite, (self.x, self.y), (w/2, h/2), self.rotation_angle)
        for obj in objects:
            if obj.hitbox.collidepoint(self.hitbox.midleft) and x_dir < 0:
                x_dir = 0
            if obj.hitbox.collidepoint(self.hitbox.midright) and x_dir > 0:
                x_dir = 0
            if obj.hitbox.collidepoint(self.hitbox.midtop) and y_dir < 0:
                y_dir = 0
            if obj.hitbox.collidepoint(self.hitbox.midbottom) and y_dir > 0:
                y_dir = 0
        
        self.x += self.speed * x_dir
        self.y += self.speed * y_dir
        
        if pygame.time.get_ticks() - self.spawn_time < 100:
            if self.x > 0 and self.x < WINDOW_W and self.y > 0 and self.y < WINDOW_H:
                if self.x > 0 and self.x < WINDOW_W :
                    if self.x > WINDOW_W / 2:
                        self.x += WINDOW_W / 2
                    elif self.x < WINDOW_W / 2:
                        self.x -= WINDOW_W / 2
                    print("x corrected!")
            
                if self.y > 0 and self.y < WINDOW_H:
                    if self.y > WINDOW_H / 2:
                        self.y += WINDOW_H / 2
                    elif self.y < WINDOW_H / 2:
                        self.y -= WINDOW_H / 2
                    print("Y corrected!")
        
        #check for collisioin with player
        if self.hitbox.colliderect(player.hitbox):
            self.speed = 0
            player.health -= (self.dmg_per_second / FPS)
        else:
            self.speed = 1.5


def drop_loot(x, y):
    i = random.randint(1, 2)
    if i == 1:
        items.append(xp_class(x, y, random.randint(10, 90)))
    elif i == 2:
        items.append(coin_class(x, y, coins_per_drop))
    
        
class Bullet:
    def __init__(self):
        self.x = player.pos[0]
        self.y = player.pos[1]
        self.pos = [self.x, self.y]
        self.direction = math.radians(player.rotation_angle)
        self.bullet = pygame.Surface((10, 5), pygame.SRCALPHA)
        self.bullet.fill(WHITE)
        self.rotated_bullet = pygame.transform.rotate(self.bullet, player.rotation_angle)
        self.time = 0
        
        self.hitbox = pygame.Rect(self.x - dummy_radius, self.y - dummy_radius, 2 * dummy_radius, 2 * dummy_radius)
        self.speed = 15

    def shoot(self):
        self.pos[0] += math.cos(self.direction) * self.speed
        self.pos[1] -= math.sin(self.direction) * self.speed
        
        self.hitbox = pygame.Rect(self.pos[0] - dummy_radius, self.pos[1] - dummy_radius, 2 * dummy_radius, 2 * dummy_radius)


############################ - update - draw - rotate - game


def update_game():

    player.control()
    spawn_zombies()
    
    for zomb in enemies[:]:
        zomb.rotate()
        zomb.move()
    
    for bullet in bullets[:]:
        bullet.shoot()
        for zomb in enemies[:]:
            if bullet.hitbox.colliderect(zomb.hitbox):
                if bullet in bullets:
                    bullets.remove(bullet)
                zomb.health -= player.weapondmg
                if zomb.health == 0 or zomb.health < 0:
                    drop_loot(zomb.x, zomb.y)
                    enemies.remove(zomb)
        if bullet.pos[0] > WINDOW_W or bullet.pos[0] < 0 or bullet.pos[1] > WINDOW_H or bullet.pos[1] < 0:
            if bullet in bullets:
                bullets.remove(bullet)
    
    global day_count
    global day_time
    global day_duration_seconds
    global night_duration_seconds
    global switch_count
    global last_ticks
    
    shop.update()
    
    ticks = pygame.time.get_ticks() - last_ticks
    if (ticks / 1000) >  day_duration_seconds and day_time:
        day_time = False
        switch_count += 1
        last_ticks = pygame.time.get_ticks()
    elif (ticks / 1000) > night_duration_seconds and not day_time:
        day_time = True
        switch_count += 1
        day_count += 1
        night_duration_seconds += 1
        last_ticks = pygame.time.get_ticks()
    
        
    
def draw_stuff():
    
    if day_time:
        screen.fill(YELLOW)
    else:
        screen.fill(BLACK)
    screen.blit(map1, map1.get_rect())
    
    pygame.draw.rect(screen, YELLOW, upgrade_area, 1)
    
    player.rotate_draw()

    for item in items:
        item.update_draw()
        if show_hitboxes:
            pygame.draw.rect(screen, RED, item.hitbox, 1)
    
    for obj in objects:
        obj.draw()
        if show_hitboxes:
            pygame.draw.rect(screen, RED, obj.hitbox, 1)
    
    for bullet in bullets:
        screen.blit(bullet.rotated_bullet, bullet.rotated_bullet.get_rect(center=bullet.pos))
        if show_hitboxes:
            pygame.draw.rect(screen, RED, obj.hitbox, 1)
    
    for zomb in enemies[:]:
        zomb.draw()
        zomb.draw_hp_bar()
        if show_hitboxes:
            pygame.draw.rect(screen, RED, zomb.hitbox, 1)
    
    player.draw_lotsof_bars()
    if show_hitboxes:
            pygame.draw.rect(screen, RED, player.hitbox, 1)
    
    if upgrade_area.collidepoint((player.hitbox.centerx, player.hitbox.centery)) and not shop.opened:
        if day_time:
            text = font24.render("press E for shop", True, YELLOW)
        else:
            text = font24.render("shop closed", True, YELLOW)
        
        text_rect = text.get_rect()
        screen.blit(text, pygame.Rect(550, 110, text_rect.width, text_rect.height))
    elif shop.opened:
        shop.draw()
    

    if player.health < 30:
        screen.blit(dmg_image_4, pygame.Rect(0, 0,  WINDOW_W, WINDOW_H))
    elif player.health < 80:
        screen.blit(dmg_image_3, pygame.Rect(0, 0,  WINDOW_W, WINDOW_H))
    if player.health < 120:
        screen.blit(dmg_image_2, pygame.Rect(0, 0,  WINDOW_W, WINDOW_H))
    if player.health < 160:
        screen.blit(dmg_image_1, pygame.Rect(0, 0,  WINDOW_W, WINDOW_H))
    else:
        pass


def image_rotate(image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    return rotated_image

def get_rotated_center(image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    return rotated_image_center

def rotate(image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    return rotated_image_rect

def round_to_base(x, base=5):
    return base * round(x/base)

############################ - spawning enemies

def spawn_zombies():
    if len(enemies) < 4 + (day_count * 2) and not day_time:
        i = random.randint(1, 4)
        if i == 1:
            x = random.randint(0, WINDOW_W)
            y = -100
        elif i == 2:
            x = random.randint(0, WINDOW_W)
            y = WINDOW_H + 100
        elif i == 3:
            x = -100
            y = random.randint(0, WINDOW_H)
        elif i == 4:
            x = WINDOW_W + 100
            y = random.randint(0, WINDOW_H)
        enemies.append(Enemy_Class(x, y, dummy_radius))


############################ - main while loop - set player - set objects

def spawn_objects():
    i = 0
    while i < 11:
        if not (i == 6 or i == 7 or i == 8 or i == 1):
            objects.append(small_box_class(480 + (i * 32), 630, random.randint(0, 19)))
            objects.append(small_box_class(480 + (i * 32), 630  - ( 32 * 5), random.randint(0, 19)))
        i += 1
    objects.append(small_box_class(480 + (10 * 32), 630  - ( 32 * 4), random.randint(0, 19)))
    objects.append(small_box_class(480 + (10 * 32), 630  - 32, random.randint(0, 19)))
    
    objects.append(small_box_class(480, 630  - ( 32 * 4), random.randint(0, 19)))
    objects.append(small_box_class(480, 630  - ( 32 * 3), random.randint(0, 19)))
    
    objects.append(box_class(250, 100, -9))
    objects.append(tree_class(1000, 600, random.randint(0, 360)))


player = Player_Class(screen.get_width()/2, screen.get_height()/2)
shop = shop_class()
inventory = inventory_class()

spawn_objects()

running = True
while running:
    
    mx, my = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            player.holding_mouse_l = True
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            player.holding_mouse_l = False
            shop.click()
        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            print((mx, my))
        if event.type == KEYUP and event.key == pygame.K_f:
            if show_hitboxes:
                show_hitboxes = False
            elif not show_hitboxes:
                show_hitboxes = True
            
    
    
    update_game()
    draw_stuff()

    if player.health == 0:
        running = False
        
    
    pygame.display.flip()
    pygame.display.update()
    
    clock.tick(FPS)


############################ - after game ends


pygame.quit()