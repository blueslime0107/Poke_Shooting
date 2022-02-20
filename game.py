from audioop import add
from re import I
from shutil import move
from sys import float_repr_style
import pygame, math
from random import randint, uniform, choice
from pygame.locals import *
import cv2
import numpy
import time

# 게임에 핵심적인 기능만 주석을 넣었습니다 ##
# 초기화
pygame.init()
pygame.mixer.pre_init(44100,-16,2,512)

# 해상도
WIDTH = 540
HEIGHT = 360
render_layer = pygame.Surface((WIDTH,HEIGHT))
up_render_layer = pygame.Surface((WIDTH,HEIGHT), SRCALPHA)
screen = pygame.display.set_mode((WIDTH*2,HEIGHT*2))
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen_rect = screen.get_rect()
bgm_num = 0
# 소리 초기설정, 불러오기
pygame.mixer.set_num_channels(32)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

def play_game():
    
    global WIDTH, HEIGHT, screen
    # 이미지 불러오기
    bullet_image = pygame.image.load('resources\Image\Bullets.png').convert_alpha()
    bg_image = pygame.image.load('resources\Image\Bg1.png').convert_alpha()
    bg2_image = pygame.image.load('resources\Image\Bg2.png').convert_alpha()
    pkmon_image = pygame.image.load('resources\Image\pokemon.png').convert_alpha()
    background_img = pygame.image.load('resources\Image\\background.jpg').convert()
    menu_img = pygame.image.load('resources\Image\Menus.png').convert_alpha()
    item_img = pygame.image.load('resources\Image\item.png').convert_alpha()
    skill_img = pygame.image.load('resources\Image\skill.png').convert_alpha()
    ui_img = pygame.image.load('resources\Image\player_ui.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    msfx_volume = 10
    mmusic_volume = 60
    try:sfx_volume = msfx_volume/100
    except:sfx_volume = 0
    try:music_volume = mmusic_volume/100
    except:music_volume = 0

    s_lazer1 = pygame.mixer.Sound('resources\Music\SFX\se_lazer00.wav')
    s_tan1 = pygame.mixer.Sound('resources\Music\SFX\se_tan00.wav')
    s_tan2 = pygame.mixer.Sound('resources\Music\SFX\se_tan01.wav')
    s_ch2 = pygame.mixer.Sound('resources\Music\SFX\se_ch02.wav')
    s_ch0 = pygame.mixer.Sound('resources\Music\SFX\se_ch00.wav')
    s_cat1 = pygame.mixer.Sound('resources\Music\SFX\se_cat00.wav')
    s_enep1 = pygame.mixer.Sound('resources\Music\SFX\se_enep01.wav')
    s_enep2 = pygame.mixer.Sound('resources\Music\SFX\se_enep02.wav')
    s_slash = pygame.mixer.Sound('resources\Music\SFX\se_slash.wav')
    s_pldead = pygame.mixer.Sound('resources\Music\SFX\se_pldead00.wav')
    s_plst0 = pygame.mixer.Sound('resources\Music\SFX\se_plst00.wav')
    s_damage0 = pygame.mixer.Sound('resources\Music\SFX\se_damage00.wav')
    s_damage1 = pygame.mixer.Sound('resources\Music\SFX\se_damage01.wav')
    s_graze = pygame.mixer.Sound('resources\Music\SFX\se_graze.wav')
    s_kira0 = pygame.mixer.Sound('resources\Music\SFX\se_kira00.wav')
    s_kira1 = pygame.mixer.Sound('resources\Music\SFX\se_kira01.wav')
    s_boom = pygame.mixer.Sound('resources\Music\SFX\se_enep02.wav')
    s_item0 = pygame.mixer.Sound('resources\Music\SFX\se_item00.wav')
    s_enedead = pygame.mixer.Sound('resources\Music\SFX\se_enep00.wav')
    FONT_1 = 'resources\Font\SEBANG Gothic Bold.ttf' 
    FIELD_1 = 'resources\Music\BGM\\1Stage.wav'
    FIELD_2 = 'resources\Music\BGM\\2Stage.wav'
    FIELD_3 = 'resources\Music\BGM\\3Stage.wav'
    FIELD_4 = 'resources\Music\BGM\\4Stage.wav'
    FIELD_5 = 'resources\Music\BGM\\5Stage.wav'
    FIELD_6 = 'resources\Music\BGM\\6Stage.wav'
    BOSS_BGM1 = 'resources\Music\BGM\\1Boss.wav'
    BOSS_BGM2 = 'resources\Music\BGM\\2Boss.wav'
    BOSS_BGM3 = 'resources\Music\BGM\\3Boss.wav'
    BOSS_BGM4 = 'resources\Music\BGM\\4Boss.wav'
    BOSS_BGM5 = 'resources\Music\BGM\\5Boss.wav'
    BOSS_BGM6 = 'resources\Music\BGM\\6Boss.wav'

    tan_channel = pygame.mixer.Channel(0)
    kira_channel = pygame.mixer.Channel(1)
    enemy_boom_channel = pygame.mixer.Channel(2)

    a_list = []
    cur_list = []
    if True:
        for i in range (0,176,16):
            for j in range (0,128,16):
                image = pygame.Surface((16, 16), pygame.SRCALPHA)
                image.blit(bullet_image, (0,0), Rect(j,i,16,16))
                image = pygame.transform.scale2x(image)
                if i == 160:
                    k_list = []
                    for k in range(0,180):
                        image2 = pygame.transform.rotate(image, k*2)
                        k_list.append(image2)
                    a_list.append(k_list)
                else:
                    a_list.append(image)
            cur_list.append(a_list)
            a_list = []
        for i in range (192,201,8):
            for j in range (0,64,8):
                image = pygame.Surface((8, 8), pygame.SRCALPHA)
                image.blit(bullet_image, (0,0), Rect(j,i,8,8))
                image = pygame.transform.scale2x(image)
                if i == 192:
                    k_list = []
                    for k in range(0,180):
                        image2 = pygame.transform.rotate(image, k*2)
                        k_list.append(image2)
                    a_list.append(k_list)
                else:
                    a_list.append(image)
            cur_list.append(a_list)
            a_list = []
        for i in range (208,400,32):
            for j in range (0,256,32):
                image = pygame.Surface((32, 32), pygame.SRCALPHA)
                image.blit(bullet_image, (0,0), Rect(j,i,32,32))
                image = pygame.transform.scale2x(image)
                if i == 240:
                    k_list = []
                    for k in range(0,180):
                        image2 = pygame.transform.rotate(image, k*2)
                        k_list.append(image2)
                    a_list.append(k_list)
                else:
                    a_list.append(image)
            cur_list.append(a_list)
            a_list = []
        for i in range(0,4):
            image = pygame.Surface((64, 64), pygame.SRCALPHA)
            image.blit(bullet_image, (0,0), Rect(i*64,432,64,64))
            image = pygame.transform.scale2x(image)
            a_list.append(image)
            a_list.append(image)
        cur_list.append(a_list)
        a_list = []
    bullets = cur_list

    cur_list = []
    for i in range(0,112,16):
        image = pygame.Surface((16,16),pygame.SRCALPHA)
        image.blit(bullet_image,(0,0),Rect(i,176,16,16))
        for j in range(1,33):
            image2 = pygame.transform.scale(image, (j,j))
            a_list.append(image2)
        cur_list.append(a_list)
        a_list = []
    bullet_erase = cur_list
    cur_list = []
    for i in range(0,256,32):
        image = pygame.Surface((32,32), pygame.SRCALPHA)
        image.blit(bullet_image, (0,0), Rect(i,400,32,32))
        for i in range(1,65,2):
            image2 = pygame.transform.scale(image,(i*2,i*2))
            a_list.append(image2)
        cur_list.append(a_list)
        a_list = []
    bullet_taning = cur_list

    cur_list = []
    for i in range(0,128,16):
        image = pygame.Surface((16,16),pygame.SRCALPHA)
        image.blit(item_img, (0,0), Rect(i,0,16,16))
        cur_list.append(image)
    items = cur_list

    cur_list = []
    a_list = []
    for i in range(0,10):
        for j in range(0,10):
            image = pygame.Surface((64, 64), pygame.SRCALPHA)
            image.blit(pkmon_image, (0,0), Rect(j*64,i*64,64,64))
            image = pygame.transform.scale2x(image)
            cur_list.append(image)
    pokemons = cur_list
    # 이펙트 미리 그려놓기
    cur_list = []
    for i in range(0,360):
        image = pygame.Surface((256,256), pygame.SRCALPHA)
        image.blit(bullet_image,(0,0),(0,496,256,256))
        image = pygame.transform.scale(image,(128,128))
        image = pygame.transform.rotate(image, i)
        cur_list.append(image)
    boss_circle = cur_list
    cur_list = []
    for i in range(1,256):
        image = pygame.Surface((2*i,2*i), pygame.SRCALPHA)
        pygame.draw.circle(image, (255,255,255,256-i), (2*i//2,2*i//2), 2*i//2)
        cur_list.append(image)
    white_circle = cur_list
    cur_list = []
    for i in range(0,60):
        image = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        image.fill((0,0,0,0+i*4))
        cur_list.append(image)
    for i in range(0,60):
        image = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        image.fill((0,0,0))
        cur_list.append(image)
    for i in range(0,60):
        image = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        image.fill((0,0,0,255-i*4))
        cur_list.append(image)
    black_screen = cur_list
    cur_list = []
    for i in range(100,256,4):
        image = pygame.Surface((64,64), pygame.SRCALPHA)        
        image.blit(bullet_image,(0,0),(192,128,64,64))
        image = pygame.transform.scale(image, (i/2, i/2))
        image.fill((255, 255, 255, 340-i), special_flags=pygame.BLEND_RGBA_MULT)
        cur_list.append(image)
    enemy_died_circle = cur_list
    cur_list = []
    for i in range(1,255,4):
        width = 256-i
        image = pygame.Surface((width,width), pygame.SRCALPHA)
        rect2 = round(image.get_width()/2)
        pygame.draw.circle(image, (255,255,255,256-i), (rect2,rect2), 1 if rect2-1 < 1 else rect2-1,1)
        cur_list.append(image)
    died_white_circle = cur_list
    cur_list = []
    for i in range(0,1):
        image = pygame.Surface((64,64), pygame.SRCALPHA)
        image.blit(bullet_image,(0,0),(128,128,64,64))
        for j in range(0,90):
            image2 = pygame.transform.rotate(image, j)  
            rect = image2.get_rect() 
            pygame.draw.circle(image2 , (200,100,100),rect.center, 4)
            pygame.draw.circle(image2 , (255,255,255),rect.center, 3)     
            cur_list.append(image2)
    slow_player_circle = cur_list
    cur_list = []
    for i in range(0,1):
        image = pygame.Surface((64,64), pygame.SRCALPHA)
        image.blit(bullet_image,(0,0),(128,0,64,64))
        for j in range(0,180):
            image2 = pygame.transform.rotate(image, j*2)  
            rect = image2.get_rect()   
            cur_list.append(image2)
    magic_circle_sprite = cur_list

    # 이미지 나눠 저장하기 
    RIGHT_POS = [(WIDTH+64,-64),(WIDTH+64,HEIGHT/6-32),(WIDTH+64,HEIGHT/4),(WIDTH+64,HEIGHT/6*2+32),(WIDTH+64,HEIGHT/2),(WIDTH+64,HEIGHT/6+HEIGHT/2-32),(WIDTH+64,HEIGHT/4+HEIGHT/2),(WIDTH+64,HEIGHT/6*2+HEIGHT/2+32),(WIDTH+64,HEIGHT+64)]
    RIGHT_POS2 = [(WIDTH+64,HEIGHT/6-32),(WIDTH+64,HEIGHT/4),(WIDTH+64,HEIGHT/6*2+32),(WIDTH+64,HEIGHT/2),(WIDTH+64,HEIGHT/6+HEIGHT/2-32),(WIDTH+64,HEIGHT/4+HEIGHT/2),(WIDTH+64,HEIGHT/6*2+HEIGHT/2+32)]
    UP_POS = [(WIDTH/2,-64),(WIDTH/2+54,-64),(WIDTH/2+54*2,-64),(WIDTH/2+54*3,-64),(WIDTH/2+54*4,-64)]
    DOWN_POS = [(WIDTH/2,HEIGHT+64),(WIDTH/2+54,HEIGHT+64),(WIDTH/2+54*2,HEIGHT+64),(WIDTH/2+54*3,HEIGHT+64),(WIDTH/2+54*4,HEIGHT+64)]
    
    clock = pygame.time.Clock()
    prev_time = time.time()
    dt = 0
    FPS = 60
    TARGET_FPS = 60
    keys = pygame.key.get_pressed() 

    def music_and_sfx_volume():
        pygame.mixer.music.set_volume(music_volume)
        s_lazer1.set_volume(sfx_volume)
        s_tan1.set_volume(sfx_volume/2)
        s_tan2.set_volume(sfx_volume/2)
        s_ch2.set_volume(sfx_volume)
        s_ch0.set_volume(sfx_volume+0.3)
        s_cat1.set_volume(sfx_volume*1.5)
        s_enep1.set_volume(sfx_volume)
        s_enep2.set_volume(sfx_volume)
        s_slash.set_volume(sfx_volume)
        s_pldead.set_volume(sfx_volume)
        s_plst0.set_volume(sfx_volume/5)
        s_damage0.set_volume(sfx_volume/5)
        s_damage1.set_volume(sfx_volume/5)
        s_graze.set_volume(sfx_volume)
        s_kira0.set_volume(sfx_volume)
        s_kira1.set_volume(sfx_volume)
        s_boom.set_volume(sfx_volume)
        s_item0.set_volume(sfx_volume)
        s_enedead.set_volume(sfx_volume)
    # 플레이어
    music_and_sfx_volume()
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y, speed, health):
            pygame.sprite.Sprite.__init__(self) # 초기화?
            self.image = pygame.Surface((128, 128), pygame.SRCALPHA) # 이미지          
            self.image.blit(pokemons[0],(0,-5)) # 이미지 위치조정
            self.rect = self.image.get_rect(center = (round(x), round(y)))
            self.image2 = self.image.copy()
            self.img_num = 0
            self.pos = (x,y)  
            self.real_pos = (x*2,y*2)          
            self.speed = speed
            self.max_health = health
            self.health = health
            self.power = 0
            self.mp = 8
            self.before_health = 0
            self.count = 0
            self.godmod = False # 무적?
            self.godmod_count = 0
            self.max_godmod_count = 0
            self.hit_speed = 0
            self.hit_dir = 0
        def update(self,collide):
            dx, dy = 0 , 0
            inum = self.img_num
            self.img_num = 0
            # 플레이어 이동 조종 SHIFT 를 누르면 느리게 움직이기
            if keys[pygame.K_LSHIFT]:self.speed = 1
            else:self.speed = 4           
            # 화면 밖으로 안나감
            if keys[pygame.K_RIGHT]:dx += 0 if self.rect.centerx >= WIDTH-20 else self.speed            
            if keys[pygame.K_LEFT]:dx -= 0 if self.rect.centerx <= 0 + 20 else self.speed            
            if keys[pygame.K_DOWN]:dy += 0 if self.rect.centery >= HEIGHT-20 else self.speed               
            if keys[pygame.K_UP]:dy -= 0 if self.rect.centery <= 0+20 else self.speed
            if self.rect.centerx <= -100: 
                dx = 0
                dy = 0
            
            # 총 쏘기 이벤트
            if keys[pygame.K_z] and frame_count % 4 == 0 and not player.godmod and not pause:
                s_plst0.play(loops=1, maxtime=50)
                beams_group.add(Beam(get_new_pos(player.pos,5,15)))
                beams_group.add(Beam(get_new_pos(player.pos,5,-15)))

            # 모양이 바꼈을 때만 모양 업데이트
            self.img_num = self.img_num + keys[pygame.K_RIGHT] + keys[pygame.K_LEFT]*2
            if inum != self.img_num:
                if self.img_num == 0:self.image = self.image2                
                if self.hit_speed == 0:
                    if self.img_num == 1:self.image = pygame.transform.rotate(self.image2, -10)
                    if self.img_num == 2:self.image = pygame.transform.rotate(self.image2, 10)                      
                self.rect = self.image.get_rect(center = (round(self.pos[0]),round(self.pos[1])))

            # 탄에 닿았을때
            if len(collide) > 0 and not self.godmod:
                s_pldead.play()
                self.godmod = True
                self.count = 0
                self.before_health = self.health
                self.health -= round(collide[0].radius/2 * 7 * collide[0].speed/2)
                self.hit_speed = collide[0].speed
                self.hit_dir = -collide[0].direction
                self.godmod_count = 60
                self.max_godmod_count = self.godmod_count
            
            # 무적이면 2초뒤 풀리기
            if self.godmod and self.hit_speed <= 0:
                self.godmod_count -= 1
                if 0 >= self.godmod_count:
                    self.godmod = False
            
            # 넉백
            if self.hit_speed > 0:
                self.pos = calculate_new_xy(self.pos, self.hit_speed, self.hit_dir)
                if self.pos[0] <= 20: self.pos = (20,self.pos[1])
                if self.pos[0] >= WIDTH-20: self.pos = (WIDTH-20,self.pos[1])
                if self.pos[1] <= 20: self.pos = (self.pos[0],20)
                if self.pos[1] >= HEIGHT-20: self.pos = (self.pos[0],HEIGHT-20)
                if self.hit_speed > 0:
                    self.hit_speed -= 0.1
                    if self.hit_speed <= 0: self.hit_speed = 0
            else:
                # 키보드 먹히기
                self.pos = (self.pos[0] + dx*dt, self.pos[1] + dy*dt)  
            self.real_pos = (self.pos[0]*2,self.pos[1]*2)
            
            self.rect.center = round(self.pos[0]), round(self.pos[1]) 
            self.count += 1
    class Player_hit(pygame.sprite.Sprite):
        def __init__(self):
            self.image = pygame.Surface((6,6)) # 이미지  
            self.rect = self.image.get_rect()
            self.pos = (0,0)
            self.radius = 3
        def update(self):
            self.pos = (player.pos[0]*2,player.pos[1]*2)
            self.rect.center = self.pos


    class Player_sub():
        def __init__(self,num):
            self.num = num
            self.ball = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(self.ball, (255, 0, 222), (16,16), 8)
            pygame.draw.circle(self.ball, (247, 178, 238), (16,16), 6)
            self.ballxy = [(-20,-20),(-20,-20),(-20,-20),(-20,-20)]
            self.adddir = 0
            self.radi = 40
            self.count = 0
        
        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_z] and while_time(self.count,6) and player.power >= 100:
                for i in range(0,int(player.power/100)):
                    beams_group.add(Beam(get_new_pos(self.ballxy[i],16,16),1))
            if keys[pygame.K_LSHIFT] and self.adddir <= 30:
                self.adddir += 2
                self.radi -= 1.2
            elif self.adddir > 0 and not keys[pygame.K_LSHIFT]:
                self.adddir -= 2
                self.radi += 1.2

            if int(player.power/100) == 1:
                self.ballxy[0] = move_circle(get_new_pos(player.pos,-16,-16),0,self.radi)
            if int(player.power/100) == 2:
                self.ballxy[0] = move_circle(get_new_pos(player.pos,-16,-16),45-self.adddir,self.radi)
                self.ballxy[1] = move_circle(get_new_pos(player.pos,-16,-16),-45+self.adddir,self.radi)
            if int(player.power/100) == 3:
                self.ballxy[0] = move_circle(get_new_pos(player.pos,-16,-16),45-self.adddir,self.radi)
                self.ballxy[1] = move_circle(get_new_pos(player.pos,-16,-16),-45+self.adddir,self.radi)
                self.ballxy[2] = move_circle(get_new_pos(player.pos,-16,-16),0,self.radi)
            if int(player.power/100) == 4:
                self.ballxy[0] = move_circle(get_new_pos(player.pos,-16,-16),45-self.adddir,self.radi)
                self.ballxy[1] = move_circle(get_new_pos(player.pos,-16,-16),-45+self.adddir,self.radi)
                self.ballxy[2] = move_circle(get_new_pos(player.pos,-16,-16),105-self.adddir*2,self.radi)
                self.ballxy[3] = move_circle(get_new_pos(player.pos,-16,-16),-105+self.adddir*2,self.radi)

            self.count += 1

        def draw(self):
            if player.power >= 100:render_layer.blit(self.ball,get_new_pos(self.ballxy[0]))
            if player.power >= 200:render_layer.blit(self.ball,get_new_pos(self.ballxy[1]))
            if player.power >= 300:render_layer.blit(self.ball,get_new_pos(self.ballxy[2]))
            if player.power >= 400:render_layer.blit(self.ball,get_new_pos(self.ballxy[3]))

    class Bomb(pygame.sprite.Sprite):
        def __init__(self, pos, num, col=0):
            pygame.sprite.Sprite.__init__(self) # 초기화?
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA) # 이미지          
            self.rect = self.image.get_rect(center = (round(pos[0]), round(pos[1])))
            self.image2 = self.image.copy()
            self.pos = pos
            self.count = 0
            self.num = num
            self.col = col
            self.radius = 0
            self.damage = 10
            self.can_damage = True

        def update(self):
            if self.count == 0:
                s_cat1.play()
                if self.num == 1:
                    image = pygame.Surface((64,64), pygame.SRCALPHA)
                    pygame.draw.circle(image, (255,0,255,90), (32,32), 32)
                self.image = image
                self.rect = self.image.get_rect(center = self.pos)
                self.image2 = self.image.copy()

            if self.num == 1:
                self.pos = player.pos
                if self.count <= 30: self.image = pygame.transform.scale(self.image2, (self.count*8, self.count*8))
                elif big_small(self.count,50,110): self.image = pygame.transform.scale(self.image2, (self.rect.width-4,self.rect.width-4))
                elif big_small(self.count,120,180): self.image = pygame.transform.scale(self.image2, (self.rect.width+18,self.rect.width+18))
                if when_time(self.count, 50): s_ch0.play()
                if when_time(self.count, 120): s_boom.play()
                self.radius = self.image.get_rect().width/2
                if self.count >= 240:
                    self.image = pygame.transform.scale(self.image2, (self.rect.width-18,self.rect.width-18))
                    if self.count >= 295: self.kill()

            self.rect = self.image.get_rect(center = get_new_pos(self.pos))
            self.count += 1
    class Bomb_hit(pygame.sprite.Sprite):
        def __init__(self, pos, num, col=0):
            pygame.sprite.Sprite.__init__(self) # 초기화?
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA) # 이미지          
            self.rect = self.image.get_rect(center = (round(pos[0]), round(pos[1])))
            self.image2 = self.image.copy()
            self.pos = (pos[0]*2,pos[1]*2)
            self.count = 0
            self.num = num
            self.col = col
            self.radius = 0
            self.damage = 10
            self.can_damage = True

        def update(self):
            if self.count == 0:
                if self.num == 1:
                    image = pygame.Surface((64,64), pygame.SRCALPHA)
                    pygame.draw.circle(image, (255,0,255,90), (32,32), 32)
                self.image = image
                self.rect = self.image.get_rect(center = self.pos)
                self.image2 = self.image.copy()

            if self.num == 1:
                self.pos = (player.pos[0]*2,player.pos[1]*2)
                if self.count <= 30: self.image = pygame.transform.scale(self.image2, (self.count*8, self.count*8))
                elif big_small(self.count,50,110): self.image = pygame.transform.scale(self.image2, (self.rect.width-4,self.rect.width-4))
                elif big_small(self.count,120,180): self.image = pygame.transform.scale(self.image2, (self.rect.width+18,self.rect.width+18))
                if when_time(self.count, 50): s_ch0.play()
                if when_time(self.count, 120): s_boom.play()
                self.radius = self.image.get_rect().width
                if self.count >= 240:
                    self.image = pygame.transform.scale(self.image2, (self.rect.width-18,self.rect.width-18))
                    if self.count >= 295: self.kill()

            self.rect = self.image.get_rect(center = get_new_pos(self.pos))
            self.count += 1


    class Tittle():
        def __init__(self,value):
            self.stage = value
            self.count = 999
            self.save = 1
            self.text = "Stage 1"
            self.name = "드넓은 초원"
        def draw(self):
            if self.count < 460: 
                if self.count > 31:
                    x_move = (self.count - 16)/5-20
                    if self.count > 300: 
                        self.save = self.save * 1.1
                        x_move -= self.save
                    
                    pygame.draw.rect(render_layer, (255,0,0), (get_new_pos((WIDTH/2-186-x_move,HEIGHT/2-26)),(130,-45)))
                    pygame.draw.rect(render_layer, (255,0,0), (get_new_pos((WIDTH/2-60-x_move,HEIGHT/2-1)),(200,-45)))
                    title_text = score_font.render(self.text, True, (255,255,255))
                    render_layer.blit(title_text,get_new_pos((WIDTH/2+10-x_move,HEIGHT/2+10)))
                    title_text = score_font.render(self.name, True, (0,0,0))
                    render_layer.blit(title_text,get_new_pos((WIDTH/2+200-x_move,HEIGHT/2)))
                if self.count < 64:
                    pygame.draw.rect(render_layer, (255,255,255), (get_new_pos((WIDTH/2-250,HEIGHT/2-1)),(700,round(-abs(math.sin(self.count/20)*100)))))
                self.count += 1
        def title_start(self,val,name):
            self.count = 0
            self.save = 1
            self.text = val
            self.name = name
    # 플레이어 총
    class Beam(pygame.sprite.Sprite):
        def __init__(self, pos, num=0, dir=0):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((20,16), pygame.SRCALPHA)                   
            self.rect = self.image.get_rect(center = get_new_pos(pos))            
            self.pos = get_new_pos(pos)
            self.num = num
            self.speed = 0
            self.direction = dir           
            self.damage = 0
            self.radius = 20
            self.died = False
            if self.num == 0:
                self.image.fill((255, 0, 222))
                pygame.draw.rect(self.image, (247, 178, 238), (1,1,18,14),0)
                self.speed = 40
                self.damage = 3
            if self.num == 1:
                # (247, 178, 238)
                self.image = pygame.Surface((52, 16), pygame.SRCALPHA)
                self.image.fill((randint(0,255),randint(0,255),randint(0,255)))
                self.speed = 50
                self.damage = 1
                if enemy_group: self.direction = look_at_point(self.pos,enemy_group.sprites()[0].pos)
                if boss.attack_start: self.direction = look_at_point(self.pos,boss_group.sprites()[0].pos)
                self.rect = self.image.get_rect(center = get_new_pos(self.pos))  
            if self.num == 2:
                self.image.fill((255, 255, 222))
                pygame.draw.rect(self.image, (247, 178, 238), (3,3,34,26),0)
                self.speed = 25
                self.damage = 2
            self.image = pygame.transform.rotate(self.image, self.direction)
            

        def update(self):
            # 화면 나가면 삭제
            if self.pos[0] >= WIDTH:
                self.kill()
            if self.died:
                self.kill()

            self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
            self.rect = self.image.get_rect(center = get_new_pos(self.pos))  
    # 적
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, dir, speed, health, img, hit_cir, num):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((128,128), pygame.SRCALPHA)
            self.image.blit(pokemons[img-1],(0,0))      
            self.rect = self.image.get_rect(center = get_new_pos((x, y)))
            self.radius = hit_cir//2
            self.pos = (x, y)
            #pygame.draw.circle(self.image, (200,0,0), (128,128), self.radius, 3)

            self.count = 0
            self.list = [0,0]
            self.max_health = health
            self.health = health
            self.num = num

            # 적이동을 위한 값
            self.move_dir = dir
            self.move_speed = speed

            self.screen_apper = False

        def update(self):
            global score

            # 능력
            if not self.health <= 0:
                self.pos, self.move_dir, self.move_speed ,self.count,self.list= enemy_attack(self.num, self.count, self.pos, self.move_dir, self.move_speed,self.list)

            if not screen_rect.colliderect(self.rect) and self.screen_apper: # 밖으로 나가면 사라지기
                self.kill() 
            if screen_rect.colliderect(self.rect) and not self.screen_apper:
                self.screen_apper = True
            if self.health <= 0: # 체력 다 달면 죽기
                if self.num == 21 and not self.health == -999:
                    bullet_effect(s_tan2,0,self.pos)
                    for i in range(0,360,20):                       
                        bullet(calculate_new_xy(self.pos,20,-i),i,0,12,0,9.4)
                enemy_boom_channel.play(s_enedead)
                effect_group.add(Effect(self.pos,1))
                effect_group.add(Effect(self.pos,3))
                for i in range(0,math.ceil(self.max_health/50)):
                    rand = [randint(-100,100),randint(-100,100)]
                    if rand[1] < 32: rand[1] = 32
                    if rand[1] >688: rand[1] = 688
                    item_group.add(Item(get_new_pos((self.pos[0]*2,self.pos[1]*2),rand[0],rand[1]),0))
                self.kill()

            self.count += 1
            self.rect.center = (int(self.pos[0]),int(self.pos[1]))    
    
    # 보스
    class Boss_Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((128,128), pygame.SRCALPHA)      
            self.rect = self.image.get_rect(center = (x, y))
            self.image2 = self.image.copy()
            self.radius = 0
            self.pos = (x, y)
            self.image_num = 0

            self.count = 0
            self.list = [0,0,0,0]
            self.max_health = 0
            self.health = 1
            self.real_max_health = 0
            self.real_health = 0
            self.num = 0

            # 적이동을 위한 값
            self.move_dir = 0
            self.move_speed = 0
            self.move_point = (0,0)
            self.move_time = 0
            self.ready = False
            self.move_ready = False # 스펠 시작시 움직이는중?
            self.godmod = False
            self.dieleft = False
            self.spell = []
            self.dies = False
            self.died_next_stage = False
            self.appear = False
            self.real_appear = False
            self.attack_start = False
            self.box_disable = False

        def update(self, collide):
            global score
            if self.appear:
                if self.attack_start:
                    inum = self.image_num
                    self.image_num = 0
                    if self.count == 0:
                        effect_group.add(Effect(self.pos,4))
                    # 보스가 등장했을때 실행
                    if not self.ready:
                        self.max_health = self.spell[0].health
                        self.health = self.max_health
                        self.godmod = True 
                    # 능력 살아있으면

                    if self.health > 0 and not self.dieleft:
                        if self.count >= 120 and self.move_ready and not self.ready:
                            self.count = 1
                            self.ready = True
                            self.godmod = False
                        self.count, self.pos, self.ready = boss_attack(self.spell[0].num, self.count, self.pos, self.ready)

                    if self.move_speed == 0:self.image_num =0
                    else:
                        imgdir = self.move_dir
                        if imgdir < 0: 360+imgdir
                        if big_small(imgdir,90,269): self.image_num =2
                        else: self.image_num =1
                    if inum != self.image_num:
                        if self.image_num == 0:self.image = self.image2                
                        if self.image_num == 1:self.image = pygame.transform.rotate(self.image2, -10)
                        if self.image_num == 2:self.image = pygame.transform.rotate(self.image2, 10)                      
                        self.rect = self.image.get_rect(center = (round(self.pos[0]),round(self.pos[1])))

                    # 빔에 맞았을때
                    if len(collide) > 0 and not self.godmod:
                        if bomb_activated:
                            for beam in collide:
                                self.health -= beam.damage
                                if self.health/self.max_health < 0.25:
                                    s_damage1.play(loops=1, maxtime=50)  
                                else: 
                                    s_damage0.play(loops=1, maxtime=50)
                                self.real_health -= beam.damage
                        else:                                
                            for beam in collide:
                                if not beam.died:
                                    self.health -= beam.damage
                                    if self.health/self.max_health < 0.25:
                                        s_damage1.play(loops=1, maxtime=50)  
                                    else: 
                                        s_damage0.play(loops=1, maxtime=50)
                                    self.real_health -= beam.damage
                                    beam.died = True

                    if self.health <= 0 and not self.dieleft and self.ready: # 체력다 닳음 죽은적이없고 스펠시전 중이였을때 실행
                        self.count = 0
                        self.move_speed = 0
                        self.move_ready = False
                        self.ready = False
                        self.box_disable = False
                        self.move_time  = 0
                        add_effect(self.pos,5)
                        if len(self.spell) > 1: # 스펠카드가 남아있다면 안죽기
                            del self.spell[0] # 사용한 스펠 삭제
                            if self.spell[0].spellcard:
                                s_cat1.play()
                            else:
                                s_tan1.play()
                                for _ in range(0,20):
                                    item_group.add(Item(get_new_pos(self.pos,randint(-100,100),randint(-100,100)),0))
                                for _ in range(0,40):
                                    item_group.add(Item(get_new_pos(self.pos,randint(-200,200),randint(-200,200)),1))
                        else:#퇴장(다음 스테이지로, 공격멈추기)
                            del self.spell[0]
                            s_enep1.play()
                            self.image = self.image2
                            self.dieleft = True
                            self.move_point = (0,0)
                            self.attack_start = False
                            self.died_next_stage = True
                            self.count = 0
                            for _ in range(0,20):
                                item_group.add(Item(get_new_pos(self.pos,randint(-100,100),randint(-100,100)),0))
                            for _ in range(0,40):
                                item_group.add(Item(get_new_pos(self.pos,randint(-200,200),randint(-200,200)),1))
                    self.count += 1

                # 처음등장시 중앙으로 오기
                if self.real_appear and not self.attack_start:
                    if distance(self.pos,(WIDTH-150,HEIGHT//2)) <= 2:
                        self.pos = (WIDTH-150,HEIGHT//2)
                        self.move_point = (0,0)
                    elif self.move_point == (0,0):
                        self.move_point = ((WIDTH-150-self.pos[0])/60,(HEIGHT//2-self.pos[1])/60)
                    self.pos = (self.pos[0]+self.move_point[0],self.pos[1] + self.move_point[1])
            
            
            if self.dieleft: # 죽었을때 이벤트
                remove_allbullet()
                if self.dies: 
                    self.pos = (-128,-128) 
                    self.dieleft = False
                    self.real_appear = False
                    self.appear = False
                else:
                    self.count += 1
                    if self.count > 60:
                        self.pos = get_new_pos(self.pos,5,5)
                        if self.pos[0] > WIDTH+50:
                            self.dieleft = False
                            self.real_appear = False
                            self.appear = False 
                            self.count = 0                          
                if self.num == 2 or self.num == 4 or self.num == 6 or self.num == 8 or self.num == 10 or self.num == 11:
                    text.pause = False
                
            self.rect.center = (int(self.pos[0]),int(self.pos[1])) 
    
    class Spell():
        def __init__(self,number,health,spellcard,col=0,sub_name="",name=""):
            self.health = health
            self.spellcard = spellcard
            self.num = number
            self.count = 0
            self.font = pygame.font.Font(FONT_1, 10)
            self.font2 = pygame.font.Font(FONT_1, 20)
            self.image = pygame.Surface((200,40), pygame.SRCALPHA)
            if self.spellcard:
                self.image.blit(skill_img,(0,0),(0,0+37*col,200,37))
                text = self.font.render(sub_name, True, 'white')
                self.image.blit(text,(13,2))
                text = self.font2.render(name, True, 'white')
                self.image.blit(text,(25,15))
        def draw(self):
            if self.count < 60: up_render_layer.blit(self.image,(WIDTH-200,0))
            if big_small(self.count,60,85): 
                up_render_layer.blit(self.image,(WIDTH-200,(self.count-60)**2))
            if self.count > 85: up_render_layer.blit(self.image,(WIDTH-200,320))
            self.count += 1
    # 총알 
    ############################################
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction, speed, bul, col, mod, num=(0,0)):
            # 이미지
            pygame.sprite.Sprite.__init__(self)
            self.shape = (bul, col)
            self.pos = (x, y)
            self.image = bullets[bul][col] if not (bul == 10 or bul == 11 or bul == 14) else bullets[bul][col][0]
            self.image2 = self.image.copy()

            self.add_dir = 0
            self.move_fun = False
            # 쓸 값
            self.rect = self.image.get_rect(center = (int(x), int(y)))
            
            self.direction = direction
            self.speed = speed
            self.radius = bullet_size[bul]//2
            self.count = 0
            self.mod = mod
            self.num = num
            self.grazed = True
            self.lotate = False if bul == 2 or bul == 3 or bul == 10 or bul==11 or bul == 12 or bul == 15 or bul == 10 or bul == 14 or bul == 19 else True   
            if self.lotate: 
                self.image = pygame.transform.rotate(self.image2, round(self.direction-90))
                self.rect = self.image.get_rect(center = (int(self.pos[0]),int(self.pos[1])))
            self.keeplotate = True if (bul == 10 or bul == 11 or bul == 14) else False
            self.keeplotate_count = 0
            self.screen_die = False
            
        def update(self, screen):
            global score
            global time_stop
            screen_die = 0
            mod, sub = math.trunc(self.mod), (self.mod*10)%10
            direc = self.direction


            #모드 값이 있으면 탄 속성 변화###############################################
            bullet_type(self,mod,sub)           
            ################################################
                        
            if direc != self.direction and self.lotate:# 각도 계산후 위치 업데이트
                self.image = pygame.transform.rotate(self.image2, round(self.direction-90))
                self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))  
            if self.keeplotate:
                self.keeplotate_count += 1
                if self.keeplotate_count == 180:
                    self.keeplotate_count = 0
                self.image = bullets[self.shape[0]][self.shape[1]][self.keeplotate_count]
                self.rect = self.image.get_rect(center = (self.pos[0],self.pos[1]))  
            if not self.move_fun and not time_stop:
                self.pos = calculate_new_xy(self.pos, self.speed*2, -self.direction)
            self.rect.center = self.pos
            dist = distance(self.pos,player.pos)

            # 플레이어가 탄을 스치면 추가점수
            if self.grazed and dist <= 25 and not player.godmod:
                s_graze.play()
                score += score_setting[3]
                self.grazed = False        
            # 화면에 없으면 없애기           
            if not self.screen_die and not small_border.colliderect(self.rect):            
                self.kill()
            if self.screen_die and not bullet_border.colliderect(self.rect):
                self.kill()
    
        def change_shape(self,bul,col):
            self.image = bullets[bul][col] if not (bul == 10 or bul == 11 or bul == 14) else bullets[bul][col][0]
            self.image2 = self.image.copy()
            self.lotate = False if bul == 2 or bul == 3 or bul == 10 or bul==11 or bul == 12 or bul == 15 or bul == 10 or bul == 14 or bul == 19 else True   
            if self.lotate: 
                self.image = pygame.transform.rotate(self.image2, self.direction-90)
                self.rect = self.image.get_rect(center = (int(self.pos[0]),int(self.pos[1])))
            self.keeplotate = True if (bul == 10 or bul == 11 or bul == 14) else False
            self.rect = self.image.get_rect(center = (round(self.pos[0]),round(self.pos[1])))
    ############################################

    class MagicField(pygame.sprite.Sprite):
        def __init__(self, pos, direction, speed, mod, screen_die = 0):
            # 이미지
            pygame.sprite.Sprite.__init__(self)
            self.image = magic_circle_sprite[0]
            
            # 쓸 값
            self.rect = self.image.get_rect(center = pos)
            self.pos = (pos[0], pos[1])
            self.direction = direction
            self.speed = speed
            self.radius = 8
            self.count = 0
            self.count2 = 1
            self.spr_trun = 0
            self.mod = mod
            self.screen_die = screen_die

        def update(self, screen):
            mod = math.trunc(self.mod)
            magic_type(self,mod)

            try:
                self.spr_trun += 1
                self.image =magic_circle_sprite[self.spr_trun]
            except:
                self.spr_trun = 0
                self.image =magic_circle_sprite[0]
            # 각도 계산후 위치 업데이트
            self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
            self.rect = self.image.get_rect(center = get_new_pos((self.pos)))
                # 화면에 없으면 없애기
            if not bullet_border.colliderect(self.rect) and self.screen_die == 0:
                self.kill()    
    ############################################

    class Effect(pygame.sprite.Sprite):
        def __init__(self, pos, num, col=0):
            pygame.sprite.Sprite.__init__(self) # 초기화?
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA) # 이미지          
            self.rect = self.image.get_rect(center = (round(pos[0]), round(pos[1])))
            self.image2 = self.image.copy()
            self.pos = pos
            self.count = 0
            self.num = num
            self.col = col

        def update(self):
            if self.num == 1: # 적 사망 파란 포켓볼
                self.count += 1
                try: self.image = enemy_died_circle[self.count -1]
                except:self.kill()
            if self.num == 2: # 탄 효과
                self.count += 1
                try:
                    self.image = bullet_taning[self.col][len(bullet_taning)-self.count]
                    if 64-self.count < 1: self.kill()
                except: self.kill()
            if self.num == 3: # 커지고 투명 원 안채워짐
                self.count += 1
                try: self.image = died_white_circle[self.count -1]
                except:self.kill()
            if self.num == 4: # 보스 주위에 도는 하얀 포켓볼
                self.pos = boss.pos
                if self.count == 360:self.count = 0
                self.image = boss_circle[self.count]
                if not boss.appear:self.kill()
            if self.num == 5: # 커지는 투명 원
                self.count += 1
                try:self.image = white_circle[self.count]
                except: self.kill()
            if self.num == 6:
                self.pos = boss.pos
                self.count += 1
                try:self.image = white_circle[len(white_circle)-1-self.count]
                except: self.kill()
            if self.num == 7: # 탄 삭제 효과
                try:self.image = bullet_erase[self.col][len(bullet_erase)-1-self.count]  
                except:
                    if not self.count == 0:
                        self.kill()
                    else:
                        self.col -= 1
                self.count += 1
            if self.num == 8: # 기보으기
                if self.count == 0:s_ch2.play()
                self.count += 6
                if self.count >= len(white_circle):self.kill() 
                self.image = white_circle[len(white_circle)-self.count]                         
            if self.num == 99:
                self.count += 1
                try:self.image = black_screen[self.count-1]   
                except:self.kill()  

            self.rect = self.image.get_rect(center = get_new_pos((self.pos)))
            self.count += 1

    class Item(pygame.sprite.Sprite):
        def __init__(self, pos, num):
            pygame.sprite.Sprite.__init__(self) # 초기화?
            self.image = items[num]      # 이미지          
            self.rect = self.image.get_rect(center = (round(pos[0]), round(pos[1])))
            self.pos = (pos[0]/2,pos[1]/2)
            self.count = 0
            self.num = num
            self.lock = False

        def update(self):
            global score
            # 화면 넘어가면 삭제:
            if not self.lock:
                if self.count < 80:
                    self.pos = (self.pos[0]+5-self.count/8,self.pos[1])
                else:
                    if self.num == 1: self.lock = True
                    self.pos = (self.pos[0]-2.5,self.pos[1])

            if self.pos[0] < -10:
                if self.num == 0: 
                    if player.power > 100: player.power -= 1
                self.kill() 
            # 플레이어 범위 작으면 먹기
            if distance(self.pos,player.pos) < 35:
                if self.num == 0: 
                    if player.power < 450: player.power += 1 # 먹으면 파워업
                    score += 2000
                if self.num == 1:
                    score += 1000
                s_item0.play()
                self.kill()
            # 좌표 600이상이면 플레이어 다라가기
            if player.pos[0] >= 300 and not self.lock:
                self.lock = True
            if self.lock:
                self.pos = calculate_new_xy(self.pos,13,-look_at_player(self.pos))


            self.rect = self.image.get_rect(center = get_new_pos((self.pos)))
            self.count += 1

    class UI():
        def __init__(self,val):
            self.val = val
            self.ui_font = pygame.font.Font(FONT_1, 15)
            self.ui_font2 = pygame.font.Font(FONT_1, 14)
            self.power= pygame.Surface((100, 20), pygame.SRCALPHA)
            self.power_xy = (30,29)
            self.skill_xy = (115,6)
            self.ui_img = pygame.Surface((400,80), pygame.SRCALPHA)
            self.ui_img.blit(ui_img,(0,0),(0,0,400,80))
            self.ui_img = pygame.transform.scale(self.ui_img, (200, 40))
            self.power_pallete = pygame.Surface((400,80), pygame.SRCALPHA)
            self.power_pallete_rect = Rect(0,0,240,85)

        def draw(self):
            if boss.attack_start and boss.health > 0: # 보스 체력바 그리기
                try:
                    drawArc(up_render_layer, (0, 0, 0), boss.pos, 56, 7, 360*100,255 if distance(player.pos,boss.pos) >= 200 else 50)
                    drawArc(up_render_layer, (0, 66, 107), boss.pos, 58, 3, 360*boss.real_health/boss.real_max_health,255 if distance(player.pos,boss.pos) >= 200 else 50)
                    drawArc(up_render_layer, health_color(boss.health/boss.max_health), boss.pos, 55, 5, 360*boss.health/boss.max_health,255 if distance(player.pos,boss.pos) >= 200 else 50)
                except:pass  
            if player.power < 100:pygame.draw.rect(self.power_pallete, (0, 59, 117), ((self.power_xy),(round(player.power*1.4),9)))
            else:pygame.draw.rect(self.power_pallete, (0, 59, 117), ((self.power_xy),(140,9)))
            if player.power < 200:pygame.draw.rect(self.power_pallete, (19, 97, 173), ((self.power_xy),(round(player.power*1.4-100*1.4),9)))
            else:pygame.draw.rect(self.power_pallete, (19, 97, 173), ((self.power_xy),(140,9)))
            if player.power < 300:pygame.draw.rect(self.power_pallete, (41, 129, 214), ((self.power_xy),(round(player.power*1.4-200*1.4),9)))
            else:pygame.draw.rect(self.power_pallete, (41, 129, 214), ((self.power_xy),(140,9)))
            if player.power < 400:pygame.draw.rect(self.power_pallete, (74, 162, 247), ((self.power_xy),(round(player.power*1.4-300*1.4),9)))
            else:pygame.draw.rect(self.power_pallete, (74, 162, 247), ((self.power_xy),(140,9)))   
            self.power_pallete.blit(self.ui_img,(0,0))
            text = self.ui_font2.render(str(player.power), True, (255,255,255))
            self.power_pallete.blit(text,get_new_pos(self.power_xy,285/2,-15/2)) 
            text = self.ui_font.render("MP " + str(player.mp)+"/ 8", True, (255,255,255))
            self.power_pallete.blit(text,self.skill_xy)
            
            self.power_pallete.fill((255, 255, 255, 50 if self.power_pallete_rect.collidepoint(player.pos) else 255), special_flags=pygame.BLEND_RGBA_MULT)
            up_render_layer.blit(self.power_pallete,(0,0))

            score_text = score_font.render(str(score).zfill(10), True, (255,255,255))
            up_render_layer.blit(score_text,(WIDTH-score_text.get_rect().width,0))            
    class Under_PI():
        def __init__(self):
            self.slow_image = slow_player_circle[0]
            self.rect = self.slow_image.get_rect(center = get_new_pos(player.pos))
            self.slow_count = 0
            self.pos = player.pos

        def draw(self):
            if keys[pygame.K_LSHIFT]:
                self.pos = player.pos
                self.slow_image = slow_player_circle[self.slow_count]
                pygame.draw.circle(render_layer, (255,0,0), self.rect.center, 3)
                self.rect = self.slow_image.get_rect(center = get_new_pos(self.pos))
                render_layer.blit(self.slow_image, self.rect.topleft)
                self.slow_count += 1
                if self.slow_count >= len(slow_player_circle): self.slow_count = 0


            if starting and not read_end: # 원형 체력바 그리기
                if player.godmod: drawArc(render_layer, (0, 194, 247), player.pos, 58, 11, 360*player.godmod_count/player.max_godmod_count,255)
                drawArc(render_layer, (0,0,0), player.pos, 56, 8, 360*100,120 if not player.godmod else 255)
                if player.godmod: drawArc(render_layer, health_color(player.health/player.max_health), player.pos, 55, 5, 360*player.before_health/player.max_health,120)
                drawArc(render_layer, health_color(player.health/player.max_health), player.pos, 55, 5, 360*player.health/player.max_health,120 if not player.godmod else 255)


    class TextBox():
        def __init__(self):
            self.image1 =  pygame.Surface((100,200), pygame.SRCALPHA)
            self.image2 =  pygame.Surface((100,200), pygame.SRCALPHA)
            self.image1.fill((255,255,255))
            self.image2.fill((255,255,255))
            self.stat = 0
            self.text = ""
            self.text2 = ""
            self.started = False
            self.pause = False
            self.count = 0
            self.font = pygame.font.Font(FONT_1, 20)
            self.textbox = pygame.Surface((490,1), pygame.SRCALPHA)
            self.textbox.fill((0,0,0,150))
            self.turn = 0
            self.char_move = [-80,-80]
            self.boss_appear_img = False
        
        def next_text(self):
            self.count = 50
            text = ""
            if self.started and not self.pause:
                self.stat += 1
                if boss.num == 2:
                    if self.stat == 1:
                        self.turn = 0
                        text = "요즘 따라 좀 덥네"
                        self.turn
                    if self.stat == 2:
                        self.turn = 0
                        text = "이럴땐 호수에서 자는게 제일인데~"
                    if self.stat == 3:
                        self.turn = 1
                        boss.real_appear = True
                        self.boss_appear_img = True
                        text = "더위를 피할거라면"
                    if self.stat == 4:
                        self.turn = 1
                        text = "큰 나무 밑에 있어봐 꽤 시원하다구"
                    if self.stat == 5:
                        self.turn = 0
                        text = "말만 그렇지 '엄청' 시원하지 않다고"
                    if self.stat == 6:
                        self.turn = 1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(BOSS_BGM1)
                        pygame.mixer.music.play(-1)
                        text = "그럼 내가 엄청 시원하게 해줄게!"
                    if self.stat == 7:
                        # 보스전 시작
                        self.pause = True
                        boss.attack_start = True
                        self.char_move = [-80,-80]
                        boss.count = 0
                        self.count = 0
                    if self.stat == 8:
                        self.turn = 0
                        text = "확실히 시원하긴 하네~"
                        boss.count = 0
                    if self.stat == 9:
                        # 대화 끝
                        self.boss_appear_img = False
                        self.started = False
                        self.count = 0
                if boss.num == 4:
                    if self.stat == 1:
                        self.turn = 0
                        text = "바다는 시원할줄 알았는데_여기도 조금 덥네"
                    if self.stat == 2:
                        self.turn = 1
                        text = "너무 더워~"
                    if self.stat == 3:
                        self.turn = 1
                        boss.real_appear = True
                        self.boss_appear_img = True
                        text = "요즘따라 바다속이 더 따뜻해졌어"
                    if self.stat == 4:
                        self.turn = 0
                        text = "넌 원래 바다속에 있어야 되지않니?"
                    if self.stat == 5:
                        self.turn = 1
                        text = "바다에 산소가 부족해져서 나왔는데_더 더워"
                    if self.stat == 6:
                        self.turn = 1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(BOSS_BGM2)
                        pygame.mixer.music.play(-1)
                        text = "하지만 너랑 싸울 기회는 노칠 수 없지!"
                    if self.stat == 7:
                        # 보스전 시작
                        self.pause = True
                        boss.attack_start = True
                        self.char_move = [-80,-80]
                        boss.count = 0
                        self.count = 0
                    if self.stat == 8:
                        self.turn = 0
                        text = "이렇게 싸우면 숨쉬러 나오는 의미가 없잖아"
                        boss.count = 0
                    if self.stat == 9:
                        self.turn = 1
                        text = "흐어..억. 그러네.."
                    if self.stat == 10:
                        # 대화 끝
                        self.boss_appear_img = False
                        self.started = False
                        self.count = 0
                if boss.num == 6:
                    if self.stat == 1:
                        self.turn = 0
                        text = "갑자기 여름이 되서 그런가_덤비는 얘들이 많네"
                    if self.stat == 2:
                        self.turn = 1
                        text = "힘을 얻어서 그래"
                    if self.stat == 3:
                        self.turn = 1
                        boss.real_appear = True
                        self.boss_appear_img = True
                        text = "내 노래 덕분에 힘이 커진거지"
                    if self.stat == 4:
                        self.turn = 0
                        text = "그러면 아까 치코리타도 너가 한짓이니?"
                    if self.stat == 5:
                        self.turn = 1
                        text = "그렇다고 볼 수 있지~_(치코리타 아닌데..)"
                    if self.stat == 6:
                        self.turn = 1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(BOSS_BGM3)
                        pygame.mixer.music.play(-1)
                        text = "모처럼 온김에 내 노래도 들어줘라!"
                    if self.stat == 7:
                        # 보스전 시작
                        self.pause = True
                        boss.attack_start = True
                        self.char_move = [-80,-80]
                        boss.count = 0
                        self.count = 0
                    if self.stat == 8:
                        self.turn = 0
                        text = "입장료는 냈지?"
                        boss.count = 0
                    if self.stat == 9:
                        self.turn = 1
                        text = "그래.."
                    if self.stat == 10:
                        # 대화 끝
                        self.boss_appear_img = False
                        self.started = False
                        self.count = 0
                if boss.num == 8:
                    if self.stat == 1:
                        self.turn = 0
                        text = "동굴안이라고 시원하지 않네_열기가 벌써 안까지 들어온건가?"
                    if self.stat == 2:
                        self.turn = 1
                        text = "침입자인가?"
                    if self.stat == 3:
                        self.turn = 1
                        boss.real_appear = True
                        self.boss_appear_img = True
                        text = "여기서 당장 나가시지?_같은 포켓몬이라 해도 서로 해치는건 안된다고"
                    if self.stat == 4:
                        self.turn = 0
                        text = "넌 누구를 보호하고 있는거냐?"
                    if self.stat == 5:
                        self.turn = 1
                        text = "그건 알려줄 수 없다!"
                    if self.stat == 6:
                        self.turn = 1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(BOSS_BGM4)
                        pygame.mixer.music.play(-1)
                        text = "그 정체를 알고싶다면_날 먼저 쓰러뜨려야 할 것 이다!"
                    if self.stat == 7:
                        # 보스전 시작
                        self.pause = True
                        boss.attack_start = True
                        self.char_move = [-80,-80]
                        boss.count = 0
                        self.count = 0
                    if self.stat == 8:
                        self.turn = 0
                        text = "자 그럼 지나간다?"
                        boss.count = 0
                    if self.stat == 9:
                        self.turn = 1
                        text = "흑흑.. 죄송합니다!"
                    if self.stat == 10:
                        # 대화 끝
                        self.boss_appear_img = False
                        self.started = False
                        self.count = 0
                if boss.num == 10:
                    if self.stat == 1:
                        self.turn = 0
                        text = "동굴안이라고 시원하지 않네_열기가 벌써 안까지 들어온건가?"
                    if self.stat == 2:
                        self.turn = 1
                        text = "침입자인가?"
                    if self.stat == 3:
                        self.turn = 1
                        boss.real_appear = True
                        self.boss_appear_img = True
                        text = "여기서 당장 나가시지?_같은 포켓몬이라 해도 서로 해치는건 안된다고"
                    if self.stat == 4:
                        self.turn = 0
                        text = "넌 누구를 보호하고 있는거냐?"
                    if self.stat == 5:
                        self.turn = 1
                        text = "그건 알려줄 수 없다!"
                    if self.stat == 6:
                        self.turn = 1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(BOSS_BGM5)
                        pygame.mixer.music.play(-1)
                        text = "그 정체를 알고싶다면_날 먼저 쓰러뜨려야 할 것 이다!"
                    if self.stat == 7:
                        # 보스전 시작
                        self.pause = True
                        boss.attack_start = True
                        self.char_move = [-80,-80]
                        boss.count = 0
                        self.count = 0
                    if self.stat == 8:
                        self.turn = 0
                        text = "자 그럼 지나간다?"
                        boss.count = 0
                    if self.stat == 9:
                        self.turn = 1
                        text = "흑흑.. 죄송합니다!"
                    if self.stat == 10:
                        # 대화 끝
                        self.boss_appear_img = False
                        self.started = False
                        self.count = 0
                if boss.num == 11:
                    if self.stat == 1:
                        self.turn = 0
                        text = "동굴안이라고 시원하지 않네_열기가 벌써 안까지 들어온건가?"
                    if self.stat == 2:
                        self.turn = 1
                        text = "침입자인가?"
                    if self.stat == 3:
                        self.turn = 1
                        boss.real_appear = True
                        self.boss_appear_img = True
                        text = "여기서 당장 나가시지?_같은 포켓몬이라 해도 서로 해치는건 안된다고"
                    if self.stat == 4:
                        self.turn = 0
                        text = "넌 누구를 보호하고 있는거냐?"
                    if self.stat == 5:
                        self.turn = 1
                        text = "그건 알려줄 수 없다!"
                    if self.stat == 6:
                        self.turn = 1
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(BOSS_BGM6)
                        pygame.mixer.music.play(-1)
                        text = "그 정체를 알고싶다면_날 먼저 쓰러뜨려야 할 것 이다!"
                    if self.stat == 7:
                        # 보스전 시작
                        self.pause = True
                        boss.attack_start = True
                        self.char_move = [-80,-80]
                        boss.count = 0
                        self.count = 0
                    if self.stat == 8:
                        self.turn = 0
                        text = "자 그럼 지나간다?"
                        boss.count = 0
                    if self.stat == 9:
                        self.turn = 1
                        text = "흑흑.. 죄송합니다!"
                    if self.stat == 10:
                        # 대화 끝
                        self.boss_appear_img = False
                        self.started = False
                        self.count = 0
                if self.stat > 0:
                    textlist = text.split('_')
                    self.text = self.font.render(textlist[0], True, (255,255,255) if self.turn == 0 else (255, 87, 84))
                    if len(textlist) == 2: self.text2 = self.font.render(textlist[1], True, (255,255,255) if self.turn == 0 else (255, 87, 84))     
                    else: self.text2 = self.font.render("", True, (255,255,255))

        def update(self):
            self.count += 1
            if self.count <= 50:
                self.textbox = pygame.transform.scale(self.textbox, (440, self.count*2))
            if self.count == 50:
                self.next_text()
            if self.count > 50:
                if self.turn == 0:
                    if self.char_move[0] < 10: self.char_move [0] += 2
                    if self.char_move[0] < 0: self.char_move [0] += 4
                    if self.char_move[1] > 0: self.char_move [1] -= 2
                    if self.char_move[1] < 0: self.char_move [1] += 4
                else:
                    if self.char_move[1] < 10: self.char_move [1] += 2
                    if self.char_move[1] < 0: self.char_move [1] += 4
                    if self.char_move[0] > 0: self.char_move [0] -= 2
                    if self.char_move[0] < 0: self.char_move [0] += 4

        def draw(self):
            if self.started and not self.pause:
                try:                    
                    if self.stat > 0: 
                        if self.count >= 50: # 대화              
                            up_render_layer.blit(self.image1,(0+self.char_move[0],HEIGHT-200-self.char_move[0]))
                            if self.boss_appear_img: up_render_layer.blit(self.image2,(WIDTH-100-self.char_move[1],HEIGHT-200-self.char_move[1]))
                        up_render_layer.blit(self.textbox,(50,HEIGHT-125))
                        up_render_layer.blit(self.text,(100,HEIGHT-115))
                        up_render_layer.blit(self.text2,(100,HEIGHT-90))
                    else:
                        up_render_layer.blit(self.textbox,(50,HEIGHT-125)) # 텍스트 박스 등장시간
                except:
                    pass

        def re_start(self):
            self.image1 =  pygame.Surface((200,400), pygame.SRCALPHA)
            self.image2 =  pygame.Surface((200,400), pygame.SRCALPHA)
            self.image1.fill((255,255,255))
            self.image2.fill((255,255,255))
            self.stat = 0
            self.text = ""
            self.text2 = ""
            self.started = False
            self.pause = False
            self.count = 0
            self.font = pygame.font.Font(FONT_1, 40)
            self.textbox = pygame.Surface((980,1), pygame.SRCALPHA)
            self.textbox.fill((0,0,0,150))
            self.turn = 0
            self.char_move = [-80,-80]
    class Back_Ground():
        def __init__(self, img, rect, speed, num, y=0,not_appear=False):
            image = pygame.Surface((rect[2],rect[3]), pygame.SRCALPHA)
            image.blit(img, (0,0), rect)
            self.image = image
            self.speed = speed
            self.num = num
            self.x = 0
            self.y = y
            self.appear = not_appear
        def update(self):
            self.x -= self.speed

    def bullet_clear():
        if spr:
            for bullet in spr.sprites():
                add_effect(bullet.pos,7,bullet.shape[1])
                bullet.kill()
    def enemy_clear():
        if enemy_group:
            for i in enemy_group.sprites():
                i.health = -999

    def get_new_pos(pos,x=0,y=0):
        return (round(pos[0] + x), round(pos[1] + y))

    def remove_allbullet():
        for i in spr.sprites():
            item_group.add(Item(i.pos,1))
        for i in magic_spr.sprites():
            item_group.add(Item(i.pos,0))
        spr.empty()
        magic_spr.empty()

    def big_small(val,min,max):
        return min < val and val < max

    def when_time(val,time):
        return val == time

    def while_time(val,time):
        return val % time == 0

    def bullet(pos,dir,speed,img,col,mode=0,num = (0,0)):
        spr.add(Bullet(pos[0]*2,pos[1]*2,dir,speed,img,col,mode,num))
    def sbullet(pos,dir,speed,img,col,mode=0,num = (0,0)):
        spr.add(Bullet(pos[0],pos[1],dir,speed,img,col,mode,num))
    def bullet_effect(sound,col,pos,only_sound = False):
        if not sound == 0:
            if sound == s_tan1:tan_channel.play(sound)
            elif sound == s_kira0:kira_channel.play(sound)
            else:sound.play()
        if not only_sound:add_effect(pos,2,col)
    def sbullet_effect(sound,col,pos,only_sound = False):
        if not sound == 0:
            if sound == s_tan1:tan_channel.play(sound)
            elif sound == s_kira0:kira_channel.play(sound)
            else:sound.play()
        if not only_sound:add_effect((pos[0]/2,pos[1]/2),2,col)
    def add_effect(pos,num,col=0):
        effect_group.add(Effect(pos,num,col))

    def magic_bullet(pos,dir,speed,mode=0,screend=0):
        magic_spr.add(MagicField(pos,dir,speed/2,mode,screend))

    def calculate_new_xy(old_xy, speed, angle_in_degrees, no_delta = False):
        move_vec = pygame.math.Vector2()
        move_vec.from_polar((speed/2, angle_in_degrees))
        if not no_delta: move_vec = (move_vec[0]*dt,move_vec[1]*dt)
        return (old_xy[0] + move_vec[0],old_xy[1] + move_vec[1])

    def noreturn_xy(speed, angle_in_degrees):
        move_vec = pygame.math.Vector2()
        move_vec.from_polar((speed, angle_in_degrees))
        return move_vec

    def distance(f_pos,sec_pos):
        if str(type(f_pos)) == "<class 'int'>": f_pos = (0,0)
        if str(type(sec_pos)) == "<class 'int'>": sec_pos = (0,0)
        return math.hypot(f_pos[0]-sec_pos[0], f_pos[1]-sec_pos[1])

    def move_circle(pos, angle,radius):
        return (round(pos[0]+math.cos(math.pi * (angle / 180)) * radius,2),round(pos[1]+math.sin(math.pi * (angle / 180)) * radius,2))
    # 두점 각도
    def look_at_point(fpos,secpos):
        x, y = fpos
        dx, dy = secpos
        angle = math.degrees(math.atan2(y - dy, dx - x))
        return angle 

    def look_at_player(pos):
        x, y = pos
        dx, dy = player.pos
        angle = math.degrees(math.atan2(y - dy, dx - x))
        return angle      

    def set_bossmove_point(pos,speed,miss,chum=True):
        try:
            if chum:
                if not boss.move_ready:
                    if boss.move_point == (0,0):
                        boss.move_point = ((pos[0]-boss.pos[0])/speed,(pos[1]-boss.pos[1])/speed) 
                        if boss.move_point == (0,0):
                            boss.move_point = (0.1,0.1)
                    boss.pos = (boss.pos[0] + boss.move_point[0],boss.pos[1] + boss.move_point[1])                 
                    if distance(pos,boss.pos) < miss and boss.move_point != (0,0):
                        boss.move_point = (0,0)
                        boss.pos = (pos[0],pos[1])
                        boss.move_ready = True
            else:
                if boss.move_point == (0,0):
                    boss.move_point = ((pos[0]-boss.pos[0])/speed,(pos[1]-boss.pos[1])/speed) 
                    if boss.move_point == (0,0):
                        boss.move_point = (0.1,0.1)
                boss.pos = (boss.pos[0] + boss.move_point[0],boss.pos[1] + boss.move_point[1])                 
                if distance(pos,boss.pos) < miss and boss.move_point != (0,0):
                    boss.move_point = (0,0)
                    boss.pos = (pos[0],pos[1])               
        except IndexError as e:
            pass      
        return (boss.pos)
    # 동그라미 게이지 (퍼옴)
    def drawArc(surf, color, center, radius, width, end_angle,alpha=255):
        circle_image = numpy.zeros((radius*2+4, radius*2+4, 4), dtype = numpy.uint8)
        circle_image = cv2.ellipse(circle_image, (radius+2, radius+2),
        (radius-width//2, radius-width//2), -90, 0, end_angle, (*color, alpha), width, lineType=cv2.LINE_AA) 
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

    def background_scroll():
        if boss.spell and boss.appear and boss.spell[0].spellcard :
            rel_x = 3*-frame_count % WIDTH
            render_layer.blit(boss_background, (rel_x - WIDTH,0))
            if rel_x < WIDTH:
                render_layer.blit(boss_background,(rel_x,0))
        else:
            if bkgd_list:
                for image in bkgd_list:
                    rel_x = image.x % WIDTH
                    if not image.appear:
                        render_layer.blit(image.image, (rel_x - WIDTH,image.y))
                    if rel_x < WIDTH:
                        render_layer.blit(image.image,(rel_x,image.y))
                    if image.appear and rel_x == 0: 
                        bkgd_list[bkgd_list.index(image)].appear = False
                        if image.num == 4:delete_background(2)
                        if image.num == 5:delete_background(1)
                        if image.num == 8:delete_background(7)
                        if image.num == 9:delete_background(6)

    def delete_background(num):
        for img in bkgd_list:
            if img.num == num:
                del bkgd_list[bkgd_list.index(img)]

    def randfloat(min,max):
        return round(uniform(min,max),1)
    
    def set_direction(dir,pdor,add):
        a_dir = dir
        while a_dir >= 360 or a_dir < 0:
            if a_dir >= 360:
                a_dir -= 360
            if a_dir < 0:
                a_dir += 360
        set_dir = pdor - a_dir
        if set_dir > 0:
            a_dir += add
            if a_dir > pdor:
                a_dir = pdor
        elif set_dir < 0:
            a_dir -= add
            if a_dir < pdor:
                a_dir = pdor
        return a_dir
    def dpos(pos):
        return (pos[0]/2,pos[1]/2)

    def set_go_boss(speed,dir,count):
        if dir > 180: 180-dir
        if boss.move_time <= 0:
            if not boss.box_disable:
                if boss.pos[0] < boss_movebox.x+boss.rect.width:
                    if big_small(dir,90,180) or big_small(dir,-180,-90):dir = -dir+180 
                    if abs(dir) == 180: dir = 0
                if boss.pos[0] > boss_movebox.x+boss_movebox.width-boss.rect.width:
                    if big_small(dir,270,360) or big_small(dir,0,90):-dir+180 
                    if abs(dir) == 0: dir = 180
                if boss.pos[1] < boss_movebox.y+boss.rect.height:
                    if big_small(dir,0,180):-dir+180 
                    if abs(dir) == -90: dir = 90
                if boss.pos[1] > boss_movebox.y+boss_movebox.height-boss.rect.height:
                    if big_small(dir,-180,0):-dir+180 
                    if abs(dir) ==90: dir = -90            
            boss.move_dir = dir
            boss.move_speed = speed
            boss.move_time = count
    def go_boss():
        pos = list(calculate_new_xy(boss.pos, boss.move_speed, boss.move_dir))
        if not boss.box_disable:
            if pos[0] < boss_movebox.x:
                pos[0] = boss_movebox.x
            if pos[0] > boss_movebox.x+boss_movebox.width:
                pos[0] = boss_movebox.x+boss_movebox.width
            if pos[1] < boss_movebox.y:
                pos[1] = boss_movebox.y
            if pos[1] > boss_movebox.y+boss_movebox.height:
                pos[1] = boss_movebox.y+boss_movebox.height
        boss.move_time -= 1
        if boss.move_time == 0:
            boss.move_speed = 0
            boss.move_dir = 0
        return pos
    # 개발자 전용
    
    global bkgd, time_stop
    global stage_count, boss_group 
    # 초기 설정
    enemy_group = pygame.sprite.Group()
    boss = Boss_Enemy(-99,-99)
    boss_group = pygame.sprite.Group(boss)
    play = True
    full_on = False
    cur_full_mod = False
    pause = False
    frame_count = 0
    time_stop = False
    stage_count = 0
    
    
    global stage_line, stage_cline, stage_repeat_count, stage_condition, stage_challenge, stage_fun
    stage_fun = 0
    stage_line = 0
    stage_cline = 0
    stage_repeat_count = 0
    stage_condition = 1
    stage_challenge = 0

    # 게임 시작전 메뉴 변수들
    curser = 0
    curser_max = 4
    select_mod = 0
    menu_mod = -1
    difficulty = 0
    character = 0
    cur_screen = 0

    bullet_border_wide = 200
    bullet_border = Rect(0-bullet_border_wide, 0-bullet_border_wide, WIDTH*2 + bullet_border_wide*2, HEIGHT*2 + bullet_border_wide*2)
    small_border = Rect(0, 0, WIDTH*2, HEIGHT*2)
    bullet_size = (10,6,8,8,6,6,6,9,6,7,7,4,5,15,15,20,10,10,10,20)
    lazer_spawner = []
    spr = pygame.sprite.Group()
    magic_spr = pygame.sprite.Group()
    player = Player(-125,-125,5,500)
    player_group = pygame.sprite.Group(player)
    player_hitbox = Player_hit()
    player_sub = Player_sub(1)
    bomb_group = pygame.sprite.Group()
    bomb_hit_group = pygame.sprite.Group()
    bomb_activated = False
    title = Tittle(1)
    ui = UI(1)
    under_ui = Under_PI()
    text = TextBox()
    beams_group = pygame.sprite.Group()
    effect_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    
    starting = True
    read_end = False
    boss_movepoint = []
    boss_movebox = Rect(300,35,204,292)

    # 점수 코어
    global score
    score = 0
    score_setting = (10,10,987650,10,0,0,0,0,0)
    slow_img = 0

    # 보스마다 기본설정
    global bkgd_list,boss_background
    bkgd_list = []
    boss_background = pygame.Surface((1080,720))
    # 폰트 불러오기
    score_font = pygame.font.Font(FONT_1, 25)
    
    # 스펠카드 모음
    spells = [Spell(1,1000,False),Spell(2,1000,True),Spell(3,1000,False),Spell(4,1300,True),\
    Spell(5,1300,True),Spell(6,1300,False),Spell(7,1300,True),Spell(8,1300,False),Spell(9,2000,True),Spell(10,1300,False),\
        Spell(11,2800,True),Spell(12,2000,True),Spell(13,1000,False),Spell(14,1000,False),Spell(15,1000,False),Spell(16,2000,True),Spell(17,1000,False),Spell(18,2000,True),\
            Spell(19,1000,False),Spell(20,1000,True),Spell(21,1000,True),Spell(22,1000,False),Spell(23,1000,False),Spell(24,1000,False),\
                Spell(25,2100,True),Spell(26,1100,False,),Spell(27,1500,True),Spell(28,800,False),Spell(29,2200,True),Spell(30,1500,True),\
                    Spell(31,1000,False),Spell(32,1000,False),Spell(33,1200,False),Spell(34,1600,True,4,"불에 뜨겁게 달궈진","사이코필드"),Spell(35,1200,False),Spell(36,2000,True,1,"차분하고 뒤엉킨","V제너렉트"),\
                        Spell(37,1200,False),Spell(38,1500,True),Spell(39,1800,True),Spell(40,1200,False)]

    # 소환 반복 (줄에 stage_line)
    def while_poke_spawn(time,repeat,line):
        global stage_cline, stage_line, stage_repeat_count, stage_count
        if stage_line == stage_cline and stage_count == time:
            return stage_count == time and stage_line == stage_cline and stage_repeat_count < repeat
        else:
            stage_cline += line 
            return False

    def end_while_poke_spawn(line,repeat):
        global stage_line, stage_repeat_count, stage_cline  
        stage_line -= line
        stage_repeat_count += 1
        if stage_repeat_count >= repeat:
            stage_line += line
            stage_repeat_count = 0

    # 다음 챌린지 넘어가기
    def next_challenge(time,kill = False):
        global stage_count, stage_line, stage_cline, stage_challenge
        if time == stage_count and stage_line == stage_cline:
            stage_count = 0
            stage_line = 0
            stage_challenge += 1
            if not kill:
                enemy_clear()
                bullet_clear()           
    # 스테이지 이름
    def title_spawn(val,time):
        global stage_count 
        global stage_line # 현재 조건의 라인
        global stage_cline # 검사 중인 라인
        
        # x, y, dir, speed, health, img, hit_cir, num = val
        if time == stage_count and stage_line == stage_cline:
            stage_count = 0
            stage_line += 1
            if val == 1:
                title.title_start("Stage 1","드넓은 초원")
            if val == 2:    
                title.title_start("Stage 2","왕자가 숨은 바다")
            if val == 3:    
                title.title_start("Stage 3","흔적없는 과거의 자취")
            if val == 4:    
                title.title_start("Stage 4","땅속 깊은 생명보호")
            if val == 5:    
                title.title_start("Stage 5","고대의 성")
            if val == 6:    
                title.title_start("Stage 5","화가 존재하는 현실")
        stage_cline += 1
    # 뒷배경 소환
    def bground_spawn(val,time):
        global stage_count 
        global stage_line # 현재 조건의 라인
        global stage_cline # 검사 중인 라인
        
        # x, y, dir, speed, health, img, hit_cir, num = val
        if time == stage_count and stage_line == stage_cline:
            stage_count = 0
            stage_line += 1
            if val == 1:bkgd_list.append(Back_Ground(bg_image,(1080,0,1080,240),1,3,0,True))
            if val == 2:bkgd_list.append(Back_Ground(bg_image,(1080,480,1080,240),3,4,480,True))
            if val == 3:bkgd_list.append(Back_Ground(bg_image,(2160,0,1080,580),2,5,0,True)) 
            if val == 8:bkgd_list.append(Back_Ground(bg_image,(1080,972,1080,468),2,8,252,True))
            if val == 9:bkgd_list.append(Back_Ground(bg_image,(1080,720,1080,252),1,9,0,True))
        stage_cline += 1
    # 게임의 배경, 스테이지
    def game_defalt_setting(fun): # 게임 스테이지 배경 정하기
        global bgm_num, bkgd_list
        bkgd_list = []
        ##############################################
        if fun == 1:
            bkgd_list.append(Back_Ground(bg_image,(0,0,1080,240),1,0,0))
            bkgd_list.append(Back_Ground(bg_image,(0,240,1080,240),2,1,240))
            bkgd_list.append(Back_Ground(bg_image,(0,480,1080,240),3,2,480))
        if fun == 2:
            bkgd_list.append(Back_Ground(bg_image,(0,720,1080,464),2,6,0))
            bkgd_list.append(Back_Ground(bg_image,(0,1184,1080,256),3,7,464))
        if fun == 3:
            bkgd_list.append(Back_Ground(bg_image,(0,1440,1080,252),5,8,0))
            bkgd_list.append(Back_Ground(bg_image,(1080,1552,1080,608),7,9,236))
        if fun == 4:
            bkgd_list.append(Back_Ground(bg_image,(0,2160,1080,720),10,10))
            bkgd_list.append(Back_Ground(bg_image,(1080,2160,1080,720),8,11))
        if fun == 5:
            bkgd_list.append(Back_Ground(bg_image,(0,1440,540,360),5,8,12))
        if fun == 6:
            bkgd_list.append(Back_Ground(bg_image,(0,1800,540,360),5,8,0))

        ###############################################
        pygame.mixer.music.stop()
        if fun == 1:
            pygame.mixer.music.load(FIELD_1)
        if fun == 2:
            pygame.mixer.music.load(FIELD_2)
        if fun == 3:
            pygame.mixer.music.load(FIELD_3)
        if fun == 4:
            pygame.mixer.music.load(FIELD_4)
        if fun == 5:
            pygame.mixer.music.load(FIELD_5)
        if fun == 6:
            pygame.mixer.music.load(FIELD_6)
    # 소환하는 적 
    def waiting(time):
        global stage_count 
        global stage_line # 현재 조건의 라인
        global stage_cline # 검사 중인 라인
        
        # x, y, dir, speed, health, img, hit_cir, num = val
        if time == stage_count and stage_line == stage_cline:
            stage_count = 0
            stage_line += 1
        stage_cline += 1
    #################################################
    def pokemon_spawn(val,pos,time,dir=0,speed=0,simple = False):
        global stage_count 
        global stage_line # 현재 조건의 라인
        global stage_cline # 검사 중인 라인
        x = pos[0]
        y = pos[1]        
        # x, y, dir, speed, health, img, hit_cir, num = val
        if (time == stage_count and stage_line == stage_cline) or simple:
            if not simple:
                stage_count = 0
                stage_line += 1
            if stage_fun == 1:
                if val == 1:
                    enemy_group.add(Enemy(x,y,180,4,3,11,30,val))  
                if val == 2:
                    enemy_group.add(Enemy(x,y,180,4,3,12,30,val))  
                if val == 3:
                    enemy_group.add(Enemy(x,y,180,3,6,14,30,val))
                if val == 4:
                    enemy_group.add(Enemy(x,y,180,4,10,13,30,val))
                if val == 5:
                    enemy_group.add(Enemy(x,y,135,6,5,11,30,val))
                if val == 6:
                    enemy_group.add(Enemy(x,y,225,6,5,12,30,val))
                if val == 7:
                    enemy_group.add(Enemy(x,y,dir,4,7,15,30,val))
            ##################### 2 스테이지 #################
            if stage_fun == 2:
                if val == 8:
                    enemy_group.add(Enemy(x,y,dir,speed,7,19,30,val))
                if val == 9:
                    enemy_group.add(Enemy(x,y,180,5,240,17,40,val))
                if val == 10:
                    enemy_group.add(Enemy(x,y,180,4,20,18,30,val))
                if val == 11:
                    enemy_group.add(Enemy(x,y,180+randint(-10,10),4,20,16,30,val))
            ##################### 3 스테이지 $$$$$$$$$$$$$$$$$
            if stage_fun == 3:
                if val == 12:
                    enemy_group.add(Enemy(x,y,180,speed,30,21,30,val))    
                if val == 13:
                    enemy_group.add(Enemy(x,y,dir,speed,80,22,40,val))   
                if val == 14:
                    enemy_group.add(Enemy(x,y,dir,speed,100,23,40,val))   
                if val == 15:
                    enemy_group.add(Enemy(x,y,dir,speed,30,24,40,val)) 
                if val == 16:
                    enemy_group.add(Enemy(x,y,dir,speed,120,25,40,val))
            if stage_fun == 4:
                if val == 17:
                    enemy_group.add(Enemy(x,y,dir,speed,15,30,40,val))
                if val == 18:
                    enemy_group.add(Enemy(x,y,dir,speed,100,27,40,val))
                if val == 19:
                    enemy_group.add(Enemy(x,y,dir,speed,250,29,50,val))
                if val == 20:
                    enemy_group.add(Enemy(x,y,dir,speed,150,28,50,val))               
            if stage_fun == 5:
                if val == 21:
                    enemy_group.add(Enemy(x,y,dir,speed,15,31,30,val))
                if val == 22:
                    enemy_group.add(Enemy(x,y,dir,speed,210,34,60,val))
                if val == 23:
                    enemy_group.add(Enemy(x,y,dir,speed,300,33,30,val))        
                if val == 24:
                    enemy_group.add(Enemy(x,y,dir,speed,100,35,30,val))
                if val == 25:
                    enemy_group.add(Enemy(x,y,dir,speed,100,32,30,val))
                if val == 26:
                    enemy_group.add(Enemy(x,y,dir,speed,20,36,30,val))      
            if stage_fun == 6:
                if val == 27:
                    enemy_group.add(Enemy(x,y,dir,speed,30,37,30,val))       
                if val == 28:
                    enemy_group.add(Enemy(x,y,dir,speed,450,38,30,val))   
                if val == 29:
                    enemy_group.add(Enemy(x,y,dir,speed,300,39,30,val))   
                if val == 30:
                    enemy_group.add(Enemy(x,y,dir,speed,200,40,30,val))              
        
        if not simple: stage_cline += 1
    # 적의 공격타입
    def enemy_attack(num,count,pos,dir,speed,list):
        pos = calculate_new_xy(pos, speed, dir)
        if stage_fun == 1:
            if num == 1:
                if dir > 90 and count > 20: dir -= 1 
                if speed > 3 and count > 20: speed -= 0.5
            if num == 2:
                if dir < 270 and count > 30: dir += 1 
                if speed > 3 and count > 30: speed -= 0.5
            if num == 4:
                if big_small(count,70,130) and speed > 0: speed -= 0.2
                if count > 130 and speed < 5:
                    speed += 0.2
                if count == 100:
                    add_effect(pos,2,2)
                    s_tan1.play()
                    for i in range(0,360,30):
                        bullet(pos,look_at_point(pos,player.pos)+i,5,2,2)
            if num == 5:
                if dir != 180: dir += 0.5
                if count == 50:
                    s_tan1.play()
                    add_effect(pos,2,3)
                    bullet(pos,look_at_player(pos),3,3,3)    
                    bullet(pos,look_at_player(pos)+45,3,3,3) 
                    bullet(pos,look_at_player(pos)-45,3,3,3) 
            if num == 6:
                if dir != 180: dir -= 0.5
                if count == 50:
                    s_tan1.play()
                    add_effect(pos,2,3)
                    bullet(pos,look_at_player(pos),3,3,3)    
                    bullet(pos,look_at_player(pos)+45,3,3,3) 
                    bullet(pos,look_at_player(pos)-45,3,3,3) 
            if num == 7:
                if big_small(count,30,50) and while_time(count,3):
                    s_tan1.play()
                    add_effect(pos,2,5)
                    bullet(pos,180,5-0.5*(count-30)/3,5,5)
                if count > 60:
                    count = 0
        if stage_fun == 2:
            if num == 8:
                if count > 120 and not abs(dir) == 180:
                    if dir < 0: dir -= 1
                    if dir > 0: dir += 1
                if when_time(count,60):
                    bullet_effect(s_tan1,3,pos)
                    bullet(pos,look_at_player(pos),5,2,3)
            if num == 9:
                if count > 60 and not speed == 0:
                    speed -= 0.5
                if while_time(count+1,120):
                    bullet_effect(s_tan1,4,pos)
                    for i in range(0,360,60):
                        bullet(pos,look_at_player(pos)+i,4,1,4)
                        bullet(pos,look_at_player(pos)+i+10,4,1,4)
                        bullet(pos,look_at_player(pos)+i-10,4,1,4)
                        bullet(pos,look_at_player(pos)+i+5,4.5,1,4)
                        bullet(pos,look_at_player(pos)+i-5,4.5,1,4)
                        bullet(pos,look_at_player(pos)+i,5,1,4)
            if num == 10:
                if when_time(count,60):
                    bullet_effect(s_tan1,3,pos)
                    for i in range(0,10):
                        bullet(pos,look_at_player(pos)+randint(-10,10),randfloat(4,6),3,3)
                    speed = 0
                if when_time(count,180):
                    speed = 4
            if num == 11:
                if when_time(count,90):
                    speed = 0
                    s_lazer1.play()
                    lazer_spawner.append([pos,look_at_player(pos),7,3,30])
                if when_time(count,150):
                    speed = 5   
        if stage_fun == 3:
            if num == 12:
                if when_time(count,90):
                    speed = 0
                    bullet_effect(s_tan1,5,pos)
                    s_tan1.play()
                    bullet(pos,look_at_player(pos),5,1,5)
                    bullet(pos,look_at_player(pos)+10,5,1,5)
                    bullet(pos,look_at_player(pos)+20,5,1,5)
                    bullet(pos,look_at_player(pos)-10,5,1,5)
                    bullet(pos,look_at_player(pos)-20,5,1,5)
                if when_time(count,150):
                    speed = 5  
            if num == 13: 
                if count > 60 and speed > 2:
                    speed -= 0.2
                if while_time(count,3):
                    bullet(get_new_pos(pos,0,50),180+90,8,1,3) 
                    bullet(get_new_pos(pos,0,50),180+60,8,1,3) 
                    bullet(get_new_pos(pos,0,50),180+30,8,1,3) 
                    bullet(get_new_pos(pos,0,-50),180-90,8,1,1) 
                    bullet(get_new_pos(pos,0,-50),180-60,8,1,1) 
                    bullet(get_new_pos(pos,0,-50),180-30,8,1,1) 
                if while_time(count,10):
                    bullet_effect(s_tan1,5,get_new_pos(pos,-50,0))
                    bullet(get_new_pos(pos,-50,0),look_at_player(pos),7,3,5) 
            if num == 14: 
                if count > 60 and speed > 0:
                    speed -= 0.5
                if while_time(count,60) and count < 181:
                    bullet(pos,look_at_player(pos),5,15,6,3)
                if count > 300 and speed < 5:
                    speed += 1             
            if num == 15:
                if when_time(count,40):
                    bullet_effect(s_tan1,0,pos)
                    bullet(pos,look_at_player(pos),7,17,0,4)
            if num == 16:
                if while_time(count,2) and big_small(count,0,160):
                    bullet_effect(s_tan1,5,pos)
                    bullet(pos,randint(-70,70),5,9,5,5)
                if while_time(count,4):
                    if speed > -5:
                        speed -= 0.1
        if stage_fun == 4:
            if num == 17:
                if count == 80:
                    bullet_effect(s_tan1,2,pos)
                    bullet(pos,look_at_player(pos),6,13,2)
            if num == 18:
                if while_time(count,20) and count > 60:
                    bullet_effect(s_tan1,0,pos)
                    rand = randint(0,9)
                    for i in range(0,360,10):
                        bullet(pos,i+rand,6,3,0)
                        bullet(pos,i+rand,6,11,0)
                if count > 60:
                    speed -= 0.1
            if num == 19:
                if while_time(count,5) and count > 60:
                    bullet_effect(s_tan1,6,pos)
                    if count == 75:
                        s_ch0.play()
                        for i in range(0,360,6):
                            bullet(pos,look_at_player(pos)+i,6,11,7)
                    for i in range(0,360,45):
                        bullet(pos,i+count*3.2,5,9,6)
                if count == 60:
                    speed =0
                if count == 240:
                    s_enep2.play()
                    for i in range(0,360,20):
                        bullet(pos,look_at_player(pos)+i,6,19,7)
                    dir = 0
                    speed =2
            if num == 20:
                if pos[1] > HEIGHT-64 or pos[1] < 64:
                    speed = 3
                    if while_time(count,10):
                        for i in range(0,360,40):
                            bullet(pos,i+randint(0,9),randfloat(3,5),12,7,10)
                        for i in range(0,360,40):
                            bullet(pos,i+randint(0,9),randfloat(3,4),9,6,10)
                else:
                    speed = 6
                    if while_time(count,50):
                        bullet_effect(s_tan1,0,pos)
                        bullet(pos,look_at_player(pos),5,8,0)
                        for i in range(5,15,5):                    
                            bullet(pos,look_at_player(pos)+i,5-i/10,8,0)
                            bullet(pos,look_at_player(pos)-i,5-i/10,8,0)
                        bullet(pos,look_at_player(pos),4,17,7)
                        for i in range(5,15,5):                    
                            bullet(pos,look_at_player(pos)+i,4-i/10,17,7)
                            bullet(pos,look_at_player(pos)-i,4-i/10,17,7)
        if stage_fun == 5:
            if num == 21:
                if distance(pos,player.pos) <= 300 and while_time(count,30):
                    bullet_effect(s_tan1,0,pos)
                    bullet(pos,look_at_player(pos),3,3,0)                 
            if num == 22:
                if while_time(count,5) and count > 60 and count < 240:
                    bullet_effect(s_tan1,2,pos)
                    bullet(pos, list[0],7,15,2,12)
                    bullet(pos, list[0],7,15,2,12.1)
                if while_time(count,30):
                    list[0] = look_at_player(pos)
                if count == 60:
                    speed = 0
                if count == 180:
                    speed = -1        
            if num == 23:
                if when_time(count,90) or when_time(count,120):
                    add_effect(pos,8)
                    bullet_effect(s_tan1,1,pos)
                    for i in range(0,360,20):
                        bullet(pos,look_at_player(pos)+i,4,12,1)
                if while_time(count,2) and count > 150 and count < 330:
                    if count > 270:
                        rand = (randint(-100,100),randint(-100,100))
                        bullet_effect(s_tan1,1,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos),8,3,1)
                    elif count > 210:
                        rand = (randint(-100,100),randint(-100,100))
                        bullet_effect(s_tan1,1,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos),9,15,1)
                    elif count > 150:
                        rand = (randint(-100,100),randint(-100,100))
                        bullet_effect(s_tan1,1,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos),10,19,0)
                if when_time(count,60):
                    speed = 0
                if when_time(count,330):
                    speed = -1                   
            if num == 24:
                if count == 40:
                    bullet_effect(s_tan1,7,pos)
                    bullet(pos,look_at_player(pos),6,19,7,13)
            if num == 25:
                if count == 0:
                    list[0] = player.pos
                    dir = -look_at_player(pos)
                if distance(pos,list[0]) <= 30 and list[1]==0:
                    bullet_effect(s_enep2,1,list[0])
                    for i in range(0,360,10):
                        bullet(list[0],i,7,18,1)
                    for i in range(0,360,15):
                        bullet(list[0],i,4,9,6)
                    for i in range(0,360,15):
                        bullet(list[0],i+7.5,3,9,6)
                    for i in range(0,360,30):
                        bullet(list[0],i,2,15,0)
                    dir = 0
                    speed = 0
                    list[1] =1
                if list[1]:
                    speed += 0.2
            if num == 26:
                if when_time(count,80):
                    bullet_effect(s_tan1,7,pos)
                    for i in range(2,6):
                        bullet(pos,look_at_player(pos)+3,i,5,7)   
                        bullet(pos,look_at_player(pos)-3,i,5,7)   
        if stage_fun == 6:
            if num == 27:
                if when_time(count,60):
                    bullet_effect(s_tan1,0,pos)
                    for i in range(10,30):
                        bullet(pos,look_at_player(pos),i/2,1,0)          
            if num == 28:
                if while_time(count,5):
                    bullet_effect(s_tan1,1,pos)
                    rand = randint(0,45)
                    for i in range(0,360,45):
                        bullet(pos,i+rand,4,3,1)  
                if when_time(count,90):
                    speed = -0.5   
            if num == 29:
                if while_time(count,180):
                    bullet_effect(s_tan1,1,pos)
                    rand = randint(0,3)
                    for i in range(0,360,3):
                        bullet(pos,i+rand,2,11,1)  
                if when_time(count,90):
                    speed = -0.5  
                    dir += randint(-25,25)   
            if num == 30:
                if while_time(count,40):
                    bullet_effect(s_tan1,5,pos)
                    for i in range(0,2):
                        bullet(pos,look_at_player(pos)+20*i,4,18,5)  
                        bullet(pos,look_at_player(pos)-20*i,4,18,5) 
                if while_time(count+20,40):
                    bullet_effect(s_tan1,2,pos)
                    for i in range(0,3):
                        bullet(pos,look_at_player(pos)+10+20*i,4,18,5)  
                        bullet(pos,look_at_player(pos)-10-20*i,4,18,5)      
        return pos,dir,speed,count,list

    def boss_spawn(num): # 보스 시작, 배경
        global boss_background
        
        # 적이동을 위한 값
        boss.image.fill((0,0,0,0))
        boss.move_dir = 0
        boss.move_speed = 0
        boss.move_point = (0,0)
        boss.ready = False
        boss.move_ready = False # 스펠 시작시 움직이는중?
        boss.godmod = False
        boss.dieleft = False
        boss.attack_start = False
        boss.real_appear = False
        boss.died_next_stage = False
        boss.image_num = 0
        if num == 1: 
            boss.pos = (WIDTH+64,HEIGHT)
            boss.radius = 40
            boss.image.blit(pokemons[1],(0,0))         
            boss.num = 1
            boss.spell = [spells[0]]
            boss.dies = False
            boss.attack_start = True           
        if num == 2: 
            boss.pos = (WIDTH+64,HEIGHT+64)
            boss.radius = 40
            boss.image.blit(pokemons[1],(0,0))         
            boss.num = 2
            boss.spell = [spells[0],spells[1],spells[2],spells[3],spells[4]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(0,0,1080,720))
            text.started = True
        if num == 3: 
            boss.pos = (WIDTH+64,120)
            boss.radius = 40
            boss.image.blit(pokemons[2],(0,0))         
            boss.num = 3
            boss.spell = [spells[5],spells[6]]
            boss.dies = False
            boss.attack_start = True
            boss_background.blit(bg2_image,(0,0),(0,720,1080,720))
        if num == 4: 
            boss.pos = (WIDTH+64,HEIGHT+64)
            boss.radius = 40
            boss.image.blit(pokemons[3],(0,0))         
            boss.num = 4
            boss.spell = [spells[7],spells[8],spells[9],spells[10],spells[11]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(0,0,1080,720))
            boss_background.blit(bg2_image,(0,0),(0,720,1080,720))
            text.started = True
        if num == 5: 
            boss.pos = (WIDTH+64,640)
            boss.radius = 70
            boss.image.blit(pokemons[8],(0,0))         
            boss.num = 5
            boss.spell = [spells[12],spells[13]]
            boss.dies = True
            boss.attack_start = True
            boss_background.blit(bg2_image,(0,0),(0,720,1080,720))
        if num == 6: 
            boss.pos = (WIDTH+64,HEIGHT+64)
            boss.radius = 40
            boss.image.blit(pokemons[7],(0,0))         
            boss.num = num
            boss.spell = [spells[14],spells[15],spells[16],spells[17],spells[18],spells[19],spells[20]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(0,0,1080,720))
            boss_background.blit(bg2_image,(0,0),(0,720,1080,720))
            text.started = True        
        if num == 7: 
            boss.pos = (WIDTH+64,0)
            boss.radius = 70
            boss.image.blit(pokemons[4],(0,0))         
            boss.num = 5
            boss.spell = [spells[21],spells[22]]
            boss.dies = False
            boss.attack_start = True     
        if num == 8: 
            boss.pos = (WIDTH+64,HEIGHT+64)
            boss.radius = 40
            boss.image.blit(pokemons[5],(0,0))         
            boss.num = num
            boss.spell = [spells[23],spells[24],spells[25],spells[26],spells[27],spells[28],spells[29]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(0,0,1080,720))
            boss_background.blit(bg2_image,(0,0),(0,720,1080,720))
            text.started = True        
        if num == 9: 
            boss.pos = (WIDTH+64,0)
            boss.radius = 70
            boss.image.blit(pokemons[6],(0,0))         
            boss.num = 9
            boss.spell = [spells[30],spells[31]]
            boss.dies = False
            boss.attack_start = True  
        if num == 10: 
            boss.pos = (WIDTH+64,HEIGHT+64)
            boss.radius = 40
            boss.image.blit(pokemons[6],(0,0))         
            boss.num = num
            boss.spell = [spells[35],spells[33],spells[34],spells[35],spells[36],spells[37],spells[38]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(0,0,540,360))
            boss_background.blit(bg2_image,(0,0),(0,360,540,360))
            text.started = True         
        if num == 11: 
            boss.pos = (WIDTH+64,HEIGHT+64)
            boss.radius = 60
            boss.image.blit(pokemons[9],(0,0))         
            boss.num = num
            boss.spell = [spells[39],spells[33],spells[34],spells[35],spells[36],spells[37],spells[38]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(0,0,540,360))
            boss_background.blit(bg2_image,(0,0),(0,360,540,360))
            text.started = True          
        boss.real_max_health = 0
        for i in boss.spell:
            boss.real_max_health += i.health
        boss.real_health = boss.real_max_health
        boss.image2 = boss.image.copy()
        boss.appear = True
        boss.rect = boss.image.get_rect(center = (boss.pos))

    def boss_attack(num,count,pos,ready):
        if True: # 123 스테
            if num == 1:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2),120,3)
                if ready:
                    if while_time(count,20) and count < 120:
                        add_effect(pos,2,5)
                        s_tan1.play()
                        for i in range(0,360,30):
                            bullet(pos,look_at_player(pos)+i,5,4,5)
                            bullet(pos,look_at_player(pos)+i+5,5,4,5)
                            bullet(pos,look_at_player(pos)+i-5,5,4,5)
                    if when_time(count,60):
                        set_go_boss(2,90,50)
                    if when_time(count,180):
                        set_go_boss(2,-90,50)
                        count = 0
            if num == 2:
                pos = set_bossmove_point((WIDTH-150,HEIGHT/2),120,3)
                if ready:
                    if while_time(count,30):
                        rand = randint(0,15)
                        add_effect(pos,2,2)
                        s_tan1.play()
                        for i in range(0,360,15):
                            bullet(pos,i+rand,4,3,2)
                    if while_time(count+1,180):
                        add_effect(pos,2,5)
                        s_tan1.play()
                        for i in range(1,20):
                            bullet(pos,look_at_player(pos),i/2,5,5)             
            if num == 3:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,20) and count < 120:
                        add_effect(pos,2,5)
                        s_tan1.play()
                        for i in range(0,360,30):
                            bullet(pos,look_at_player(pos)+i,5,4,5)
                            bullet(pos,look_at_player(pos)+i+5,5,4,5)
                            bullet(pos,look_at_player(pos)+i-5,5,4,5)
                            bullet(pos,look_at_player(pos)+i,3,1,5)
                            bullet(pos,look_at_player(pos)+i+5,3,1,5)
                            bullet(pos,look_at_player(pos)+i-5,3,1,5)
                    if when_time(count,60):
                        set_go_boss(2,90,50)
                    if when_time(count,180):
                        set_go_boss(2,-90,50)
                        count = 0
            if num == 4:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,15):
                        rand = randint(0,15)
                        add_effect(pos,2,0)
                        s_tan1.play()
                        for i in range(0,360,15):
                            bullet((pos[0]+randint(-60,60),pos[1]+randint(-60,60)),i+rand,5,randint(2,3),randint(1,7))
                    if while_time(count,180):
                        set_go_boss(2,randint(0,360),30)
            if num == 5:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,4):
                        s_tan2.play()
                        bullet(pos,count*2,4,4,5)
                        bullet(pos,count*2+180,4,4,5)
                    if while_time(count,60) and count > 180:
                        dir = look_at_player(pos)
                        s_tan1.play()
                        add_effect(pos,2,5)
                        bullet(pos,dir,2,15,5)
                        bullet((pos[0]+30,pos[1]),dir,2,15,5)
                        bullet((pos[0]-30,pos[1]),dir,2,15,5)
                        bullet((pos[0],pos[1]+30),dir,2,15,5)
                        bullet((pos[0],pos[1]-30),dir,2,15,5)
            if num == 6:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,8) and count < 90:
                        bullet_effect(s_tan1,4,pos)
                        for i in range(0,360,30):
                            bullet(pos,i+count*6.2,5,3,4)
                    if while_time(count,8) and big_small(count,90,180):
                        bullet_effect(s_tan1,3,pos)
                        for i in range(0,360,30):
                            bullet(pos,i-count*6.2,5,3,3)
                    if when_time(count,300):
                        count = 0
            if num == 7:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,8) and count<40:
                        bullet_effect(s_tan1,4,pos)
                        bullet(pos,count*4,2,15,3,1.1)  
                    if when_time(count,120):
                        count = 0
            if num == 8:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,4) and count < 90:
                        bullet_effect(s_tan1,4,pos)
                        for i in range(0,360,30):
                            bullet(pos,i+count*3.1,5,3,4)
                    if while_time(count,4) and big_small(count,90,180):
                        bullet_effect(s_tan1,3,pos)
                        for i in range(0,360,30):
                            bullet(pos,i-count*3.1,5,3,3)
                    if when_time(count,300):
                        count = 0
                    if when_time(count,90):
                        set_go_boss(5,90,60)                    
            if num == 9:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if when_time(count,60):
                        bullet_effect(s_tan1,4,pos)
                        rand = randint(0,30)
                        for i in range(0,360,30):
                            bullet(pos,i+rand,2,15,3,1.2)  
                    if when_time(count,180):
                        s_kira0.play()
                        set_go_boss(2,randint(0,360),60)
                    if when_time(count,300):
                        count = 0
            if num == 10:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,20):
                        rand = randint(0,10)
                        bullet_effect(s_tan1,4,pos)
                        for i in range(0,360,20):
                            bullet(pos,i+rand,5,4,4)
                    if while_time(count,50):
                        set_go_boss(1,randint(0,360),50) 
            if num == 11:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if when_time(count,120):
                        bullet_effect(s_tan1,3,pos)
                        for i in range(0,720,8):
                            bullet((WIDTH-randint(8,300),i),180,5,2,3,2)
                    if when_time(count,240): 
                        s_kira0.play()
                        count = 0
                    if when_time(count,240):
                        set_go_boss(2,choice([-30,30,-150,150]),50)   
            if num == 12:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,5) and count<180:
                        bullet_effect(s_tan1,3,pos)
                        bullet(pos,180+randint(-20,20),7,19,3,2.1)
                    if while_time(count,360):
                        set_go_boss(3,look_at_player(pos)+180,60)   
                        count = 0                           
            if num == 13:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,30):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,3):
                            bullet(pos,i+randint(-3,3),3,3,5)
            if num == 14:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,5):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,4):
                            bullet(pos,count+90*i,6,9,5)
                            bullet(pos,count-7+90*i,6,9,5)
                            bullet(pos,count-14+90*i,6,9,5)
                            bullet(pos,count+7+90*i,6,9,5)
                            bullet(pos,count+14+90*i,6,9,5)
                    if while_time(count,180):
                        set_go_boss(3,look_at_player(pos),60)  
            if num == 15:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,8) and count < 60:
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,10):
                            bullet(pos,i,6,9,5)
                    if while_time(count+4,8) and count < 60:
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,10):
                            bullet(pos,i+5,6,9,5)
                    if while_time(count,60):
                        set_go_boss(3,choice([90,270]),30)
                    if when_time(count,150):
                        count = 0                        
            if num == 16:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,2) and count < 180:
                        bullet_effect(s_tan1,1,pos)
                        for i in range(0,360,90):
                            bullet(pos,count**1.4+i,4,2,1,6)  
                    if while_time(count,10) and count > 180:
                        bullet_effect(s_tan2,0,pos)
                        bullet(pos,look_at_player(pos),7,18,5)
                        bullet(pos,look_at_player(pos),5,18,5)
                        bullet(pos,look_at_player(pos),3,18,5)

                    if when_time(count,300):
                        count = 0   
            if num == 17:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,30):
                        rand = ((randint(boss_movebox.x,boss_movebox.x+boss_movebox.width),randint(boss_movebox.y,boss_movebox.y+boss_movebox.height)),randint(4,5))
                        set_go_boss(4,-look_at_point(pos,rand[0]),29)
                        bullet_effect(s_tan1,rand[1],rand[0])
                        for i in range(0,360,5):
                            bullet(rand[0],count+i,6,10,rand[1])        
            if num == 18:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if when_time(count,60):
                        magic_bullet((1080,pos[1]),180,10,1)
                        magic_bullet((1090,pos[1]+100),180,10,1)
                        magic_bullet((1100,pos[1]-100),180,10,1)
                        magic_bullet((1110,pos[1]+200),180,10,1)
                        magic_bullet((1120,pos[1]-200),180,10,1)
                    if count == 180:
                        s_ch0.play()
                    if count == 240:
                        s_kira0.play()
                        add_effect(pos,5)
                        count = 0
                    if while_time(count,60):
                        set_go_boss(3,-look_at_player(pos),30)
            if num == 19:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count+8,16):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,20):
                            bullet(calculate_new_xy(pos,50,-(count*2.2+i)),count*2.2+i,5,3,5,8)            
                    if while_time(count,16):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,20):
                            bullet(calculate_new_xy(pos,50,-(count*2.2+i)),count*2.2+i,5,3,2,8.1)   
            if num == 20:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:   
                    if while_time(count,60):
                        bullet_effect(s_tan1,0,pos)
                        rand = randint(0,359)
                        magic_bullet(pos,rand,3,2)  
                        magic_bullet(pos,rand+180,3,2)                        
            if num == 21:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if when_time(count,60):
                        s_tan1.play()
                        magic_bullet(get_new_pos(player.pos,100),0,0,3,1) 
                        magic_bullet(get_new_pos(player.pos,100),0,0,4,1)
        if True:
            if num == 22:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,6):
                        sub = count * 2.2
                        for i in range(1,5):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub,True))
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub-90,5,1,4)
                    if while_time(count,120):
                        set_go_boss(5,randint(0,360),30)
            if num == 23:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,6):
                        sub = count * 2.2
                        for i in range(1,5):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub,True))
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub-90,5,1,4)
                            bullet_effect(s_tan1,1,calculate_new_xy(pos,-70*i,sub,True))
                            bullet(calculate_new_xy(pos,-70*i,sub,True),-sub+45,5,1,1)
                            bullet(calculate_new_xy(pos,-70*i,sub,True),-sub+135,5,1,1)
                    if while_time(count,120):
                        set_go_boss(5,randint(0,360),30)
            if num == 24:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,3) and count< 120:
                        sub = -(count * 3.2 + 45 )
                        for i in range(1,6):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub))
                            bullet(calculate_new_xy(pos,60*i,sub),-sub-90,5,1,4,0.1)
                    if while_time(count,3) and count> 120:
                        sub = count * 3.2 + 45
                        for i in range(1,6):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub))
                            bullet(calculate_new_xy(pos,60*i,sub),-sub-90,5,1,4,0.1)
                    if count == 240:
                        count = 0
                    if while_time(count,120):
                        set_go_boss(5,-look_at_player(pos),30)     
            if num == 25:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,3) and count< 90:
                        sub = -(count * 3.2 + 45 )
                        for i in range(2,6):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub,True))
                            bullet(calculate_new_xy(pos,60*i,sub,True),look_at_player(boss.pos),0,1,4,11.4)
                    if count == 90:
                        bullet_effect(s_kira0,0,0,True)
                    if while_time(count,120):
                        count = 0
                        set_go_boss(5,choice([-90,90]),30)          
            if num == 26:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,20):
                        bullet_effect(s_tan1,7,get_new_pos(pos,0,100))
                        bullet_effect(s_tan1,7,get_new_pos(pos,0,-100))
                        bullet(get_new_pos(pos,0,100),180,8,15,7)
                        bullet(get_new_pos(pos,-30,100),180,8,18,7)
                        bullet(get_new_pos(pos,-60,100),180,8,17,7)
                        bullet(get_new_pos(pos,-90,100),180,8,5,7)
                        bullet(get_new_pos(pos,0,-100),180,8,15,7)
                        bullet(get_new_pos(pos,-30,-100),180,8,18,7)
                        bullet(get_new_pos(pos,-60,-100),180,8,17,7)
                        bullet(get_new_pos(pos,-90,-100),180,8,5,7)
                    if while_time(count,10):
                        bullet_effect(s_tan1,0,pos)
                        bullet(pos,look_at_player(pos),5,17,0)
                    if while_time(count,60):
                        count = 0
                        set_go_boss(5,-look_at_point(pos,(780,player.pos[1]))+randint(-30,30),60)         
            if num == 27:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                boss.box_disable = True
                if ready:
                    if while_time(count,2) and boss.move_speed == 20:
                        rand = (randint(-100,100),randint(-100,100))
                        bullet_effect(s_tan1,7,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),-boss.move_dir,8,15,7)     
                    if while_time(count,3) and boss.list[0]:
                        sub = -(count * 4.2 + 45)
                        for i in range(2,4):
                            bullet_effect(s_tan1,7,calculate_new_xy(pos,60*i,sub,True))
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub-90,4,1,7)                       
                    if while_time(count,60):
                        set_go_boss(20,-look_at_point(pos,(0,player.pos[1])),999)                
                    if pos[0] < 64 and not boss.list[0]:
                        boss.move_speed = 5
                        boss.list[0] = True
                        s_enep2.play()
                        boss.health -= 80
                        for i in range(0,360,10):
                            bullet(get_new_pos(pos),i,4,9,7)   
                    if boss.list[0]:
                        boss.move_dir = 0
                        if pos[0] >= 880:
                            boss.move_speed = 0
                            boss.move_time = 0
                            boss.list[0] = False
            if num == 28:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:   
                    if while_time(count,20): 
                        bullet_effect(s_tan1,5,pos)
                        for j in range(0,360,90):
                            for i in range(0,10):                       
                                bullet(pos,look_at_player(pos)+i/2+j,10-i/2+1,4,5)
                                bullet(pos,look_at_player(pos)-i/2+j,10-i/2+1,4,5)
                    if while_time(count,30): 
                        bullet_effect(s_tan1,5,pos)
                        for j in range(0,360,90):
                            for i in range(0,10):                       
                                bullet(pos,look_at_player(pos)+i/2+j,10-i/2+1,6,6)
                                bullet(pos,look_at_player(pos)-i/2+j,10-i/2+1,6,6)
                    if while_time(count,60):
                        set_go_boss(3,-look_at_player(pos),30)
            if num == 29:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                boss.box_disable = True
                if ready:            
                    if while_time(count,100):
                        set_go_boss(10,-look_at_player(pos),50)  
                    if while_time(count,4) and not boss.move_time > 0 and count > 100:  
                        bullet_effect(s_tan1,5,pos)  
                        for i in range(0,360,45):                       
                            bullet(pos,count+i,3,7,5)  
                        if while_time(count,16):
                            for i in range(0,10):                       
                                bullet(pos,look_at_player(pos)+i/2,10-i+1,4,5,0.1)
                                bullet(pos,look_at_player(pos)-i/2,10-i+1,4,5,0.1) 
                    if boss.move_time > 0:
                        boss.health -= 3
            if num == 30:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:                
                    if while_time(count,3) and count < 60:
                        sub = -(count * 5.2 +45)
                        for i in range(2,10):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub,True))
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub+90,5,1,4)
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub+135,5,1,4)
                    if while_time(count,2) and big_small(count,60,80):
                        rand = (randint(-100,100),randint(-100,100))
                        bullet_effect(s_tan1,4,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos)+randint(-5,5),7,17,7)
                        rand = (randint(-100,100),randint(-100,100))
                        bullet_effect(s_tan1,4,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos)+randint(-5,5),7,17,7)
                        rand = (randint(-100,100),randint(-100,100))
                        bullet_effect(s_tan1,4,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos)+randint(-5,5),7,17,7)
                    if while_time(count,4)and big_small(count,80,100): 
                        bullet_effect(s_tan1,5,pos)
                        for j in range(0,360,90):
                            for i in range(0,10):                       
                                bullet(pos,look_at_player(pos)+i/2+j,10-i/2+3,4,5)
                                bullet(pos,look_at_player(pos)-i/2+j,10-i/2+3,4,5)  
                    if count == 101:
                        count = 0  
            if num == 31:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready: 
                    if while_time(count,40):
                        boss.list[0] = look_at_player(pos)
                        count = 0
                    if while_time(count,2) and count < 30:
                        bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-boss.list[0],True))  
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]+20,6,1,1,14.6,[boss.list[0]])   
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]-20,6,1,1,14.6,[boss.list[0]])    
                    if while_time(count,40):
                        bullet_effect(s_tan2,6,pos)  
                        for i in range(0,360,10):
                            bullet(pos,i,4,2,6)    
            if num == 32:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready: 
                    if while_time(count,40):
                        boss.list[0] = look_at_player(pos)
                        count = 0
                    if while_time(count,5) and count < 30:
                        bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-boss.list[0],True))  
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]+60,12,1,1,14.6,[boss.list[0]])   
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]-60,12,1,1,14.6,[boss.list[0]]) 
                    if when_time(count,30):
                        bullet_effect(s_tan1,1,pos)  
                        bullet(pos,boss.list[0],8,15,1)  
            if num == 33:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready: 
                    if while_time(count,40):
                        boss.list[0] = look_at_player(pos)
                        count = 0
                    if while_time(count,2) and count < 30:
                        bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-boss.list[0],True))  
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]+20,6,1,1,14.6,[boss.list[0]])   
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]-20,6,1,1,14.6,[boss.list[0]])    
                    if while_time(count,20):
                        bullet_effect(s_tan2,2,pos)  
                        for i in range(0,360,10):
                            bullet(pos,i,4,11,2)             
            if num == 34:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready: 
                    if while_time(count,80):
                        boss.list[0] = look_at_player(pos)
                        count = 0
                    if while_time(count,6) and count < 60:
                        bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-boss.list[0],True))  
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]+20,8,1,1,15,[boss.list[0]])   
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]-20,8,1,1,15,[boss.list[0]])
                    if while_time(count,120): 
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0],3,3,7)    
                    if while_time(count,40):
                        for i in range(0,HEIGHT,20):
                            bullet((WIDTH,i+10),180,3,12,2) 
            if num == 35:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready: 
                    if while_time(count,30):
                        bullet_effect(s_tan1,4,calculate_new_xy(pos,100,-boss.list[0]+90,True))
                        bullet_effect(s_tan1,4,calculate_new_xy(pos,100,-boss.list[0]-90,True))
                        bullet_effect(s_tan1,4,calculate_new_xy(pos,100,-boss.list[0]+180,True))
                        bullet(calculate_new_xy(pos,100,-boss.list[0]+90,True),look_at_player(calculate_new_xy(pos,100,-boss.list[0]+90,True)),5,15,4)   
                        bullet(calculate_new_xy(pos,100,-boss.list[0]-90,True),look_at_player(calculate_new_xy(pos,100,-boss.list[0]-90,True)),5,15,4) 
                        bullet(calculate_new_xy(pos,100,-boss.list[0]+180,True),look_at_player(calculate_new_xy(pos,100,-boss.list[0]+180,True)),5,15,4) 
                        boss.list[0] = look_at_player(pos)
                        count = 0
                    if while_time(count,5):
                        bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-boss.list[0],True))  
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]+40,12,1,1,14.3,[boss.list[0]])   
                        bullet(calculate_new_xy(pos,100,-boss.list[0],True),boss.list[0]-40,12,1,1,14.3,[boss.list[0]]) 
                    if when_time(count,30):
                        bullet_effect(s_tan1,1,pos)  
                        bullet(pos,boss.list[0],8,15,1) 
                    if while_time(count,120):
                        set_go_boss(2,-look_at_player(pos),60)
            if num == 36:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if when_time(count,100):
                        magic_bullet(calculate_new_xy(pos,130,-look_at_player(pos)),look_at_player(pos),0,5)     
                        magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)+20),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)-20),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)+45),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)-45),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)+85),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)-85),look_at_player(pos),0,5) 
                    if when_time(count,130):
                        set_go_boss(6,-90,60)
                    if when_time(count,200):
                        magic_bullet(calculate_new_xy(pos,130,-look_at_player(pos)),look_at_player(pos),0,5)     
                        magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)+20),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)-20),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)+45),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)-45),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)+85),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)-85),look_at_player(pos),0,5) 
                    if when_time(count,230):
                        set_go_boss(12,90,60)
                    if when_time(count,300):
                        magic_bullet(calculate_new_xy(pos,130,-look_at_player(pos)),look_at_player(pos),0,5)     
                        magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)+20),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)-20),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)+45),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)-45),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)+85),look_at_player(pos),0,5) 
                        magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)-85),look_at_player(pos),0,5) 
                    if when_time(count,330):
                        set_go_boss(6,-90,60)
                    if when_time(count,390):
                        add_effect(pos,8)
                    if when_time(count,450):
                        for i in range(0,360,45):
                            magic_bullet(calculate_new_xy(pos,130,-look_at_player(pos)-i),-i,0,5)     
                            magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)+20+i),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)-20+i),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)+45+i),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)-45+i),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)+85+i),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)-85+i),-i,0,5)                         
                    if when_time(count,600):
                        count = 0
            if num == 37:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:            
                    if while_time(count,120):
                        boss.list[0] = look_at_player(pos)
                        count = 0
                    if while_time(count,3) and count < 30:
                        for i in range(0,360,30):
                            bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-boss.list[0]+i,True))  
                            bullet(calculate_new_xy(pos,100,-boss.list[0]+i,True),boss.list[0]+40+i,12,1,1,14.2,[boss.list[0]+i])   
                            bullet(calculate_new_xy(pos,100,-boss.list[0]+i,True),boss.list[0]-40+i,12,1,1,14.2,[boss.list[0]+i])
                    if while_time(count,60):
                        set_go_boss(3,choice([70,110,-70,-110]),10)    
            if num == 38:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:  
                    if while_time(count,10):
                        magic_bullet((WIDTH,randint(30,690)),randint(-45,45),5,randint(6,7))
                    if while_time(count,60):
                        set_go_boss(3,randint(0,359),40) 
            if num == 39:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:  
                    if when_time(count,60):
                        bullet_effect(s_lazer1,6,pos)
                        boss.list[0] = look_at_player(pos)
                    if while_time(count,2) and big_small(count,60,180):
                        bullet_effect(0,6,pos)
                        bullet(pos,boss.list[0]+45,12,0,6,18)
                        bullet(pos,boss.list[0]-45,12,0,6,18)
                    if when_time(count,300):
                        count = 0
                        set_go_boss(1,randint(0,359),120) 
        if num == 40:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready:                                       

        if ready:pos = go_boss()
        else:pos = calculate_new_xy(pos,boss.move_speed,boss.move_dir)
        return count,pos,ready
    # 스테이지
    def bullet_type(self,mod,sub):
        if mod == 0 and sub == 1:
            self.screen_die = True
        if mod == 1:
            if sub == 1:
                self.count += 1
                if when_time(self.count,120):
                    for i in range(0,360,20):
                        bullet(self.pos,i+randint(-5,5),3,2,0)
                    self.kill()
            if sub == 2:
                self.count += 1
                if when_time(self.count,120):
                    for i in range(0,360,20):
                        bullet(self.pos,i+randint(-5,5),3,2,0)
                        bullet(self.pos,i+randint(-7,7),2,2,0)
                    self.kill()                        
        if mod == 2:
            if sub == 0:
                self.count += 1
                if self.count > 120:
                    bullet(self.pos,randint(-88,88)+180,2,12,3)
                    bullet(self.pos,randint(-88,88)+180,2,12,3)
                    self.kill()
                elif self.count > 80 and self.speed != 0:
                    self.speed -= 0.2
            if sub == 1:
                if self.pos[0] < -30:
                    self.pos = get_new_pos(self.pos,1143,0)
                    bullet(self.pos,randint(-88,88)+180,5,18,4)
                    bullet(self.pos,randint(-88,88)+180,5,18,4)  
                    for i in range(4,6):
                        for j in range(1,11,5):
                            bullet(self.pos,180,i+j/10,4,4) 
                    for _ in range(0,5):
                        for c in range(4,6):
                            bullet((self.pos[0]+randint(-30,30),self.pos[1]),180,c,4,4) 
                    s_tan2.play()
                    self.kill()
        if mod == 3:
            if sub == 0:
                self.count += 1
                if while_time(self.count,30) and self.count < 91:
                    bullet_effect(s_tan2,6,self.pos)
                    rand = randint(0,59)
                    for i in range(0,360,45):
                        bullet(self.pos,i+rand,1,10,7,3.1)
                        
            if sub == 1:
                self.count += 1
                if self.count == 60:
                    bullet_effect(s_kira0,0,0,True)
                if self.count > 120 and self.speed < 6:
                    self.speed += 0.1
        if mod == 4:
            self.count += 1
            if sub == 0:
                if while_time(self.count,2):
                    bullet(self.pos,self.direction+randint(-10,10),0,11,7,4.1)
            if sub == 1:
                if self.count > 120 and self.speed < 5:
                    self.speed += 0.05
        if mod == 5:
            self.count += 1
            if self.count < 30 and self.speed > 0:
                self.speed -= 0.2
            if self.count == 120:
                bullet_effect(s_kira0,0,0,True)
                bullet(self.pos,180,7,4,5)
                self.kill()  
        if mod == 6:
            self.count += 1
            if self.count == 60:
                bullet_effect(s_kira0,3,self.pos)
                bullet(self.pos,self.direction,6,2,3)
        if mod == 7:
            if boss.count == 240:
                self.speed = 2
        if mod == 8: # 2초 동안 각도 바꾸기
            self.count += 1
            if while_time(self.count,2) and self.count < 120:
                if sub == 0:
                    self.direction += 2
                else:
                    self.direction -= 2
        if mod == 9:  # 60초후 넘 값의 방향으로 속도3
            self.count += 1
            self.screen_die = True
            if self.count == 60:
                self.speed = 3 if sub==0 else sub
                if sub == 0:self.direction = self.num[0]
        if mod == 10:# 점점 아래로 떨어짐
            if self.count < 40: self.count += 1
            self.pos = get_new_pos(self.pos,0,self.count/8)
        if mod == 11:
            self.screen_die = True
            if boss.count == 90:
                self.speed = sub
        if mod == 12:
            self.count += 5
            if sub == 0:
                self.direction += math.cos(math.pi * (self.count / 180))*2.2
            if sub == 1:
                self.direction += math.cos(math.pi * (self.count / 180))*-2.2
        if mod == 13:
            self.count += 1
            if self.count == 60:
                bullet_effect(s_kira0,0,0,True)
                if sub == 0:
                    for i in range(0,360,30):
                        bullet(self.pos,self.direction+i,self.speed/2,14,7,13.1)
                if sub == 1:
                    for i in range(0,360,90):
                        bullet(self.pos,self.direction+i+45,self.speed/2,18,7,13.2)
                if sub == 2:
                    for i in range(0,360,90):
                        bullet(self.pos,self.direction+i,self.speed/2,11,7)
                self.kill()
        if mod == 14:
            if boss.count == 30:
                self.direction = self.num[0]
                self.speed = sub
        if mod == 15:
            if boss.count == 60:
                self.direction = self.num[0]
                self.speed = 4
        if mod == 16:
            if self.count == 0:
                self.count += self.num
            
            if self.count >= 180 and self.speed < 6:
                self.speed += 0.1
                if self.count == 180:
                    bullet_effect(s_kira0,0,0,True)
                    self.change_shape(2,1)
            self.count += 1
        if mod == 17:
            if self.speed <= 10:
                self.speed += 0.2            
        if mod == 18:
            if sub == 0:
                if not small_border.collidepoint(self.pos):
                    bullet_effect(s_tan1,1,get_new_pos(self.pos,randint(-50,50),randint(-50,50)))
                    rand = randint(0,90)
                    for i in range(0,360,90):
                        bullet(self.pos,i+rand,12,8,7,18.1)
                    rand = randint(0,90)
                    for i in range(0,360,90):
                        bullet(self.pos,i+rand,8,3,7,18.1)
                    self.kill()


            if sub == 1:
                self.count += 1
                if self.count == 10: self.speed /= 4
   
    def magic_type(self,mod):
        if mod == 1:
            self.count += 1
            if while_time(self.count+2,4) and self.count < 180:
                bullet_effect(s_tan1,0,self.pos)
                bullet(self.pos,90,0,1,0,7) 
            if while_time(self.count,4) and self.count < 180:
                bullet_effect(s_tan1,0,self.pos)
                bullet(self.pos,270,0,1,0,7)  
        if mod == 2:
            self.count += 1
            if when_time(self.count,60):
                self.speed = 0
                bullet(self.pos,0,0,19,0,9,(look_at_player(self.pos),0))
                for i in range(0,360,15):
                    bullet(self.pos,i,3,1,0,9,(look_at_player(self.pos),0)) 
                    self.direction = look_at_player(self.pos)
            if when_time(self.count,120):
                bullet_effect(s_kira0,0,0,True)
                self.speed = 3
        if mod == 3:
            self.count += 1
            self.pos = move_circle(player.pos,self.count*3,300)
            if while_time(self.count,6):
                bullet_effect(s_tan1,4,self.pos)
                bullet(self.pos,look_at_player(self.pos),2,10,4,0.1)
                bullet(self.pos,look_at_player(self.pos)+90,5,16,4)
                bullet(self.pos,look_at_player(self.pos)+85,4,16,5)
                bullet(self.pos,look_at_player(self.pos)+95,6,16,5)
        if mod == 4:
            self.count += 1
            self.pos = move_circle(player.pos,self.count*3+180,300)
            if while_time(self.count,6):
                bullet_effect(s_tan1,5,self.pos)
                bullet(self.pos,look_at_player(self.pos),2,10,5,0.1)
                bullet(self.pos,look_at_player(self.pos)+90,5,16,5)
                bullet(self.pos,look_at_player(self.pos)+85,4,16,4)
                bullet(self.pos,look_at_player(self.pos)+95,6,16,4)
        if mod == 5:
            if self.count == 0:
                bullet_effect(s_tan1,1,self.pos)
                bullet(self.pos,self.direction,0,15,1,17)
            self.count += 1
            if while_time(self.count,5) and self.count <= 180:
                bullet(self.pos,self.direction+randint(-20,20),0,1,1,16,self.count)
            if self.speed <= 10:
                self.speed += 0.2
        if mod == 6:
            if self.pos[0] >= WIDTH:
                if self.count == 0:
                    bullet_effect(s_tan1,1,self.pos)
                self.speed = 0                
                if while_time(self.count,8):
                    bullet(get_new_pos(self.pos,0,self.count*1.8),180,5,4,1)
                    bullet(get_new_pos(self.pos,0,-self.count*1.8),180,5,4,1)
                self.count += 1
                if self.count == 40:
                    self.kill()
        if mod == 7:
            if self.pos[0] >= WIDTH:
                if self.count == 0:
                    bullet_effect(s_tan1,6,self.pos)
                self.speed = 0                
                if while_time(self.count,7):
                    bullet(get_new_pos(self.pos,0,self.count*1.8),180,6,7,6)
                    bullet(get_new_pos(self.pos,0,-self.count*1.8),180,6,7,6)
                self.count += 1
                if self.count == 40:
                    self.kill()
    
    
    player.power = 400
    stage_challenge = 2
    stage_fun =5
    def stage_manager():
        global stage_cline, stage_line, stage_repeat_count, stage_count, stage_condition, stage_challenge,stage_fun
        
        if True:
            if stage_condition == 1:
                add_effect((WIDTH/2,HEIGHT/2),99)
                stage_fun += 1
                stage_count = 0
                stage_condition += 1
            if stage_condition == 2:
                stage_count += 1
                if stage_count >= 60:
                    stage_condition += 1
            if stage_condition == 3:
                game_defalt_setting(stage_fun)
                player.pos = (WIDTH/4,HEIGHT/2)
                stage_condition += 1
            if stage_condition == 4:
                stage_count += 1
                if stage_count >= 180:
                    stage_condition += 1
            if stage_condition == 5:
                pygame.mixer.music.play(-1)
                stage_condition += 1
                stage_count = 0
        if stage_condition == 6:
            if stage_fun == 1:
                if stage_challenge == 0:
                    pokemon_spawn(1,(506,-30),120)
                    pokemon_spawn(1,(456,-30),0)

                    if while_poke_spawn(30,10,2):
                        pokemon_spawn(1,(506,-30),30)
                        pokemon_spawn(1,(456,-30),0)
                        end_while_poke_spawn(2,10)

                    pokemon_spawn(2,(506,HEIGHT+30),0)
                    pokemon_spawn(2,(456,HEIGHT+30),0)

                    if while_poke_spawn(30,10,2):
                        pokemon_spawn(2,(506,HEIGHT+30),30)
                        pokemon_spawn(2,(456,HEIGHT+30),0)
                        end_while_poke_spawn(2,10)

                    pokemon_spawn(1,(506,-30),0)
                    pokemon_spawn(1,(456,-30),0)
                    pokemon_spawn(2,(506,HEIGHT+30),0)
                    pokemon_spawn(2,(456,HEIGHT+30),0)

                    if while_poke_spawn(30,10,4):
                        pokemon_spawn(1,(506,-30),30)
                        pokemon_spawn(1,(456,-30),0)
                        pokemon_spawn(2,(506,HEIGHT+30),0)
                        pokemon_spawn(2,(456,HEIGHT+30),0) 
                        end_while_poke_spawn(4,10)    

                    pokemon_spawn(1,(556,-30),60)
                    pokemon_spawn(2,(556,HEIGHT+30),10)
                    pokemon_spawn(1,(556,-30),10)
                    pokemon_spawn(2,(556,HEIGHT+30),10)
                    title_spawn(1,240)

                    next_challenge(260)
                if stage_challenge == 1:
                    bground_spawn(1,1)
                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(stage_repeat_count,3):
                            enemy_group.add(Enemy(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,180,4,10,13,30,4))
                        end_while_poke_spawn(2,10)

                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(stage_repeat_count,3):
                            enemy_group.add(Enemy(WIDTH+64,stage_repeat_count*HEIGHT/10+20,180,4,10,13,30,4))
                        end_while_poke_spawn(2,10)

                    if while_poke_spawn(10,15,2):
                        pokemon_spawn(5,(WIDTH,20),10)
                        pokemon_spawn(6,(WIDTH,HEIGHT-20),0)
                        end_while_poke_spawn(2,15)

                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(stage_repeat_count,2):
                            enemy_group.add(Enemy(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,180,4,10,13,30,4))
                            enemy_group.add(Enemy(WIDTH+64,stage_repeat_count*HEIGHT/10+20,180,4,10,13,30,4))
                        end_while_poke_spawn(2,10)
                    
                    next_challenge(240)
                if stage_challenge == 2:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(1)
                    if boss.died_next_stage:
                        stage_count = 0
                        boss.died_next_stage = False
                        next_challenge(0)
                if stage_challenge == 3:
                    bground_spawn(2,1)
                    if while_poke_spawn(10,5,2):
                        pokemon_spawn(5,(WIDTH,20),10)
                        pokemon_spawn(6,(WIDTH,HEIGHT-20),0)
                        end_while_poke_spawn(2,5)

                    pokemon_spawn(4,(WIDTH,HEIGHT/2),60)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2+20),60)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2+60),60)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2-20),60)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2-60),60)

                    if while_poke_spawn(20,10,4):
                        pokemon_spawn(1,(1012,-30),20)
                        pokemon_spawn(1,(912,-30),0)
                        pokemon_spawn(2,(1012,HEIGHT+30),0)
                        pokemon_spawn(2,(912,HEIGHT+30),0) 
                        end_while_poke_spawn(4,10)

                    if while_poke_spawn(10,5,2):
                        pokemon_spawn(5,(WIDTH,20),10)
                        pokemon_spawn(6,(WIDTH,HEIGHT-20),0)
                        end_while_poke_spawn(2,5)

                    pokemon_spawn(4,(WIDTH,HEIGHT/2),30)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2+40),30)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2-40),0)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2+80),30)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2),0)
                    pokemon_spawn(4,(WIDTH,HEIGHT/2-80),0)
                    next_challenge(360)
                if stage_challenge == 4:
                    bground_spawn(3,1)
                    pokemon_spawn(7,(WIDTH-120,-30),60,90)
                    pokemon_spawn(7,(WIDTH-120,-30),60,90)
                    pokemon_spawn(7,(WIDTH-120,-30),60,90)
                    pokemon_spawn(7,(WIDTH-120,-30),120,90)
                    pokemon_spawn(7,(WIDTH-120,HEIGHT+30),60,-90)
                    pokemon_spawn(7,(WIDTH-120,-30),60,90)
                    pokemon_spawn(7,(WIDTH-120,HEIGHT+30),60,-90)
                    pokemon_spawn(7,(WIDTH-120,-30),60,90)
                    pokemon_spawn(7,(WIDTH-120,HEIGHT+30),60,-90)

                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(stage_repeat_count,3):
                            enemy_group.add(Enemy(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,180,4,10,13,30,4))
                        if while_time(stage_repeat_count,2):
                            enemy_group.add(Enemy(WIDTH-120,HEIGHT+30,-90,4,7,15,30,7))
                        end_while_poke_spawn(2,10)
                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(stage_repeat_count,3):
                            enemy_group.add(Enemy(WIDTH+64,stage_repeat_count*HEIGHT/10+20,180,4,10,13,30,4))
                        if while_time(stage_repeat_count,2):
                            enemy_group.add(Enemy(WIDTH-120,-30,90,4,7,15,30,7))
                        end_while_poke_spawn(2,10)
                    next_challenge(360)
                if stage_challenge == 5:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(2)
                    if boss.died_next_stage:
                        stage_count = 0
                        if not text.started:
                            stage_challenge = 0
                            stage_line = 0
                            text.re_start()
                            stage_condition = 1
            if stage_fun == 2:
                if stage_challenge == 0:
                    pokemon_spawn(8,(WIDTH,HEIGHT),120,-135,4)
                    pokemon_spawn(8,(WIDTH,0),0,135,4)
                    if while_poke_spawn(10,10,2):
                        pokemon_spawn(8,(WIDTH,HEIGHT),10,-135,4)
                        pokemon_spawn(8,(WIDTH,0),0,135,4)
                        end_while_poke_spawn(2,10)
                    
                    pokemon_spawn(8,(WIDTH,HEIGHT),120,-110,6)
                    pokemon_spawn(8,(WIDTH,0),0,110,6)
                    if while_poke_spawn(10,10,2):
                        pokemon_spawn(8,(WIDTH,HEIGHT),10,-110,6)
                        pokemon_spawn(8,(WIDTH,0),0,110,6)
                        end_while_poke_spawn(2,10)

                    pokemon_spawn(8,(WIDTH-200,HEIGHT),120,-90,6)
                    pokemon_spawn(8,(WIDTH-200,0),0,90,6)
                    if while_poke_spawn(15,10,2):
                        pokemon_spawn(8,(WIDTH-100,HEIGHT),15,-90,6)
                        pokemon_spawn(8,(WIDTH-100,0),0,90,6)
                        end_while_poke_spawn(2,10)

                    pokemon_spawn(9,(WIDTH,480),30)
                    pokemon_spawn(9,(WIDTH,240),0)

                    pokemon_spawn(8,(WIDTH-200,HEIGHT),240,-90,6)
                    pokemon_spawn(8,(WIDTH-200,0),0,90,6)
                    if while_poke_spawn(15,10,2):
                        pokemon_spawn(8,(WIDTH-100,HEIGHT),15,-90,6)
                        pokemon_spawn(8,(WIDTH-100,0),0,90,6)
                        end_while_poke_spawn(2,10)                    

                    pokemon_spawn(8,(WIDTH,HEIGHT),120,-135,4)
                    pokemon_spawn(8,(WIDTH,0),0,135,4)
                    if while_poke_spawn(10,10,2):
                        pokemon_spawn(8,(WIDTH,HEIGHT),10,-135,4)
                        pokemon_spawn(8,(WIDTH,0),0,135,4)
                        end_while_poke_spawn(2,10)

                    title_spawn(2,120)

                    next_challenge(260)
                if stage_challenge == 1:

                    if while_poke_spawn(40,10,1):
                        pokemon_spawn(10,(WIDTH+64,randint(50,HEIGHT-50)),40)
                        end_while_poke_spawn(1,10)
                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(11,(WIDTH+64,randint(200,HEIGHT-100)),40)
                        pokemon_spawn(10,(WIDTH+64,randint(50,HEIGHT-25)),0)
                        end_while_poke_spawn(2,10)
                    bground_spawn(8,1)
                    bground_spawn(9,0)
                    pokemon_spawn(9,(WIDTH+64,480),60)
                    pokemon_spawn(9,(WIDTH+64,240),0)                    

                    next_challenge(480)
                if stage_challenge == 2:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(3)
                    if boss.died_next_stage:
                        stage_count = 0
                        boss.died_next_stage = False
                        next_challenge(0)
                if stage_challenge == 3:
                    pokemon_spawn(9,(WIDTH+64,480),30)
                    pokemon_spawn(9,(WIDTH+64,240),0)
                    if while_poke_spawn(40,10,1):
                        pokemon_spawn(11,(WIDTH+64,randint(200,HEIGHT-200)),40)
                        end_while_poke_spawn(1,10)

                    pokemon_spawn(10,(WIDTH+64,HEIGHT/20*stage_repeat_count),120)
                    if while_poke_spawn(20,10,1):
                        pokemon_spawn(10,(WIDTH+64,HEIGHT/20*stage_repeat_count),20)
                        end_while_poke_spawn(1,10)
                    if while_poke_spawn(20,10,1):
                        pokemon_spawn(10,(WIDTH+64,HEIGHT-HEIGHT/20*stage_repeat_count),20)
                        end_while_poke_spawn(1,10)
                    pokemon_spawn(8,(WIDTH,HEIGHT),30,-135,4)
                    pokemon_spawn(8,(WIDTH,0),0,135,4)
                    if while_poke_spawn(10,10,2):
                        pokemon_spawn(8,(WIDTH,HEIGHT),10,-135,4)
                        pokemon_spawn(8,(WIDTH,0),0,135,4)
                        end_while_poke_spawn(2,10)
                    pokemon_spawn(10,(WIDTH+64,120),180)
                    pokemon_spawn(10,(WIDTH+64,600),0)                        
                    if while_poke_spawn(20,10,2):
                        pokemon_spawn(10,(WIDTH+64,HEIGHT/20*stage_repeat_count*2),20)
                        pokemon_spawn(10,(WIDTH+64,HEIGHT-HEIGHT/20*stage_repeat_count*2),0)
                        end_while_poke_spawn(2,10)

                    pokemon_spawn(11,(WIDTH+64,randint(200,HEIGHT-200)),60)
                    if while_poke_spawn(10,10,5):
                        pokemon_spawn(8,(WIDTH+64,randint(200,HEIGHT-200)),10,180,5)
                        pokemon_spawn(8,(WIDTH+64,randint(200,HEIGHT-200)),0,180,5)
                        pokemon_spawn(8,(WIDTH+64,randint(200,HEIGHT-200)),0,180,5)
                        pokemon_spawn(8,(WIDTH+64,randint(200,HEIGHT-200)),0,180,5)
                        pokemon_spawn(8,(WIDTH+64,randint(200,HEIGHT-200)),0,180,5)
                        end_while_poke_spawn(5,10)
                    next_challenge(480)
                if stage_challenge == 4:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(4)
                    if boss.died_next_stage:
                        stage_count = 0
                        if not text.started:
                            stage_challenge = 0
                            stage_line = 0
                            text.re_start()
                            stage_condition = 1   
            if stage_fun == 3:
                if stage_challenge == 0:

                    pokemon_spawn(12,RIGHT_POS[1],120,-135,4)
                    pokemon_spawn(12,RIGHT_POS[2],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[3],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[4],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[5],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[6],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[7],10,-135,4)

                    title_spawn(3,120)

                    next_challenge(260)
                if stage_challenge == 1:
                    pokemon_spawn(13,RIGHT_POS[randint(3,5)],60,180+randint(-20,20),4)

                    if while_poke_spawn(120,3,1):
                        pokemon_spawn(13,RIGHT_POS[randint(3,5)],120,180+randint(-20,20),4)
                        end_while_poke_spawn(1,3)

                    if while_poke_spawn(80,6,3):
                        pokemon_spawn(13,RIGHT_POS[randint(3,5)],80,180+randint(-20,20),4)
                        pokemon_spawn(12,RIGHT_POS[randint(2,6)],0,180,5)
                        pokemon_spawn(12,RIGHT_POS[randint(2,6)],0,180,5)
                        end_while_poke_spawn(3,6)
                    next_challenge(120)
                if stage_challenge == 2:
                    pokemon_spawn(14,RIGHT_POS[4],120,180,5)
                    pokemon_spawn(14,RIGHT_POS[5],300,180,5)
                    pokemon_spawn(14,RIGHT_POS[3],0,180,5)
                    pokemon_spawn(14,RIGHT_POS[6],300,180,5)
                    pokemon_spawn(14,RIGHT_POS[4],0,180,5)
                    pokemon_spawn(14,RIGHT_POS[2],0,180,5)
                    pokemon_spawn(14,RIGHT_POS[2],300,180,5)
                    pokemon_spawn(14,RIGHT_POS[3],0,180,5)
                    pokemon_spawn(14,RIGHT_POS[5],0,180,5)
                    pokemon_spawn(14,RIGHT_POS[6],0,180,5)
                    next_challenge(120)
                if stage_challenge == 3:
                    if while_poke_spawn(80,8,2):
                        pokemon_spawn(15,RIGHT_POS[1],80,180,5)
                        pokemon_spawn(15,RIGHT_POS[7],0,180,5)
                        end_while_poke_spawn(2,8)
                    next_challenge(120)
                if stage_challenge == 4:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(5)
                    if boss.died_next_stage:
                        stage_count = 0
                        boss.died_next_stage = False
                        next_challenge(0)   
                if stage_challenge == 5:
                    if while_poke_spawn(80,8,1):
                        if stage_repeat_count % 2 == 0:
                            pokemon_spawn(13,RIGHT_POS[2],80,180,5)
                        else:
                            pokemon_spawn(13,RIGHT_POS[6],80,180,5)
                        if stage_repeat_count > 4:
                            pokemon_spawn(15,RIGHT_POS[4],0,180,5,True)
                        end_while_poke_spawn(1,8)  
                    next_challenge(120)          
                if stage_challenge == 6:
                    pokemon_spawn(14,RIGHT_POS[1],60,180,4)  
                    pokemon_spawn(14,RIGHT_POS[2],0,180,4)
                    pokemon_spawn(14,RIGHT_POS[4],0,180,4)
                    pokemon_spawn(14,RIGHT_POS[6],0,180,4)
                    pokemon_spawn(14,RIGHT_POS[7],0,180,4) 
                    pokemon_spawn(15,RIGHT_POS[1],480,180,4)  
                    pokemon_spawn(15,RIGHT_POS[2],0,180,4)
                    pokemon_spawn(15,RIGHT_POS[3],0,180,4)
                    pokemon_spawn(15,RIGHT_POS[4],0,180,4)
                    pokemon_spawn(15,RIGHT_POS[5],0,180,4)
                    pokemon_spawn(15,RIGHT_POS[6],0,180,4)
                    pokemon_spawn(15,RIGHT_POS[7],0,180,4)
                    next_challenge(120)
                if stage_challenge == 7:
                    pokemon_spawn(16,RIGHT_POS[4],120,180,6)  
                    pokemon_spawn(16,RIGHT_POS[5],180,180,6)
                    pokemon_spawn(16,RIGHT_POS[3],0,180,6)
                    pokemon_spawn(16,RIGHT_POS[1],180,180,6)           
                    pokemon_spawn(16,RIGHT_POS[7],0,180,6)
                    pokemon_spawn(16,RIGHT_POS[4],180,180,6)
                    pokemon_spawn(13,RIGHT_POS[4],0,180,6)  
                    pokemon_spawn(16,RIGHT_POS[5],180,180,6)
                    pokemon_spawn(16,RIGHT_POS[3],0,180,6)
                    pokemon_spawn(13,RIGHT_POS[4],0,180,6) 
                    pokemon_spawn(16,RIGHT_POS[1],180,180,6)          
                    pokemon_spawn(16,RIGHT_POS[7],0,180,6)
                    pokemon_spawn(13,RIGHT_POS[4],0,180,6)
                    next_challenge(120)   
                if stage_challenge == 8:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(6)
                    if boss.died_next_stage:
                        stage_count = 0
                        if not text.started:
                            stage_challenge = 0
                            stage_line = 0
                            text.re_start()
                            stage_condition = 1 
            if stage_fun == 4:
                if stage_challenge == 0:
                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(17,choice(UP_POS),10,randint(90,110),4)
                        end_while_poke_spawn(1,24)

                    title_spawn(4,120)
                    next_challenge(260)
                if stage_challenge == 1:
                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(17,RIGHT_POS[2],10,170,5)
                        if stage_repeat_count == 0:
                            pokemon_spawn(18,RIGHT_POS[6],0,200,4,True)
                        if stage_repeat_count == 12:
                            pokemon_spawn(18,RIGHT_POS[5],0,200,4,True)
                        end_while_poke_spawn(1,24) 
                    waiting(120)                   
                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(17,RIGHT_POS[6],10,190,5)
                        if stage_repeat_count == 0:
                            pokemon_spawn(18,RIGHT_POS[2],0,160,4,True)
                        if stage_repeat_count == 12:
                            pokemon_spawn(18,RIGHT_POS[3],0,160,4,True)
                        end_while_poke_spawn(1,24)
                    waiting(120) 
                    if while_poke_spawn(10,24,2):
                        pokemon_spawn(17,RIGHT_POS[6],10,190,5)
                        pokemon_spawn(17,RIGHT_POS[2],0,170,5)
                        if stage_repeat_count == 0:
                            pokemon_spawn(18,RIGHT_POS[4],0,180,4,True)
                        if stage_repeat_count == 12:
                            pokemon_spawn(18,RIGHT_POS[4],0,180,4,True)
                        end_while_poke_spawn(2,24)
                    next_challenge(60,True)
                if stage_challenge == 2:
                    pokemon_spawn(19,RIGHT_POS[4],60,180,5)
                    pokemon_spawn(19,RIGHT_POS[3],420,180,5)
                    pokemon_spawn(19,RIGHT_POS[5],0,180,5)
                    pokemon_spawn(19,RIGHT_POS[2],420,180,5)
                    pokemon_spawn(19,RIGHT_POS[6],0,180,5)
                    next_challenge(660,True)
                if stage_challenge == 3:
                    if while_poke_spawn(30,7,1):
                        pokemon_spawn(20,choice([DOWN_POS[2],DOWN_POS[3],DOWN_POS[4]]),30,-90,0)
                        if stage_repeat_count>3:
                            pokemon_spawn(17,choice([RIGHT_POS[5],RIGHT_POS[3],RIGHT_POS[4]]),60,180,7,True)
                            pokemon_spawn(17,choice([RIGHT_POS[5],RIGHT_POS[3],RIGHT_POS[4]]),60,180,7,True)
                        end_while_poke_spawn(1,7)
                    waiting(120)
                    if while_poke_spawn(30,7,1):
                        pokemon_spawn(20,choice([UP_POS[2],UP_POS[3],UP_POS[4]]),30,90,0)
                        if stage_repeat_count>3:
                            pokemon_spawn(17,choice([RIGHT_POS[5],RIGHT_POS[3],RIGHT_POS[4]]),60,180,7,True)
                            pokemon_spawn(17,choice([RIGHT_POS[5],RIGHT_POS[3],RIGHT_POS[4]]),60,180,7,True)
                        end_while_poke_spawn(1,7)
                    next_challenge(240)
                if stage_challenge == 4:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(7)
                    if boss.died_next_stage:
                        stage_count = 0
                        boss.died_next_stage = False
                        next_challenge(0) 
                if stage_challenge == 5:
                    if while_poke_spawn(10,60,1):
                        pokemon_spawn(17,choice([RIGHT_POS[1],RIGHT_POS[2],RIGHT_POS[3],RIGHT_POS[4]]),10,randint(150,170),7)
                        if while_time(stage_repeat_count,10):
                            pokemon_spawn(18,RIGHT_POS[4],0,180,6,True)
                        end_while_poke_spawn(1,30)    
                    waiting(120)                            
                    if while_poke_spawn(10,60,1):
                        pokemon_spawn(17,choice([RIGHT_POS[7],RIGHT_POS[6],RIGHT_POS[5],RIGHT_POS[4]]),10,randint(190,210),7)
                        if while_time(stage_repeat_count,10):
                            pokemon_spawn(18,RIGHT_POS[4],0,180,6,True)
                        end_while_poke_spawn(1,30)    
                    waiting(120) 
                    if while_poke_spawn(10,60,1):
                        pokemon_spawn(17,choice([RIGHT_POS[1],RIGHT_POS[2],RIGHT_POS[3],RIGHT_POS[4]]),10,randint(150,170),7)
                        if while_time(stage_repeat_count,29):
                            pokemon_spawn(19,RIGHT_POS[5],0,180,6,True)
                        end_while_poke_spawn(1,30)    
                    waiting(120) 
                    if while_poke_spawn(10,60,1):
                        pokemon_spawn(17,choice([RIGHT_POS[7],RIGHT_POS[6],RIGHT_POS[5],RIGHT_POS[4]]),10,randint(190,210),7)
                        if while_time(stage_repeat_count,29):
                            pokemon_spawn(19,RIGHT_POS[3],0,180,6,True)
                        end_while_poke_spawn(1,30)    
                    next_challenge(240)
                if stage_challenge == 6:
                    if while_poke_spawn(100,8,1):
                        pokemon_spawn(20,(player.pos[0],HEIGHT+64),100,-90,0)
                        if stage_repeat_count > 3:
                            pokemon_spawn(17,(WIDTH + 64,player.pos[1]),0,172,7,True)
                            pokemon_spawn(17,(WIDTH + 64,player.pos[1]),0,174,6,True)
                            pokemon_spawn(17,(WIDTH + 64,player.pos[1]),0,176,5,True)
                            pokemon_spawn(17,(WIDTH + 64,player.pos[1]),0,178,4,True)
                            pokemon_spawn(17,(WIDTH + 64,player.pos[1]),0,180,3,True)
                        end_while_poke_spawn(1,8)     
                    next_challenge(120)  
                if stage_challenge == 7:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(8)
                    if boss.died_next_stage:
                        stage_count = 0
                        if not text.started:
                            stage_challenge = 0
                            stage_line = 0
                            text.re_start()
                            stage_condition = 1                                              
            if stage_fun == 5:
                if stage_challenge == 0:
                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(21,choice(RIGHT_POS2),10,180,4)
                        end_while_poke_spawn(1,24)
                    title_spawn(5,120)
                    next_challenge(240)                
                if stage_challenge == 1:
                    pokemon_spawn(22,RIGHT_POS[5],1,180,4)   
                    pokemon_spawn(22,RIGHT_POS[3],180,180,4)  
                    pokemon_spawn(22,RIGHT_POS[4],180,180,4)        
                    pokemon_spawn(22,RIGHT_POS[3],180,180,4)  
                    pokemon_spawn(22,RIGHT_POS[5],0,180,4)              
                    pokemon_spawn(22,RIGHT_POS[2],180,180,4)  
                    pokemon_spawn(22,RIGHT_POS[6],0,180,4)

                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(21,RIGHT_POS[7],10,randint(25,65)+180,4)    
                        end_while_poke_spawn(1,24) 
                    next_challenge(60)
                if stage_challenge == 2:
                    pokemon_spawn(23,RIGHT_POS[2],1,160,5)   
                    pokemon_spawn(23,RIGHT_POS[6],300,-160,5)  
                    pokemon_spawn(23,RIGHT_POS[4],200,-160,5) 
                    waiting(280)
                    if while_poke_spawn(10,140,1):
                        pokemon_spawn(21,choice(DOWN_POS),10,-90,randint(4,5)) 
                        if when_time(stage_repeat_count,24):
                            pokemon_spawn(22,RIGHT_POS2[1],0,170,5,True) 
                        if when_time(stage_repeat_count,48):
                            pokemon_spawn(22,RIGHT_POS2[2],0,170,5,True) 
                        if when_time(stage_repeat_count,72):
                            pokemon_spawn(22,RIGHT_POS2[3],0,170,5,True) 
                        if when_time(stage_repeat_count,96):
                            pokemon_spawn(22,RIGHT_POS2[4],0,170,5,True) 
                        end_while_poke_spawn(1,92)      

                    pokemon_spawn(23,RIGHT_POS[3],60,160,5)  
                    pokemon_spawn(23,RIGHT_POS[5],0,-160,5)
                    next_challenge(360)
                if stage_challenge == 3:
                    waiting(120)
                    pokemon_spawn(24,RIGHT_POS[6],20,180,5) 
                    if while_poke_spawn(20,16,1):
                        pokemon_spawn(26,RIGHT_POS[6],20,180,5)  
                        end_while_poke_spawn(1,16)  
                    pokemon_spawn(24,RIGHT_POS[2],20,180,5) 
                    if while_poke_spawn(20,16,1):
                        pokemon_spawn(26,RIGHT_POS[2],20,180,5)  
                        end_while_poke_spawn(1,16)   

                    pokemon_spawn(24,RIGHT_POS[4],60,180,5)
                    if while_poke_spawn(20,8,2):
                        pokemon_spawn(26,RIGHT_POS[3],20,160,5)  
                        pokemon_spawn(26,RIGHT_POS[5],0,-160,5)  
                        end_while_poke_spawn(2,8) 
                    pokemon_spawn(24,RIGHT_POS[2],60,180,5)
                    pokemon_spawn(24,RIGHT_POS[6],0,180,5)
                    if while_poke_spawn(20,8,2):
                        pokemon_spawn(26,RIGHT_POS[2],20,135,5)  
                        pokemon_spawn(26,RIGHT_POS[6],0,-135,5)  
                        end_while_poke_spawn(2,8) 
                    next_challenge(120)
                if stage_challenge == 4:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(9)
                    if boss.died_next_stage:
                        stage_count = 0
                        boss.died_next_stage = False
                        next_challenge(0) 
                if stage_challenge == 5:
                    pokemon_spawn(25,RIGHT_POS[4],60,180,12) 
                    pokemon_spawn(25,RIGHT_POS[4],120,180,12)
                    pokemon_spawn(25,RIGHT_POS[4],60,180,12)
                    if while_poke_spawn(20,32,2): 
                        pokemon_spawn(26,RIGHT_POS[7],20,180,5) 
                        pokemon_spawn(21,RIGHT_POS[4],0,randint(170,190),5) 
                        if while_time(stage_repeat_count,14):
                            pokemon_spawn(22,RIGHT_POS[4],0,180,5,True) 
                        if when_time(stage_repeat_count,16):
                            pokemon_spawn(23,RIGHT_POS[2],0,160,6,True)
                        end_while_poke_spawn(2,64)
                    next_challenge(300) 
                if stage_challenge == 6:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(10)
                    if boss.died_next_stage:
                        stage_count = 0
                        if not text.started:
                            stage_challenge = 0
                            stage_line = 0
                            text.re_start()
                            stage_condition = 1                      
            if stage_fun == 6:              
                if stage_challenge == 0:
                    title_spawn(6,120)
                    waiting(60*4)
                    if while_poke_spawn(20,20,1):
                        pokemon_spawn(27,(WIDTH+64,16+stage_repeat_count*15),20,180,6)
                        end_while_poke_spawn(1,20)
                    if while_poke_spawn(20,20,1):
                        pokemon_spawn(27,(WIDTH+64,HEIGHT-16-stage_repeat_count*15),20,180,6)
                        end_while_poke_spawn(1,20)            

                    pokemon_spawn(28,RIGHT_POS[4],360,180,6)   
                    pokemon_spawn(28,RIGHT_POS[3],240,180,6)    
                    pokemon_spawn(28,RIGHT_POS[5],240,180,6)
                    pokemon_spawn(28,RIGHT_POS[2],240,180,6)
                    pokemon_spawn(28,RIGHT_POS[6],240,180,6)
                    pokemon_spawn(28,RIGHT_POS[4],240,180,6)

                    pokemon_spawn(29,RIGHT_POS[1],360,180,6)
                    pokemon_spawn(29,RIGHT_POS[7],0,180,6)     
                    pokemon_spawn(29,RIGHT_POS[1],300,180,6)
                    pokemon_spawn(29,RIGHT_POS[7],0,180,6)  
                    pokemon_spawn(29,RIGHT_POS[1],300,180,6)
                    pokemon_spawn(29,RIGHT_POS[7],0,180,6) 
                    next_challenge(360)
                if stage_challenge == 1:
                    pokemon_spawn(30,RIGHT_POS[4],180,180,2)
                    pokemon_spawn(30,RIGHT_POS[1],120,180,2)
                    pokemon_spawn(30,RIGHT_POS[5],120,180,2)
                    pokemon_spawn(30,RIGHT_POS[6],120,180,2)
                    pokemon_spawn(30,RIGHT_POS[2],120,180,2)
                    pokemon_spawn(30,RIGHT_POS[3],120,180,2)
                    waiting(360)
                    if while_poke_spawn(20,20,1):
                        pokemon_spawn(27,(WIDTH+64,16+stage_repeat_count*15),20,180,6)
                        end_while_poke_spawn(1,20)
                    pokemon_spawn(29,RIGHT_POS[4],90,180,6)
                    waiting(90)
                    if while_poke_spawn(20,20,1):
                        pokemon_spawn(27,(WIDTH+64,HEIGHT-16-stage_repeat_count*15),20,180,6)
                        end_while_poke_spawn(1,20) 
                    next_challenge(60*12)
                if stage_challenge == 2:
                    if not boss.appear and not boss.died_next_stage: 
                        boss_spawn(11)
                    if boss.died_next_stage:
                        stage_count = 0
                        if not text.started:
                            stage_challenge = 0
                            stage_line = 0
                            text.re_start()
                            stage_condition = 1 
                
            stage_cline = 0
    ################################################# 
    while play:
        # 60 프레임
        clock.tick(FPS)
        now = time.time()
        dt = (now-prev_time)*TARGET_FPS
        prev_time = now
        keys = pygame.key.get_pressed() 
        if cur_screen == 1:
            # 키 이벤트
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    play = False
                if ev.type == pygame.KEYDOWN:                    
                    if ev.key == pygame.K_f:
                        full_on = False if full_on == True else True
                    if ev.key == pygame.K_ESCAPE:
                        pause = False if pause == True else True
                    if ev.key == pygame.K_z and text.started and text.count > 50 and not text.pause:
                        text.next_text()
                    if ev.key == pygame.K_x and player.mp > 0 and not bomb_activated:
                        bomb_group.add(Bomb(player.pos,1))
                        bomb_hit_group.add(Bomb_hit(player.pos,1))
                        player.mp -= 1      
                        bomb_activated = True
            # 탄에 박았는가
            hit_list = pygame.sprite.spritecollide(player_hitbox, spr, not player.godmod, pygame.sprite.collide_circle)
            beam_collide = pygame.sprite.groupcollide(beams_group, enemy_group, False, False, pygame.sprite.collide_circle)
            if beam_collide.items():
                for beam, enemy in beam_collide.items():                   
                    for i in range(0,len(enemy)): 
                        if not beam.died: 
                            enemy[i].health -= beam.damage
                            beam.died = True

            if boss.appear: boss_collide = pygame.sprite.spritecollide(boss, beams_group, False, pygame.sprite.collide_circle)
        
            if bomb_activated:
                beam_collide = pygame.sprite.groupcollide(bomb_group, enemy_group, False, False, pygame.sprite.collide_circle)
                if beam_collide.items():
                    for beam, enemy in beam_collide.items():
                        for i in range(0,len(enemy)): 
                            enemy[i].health -= 1
                if boss.appear: boss_collide = pygame.sprite.spritecollide(boss, bomb_group, False, pygame.sprite.collide_circle)
                beam_collide = pygame.sprite.groupcollide(bomb_hit_group, spr, False, False, pygame.sprite.collide_circle)
                if beam_collide.items(): # 봄이 탄에 맞았을때 작은점수
                    for beam, enemy in beam_collide.items():
                        for i in range(0,len(enemy)): 
                            item_group.add(Item(enemy[i].pos,1))
                            enemy[i].kill()

                if not bomb_group:
                    bomb_activated = False
            # 연산 업데이트
            if not pause:      
                if len(magic_spr.sprites()) != 0:magic_spr.update(screen)    
                if boss.appear and boss.health <= 0: remove_allbullet()  
                if lazer_spawner:
                    for i in lazer_spawner:
                        add_effect(i[0],2,i[3])
                        if while_time(i[4],3):bullet(i[0],i[1],i[2],0,i[3])
                        lazer_spawner[lazer_spawner.index(i)][4] -= 1
                        if lazer_spawner[lazer_spawner.index(i)][4] == 0:
                            del lazer_spawner[lazer_spawner.index(i)]
                spr.update(screen)
                if not time_stop:
                    player_hitbox.update()
                    if beams_group: beams_group.update()                            
                    player_group.update(hit_list)
                    if enemy_group:enemy_group.update()
                    if item_group: item_group.update()
                    if boss.appear: boss_group.update(boss_collide)
                    if effect_group: effect_group.update()
                    player_sub.update()
                    if bomb_group: 
                        bomb_group.update()
                        bomb_hit_group.update()
                    if text.started and not text.pause: text.update()
                    stage_manager()
                    frame_count += 1
                    stage_count += 1
                    if not bkgd_list == []:
                        for i in bkgd_list:i.update()
                
            # 그리기 시작
            render_layer.fill((0,0,0))
            #배경 스크롤
            background_scroll()                
            # 점수 표시
            bomb_group.draw(render_layer)
            item_group.draw(render_layer)
            magic_spr.draw(render_layer)      
            beams_group.draw(render_layer)
            player_group.draw(render_layer) 
            player_sub.draw()
            enemy_group.draw(render_layer)            
            if not starting or read_end: enemy_group.draw(render_layer)
            if boss.appear: boss_group.draw(render_layer)
            under_ui.draw()
            screen.blit(pygame.transform.scale2x(render_layer),(0,0))
            spr.draw(screen)
            up_render_layer.fill((0,0,0,0))
            effect_group.draw(up_render_layer)                     
            title.draw()
            if text.started:text.draw()
            ui.draw()
            if boss.spell and boss.appear and boss.spell[0].spellcard:
                boss.spell[0].draw()
            screen.blit(pygame.transform.scale2x(up_render_layer),(0,0))
            pygame.display.flip()
        if cur_screen == 0:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    play = False
                if ev.type == pygame.KEYDOWN: 
                    if ev.key == pygame.K_UP:
                        curser = curser_max if curser == 0 else curser - 1 # 커서위로
                    if ev.key == pygame.K_DOWN:
                        curser = 0 if curser == curser_max else curser + 1 # 커서밑으로
                    if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                        if (curser == 1 or curser == 2) and select_mod == 0: break
                        if curser == 4 and select_mod == 0: play = False # 게임끄기
                        if not menu_mod == 3: # 옵션 창이면 모드 옮기기 X
                            select_mod += 1
                        if menu_mod == 0: cur_screen = 1 ############ 게임시작
                        menu_mod = curser
                        curser = 0
                    if ev.key == pygame.K_f:
                        full_on = False if full_on == True else True                        
                    if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                        if select_mod > 0: select_mod -= 1
                        menu_mod = -1
                        try:sfx_volume = msfx_volume/100
                        except:sfx_volume = 0
                        try:music_volume = mmusic_volume/100
                        except:music_volume = 0
                        music_and_sfx_volume()
                    if ev.key == pygame.K_RIGHT:
                        if menu_mod == 3:
                            if curser == 1:
                                mmusic_volume = mmusic_volume + 5 if mmusic_volume < 100 else 100
                            if curser == 2:
                                msfx_volume = msfx_volume + 5 if msfx_volume < 100 else 100
                    if ev.key == pygame.K_LEFT:
                        if menu_mod == 3:
                            if curser == 1:
                                mmusic_volume = mmusic_volume - 5 if mmusic_volume > 0 else 0
                            if curser == 2:
                                msfx_volume = msfx_volume - 5 if msfx_volume > 0 else 0
            render_layer.blit(background_img,(0,0))
            
            ui_x = WIDTH - 150
            ui_y = HEIGHT - 200
            if select_mod == 0:
                curser_max = 4
                render_layer.blit(menu_img,(0,0),(0,0,320,40))
                for i in range(0,5):
                    if curser == i:
                        render_layer.blit(menu_img,(ui_x,ui_y+20*i),(128,40+20*i,114,23))
                    else:
                        render_layer.blit(menu_img,(ui_x,ui_y+20*i),(0,40+20*i,114,23))
            if select_mod == 1:
                if menu_mod == 0: # 난이도 정하기
                    curser_max = 3
                    for i in range(0,4):
                        render_layer.blit(menu_img,(int(WIDTH/2-120),int(HEIGHT/2-60+128*i-128*curser)),(0,320+64*i,288,64))
                        difficulty = curser
                if menu_mod == 3:
                    curser_max = 3
                    text_box = ["화면모드","음악","효과음","플레이어"]

                    text_box[0] = "화면모드    창모드" if full_on == 0 else "화면모드    전체화면"
                    text_box[1] = "음악   " + str(mmusic_volume)
                    text_box[2] = "효과음  " + str(msfx_volume)
                    for i in range(0,4):
                        text_color = (255,0,255) if i == curser else (0,0,255)
                        text1 = score_font.render(text_box[i], True, text_color)
                        render_layer.blit(text1,(200,200+80*i))
            screen.blit(pygame.transform.scale2x(render_layer),(0,0))
            pygame.display.flip()
        
        if full_on != cur_full_mod:
            if full_on:
                screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN|pygame.SCALED)
            else:
                screen = pygame.display.set_mode((WIDTH*2, HEIGHT*2))
            cur_full_mod = full_on

    pygame.quit()
    exit()

if __name__ == "__main__":
    play_game()

