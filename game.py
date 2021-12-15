import pygame, math
from random import randint, uniform
from pygame import time
from pygame.locals import *
import ctypes
import cv2
import numpy

# 게임에 핵심적인 기능만 주석을 넣었습니다 ##
# 초기화
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
# 해상도
WIDTH = 1080
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH,HEIGHT))
screen_rect = screen.get_rect()
bgm_num = 0
# 소리 초기설정, 불러오기
pygame.mixer.set_num_channels(16)

def play_game():
    
    global WIDTH, HEIGHT, screen
    
    # 이미지 불러오기
    bullet_image = pygame.image.load('Image\Bullets.png').convert_alpha()
    bg_image = pygame.image.load('Image\Bg1.png').convert()
    bg2_image = pygame.image.load('Image\Bg2.png').convert()
    pkmon_image = pygame.image.load('Image\pokemon.png').convert_alpha()
    background_img = pygame.image.load('Image\\background.jpg').convert()
    menu_img = pygame.image.load('Image\Menus.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    player_slow_img = pygame.Surface((64, 64), pygame.SRCALPHA)
    player_slow_img.blit(bullet_image, (0,0), Rect(128,128,64,64))
    player_slow_img = pygame.transform.scale(player_slow_img, (64*2, 64*2))

    sfx_volume = 0.1
    music_volume = 0.5
    pygame.mixer.music.load('Music\BGM\Shoot the Bullet - Tengu is Watching.wav')
    pygame.mixer.music.set_volume(music_volume)

    s_lazer1 = pygame.mixer.Sound('Music\SFX\se_lazer00.wav')
    s_lazer1.set_volume(sfx_volume)
    s_tan1 = pygame.mixer.Sound('Music\SFX\se_tan00.wav')
    s_tan1.set_volume(sfx_volume)
    s_tan2 = pygame.mixer.Sound('Music\SFX\se_tan01.wav')
    s_tan2.set_volume(sfx_volume)
    s_ch2 = pygame.mixer.Sound('Music\SFX\se_ch02.wav')
    s_ch2.set_volume(sfx_volume+0.2)
    s_ch0 = pygame.mixer.Sound('Music\SFX\se_ch00.wav')
    s_ch0.set_volume(sfx_volume+0.2)
    s_cat1 = pygame.mixer.Sound('Music\SFX\se_cat00.wav')
    s_cat1.set_volume(sfx_volume+0.2)
    s_enep1 = pygame.mixer.Sound('Music\SFX\se_enep01.wav')
    s_enep1.set_volume(sfx_volume)
    s_enep2 = pygame.mixer.Sound('Music\SFX\se_enep02.wav')
    s_enep2.set_volume(sfx_volume+0.2)
    s_slash = pygame.mixer.Sound('Music\SFX\se_slash.wav')
    s_slash.set_volume(sfx_volume+0.2)
    s_pldead = pygame.mixer.Sound('Music\SFX\se_pldead00.wav')
    s_pldead.set_volume(sfx_volume)
    s_plst0 = pygame.mixer.Sound('Music\SFX\se_plst00.wav')
    s_plst0.set_volume(sfx_volume-0.1)
    s_damage0 = pygame.mixer.Sound('Music\SFX\se_damage00.wav')
    s_damage0.set_volume(sfx_volume)
    s_damage1 = pygame.mixer.Sound('Music\SFX\se_damage01.wav')
    s_damage1.set_volume(sfx_volume)
    s_graze = pygame.mixer.Sound('Music\SFX\se_graze.wav')
    s_graze.set_volume(sfx_volume)
    s_kira0 = pygame.mixer.Sound('Music\SFX\se_kira00.wav')
    s_kira0.set_volume(sfx_volume+0.2)
    s_kira1 = pygame.mixer.Sound('Music\SFX\se_kira01.wav')
    s_kira1.set_volume(sfx_volume)
    s_boom = pygame.mixer.Sound('Music\SFX\se_enep02.wav')
    s_boom.set_volume(sfx_volume+0.2)

    # 플레이어
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y, speed, health):
            pygame.sprite.Sprite.__init__(self) # 초기화?
            self.image = pygame.Surface((256, 256), pygame.SRCALPHA) # 이미지          
            self.image.blit(pokemons[0],(0,-10)) # 이미지 위치조정
            self.rect = self.image.get_rect(center = (round(x), round(y)))
            self.image2 = self.image.copy()
            self.img_num = 0
            self.pos = (x,y)
            
            self.speed = speed
            self.health = health

            self.count = 0
            self.radius = 4 # 원 충돌범위를 위한 반지름 값
            self.godmod = False # 무적?
            self.hit_speed = 0
            self.hit_dir = 0

        def update(self,collide):

            dx, dy = 0 , 0
            keys = pygame.key.get_pressed() 
            inum = self.img_num

            # 플레이어 이동 조종 SHIFT 를 누르면 느리게 움직이기
            if keys[pygame.K_LSHIFT]:
                self.speed = 2
            else:
                self.speed = 5
            
            if keys[pygame.K_RIGHT]:
                dx += 0 if self.rect.centerx >= WIDTH-20 else self.speed
            if keys[pygame.K_LEFT]:
                dx -= 0 if self.rect.centerx <= 0 + 20 else self.speed
            if keys[pygame.K_DOWN]:
                dy += 0 if self.rect.centery >= 720-20 else self.speed
            if keys[pygame.K_UP]:
                dy -= 0 if self.rect.centery <= 0+20 else self.speed

            if keys[pygame.K_RIGHT]:
                self.img_num = 1
            elif keys[pygame.K_LEFT]:
                self.img_num = 2
            else:
                self.img_num = 0
            
            if inum != self.img_num:
                if self.img_num == 0:
                    self.image = self.image2
                if self.hit_speed == 0:
                    if self.img_num == 1:
                        self.image = pygame.transform.rotate(self.image2, -10)
                    if self.img_num == 2:
                        self.image = pygame.transform.rotate(self.image2, 10)
                self.rect = self.image.get_rect(center = (round(self.pos[0]),round(self.pos[1])))

            # 탄에 닿았을때
            if len(collide) > 0 and not self.godmod:
                s_pldead.play()
                self.godmod = True
                self.count = 0
                self.health -= 60
                # self.hit_speed = collide[0].speed
                # self.hit_dir = collide[0].direction
            
            # 무적이면 2초뒤 풀리기
            if self.godmod:
                if self.count >= 120:
                    self.godmod = False
            
            # 넉백
            if self.hit_speed != 0:
                self.pos = calculate_new_xy(self.pos, self.hit_speed, self.hit_dir)
                if self.pos[0] <= 20: self.pos[0] = 20 
                if self.pos[0] >= WIDTH-20: self.pos[0] = WIDTH-20 
                if self.pos[1] <= 20: self.pos[1] = 20 
                if self.pos[1] >= HEIGHT-20: self.pos[1] = HEIGHT-20 
                if self.count >= 60:
                    self.hit_dir = 0
                    self.hit_speed = 0
            else:
                self.pos = (self.pos[0] + dx, self.pos[1] + dy)  
            
            self.rect.center = round(self.pos[0]), round(self.pos[1]) 
            self.count += 1

    # 플레이어 총
    class Beam(pygame.sprite.Sprite):
        def __init__(self, x, y, speed, dir=0):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((20, 16), pygame.SRCALPHA)  
            self.image.fill((200,200,200))
                
            self.image_sample = self.image.copy()
            self.rect = self.image.get_rect(center = (x, y))
            self.pos = (x, y)
            self.speed = speed
            self.direction = dir
            self.image_rotate = pygame.transform.rotate(self.image_sample, self.direction)
            self.damage = 2.5

            

        def update(self):
            
            # 화면 나가면 삭제
            if self.pos[0] >= WIDTH:
                self.kill()

            self.image_rotate = pygame.transform.rotate(self.image_sample, self.direction)
            self.image = self.image_rotate
            self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
            self.rect.center = round(self.pos[0]), round(self.pos[1]) 

    # 적
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, dir, speed, health, img, hit_cir, num):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((256, 256), pygame.SRCALPHA)      

            pokemonimg = pokemons[img-1] # 이미지
                        
            self.image.blit(pokemonimg,(0,0))
            self.rect = self.image.get_rect(center = (x, y))
            self.radius = hit_cir
            self.pos = (x, y)
            pygame.draw.circle(self.image, (200,0,0), (128,128), self.radius, 3)

            self.count = 0
            self.list = [0,0,0,0]
            self.health = health
            self.num = num

            # 적이동을 위한 값
            self.move_dir = dir
            self.move_speed = speed

            self.screen_apper = False

        def update(self):
            global score

            # 능력
            self.pos, self.move_dir, self.move_speed = enemy_attack(self.num, self.count, self.pos, self.move_dir, self.move_speed)

            if not screen_rect.colliderect(self.rect) and self.screen_apper: # 밖으로 나가면 사라지기
                self.kill() 
            if screen_rect.colliderect(self.rect) and not self.screen_apper:
                self.screen_apper = True
            if self.health <= 0: # 체력 다 달면 죽기
                s_tan1.play()
                self.kill()
            self.count += 1
            self.rect.center = self.pos    
    # 총알
    ############################################
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction, speed, bul, col, mod, num=(0,0)):
            # 이미지
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.transform.scale2x(bullets[bul][col])        
            self.image2 = self.image.copy() # 이미지 회전을 위한 이미지 복사
            self.add_dir = 0
            self.move_fun = False
            # 쓸 값
            self.rect = self.image.get_rect(center = (x, y))
            self.pos = (x, y)
            self.direction = direction
            self.speed = speed
            self.radius = bullet_size[bul]
            self.count = 0
            self.mod = mod
            self.num = num
            self.grazed = True
            self.lotate = False if bul == 2 or bul == 3 or bul==11 or bul == 12 or bul == 15 or bul == 10 or bul == 14 or bul == 19 else True   
            if self.lotate: 
                self.image = pygame.transform.rotate(self.image2, self.direction-90)
                self.rect = self.image.get_rect(center = self.pos)
            
        def update(self, screen):
            global score
            global time_stop
            screen_die = 0
            mod, sub = math.trunc(self.mod), (self.mod*10)%10
            direc = self.direction


            #모드 값이 있으면 탄 속성 변화###############################################
            if True:
                if mod == 0 and sub == 1:
                    screen_die = 1
                if mod == 1:
                    if sub == 0:
                        if not small_border.collidepoint(self.pos) and self.count == 0:
                            self.direction = look_at_point(self.pos,player.pos)
                            self.count = 1
                            self.speed = 2
                    if sub == 1:
                        if self.pos[0] <= player.pos[0] and self.count == 0:
                            self.direction = look_at_point(self.pos,player.pos)
                            if self.direction>0:
                                self.direction = 90
                            else:
                                self.direction = -90
                            self.count = 1
                if mod == 2:
                    if sub == 0:
                        self.direction = look_at_point(self.pos, enemy.pos)
                        if self.rect.collidepoint(enemy.pos):
                            self.kill()
                    if sub == 1:
                        screen_die = 1
                        if not small_border.collidepoint(self.pos):
                            rand_pos = (self.pos[0] + randint(-90,90),self.pos[1] + randint(-90,90))
                            rand_num = randint(0,90)
                            s_tan1.play(loops=1, maxtime=50)
                            for i in range(0,360,90):                       
                                bullet(rand_pos,i+rand_num,12,6,4,2.2)
                            self.kill()
                    if sub == 2:
                        screen_die = 1
                        self.count += 1
                        if self.count <= self.speed:
                            self.speed -= 0.1
                        elif self.count <= 90:
                            self.speed = 0
                        elif self.count <= 91:
                            bullet(self.pos,self.direction,4,4,3)
                        else:
                            self.speed = 6
                if mod == 3:
                    if enemy.list[1] == 1:
                        rand_int = randint(0,90)
                        for i in range(0,360,120):
                            bullet(self.pos,i+rand_int,3,9,6)       
                        self.kill()
                if mod == 4:
                    if sub == 0:
                        if not small_border.collidepoint(self.pos):
                            shape = (2,11,15,18)
                            play_sound(s_boom,1,1)
                            for j in range(0,720,20):
                                bullet((self.pos[0]+j,self.pos[1]),90,round(uniform(6,10),2),shape[randint(0,3)],1,4.1)
                                bullet((self.pos[0]+j,self.pos[1]),-90,round(uniform(6,10),2),shape[randint(0,3)],1,4.1) 
                                bullet((self.pos[0]-j,self.pos[1]),90,round(uniform(6,10),2),shape[randint(0,3)],1,4.1)
                                bullet((self.pos[0]-j,self.pos[1]),-90,round(uniform(6,10),2),shape[randint(0,3)],1,4.1)
                                if j % 40 == 0:  
                                    bullet((self.pos[0]+j,self.pos[1]),90,round(uniform(6,10),2),11,0,4.2)
                                    bullet((self.pos[0]+j,self.pos[1]),-90,round(uniform(6,10),2),11,0,4.2)
                                    bullet((self.pos[0]-j,self.pos[1]),90,round(uniform(6,10),2),11,0,4.2)
                                    bullet((self.pos[0]-j,self.pos[1]),-90,round(uniform(6,10),2),11,0,4.2)
                            self.kill()
                    if sub == 1:
                        screen_die = 1
                        if self.speed >= -3 : self.speed -= 0.1
                    if sub == 2:
                        screen_die = 1
                        if self.speed >= 3 : self.speed -= 0.1
                if mod == 5:  
                    screen_die = 1  
                    if self.count == 60: self.pos = calculate_new_xy(player.pos,100,self.direction*-1)
                    if self.count == 90:
                        self.image2 = pygame.transform.scale2x(bullets[9][6])
                        self.image = pygame.transform.rotate(self.image2, self.direction-90) 
                    if self.count >= 90:
                        if self.speed >= -5: self.speed -= 0.1
                    self.count += 1
                if mod == 6:
                    if sub == 0:
                        if distance(self.pos,player.pos) <= 200 and self.count == 0:
                            s_kira1.play(loops = 0, maxtime = 100)
                            self.image2 = pygame.transform.scale2x(bullets[4][3])
                            self.image = pygame.transform.rotate(self.image2, self.direction-90)   
                            self.speed /= 2
                            self.count += 1
                    if sub == 1:
                        self.count += self.speed/10
                        self.speed = 0
                        self.count += 1
                        if self.count > 0:
                            bullet(self.pos,self.direction,(self.count - int(self.count))*15,0,7)                   
                        if self.count > 20:
                            self.kill()
                if mod == 8:
                    if sub == 0:
                        if distance(self.pos,enemy.list[0]) < 50 and self.speed != 0:
                            self.speed -= 1
                        if self.speed <= 2:
                            if self.count == 0:
                                s_enep2.play()
                                for i in range(0,360,15):
                                    bullet(self.rect.center,i+self.count,5,15,4)
                            if while_time(self.count,10):
                                for i in range(0,360,45):
                                    bullet(self.rect.center,i+self.count+min_dir,5,18,4)
                            if while_time(self.count,30):
                                s_tan1.play()
                                for i in range(0,360,45):
                                    bullet(self.rect.center,i+self.count*2,3,12,4)
                            self.count += 1
                            if self.count == 120:
                                self.kill()
                if mod == 9:
                    if when_time(self.count, 0):
                        self.pos = calculate_new_xy(self.pos,40,-self.direction)
                        self.count = 1
                    self.pos = (self.pos[0] +self.num[0], self.pos[1] +self.num[1])
                    if self.speed <= 4:
                        self.speed += 0.1
                    # if when_time(self.count,60) and not self.move_fun:
                    #     self.move_fun = True
                    #     self.count = 0
                    #     self.count += look_at_point(enemy.pos,self.pos)
                    #     self.count2 = distance(self.pos, enemy.pos)
                    # if self.move_fun:
                    #     self.pos = move_circle(enemy.pos,self.count,self.count2)
                    #     self.pos = (self.pos[0] -self.count3, self.pos[1])
                    #     self.count3 += 2
                    # self.count += 1
                if mod == 10:
                    if sub == 0:
                        if enemy.list[0] == 1:
                            self.direction = look_at_point(self.pos,enemy.pos)
                            if self.speed <= 5:
                                self.speed += 0.1
                            if distance(self.pos,enemy.pos) <= 10:
                                self.kill()
                    if sub == 1:
                        screen_die = 1
                        self.count += 1
                        if self.count == 45 or not small_border.collidepoint(self.pos):
                            for i in range(0,360,30):
                                bullet(self.pos,i+self.count,4,2,2,0.1)
                            for i in range(0,360,20):
                                bullet(self.pos,i+self.count,3,4,2,0.1)
                            for i in range(0,360,10):
                                bullet(self.pos,i+self.count,2,11,2,0.1)
                            for i in range(0,360,90):
                                for j in range(0,5):
                                    bullet(self.pos,look_at_point(self.pos,player.pos)+20-10*j+i,5,17,2,0.1)
                            self.kill()
                if mod == 11:
                    if sub == 0:
                        if self.speed >= 0 and self.count <= 120:
                            self.speed -= 0.1            
                        if self.count == 60:
                            self.image2 = pygame.transform.scale2x(bullets[16][self.num[0]])
                            self.image = pygame.transform.rotate(self.image2, self.direction-90)
                            self.rect = self.image.get_rect(center = self.pos) 
                        self.count += 1
                        if while_time(self.count,60) and self.count <= 120:
                            self.speed = self.num[1]
                            self.direction = look_at_point(self.pos,player.pos) + randint(-40,40)
                            self.rect = self.image.get_rect(center = self.pos)
                        if while_time(self.count,30) and self.count >=120 and distance(self.pos,player.pos) >= 40:
                            bullet(self.pos,self.direction,0,2,self.num[0],11.1)
                    if sub == 1:
                        self.count += 1
                        if self.count >= 120 and self.speed <= 7:
                            self.speed += 0.1
                if mod == 12:
                    if sub == 0:
                        if self.count <= 40:
                            self.direction -= 5
                        else:
                            self.kill()
                        self.pos = (self.pos[0] +self.num[0], self.pos[1] +self.num[1])
                    if sub == 1:
                        self.direction -= 0.4
                    if sub == 2:
                        self.direction += 0.4
                    self.count += 1
                if mod == 15:
                    if distance(self.pos,player.pos) <= 300 and self.count == 0:
                        self.speed /= 2
                        self.count += 1
                    if distance(self.pos,enemy.list[0]) <= 150 and time_stop:
                        s_tan1.play()
                        for i in range(0,360,30):
                            bullet(calculate_new_xy(self.pos, 64, -i),i,2,1,5)
                        for i in range(0,360,30):
                            bullet(calculate_new_xy(self.pos, 32, -i),i,3,12,5)
                        self.kill()
                if mod == 16:
                    if sub == 0:
                        if self.count <= 60:
                            self.direction -= 2
                        else:
                            self.direction += 2
                        
                        if self.count == 120:
                            self.count = 0
                    if sub == 1:
                        if self.count <= 60:
                            self.direction += 2
                        else:
                            self.direction -= 2 
                        if self.count == 120:
                            self.count = 0
                    if sub == 2:
                        if self.speed > 0 and self.count < 90:
                            self.speed -= 0.1
                        if self.count == 90:
                            self.speed = 4
                            self.direction = look_at_point(self.pos,player.pos)
                    self.count += 1 
                if mod == 17:
                    if sub == 0:
                        if enemy.list[1] != self.num[1] :
                            self.move_fun = True 
                        else:
                            self.move_fun = False
                if mod == 18:
                    screen_die = 1
                    if sub == 0:
                        self.count += 1
                        if self.speed <= 7 and self.count >= 120:
                            self.speed += 0.1
                    if sub == 1:
                        if self.speed <= 7 and enemy.list[1] > 0:
                            self.speed += 0.03
                    if sub == 2:
                        
                        if self.count >=15 and not self.speed == 0:
                            self.speed = 0
                        else:
                            self.count += 1
                        if enemy.list[1] > 0:
                            self.speed = 4
            
            ################################################
                        
            if direc != self.direction and self.lotate:# 각도 계산후 위치 업데이트
                self.image = pygame.transform.rotate(self.image2, self.direction-90)
                self.rect = self.image.get_rect(center = (round(self.pos[0]),round(self.pos[1])))     
            if not self.move_fun and not time_stop:
                self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
            self.rect.center = round(self.pos[0]), round(self.pos[1]) 
            dist = distance(self.pos,player.pos)

            # 플레이어가 탄을 스치면 추가점수
            if self.grazed and dist <= 50 and not player.godmod:
                s_graze.play()
                score += score_setting[3]
                self.grazed = False        
            # 화면에 없으면 없애기
            
            if screen_die == 0 and not small_border.colliderect(self.rect):            
                self.kill()
            if screen_die == 1 and not bullet_border.colliderect(self.rect):
                self.kill()
    ############################################

    class MagicField(pygame.sprite.Sprite):
        def __init__(self, pos, direction, speed, col, mod, screen_die = 0):
            # 이미지
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            
            # 쓸 값
            self.rect = self.image.get_rect(center = pos)
            self.pos = pos
            self.direction = direction
            self.speed = speed
            self.radius = 8
            self.count = 0
            self.count2 = 1
            self.mod = mod
            self.screen_die = screen_die

            if not self.mod == 18:
                pygame.draw.circle(self.image, col, (32,32), 32)
            pygame.transform.rotate(self.image, direction)

        def update(self, screen):
            mod, sub = math.trunc(self.mod), (self.mod*10)%10
            subxy = self.pos
            if mod == 9:
                if while_time(self.count,10):
                    for i in range(0,360,90):                    
                        bullet(self.pos, i+self.count,1,2,0,9,noreturn_xy(self.speed,-self.direction))
                self.count += 1
            if mod == 12:
                if self.count <= 60:
                    self.speed = 0
                elif self.count == 61:
                    s_boom.play()
                    self.speed = 6
                    randnum = randint(0,360)
                    for i in range(0,360,12):
                        bullet(enemy.pos,randnum+i,4,4,3,12.1)
                        bullet(enemy.pos,randnum+i,4,4,3,12.2)
                    randnum = randint(0,360)
                    for i in range(0,360,24):
                        bullet(enemy.pos,randnum+i,3,3,3,12.1)
                        bullet(enemy.pos,randnum+i,3,3,3,12.2)
                if while_time(self.count,5):
                    for i in range(0,360,90):
                        bullet(self.pos,i+self.count,8,1,4,12,noreturn_xy(self.speed,-self.direction))
                        bullet(self.pos,i+self.count+20,8,1,4,12,noreturn_xy(self.speed,-self.direction))
                        bullet(self.pos,i+self.count-20,8,1,4,12,noreturn_xy(self.speed,-self.direction))
                self.count += 1
            if mod == 18:
                self.count2  += 1
                self.count += 1
                if self.count2 >= 325: 
                    self.count2 -= 650
                    enemy.list[1] = 2
                if sub == 0:
                    self.pos = move_circle(enemy.pos,enemy.count*3+self.direction,self.count2*2)
                    if while_time(self.count,4) and not distance(self.pos,enemy.pos) <= 200:
                        s_tan1.play(loops=1,maxtime=micro_sec(4))
                    if self.count2 < 0 and while_time(self.count,4):
                        s_kira0.play(loops=1,maxtime=micro_sec(4))

                    if self.count2 < 0 and distance(self.pos,enemy.pos) <= 50:
                        enemy.list[1] = 1
                        self.kill() 
                if sub == 1:        
                    self.pos = move_circle(enemy.pos,enemy.count*3+self.direction,self.count2*2)                
                    if self.count2 < 0 and distance(self.pos,enemy.pos) <= 50:
                        self.kill()
                    if while_time(self.count,4) and not distance(self.pos,enemy.pos) <= 200:
                        if self.count2 >= 0 and distance(self.pos,player.pos) > 30:
                            bullet(self.pos,look_at_point(subxy,self.pos)+180,0,3,randint(1,3),18)
                    if while_time(self.count,4) and self.count2 < 0:
                        bullet(self.pos,look_at_point(self.pos,enemy.pos),6,1,randint(1,3),0.1)
                if sub == 2:        
                    self.pos = move_circle(enemy.pos,-(enemy.count*3+self.direction),self.count2*2)                
                    if self.count2 < 0 and distance(self.pos,enemy.pos) <= 50:
                        self.kill()
                    if while_time(self.count,2) and not distance(self.pos,enemy.pos) <= 200 and self.count <= 24:
                        if self.count2 >= 0 and distance(self.pos,player.pos) > 30:
                            bullet(self.pos,look_at_point(self.pos,enemy.pos),0,4,randint(5,7),18.1)
                    if self.count == 36:
                        self.count = 0
                    if while_time(self.count,5) and self.count2 < 0 and not distance(self.pos,player.pos) <= 50:
                        bullet(self.pos,look_at_point(self.pos,enemy.pos)+180,2,6,randint(5,7))
                    # if while_time(self.count,4) and self.count2 < 0:
                    #     bullet(self.pos,look_at_point(self.pos,enemy.pos),6,1,randint(1,3),0.1)
                if sub == 3:
                    li = (1,6,7)
                    self.pos = move_circle(enemy.pos,enemy.count*3+self.direction,self.count2*2)                
                    if self.count2 < 0 and distance(self.pos,enemy.pos) <= 50:
                        self.kill()
                    if while_time(self.count,2) and not distance(self.pos,enemy.pos) <= 200:
                        if self.count2 >= 0 and distance(self.pos,player.pos) > 30:
                            bullet(self.pos,look_at_point(self.pos,enemy.pos),7,9,li[randint(0,2)],18.2)
                    if while_time(self.count,2) and self.count2 < 0 and distance(self.pos,player.pos) > 30:
                        bullet(self.pos,look_at_point(self.pos,enemy.pos)+90,0,6,li[randint(0,2)],18.1)
                    if while_time(self.count,10) and self.count2 < 0 and distance(self.pos,player.pos) > 30:
                        bullet(self.pos,look_at_point(self.pos,enemy.pos),2,6,li[randint(0,2)],0.1)
                        bullet(self.pos,look_at_point(self.pos,enemy.pos)+20,2,6,li[randint(0,2)],0.1)
                        bullet(self.pos,look_at_point(self.pos,enemy.pos)-20,2,6,li[randint(0,2)],0.1)


            # 각도 계산후 위치 업데이트
            self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
            self.rect.center = round(self.pos[0]), round(self.pos[1]) 
                # 화면에 없으면 없애기
            if not bullet_border.colliderect(self.rect) and self.screen_die == 0:
                self.kill()
            
    ############################################


    def micro_sec(value):
        return round(1000/60)*value

    def big_small(val,min,max):
        return min < val and val < max

    def when_time(val,time):
        return val == time

    def while_time(val,time):
        return val % time == 0

    def bullet(pos,dir,speed,img,col,mode=0,num = (0,0)):
        spr.add(Bullet(pos[0],pos[1],dir,speed,img,col,mode,num))

    def magic_bullet(pos,dir,speed,col,mode=0,screend=0):
        magic_spr.add(MagicField(pos,dir,speed,col,mode,screend))

    def calculate_new_xy(old_xy, speed, angle_in_degrees):
        move_vec = pygame.math.Vector2()
        move_vec.from_polar((speed, angle_in_degrees))
        return old_xy + move_vec

    def noreturn_xy(speed, angle_in_degrees):
        move_vec = pygame.math.Vector2()
        move_vec.from_polar((speed, angle_in_degrees))
        return move_vec

    def distance(f_pos,sec_pos):
        if str(type(f_pos)) == "<class 'int'>": f_pos = (0,0)
        if str(type(sec_pos)) == "<class 'int'>": sec_pos = (0,0)
        return math.hypot(f_pos[0]-sec_pos[0], f_pos[1]-sec_pos[1])

    # 적 움직임
    def enemy_move(dir, speed, time):
        if not enemy.move_time > 0:
            enemy.move_dir = dir
            enemy.move_speed = speed
            enemy.move_time = time 

    # 소리
    def play_sound(sound,count,time,max=0):
        if when_time(count,time):
            sound.play(loops=0, maxtime=max)

    def move_circle(pos, angle,radius):
        return(round(pos[0]+math.cos(math.pi * (angle / 180)) * radius,2),round(pos[1]+math.sin(math.pi * (angle / 180)) * radius,2))


    # 두점 각도
    def look_at_point(fpos,secpos):
        x, y = fpos
        dx, dy = secpos
        angle = math.degrees(math.atan2(y - dy, dx - x))
        return angle 

    # 동그라미 게이지 (퍼옴)
    def drawArc(surf, color, center, radius, width, end_angle):
        circle_image = numpy.zeros((radius*2+4, radius*2+4, 4), dtype = numpy.uint8)
        circle_image = cv2.ellipse(circle_image, (radius+2, radius+2),
        (radius-width//2, radius-width//2), -90, 0, end_angle, (*color, 255), width, lineType=cv2.LINE_AA) 
        circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius*2+4, radius*2+4), 'RGBA')
        circle_surface = pygame.transform.flip(circle_surface, True,False)
        surf.blit(circle_surface, circle_surface.get_rect(center = (round(center[0]),round(center[1]))))

    def health_color(val):
        if val < 0.25:
            return (255,0,0)
        elif val < 0.5:
            return (255,255,0)
        else:
            return (0,255,0)

    # 이미지 나눠 저장하기
    a_list = []
    cur_list = []

    if True:
        for i in range (0,176,16):
            for j in range (0,128,16):
                image = pygame.Surface((16, 16), pygame.SRCALPHA)
                image.blit(bullet_image, (0,0), Rect(j,i,16,16))
                a_list.append(image)
            cur_list.append(a_list)
            a_list = []
        for i in range (192,201,8):
            for j in range (0,64,8):
                image = pygame.Surface((8, 8), pygame.SRCALPHA)
                image.blit(bullet_image, (0,0), Rect(j,i,8,8))
                a_list.append(image)
            cur_list.append(a_list)
            a_list = []
        for i in range (208,400,32):
            for j in range (0,256,32):
                image = pygame.Surface((32, 32), pygame.SRCALPHA)
                image.blit(bullet_image, (0,0), Rect(j,i,32,32))
                a_list.append(image)
            cur_list.append(a_list)
            a_list = []
        for i in range(0,4):
            image = pygame.Surface((64, 64), pygame.SRCALPHA)
            image.blit(bullet_image, (0,0), Rect(i*64,432,64,64))
            a_list.append(image)
            a_list.append(image)

    cur_list.append(a_list)
    a_list = []
    bullets = cur_list

    cur_list = []
    for i in range(0,10):
        for j in range(0,10):
            image = pygame.Surface((64, 64), pygame.SRCALPHA)
            image.blit(pkmon_image, (0,0), Rect(j*64,i*64,64,64))
            image = pygame.transform.scale(image,(128*2,128*2))
            cur_list.append(image)
    pokemons = cur_list

    # 개발자 전용
    stage_fun = 1
    global bkgd1, time_stop
    global stage_count
    # 초기 설정
    enemy_group = pygame.sprite.Group()
    play = True
    full_on = False
    cur_full_mod = False
    pause = False
    frame_count = 0
    min_dir = 0
    time_stop = False
    stage_count = 0
    
    
    global stage_line
    stage_line = 0
    global stage_cline
    stage_cline = 0
    global stage_repeat_count
    stage_repeat_count = 0

    # 게임 시작전 메뉴 변수들
    curser = 0
    curser_max = 4
    select_mod = 0
    menu_mod = -1
    difficulty = 0
    character = 0

    cur_screen = 0

    bullet_border_wide = 200
    bullet_border = Rect(0-bullet_border_wide, 0-bullet_border_wide, WIDTH + bullet_border_wide*2, HEIGHT + bullet_border_wide*2)
    small_border = Rect(0-64, 0-64, WIDTH + 64, HEIGHT + 64)
    bullet_size = (10,6,8,8,6,6,6,9,6,7,7,4,5,15,15,20,10,10,10,20)
    spr = pygame.sprite.Group()
    magic_spr = pygame.sprite.Group()
    player = Player(WIDTH/4,HEIGHT/2,5,500)
    player_group = pygame.sprite.Group(player)
    beams = pygame.sprite.Group()

    starting = True
    read_end = False

    clock = pygame.time.Clock()

    # 점수 코어
    global score
    score = 0
    score_setting = (10,10,987650,10,0,0,0,0,0)

    # 보스마다 기본설정
    bkgd1 = pygame.Surface((0, 0))

    bg_x = 0
    fps = 60

    #################################################

    # 게임의 배경, 스테이지
    def game_defalt_setting(fun):
        global bgm_num, bkgd1
        bkgd1 = pygame.Surface((640, 360))
        ##############################################
        if fun == 1:
            bgm = 1
            bkgd1.blit(bg2_image,(0,0),(540,0,540,360))
        if fun == 2:
            bgm = 1
        if fun == 3:
            bgm = 1
        if fun == 4:
            enemy_health = 500
            bgm = 1
        if fun == 5:
            enemy_health = 500
            bgm = 1
        if fun == 6:
            enemy_health = 500
            bgm = 1

        ###############################################

        bkgd1 = pygame.transform.scale2x(bkgd1)

        if bgm != bgm_num:
            
            pygame.mixer.music.stop()
            if bgm == 1:
                pygame.mixer.music.load('Music\BGM\Shoot the Bullet - Tengu is Watching.wav')
            if bgm == 2:
                pygame.mixer.music.load('Music\BGM\Shoot the Bullet -  Sleepless Night of the Eastern Country.wav')
            if bgm == 3:
                pygame.mixer.music.load('Music\BGM\Shoot the Bullet - Retrospective Kyoto.wav') 
            if bgm == 4:
                pygame.mixer.music.load('Music\BGM\동방영야초 - 라스트 워드 테마.wav')  
            bgm_num = bgm
            #pygame.mixer.music.play(-1)

    # 소환하는 적 
    def pokemon_spawn(val,x,y,time):
        global stage_count 
        global stage_line # 현재 조건의 라인
        global stage_cline # 검사 중인 라인
        
        # x, y, dir, speed, health, img, hit_cir, num
        if time == stage_count and stage_line == stage_cline:
            stage_count = 0
            stage_line += 1
            if val == 1:
                enemy_group.add(Enemy(x,y,180,4,5,11,30,1))  
            if val == 2:
                enemy_group.add(Enemy(x,y,180,4,5,12,30,2))  


        stage_cline += 1

    # 소환 반복 (줄에 stage_line)
    # stage_line -= 1
    # stage_repeat_count += 1
    def while_poke_spawn(time,repeat):
        global stage_cline, stage_line, stage_repeat_count, stage_count
        return stage_count == time and stage_line == stage_cline and stage_repeat_count < repeat

    def end_while_poke_spawn(line):
        global stage_line, stage_repeat_count
        stage_line -= line
        stage_repeat_count += 1
    # 적의 공격타입
    def enemy_attack(num,count,pos,dir,speed):
        if num == 1:
            pos = calculate_new_xy(pos, speed, dir)
            if dir > 90 and count > 20: dir -= 1 
            if speed > 5 and count > 20: speed -= 0.5
            if while_time(count,30):
                bullet(pos,look_at_point(pos,player.pos),9,2,1)
        if num == 2:
            pos = calculate_new_xy(pos, speed, dir)
            if dir < 270 and count > 30: dir += 1 
            if speed > 5 and count > 30: speed -= 0.5
            if while_time(count,30):
                bullet(pos,look_at_point(pos,player.pos),9,2,3)
        return pos,dir,speed

    # 스테이지
    def stage_manager():
        global stage_cline, stage_line, stage_repeat_count, stage_count
        
        if stage_fun == 1:

            pokemon_spawn(1,1112,-30,40)
            pokemon_spawn(1,1012,-30,10)
            pokemon_spawn(1,912,-30,10)

            if while_poke_spawn(10,10):
                pokemon_spawn(1,1112,-30,0)
                pokemon_spawn(1,1012,-30,0)
                pokemon_spawn(1,912,-30,0)
                end_while_poke_spawn(3)

            stage_cline = 0


    ################################################# 

    game_defalt_setting(stage_fun)

    # 폰트 불러오기
    score_font = pygame.font.Font('Font\SEBANG Gothic Bold.ttf', 50)


    # BGM 재생
    #pygame.mixer.music.play(-1)


    while play:
        # 60 프레임
        clock.tick(fps)
        # 키 이벤트
        if cur_screen == 1:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    play = False
                if ev.type == pygame.KEYDOWN:                    
                    if ev.key == pygame.K_f:
                        full_on = False if full_on == True else True
                    if ev.key == pygame.K_ESCAPE:
                        pause = False if pause == True else True
            keys = pygame.key.get_pressed()
            # 총 쏘기 이벤트
            if keys[pygame.K_z] and frame_count % 4 == 0 and not player.godmod and not pause:
                s_plst0.play(loops=1, maxtime=50)
                beams.add(Beam(player.pos[0]+5,player.pos[1]+10,40))
                beams.add(Beam(player.pos[0]+5,player.pos[1]-10,40))
                if frame_count % 1 == 0:
                    if keys[pygame.K_LSHIFT]:
                        beams.add(Beam(player.pos[0]+5,player.pos[1]+20,30,5))
                        beams.add(Beam(player.pos[0]+5,player.pos[1]-20,30,-5))
                    else:
                        beams.add(Beam(player.pos[0]+5,player.pos[1]+10,30,-10))
                        beams.add(Beam(player.pos[0]+5,player.pos[1]-10,30,10))
            if keys[pygame.K_x]: # 탄 소거
                fps = 30
            else:
                fps = 60
            
            # 탄에 박았는가
            hit_list = pygame.sprite.spritecollide(player, spr, not player.godmod, pygame.sprite.collide_circle)
            ehit_list = []
            beam_collide = pygame.sprite.groupcollide(beams, enemy_group, True, False, pygame.sprite.collide_circle)
            if beam_collide.items():
                for beam, enemy in beam_collide.items():
                    enemy[0].health -= 1

            if not pause:     
                if not starting or read_end: enemy_group.update(ehit_list)  
                if len(magic_spr.sprites()) != 0:magic_spr.update(screen)                  
                spr.update(screen)
            # 연산 업데이트
            if not time_stop:
                if not pause:
                    beams.update()                            
                    player_group.update(hit_list)
                    enemy_group.update()
                    stage_manager()
                    frame_count += 1
                    stage_count += 1
                    min_dir += 0.2
                    bg_x -= 3
                    rotated_sprite = pygame.transform.rotate(player_slow_img, math.degrees(frame_count/20))
                    rect = rotated_sprite.get_rect(center = (round(player.pos[0]), round(player.pos[1])))
                
            # 그리기 시작
            screen.fill((0,0,0))
            #배경 스크롤
            rel_x = bg_x % WIDTH
            screen.blit(bkgd1, (rel_x - WIDTH,0))
            if rel_x < WIDTH:
                screen.blit(bkgd1,(rel_x,0))

            # 점수 표시
            score_text = score_font.render(str(score).zfill(10), True, (255,255,255))
            screen.blit(score_text,(WIDTH-score_text.get_rect().width,0))
            
            # 원형 체력바 그리기
            if starting and not read_end: 
                # drawArc(screen, (0, 0, 0), enemy.pos, 112, 15, 360*100)
                # drawArc(screen, health_color(enemy.health/enemy_health), enemy.pos, 110, 10, 360*enemy.health/enemy_health)
                drawArc(screen, (0,0, 0), player.pos, 112, 15, 360*100)
                drawArc(screen, health_color(player.health/500), player.pos, 110, 10, 360*player.health/500)

            magic_spr.draw(screen)      
            beams.draw(screen)
            player_group.draw(screen)  
            enemy_group.draw(screen)
            
            if not starting or read_end: enemy_group.draw(screen)
            spr.draw(screen)
            

            # SHIFT 눌렀을때 특별한 원 보이기
            pygame.draw.circle(screen, (200,100,100), (round(player.pos[0]),round(player.pos[1])), 8)
            pygame.draw.circle(screen, (255,255,255), (round(player.pos[0]),round(player.pos[1])), 7)  
            if keys[pygame.K_LSHIFT]: 
                
                screen.blit(rotated_sprite, rect)
            pygame.display.flip()
        if cur_screen == 0:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    play = False
                if ev.type == pygame.KEYDOWN: 
                    if ev.key == pygame.K_UP:
                        curser = curser_max if curser == 0 else curser - 1
                    if ev.key == pygame.K_DOWN:
                        curser = 0 if curser == curser_max else curser + 1
                    if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                        if menu_mod == 3:
                            if curser == 0:
                                full_on = False if full_on == True else True
                        else:
                            if (curser == 1 or curser == 2) and select_mod == 0: break
                            if curser == 4 and select_mod == 0: play = False
                            select_mod += 1
                            if menu_mod == 0:
                                print(difficulty)
                                cur_screen = 1 ############ rpdlatlwks
                            menu_mod = curser
                            curser = 0
                    if ev.key == pygame.K_f:
                        full_on = False if full_on == True else True
                        
                        
                    if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                        if select_mod > 0: select_mod -= 1
                        menu_mod = -1
            screen.blit(background_img,(0,0))
            
            ui_x = WIDTH - 300
            ui_y = HEIGHT - 400
            if select_mod == 0:
                curser_max = 4
                screen.blit(menu_img,(0,0),(0,0,528,80))
                for i in range(0,5):
                    if curser == i:
                        screen.blit(menu_img,(ui_x,ui_y+70*i),(256,80+48*i,256,48))
                    else:
                        screen.blit(menu_img,(ui_x,ui_y+70*i),(0,80+48*i,240,48))
            if select_mod == 1:
                if menu_mod == 0: # 난이도 정하기
                    curser_max = 3
                    for i in range(0,4):
                        screen.blit(menu_img,(WIDTH/2-120,HEIGHT/2-60+128*i-128*curser),(0,320+64*i,288,64))
                        difficulty = curser
                if menu_mod == 3:
                    curser_max = 3
                    text_box = ["화면모드","음악","효과음","플레이어"]
                    text_box[0] = "화면모드    창모드" if full_on == 0 else "화면모드    전체화면"
                    text_box[1] = "음악   " + str(music_volume)
                    text_box[2] = "효과음  " + str(sfx_volume)
                    for i in range(0,4):
                        text_color = (255,0,255) if i == curser else (0,0,255)
                        text = score_font.render(text_box[i], True, text_color)
                        screen.blit(text,(200,200+80*i))
            pygame.display.flip()
        
        if full_on != cur_full_mod:
            if full_on:
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN|pygame.SCALED)
            else:
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
            cur_full_mod = full_on

    pygame.quit()
    exit()

if __name__ == "__main__":
    play_game()

