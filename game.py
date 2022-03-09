from cv2 import circle
import pygame, math
from random import randint, uniform, choice
from pygame.locals import *
import cv2
import numpy
import time
from game_sprites import *
from main_func import *
from start import *


# 게임에 핵심적인 기능만 주석을 넣었습니다 ##
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
pygame.mixer = audio_mixer

# 해상도
def play_game():
    
    global WIDTH, HEIGHT, screen,prev_time,bkgd_list,boss_background, mmusic_volume, msfx_volume,music_volume, sfx_volume, game_restart, score, full_on
    music_and_sfx_volume(music_volume,sfx_volume)
    start_fun = 0
    practicing = False
    continued = 0
    global bkgd, time_stop
    global stage_count, boss_group, screen_shake_count, pause, add_dam, drilling,cur_count,game_clear
    # 초기 설정
    enemy_group = pygame.sprite.Group()
    boss = Boss_Enemy(-99,-99)
    boss_group = pygame.sprite.Group(boss)
    play = True
    cur_full_mod = False
    pause = False
    frame_count = 0
    cur_count = 0
    time_stop = False
    stage_count = 0
    screen_shake_count = 0
    add_dam = 0
    drilling = False
    game_clear = False   
    global character
    curser = 0
    curser_max = 4
    select_mod = 0
    menu_mod = []
    character = 0
    cur_screen = 0
    global stage_line, stage_cline, stage_repeat_count, stage_condition, stage_challenge, stage_fun, stage_end
    stage_fun = 0
    stage_line = 0
    stage_cline = 0
    stage_repeat_count = 0
    stage_condition = 1
    stage_challenge = 0
    stage_end = 0
    skill_activating = []
    # 게임 시작전 메뉴 변수들
    spr = pygame.sprite.Group()
    magic_spr = pygame.sprite.Group()
    player = Player(-125,-125,5,500)
    player_group = pygame.sprite.Group(player)
    player_hitbox = Player_hit()
    player_sub = Player_sub(1)
    skillobj_group = pygame.sprite.Group()
    title = Tittle(1)
    ui = UI(1)
    under_ui = Under_PI(player)
    text = TextBox()
    beams_group = pygame.sprite.Group()
    effect_group = pygame.sprite.Group()
    item_group = pygame.sprite.Group()
    
    starting = True
    read_end = False

    spells = [Spell(1,700,False),Spell(2,1000,True,3,"뭐든지 가르는","메지컬리프"),Spell(3,1000,False),Spell(4,1000,False),\
    Spell(5,1300,True,3,"네잎클로버가 담긴","리프스톰"),Spell(6,1300,False),Spell(7,1300,True,2,"큰 물방울","물놀이"),Spell(8,1300,False),Spell(9,1800,True,2,"안에 뭔가를 넣은","거품"),Spell(10,1300,False),\
        Spell(11,2800,True,2,"잔잔해지는","물의파동"),Spell(12,2000,True,2,"왕의 소나기","거품광선"),Spell(13,1000,False),Spell(14,1000,False),Spell(15,1000,False),Spell(16,2000,True,4,"꽃도 춤추게 하는","염동력"),Spell(17,1000,False),Spell(18,1800,True,0,"노래폭력","에코보이스"),\
            Spell(19,1000,False),Spell(20,1600,True,4,"그래도 방어는 필수","인파이트"),Spell(21,1500,True,0,"주위에 맴도는","옛노래"),Spell(22,1000,False),Spell(23,1000,False),Spell(24,1000,False),\
                Spell(25,1700,True,1,"성스러운 입자","성스러운칼"),Spell(26,1100,False),Spell(27,1500,True,1,"베는데 1초","인파이트"),Spell(28,800,False),Spell(29,1800,True,1,"뭐든지 꿰뚫는 창","두세번치기"),Spell(30,1500,True,1,"모든 경험이 깆든","신비의칼"),\
                    Spell(31,1000,False),Spell(32,1000,False),Spell(33,1200,False),Spell(34,1600,True,4,"불에 뜨겁게 달궈진","염동력"),Spell(35,1200,False),Spell(36,1800,True,1,"차분하고 뒤엉킨","V제너레이트"),\
                        Spell(37,1200,False),Spell(38,1500,True,1,"주위의 도움으로","플레어드라이브"),Spell(39,1500,True,0,"V 모양으로","파괴광선"),\
                            Spell(40,1200,False),Spell(41,1800,True,4,"멀리서만 아름다운","신통력"),Spell(42,1200,False),Spell(43,2000,True,9,"용이 부르짖는다","용의파동"),\
                                Spell(44,1200,False),Spell(45,1700,True,1,"지나간 자리엔 남지않는","쾌청"),Spell(46,1200,False),Spell(47,2400,True,1,"도피하기엔 틈이없다","푸른불꽃"),Spell(48,5000,True,1,"크로스플레임","크로스플레임")]

    player.skill_list.append(Skill(3,5,"저리가람","바람일으키기",10,60,30))
    player.skill_list.append(Skill(0,7,"Press C key!","몸부림",30,60,10))
    player.skill_list.append(Skill(0,7,"Press C key!","몸부림",30,60,10))

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
            title.count = 0
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
                title.title_start("Stage 6","화가 존재하는 현실")
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
            if val == 1:bkgd_list.append(Back_Ground(bg_image,(540,0,540,120),1,3,0,True))
            if val == 2:bkgd_list.append(Back_Ground(bg_image,(540,240,540,120),3,4,240,True))
            if val == 3:bkgd_list.append(Back_Ground(bg_image,(1080,0,540,290),2,5,0,True)) 
            if val == 8:bkgd_list.append(Back_Ground(bg_image,(1080//2,972//2,1080//2,468//2),2,8,126,True))
            if val == 9:bkgd_list.append(Back_Ground(bg_image,(1080//2,720//2,1080//2,252//2),1,9,0,True))
        stage_cline += 1
    # 게임의 배경, 스테이지
    def game_defalt_setting(fun): # 게임 스테이지 배경 정하기
        global bgm_num, bkgd_list,skill_activating
        bkgd_list = []
        ##############################################
        if fun == 1:
            bkgd_list.append(Back_Ground(bg_image,(0,0,1080,240),1,0,0))
            bkgd_list.append(Back_Ground(bg_image,(0,240,1080,240),2,1,240))
            bkgd_list.append(Back_Ground(bg_image,(0,480,1080,240),3,2,480))
        if fun == 2:
            bkgd_list.append(Back_Ground(bg_image,(0,360,540,232),2,6,0))
            bkgd_list.append(Back_Ground(bg_image,(0,592,540,128),3,7,232))
        if fun == 3:
            bkgd_list.append(Back_Ground(bg_image,(0,720,540,126),5,8,0))
            bkgd_list.append(Back_Ground(bg_image,(540,776,540,304),7,9,118))
        if fun == 4:
            bkgd_list.append(Back_Ground(bg_image,(0,1080,720,360),10,10))
            bkgd_list.append(Back_Ground(bg_image,(540,1080,540,360),8,11))
        if fun == 5:
            bkgd_list.append(Back_Ground(bg_image,(0,1440,540,72),7,8,0))
            bkgd_list.append(Back_Ground(bg_image,(0,1440+72,540,72),5,8,72))
            bkgd_list.append(Back_Ground(bg_image,(0,1440+72*2,540,72),3,8,72*2))
            bkgd_list.append(Back_Ground(bg_image,(0,1440+72*3,540,72),5,8,72*3))
            bkgd_list.append(Back_Ground(bg_image,(0,1440+72*4,540,72),7,8,72*4))
        if fun == 6:
            bkgd_list.append(Back_Ground(bg_image,(0,1800,540,360),5,8,0))
            bkgd_list.append(Back_Ground(bg_image,(540,2070,540,90),3,8,280))

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
        val, item = math.trunc(val), (val*10)%10
        # x, y, dir, speed, health, img, hit_cir, num = val
        if (time == stage_count and stage_line == stage_cline) or simple:
            if not simple:
                stage_count = 0
                stage_line += 1
            if stage_fun == 1:
                if val == 1:
                    enemy_group.add(Enemy(x,y,180,4,3,11,30,val,Skill(1,0,"평범하기 그지없는","몸통박치기",10,40,10),item))  
                if val == 2:
                    enemy_group.add(Enemy(x,y,180,4,3,12,30,val,Skill(2,5,"얍삽한","쪼기",10,40,10),item))  
                if val == 3:
                    enemy_group.add(Enemy(x,y,180,3,6,14,30,val,Skill(2,5,"얍삽한","쪼기",10,40,10),item))
                if val == 4:
                    enemy_group.add(Enemy(x,y,180,4,10,13,30,val,Skill(3,5,"저리가람","바람일으키기",10,60,30),item))
                if val == 5:
                    enemy_group.add(Enemy(x,y,135,6,5,11,30,val,Skill(1,0,"평범하기 그지없는","몸통박치기",10,40,10),item))
                if val == 6:
                    enemy_group.add(Enemy(x,y,225,6,5,12,30,val,Skill(2,5,"얍삽한","쪼기",10,40,10),item))
                if val == 7:
                    enemy_group.add(Enemy(x,y,dir,4,7,15,30,val,Skill(4,8,"보이지 않는 장막","실뿜기",5,5,30),item))
            ##################### 2 스테이지 #################
            if stage_fun == 2:
                if val == 8:
                    enemy_group.add(Enemy(x,y,dir,speed,7,19,30,val,Skill(5,2,"조금 위협적인","물놀이",10,60,15),item))
                if val == 9:
                    enemy_group.add(Enemy(x,y,180,5,240,17,40,val,Skill(6,2,"아마도 모든걸 베는","셸블레이드",20,60,50),item))
                if val == 10:
                    enemy_group.add(Enemy(x,y,180,4,20,18,30,val,Skill(7,2,"모양은 원모양","거품발사",20,50,30),item))
                if val == 11:
                    enemy_group.add(Enemy(x,y,180+randint(-10,10),4,20,16,30,val,Skill(8,2,"불끌때 제법인","물대포",5,90,80),item))
            ##################### 3 스테이지 $$$$$$$$$$$$$$$$$
            if stage_fun == 3:
                if val == 12:
                    enemy_group.add(Enemy(x,y,180,speed,30,21,30,val,Skill(9,3,"어떻게 보면 잔인한","씨앗심기",3,120,30),item))    
                if val == 13:
                    enemy_group.add(Enemy(x,y,dir,speed,80,22,40,val,Skill(10,0,"충격 흡수량 최대","코튼가드",10,5,50),item))   
                if val == 14:
                    enemy_group.add(Enemy(x,y,dir,speed,100,23,40,val,Skill(11,8,"뭔 이상한거에만 효과있는","마비가루",20,60,20),item))   
                if val == 15:
                    enemy_group.add(Enemy(x,y,dir,speed,30,24,40,val,Skill(12,9,"날카로운 확인사살","독침",5,90,80),item)) 
                if val == 16:
                    enemy_group.add(Enemy(x,y,dir,speed,120,25,40,val,Skill(13,3,"완벽을 추구하는","HP필드",5,180,100),item))
            if stage_fun == 4:
                if val == 17:
                    enemy_group.add(Enemy(x,y,dir,speed,15,30,40,val,Skill(14,4,"소음따위는 안들린다","명상",5,240,20),item))
                if val == 18:
                    enemy_group.add(Enemy(x,y,dir,speed,100,27,40,val,Skill(15,4,"저격한다!","사이코리모트",10,500,80),item))
                if val == 19:
                    enemy_group.add(Enemy(x,y,dir,speed,250,29,50,val,Skill(16,6,"마비는 안걸리는 안전한","방전",10,300,50),item))
                if val == 20:
                    enemy_group.add(Enemy(x,y,dir,speed,150,28,50,val,Skill(17,10,"경계를 뚫는?!","땅굴파기",10,120,80),item))               
            if stage_fun == 5:
                if val == 21:
                    enemy_group.add(Enemy(x,y,dir,speed,15,31,30,val,Skill(18,5,"물리를 행사하는","흑안개",30,60*20,10),item))
                if val == 22:
                    enemy_group.add(Enemy(x,y,dir,speed,210,34,60,val,Skill(19,4,"전부 멀리 가버려!","사이코키네시스",5,5,50),item))
                if val == 23:
                    enemy_group.add(Enemy(x,y,dir,speed,300,33,30,val,Skill(20,1,"눈앞이 불지옥","화염방사",5,240,80),item))        
                if val == 24:
                    enemy_group.add(Enemy(x,y,dir,speed,100,35,30,val,Skill(21,10,"불안전지대","스텔스록",10,300,50),item))
                if val == 25:
                    enemy_group.add(Enemy(x,y,dir,speed,100,32,30,val,Skill(23,1,"불꽃펀치","불꽃펀치",3,60,80),item))
                if val == 26:
                    enemy_group.add(Enemy(x,y,dir,speed,20,36,30,val,Skill(22,0,"상대를 속이진 않는","속이다",10,60,5),item))      
            if stage_fun == 6:
                if val == 27:
                    enemy_group.add(Enemy(x,y,dir,speed,30,37,30,val,Skill(24,0,"아마도 누구든지 배울 수 있는","파괴광선",1,600,200),item))       
                if val == 28:
                    enemy_group.add(Enemy(x,y,dir,speed,450,38,30,val,Skill(10,0,"충격 흡수량 최대","코튼가드",10,5,50),item))   
                if val == 29:
                    enemy_group.add(Enemy(x,y,dir,speed,300,39,30,val,Skill(24,0,"아마도 누구든지 배울 수 있는","파괴광선",1,600,200),item))   
                if val == 30:
                    enemy_group.add(Enemy(x,y,dir,speed,200,40,30,val,Skill(10,0,"충격 흡수량 최대","코튼가드",10,5,50),item))              
        
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
                    bullet_effect(s_tan1,5,pos)
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
                    for i in range(0,6):
                        bullet(pos,look_at_player(pos)+randint(-5,5),randfloat(4,6),3,3)
                    speed = 0
                if when_time(count,180):
                    speed = 4
            if num == 11:
                if when_time(count,90):
                    speed = 0
                    s_lazer1.play()
                    list[0] = look_at_player(pos)
                if when_time(count,150):
                    speed = 5   
                if while_time(count,3) and big_small(count,90,150):
                    bullet_effect(0,3,pos)
                    bullet(pos,list[0],7,0,3)
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
                if while_time(count,6):
                    for i in range(60,330,30):
                        bullet(calculate_new_xy(pos,40,-i-180),i+180,8,4,0) 
                if while_time(count,20):
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
                        rand = (randint(-50,50),randint(-50,50))
                        bullet_effect(s_tan1,1,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos),8,3,1)
                    elif count > 210:
                        rand = (randint(-50,50),randint(-50,50))
                        bullet_effect(s_tan1,1,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos),9,15,1)
                    elif count > 150:
                        rand = (randint(-50,50),randint(-50,50))
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
                        bullet(pos,look_at_player(pos)+6,i,5,7)   
                        bullet(pos,look_at_player(pos)-6,i,5,7)   
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
        if num == 0:
            boss.pos = (WIDTH+64,HEIGHT)
            boss.radius = 0
            boss.image.blit(pokemons[1],(0,0))         
            boss.num = 1
            boss.spell = []
            boss.dies = False
            boss.attack_start = True            
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
            boss.spell = [spells[3],spells[1],spells[2],spells[4]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(0,0,540,360))
            text.started = True
        if num == 3: 
            boss.pos = (WIDTH+64,120)
            boss.radius = 40
            boss.image.blit(pokemons[2],(0,0))         
            boss.num = 3
            boss.spell = [spells[5],spells[6]]
            boss.dies = True
            boss.attack_start = True
            boss_background.blit(bg2_image,(0,0),(0,360,540,360))
        if num == 4: 
            boss.pos = (WIDTH+64,HEIGHT+64)
            boss.radius = 40
            boss.image.blit(pokemons[3],(0,0))         
            boss.num = 4
            boss.spell = [spells[7],spells[8],spells[9],spells[10],spells[11]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(0,360,540,360))
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
            boss_background.blit(bg2_image,(0,0),(0,720,540,360))
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
            boss_background.blit(bg2_image,(0,0),(540,0,540,360))
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
            boss.spell = [spells[32],spells[33],spells[34],spells[35],spells[36],spells[37],spells[38]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(540,360,540,360))
            text.started = True         
        if num == 11: 
            boss.pos = (WIDTH+64,HEIGHT+64)
            boss.radius = 60
            boss.image.blit(pokemons[9],(0,0))         
            boss.num = num
            boss.spell = [spells[39],spells[40],spells[41],spells[42],spells[43],spells[44],spells[45],spells[46],spells[47]]
            boss.dies = True
            boss_background.blit(bg2_image,(0,0),(540,720,540,360))
            text.started = True          
        boss.real_max_health = 0
        boss.radius /= 2
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
                    if while_time(count,40) and count < 120:
                        add_effect(pos,2,5)
                        s_tan1.play()
                        for i in range(0,360,30):
                            bullet(pos,look_at_player(pos)+i,5,4,5)
                            bullet(pos,look_at_player(pos)+i+5,5,4,5)
                            bullet(pos,look_at_player(pos)+i-5,5,4,5)
                    if while_time(count,180):
                        set_go_boss(3,choice([-90,90]),60)
                        count = 0
            if num == 2:
                pos = set_bossmove_point((WIDTH-150,HEIGHT/2),120,3)
                if ready:
                    if while_time(count,30):
                        rand = randint(0,15)
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,15):
                            bullet(pos,i+rand,4,3,2)
                    if while_time(count+1,180):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(1,20):
                            bullet(pos,look_at_player(pos),i/2,5,5)   
                    if while_time(count+20,180):                  
                        bullet_effect(s_tan1,5,pos)
                        for i in range(1,20):
                            bullet(pos,look_at_player(pos),i/2,5,5)
                    if while_time(count+40,180):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(1,20):
                            bullet(pos,look_at_player(pos),i/2,5,5)          
            if num == 3:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2),120,3)
                if ready:
                    if while_time(count,20) and count < 120:
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,30):
                            bullet(pos,look_at_player(pos)+i,5,4,5)
                            bullet(pos,look_at_player(pos)+i+5,5,4,5)
                            bullet(pos,look_at_player(pos)+i-5,5,4,5)
                    if when_time(count,120):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,20):
                            bullet(pos,i,5,3,5)
                        set_go_boss(3,choice([-90,90]),60)
                    if when_time(count,180):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(1,10):
                            bullet(pos,look_at_player(pos),i/2,5,5)  
                        count = 0
            if num == 4:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2),120,3)
                if ready:
                    if while_time(count,20) and count < 120:
                        add_effect(pos,2,5)
                        s_tan1.play()
                        for i in range(0,360,30):
                            bullet(pos,look_at_player(pos)+i,5,4,5)
                            bullet(pos,look_at_player(pos)+i+5,5,4,5)
                            bullet(pos,look_at_player(pos)+i-5,5,4,5)
                    if while_time(count,120):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,20):
                            bullet(pos,i,5,3,5)
                        set_go_boss(3,choice([-90,90]),60)
                    if when_time(count,180):
                        count = 0
            if num == 5:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,4):
                        bullet_effect(s_tan2,0,0,True)
                        bullet(pos,count*2,4,4,5)
                        bullet(pos,count*2+180,4,4,5)
                    if while_time(count,60) and count > 180:
                        dir = look_at_player(pos)
                        s_tan2.play()
                        add_effect(pos,2,5)
                        bullet((pos[0]+15,pos[1]),dir,2,15,5)
                        bullet((pos[0]-15,pos[1]),dir,2,15,5)
                        bullet((pos[0],pos[1]+15),dir,2,15,5)
                        bullet((pos[0],pos[1]-15),dir,2,15,5)
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
                    if when_time(count,180):
                        set_go_boss(3,randint(0,360),60)
                    if while_time(count,20) and big_small(count,180,280):
                        bullet_effect(s_tan1,3,pos)
                        for i in range(0,360,45):
                            bullet(pos,i,5,9,4)
                    if when_time(count,300):
                        count = 0
            if num == 7:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,40):
                        bullet_effect(s_tan1,4,pos)
                        for i in range(0,360,90):
                            bullet(pos,i,3,15,3,1.1)  
                    if when_time(count,120):
                        set_go_boss(1,randint(0,360),60)
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
                        for i in range(0,360,10):
                            bullet(pos,i+rand,5,4,4)
                    if while_time(count,50):
                        set_go_boss(1,randint(0,360),50) 
            if num == 11:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,20) and count < 130:
                        bullet_effect(s_tan1,3,pos)
                        for i in range(0,360,24):
                            bullet((WIDTH-randint(4,100),i-randint(0,20)),180,5,2,3,2)
                    if when_time(count,240):
                        set_go_boss(2,choice([-30,30,-150,150]),50)   
                        count = 0
            if num == 12:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,5) and count<180:
                        bullet_effect(s_tan1,3,pos)
                        bullet(pos,180+randint(-10,10),7,19,3,2.1)
                    if while_time(count,360):
                        set_go_boss(3,look_at_player(pos)+180,60)   
                        count = 0                           
            if num == 13:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,30):
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,6):
                            bullet(pos,i+randint(-3,3),4,3,5)
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
                            bullet(pos,i,8,9,5)
                    if while_time(count+4,8) and count < 60:
                        bullet_effect(s_tan1,5,pos)
                        for i in range(0,360,10):
                            bullet(pos,i+5,8,4,5)
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
                        for i in range(0,360,6):
                            bullet(rand[0],count+i,6,10,rand[1],9,[count+i])        
            if num == 18:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if when_time(count,60):
                        magic_bullet((WIDTH,pos[1]),180,18,1)
                        magic_bullet((WIDTH+15,pos[1]+50),180,18,1)
                        magic_bullet((WIDTH+20,pos[1]-50),180,18,1)
                        magic_bullet((WIDTH+25,pos[1]+100),180,18,1)
                        magic_bullet((WIDTH+30,pos[1]-100),180,18,1)
                    if count == 180:
                        s_ch0.play()
                    if count == 240:
                        s_kira0.play()
                        add_effect(pos,5)
                        count = 0
                    if while_time(count,120):
                        set_go_boss(3,-look_at_player(pos),30)
                        bullet_effect(s_kira1,2,pos)
                        bullet(pos,look_at_player(pos),4,15,2)
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
                        magic_bullet(pos,rand,5,2)  
                        magic_bullet(pos,rand+180,5,2)                        
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
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub,True))
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub-90,5,1,4,0.1)
                    if while_time(count,3) and count> 120:
                        sub = count * 3.2 + 45
                        for i in range(1,6):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub,True))
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub-90,5,1,4,0.1)
                    if count == 240:
                        count = 0
                    if while_time(count,120):
                        set_go_boss(5,-look_at_player(pos),30)     
            if num == 25:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,3) and count< 90:
                        sub = -(count * 3.2 + 45 )
                        for i in range(4,7):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,60*i,sub,True))
                            bullet(calculate_new_xy(pos,60*i,sub,True),look_at_player(boss.pos),1,1,4,11.4)
                        bullet_effect(s_tan1,0,calculate_new_xy(pos,60*3,sub,True))
                        bullet(calculate_new_xy(pos,60*3,sub,True),look_at_player(boss.pos)+30,5,5,3)
                        bullet(calculate_new_xy(pos,60*3,sub,True),look_at_player(boss.pos)-30,5,5,3)
                    if count == 90:
                        bullet_effect(s_kira0,0,0,True)
                    if while_time(count,120):
                        count = 0
                        set_go_boss(5,choice([-90,90]),30)          
            if num == 26:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:
                    if while_time(count,20):
                        bullet_effect(s_tan1,7,get_new_pos(pos,0,50))
                        bullet_effect(s_tan1,7,get_new_pos(pos,0,-50))
                        bullet(get_new_pos(pos,0,50),180,8,15,7)
                        bullet(get_new_pos(pos,-30,50),180,8,18,7)
                        bullet(get_new_pos(pos,-60,50),180,8,17,7)
                        bullet(get_new_pos(pos,-90,50),180,8,5,7)
                        bullet(get_new_pos(pos,0,-50),180,8,15,7)
                        bullet(get_new_pos(pos,-30,-50),180,8,18,7)
                        bullet(get_new_pos(pos,-60,-50),180,8,17,7)
                        bullet(get_new_pos(pos,-90,-50),180,8,5,7)
                    if while_time(count,10):
                        bullet_effect(s_tan1,0,pos)
                        bullet(pos,look_at_player(pos),5,17,0)
                    if while_time(count,60):
                        count = 0
                        set_go_boss(5,-look_at_point(pos,(pos[0],player.pos[1]))+randint(-20,20),60)         
            if num == 27:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                boss.box_disable = True
                if ready:
                    if while_time(count,2) and boss.move_speed == 20:
                        rand = (randint(-50,50),randint(-50,50))
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
                        if pos[0] >= WIDTH-100:
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
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub+90,4,1,4)
                            bullet(calculate_new_xy(pos,60*i,sub,True),-sub+135,4,1,4)
                    if while_time(count,2) and big_small(count,60,80):
                        rand = (randint(-30,30),randint(-30,30))
                        bullet_effect(s_tan1,4,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos)+randint(-5,5),7,17,7)
                        rand = (randint(-35,35),randint(-35,35))
                        bullet_effect(s_tan1,4,get_new_pos(pos,rand[0],rand[1]))
                        bullet(get_new_pos(pos,rand[0],rand[1]),look_at_player(pos)+randint(-5,5),7,17,7)
                        rand = (randint(-40,40),randint(-40,40))
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
                    if while_time(count,4):
                        bullet_effect(s_tan1,1,pos)  
                        for i in range(0,360,45):
                            bullet(pos,count**1.2+i,5,3,1)
                    if while_time(count,60): 
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
                            magic_bullet(calculate_new_xy(pos,130,-look_at_player(pos)-i+180),-i,0,5)     
                            magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)+20+i+180),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,100,-look_at_player(pos)-20+i+180),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)+45+i+180),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,80,-look_at_player(pos)-45+i+180),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)+85+i+180),-i,0,5) 
                            magic_bullet(calculate_new_xy(pos,75,-look_at_player(pos)-85+i+180),-i,0,5) 
                    if while_time(count,5) and big_small(count,510,600): 
                        bullet_effect(s_tan1,1,pos)  
                        for i in range(0,360,10):
                            bullet(pos,look_at_player(pos)+i,5,4,7)  
                            bullet(pos,look_at_player(pos)+i,6,18,1)      
                                          
                    if when_time(count,600):
                        count = 0
            if num == 37:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:            
                    if count > 120:
                        boss.list[0] += 2
                    if while_time(count,4):
                        for i in range(0,360,30):
                            bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-boss.list[0]+i,True))  
                            bullet(calculate_new_xy(pos,100,-boss.list[0]+i,True),boss.list[0]+40+i,5,10,randint(6,7))   
                            bullet(calculate_new_xy(pos,100,-boss.list[0]+i,True),boss.list[0]-40+i,5,10,randint(6,7))
                    if while_time(count,60) and count > 120:
                        set_go_boss(3,choice([70,110,-70,-110]),10)    
            if num == 38:
                pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
                if ready:  
                    if while_time(count+120,180):
                        bullet_effect(s_tan1,1,pos)
                        for i in range(0,360,6):
                            bullet(pos,i+count,2,3,1,22)
                        set_go_boss(1,randint(0,359),40) 
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
                if while_time(count,20):
                    rand = get_new_pos(boss.pos,randint(-100,100),randint(-100,100))
                    bullet_effect(s_tan1,1,rand)
                    for i in range(0,360,12):
                        bullet(rand,i,2.5,3,7)
                if while_time(count+20,40):
                    rand = get_new_pos(boss.pos,randint(-100,100),randint(-100,100))
                    bullet_effect(s_tan1,1,rand)
                    for i in range(0,360,12):
                        bullet(rand,i,3,3,1)
                if when_time(count,100):
                    add_effect(pos,8)
                    s_ch0.play()
                    boss.fire_field = [300,120]  
                if when_time(count,100+60*5):
                    boss.fire_field = [-300,120] 
                    count = 0                              
        if num == 41:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready: 
                if while_time(count,5) and count < 150:
                    for i in range(0,360,45):
                        bullet_effect(s_tan1,1,calculate_new_xy(pos,count*3+60,-i-count*4.7,True))
                        bullet(calculate_new_xy(pos,count*3+60,-i-count*4.7,True),i+count*4.4,0,2,1)
                        bullet_effect(s_tan1,2,calculate_new_xy(pos,-count*2-60,-i-count*4.7,True))
                        bullet(calculate_new_xy(pos,-count*2-60,-i-count*4.7,True),i+count*4.4,0,7,2,0.2)
                if when_time(count,150):
                    add_effect(pos,8)
                    boss.fire_field = [300,30]
                if when_time(count,270):
                    boss.fire_field = [-300,30]  
                if when_time(count,270):
                    set_go_boss(2,randint(0,360),60)
                if when_time(count,330):
                    count = 0
                if while_time(count,60):
                    for i in range(0,360,5):
                        bullet(pos,count*1.7+i,8,4,4,9,[count*1.7+i])
        if num == 42:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready: 
                if while_time(count,20):
                    rand = randint(0,30)
                    bullet_effect(s_tan1,1,pos)
                    for i in range(0,360,6):
                        bullet(get_new_pos(pos,randint(-50,50),randint(-50,50)),i,2,2,1)
                if while_time(count+120,180):
                    add_effect(pos,8)
                    boss.fire_field = [300,60]        
                if while_time(count,180):
                    add_effect(pos,8)
                    boss.fire_field = [-300,60]   
        if num == 43:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready: 
                if while_time(count,5):
                    for i in range(0,360,45):
                        bullet_effect(s_tan1,3,calculate_new_xy(pos,200,-i-count*10.3,True))
                        bullet(calculate_new_xy(pos,200,-i-count*10.3,True),i+180+count*10.3,1,2,2)    
                        bullet(calculate_new_xy(pos,200,-i-count*10.3,True),i+count*10.3+20,5,7,4)   
                        bullet(calculate_new_xy(pos,200,-i-count*10.3,True),i+count*10.3-20,5,12,3)
                if while_time(count+200,300):
                    add_effect(pos,8)
                    boss.fire_field = [120,30]        
                if while_time(count,300):
                    boss.fire_field = [-120,30]
                if while_time(count,120) and count > 240:
                    bullet(pos,look_at_player(pos),5,19,6)   
        if num == 44:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready:   
                if while_time(count,8):
                    bullet_effect(s_kira1,1,pos)   
                    bullet(calculate_new_xy(pos,50,-look_at_player(pos)-90,True),look_at_player(boss.pos),10,18,1)  
                    bullet(calculate_new_xy(pos,50,-look_at_player(pos)+90,True),look_at_player(boss.pos),10,18,1)
                if when_time(count,60):
                    set_go_boss(3,choice([60,120,-60,-120]),60)
                if when_time(count,100):
                    add_effect(pos,8) 
                if while_time(count,2) and big_small(count,120,240):  
                    bullet_effect(s_tan1,1,calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True))   
                    bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(boss.pos)+randint(-10,10)+15,12,15,1) 
                    bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(boss.pos)+randint(-10,10)+15,8,12,1)
                    bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(boss.pos)+randint(-10,10)-15,12,15,1) 
                    bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(boss.pos)+randint(-10,10)-15,8,12,1)
                    bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(boss.pos),7,3,3)
                if when_time(count,180):
                    set_go_boss(3,choice([60,120,-60,-120]),60)
                if when_time(count,300):
                    count = 0   
        if num == 45:
            boss.box_disable = True
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready:   
                if boss.list[0] % 2 == 0:
                    if while_time(count,30) and count < 160:
                        rand = (WIDTH,60*count/30)
                        bullet_effect(s_kira0,0,rand)
                        magic_bullet(rand,180,20,8)
                else:
                    if while_time(count,30) and count < 160:
                        rand = (0,70*count/30-40)
                        bullet_effect(s_kira0,0,rand)
                        magic_bullet(rand,0,20,9)                   
                if when_time(count,270):   
                    s_ch0.play()
                    boss.fire_field = (120,60)
                    set_go_boss(7,-look_at_player(pos),60)   
                if when_time(count,390):   
                    s_ch0.play()
                    boss.fire_field = (240,60)
                    set_go_boss(7,-look_at_player(pos),60)
                if when_time(count,540):   
                    boss.fire_field = (-240,60)
                    set_go_boss(7,-look_at_point(pos,boss_movebox.center),60)
                    count=0
                    boss.fire_field = (0,0)
                    boss.fire_field_radius = 0
                    boss.list[0] += 1                  
        if num == 46:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready:
                if while_time(count,20):
                    bullet_effect(s_kira1,0,0,True)
                    for i in range(0,15):
                        bullet((WIDTH+8,i*2*HEIGHT/30+15),180+randint(-5,5),2,6,1)
                if while_time(count+70,190):
                    s_ch0.play()
                    set_go_boss(3,-look_at_point(pos,(pos[0],player.pos[1])),60)
                    boss.fire_field = (120,60)
                if while_time(count,190):
                    boss.fire_field = (0,0)
                    boss.fire_field_radius = 0
                    s_enep2.play()
                    for i in range(0,360,20):
                        bullet(pos,i+randint(0,10),5,19,1)
                    count = 0
        if num == 47:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready:
                if count == 1:
                    add_effect(pos,8)  
                if count > 60:   
                    if while_time(count,3):
                        for i in range(0,360,90):
                            bullet_effect(s_tan1,4,calculate_new_xy(pos,100,-count*-1.7-i,True))
                            bullet(calculate_new_xy(pos,100,-count*0.7-i,True),count*-1.7+i,5,9,4)        
                        for i in range(0,360,90):
                            bullet_effect(0,3,calculate_new_xy(pos,100,count*2.7+i,True))
                            bullet(calculate_new_xy(pos,100,count*2.7+i,True),-count*2.7-i,8,9,3)    
                    if count > 600:
                        if while_time(count,10):
                            for i in range(0,360,90):
                                rand = player.pos[1]+randint(-50,50)
                                bullet_effect(s_tan1,4,(WIDTH,rand))
                                bullet((WIDTH,rand),180,randint(3,5),18,0)   
                    if count == 240 or count == 540:
                        add_effect(pos,8) 
                    if count > 300:          
                        if while_time(count,40):
                            bullet_effect(s_tan1,5,pos)
                            for i in range(0,360,10):    
                                bullet(pos,i+count*5.7,6,15,5)         
        if num == 48:
            boss.box_disable = True
            pos = set_bossmove_point((WIDTH//2,HEIGHT//2,0),120,3)
            if ready:
                if count == 1:
                    add_effect(pos,8)
                    boss.list[0] = 0
                if count == 60:
                    s_enep2.play()            
                if count > 60:
                    if boss.list[0]>3:
                        if while_time(count,1):
                            for i in range(0,360,90):
                                bullet(pos,i+count//1.5,17,15,1)    
                    else:
                        if while_time(count,1):
                            for i in range(0,360,90):
                                bullet(pos,i+count//2,15,3,1)  
                    if while_time(count,60) and boss.list[0]>0:
                        bullet_effect(s_tan1,7,pos)
                        for i in range(0,360,10):
                            bullet(pos,count*2.7+i,3,3,7)    
                    if while_time(count,180) and boss.list[0]>1:
                        bullet_effect(s_kira0,0,0,True)
                        for i in range(0,360,10):
                            bullet(calculate_new_xy(pos,720,-count*1.7-i,True),count*1.7+i+180,2,10,6,23) 
                    if while_time(count,20) and boss.list[0]>2:
                        bullet_effect(s_tan2,5,pos)
                        for i in range(0,360,45):
                            bullet(pos,i,4,7,5)
                    if boss.health<=boss.max_health-round(boss.max_health/5)*(boss.list[1]+1):
                        boss.health -= 1
                        s_enep2.play()     
                        bullet_clear()
                        boss.list[1] += 1
                        boss.list[0] += 1
        
        if ready:pos = go_boss()
        else:pos = calculate_new_xy(pos,boss.move_speed,boss.move_dir)
        return count,pos,ready
    # 스테이지
    def bullet_type(self,mod,sub):
        if mod == 0:
            if sub == 1:
                if self.count == 0:self.screen_die = 1
                self.count += 1
            if sub == 2:
                if self.count == 0:self.screen_die = 2
                self.count += 1
        if mod == 1:
            if sub == 1:
                self.count += 1
                if when_time(self.count,120):
                    for i in range(0,360,20):
                        sbullet(self.pos,i+randint(-5,5),3,2,0)
                    self.kill()
            if sub == 2:
                self.count += 1
                if when_time(self.count,120):
                    for i in range(0,360,20):
                        sbullet(self.pos,i+randint(-5,5),3,2,0)
                        sbullet(self.pos,i+randint(-7,7),2,2,0)
                    self.kill()                        
        if mod == 2:
            if sub == 0:
                self.count += 1
                if self.count > 120:
                    bullet_effect(s_kira0,0,0,True)
                    sbullet(self.pos,randint(-88,88)+180,2,12,3)
                    sbullet(self.pos,randint(-88,88)+180,2,12,3)
                    self.kill()
                elif self.count > 80 and self.speed != 0:
                    self.speed -= 0.2
            if sub == 1:
                if self.pos[0] < -30:
                    self.pos = get_new_pos(self.pos,1143,0)
                    sbullet(self.pos,randint(-88,88)+180,5,18,4)
                    sbullet(self.pos,randint(-88,88)+180,5,18,4)  
                    for i in range(4,6):
                        for j in range(1,11,5):
                            sbullet(self.pos,180,i+j/10,4,4) 
                    for _ in range(0,5):
                        for c in range(4,6):
                            sbullet((self.pos[0]+randint(-30,30),self.pos[1]),180,c,4,4) 
                    s_tan2.play()
                    self.kill()
        if mod == 3:
            if sub == 0:
                self.count += 1
                if while_time(self.count,30) and self.count < 91:
                    sbullet_effect(s_tan2,6,self.pos)
                    rand = randint(0,59)
                    for i in range(0,360,45):
                        sbullet(self.pos,i+rand,1,10,7,3.1)
                        
            if sub == 1:
                self.count += 1
                if self.count == 60:
                    sbullet_effect(s_kira0,0,0,True)
                if self.count > 120 and self.speed < 6:
                    self.speed += 0.1
        if mod == 4:
            self.count += 1
            if sub == 0:
                if while_time(self.count,4):
                    sbullet(self.pos,self.direction+randint(-10,10),0,11,7,4.1)
            if sub == 1:
                if self.count > 120 and self.speed < 5:
                    self.speed += 0.05
        if mod == 5:
            self.count += 1
            if self.count < 30 and self.speed > 0:
                self.speed -= 0.2
            if self.count == 120:
                sbullet_effect(s_kira0,0,0,True)
                sbullet(self.pos,180,7,4,5)
                self.kill()  
        if mod == 6:
            self.count += 1
            if self.count == 60:
                sbullet_effect(s_kira0,3,self.pos)
                sbullet(self.pos,self.direction,6,2,3)
        if mod == 7:
            if boss.count == 240:
                self.speed = 2
        if mod == 8: # 2초 동안 각도 바꾸기
            self.count += 1
            if while_time(self.count,2) and self.count < 60:
                if sub == 0:
                    self.direction += 2
                else:
                    self.direction -= 2
            if self.count == 60: self.speed = self.speed // 2
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
                sbullet_effect(s_kira0,0,0,True)
                if sub == 0:
                    for i in range(0,360,30):
                        sbullet(self.pos,self.direction+i,self.speed/2,14,7,13.1)
                if sub == 1:
                    for i in range(0,360,90):
                        sbullet(self.pos,self.direction+i+45,self.speed/2,18,7,13.2)
                if sub == 2:
                    for i in range(0,360,90):
                        sbullet(self.pos,self.direction+i,self.speed/2,11,7)
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
                    sbullet_effect(s_kira0,0,0,True)
                    self.change_shape(2,1)
            self.count += 1
        if mod == 17:
            if self.speed <= 10:
                self.speed += 0.2            
        if mod == 18:
            if sub == 0:
                if not small_border.collidepoint(self.pos):
                    sbullet_effect(s_tan1,1,get_new_pos(self.pos,randint(-50,50),randint(-50,50)))
                    rand = randint(0,90)
                    for i in range(0,360,90):
                        sbullet(self.pos,i+rand,12,8,7,18.1)
                    rand = randint(0,90)
                    for i in range(0,360,90):
                        sbullet(self.pos,i+rand,8,3,7,18.1)
                    self.kill()
            if sub == 1:
                self.count += 1
                if self.count == 10: self.speed /= 5
        if mod == 19:
            if self.count == 0:
                self.screen_die =2
            self.count += 1
            if distance(self.pos,(boss.pos[0]*2,boss.pos[1]*2)) <= 70:
                self.kill()
        if mod == 20:
            if while_time(boss.count,540):
                sbullet_effect(s_kira1,0,0,True)
                self.speed += 5
        if mod == 21:
            if self.speed > 6:
                self.speed = 6
            if distance(self.pos,(player.pos[0]*2,player.pos[1]*2)) <= 100:
                self.speed = 1
        if mod == 22: #반사탄
            if self.pos[0] > WIDTH*2:
                self.direction  = 180-self.direction
                self.pos = (WIDTH*2,self.pos[1])
            if self.pos[1] > HEIGHT*2: 
                self.direction  = -self.direction
                self.pos = (self.pos[0],HEIGHT*2)
            if self.pos[1] < 0:
                self.direction  = -self.direction
                self.pos = (self.pos[0],0)
        if mod == 23:
            if self.count == 0:self.screen_die = 2
            self.count += 1
            if distance((self.pos[0]//2,self.pos[1]//2),boss.pos) <= 20:
                self.kill()

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
            self.pos = move_circle(player.pos,self.count*3,150)
            if while_time(self.count,6):
                bullet_effect(s_tan1,4,self.pos)
                bullet(self.pos,look_at_player(self.pos),2,10,4,0.1)
                bullet(self.pos,look_at_player(self.pos)+90,5,16,4)
                bullet(self.pos,look_at_player(self.pos)+85,4,16,5)
                bullet(self.pos,look_at_player(self.pos)+95,6,16,5)
        if mod == 4:
            self.count += 1
            self.pos = move_circle(player.pos,self.count*3+180,200)
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
                    sbullet_effect(s_tan1,1,self.pos)
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
                    sbullet_effect(s_tan1,6,self.pos)
                self.speed = 0                
                if while_time(self.count,7):
                    bullet(get_new_pos(self.pos,0,self.count*1.8),180,6,7,6)
                    bullet(get_new_pos(self.pos,0,-self.count*1.8),180,6,7,6)
                self.count += 1
                if self.count == 40:
                    self.kill()
        if mod == 8:
            self.count += 1
            if while_time(self.count,2):
                #sbullet_effect(s_kira1,6,self.pos)
                bullet(self.pos,self.count*2.1,0,4,6,20)
                bullet(self.pos,-self.count*2.1,0,4,7,20)
        if mod == 9:
            self.count += 1
            if while_time(self.count,2):
                #sbullet_effect(s_kira1,6,self.pos)
                bullet(self.pos,self.count*2.1+180,0,4,5,20)
                bullet(self.pos,self.count*2.1,0,4,3,20)

    def stage_manager():
        global stage_cline, stage_line, stage_repeat_count, stage_count, stage_condition, stage_challenge,stage_fun, stage_end
        
        if stage_end <= 0:
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
                                pokemon_spawn(4,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),0,180,4,True)
                            end_while_poke_spawn(2,10)

                        if while_poke_spawn(40,10,2):
                            pokemon_spawn(3,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),40)
                            pokemon_spawn(3,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0)
                            if while_time(stage_repeat_count,3):
                                pokemon_spawn(4,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0,180,4,True)
                            end_while_poke_spawn(2,10)

                        if while_poke_spawn(10,15,2):
                            pokemon_spawn(5,(WIDTH,20),10)
                            pokemon_spawn(6,(WIDTH,HEIGHT-20),0)
                            end_while_poke_spawn(2,15)

                        if while_poke_spawn(40,10,2):
                            pokemon_spawn(3,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),40)
                            pokemon_spawn(3,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0)
                            if while_time(stage_repeat_count,2):
                                pokemon_spawn(4,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),0,180,4,True)
                                pokemon_spawn(4,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0,180,4,True)
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
                            pokemon_spawn(1,(506,-15),20)
                            pokemon_spawn(1,(912//2,-15),0)
                            pokemon_spawn(2,(506,HEIGHT+15),0)
                            pokemon_spawn(2,(912//2,HEIGHT+15),0) 
                            end_while_poke_spawn(4,10)

                        if while_poke_spawn(10,5,2):
                            pokemon_spawn(5,(WIDTH,10),10)
                            pokemon_spawn(6,(WIDTH,HEIGHT-10),0)
                            end_while_poke_spawn(2,5)

                        pokemon_spawn(4,(WIDTH,HEIGHT/2),30)
                        pokemon_spawn(4,(WIDTH,HEIGHT/2+20),30)
                        pokemon_spawn(4,(WIDTH,HEIGHT/2-20),0)
                        pokemon_spawn(4,(WIDTH,HEIGHT/2+40),30)
                        pokemon_spawn(4,(WIDTH,HEIGHT/2),0)
                        pokemon_spawn(4,(WIDTH,HEIGHT/2-40),0)
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
                                pokemon_spawn(4,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),0,180,4,True)
                            if while_time(stage_repeat_count,2):
                                pokemon_spawn(7,(WIDTH-120,HEIGHT+30),0,-90,4,True)
                            end_while_poke_spawn(2,10)
                        if while_poke_spawn(40,10,2):
                            pokemon_spawn(3,(WIDTH+64,HEIGHT-stage_repeat_count*HEIGHT/10-20),40)
                            pokemon_spawn(3,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0)
                            if while_time(stage_repeat_count,3):
                                pokemon_spawn(4,(WIDTH+64,stage_repeat_count*HEIGHT/10+20),0,180,4,True)
                            if while_time(stage_repeat_count,2):
                                pokemon_spawn(7,(WIDTH-120,-30),0,-90,4,True)
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
                                stage_end = 60
                                stage_condition = 1
                                boss.died_next_stage = False   
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

                        pokemon_spawn(8,(WIDTH-100,HEIGHT),120,-90,6)
                        pokemon_spawn(8,(WIDTH-100,0),0,90,6)
                        if while_poke_spawn(15,10,2):
                            pokemon_spawn(8,(WIDTH-50,HEIGHT),15,-90,6)
                            pokemon_spawn(8,(WIDTH-50,0),0,90,6)
                            end_while_poke_spawn(2,10)

                        pokemon_spawn(9,(WIDTH,HEIGHT//2-60),30)
                        pokemon_spawn(9,(WIDTH,HEIGHT//2+60),0)

                        pokemon_spawn(8,(WIDTH-100,HEIGHT),240,-90,6)
                        pokemon_spawn(8,(WIDTH-100,0),0,90,6)
                        if while_poke_spawn(15,10,2):
                            pokemon_spawn(8,(WIDTH-50,HEIGHT),15,-90,6)
                            pokemon_spawn(8,(WIDTH-50,0),0,90,6)
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
                            pokemon_spawn(10,(WIDTH+32,randint(25,HEIGHT-25)),40)
                            end_while_poke_spawn(1,10)
                        if while_poke_spawn(40,10,2):
                            pokemon_spawn(11,(WIDTH+32,randint(100,HEIGHT-50)),40)
                            pokemon_spawn(10,(WIDTH+32,randint(25,HEIGHT-14)),0)
                            end_while_poke_spawn(2,10)
                        bground_spawn(8,1)
                        bground_spawn(9,0)
                        pokemon_spawn(9,(WIDTH+16,HEIGHT//2-60),60)
                        pokemon_spawn(9,(WIDTH+16,HEIGHT//2+60),0)                    

                        next_challenge(480)
                    if stage_challenge == 2:
                        if not boss.appear and not boss.died_next_stage: 
                            boss_spawn(3)
                        if boss.died_next_stage:
                            stage_count = 0
                            boss.died_next_stage = False
                            next_challenge(0)
                    if stage_challenge == 3:
                        pokemon_spawn(9.2,(WIDTH+32,HEIGHT//2+60),30)
                        pokemon_spawn(9.2,(WIDTH+32,HEIGHT//2-60),0)
                        if while_poke_spawn(40,10,1):
                            pokemon_spawn(11,(WIDTH+32,randint(100,HEIGHT-100)),40)
                            end_while_poke_spawn(1,10)

                        pokemon_spawn(10,(WIDTH+32,HEIGHT/10*stage_repeat_count),120)
                        if while_poke_spawn(20,10,1):
                            pokemon_spawn(10,(WIDTH+32,HEIGHT/10*stage_repeat_count),20)
                            end_while_poke_spawn(1,10)
                        if while_poke_spawn(20,10,1):
                            pokemon_spawn(10,(WIDTH+32,HEIGHT-HEIGHT/10*stage_repeat_count),20)
                            end_while_poke_spawn(1,10)
                        pokemon_spawn(8,(WIDTH,HEIGHT),30,-135,4)
                        pokemon_spawn(8,(WIDTH,0),0,135,4)
                        if while_poke_spawn(10,10,2):
                            pokemon_spawn(8,(WIDTH,HEIGHT),10,-135,4)
                            pokemon_spawn(8,(WIDTH,0),0,135,4)
                            end_while_poke_spawn(2,10)
                        pokemon_spawn(10,(WIDTH+32,HEIGHT//2-240),180)
                        pokemon_spawn(10,(WIDTH+32,HEIGHT//2+240),0)                        
                        if while_poke_spawn(20,10,2):
                            pokemon_spawn(10,(WIDTH+32,HEIGHT/10*stage_repeat_count),20)
                            pokemon_spawn(10,(WIDTH+32,HEIGHT-HEIGHT/10*stage_repeat_count),0)
                            end_while_poke_spawn(2,10)

                        pokemon_spawn(11.4,(WIDTH+32,randint(100,HEIGHT-100)),60)
                        if while_poke_spawn(10,10,5):
                            pokemon_spawn(8,(WIDTH+32,randint(100,HEIGHT-100)),10,180,5)
                            pokemon_spawn(8,(WIDTH+32,randint(100,HEIGHT-100)),0,180,5)
                            pokemon_spawn(8,(WIDTH+32,randint(100,HEIGHT-100)),0,180,5)
                            pokemon_spawn(8,(WIDTH+32,randint(100,HEIGHT-100)),0,180,5)
                            pokemon_spawn(8,(WIDTH+32,randint(100,HEIGHT-100)),0,180,5)
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
                                stage_end = 60
                                stage_condition = 1   
                                boss.died_next_stage = False   
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
                            pokemon_spawn(12.4,RIGHT_POS[randint(2,6)],0,180,5)
                            pokemon_spawn(12.4,RIGHT_POS[randint(2,6)],0,180,5)
                            end_while_poke_spawn(3,6)
                        next_challenge(120)
                    if stage_challenge == 2:
                        pokemon_spawn(14,RIGHT_POS[4],120,180,5)
                        pokemon_spawn(14,RIGHT_POS[5],300,180,5)
                        pokemon_spawn(14,RIGHT_POS[3],0,180,5)
                        pokemon_spawn(14,RIGHT_POS[6],300,180,5)
                        pokemon_spawn(14,RIGHT_POS[4],0,180,5)
                        pokemon_spawn(14,RIGHT_POS[2],0,180,5)
                        if while_poke_spawn(20,10,1):
                            pokemon_spawn(12,RIGHT_POS[2],20,-135,5)
                            end_while_poke_spawn(1,10)
    
                        next_challenge(120,True)
                    if stage_challenge == 3:
                        if while_poke_spawn(80,6,2):
                            pokemon_spawn(15,RIGHT_POS[1+stage_repeat_count],80,180,5)
                            pokemon_spawn(15,RIGHT_POS[7-stage_repeat_count],0,180,5)
                            end_while_poke_spawn(2,6)
                        if while_poke_spawn(20,10,1):
                            pokemon_spawn(12,RIGHT_POS[6],20,-135,5)
                            end_while_poke_spawn(1,10)
                        next_challenge(120,True)
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
                        pokemon_spawn(15.4,RIGHT_POS[1],120,180,4)  
                        pokemon_spawn(15.4,RIGHT_POS[2],0,180,4)
                        pokemon_spawn(15.4,RIGHT_POS[3],0,180,4)
                        pokemon_spawn(15.2,RIGHT_POS[4],0,180,4)
                        pokemon_spawn(15.4,RIGHT_POS[5],0,180,4)
                        pokemon_spawn(15.4,RIGHT_POS[6],0,180,4)
                        pokemon_spawn(15.4,RIGHT_POS[7],0,180,4)
                        next_challenge(120, True)
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
                        next_challenge(240)   
                    if stage_challenge == 8:
                        if not boss.appear and not boss.died_next_stage: 
                            boss_spawn(6)
                        if boss.died_next_stage:
                            stage_count = 0
                            if not text.started:
                                stage_challenge = 0
                                stage_line = 0
                                text.re_start()
                                stage_end = 60
                                stage_condition = 1 
                                boss.died_next_stage = False   
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
                                pokemon_spawn(18.4,RIGHT_POS[5],0,200,4,True)
                            end_while_poke_spawn(1,24) 
                        waiting(120)                   
                        if while_poke_spawn(10,24,1):
                            pokemon_spawn(17,RIGHT_POS[6],10,190,5)
                            if stage_repeat_count == 0:
                                pokemon_spawn(18,RIGHT_POS[2],0,160,4,True)
                            if stage_repeat_count == 12:
                                pokemon_spawn(18.4,RIGHT_POS[3],0,160,4,True)
                            end_while_poke_spawn(1,24)
                        waiting(120) 
                        if while_poke_spawn(10,24,2):
                            pokemon_spawn(17,RIGHT_POS[6],10,190,5)
                            pokemon_spawn(17,RIGHT_POS[2],0,170,5)
                            if stage_repeat_count == 0:
                                pokemon_spawn(18,RIGHT_POS[4],0,180,4,True)
                            if stage_repeat_count == 12:
                                pokemon_spawn(18.4,RIGHT_POS[4],0,180,4,True)
                            end_while_poke_spawn(2,24)
                        next_challenge(60,True)
                    if stage_challenge == 2:
                        pokemon_spawn(19.5,RIGHT_POS[4],60,180,5)
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
                                pokemon_spawn(19.2,RIGHT_POS[3],0,180,6,True)
                            end_while_poke_spawn(1,30)    
                        next_challenge(240)
                    if stage_challenge == 6:
                        if while_poke_spawn(100,8,1):
                            pokemon_spawn(20,(player.pos[0],HEIGHT+64),100,-90,0)
                            if stage_repeat_count > 3:
                                pokemon_spawn(17.4,(WIDTH + 64,player.pos[1]),0,172,7,True)
                                pokemon_spawn(17.4,(WIDTH + 64,player.pos[1]),0,174,6,True)
                                pokemon_spawn(17.4,(WIDTH + 64,player.pos[1]),0,176,5,True)
                                pokemon_spawn(17.4,(WIDTH + 64,player.pos[1]),0,178,4,True)
                                if stage_repeat_count == 7:
                                    pokemon_spawn(17 if stage_repeat_count == 7 else 17.5,(WIDTH + 64,player.pos[1]),0,180,3,True)
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
                                stage_end = 60
                                stage_condition = 1     
                                boss.died_next_stage = False                                            
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
                        pokemon_spawn(22.2,RIGHT_POS[2],180,180,4)  
                        pokemon_spawn(22.2,RIGHT_POS[6],0,180,4)

                        if while_poke_spawn(10,24,1):
                            pokemon_spawn(21,RIGHT_POS[7],10,randint(25,65)+180,4)    
                            end_while_poke_spawn(1,24) 
                        next_challenge(60)
                    if stage_challenge == 2:
                        pokemon_spawn(23,RIGHT_POS[2],1,160,5)   
                        pokemon_spawn(23,RIGHT_POS[6],300,-160,5)  
                        pokemon_spawn(23.4,RIGHT_POS[4],200,-160,5) 
                        waiting(280)
                        if while_poke_spawn(10,140,1):
                            pokemon_spawn(21,choice(DOWN_POS),10,-90,randint(4,5)) 
                            if when_time(stage_repeat_count,24):
                                pokemon_spawn(22.2,RIGHT_POS2[1],0,170,5,True) 
                            if when_time(stage_repeat_count,48):
                                pokemon_spawn(22.4,RIGHT_POS2[2],0,170,5,True) 
                            if when_time(stage_repeat_count,72):
                                pokemon_spawn(22.2,RIGHT_POS2[3],0,170,5,True) 
                            if when_time(stage_repeat_count,96):
                                pokemon_spawn(22.4,RIGHT_POS2[4],0,170,5,True) 
                            end_while_poke_spawn(1,92)      

                        pokemon_spawn(23,RIGHT_POS[3],60,160,5)  
                        pokemon_spawn(23.3,RIGHT_POS[5],0,-160,5)
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
                        pokemon_spawn(24.2,RIGHT_POS[6],0,180,5)
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
                        pokemon_spawn(25.2,RIGHT_POS[4],120,180,12)
                        pokemon_spawn(25.5,RIGHT_POS[4],60,180,12)
                        if while_poke_spawn(20,32,2): 
                            pokemon_spawn(26,RIGHT_POS[7],20,180,5) 
                            pokemon_spawn(21,RIGHT_POS[4],0,randint(170,190),5) 
                            if while_time(stage_repeat_count,14):
                                pokemon_spawn(22.4,RIGHT_POS[4],0,180,5,True) 
                            if when_time(stage_repeat_count,16):
                                pokemon_spawn(23.4,RIGHT_POS[2],0,160,6,True)
                            end_while_poke_spawn(2,32)
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
                                stage_end = 60
                                stage_condition = 1    
                                boss.died_next_stage = False                  
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

                        pokemon_spawn(28,RIGHT_POS[4],120,180,6)   
                        pokemon_spawn(28,RIGHT_POS[3],240,180,6)    
                        pokemon_spawn(28,RIGHT_POS[5],240,180,6)
                        pokemon_spawn(28,RIGHT_POS[2],240,180,6)
                        pokemon_spawn(28,RIGHT_POS[6],240,180,6)
                        pokemon_spawn(28,RIGHT_POS[4],240,180,6)

                        pokemon_spawn(29,RIGHT_POS[1],360,180,6)
                        pokemon_spawn(29,RIGHT_POS[7],0,180,6)     
                        pokemon_spawn(29,RIGHT_POS[1],300,180,6)
                        pokemon_spawn(29,RIGHT_POS[7],0,180,6)  
                        next_challenge(480)
                    if stage_challenge == 1:
                        pokemon_spawn(30,RIGHT_POS[4],180,180,2)
                        pokemon_spawn(30,RIGHT_POS[1],120,180,2)
                        pokemon_spawn(30,RIGHT_POS[5],120,180,2)
                        pokemon_spawn(30,RIGHT_POS[6],120,180,2)
                        pokemon_spawn(30,RIGHT_POS[2],120,180,2)
                        pokemon_spawn(30,RIGHT_POS[3],120,180,2)
                        waiting(360)
                        if while_poke_spawn(20,20,1):
                            pokemon_spawn(27.2,(WIDTH+64,16+stage_repeat_count*15),20,180,6)
                            end_while_poke_spawn(1,20)
                        pokemon_spawn(29.4,RIGHT_POS[4],90,180,6)
                        waiting(90)
                        if while_poke_spawn(20,20,1):
                            pokemon_spawn(27.2,(WIDTH+64,HEIGHT-16-stage_repeat_count*15),20,180,6)
                            end_while_poke_spawn(1,20) 
                        next_challenge(360)
                    if stage_challenge == 2:
                        if not boss.appear and not boss.died_next_stage: 
                            boss_spawn(11)  
                    
                stage_cline = 0
        else:
            stage_end -= 1
    
    ################################################# 
    while play:
        # 60 프레임
        clock.tick(clock_fps)
        now = time.time()        
        dt = (now-prev_time)*TARGET_FPS        
        prev_time = now
        keys = pygame.key.get_pressed() 
        if cur_screen == 1:
            # 키 이벤트
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    pygame.quit()
                    exit()
                if ev.type == pygame.KEYDOWN:    
                    if not pause:                
                        if ev.key == pygame.K_f:
                            full_on = False if full_on == True else True
                        if ev.key == pygame.K_ESCAPE and not (text.started and not text.pause) and frame_count >= 60:
                            s_pause.play()
                            pause = True
                            pygame.mixer.music.pause()                        
                        if ev.key == pygame.K_z and text.started and text.count > 50 and not text.pause:
                            text.next_text()
                        if (text.started and text.pause) or not text.started:
                            if ev.key == pygame.K_z and player.gatcha >= player.gatcha_max:
                                if player.shoot_gatcha > 0:
                                    beams_group.add(Beam(get_new_pos(player.pos,5),4))
                                if player.shoot_gatcha == 0:
                                    player.shoot_gatcha = 10                            
                        if (text.started and text.pause) or not text.started:
                            if ev.key == pygame.K_x and player.mp > 0:
                                skill_activating.append(Skill_Core(26,295))
                                boss.spell_clear = False
                                player.mp -= 1      
                            if ev.key == pygame.K_c and player.skill_list[player.skill_pointer].pp > 0:
                                player.skill_list[player.skill_pointer].pp -= 1    
                                skill_activating.append(Skill_Core(player.skill_list[player.skill_pointer].num,player.skill_list[player.skill_pointer].cool))
                        if ev.key == pygame.K_d:
                            player.skill_list.append(player.skill_list.pop(0))
                    else:
                        if ev.key == pygame.K_UP:
                            s_ok.play()
                            curser = 2 if curser == 0 else curser-1
                        if ev.key == pygame.K_DOWN:
                            s_ok.play()
                            curser = 0 if curser == 2 else curser+1
                        if ev.key == pygame.K_z:
                            s_select.play()
                            if curser == 0: 
                                if practicing and boss.died_next_stage:
                                    pass
                                elif player.died:
                                    player.health = player.max_health
                                    player.power = 400
                                    player.count = 0
                                    player.mp = 4
                                    player.died = False
                                    pause = False
                                    continued += 1
                                    pygame.mixer.music.unpause()
                                else:
                                    pause = False
                                    pygame.mixer.music.unpause()
                            if curser == 1:
                                if practicing:practicing = False
                                player.power = 0
                                player.health = player.max_health
                                stage_fun = start_fun
                                stage_line = 0
                                stage_cline = 0
                                stage_repeat_count = 0
                                stage_condition = 1
                                stage_challenge = 0
                                player.skill_list = []
                                player.skill_list.append(Skill(0,7,"Press C key!","몸부림",30,60))
                                player.skill_list.append(Skill(0,7,"Press C key!","몸부림",30,60))
                                player.skill_list.append(Skill(0,7,"Press C key!","몸부림",30,60))
                                score = 0
                                skill_activating = []
                                pause = False
                                pygame.mixer.music.unpause()  
                                enemy_group.empty()     
                                spr.empty()     
                                item_group.empty()  
                                boss.reset()             
                                continued = 0             
                            if curser == 2: game_restart = True
                        if ev.key == pygame.K_ESCAPE:
                            pause = False
                            pygame.mixer.music.unpause()
            if keys[pygame.K_LCTRL] and text.started and text.count > 50 and not text.pause:
                text.next_text()
            if game_restart:
                frame_count = 0
                break
            
            # 탄에 박았는가
            hit_list = pygame.sprite.spritecollide(player_hitbox, spr, not player.godmod, pygame.sprite.collide_circle)
            beam_collide = pygame.sprite.groupcollide(beams_group, enemy_group, False, False, pygame.sprite.collide_circle)
            if beam_collide.items():
                for beam, enemy in beam_collide.items():                 
                    for i in range(0,len(enemy)): 
                        if not beam.died:
                            enemy[i].health -= beam.damage
                            if beam.num == 4 and enemy[i].health <= 0:
                                player.skill_list[player.skill_pointer] = enemy[i].skill   
                                score+=score_setting[4] 
                            beam.died = True                       
            if boss.appear: boss_collide = pygame.sprite.spritecollide(boss, beams_group, False, pygame.sprite.collide_circle)
            # 연산 업데이트
            if not pause:      
                if magic_spr.sprites():magic_spr.update(screen)    
                if boss.appear and boss.health <= 0: remove_allbullet()  
                if boss.fire_field_radius > 0:
                    for item in spr.sprites():
                        if distance(item.pos,(boss.pos[0]*2,boss.pos[1]*2)) <= boss.fire_field_radius*2 and not item.shape[1]==4:
                            item.speed += 0.1
                if skill_activating:
                    for skill in skill_activating[:]:
                        skill.update(boss)
                        if skill.cool <= 0 and skill.draw_cool <= 0: skill_activating.remove(skill)
                if skillobj_group: skillobj_group.update(screen)
                spr.update(screen)
                if not time_stop:
                    if not player.died:player_hitbox.update(player)
                    if beams_group: beams_group.update()                            
                    player_group.update(hit_list, text)
                    if enemy_group:enemy_group.update()
                    if item_group: item_group.update()
                    if boss.appear: boss_group.update(boss_collide)
                    if effect_group: effect_group.update(text)
                    if not player.died:player_sub.update(text,player,beams_group, character)
                    if text.started and not text.pause: text.update()
                    stage_manager()
                    if practicing and boss.died_next_stage:
                        pause = True
                    frame_count += 1
                    stage_count += 1
                    if not bkgd_list == []:
                        for i in bkgd_list:i.update()
            if boss.died_next_stage and stage_fun == 6 and stage_challenge == 2 and not game_clear:
                pygame.mixer.music.fadeout(9000)
                stage_count = 0
                cur_count = frame_count
                game_clear = True 
            if game_clear:
                if frame_count - cur_count > 600:
                    cur_screen = 0
                    frame_count = 0
            # 그리기 시작
            #배경 스크롤
            if frame_count >= 60:
                if not pause:
                    background_scroll()               
                    if boss.fire_field_radius > 0:
                        fire_layer = pygame.Surface((WIDTH,HEIGHT), SRCALPHA)
                        pygame.draw.circle(fire_layer, (255,0,0,150), boss.pos, boss.fire_field_radius)
                        render_layer.blit(fire_layer,(0,0))
                    skill_surface.fill((0,0,0,0))
                    if skill_activating:                    
                        for skill in skill_activating[:]:
                            skill.draw(skill_surface)
                    if skillobj_group: skillobj_group.draw(skill_surface)
                    render_layer.blit(skill_surface,(0,0))              
                    item_group.draw(render_layer)
                    magic_spr.draw(render_layer)      
                    beams_group.draw(render_layer)  
                    if not player.died and not drilling:player_group.draw(render_layer) 
                    if not player.died and not drilling:player_sub.draw()
                    enemy_group.draw(render_layer)            
                    if not starting or read_end: enemy_group.draw(render_layer)
                    if boss.appear: boss_group.draw(render_layer)
                    under_ui.draw()
                    scaled = pygame.transform.scale2x(render_layer)
                    screen.blit(scaled,(0,0))                    
                    spr.draw(screen)
                    up_render_layer.fill((255,255,255,0))
                    effect_group.draw(up_render_layer)   
                    player.skill_list[player.skill_pointer].draw()                  
                    if title.count < 460: title.draw()
                    if text.started:text.draw()
                    ui.draw()
                    if boss.spell and boss.appear and boss.spell[0].spellcard:
                        boss.spell[0].draw()
                    if game_clear:
                        if frame_count-cur_count > 300:
                            up_render_layer.fill((255,255,255,frame_count-300-cur_count if frame_count-300-cur_count < 256 else 255))                    
                    screen.blit(pygame.transform.scale2x(up_render_layer),(0,0))
                    if screen_shake_count > 0:
                        screen.blit(screen,(randint(-20,20),randint(-20,20)))
                        screen_shake_count -= 1
                else: 
                    screen.blit(pygame.transform.scale2x(render_layer),(0,0))
                    spr.draw(screen)
                    screen.blit(pygame.transform.scale2x(up_render_layer),(0,0))
                    pause_menu = pygame.Surface((WIDTH,HEIGHT), SRCALPHA)  
                    pause_menu.fill((255, 0, 85,100))
                    pause_menu.blit(menu_img,(10,100),(160,48,160,32))
                    for i in range(0,3): # 메뉴 그리기
                        menu = pygame.Surface((160,32), SRCALPHA)
                        if curser == i: menu.fill((0,0,0,200))
                        menu.blit(menu_img,(0,0),(160,80+32*i,160,32))
                        if i == 0 and practicing and boss.died_next_stage: 
                            pygame.draw.rect(menu, (0,0,0,100), (0,0,160,32))
                        pause_menu.blit(menu,(0,200+32*i))
                    screen.blit(pygame.transform.scale2x(pause_menu),(0,0))     
            else:
                pass 
            
            pygame.display.flip()       
        if cur_screen == 0:
            if frame_count == 0 and not game_clear:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(TITLE)
                pygame.mixer.music.play(-1)
                frame_count -= 1
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    play = False
                if ev.type == pygame.KEYDOWN: 
                    if not game_clear:
                        if ev.key == pygame.K_f:
                            full_on = False if full_on == True else True  
                        if ev.key == pygame.K_UP:
                            curser = curser_max if curser == 0 else curser - 1 # 커서위로
                            s_ok.play()
                        if ev.key == pygame.K_DOWN:
                            curser = 0 if curser == curser_max else curser + 1 # 커서밑으로
                            s_ok.play()
                        if select_mod == 0: # 시작화면
                            if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                s_select.play()
                                if curser == 5: play = False # 게임끄기
                                else:select_mod += 1 ############ 게임시작
                                menu_mod.append(curser) # 현재 어떤 버튼 눌렀는지 저장
                                curser = 0
                                break
                        if select_mod == 1:
                            if menu_mod[0] == 0:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    s_select.play()
                                    character = 0 if curser == 0 else 41
                                    player.power = 0
                                    cur_screen = 1  
                                    stage_fun = 0
                                    start_fun = stage_fun
                                    frame_count = 0
                                    curser = 0
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    curser = 0
                                    select_mod -= 1
                                    del menu_mod[len(menu_mod)-1]      
                                    break             
                            if menu_mod[0] == 1:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    select_mod += 1
                                    menu_mod.append(curser)
                                    s_select.play()
                                    curser = 0
                                    break 
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    curser = 0
                                    select_mod -= 1
                                    del menu_mod[len(menu_mod)-1]   
                                    break 
                                if ev.key == pygame.K_RIGHT or ev.key == pygame.K_LEFT:
                                    s_select.play()
                                    character = 41 if character == 0 else 0      
                            if menu_mod[0] == 2:
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    curser = 0
                                    select_mod -= 1
                                    del menu_mod[len(menu_mod)-1]   
                                    break
                            if menu_mod[0] == 3:
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    curser = 0
                                    select_mod -= 1
                                    del menu_mod[len(menu_mod)-1]   
                                    break
                            if menu_mod[0] == 4:
                                if ev.key == pygame.K_RIGHT:
                                    s_ok.play()
                                    if curser == 0:
                                        full_on = 1 if full_on == 0 else 0
                                    if curser == 1:
                                        mmusic_volume = mmusic_volume + 5 if mmusic_volume < 100 else 100
                                    if curser == 2:
                                        msfx_volume = msfx_volume + 5 if msfx_volume < 100 else 100                                
                                if ev.key == pygame.K_LEFT:
                                    s_ok.play()
                                    if curser == 0:
                                        full_on = 1 if full_on == 0 else 0
                                    if curser == 1:
                                        mmusic_volume = mmusic_volume - 5 if mmusic_volume > 0 else 0
                                    if curser == 2:
                                        msfx_volume = msfx_volume - 5 if msfx_volume > 0 else 0
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    try:sfx_volume = msfx_volume/100
                                    except:sfx_volume = 0
                                    try:music_volume = mmusic_volume/100
                                    except:music_volume = 0
                                    music_and_sfx_volume(music_volume,sfx_volume)
                                    with open('resources\setting.txt','w',encoding="UTF-8") as f:
                                        f.write("fullscreen"+"="+str(full_on)+"\n")
                                        f.write("sfx"+"="+str(msfx_volume)+"\n")
                                        f.write("bgm"+"="+str(mmusic_volume)+"\n")
                                    curser = 0
                                    select_mod -= 1
                                    del menu_mod[len(menu_mod)-1]     
                                    break                        
                        if select_mod == 2:
                            if menu_mod[0] == 1:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    s_select.play()                                    
                                    player.power = 400
                                    stage_fun = menu_mod[1]                                 
                                    start_fun = stage_fun  
                                    if curser == 1:
                                        if menu_mod[1] == 0:stage_challenge = 5
                                        if menu_mod[1] == 1:stage_challenge = 4
                                        if menu_mod[1] == 2:stage_challenge = 8
                                        if menu_mod[1] == 3:stage_challenge = 7
                                        if menu_mod[1] == 4:stage_challenge = 6
                                        if menu_mod[1] == 5:stage_challenge = 2
                                    curser = 0
                                    cur_screen = 1 
                                    practicing = True
                                    frame_count = 0
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    curser = menu_mod[1]
                                    select_mod -= 1
                                    del menu_mod[len(menu_mod)-1]   
                                    break 
                    
                    else:
                        if ev.key == K_x or ev.key == K_ESCAPE or ev.key == K_z:
                            old_score = 0
                            if character == 0:
                                old_score = int(score_scroll[0][2:])
                                if old_score < score:
                                    score_scroll[0] = "H:"+str(score).zfill(10)
                                    score_scroll[0] = score_scroll[0]
                            else:
                                old_score = int(score_scroll[1][2:])
                                if old_score < score:
                                    score_scroll[1] = "F:"+str(score).zfill(10)
                                    score_scroll[1] = score_scroll[1]
                            with open('resources\score.txt','w',encoding="UTF-8") as f:
                                f.write(score_scroll[0]+"\n")
                                f.write(score_scroll[1]+"\n")
                                
                            game_restart = True
            if game_restart:
                frame_count = 0
                break    
            render_layer.blit(background_img,(0,0))            
            ui_x = WIDTH - 180
            ui_y = 20
            if not game_clear:
                if select_mod == 0: # 시작화면
                    curser_max = 5
                    render_layer.blit(title_img,(0,0))# 타이틀
                    for i in range(0,6): # 메뉴 그리기
                        menu = pygame.Surface((160,32), SRCALPHA)
                        if curser == i: menu.fill((0,0,255,200))
                        menu.blit(menu_img,(0,0),(0,48+32*i,320,48))
                        render_layer.blit(menu,(ui_x,ui_y+32*i))
                    text1 = score_font.render(score_scroll[0], True, (0,0,0))
                    render_layer.blit(text1,(0,HEIGHT-60))
                    text1 = score_font.render(score_scroll[1], True, (0,0,0))
                    render_layer.blit(text1,(2,HEIGHT-30))
                if select_mod == 1: # 다음옴션
                    if menu_mod[0] == 0: # 시작>난이도 정하기
                        curser_max = 1
                        render_layer.blit(menu_img,(0,0),(0,240,320,48))
                        for i in range(0,2): # 메뉴 그리기
                            menu = pygame.Surface((208,32), SRCALPHA)
                            if curser == i: menu.fill((0,0,0,200))
                            menu.blit(menu_img,(0,0),(0,288+32*i,192,32))
                            render_layer.blit(menu,(int(WIDTH/2-240),int(HEIGHT/2-30+64*i-64*curser)))
                    if menu_mod[0] == 1:
                        curser_max = 5
                        text_box = ["Stage1","Stage2","Stage3","Stage4","Stage5","Stage6"]
                        for i in range(0,6):
                            text_color = (255,0,255) if i == curser else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(100,50+40*i))
                        if character == 0:
                            text_color = (0,0,0)
                            text1 = score_font.render("Homing", True, text_color)                        
                            render_layer.blit(text1,(300,100))  
                        else:  
                            text_color = (0,0,0)
                            text1 = score_font.render("FFocus", True, text_color)                        
                            render_layer.blit(text1,(300,100))   
                    if menu_mod[0] == 2:
                        font = pygame.font.Font(FONT_2, 30)
                        pygame.draw.rect(render_layer, (0,0,0), (20,20,WIDTH-40,HEIGHT-40), width=0)
                        for texta in range(0,len(htp_scroll)):
                            text1 = font.render(htp_scroll[texta], True, (255,255,255))
                            render_layer.blit(text1,(40,30*texta+30))
                    if menu_mod[0] == 3:
                        font = pygame.font.Font(FONT_2, 10)
                        pygame.draw.rect(render_layer, (0,0,0), (20,20,WIDTH-40,HEIGHT-40), width=0)
                        for texta in range(0,len(credit_scroll)):
                            text1 = font.render(credit_scroll[texta], True, (255,255,255))
                            render_layer.blit(text1,(30,10*texta+30))
                    if menu_mod[0] == 4:
                        curser_max = 2
                        text_box = ["화면모드","음악","효과음"]
                        text_box[0] = "화면모드    창모드" if full_on == 0 else "화면모드    전체화면"
                        text_box[1] = "음악   " + str(mmusic_volume)
                        text_box[2] = "효과음  " + str(msfx_volume)
                        for i in range(0,3):
                            text_color = (255,0,255) if i == curser else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(200,100+40*i))
                if select_mod == 2:
                    if menu_mod[0] == 1:
                        curser_max = 1
                        text_box = ["Field","Boss"]
                        for i in range(0,2):
                            text_color = (255,0,255) if i == curser else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(200,50+40*i))
                        text_box = ["Stage1","Stage2","Stage3","Stage4","Stage5","Stage6"]
                        for i in range(0,6):
                            text_color = (255,0,255) if i == menu_mod[1] else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(100,50+40*i))
                        if character == 0:
                            text_color = (0,0,0)
                            text1 = score_font.render("Homing", True, text_color)                        
                            render_layer.blit(text1,(300,100))  
                        else:  
                            text_color = (0,0,0)
                            text1 = score_font.render("FFocus", True, text_color)                        
                            render_layer.blit(text1,(300,100)) 

                # if select_mod == 2:
                #     if menu_mod == 1:




                if frame_count > 0:
                    frame_count -= 1
                    if frame_count == 0:
                        character = 0 if curser == 0 else 41
                        player.power = 0
                        cur_screen = 1  
                        stage_fun = 0
                        start_fun = stage_fun  
                        curser = 0
            else:
                x = 80
                y = 80 + math.sin(math.pi * (frame_count / 180))*5
                y2 = 80 + math.sin(math.pi * (frame_count*2 / 180))*5
                font = pygame.font.Font(FONT_1, 20)    
                text1 = font.render("!GAME CLEAR!", True, (0,0,255))   
                render_layer.blit(text1,(0,0))              
                text1 = font.render("HP: "+str(player.health)+"/"+str(player.max_health), True, (0,0,0))   
                render_layer.blit(text1,(x,y)) 
                if character == 0:text1 = font.render("Weapon:"+"Homing", True, (0,0,0))
                else: text1 = font.render("Weapon:"+"FFocus", True, (0,0,0))  
                render_layer.blit(text1,(x+10,y+30)) 
                text1 = font.render("Continue:"+str(continued), True, (0,0,0))   
                render_layer.blit(text1,(x+20,y+60)) 
                text1 = font.render("Final Score", True, (0,0,0))   
                render_layer.blit(text1,(x+60,y+90)) 
                text1 = font.render(str(score).zfill(10), True, (0,0,0))   
                render_layer.blit(text1,(x+60,y+120))
                render_layer.blit(pokemons[0],(x+260,y2+100))
                frame_count += 1

            if cur_screen == 0:screen.blit(pygame.transform.scale2x(render_layer),(0,0))
            pygame.display.flip()
        
        if full_on != cur_full_mod:
            if full_on:
                screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN|pygame.SCALED)
            else:
                screen = pygame.display.set_mode((WIDTH*2, HEIGHT*2))
            cur_full_mod = full_on
    if game_restart:
        game_restart = False
        play_game()

if __name__ == "__main__":
    play_game()

