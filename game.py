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

    def shoot_pattern(count,num,list):
        global time_stop
        #################################
        if num == 1:
            if when_time(count,0):
                s_lazer1.play()
            if while_time(count,1):
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos)+10,27,0,1) 
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos)-10,27,0,1)   
            if while_time(count,30):
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos)+20,5,2,6,1) 
                bullet((enemy.pos[0],enemy.pos[1]+5),look_at_point(enemy.pos,player.pos)-20,5,2,6,1) 
            if while_time(count,50):
                s_tan1.play()
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos)+11,3,4,1,1.1) 
                bullet((enemy.pos[0],enemy.pos[1]+5),look_at_point(enemy.pos,player.pos)-11,3,4,1,1.1) 
            if while_time(count,100) and enemy.health <= 700:
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos),5,15,1) 
        if num == 2:
            if when_time(count,1):
                s_ch0.play()
                enemy_move(randint(0,360),5,20)
            if while_time(count,5) and count < 90:
                bullet((enemy.pos[0]+randint(-180,180),enemy.pos[1]+randint(-180,180)),0,6,3,4,2) 
                list[0] = look_at_point(enemy.pos,player.pos)
            if when_time(count,90):
                s_lazer1.play()
            if while_time(count,1) and big_small(count,90,120):
                bullet(enemy.pos,list[0],27,0,3,2.1)
            if when_time(count,180):
                s_kira0.play()
            if when_time(count,180):
                count = 0 
        if num == 3:
            if when_time(count,1):
                list[0] = look_at_point(enemy.pos,player.pos)
                list[1] = 0
            play_sound(s_lazer1,count,1)
            play_sound(s_lazer1,count,120)
            if while_time(count,1) and count <= 120:
                bullet(enemy.pos,list[0]+25,27,0,6,3)
                bullet(enemy.pos,list[0]-25,27,0,6,3)
                bullet(enemy.pos,list[0]+50,27,0,6,3)
                bullet(enemy.pos,list[0]-50,27,0,6,3)
            if when_time(count,120):
                list[1] = 1
                enemy_move(randint(0,360),5,20)
            if when_time(count,240):
                count = 0
        if num == 4:
            if when_time(count,120):
                s_tan1.play()
                bullet(enemy.pos,randint(100,130),7,19,1,4)
            if when_time(count,180):
                enemy_move(dont_go_center(),2,40)
            if when_time(count,240):
                s_tan1.play()
                bullet(enemy.pos,randint(100,130)+120,7,19,1,4)
                count = 0
            
            play_sound(s_tan1,count,1)
        if num == 5:
            if while_time(count,5):
                s_tan1.play()
                for i in range(0,360,45):
                    bullet(enemy.pos,i+frame_count+min_dir,5,3,6,5)
        if num == 6:        
            if while_time(count,2): 
                bullet((WIDTH,randint(10,HEIGHT-20)),180+randint(-10,10),randint(4,7),4,4,6)
            if while_time(count,10):
                bullet((WIDTH,randint(10,HEIGHT-20)),180+randint(-10,10),randint(4,7),4,4,6.1)
            if while_time(count,18):
                s_tan2.play()
            if while_time(count,120):
                enemy_move(dont_go_center(),4,40)
        if num == 7:
            if when_time(count,0):
                list[2] = 1
            if when_time(count,1):
                s_lazer1.play()
                list[2] = -list[2]
                list[0] = look_at_point(enemy.pos,player.pos)
                list[1] = 90
            if count <= 300:
                if list[1] > 10: list[1] -= 0.5
                if while_time(count,1):
                    bullet(enemy.pos,list[0]+list[1],27,0,2)
                    bullet(enemy.pos,list[0]-list[1],27,0,2)
                if while_time(count,10):
                    s_tan1.play(loops = 1, maxtime = 200)
                    bullet(enemy.pos,look_at_point(enemy.pos,player.pos),7,15,2)
                if while_time(count,5):
                    bullet(enemy.pos,list[0]+list[1]+10,14,18,2)
                    bullet(enemy.pos,list[0]+list[1]/2+10,14,18,2)
                    bullet(enemy.pos,list[0]-list[1]/2-10,14,18,2)
                    bullet(enemy.pos,list[0]-list[1]-10,14,18,2)
                if when_time(count,150):
                    enemy_move(dont_go_center(),2,40)
            if while_time(count,10):
                for i in range(0,360,45):
                    bullet(enemy.pos,(i+count+min_dir)*list[2],5,3,0)
            
            if when_time(count,330):
                count = 0
        if num == 8:
            play_sound(s_ch0,count,1)
            if while_time(count,5) and count <= 120:            
                for _ in range(0,8):
                    bullet(enemy.pos,randint(0,360),5,2,4) 
            if when_time(count,120):
                play_sound(s_enep2,count,120)
                list[0] = player.pos
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos),10,19,2,8)
            if when_time(count,240):
                count = 0     
        if num == 9:
            if while_time(count,360):
                s_boom.play()
                magic_bullet(enemy.pos,180+randint(-10,10),2,(255,255,255),9)
            if while_time(count,10):
                s_tan1.play(loops=1,maxtime=240)
                for i in range(0,360,90):               
                    bullet(enemy.pos,-(i+min_dir),6,1,4)
        if num == 10:
            pos = player.pos
            while distance(pos,player.pos) <= 100:
                pos = (randint(30,WIDTH-30),randint(30,HEIGHT-30))
            
            play_sound(s_ch0,count,1)
            if while_time(count,1) and count <= 140:
                s_tan1.play(loops=1,maxtime=60)
                bullet(pos,0,0,3,2,10)
            if when_time(count,240):
                s_kira0.play()
                list[0] = 1
            if while_time(count,30) and big_small(count,280,430):
                s_boom.play()
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos),12,19,2,10.1)
            if when_time(count,280):
                enemy_move(dont_go_center(),2,120)
            if when_time(count,500):
                count =  0
                list[0] = 0
        if num == 11:
            if while_time(count,80):
                s_tan2.play(loops=1)
                for _ in range(0,14):
                    randnum = randint(1,7)
                    bullet(enemy.pos,randint(0,360),5,7,randnum,11,(randnum,5))
            if while_time(count+1,60):
                s_kira0.play()
        if num == 12:
            if while_time(count,120):
                s_ch0.play()
                magic_bullet(enemy.pos,look_at_point(enemy.pos,player.pos),3,(0,0,100),12)
        if num == 13:
            if when_time(count,60):
                s_tan1.play()
                rand_num = randint(0,4)
                for i in range(0,360,4):
                    bullet(enemy.pos,i+rand_num,6,9,5)
                for i in range(0,360,4):
                    bullet(enemy.pos,i+rand_num,4,9,5)
                for i in range(0,360,5):
                    bullet(enemy.pos,i+rand_num,2,9,5)
            if when_time(count,120):
                time_stop = True
                s_slash.play()
                enemy_move(dont_go_center(),2,120)
            if while_time(count,5) and time_stop:
                s_tan1.play(loops=1,maxtime=80)
                for i in range(0,360,90):
                    ran_lis = (randint(-30,30),randint(-30,30))
                    bullet(tuple(map(sum,zip(enemy.pos,ran_lis))),i+count,4,13,5)
                    bullet(tuple(map(sum,zip(enemy.pos,ran_lis))),i+count,3,7,5)
                    bullet(tuple(map(sum,zip(enemy.pos,ran_lis))),i+count,2,10,5)
            if when_time(count,240):
                s_kira0.play()
                time_stop = False
            if when_time(count,480):
                count = 0
        if num == 14:
            s_tan1.play(loops=1,maxtime=17)
            for i in range(0,360,45):            
                bullet(enemy.pos,i+count*count/10+min_dir,5,12,2)
        if num == 15:
            if while_time(count, 6) and not time_stop:
                s_tan1.play(loops=1,maxtime=95)
                bullet(enemy.pos,count*4+min_dir,4,19,5,15)
                bullet(enemy.pos,-count*4+min_dir,4,19,5,15)           
                list.append(player.pos)
                magic_bullet(player.pos,0,0,(255,100,255),15)
            if while_time(count, 60) and not time_stop:
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos),6,19,6,15)
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos)+30,6,19,6,15)
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos)-30,6,19,6,15)          
            if when_time(count,240):
                s_slash.play()
                bullet(enemy.pos,0,0,19,5,15)
                list[0] = (0,0)
                time_stop = True
            if time_stop and not count-240+3 > len(list)-1 and while_time(count,5):
                list[0] = list[count-240+3]
            if when_time(count,360):
                s_kira0.play()
                list = [0,0,0,0]
                time_stop = False
                magic_spr.empty()
            if when_time(count,420):           
                count = 0
        if num == 16:
            enemy.move_mod = 1
            if while_time(count,10):
                bullet(enemy.pos,enemy.move_dir+180,3,3,1)
                bullet(enemy.pos,enemy.move_dir+150,3,3,1)
                bullet(enemy.pos,enemy.move_dir+210,3,3,1)
            if while_time(count,7):
                bullet(enemy.pos,enemy.move_dir+180,3,4,3,16)
                bullet(enemy.pos,enemy.move_dir+150,3,4,3,16)
                bullet(enemy.pos,enemy.move_dir+210,3,4,3,16)
            if while_time(count,7):
                bullet(enemy.pos,enemy.move_dir+180,3,4,5,16.1)
                bullet(enemy.pos,enemy.move_dir+150,3,4,5,16.1)
                bullet(enemy.pos,enemy.move_dir+210,3,4,5,16.1)
            if while_time(count,100):
                for i in range(0,360,10):
                    bullet(enemy.pos,enemy.move_dir+30+i,3,16,2)
                    if i == 300:
                        break
            if while_time(count+1,80):
                for i in range(1,20):
                    bullet(enemy.pos,enemy.move_dir+180,i,7,6,16.2)
                    bullet(enemy.pos,enemy.move_dir+10+180,i,7,6,16.2)
                    bullet(enemy.pos,enemy.move_dir-10+180,i,7,6,16.2)
            if while_time(count+1,50):
                for i in range(5,10):
                    bullet(enemy.pos,enemy.move_dir,i,17,0)
            if enemy.move_time < 1:
                enemy_move(look_at_point(enemy.pos,player.pos),1,60)
        if num == 17:
            if when_time(count,0):
                enemy.move_mod = 1
                enemy_move(180,3,85)
            if list[1] == 0:
                if while_time(count,40):
                    s_tan1.play(loops = 1, maxtime = micro_sec(40))
                    for i in range(0,9):
                        bullet((0,HEIGHT/9*i+40),0,7,3,0,17,(3,0))
                    for i in range(0,9):
                        bullet((WIDTH,HEIGHT/9*i+40),180,7,3,0,17,(3,0))
                    for i in range(0,8):
                        bullet((WIDTH/8*i+65,HEIGHT),90,5,3,0,17,(3,0))
                    for i in range(0,8):
                        bullet((WIDTH/8*i+65,0),-90,5,3,0,17,(3,0))
            if list[1] == 1:
                if while_time(count,5):
                    s_tan1.play(loops = 1, maxtime = micro_sec(5))
                    for i in range(0,360,45):
                        bullet((WIDTH/2,HEIGHT/2),count*4.7+i,4,1,2,17,(1,1))
            if list[1] == 2:
                if while_time(count,40):
                    s_tan1.play(loops = 1, maxtime = micro_sec(20))
                    for i in range(0,360,6):
                        bullet((WIDTH/2,HEIGHT/2),count*4.7+i,3,4,5,17,(4,2))
            if list[1] == 3:
                if while_time(count,10):
                    s_tan1.play(loops = 1, maxtime = micro_sec(10))
                    for i in range(0,360,72):
                        bullet((WIDTH/2,HEIGHT/2),count*4.7+i,2,7,7,17,(7,3))
            if while_time(count,120):
                bullet(enemy.pos,look_at_point(enemy.pos,player.pos),2,15,3)
            if while_time(count+1,180):
                s_slash.play()
                list[1] += 1
                if list[1] == 4: list[1] = 0
        if num == 18:
            enemy.health -= 0.72
            if when_time(count,0):
                magic_bullet(enemy.pos,0,0,(0,0,0),18,1)
                s_tan1.play()
                s_ch0.play()
                for i in range(0,360,45):
                    magic_bullet(enemy.pos,i,0,(255, 255, 255),18.1,1)
            if list[1] == 1 and list[0] == 0:
                if list[3] == 0:
                    c = 2
                if list[3] == 1:
                    c = 5
                if list[3] == 2:
                    c = 1
                if list[3] == 3:
                    c = 5

                s_boom.play()
                for i in range(0,360,12):
                    bullet(enemy.pos,i+count,8,19,c)
                    bullet(enemy.pos,i+count,6,19,c)
                    bullet(enemy.pos,i+count,4,19,c)
                for i in range(0,360,12):
                    bullet(enemy.pos,i+count+randint(-30,30),1,16,c,18)
                for i in range(0,360,12):
                    bullet(enemy.pos,i+count+randint(-20,20),2,16,c,18)
                
                for i in range(0,360,12):
                    bullet(enemy.pos,i+count+randint(-10,10),3,16,c,18.3)
                
                for i in range(0,360,20):
                    bullet(enemy.pos,i+randint(-20,20),round(uniform(1,4), 2),randint(1,10),c,18)
                for i in range(0,360,10):
                    bullet(enemy.pos,i+randint(-20,20),round(uniform(1,3), 2),randint(1,10),c,18)
                for i in range(0,360,5):
                    bullet(enemy.pos,i+randint(-20,20),round(uniform(1,2), 2),randint(1,10),c,18)
                count = 0
                list[0] = 1
                
                
            if list[1] == 1 and when_time(count,120):
                magic_bullet(enemy.pos,0,0,(0,0,0),18,1)
                s_tan1.play()
                s_ch0.play()
                for i in range(0,360,45):
                    magic_bullet(enemy.pos,i,0,(255, 255, 255),18.2+0.1*list[3],1)
                list[1] = 0
                list[0] = 0
                list[3] += 1
                count += randint(0,120)


        #################################
        return count + 1, list

    ##########################################e

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

    # 적(보스)
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, health, num):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((256, 256), pygame.SRCALPHA)      
            self.rect = self.image.get_rect(center = (x, y))

            if num == 10:
                pokemonimg = pokemons[7]
            elif num == 11:
                pokemonimg = pokemons[8]
            elif num == 12:
                pokemonimg = pokemons[9]
            elif num == 13 or num == 15 or num == 17:
                pokemonimg = pokemons[10]
            elif num == 14 or num == 16 or num == 18:
                pokemonimg = pokemons[11]
            else:
                pokemonimg = pokemons[num] # 이미지


            self.image.blit(pokemonimg,(0,0))
            self.image2 = self.image.copy()
            self.img_num = 0
            self.hit_box = Rect(self.rect.x+64,self.rect.y+64,128,128)
            self.pos = (x, y)
            self.pos_copy = self.hit_box.center

            self.count = 0
            self.cos = 45
            self.list = [0,0,0,0]
            self.health = health
            self.num = num

            # 적이동을 위한 값
            self.move_dir = 0
            self.move_speed = 0
            self.move_time = 0
            self.move_mod = 0

            self.rest = True # 공격 쉬기?
            
        def update(self,collide):
            global score
            imgnum = self.img_num
            if not enemy_died:  # 죽었다면 공격하지 않기
                if self.rest:
                    self.count = 0 
                    if self.num == 18: 
                        self.move_mod = 1
                        enemy_move(180,4,7)
                        if self.move_time == 1:
                            self.pos = (WIDTH/2,HEIGHT/2)
                            self.rect.center = self.pos
                            self.move_time = 0

                else:
                    self.count, self.list =shoot_pattern(self.count,self.num,self.list)
                self.cos += 1
            
            # 만약 빔에 맞았을때
            if len(collide) > 0 and not self.rest:
                if self.health/enemy_health < 0.25:
                    s_damage1.play(loops=1, maxtime=50)  
                else: 
                    s_damage0.play(loops=1, maxtime=50)
                self.health -= collide[0].damage
                
                score += score_setting[1]
            
            # 움직이기 (벽 안나가게)
            if self.move_time > 0:
                self.pos_copy = calculate_new_xy(self.hit_box.center,self.move_speed,-self.move_dir)
                self.hit_box.center = (round(self.pos_copy[0]),round(self.pos_copy[1]))
                if self.move_mod == 0:
                    if self.hit_box.right > enemy_movebox.right:
                        self.hit_box.x = enemy_movebox.right - self.hit_box.w
                    if self.hit_box.left < enemy_movebox.left:
                        self.hit_box.x = enemy_movebox.left
                    if self.hit_box.bottom > enemy_movebox.bottom:
                        self.hit_box.y = enemy_movebox.bottom - self.hit_box.h
                    if self.hit_box.top < enemy_movebox.top:
                        self.hit_box.y = enemy_movebox.top
                self.move_time -= 1
            
            if imgnum != self.img_num:
                pass

            # 죽었을때
            if enemy_died and frame_count % 7 == 0 and self.count <= 10: 
                s_tan1.play()
                self.pos = calculate_new_xy(self.pos,2,0)
                self.count += 1
                

            self.rect.center = self.hit_box.center
            self.rect.y += round(math.cos(self.cos/30)*20)
            self.pos = self.hit_box.center
                
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

    # 거리





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

    def dont_go_center():
        rand_list = (70,-70,110,-110)
        if distance(enemy.pos,enemy_movebox.midtop) <= 200 or distance(enemy.pos,enemy_movebox.midbottom) <= 200:
            return look_at_point(enemy.pos, enemy_movebox.center)
        else:
            return rand_list[randint(0,3)] 

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
    boss_fun = 1
    global boss_dodon, bkgd1, boss_dodon_copy, enemy_health, score, time_stop
    # 초기 설정
    enemy_health = 500
    enemy_start = (round(WIDTH - WIDTH / 4),round(HEIGHT/2))
    enemy = Enemy(enemy_start[0],enemy_start[1],enemy_health,boss_fun)
    enemy_group = pygame.sprite.Group(enemy)
    enemy_movebox = Rect(600,80,380,560)
    play = True
    full_on = False
    cur_full_mod = False
    pause = False
    frame_count = 0
    min_dir = 0
    time_stop = False

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
    enemy_died = False
    read_end = False

    clock = pygame.time.Clock()

    # 점수 코어
    score = 0
    score_setting = (10,10,987650,10,0,0,0,0,0)

    # 보스마다 기본설정
    boss_dodon = pygame.Surface((64, 64), pygame.SRCALPHA)
    boss_dodon_copy = 0
    bos_xy = 0
    bkgd1 = pygame.Surface((0, 0))

    bg_x = 0
    fps = 60
    #################################################
    def game_defalt_setting(fun):
        global bgm_num, boss_dodon, bkgd1, boss_dodon_copy, enemy_health
        boss_dodon = pygame.Surface((64, 64), pygame.SRCALPHA)
        boss_dodon_copy = 0
        bkgd1 = pygame.Surface((640, 360))
        ##############################################
        if fun == 1:
            enemy_health = 500
            bgm = 1
            bg_nums = (0,0)
            boss_dodonimg = (128,0)
        if fun == 2:
            enemy_health = 500
            bgm = 1
            bg_nums = (540,0)
            boss_dodonimg = (192,0)
        if fun == 3:
            enemy_health = 500
            bgm = 1
            bg_nums = (0,360)
            boss_dodonimg = (128,64)
        if fun == 4:
            enemy_health = 500
            bg_nums = (540,360)
            bgm = 1
            boss_dodonimg = (128,0)
        if fun == 5:
            enemy_health = 500
            bg_nums = (0,720)
            bgm = 1
            boss_dodonimg = (128,64)
        if fun == 6:
            enemy_health = 500
            bg_nums = (540,720)
            bgm = 1
            boss_dodonimg = (192,0)
        if fun == 7:
            enemy_health = 800
            bgm = 2
            bg_nums = (0,0)
            boss_dodonimg = (192,0)
        if fun == 8:
            enemy_health = 800
            bgm = 2
            bg_nums = (540,0)
            boss_dodonimg = (192,0)
        if fun == 9:
            enemy_health = 800
            bgm = 2
            bg_nums = (0,360)
            boss_dodonimg = (192,0)
        if fun == 10:
            enemy_health = 800
            bgm = 2
            bg_nums = (0,0)
            boss_dodonimg = (192,0)
        if fun == 11:
            enemy_health = 800
            bgm = 2
            bg_nums = (540,0)
            boss_dodonimg = (192,0)
        if fun == 12:
            enemy_health = 800
            bgm = 2
            bg_nums = (0,360)
            boss_dodonimg = (192,0)
        if fun == 13:
            enemy_health = 800
            bgm = 3
            bg_nums = (0,0)
            boss_dodonimg = (192,64)
        if fun == 14:
            enemy_health = 800
            bgm = 3
            bg_nums = (0,0)
            boss_dodonimg = (128,0) 
        if fun == 15:
            enemy_health = 800
            bgm = 3
            bg_nums = (0,0)
            boss_dodonimg = (192,64)
        if fun == 16:
            enemy_health = 1600
            bgm = 3
            bg_nums = (0,0)
            boss_dodonimg = (128,0)
        if fun == 17:
            enemy_health = 800
            bgm = 3
            bg_nums = (0,0)
            boss_dodonimg = (192,64)
        if fun == 18:
            enemy_health = 1600
            bgm = 4
            bg_nums = (0,0)
            boss_dodonimg = (128,0)
        ###############################################
        enemy.health = enemy_health
        boss_dodon.blit(bullet_image, (0,0), Rect(boss_dodonimg,(64,64)))
        boss_dodon = pygame.transform.scale(boss_dodon,(128*4,128*4))
        boss_dodon_copy = boss_dodon.copy()

        if fun >= 7:
            bkgd1.blit(bg2_image,(0,0),(bg_nums,(540,360)))
        else:
            bkgd1.blit(bg_image,(0,0),(bg_nums,(540,360)))
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


    ################################################# 

    game_defalt_setting(boss_fun)

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
                    if ev.key == pygame.K_r or ev.key == pygame.K_t or ev.key == pygame.K_e: # 다음 스테이지 넘어가기
                        if ev.key == pygame.K_t: # 다음 스테이지 넘어가기
                            boss_fun += 1
                        if ev.key == pygame.K_e: # 다음 스테이지 넘어가기
                            boss_fun -= 1
                        spr.empty()
                        magic_spr.empty()
                        player.health = 500
                        enemy = Enemy(enemy_start[0],enemy_start[1],enemy_health,boss_fun)
                        enemy_group = pygame.sprite.Group(enemy)
                        play = True
                        starting = True
                        enemy_died = False
                        read_end = False
                        frame_count = 0
                        count = 0
                        min_dir = 0
                        bos_xy = 0
                        time_stop = False
                        game_defalt_setting(boss_fun)
                    
                    
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

            # 적 체력 없을때            
            if enemy.health <=  0 and not enemy_died:
                enemy_died = True
                enemy.count = 0
                spr.empty()
                magic_spr.empty()
                enemy.rest = True
                score += score_setting[2]

            # 적 3초뒤 활동하기
            if frame_count == 180 and enemy.rest:
                enemy.rest = False

            # 적이 죽었다면
            if enemy_died and enemy.count >= 10 and not read_end:
                s_enep1.play()
                enemy_group.empty()
                read_end = True
            
            # 탄에 박았는가
            hit_list = pygame.sprite.spritecollide(player, spr, not player.godmod, pygame.sprite.collide_circle)
            ehit_list = []
            for sprite in pygame.sprite.spritecollide(enemy, beams, False, pygame.sprite.collide_rect):
                if sprite.rect.colliderect(enemy.hit_box):
                    sprite.kill()
                    ehit_list.append(sprite)

            if not pause:      
                if not starting or read_end: enemy_group.update(ehit_list)  
                if len(magic_spr.sprites()) != 0:magic_spr.update(screen)                  
                spr.update(screen)
            # 연산 업데이트
            if not time_stop:
                if not pause:
                    beams.update()                            
                    player_group.update(hit_list)
                    frame_count += 1
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
            #pygame.draw.rect(screen, (0,0,255), enemy_movebox)

            # 게임 시작할때
            if starting and frame_count > 60:
                if bos_xy == 0 :s_ch2.play()
                bos_xy = boss_dodon_copy.get_size()
                                
                if bos_xy[0]-frame_count/8 <= 0:
                    starting = False
                    s_cat1.play()
                else:
                    boss_dodon_copy = pygame.transform.scale(boss_dodon, (bos_xy[0]-round(frame_count/8), bos_xy[0]-round(frame_count/8)))
                    screen.blit(boss_dodon_copy, (round(enemy.rect.x+ 100 - bos_xy[0]/2+40),round(enemy.rect.y+ 100- bos_xy[0]/2+40)))

            # 보스 처치 이벤트
            if read_end and bos_xy[0] <= 1024:
                bos_xy = boss_dodon_copy.get_size()       
                screen.blit(boss_dodon_copy, (enemy.rect.x+ 64- bos_xy[0]/2+40,enemy.rect.y+ 64 - bos_xy[0]/2+40))
                boss_dodon_copy = pygame.transform.scale(boss_dodon, (bos_xy[0]+12, bos_xy[0]+12))


            # 점수 표시
            score_text = score_font.render(str(score).zfill(10), True, (255,255,255))
            screen.blit(score_text,(WIDTH-score_text.get_rect().width,0))
            
            # 원형 체력바 그리기
            if not enemy.rest and not starting and not read_end: 
                drawArc(screen, (0, 0, 0), enemy.pos, 112, 15, 360*100)
                drawArc(screen, health_color(enemy.health/enemy_health), enemy.pos, 110, 10, 360*enemy.health/enemy_health)
                drawArc(screen, (0,0, 0), player.pos, 112, 15, 360*100)
                drawArc(screen, health_color(player.health/500), player.pos, 110, 10, 360*player.health/500)

            magic_spr.draw(screen)      
            beams.draw(screen)
            player_group.draw(screen)  
            
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
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
            cur_full_mod = full_on

    pygame.quit()
    exit()

if __name__ == "__main__":
    play_game()

