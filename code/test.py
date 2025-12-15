import pygame, time, math, random
from pygame.locals import *
pygame.init()

WINDOW_W = 1100
WINDOW_H = 700

FPS = 60

YELLOW = (255, 255, 100)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 237, 255)
GREEN = (0, 255, 0)
RED = (179, 21, 21)
GRAY = (158, 158, 158)

screen = pygame.display.set_mode([ WINDOW_W, WINDOW_H])
pygame.display.set_caption("PWS spel")
clock = pygame.time.Clock()

padding = 10
dummy_radius = 21

map1 = pygame.image.load("assets/map1.png").convert_alpha()

player_pistol =     pygame.image.load("assets/soldier/soldier1_gun.png").convert_alpha()

def update_game():
    player.control()

def draw_stuff():
    screen.fill(YELLOW)
    screen.blit(map1, map1.get_rect())
    
    player.draw()
    


class Player_Class:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x - dummy_radius, self.y - dummy_radius, 2 * dummy_radius, 2 * dummy_radius)
        self.speed = 3
        self.radius = dummy_radius
        
    
    def draw(self):
        self.hitbox = pygame.Rect(self.x - dummy_radius, self.y - dummy_radius, 2 * dummy_radius, 2 * dummy_radius)
        screen.blit(player_pistol, self.hitbox)
    
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
        
        self.x += self.speed * x_dir
        self.y += self.speed * y_dir
        

player = Player_Class(100, 100)

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

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    update_game()
    draw_stuff()
    
    pygame.display.flip()
    pygame.display.update()
    
    clock.tick(FPS)

pygame.quit()