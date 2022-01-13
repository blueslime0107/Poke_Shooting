from sys import float_repr_style
import pygame, math
from random import randint, uniform
from pygame.locals import *
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
pygame.mixer.set_num_channels(32)

def play_game():
    
    global WIDTH, HEIGHT, screen
    # 이미지 불러오기
    bullet_image = pygame.image.load('Image\Bullets.png').convert_alpha()
    bg_image = pygame.image.load('Image\Bg1.png').convert()
    bg2_image = pygame.image.load('Image\Bg2.png').convert()
    pkmon_image = pygame.image.load('Image\pokemon.png').convert_alpha()
    background_img = pygame.image.load('Image\\background.jpg').convert()
    menu_img = pygame.image.load('Image\Menus.png').convert_alpha()
    item_img = pygame.image.load('Image\item.png').convert_alpha()
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    player_slow_img = pygame.Surface((64, 64), pygame.SRCALPHA)
    player_slow_img.blit(bullet_image, (0,0), Rect(128,128,64,64))
    player_slow_img = pygame.transform.scale(player_slow_img, (64*2, 64*2))

    msfx_volume = 100
    mmusic_volume = 100
    try:sfx_volume = msfx_volume / 1000
    except:sfx_volume = 0
    try:music_volume = mmusic_volume / 200
    except:music_volume = 0
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
    s_item0 = pygame.mixer.Sound('Music\SFX\se_item00.wav')
    s_item0.set_volume(sfx_volume+0.1)
    s_enedead = pygame.mixer.Sound('Music\SFX\se_enep00.wav')
    s_enedead.set_volume(sfx_volume+0.15)
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
            self.power = 0
            self.mp = 8

            self.count = 0
            self.radius = 4 # 원 충돌범위를 위한 반지름 값
            self.godmod = False # 무적?
            self.hit_speed = 0
            self.hit_dir = 0

        def update(self,collide):

            dx, dy = 0 , 0
            keys = pygame.key.get_pressed() 
            inum = self.img_num
            self.img_num = 0

            # 플레이어 이동 조종 SHIFT 를 누르면 느리게 움직이기
            if keys[pygame.K_LSHIFT]:
                self.speed = 2
            else:
                self.speed = 7
            
            # 화면 밖으로 안나감
            if keys[pygame.K_RIGHT]:dx += 0 if self.rect.centerx >= WIDTH-20 else self.speed            
            if keys[pygame.K_LEFT]:dx -= 0 if self.rect.centerx <= 0 + 20 else self.speed            
            if keys[pygame.K_DOWN]:dy += 0 if self.rect.centery >= 720-20 else self.speed               
            if keys[pygame.K_UP]:dy -= 0 if self.rect.centery <= 0+20 else self.speed
               
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

    class Player_sub():
        def __init__(self,num):
            self.num = num
            self.ball = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(self.ball, (255, 0, 222), (16,16), 16)
            pygame.draw.circle(self.ball, (247, 178, 238), (16,16), 13)
            self.ballxy = [(-20,-20),(-20,-20),(-20,-20),(-20,-20)]
            self.adddir = 0
            self.radi = 80
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
            screen.blit(self.ball,get_new_pos(self.ballxy[0]))
            screen.blit(self.ball,get_new_pos(self.ballxy[1]))
            screen.blit(self.ball,get_new_pos(self.ballxy[2]))
            screen.blit(self.ball,get_new_pos(self.ballxy[3]))

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
            self.damage = 1
            self.can_damage = True

        def update(self):
            if self.count == 0:
                s_cat1.play()
                if self.num == 1:
                    image = pygame.Surface((64,64), pygame.SRCALPHA)
                    pygame.draw.circle(image, (255,0,255,90), (32,32), 32)

                image = pygame.transform.scale2x(image)
                self.image = image
                self.rect = self.image.get_rect(center = get_new_pos(self.pos))
                self.image2 = self.image.copy()

            if self.num == 1:
                self.pos = player.pos
                if self.count <= 30: self.image = pygame.transform.scale(self.image2, (self.count*16, self.count*16))
                elif big_small(self.count,50,110): self.image = pygame.transform.scale(self.image2, (self.rect.width-8,self.rect.width-8))
                elif big_small(self.count,120,180): self.image = pygame.transform.scale(self.image2, (self.rect.width+35,self.rect.width+35))
                if when_time(self.count, 50): s_ch0.play()
                if when_time(self.count, 120): s_boom.play()


                self.radius = self.image.get_rect().width/2
                if self.count >= 240:
                    self.image = pygame.transform.scale(self.image2, (self.rect.width-35,self.rect.width-35))
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
                    x_move = (self.count - 32)/5-20
                    if self.count > 300: 
                        self.save = self.save * 1.1
                        x_move -= self.save
                    
                    pygame.draw.rect(screen, (255,0,0), (get_new_pos((WIDTH/2-186-x_move,HEIGHT/2-26)),(130,-45)))
                    pygame.draw.rect(screen, (255,0,0), (get_new_pos((WIDTH/2-60-x_move,HEIGHT/2-1)),(200,-45)))
                    title_text = score_font.render(self.text, True, (255,255,255))
                    screen.blit(title_text,get_new_pos((WIDTH/2-250+10-x_move,HEIGHT/2-100+10)))
                    title_text = score_font.render(self.name, True, (0,0,0))
                    screen.blit(title_text,get_new_pos((WIDTH/2-250+200-x_move,HEIGHT/2-60)))
                if self.count < 64:
                    pygame.draw.rect(screen, (255,255,255), (get_new_pos((WIDTH/2-250,HEIGHT/2-1)),(500,round(-abs(math.sin(self.count/20)*100)))))
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
            self.image = pygame.Surface((40, 32), pygame.SRCALPHA)                   
            self.rect = self.image.get_rect(center = get_new_pos(pos))            
            self.pos = get_new_pos(pos)
            self.num = num
            self.speed = 0
            self.direction = dir           
            self.damage = 0
            self.can_damage = True
            self.radius = 20
            if self.num == 0:
                self.image.fill((255, 0, 222))
                pygame.draw.rect(self.image, (247, 178, 238), (3,3,34,26),0)
                self.speed = 40
                self.damage = 3
            if self.num == 1:
                pygame.draw.rect(self.image, (247, 178, 238), (3,3,34,26),0)
                self.speed = 20
                self.damage = 1
                if enemy_group: self.direction = look_at_point(self.pos,enemy_group.sprites()[0].pos)
                if boss.appear: self.direction = look_at_point(self.pos,boss_group.sprites()[0].pos)
            self.image_sample = self.image.copy()
            self.image_rotate = pygame.transform.rotate(self.image_sample, self.direction)
            

        def update(self):
            # 화면 나가면 삭제
            if self.pos[0] >= WIDTH:
                self.kill()
            if self.speed == 0:
                self.kill()
            if not self.can_damage:
                self.image_sample.fill((255,255,255))
                self.image_sample = pygame.transform.scale(self.image_sample, (60, 32))
                self.speed = 0
    
                

            self.image_rotate = pygame.transform.rotate(self.image_sample, self.direction)
            self.image = self.image_rotate
            self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
            self.rect.center = round(self.pos[0]), round(self.pos[1]) 

    # 적
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, dir, speed, health, img, hit_cir, num):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((256, 256), pygame.SRCALPHA)
            self.image.blit(pokemons[img-1],(0,0))      
            self.rect = self.image.get_rect(center = get_new_pos((x, y)))
            self.radius = hit_cir
            self.pos = (x, y)
            #pygame.draw.circle(self.image, (200,0,0), (128,128), self.radius, 3)

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
            self.pos, self.move_dir, self.move_speed ,self.count= enemy_attack(self.num, self.count, self.pos, self.move_dir, self.move_speed)

            if not screen_rect.colliderect(self.rect) and self.screen_apper: # 밖으로 나가면 사라지기
                self.kill() 
            if screen_rect.colliderect(self.rect) and not self.screen_apper:
                self.screen_apper = True
            if self.health <= 0: # 체력 다 달면 죽기
                s_enedead.play()
                effect_group.add(Effect(self.pos,1))
                item_group.add(Item(self.pos,0))
                self.kill()

            self.count += 1
            self.rect.center = (int(self.pos[0]),int(self.pos[1]))    
    
    # 보스
    class Boss_Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((256, 256), pygame.SRCALPHA)      
            self.rect = self.image.get_rect(center = (x, y))
            self.radius = 0
            self.pos = (x, y)
            

            self.count = 0
            self.list = [0,0,0,0]
            self.max_health = 0
            self.health = 1
            self.num = 0

            # 적이동을 위한 값
            self.move_dir = 0
            self.move_speed = 0
            self.move_point = (0,0)
            self.ready = False
            self.move_ready = False # 스펠 시작시 움직이는중?
            self.godmod = False
            self.dieleft = False
            self.spell = []
            self.dies = False

            self.appear = False
            self.real_appear = False
            self.attack_start = False

        def update(self, collide):
            global score
            if self.appear:

                if self.attack_start:
                    # 보스가 등장했을때 실행
                    if self.dieleft: # 죽었다면 삭제
                        self.pos = (-128,-128) 
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
                        self.count, self.pos, self.move_dir, self.move_speed, self.ready = boss_attack(self.spell[0].num, self.count, self.pos, self.move_dir, self.move_speed, self.ready)

                    # 빔에 맞았을때
                    if len(collide) > 0 and not self.godmod:
                        for beam in collide:
                            if beam.can_damage:
                                self.health -= beam.damage
                                if self.health/self.max_health < 0.25:
                                    s_damage1.play(loops=1, maxtime=50)  
                                else: 
                                    s_damage0.play(loops=1, maxtime=50)
                                beam.can_damage = False

                    if self.health <= 0 and not self.dieleft and self.ready: # 체력다 닳음 죽은적이없고 스펠시전 중이였을때 실행
                        self.count = 0
                        self.move_speed = 0
                        self.move_ready = False
                        self.ready = False
                        if len(self.spell) > 1: # 스펠카드가 남아있다면 안죽기
                            del self.spell[0] # 사용한 스펠 삭제
                            if self.spell[0].spellcard:
                                s_cat1.play()
                            else:
                                s_tan1.play()
                        else:#퇴장
                            s_enep1.play()
                            self.dieleft = True
                            self.move_point = (0,0)
                            self.appear = False
                    self.count += 1
                if self.real_appear and not self.attack_start:
                    if distance(self.pos,(780,360)) <= 5:
                        self.pos = (WIDTH-300,HEIGHT/2)
                        self.move_point = (0,0)
                    elif self.move_point == (0,0):
                        self.move_point = ((780-self.pos[0])/60,(360-self.pos[1])/60)
                        print(self.move_point) 
                    self.pos = (self.pos[0]+self.move_point[0],self.pos[1] + self.move_point[1])

            self.rect.center = (int(self.pos[0]),int(self.pos[1])) 
    
    class Spell():
        def __init__(self,number,health,spellcard):
            self.health = health
            self.spellcard = spellcard
            self.num = number
        
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
            self.rect = self.image.get_rect(center = (int(x), int(y)))
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
                self.rect = self.image.get_rect(center = (int(self.pos[0]),int(self.pos[1])))
            
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


            # 각도 계산후 위치 업데이트
            self.pos = calculate_new_xy(self.pos, self.speed, -self.direction)
            self.rect.center = round(self.pos[0]), round(self.pos[1]) 
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
            if self.count == 0:
                if self.num == 1:
                    image = pygame.Surface((64,64), pygame.SRCALPHA)
                    image.blit(bullet_image,(0,0),(192,128,64,64))
                    effect_group.add(Effect(self.pos,3))
                if self.num == 2:
                    image = bullets[21][self.col]
                    image = pygame.transform.scale2x(image)
                    image = pygame.transform.scale2x(image)
                if self.num == 3:
                    image = pygame.Surface((64,64), pygame.SRCALPHA)
                if self.num == 4:
                    image = pygame.Surface((64,64), pygame.SRCALPHA)
                image = pygame.transform.scale2x(image)
                self.image = image
                self.rect = self.image.get_rect(center = (get_new_pos((self.pos))))
                self.image2 = self.image.copy()
            if self.num == 1 or self.num == 2:
                if self.rect.width-self.count*2 <= 0: self.kill()
                else: self.image = pygame.transform.scale(self.image2, (self.rect.width-self.count*2,self.rect.height-self.count*2))
            if self.num == 3:
                if self.rect.width+self.count*4 >= 512: self.kill()
                else: 
                    self.image = pygame.transform.scale(self.image2, (self.rect.width+self.count*4,self.rect.height+self.count*4))
                    self.image.fill((0,0,0,0))
                    pygame.draw.circle(self.image, (255,255,255,80), (round((self.rect.width+self.count*4)/2),round((self.rect.width+self.count*4)/2)), round((self.rect.width+self.count*4)/2), 1)

            self.rect = self.image.get_rect(center = get_new_pos((self.pos)))
            self.count += 1

    class Item(pygame.sprite.Sprite):
        def __init__(self, pos, num):
            pygame.sprite.Sprite.__init__(self) # 초기화?
            self.image = pygame.transform.scale2x(items[num])       # 이미지          
            self.rect = self.image.get_rect(center = (round(pos[0]), round(pos[1])))
            self.image2 = self.image.copy()
            self.pos = pos
            self.count = 0
            self.num = num
            self.lock = False

        def update(self):
            global score
            
            # 움직임
            if not self.lock:
                if self.count < 80:
                    self.pos = (self.pos[0]+10-self.count/4,self.pos[1])
                    self.image = pygame.transform.rotate(self.image2, self.count*4)
                else:
                    self.pos = (self.pos[0]-5,self.pos[1])
                if self.count == 80:
                    self.image = pygame.transform.rotate(self.image2, 0)

            # 화면 넘어가면 삭제:
            if self.pos[0] < -20:
                self.kill()
            # 플레이어 범위 작으면 먹기
            if distance(self.pos,player.pos) < 70:
                score += 100
                if player.power < 400: player.power += 1
                s_item0.play()
                self.kill()
            # 좌표 600이상이면 플레이어 다라가기
            if player.pos[0] >= 600 and not self.lock:
                self.lock = True
                self.image = pygame.transform.rotate(self.image2, 0)
            if self.lock:
                self.pos = calculate_new_xy(self.pos,13,-look_at_player(self.pos))


            self.rect = self.image.get_rect(center = get_new_pos((self.pos)))
            self.count += 1

    class UI():
        def __init__(self,val):
            self.val = val
            self.power= pygame.Surface((100, 20), pygame.SRCALPHA)
            self.power_xy = (20,20)
            self.skill_xy = (0,0)

        def draw(self):
            if player.power < 100:pygame.draw.rect(screen, (255,10,0), ((self.power_xy),(player.power*2,20)))
            else:pygame.draw.rect(screen, (255,10,0), ((self.power_xy),(200,20)))
            if player.power < 200:pygame.draw.rect(screen, (0,255,0), ((self.power_xy),(player.power*2-100*2,20)))
            else:pygame.draw.rect(screen, (0,255,0), ((self.power_xy),(200,20)))
            if player.power < 300:pygame.draw.rect(screen, (0,0,255), ((self.power_xy),(player.power*2-200*2,20)))
            else:pygame.draw.rect(screen, (0,0,255), ((self.power_xy),(200,20)))
            if player.power < 400:pygame.draw.rect(screen, (0,0,0), ((self.power_xy),(player.power*2-300*2,20)))
            else:pygame.draw.rect(screen, (0,0,0), ((self.power_xy),(200,20)))
            text = ui_font.render(str(player.power), True, (255,255,255))
            screen.blit(text,self.power_xy) 
            text = ui_font.render("MP " + str(player.mp)+"/ 8", True, (255,255,255))
            screen.blit(text,self.skill_xy)
    
    class TextBox():
        def __init__(self):
            self.image1 =  0
            self.image2 =  0
            self.stat = 0
            self.text = 0
            self.text2 = 0
            self.started = False
            self.count = 0
            self.font = pygame.font.Font('Font\SEBANG Gothic Bold.ttf', 40)
            self.textbox = pygame.Surface((980,200), pygame.SRCALPHA)
            self.textbox.fill((0,0,0,150))
            self.alpha = 0
        
        def next_text(self):
            self.count = 50
            text = ""
            if self.started:
                self.stat += 1
                if self.stat == 1:
                    text = "test1_test2"
                if self.stat == 2:
                    boss.real_appear = True
                    text = "boss_appear"
                if self.stat == 3:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('Music\\BGM\\The Rabbit Has Landed.wav')
                    pygame.mixer.music.play(-1)
                    text = "boss_sound_play"
                if self.stat == 4:
                    self.started = False
                    boss.attack_start = True
                    self.stat = 0

                if self.stat > 0:
                    textlist = text.split('_')
                    self.text = self.font.render(textlist[0], True, (255,255,255))
                    if len(textlist) == 2: self.text2 = self.font.render(textlist[1], True, (255,255,255))     
                    else: self.text2 = self.font.render("", True, (255,255,255))

        def update(self):
            self.count += 1
            if self.count <= 50:
                self.textbox = pygame.transform.scale(self.textbox, (980, self.count*4))
            if self.count == 50:
                self.next_text()
        def draw(self):
            if self.started:
                screen.blit(self.textbox,(50,HEIGHT-250))
                if self.stat > 0: 
                    screen.blit(self.text,(100,HEIGHT-230))
                    screen.blit(self.text2,(100,HEIGHT-180))


    def get_new_pos(pos,x=0,y=0):
        return (round(pos[0] + x), round(pos[1] + y))

    def big_small(val,min,max):
        return min < val and val < max

    def when_time(val,time):
        return val == time

    def while_time(val,time):
        return val % time == 0

    def bullet(pos,dir,speed,img,col,mode=0,num = (0,0)):
        #effect.add(Effect(pos,1))
        spr.add(Bullet(pos[0],pos[1],dir,speed,img,col,mode,num))

    def add_effect(pos,num,col=0):
        effect_group.add(Effect(pos,num,col))

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

    # 소리
    def play_sound(sound,count,time,max=0):
        if when_time(count,time):
            sound.play(loops=0, maxtime=max)

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

    def set_bossmove_point(pos,speed,miss):
        try:
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
                    boss.move_dir = 0
                    boss.move_speed = 0
        except IndexError as e:
            pass      
        return (boss.pos)
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
        for i in range(0,176,16):
            image = pygame.Surface((16,16), pygame.SRCALPHA)
            image.blit(bullet_image, (0,0), Rect(i,176,16,16))
            a_list.append(image)
        cur_list.append(a_list)
        a_list = []
        for i in range(0,256,32):
            image = pygame.Surface((32,32), pygame.SRCALPHA)
            image.blit(bullet_image, (0,0), Rect(i,400,32,32))
            a_list.append(image)
        cur_list.append(a_list)
        a_list = []
    bullets = cur_list
    cur_list = []
    for i in range(0,128,16):
        image = pygame.Surface((16,16),pygame.SRCALPHA)
        image.blit(item_img, (0,0), Rect(i,0,16,16))
        cur_list.append(image)
    items = cur_list

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
    min_dir = 0
    time_stop = False
    stage_count = 0
    
    
    global stage_line, stage_cline, stage_repeat_count, stage_condition, stage_challenge
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
    bullet_border = Rect(0-bullet_border_wide, 0-bullet_border_wide, WIDTH + bullet_border_wide*2, HEIGHT + bullet_border_wide*2)
    small_border = Rect(0-64, 0-64, WIDTH + 64, HEIGHT + 64)
    bullet_size = (10,6,8,8,6,6,6,9,6,7,7,4,5,15,15,20,10,10,10,20)
    spr = pygame.sprite.Group()
    magic_spr = pygame.sprite.Group()
    player = Player(WIDTH/4,HEIGHT/2,5,500)
    player_group = pygame.sprite.Group(player)
    player_sub = Player_sub(1)
    bomb_group = pygame.sprite.Group()
    bomb_activated = False
    title = Tittle(1)
    ui = UI(1)
    text = TextBox()
    beams_group = pygame.sprite.Group()
    effect_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    

    starting = True
    read_end = False

    clock = pygame.time.Clock()

    # 점수 코어
    global score
    score = 0
    score_setting = (10,10,987650,10,0,0,0,0,0)

    # 보스마다 기본설정
    bkgd = pygame.Surface((540, 360))
    global bkgd_list,boss_background
    bkgd_list = [pygame.Surface((1080, 240)),pygame.Surface((1080, 240)),pygame.Surface((1080, 240))]
    boss_background = pygame.Surface((540,360))
    # 폰트 불러오기
    score_font = pygame.font.Font('Font\SEBANG Gothic Bold.ttf', 50)
    ui_font = pygame.font.Font('Font\SEBANG Gothic Bold.ttf', 20)
    bg_x = [0,0,0,0]
    fps = 60

    spells = [Spell(1,1000,False),
    Spell(2,1000,True),
    Spell(3,1000,False),
    Spell(4,1300,True),
    Spell(5,1300,True)]
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

    def next_challenge(time):
        global stage_count, stage_line, stage_cline, stage_challenge
        if time == stage_count and stage_line == stage_cline:
            stage_count = 0
            stage_line = 0
            stage_challenge += 1

    #################################################
    def title_spawn(val,time,dir=0):
        global stage_count 
        global stage_line # 현재 조건의 라인
        global stage_cline # 검사 중인 라인
        
        # x, y, dir, speed, health, img, hit_cir, num = val
        if time == stage_count and stage_line == stage_cline:
            stage_count = 0
            stage_line += 1
            if val == 1:
                title.title_start("Stage 1","드넓은 초원")
        stage_cline += 1
    # 게임의 배경, 스테이지
    def game_defalt_setting(fun):
        global bgm_num, bkgd, bkgd_list
        ##############################################
        if fun == 1:
            bkgd.blit(bg_image,(0,0),(0,0,540,360))
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

        bkgd = pygame.transform.scale2x(bkgd)
        bkgd_list[0].blit(bkgd,(0,0),(0,0,1080,240))
        bkgd_list[1].blit(bkgd,(0,0),(0,240,1080,240))
        bkgd_list[2].blit(bkgd,(0,0),(0,480,1080,240))

        pygame.mixer.music.stop()
        if fun == 1:
            pygame.mixer.music.load('Music\\BGM\\Unforgettable, the Nostalgic Greenery.wav')
    # 소환하는 적 
    def pokemon_spawn(val,x,y,time,dir=0):
        global stage_count 
        global stage_line # 현재 조건의 라인
        global stage_cline # 검사 중인 라인
        
        # x, y, dir, speed, health, img, hit_cir, num = val
        if time == stage_count and stage_line == stage_cline:
            stage_count = 0
            stage_line += 1
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
        stage_cline += 1
    # 적의 공격타입
    def enemy_attack(num,count,pos,dir,speed):
        pos = calculate_new_xy(pos, speed, dir)
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
        return pos,dir,speed,count

    def boss_spawn(num):
        global boss_background
        
        # 적이동을 위한 값
        boss.move_dir = 0
        boss.move_speed = 0
        boss.move_point = (0,0)
        boss.ready = False
        boss.move_ready = False # 스펠 시작시 움직이는중?
        boss.godmod = False
        boss.dieleft = False
        boss.attack_start = False
        boss.real_appear = False
        if num == 1: 
            boss.pos = (WIDTH,HEIGHT)
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
            boss.num = 1
            boss.spell = [spells[0],spells[1],spells[2],spells[3],spells[4]]
            boss.dies = True
            boss_background.blit(bg_image,(0,0),(540,0,540,360))
            boss_background = pygame.transform.scale2x(boss_background)
            text.started = True
        #boss.appear = True
        boss.appear = True
        boss.rect = boss.image.get_rect(center = (boss.pos))
        
        
    def boss_attack(num,count,pos,dir,speed,ready):
        if num == 1:
            pos = set_bossmove_point((WIDTH-300,HEIGHT/2),130,10)
            if ready:
                if while_time(count,20) and count < 120:
                    add_effect(pos,2,5)
                    s_tan1.play()
                    for i in range(0,360,30):
                        bullet(pos,look_at_player(pos)+i,5,4,5)
                        bullet(pos,look_at_player(pos)+i+5,5,4,5)
                        bullet(pos,look_at_player(pos)+i-5,5,4,5)
                if when_time(count,60):
                    dir , speed = 90 , 2
                if when_time(count,120):
                    dir , speed = 0 , 0
                if when_time(count,180):
                    dir , speed = 270 , 2
                if when_time(count,240):
                    dir , speed = 0 , 0
                    count = 0
        if num == 2:
            pos = set_bossmove_point((WIDTH-300,HEIGHT/2),130,10)
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
            pos = set_bossmove_point((WIDTH-300,HEIGHT/2),130,50)
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
                    dir , speed = 90 , 2
                if when_time(count,120):
                    dir , speed = 0 , 0
                if when_time(count,180):
                    dir , speed = 270 , 2
                if when_time(count,240):
                    dir , speed = 0 , 0
                    count = 0
        if num == 4:
            pos = set_bossmove_point((WIDTH-300,HEIGHT/2,0),130,50)
            if ready:
                if while_time(count,15):
                    rand = randint(0,15)
                    add_effect(pos,2,0)
                    s_tan1.play()
                    for i in range(0,360,15):
                        bullet((pos[0]+randint(-60,60),pos[1]+randint(-60,60)),i+rand,5,randint(2,3),randint(1,7))
        if num == 5:
            pos = set_bossmove_point((WIDTH-300,HEIGHT/2,0),130,50)
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
            

        pos = calculate_new_xy(pos, speed, dir)
        return count,pos,dir,speed,ready
    # 스테이지
    def stage_manager():
        global stage_cline, stage_line, stage_repeat_count, stage_count, stage_condition, stage_challenge
        
        if stage_condition == 1:
            game_defalt_setting(stage_fun)
            pygame.mixer.music.play(-1)
            stage_condition = 2
            #effect.add(Effect(player.pos,1))
        if stage_fun == 1:
            if stage_challenge == 0:
                pokemon_spawn(1,1012,-30,120)
                pokemon_spawn(1,912,-30,0)

                if while_poke_spawn(30,10,2):
                    pokemon_spawn(1,1012,-30,30)
                    pokemon_spawn(1,912,-30,0)
                    end_while_poke_spawn(2,10)

                pokemon_spawn(2,1012,HEIGHT+30,0)
                pokemon_spawn(2,912,HEIGHT+30,0)

                if while_poke_spawn(30,10,2):
                    pokemon_spawn(2,1012,HEIGHT+30,30)
                    pokemon_spawn(2,912,HEIGHT+30,0)
                    end_while_poke_spawn(2,10)

                pokemon_spawn(1,1012,-30,0)
                pokemon_spawn(1,912,-30,0)
                pokemon_spawn(2,1012,HEIGHT+30,0)
                pokemon_spawn(2,912,HEIGHT+30,0)

                if while_poke_spawn(30,10,4):
                    pokemon_spawn(1,1012,-30,30)
                    pokemon_spawn(1,912,-30,0)
                    pokemon_spawn(2,1012,HEIGHT+30,0)
                    pokemon_spawn(2,912,HEIGHT+30,0) 
                    end_while_poke_spawn(4,10)    

                pokemon_spawn(1,1112,-30,60)
                pokemon_spawn(2,1112,HEIGHT+30,10)
                pokemon_spawn(1,1112,-30,10)
                pokemon_spawn(2,1112,HEIGHT+30,10)
                title_spawn(1,240)

                next_challenge(260)
            if stage_challenge == 1:

                if while_poke_spawn(40,10,2):
                    pokemon_spawn(3,WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,40)
                    pokemon_spawn(3,WIDTH+64,stage_repeat_count*HEIGHT/10+20,0)
                    if while_time(stage_repeat_count,3):
                        enemy_group.add(Enemy(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,180,4,10,13,30,4))
                    end_while_poke_spawn(2,10)

                if while_poke_spawn(40,10,2):
                    pokemon_spawn(3,WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,40)
                    pokemon_spawn(3,WIDTH+64,stage_repeat_count*HEIGHT/10+20,0)
                    if while_time(stage_repeat_count,3):
                        enemy_group.add(Enemy(WIDTH+64,stage_repeat_count*HEIGHT/10+20,180,4,10,13,30,4))
                    end_while_poke_spawn(2,10)

                if while_poke_spawn(10,15,2):
                    pokemon_spawn(5,WIDTH,20,10)
                    pokemon_spawn(6,WIDTH,HEIGHT-20,0)
                    end_while_poke_spawn(2,15)

                if while_poke_spawn(40,10,2):
                    pokemon_spawn(3,WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,40)
                    pokemon_spawn(3,WIDTH+64,stage_repeat_count*HEIGHT/10+20,0)
                    if while_time(stage_repeat_count,2):
                        enemy_group.add(Enemy(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,180,4,10,13,30,4))
                        enemy_group.add(Enemy(WIDTH+64,stage_repeat_count*HEIGHT/10+20,180,4,10,13,30,4))
                    end_while_poke_spawn(2,10)
                
                next_challenge(240)
            if stage_challenge == 2:
                if not boss.appear: 
                    boss_spawn(1)
                if boss.health <= 0 and boss.appear:
                    stage_count = 0
                    boss.appear = False
                    next_challenge(0)
            if stage_challenge == 3:
                if while_poke_spawn(10,5,2):
                    pokemon_spawn(5,WIDTH,20,10)
                    pokemon_spawn(6,WIDTH,HEIGHT-20,0)
                    end_while_poke_spawn(2,5)

                pokemon_spawn(4,WIDTH,HEIGHT/2,60)
                pokemon_spawn(4,WIDTH,HEIGHT/2+20,60)
                pokemon_spawn(4,WIDTH,HEIGHT/2+60,60)
                pokemon_spawn(4,WIDTH,HEIGHT/2-20,60)
                pokemon_spawn(4,WIDTH,HEIGHT/2-60,60)

                if while_poke_spawn(20,10,4):
                    pokemon_spawn(1,1012,-30,20)
                    pokemon_spawn(1,912,-30,0)
                    pokemon_spawn(2,1012,HEIGHT+30,0)
                    pokemon_spawn(2,912,HEIGHT+30,0) 
                    end_while_poke_spawn(4,10)

                if while_poke_spawn(10,5,2):
                    pokemon_spawn(5,WIDTH,20,10)
                    pokemon_spawn(6,WIDTH,HEIGHT-20,0)
                    end_while_poke_spawn(2,5)

                pokemon_spawn(4,WIDTH,HEIGHT/2,30)
                pokemon_spawn(4,WIDTH,HEIGHT/2+40,30)
                pokemon_spawn(4,WIDTH,HEIGHT/2-40,0)
                pokemon_spawn(4,WIDTH,HEIGHT/2+80,30)
                pokemon_spawn(4,WIDTH,HEIGHT/2,0)
                pokemon_spawn(4,WIDTH,HEIGHT/2-80,0)
                next_challenge(360)
            if stage_challenge == 4:
                pokemon_spawn(7,WIDTH-120,-30,60,90)
                pokemon_spawn(7,WIDTH-120,-30,60,90)
                pokemon_spawn(7,WIDTH-120,-30,60,90)
                pokemon_spawn(7,WIDTH-120,-30,120,90)
                pokemon_spawn(7,WIDTH-120,HEIGHT+30,60,-90)
                pokemon_spawn(7,WIDTH-120,-30,60,90)
                pokemon_spawn(7,WIDTH-120,HEIGHT+30,60,-90)
                pokemon_spawn(7,WIDTH-120,-30,60,90)
                pokemon_spawn(7,WIDTH-120,HEIGHT+30,60,-90)

                if while_poke_spawn(40,10,2):
                    pokemon_spawn(3,WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,40)
                    pokemon_spawn(3,WIDTH+64,stage_repeat_count*HEIGHT/10+20,0)
                    if while_time(stage_repeat_count,3):
                        enemy_group.add(Enemy(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,180,4,10,13,30,4))
                    if while_time(stage_repeat_count,2):
                        enemy_group.add(Enemy(WIDTH-120,HEIGHT+30,-90,4,7,15,30,7))
                    end_while_poke_spawn(2,10)
                if while_poke_spawn(40,10,2):
                    pokemon_spawn(3,WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20,40)
                    pokemon_spawn(3,WIDTH+64,stage_repeat_count*HEIGHT/10+20,0)
                    if while_time(stage_repeat_count,3):
                        enemy_group.add(Enemy(WIDTH+64,stage_repeat_count*HEIGHT/10+20,180,4,10,13,30,4))
                    if while_time(stage_repeat_count,2):
                        enemy_group.add(Enemy(WIDTH-120,-30,90,4,7,15,30,7))
                    end_while_poke_spawn(2,10)
                next_challenge(360)
            if stage_challenge == 5:
                if not boss.appear: 
                    boss_spawn(2)
                if boss.health <= 0 and boss.appear:
                    stage_count = 0
                    next_challenge(0)



            stage_cline = 0
    ################################################# 

    while play:
        # 60 프레임
        clock.tick(fps)
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
                    if ev.key == pygame.K_z and text.started and text.count > 50:
                        text.next_text()
                    if ev.key == pygame.K_x and player.mp > 0 and not bomb_activated:
                        bomb_group.add(Bomb(player.pos,1))
                        player.mp -= 1      
                        bomb_activated = True
            # 탄에 박았는가
            hit_list = pygame.sprite.spritecollide(player, spr, not player.godmod, pygame.sprite.collide_circle)
            beam_collide = pygame.sprite.groupcollide(beams_group, enemy_group, False, False, pygame.sprite.collide_circle)
            if beam_collide.items():
                for beam, enemy in beam_collide.items():
                    for i in range(0,len(enemy)):
                        if beam.can_damage: 
                            enemy[i].health -= beam.damage
                            beam.can_damage = False
            if boss.appear: boss_collide = pygame.sprite.spritecollide(boss, beams_group, False, pygame.sprite.collide_circle)
        
            if bomb_activated:
                beam_collide = pygame.sprite.groupcollide(bomb_group, enemy_group, False, False, pygame.sprite.collide_circle)
                if beam_collide.items():
                    for beam, enemy in beam_collide.items():
                        for i in range(0,len(enemy)): 
                            enemy[i].health -= 1
                if boss.appear: boss_collide = pygame.sprite.spritecollide(boss, bomb_group, False, pygame.sprite.collide_circle)
                beam_collide = pygame.sprite.groupcollide(bomb_group, spr, False, False, pygame.sprite.collide_circle)
                if beam_collide.items():
                    for beam, enemy in beam_collide.items():
                        for i in range(0,len(enemy)): 
                            item_group.add(Item(enemy[i].pos,0))
                            enemy[i].kill()
                if not bomb_group:
                    bomb_activated = False
            # 연산 업데이트
            if not pause:      
                if len(magic_spr.sprites()) != 0:magic_spr.update(screen)    
                if boss.appear and boss.health <= 0: spr.empty()              
                spr.update(screen)
                if not time_stop:
                    beams_group.update()                            
                    player_group.update(hit_list)
                    enemy_group.update()
                    item_group.update()
                    if boss.appear: boss_group.update(boss_collide)
                    effect_group.update()
                    player_sub.update()
                    bomb_group.update()
                    if text.started: text.update()
                    stage_manager()
                    frame_count += 1
                    stage_count += 1
                    min_dir += 0.2
                    bg_x[0] -= 1
                    bg_x[1] -= 2
                    bg_x[2] -= 3
                    bg_x[3] -= 3
                    rotated_sprite = pygame.transform.rotate(player_slow_img, math.degrees(frame_count/20))
                    rect = rotated_sprite.get_rect(center = (round(player.pos[0]), round(player.pos[1])))
                
            # 그리기 시작
            screen.fill((0,0,0))
            #배경 스크롤
            for image in bkgd_list:
                rel_x = bg_x[bkgd_list.index(image)] % WIDTH
                screen.blit(image, (rel_x - WIDTH,0+240*bkgd_list.index(image)))
                if rel_x < WIDTH:
                    screen.blit(image,(rel_x,0+240*bkgd_list.index(image)))
            if boss.appear and boss.spell[0].spellcard:
                rel_x = bg_x[3] % WIDTH
                screen.blit(boss_background, (rel_x - WIDTH,0))
                if rel_x < WIDTH:
                    screen.blit(boss_background,(rel_x,0))
            # 점수 표시
            bomb_group.draw(screen)
            score_text = score_font.render(str(score).zfill(10), True, (255,255,255))
            screen.blit(score_text,(WIDTH-score_text.get_rect().width,0))
            
            # 원형 체력바 그리기
            if starting and not read_end: 
                drawArc(screen, (0,0, 0), player.pos, 112, 15, 360*100)
                drawArc(screen, health_color(player.health/500), player.pos, 110, 10, 360*player.health/500)
            if boss.attack_start and boss.health > 0:
                try:
                    drawArc(screen, (0, 0, 0), boss.pos, 112, 15, 360*100)
                    drawArc(screen, health_color(boss.health/boss.max_health), boss.pos, 110, 10, 360*boss.health/boss.max_health)
                except:
                    drawArc(screen, (0, 0, 0), boss.pos, 112, 15, 360*100)
                    drawArc(screen, (0,0,0), boss.pos, 110, 10, 1)                   



            item_group.draw(screen)
            magic_spr.draw(screen)      
            beams_group.draw(screen)

            player_group.draw(screen) 
            player_sub.draw()
            enemy_group.draw(screen)
            
            if not starting or read_end: enemy_group.draw(screen)
            if boss.appear: boss_group.draw(screen)
            effect_group.draw(screen)
            spr.draw(screen)

            # 피격점 표시
            pygame.draw.circle(screen, (200,100,100), get_new_pos(player.pos), 8)
            pygame.draw.circle(screen, (255,255,255), get_new_pos(player.pos), 7)

            title.draw()
            text.draw()
            ui.draw()
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
                        screen.blit(menu_img,(int(WIDTH/2-120),int(HEIGHT/2-60+128*i-128*curser)),(0,320+64*i,288,64))
                        difficulty = curser
                if menu_mod == 3:
                    curser_max = 3
                    text_box = ["화면모드","음악","효과음","플레이어"]

                    text_box[0] = "화면모드    창모드" if full_on == 0 else "화면모드    전체화면"
                    text_box[1] = "음악   " + str(mmusic_volume)
                    text_box[2] = "효과음  " + str(msfx_volume)
                    for i in range(0,4):
                        text_color = (255,0,255) if i == curser else (0,0,255)
                        text = score_font.render(text_box[i], True, text_color)
                        screen.blit(text,(200,200+80*i))
            pygame.display.flip()
        
        if full_on != cur_full_mod:
            if full_on:
                try:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN|pygame.SCALED)
                except AttributeError:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
            cur_full_mod = full_on

    pygame.quit()
    exit()

if __name__ == "__main__":
    play_game()

