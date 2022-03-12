import start as st
from start import WIDTH,HEIGHT, bg_image, bg2_image, FIELD_1, FIELD_2, FIELD_3, FIELD_4, FIELD_5, FIELD_6, RIGHT_POS, RIGHT_POS2, UP_POS, DOWN_POS, pokemons, boss_movebox, small_border
from spec_func import *
import stage_var as sv
import pygame, math
from random import randint, choice
from start import s_lazer1, s_enep2, s_ch0,  s_tan1, s_tan2
from norm_func import *

def while_poke_spawn(time,repeat,line):
    if sv.stage_line == sv.stage_cline and sv.stage_count == time:
        return sv.stage_count == time and sv.stage_line == sv.stage_cline and sv.stage_repeat_count < repeat
    else:
        sv.stage_cline += line 
        return False

def end_while_poke_spawn(line,repeat):
 
    sv.stage_line -= line
    sv.stage_repeat_count += 1
    if sv.stage_repeat_count >= repeat:
        sv.stage_line += line
        sv.stage_repeat_count = 0

# 다음 챌린지 넘어가기
def next_challenge(time,kill = False):

    if time == sv.stage_count and sv.stage_line == sv.stage_cline:
        sv.stage_count = 0
        sv.stage_line = 0
        sv.stage_challenge += 1
        if not kill:
            enemy_clear()
            bullet_clear()           
# 스테이지 이름
def title_spawn(val,time):

    # x, y, dir, speed, health, img, hit_cir, num = val
    if time == sv.stage_count and sv.stage_line == sv.stage_cline:
        sv.title.count = 0
        sv.stage_count = 0
        sv.stage_line += 1
        if val == 1:
            sv.title.title_start("Stage 1","드넓은 초원")
        if val == 2:    
            sv.title.title_start("Stage 2","왕자가 숨은 바다")
        if val == 3:    
            sv.title.title_start("Stage 3","흔적없는 과거의 자취")
        if val == 4:    
            sv.title.title_start("Stage 4","땅속 깊은 생명보호")
        if val == 5:    
            sv.title.title_start("Stage 5","고대의 성")
        if val == 6:    
            sv.title.title_start("Stage 6","화가 존재하는 현실")
    sv.stage_cline += 1
# 뒷배경 소환
def bground_spawn(val,time):

    # x, y, dir, speed, health, img, hit_cir, num = val
    if time == sv.stage_count and sv.stage_line == sv.stage_cline:
        sv.stage_count = 0
        sv.stage_line += 1
        if val == 1:st.bkgd_list.append(sv.Back_Ground(bg_image,(540,0,540,120),1,3,0,True))
        if val == 2:st.bkgd_list.append(sv.Back_Ground(bg_image,(540,240,540,120),3,4,240,True))
        if val == 3:st.bkgd_list.append(sv.Back_Ground(bg_image,(1080,0,540,290),2,5,0,True)) 
        if val == 8:st.bkgd_list.append(sv.Back_Ground(bg_image,(1080//2,972//2,1080//2,468//2),2,8,126,True))
        if val == 9:st.bkgd_list.append(sv.Back_Ground(bg_image,(1080//2,720//2,1080//2,252//2),1,9,0,True))
    sv.stage_cline += 1
# 게임의 배경, 스테이지
def game_defalt_setting(fun): # 게임 스테이지 배경 정하기
    st.bkgd_list = []
    ##############################################
    if fun == 1:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,0,1080,240),1,0,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,240,1080,240),2,1,240))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,480,1080,240),3,2,480))
    if fun == 2:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,360,540,232),2,6,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,592,540,128),3,7,232))
    if fun == 3:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,720,540,126),5,8,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,776,540,304),7,9,118))
    if fun == 4:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1080,720,360),10,10))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,1080,540,360),8,11))
    if fun == 5:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440,540,72),7,8,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440+72,540,72),5,8,72))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440+72*2,540,72),3,8,72*2))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440+72*3,540,72),5,8,72*3))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1440+72*4,540,72),7,8,72*4))
    if fun == 6:
        st.bkgd_list.append(sv.Back_Ground(bg_image,(0,1800,540,360),5,8,0))
        st.bkgd_list.append(sv.Back_Ground(bg_image,(540,2070,540,90),3,8,280))

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
    
    # x, y, dir, speed, health, img, hit_cir, num = val
    if time == sv.stage_count and sv.stage_line == sv.stage_cline:
        sv.stage_count = 0
        sv.stage_line += 1
    sv.stage_cline += 1
#################################################
def pokemon_spawn(val,pos,time,dir=0,speed=0,simple = False):
    x = pos[0]
    y = pos[1]        
    val, item = math.trunc(val), (val*10)%10
    # x, y, dir, speed, health, img, hit_cir, num = val
    if (time == sv.stage_count and sv.stage_line == sv.stage_cline) or simple:
        if not simple:
            sv.stage_count = 0
            sv.stage_line += 1
        if sv.stage_fun == 1:
            if val == 1:
                sv.enemy_group.add(sv.Enemy(x,y,180,4,3,11,30,val,sv.Skill(1,0,"평범하기 그지없는","몸통박치기",10,40,10),item))  
            if val == 2:
                sv.enemy_group.add(sv.Enemy(x,y,180,4,3,12,30,val,sv.Skill(2,5,"얍삽한","쪼기",10,40,10),item))  
            if val == 3:
                sv.enemy_group.add(sv.Enemy(x,y,180,3,6,14,30,val,sv.Skill(2,5,"얍삽한","쪼기",10,40,10),item))
            if val == 4:
                sv.enemy_group.add(sv.Enemy(x,y,180,4,10,13,30,val,sv.Skill(3,5,"저리가람","바람일으키기",10,60,30),item))
            if val == 5:
                sv.enemy_group.add(sv.Enemy(x,y,135,6,5,11,30,val,sv.Skill(1,0,"평범하기 그지없는","몸통박치기",10,40,10),item))
            if val == 6:
                sv.enemy_group.add(sv.Enemy(x,y,225,6,5,12,30,val,sv.Skill(2,5,"얍삽한","쪼기",10,40,10),item))
            if val == 7:
                sv.enemy_group.add(sv.Enemy(x,y,dir,4,7,15,30,val,sv.Skill(4,8,"보이지 않는 장막","실뿜기",5,5,30),item))
        ##################### 2 스테이지 #################
        if sv.stage_fun == 2:
            if val == 8:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,7,19,30,val,sv.Skill(5,2,"조금 위협적인","물놀이",10,60,15),item))
            if val == 9:
                sv.enemy_group.add(sv.Enemy(x,y,180,5,240,17,40,val,sv.Skill(6,2,"아마도 모든걸 베는","셸블레이드",20,60,50),item))
            if val == 10:
                sv.enemy_group.add(sv.Enemy(x,y,180,4,20,18,30,val,sv.Skill(7,2,"모양은 원모양","거품발사",20,50,30),item))
            if val == 11:
                sv.enemy_group.add(sv.Enemy(x,y,180+randint(-10,10),4,20,16,30,val,sv.Skill(8,2,"불끌때 제법인","물대포",5,90,80),item))
        ##################### 3 스테이지 $$$$$$$$$$$$$$$$$
        if sv.stage_fun == 3:
            if val == 12:
                sv.enemy_group.add(sv.Enemy(x,y,180,speed,30,21,30,val,sv.Skill(9,3,"어떻게 보면 잔인한","씨앗심기",3,120,30),item))    
            if val == 13:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,80,22,40,val,sv.Skill(10,0,"충격 흡수량 최대","코튼가드",10,5,50),item))   
            if val == 14:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,100,23,40,val,sv.Skill(11,8,"뭔 이상한거에만 효과있는","마비가루",20,60,20),item))   
            if val == 15:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,30,24,40,val,sv.Skill(12,9,"날카로운 확인사살","독침",5,90,80),item)) 
            if val == 16:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,120,25,40,val,sv.Skill(13,3,"완벽을 추구하는","HP필드",5,180,100),item))
        if sv.stage_fun == 4:
            if val == 17:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,15,30,40,val,sv.Skill(14,4,"소음따위는 안들린다","명상",5,240,20),item))
            if val == 18:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,100,27,40,val,sv.Skill(15,4,"저격한다!","사이코리모트",10,500,80),item))
            if val == 19:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,250,29,50,val,sv.Skill(16,6,"마비는 안걸리는 안전한","방전",10,300,50),item))
            if val == 20:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,150,28,50,val,sv.Skill(17,10,"경계를 뚫는?!","땅굴파기",10,120,80),item))               
        if sv.stage_fun == 5:
            if val == 21:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,15,31,30,val,sv.Skill(18,5,"물리를 행사하는","흑안개",30,60*20,10),item))
            if val == 22:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,210,34,60,val,sv.Skill(19,4,"전부 멀리 가버려!","사이코키네시스",5,5,50),item))
            if val == 23:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,300,33,30,val,sv.Skill(20,1,"눈앞이 불지옥","화염방사",5,240,80),item))        
            if val == 24:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,100,35,30,val,sv.Skill(21,10,"불안전지대","스텔스록",10,300,50),item))
            if val == 25:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,100,32,30,val,sv.Skill(23,1,"불꽃펀치","불꽃펀치",3,60,80),item))
            if val == 26:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,20,36,30,val,sv.Skill(22,0,"상대를 속이진 않는","속이다",10,60,5),item))      
        if sv.stage_fun == 6:
            if val == 27:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,30,37,30,val,sv.Skill(24,0,"아마도 누구든지 배울 수 있는","파괴광선",1,600,200),item))       
            if val == 28:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,450,38,30,val,sv.Skill(10,0,"충격 흡수량 최대","코튼가드",10,5,50),item))   
            if val == 29:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,300,39,30,val,sv.Skill(24,0,"아마도 누구든지 배울 수 있는","파괴광선",1,600,200),item))   
            if val == 30:
                sv.enemy_group.add(sv.Enemy(x,y,dir,speed,200,40,30,val,sv.Skill(10,0,"충격 흡수량 최대","코튼가드",10,5,50),item))              
    
    if not simple: sv.stage_cline += 1
# 적의 공격타입
def enemy_attack(num,count,pos,dir,speed,list):
    pos = calculate_new_xy(pos, speed, dir)
    
    if sv.stage_fun == 1:
        if num == 1:
            if dir > 90 and count > 20: dir -= 1 
            if speed > 3 and count > 20: speed -= 0.5
            if dif(2) and while_time(count,60):
                bullet_effect(s_tan1,3,pos)
                bullet(pos,look_at_player(pos),5,3,3)
                
        if num == 2:
            if dir < 270 and count > 30: dir += 1 
            if speed > 3 and count > 30: speed -= 0.5
            if dif(2) and while_time(count,60):
                bullet_effect(s_tan1,3,pos)
                bullet(pos,look_at_player(pos),5,3,3)
        if num == 4:
            if big_small(count,70,130) and speed > 0: speed -= 0.2
            if count > 130 and speed < 5:
                speed += 0.2
            if count == 100:
                add_effect(pos,2,2)
                s_tan1.play()
                for i in range(0,360,30):
                    bullet(pos,look_at_point(pos,sv.player.pos)+i,5,2,2)
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
    if sv.stage_fun == 2:
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
    if sv.stage_fun == 3:
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
    if sv.stage_fun == 4:
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
    if sv.stage_fun == 5:               
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
                list[0] = sv.player.pos
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
    if sv.stage_fun == 6:
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
    
    # 적이동을 위한 값
    sv.boss.image.fill((0,0,0,0))
    sv.boss.move_dir = 0
    sv.boss.move_speed = 0
    sv.boss.move_point = (0,0)
    sv.boss.ready = False
    sv.boss.move_ready = False # 스펠 시작시 움직이는중?
    sv.boss.godmod = False
    sv.boss.dieleft = False
    sv.boss.attack_start = False
    sv.boss.real_appear = False
    sv.boss.died_next_stage = False
    sv.boss.image_num = 0
    if num == 0:
        sv.boss.pos = (WIDTH+64,HEIGHT)
        sv.boss.radius = 0
        sv.boss.image.blit(pokemons[1],(0,0))         
        sv.boss.num = 1
        sv.boss.spell = []
        sv.boss.dies = False
        sv.boss.attack_start = True            
    if num == 1: 
        sv.boss.pos = (WIDTH+64,HEIGHT)
        sv.boss.radius = 40
        sv.boss.image.blit(pokemons[1],(0,0))         
        sv.boss.num = 1
        sv.boss.spell = [sv.spells[0]]
        sv.boss.dies = False
        sv.boss.attack_start = True           
    if num == 2: 
        sv.boss.pos = (WIDTH+64,HEIGHT+64)
        sv.boss.radius = 40
        sv.boss.image.blit(pokemons[1],(0,0))         
        sv.boss.num = 2
        sv.boss.spell = [sv.spells[3],sv.spells[1],sv.spells[2],sv.spells[4]]
        sv.boss.dies = True
        st.boss_background.blit(bg2_image,(0,0),(0,0,540,360))
        sv.text.started = True
    if num == 3: 
        sv.boss.pos = (WIDTH+64,120)
        sv.boss.radius = 40
        sv.boss.image.blit(pokemons[2],(0,0))         
        sv.boss.num = 3
        sv.boss.spell = [sv.spells[5],sv.spells[6]]
        sv.boss.dies = True
        sv.boss.attack_start = True
        st.boss_background.blit(bg2_image,(0,0),(0,360,540,360))
    if num == 4: 
        sv.boss.pos = (WIDTH+64,HEIGHT+64)
        sv.boss.radius = 40
        sv.boss.image.blit(pokemons[3],(0,0))         
        sv.boss.num = 4
        sv.boss.spell = [sv.spells[7],sv.spells[8],sv.spells[9],sv.spells[10],sv.spells[11]]
        sv.boss.dies = True
        st.boss_background.blit(bg2_image,(0,0),(0,360,540,360))
        sv.text.started = True
    if num == 5: 
        sv.boss.pos = (WIDTH+64,640)
        sv.boss.radius = 70
        sv.boss.image.blit(pokemons[8],(0,0))         
        sv.boss.num = 5
        sv.boss.spell = [sv.spells[12],sv.spells[13]]
        sv.boss.dies = True
        sv.boss.attack_start = True
        st.boss_background.blit(bg2_image,(0,0),(0,720,1080,720))
    if num == 6: 
        sv.boss.pos = (WIDTH+64,HEIGHT+64)
        sv.boss.radius = 40
        sv.boss.image.blit(pokemons[7],(0,0))         
        sv.boss.num = num
        sv.boss.spell = [sv.spells[14],sv.spells[15],sv.spells[16],sv.spells[17],sv.spells[18],sv.spells[19],sv.spells[20]]
        sv.boss.dies = True
        st.boss_background.blit(bg2_image,(0,0),(0,720,540,360))
        sv.text.started = True        
    if num == 7: 
        sv.boss.pos = (WIDTH+64,0)
        sv.boss.radius = 70
        sv.boss.image.blit(pokemons[4],(0,0))         
        sv.boss.num = 5
        sv.boss.spell = [sv.spells[21],sv.spells[22]]
        sv.boss.dies = False
        sv.boss.attack_start = True     
    if num == 8: 
        sv.boss.pos = (WIDTH+64,HEIGHT+64)
        sv.boss.radius = 40
        sv.boss.image.blit(pokemons[5],(0,0))         
        sv.boss.num = num
        sv.boss.spell = [sv.spells[23],sv.spells[24],sv.spells[25],sv.spells[26],sv.spells[27],sv.spells[28],sv.spells[29]]
        sv.boss.dies = True
        st.boss_background.blit(bg2_image,(0,0),(540,0,540,360))
        sv.text.started = True        
    if num == 9: 
        sv.boss.pos = (WIDTH+64,0)
        sv.boss.radius = 70
        sv.boss.image.blit(pokemons[6],(0,0))         
        sv.boss.num = 9
        sv.boss.spell = [sv.spells[30],sv.spells[31]]
        sv.boss.dies = False
        sv.boss.attack_start = True  
    if num == 10: 
        sv.boss.pos = (WIDTH+64,HEIGHT+64)
        sv.boss.radius = 40
        sv.boss.image.blit(pokemons[6],(0,0))         
        sv.boss.num = num
        sv.boss.spell = [sv.spells[32],sv.spells[33],sv.spells[34],sv.spells[35],sv.spells[36],sv.spells[37],sv.spells[38]]
        sv.boss.dies = True
        st.boss_background.blit(bg2_image,(0,0),(540,360,540,360))
        sv.text.started = True         
    if num == 11: 
        sv.boss.pos = (WIDTH+64,HEIGHT+64)
        sv.boss.radius = 60
        sv.boss.image.blit(pokemons[9],(0,0))         
        sv.boss.num = num
        sv.boss.spell = [sv.spells[39],sv.spells[40],sv.spells[41],sv.spells[42],sv.spells[43],sv.spells[44],sv.spells[45],sv.spells[46],sv.spells[47]]
        sv.boss.dies = True
        st.boss_background.blit(bg2_image,(0,0),(540,720,540,360))
        sv.text.started = True          
    sv.boss.real_max_health = 0
    sv.boss.radius /= 2
    for i in sv.boss.spell:
        sv.boss.real_max_health += i.health
    sv.boss.real_health = sv.boss.real_max_health
    sv.boss.image2 = sv.boss.image.copy()
    sv.boss.appear = True
    sv.boss.rect = sv.boss.image.get_rect(center = (sv.boss.pos))

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
                    magic_bullet(get_new_pos(sv.player.pos,100),0,0,3,1) 
                    magic_bullet(get_new_pos(sv.player.pos,100),0,0,4,1)
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
                        bullet(calculate_new_xy(pos,60*i,sub,True),look_at_player(sv.boss.pos),1,1,4,11.4)
                    bullet_effect(s_tan1,0,calculate_new_xy(pos,60*3,sub,True))
                    bullet(calculate_new_xy(pos,60*3,sub,True),look_at_player(sv.boss.pos)+30,5,5,3)
                    bullet(calculate_new_xy(pos,60*3,sub,True),look_at_player(sv.boss.pos)-30,5,5,3)
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
                    set_go_boss(5,-look_at_point(pos,(pos[0],sv.player.pos[1]))+randint(-20,20),60)         
        if num == 27:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            sv.boss.box_disable = True
            if ready:
                if while_time(count,2) and sv.boss.move_speed == 20:
                    rand = (randint(-50,50),randint(-50,50))
                    bullet_effect(s_tan1,7,get_new_pos(pos,rand[0],rand[1]))
                    bullet(get_new_pos(pos,rand[0],rand[1]),-sv.boss.move_dir,8,15,7)     
                if while_time(count,3) and sv.boss.list[0]:
                    sub = -(count * 4.2 + 45)
                    for i in range(2,4):
                        bullet_effect(s_tan1,7,calculate_new_xy(pos,60*i,sub,True))
                        bullet(calculate_new_xy(pos,60*i,sub,True),-sub-90,4,1,7)                       
                if while_time(count,60):
                    set_go_boss(20,-look_at_point(pos,(0,sv.player.pos[1])),999)                
                if pos[0] < 64 and not sv.boss.list[0]:
                    sv.boss.move_speed = 5
                    sv.boss.list[0] = True
                    s_enep2.play()
                    sv.boss.health -= 80
                    for i in range(0,360,10):
                        bullet(get_new_pos(pos),i,4,9,7)   
                if sv.boss.list[0]:
                    sv.boss.move_dir = 0
                    if pos[0] >= WIDTH-100:
                        sv.boss.move_speed = 0
                        sv.boss.move_time = 0
                        sv.boss.list[0] = False
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
            sv.boss.box_disable = True
            if ready:            
                if while_time(count,100):
                    set_go_boss(10,-look_at_player(pos),50)  
                if while_time(count,4) and not sv.boss.move_time > 0 and count > 100:  
                    bullet_effect(s_tan1,5,pos)  
                    for i in range(0,360,45):                       
                        bullet(pos,count+i,3,7,5)  
                    if while_time(count,16):
                        for i in range(0,10):                       
                            bullet(pos,look_at_player(pos)+i/2,10-i+1,4,5,0.1)
                            bullet(pos,look_at_player(pos)-i/2,10-i+1,4,5,0.1) 
                if sv.boss.move_time > 0:
                    sv.boss.health -= 3
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
                    sv.boss.list[0] = look_at_player(pos)
                    count = 0
                if while_time(count,2) and count < 30:
                    bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-sv.boss.list[0],True))  
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0]+20,6,1,1,14.6,[sv.boss.list[0]])   
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0]-20,6,1,1,14.6,[sv.boss.list[0]])    
                if while_time(count,40):
                    bullet_effect(s_tan2,6,pos)  
                    for i in range(0,360,10):
                        bullet(pos,i,4,2,6)    
        if num == 32:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready: 
                if while_time(count,40):
                    sv.boss.list[0] = look_at_player(pos)
                    count = 0
                if while_time(count,5) and count < 30:
                    bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-sv.boss.list[0],True))  
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0]+60,12,1,1,14.6,[sv.boss.list[0]])   
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0]-60,12,1,1,14.6,[sv.boss.list[0]]) 
                if when_time(count,30):
                    bullet_effect(s_tan1,1,pos)  
                    bullet(pos,sv.boss.list[0],8,15,1)  
        if num == 33:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready: 
                if while_time(count,40):
                    sv.boss.list[0] = look_at_player(pos)
                    count = 0
                if while_time(count,2) and count < 30:
                    bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-sv.boss.list[0],True))  
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0]+20,6,1,1,14.6,[sv.boss.list[0]])   
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0]-20,6,1,1,14.6,[sv.boss.list[0]])    
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
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0],3,3,7)    
                if while_time(count,40):
                    for i in range(0,HEIGHT,20):
                        bullet((WIDTH,i+10),180,3,12,2) 
        if num == 35:
            pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
            if ready: 
                if while_time(count,30):
                    bullet_effect(s_tan1,4,calculate_new_xy(pos,100,-sv.boss.list[0]+90,True))
                    bullet_effect(s_tan1,4,calculate_new_xy(pos,100,-sv.boss.list[0]-90,True))
                    bullet_effect(s_tan1,4,calculate_new_xy(pos,100,-sv.boss.list[0]+180,True))
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0]+90,True),look_at_player(calculate_new_xy(pos,100,-sv.boss.list[0]+90,True)),5,15,4)   
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0]-90,True),look_at_player(calculate_new_xy(pos,100,-sv.boss.list[0]-90,True)),5,15,4) 
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0]+180,True),look_at_player(calculate_new_xy(pos,100,-sv.boss.list[0]+180,True)),5,15,4) 
                    sv.boss.list[0] = look_at_player(pos)
                    count = 0
                if while_time(count,5):
                    bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-sv.boss.list[0],True))  
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0]+40,12,1,1,14.3,[sv.boss.list[0]])   
                    bullet(calculate_new_xy(pos,100,-sv.boss.list[0],True),sv.boss.list[0]-40,12,1,1,14.3,[sv.boss.list[0]]) 
                if when_time(count,30):
                    bullet_effect(s_tan1,1,pos)  
                    bullet(pos,sv.boss.list[0],8,15,1) 
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
                    sv.boss.list[0] += 2
                if while_time(count,4):
                    for i in range(0,360,30):
                        bullet_effect(s_tan1,1,calculate_new_xy(pos,100,-sv.boss.list[0]+i,True))  
                        bullet(calculate_new_xy(pos,100,-sv.boss.list[0]+i,True),sv.boss.list[0]+40+i,5,10,randint(6,7))   
                        bullet(calculate_new_xy(pos,100,-sv.boss.list[0]+i,True),sv.boss.list[0]-40+i,5,10,randint(6,7))
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
                    sv.boss.list[0] = look_at_player(pos)
                if while_time(count,2) and big_small(count,60,180):
                    bullet_effect(0,6,pos)
                    bullet(pos,sv.boss.list[0]+45,12,0,6,18)
                    bullet(pos,sv.boss.list[0]-45,12,0,6,18)
                if when_time(count,300):
                    count = 0
                    set_go_boss(1,randint(0,359),120) 
    if num == 40:
        pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
        if ready: 
            if while_time(count,20):
                rand = get_new_pos(sv.boss.pos,randint(-100,100),randint(-100,100))
                bullet_effect(s_tan1,1,rand)
                for i in range(0,360,12):
                    bullet(rand,i,2.5,3,7)
            if while_time(count+20,40):
                rand = get_new_pos(sv.boss.pos,randint(-100,100),randint(-100,100))
                bullet_effect(s_tan1,1,rand)
                for i in range(0,360,12):
                    bullet(rand,i,3,3,1)
            if when_time(count,100):
                add_effect(pos,8)
                s_ch0.play()
                sv.boss.fire_field = [300,120]  
            if when_time(count,100+60*5):
                sv.boss.fire_field = [-300,120] 
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
                sv.boss.fire_field = [300,30]
            if when_time(count,270):
                sv.boss.fire_field = [-300,30]  
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
                sv.boss.fire_field = [300,60]        
            if while_time(count,180):
                add_effect(pos,8)
                sv.boss.fire_field = [-300,60]   
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
                sv.boss.fire_field = [120,30]        
            if while_time(count,300):
                sv.boss.fire_field = [-120,30]
            if while_time(count,120) and count > 240:
                bullet(pos,look_at_player(pos),5,19,6)   
    if num == 44:
        pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
        if ready:   
            if while_time(count,8):
                bullet_effect(s_kira1,1,pos)   
                bullet(calculate_new_xy(pos,50,-look_at_player(pos)-90,True),look_at_player(sv.boss.pos),10,18,1)  
                bullet(calculate_new_xy(pos,50,-look_at_player(pos)+90,True),look_at_player(sv.boss.pos),10,18,1)
            if when_time(count,60):
                set_go_boss(3,choice([60,120,-60,-120]),60)
            if when_time(count,100):
                add_effect(pos,8) 
            if while_time(count,2) and big_small(count,120,240):  
                bullet_effect(s_tan1,1,calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True))   
                bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(sv.boss.pos)+randint(-10,10)+15,12,15,1) 
                bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(sv.boss.pos)+randint(-10,10)+15,8,12,1)
                bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(sv.boss.pos)+randint(-10,10)-15,12,15,1) 
                bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(sv.boss.pos)+randint(-10,10)-15,8,12,1)
                bullet(calculate_new_xy(pos,20,-look_at_player(pos)+randint(-15,15),True),look_at_player(sv.boss.pos),7,3,3)
            if when_time(count,180):
                set_go_boss(3,choice([60,120,-60,-120]),60)
            if when_time(count,300):
                count = 0   
    if num == 45:
        sv.boss.box_disable = True
        pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
        if ready:   
            if sv.boss.list[0] % 2 == 0:
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
                sv.boss.fire_field = (120,60)
                set_go_boss(7,-look_at_player(pos),60)   
            if when_time(count,390):   
                s_ch0.play()
                sv.boss.fire_field = (240,60)
                set_go_boss(7,-look_at_player(pos),60)
            if when_time(count,540):   
                sv.boss.fire_field = (-240,60)
                set_go_boss(7,-look_at_point(pos,boss_movebox.center),60)
                count=0
                sv.boss.fire_field = (0,0)
                sv.boss.fire_field_radius = 0
                sv.boss.list[0] += 1                  
    if num == 46:
        pos = set_bossmove_point((WIDTH-150,HEIGHT//2,0),120,3)
        if ready:
            if while_time(count,20):
                bullet_effect(s_kira1,0,0,True)
                for i in range(0,15):
                    bullet((WIDTH+8,i*2*HEIGHT/30+15),180+randint(-5,5),2,6,1)
            if while_time(count+70,190):
                s_ch0.play()
                set_go_boss(3,-look_at_point(pos,(pos[0],sv.player.pos[1])),60)
                sv.boss.fire_field = (120,60)
            if while_time(count,190):
                sv.boss.fire_field = (0,0)
                sv.boss.fire_field_radius = 0
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
                            rand = sv.player.pos[1]+randint(-50,50)
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
        sv.boss.box_disable = True
        pos = set_bossmove_point((WIDTH//2,HEIGHT//2,0),120,3)
        if ready:
            if count == 1:
                add_effect(pos,8)
                sv.boss.list[0] = 0
            if count == 60:
                s_enep2.play()            
            if count > 60:
                if sv.boss.list[0]>3:
                    if while_time(count,1):
                        for i in range(0,360,90):
                            bullet(pos,i+count//1.5,17,15,1)    
                else:
                    if while_time(count,1):
                        for i in range(0,360,90):
                            bullet(pos,i+count//2,15,3,1)  
                if while_time(count,60) and sv.boss.list[0]>0:
                    bullet_effect(s_tan1,7,pos)
                    for i in range(0,360,10):
                        bullet(pos,count*2.7+i,3,3,7)    
                if while_time(count,180) and sv.boss.list[0]>1:
                    bullet_effect(s_kira0,0,0,True)
                    for i in range(0,360,10):
                        bullet(calculate_new_xy(pos,720,-count*1.7-i,True),count*1.7+i+180,2,10,6,23) 
                if while_time(count,20) and sv.boss.list[0]>2:
                    bullet_effect(s_tan2,5,pos)
                    for i in range(0,360,45):
                        bullet(pos,i,4,7,5)
                if sv.boss.health<=sv.boss.max_health-round(sv.boss.max_health/5)*(sv.boss.list[1]+1):
                    sv.boss.health -= 1
                    s_enep2.play()     
                    bullet_clear()
                    sv.boss.list[1] += 1
                    sv.boss.list[0] += 1
    
    if ready:pos = go_boss()
    else:pos = calculate_new_xy(pos,sv.boss.move_speed,sv.boss.move_dir)
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
        if sv.boss.count == 240:
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
        if sv.boss.count == 90:
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
        if sv.boss.count == 30:
            self.direction = self.num[0]
            self.speed = sub
    if mod == 15:
        if sv.boss.count == 60:
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
        if distance(self.pos,(sv.boss.pos[0]*2,sv.boss.pos[1]*2)) <= 70:
            self.kill()
    if mod == 20:
        if while_time(sv.boss.count,540):
            sbullet_effect(s_kira1,0,0,True)
            self.speed += 5
    if mod == 21:
        if self.speed > 6:
            self.speed = 6
        if distance(self.pos,(sv.player.pos[0]*2,sv.player.pos[1]*2)) <= 100:
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
        if distance((self.pos[0]//2,self.pos[1]//2),sv.boss.pos) <= 20:
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
        self.pos = move_circle(sv.player.pos,self.count*3,150)
        if while_time(self.count,6):
            bullet_effect(s_tan1,4,self.pos)
            bullet(self.pos,look_at_player(self.pos),2,10,4,0.1)
            bullet(self.pos,look_at_player(self.pos)+90,5,16,4)
            bullet(self.pos,look_at_player(self.pos)+85,4,16,5)
            bullet(self.pos,look_at_player(self.pos)+95,6,16,5)
    if mod == 4:
        self.count += 1
        self.pos = move_circle(sv.player.pos,self.count*3+180,200)
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
    
    if sv.stage_end <= 0:
        if True:
            if sv.stage_condition == 1:
                add_effect((WIDTH/2,HEIGHT/2),99)
                sv.stage_fun += 1
                sv.stage_count = 0
                sv.stage_condition += 1
            if sv.stage_condition == 2:
                sv.stage_count += 1
                if sv.stage_count >= 60:
                    sv.stage_condition += 1
            if sv.stage_condition == 3:
                game_defalt_setting(sv.stage_fun)
                sv.player.pos = (WIDTH/4,HEIGHT/2)
                sv.stage_condition += 1
            if sv.stage_condition == 4:
                sv.stage_count += 1
                if sv.stage_count >= 180:
                    sv.stage_condition += 1
            if sv.stage_condition == 5:
                pygame.mixer.music.play(-1)
                sv.stage_condition += 1
                sv.stage_count = 0
        if sv.stage_condition == 6:
            if sv.stage_fun == 1:
                if sv.stage_challenge == 0:
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
                if sv.stage_challenge == 1:
                    bground_spawn(1,1)
                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-sv.stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,sv.stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(sv.stage_repeat_count,3):
                            pokemon_spawn(4,(WIDTH+64,HEIGHT-sv.stage_repeat_count*HEIGHT/10-20),0,180,4,True)
                        end_while_poke_spawn(2,10)

                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-sv.stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,sv.stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(sv.stage_repeat_count,3):
                            pokemon_spawn(4,(WIDTH+64,sv.stage_repeat_count*HEIGHT/10+20),0,180,4,True)
                        end_while_poke_spawn(2,10)

                    if while_poke_spawn(10,15,2):
                        pokemon_spawn(5,(WIDTH,20),10)
                        pokemon_spawn(6,(WIDTH,HEIGHT-20),0)
                        end_while_poke_spawn(2,15)

                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-sv.stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,sv.stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(sv.stage_repeat_count,2):
                            pokemon_spawn(4,(WIDTH+64,HEIGHT-sv.stage_repeat_count*HEIGHT/10-20),0,180,4,True)
                            pokemon_spawn(4,(WIDTH+64,sv.stage_repeat_count*HEIGHT/10+20),0,180,4,True)
                        end_while_poke_spawn(2,10)
                    
                    next_challenge(240)
                if sv.stage_challenge == 2:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(1)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        sv.boss.died_next_stage = False
                        next_challenge(0)
                if sv.stage_challenge == 3:
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
                if sv.stage_challenge == 4:
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
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-sv.stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,sv.stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(sv.stage_repeat_count,3):
                            pokemon_spawn(4,(WIDTH+64,HEIGHT-sv.stage_repeat_count*HEIGHT/10-20),0,180,4,True)
                        if while_time(sv.stage_repeat_count,2):
                            pokemon_spawn(7,(WIDTH-120,HEIGHT+30),0,-90,4,True)
                        end_while_poke_spawn(2,10)
                    if while_poke_spawn(40,10,2):
                        pokemon_spawn(3,(WIDTH+64,HEIGHT-sv.stage_repeat_count*HEIGHT/10-20),40)
                        pokemon_spawn(3,(WIDTH+64,sv.stage_repeat_count*HEIGHT/10+20),0)
                        if while_time(sv.stage_repeat_count,3):
                            pokemon_spawn(4,(WIDTH+64,sv.stage_repeat_count*HEIGHT/10+20),0,180,4,True)
                        if while_time(sv.stage_repeat_count,2):
                            pokemon_spawn(7,(WIDTH-120,-30),0,-90,4,True)
                        end_while_poke_spawn(2,10)
                    next_challenge(360)
                if sv.stage_challenge == 5:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(2)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        if not sv.text.started:
                            sv.stage_challenge = 0
                            sv.stage_line = 0
                            sv.text.re_start()
                            sv.stage_end = 60
                            sv.stage_condition = 1
                            sv.boss.died_next_stage = False   
            if sv.stage_fun == 2:
                if sv.stage_challenge == 0:
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
                if sv.stage_challenge == 1:

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
                if sv.stage_challenge == 2:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(3)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        sv.boss.died_next_stage = False
                        next_challenge(0)
                if sv.stage_challenge == 3:
                    pokemon_spawn(9.2,(WIDTH+32,HEIGHT//2+60),30)
                    pokemon_spawn(9.2,(WIDTH+32,HEIGHT//2-60),0)
                    if while_poke_spawn(40,10,1):
                        pokemon_spawn(11,(WIDTH+32,randint(100,HEIGHT-100)),40)
                        end_while_poke_spawn(1,10)

                    pokemon_spawn(10,(WIDTH+32,HEIGHT/10*sv.stage_repeat_count),120)
                    if while_poke_spawn(20,10,1):
                        pokemon_spawn(10,(WIDTH+32,HEIGHT/10*sv.stage_repeat_count),20)
                        end_while_poke_spawn(1,10)
                    if while_poke_spawn(20,10,1):
                        pokemon_spawn(10,(WIDTH+32,HEIGHT-HEIGHT/10*sv.stage_repeat_count),20)
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
                        pokemon_spawn(10,(WIDTH+32,HEIGHT/10*sv.stage_repeat_count),20)
                        pokemon_spawn(10,(WIDTH+32,HEIGHT-HEIGHT/10*sv.stage_repeat_count),0)
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
                if sv.stage_challenge == 4:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(4)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        if not sv.text.started:
                            sv.stage_challenge = 0
                            sv.stage_line = 0
                            sv.text.re_start()
                            sv.stage_end = 60
                            sv.stage_condition = 1   
                            sv.boss.died_next_stage = False   
            if sv.stage_fun == 3:
                if sv.stage_challenge == 0:
                    pokemon_spawn(12,RIGHT_POS[1],120,-135,4)
                    pokemon_spawn(12,RIGHT_POS[2],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[3],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[4],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[5],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[6],10,-135,4)
                    pokemon_spawn(12,RIGHT_POS[7],10,-135,4)
                    title_spawn(3,120)
                    next_challenge(260)
                if sv.stage_challenge == 1:
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
                if sv.stage_challenge == 2:
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
                if sv.stage_challenge == 3:
                    if while_poke_spawn(80,6,2):
                        pokemon_spawn(15,RIGHT_POS[1+sv.stage_repeat_count],80,180,5)
                        pokemon_spawn(15,RIGHT_POS[7-sv.stage_repeat_count],0,180,5)
                        end_while_poke_spawn(2,6)
                    if while_poke_spawn(20,10,1):
                        pokemon_spawn(12,RIGHT_POS[6],20,-135,5)
                        end_while_poke_spawn(1,10)
                    next_challenge(120,True)
                if sv.stage_challenge == 4:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(5)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        sv.boss.died_next_stage = False
                        next_challenge(0)   
                if sv.stage_challenge == 5:
                    if while_poke_spawn(80,8,1):
                        if sv.stage_repeat_count % 2 == 0:
                            pokemon_spawn(13,RIGHT_POS[2],80,180,5)
                        else:
                            pokemon_spawn(13,RIGHT_POS[6],80,180,5)
                        if sv.stage_repeat_count > 4:
                            pokemon_spawn(15,RIGHT_POS[4],0,180,5,True)
                        end_while_poke_spawn(1,8)  
                    next_challenge(120)          
                if sv.stage_challenge == 6:
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
                if sv.stage_challenge == 7:
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
                if sv.stage_challenge == 8:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(6)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        if not sv.text.started:
                            sv.stage_challenge = 0
                            sv.stage_line = 0
                            sv.text.re_start()
                            sv.stage_end = 60
                            sv.stage_condition = 1 
                            sv.boss.died_next_stage = False   
            if sv.stage_fun == 4:
                if sv.stage_challenge == 0:
                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(17,choice(UP_POS),10,randint(90,110),4)
                        end_while_poke_spawn(1,24)

                    title_spawn(4,120)
                    next_challenge(260)
                if sv.stage_challenge == 1:
                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(17,RIGHT_POS[2],10,170,5)
                        if sv.stage_repeat_count == 0:
                            pokemon_spawn(18,RIGHT_POS[6],0,200,4,True)
                        if sv.stage_repeat_count == 12:
                            pokemon_spawn(18.4,RIGHT_POS[5],0,200,4,True)
                        end_while_poke_spawn(1,24) 
                    waiting(120)                   
                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(17,RIGHT_POS[6],10,190,5)
                        if sv.stage_repeat_count == 0:
                            pokemon_spawn(18,RIGHT_POS[2],0,160,4,True)
                        if sv.stage_repeat_count == 12:
                            pokemon_spawn(18.4,RIGHT_POS[3],0,160,4,True)
                        end_while_poke_spawn(1,24)
                    waiting(120) 
                    if while_poke_spawn(10,24,2):
                        pokemon_spawn(17,RIGHT_POS[6],10,190,5)
                        pokemon_spawn(17,RIGHT_POS[2],0,170,5)
                        if sv.stage_repeat_count == 0:
                            pokemon_spawn(18,RIGHT_POS[4],0,180,4,True)
                        if sv.stage_repeat_count == 12:
                            pokemon_spawn(18.4,RIGHT_POS[4],0,180,4,True)
                        end_while_poke_spawn(2,24)
                    next_challenge(60,True)
                if sv.stage_challenge == 2:
                    pokemon_spawn(19.5,RIGHT_POS[4],60,180,5)
                    pokemon_spawn(19,RIGHT_POS[3],420,180,5)
                    pokemon_spawn(19,RIGHT_POS[5],0,180,5)
                    pokemon_spawn(19,RIGHT_POS[2],420,180,5)
                    pokemon_spawn(19,RIGHT_POS[6],0,180,5)
                    next_challenge(660,True)
                if sv.stage_challenge == 3:
                    if while_poke_spawn(30,7,1):
                        pokemon_spawn(20,choice([DOWN_POS[2],DOWN_POS[3],DOWN_POS[4]]),30,-90,0)
                        if sv.stage_repeat_count>3:
                            pokemon_spawn(17,choice([RIGHT_POS[5],RIGHT_POS[3],RIGHT_POS[4]]),60,180,7,True)
                            pokemon_spawn(17,choice([RIGHT_POS[5],RIGHT_POS[3],RIGHT_POS[4]]),60,180,7,True)
                        end_while_poke_spawn(1,7)
                    waiting(120)
                    if while_poke_spawn(30,7,1):
                        pokemon_spawn(20,choice([UP_POS[2],UP_POS[3],UP_POS[4]]),30,90,0)
                        if sv.stage_repeat_count>3:
                            pokemon_spawn(17,choice([RIGHT_POS[5],RIGHT_POS[3],RIGHT_POS[4]]),60,180,7,True)
                            pokemon_spawn(17,choice([RIGHT_POS[5],RIGHT_POS[3],RIGHT_POS[4]]),60,180,7,True)
                        end_while_poke_spawn(1,7)
                    next_challenge(240)
                if sv.stage_challenge == 4:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(7)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        sv.boss.died_next_stage = False
                        next_challenge(0) 
                if sv.stage_challenge == 5:
                    if while_poke_spawn(10,60,1):
                        pokemon_spawn(17,choice([RIGHT_POS[1],RIGHT_POS[2],RIGHT_POS[3],RIGHT_POS[4]]),10,randint(150,170),7)
                        if while_time(sv.stage_repeat_count,10):
                            pokemon_spawn(18,RIGHT_POS[4],0,180,6,True)
                        end_while_poke_spawn(1,30)    
                    waiting(120)                            
                    if while_poke_spawn(10,60,1):
                        pokemon_spawn(17,choice([RIGHT_POS[7],RIGHT_POS[6],RIGHT_POS[5],RIGHT_POS[4]]),10,randint(190,210),7)
                        if while_time(sv.stage_repeat_count,10):
                            pokemon_spawn(18,RIGHT_POS[4],0,180,6,True)
                        end_while_poke_spawn(1,30)    
                    waiting(120) 
                    if while_poke_spawn(10,60,1):
                        pokemon_spawn(17,choice([RIGHT_POS[1],RIGHT_POS[2],RIGHT_POS[3],RIGHT_POS[4]]),10,randint(150,170),7)
                        if while_time(sv.stage_repeat_count,29):
                            pokemon_spawn(19,RIGHT_POS[5],0,180,6,True)
                        end_while_poke_spawn(1,30)    
                    waiting(120) 
                    if while_poke_spawn(10,60,1):
                        pokemon_spawn(17,choice([RIGHT_POS[7],RIGHT_POS[6],RIGHT_POS[5],RIGHT_POS[4]]),10,randint(190,210),7)
                        if while_time(sv.stage_repeat_count,29):
                            pokemon_spawn(19.2,RIGHT_POS[3],0,180,6,True)
                        end_while_poke_spawn(1,30)    
                    next_challenge(240)
                if sv.stage_challenge == 6:
                    if while_poke_spawn(100,8,1):
                        pokemon_spawn(20,(sv.player.pos[0],HEIGHT+64),100,-90,0)
                        if sv.stage_repeat_count > 3:
                            pokemon_spawn(17.4,(WIDTH + 64,sv.player.pos[1]),0,172,7,True)
                            pokemon_spawn(17.4,(WIDTH + 64,sv.player.pos[1]),0,174,6,True)
                            pokemon_spawn(17.4,(WIDTH + 64,sv.player.pos[1]),0,176,5,True)
                            pokemon_spawn(17.4,(WIDTH + 64,sv.player.pos[1]),0,178,4,True)
                            if sv.stage_repeat_count == 7:
                                pokemon_spawn(17 if sv.stage_repeat_count == 7 else 17.5,(WIDTH + 64,sv.player.pos[1]),0,180,3,True)
                        end_while_poke_spawn(1,8)     
                    next_challenge(120)  
                if sv.stage_challenge == 7:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(8)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        if not sv.text.started:
                            sv.stage_challenge = 0
                            sv.stage_line = 0
                            sv.text.re_start()
                            sv.stage_end = 60
                            sv.stage_condition = 1     
                            sv.boss.died_next_stage = False                                            
            if sv.stage_fun == 5:
                if sv.stage_challenge == 0:
                    if while_poke_spawn(10,24,1):
                        pokemon_spawn(21,choice(RIGHT_POS2),10,180,4)
                        end_while_poke_spawn(1,24)
                    title_spawn(5,120)
                    next_challenge(240)                
                if sv.stage_challenge == 1:
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
                if sv.stage_challenge == 2:
                    pokemon_spawn(23,RIGHT_POS[2],1,160,5)   
                    pokemon_spawn(23,RIGHT_POS[6],300,-160,5)  
                    pokemon_spawn(23.4,RIGHT_POS[4],200,-160,5) 
                    waiting(280)
                    if while_poke_spawn(10,140,1):
                        pokemon_spawn(21,choice(DOWN_POS),10,-90,randint(4,5)) 
                        if when_time(sv.stage_repeat_count,24):
                            pokemon_spawn(22.2,RIGHT_POS2[1],0,170,5,True) 
                        if when_time(sv.stage_repeat_count,48):
                            pokemon_spawn(22.4,RIGHT_POS2[2],0,170,5,True) 
                        if when_time(sv.stage_repeat_count,72):
                            pokemon_spawn(22.2,RIGHT_POS2[3],0,170,5,True) 
                        if when_time(sv.stage_repeat_count,96):
                            pokemon_spawn(22.4,RIGHT_POS2[4],0,170,5,True) 
                        end_while_poke_spawn(1,92)      

                    pokemon_spawn(23,RIGHT_POS[3],60,160,5)  
                    pokemon_spawn(23.3,RIGHT_POS[5],0,-160,5)
                    next_challenge(360)
                if sv.stage_challenge == 3:
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
                if sv.stage_challenge == 4:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(9)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        sv.boss.died_next_stage = False
                        next_challenge(0) 
                if sv.stage_challenge == 5:
                    pokemon_spawn(25,RIGHT_POS[4],60,180,12) 
                    pokemon_spawn(25.2,RIGHT_POS[4],120,180,12)
                    pokemon_spawn(25.5,RIGHT_POS[4],60,180,12)
                    if while_poke_spawn(20,32,2): 
                        pokemon_spawn(26,RIGHT_POS[7],20,180,5) 
                        pokemon_spawn(21,RIGHT_POS[4],0,randint(170,190),5) 
                        if while_time(sv.stage_repeat_count,14):
                            pokemon_spawn(22.4,RIGHT_POS[4],0,180,5,True) 
                        if when_time(sv.stage_repeat_count,16):
                            pokemon_spawn(23.4,RIGHT_POS[2],0,160,6,True)
                        end_while_poke_spawn(2,32)
                    next_challenge(300) 
                if sv.stage_challenge == 6:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(10)
                    if sv.boss.died_next_stage:
                        sv.stage_count = 0
                        if not sv.text.started:
                            sv.stage_challenge = 0
                            sv.stage_line = 0
                            sv.text.re_start()
                            sv.stage_end = 60
                            sv.stage_condition = 1    
                            sv.boss.died_next_stage = False                  
            if sv.stage_fun == 6:              
                if sv.stage_challenge == 0:
                    title_spawn(6,120)
                    waiting(60*4)
                    if while_poke_spawn(20,20,1):
                        pokemon_spawn(27,(WIDTH+64,16+sv.stage_repeat_count*15),20,180,6)
                        end_while_poke_spawn(1,20)
                    if while_poke_spawn(20,20,1):
                        pokemon_spawn(27,(WIDTH+64,HEIGHT-16-sv.stage_repeat_count*15),20,180,6)
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
                if sv.stage_challenge == 1:
                    pokemon_spawn(30,RIGHT_POS[4],180,180,2)
                    pokemon_spawn(30,RIGHT_POS[1],120,180,2)
                    pokemon_spawn(30,RIGHT_POS[5],120,180,2)
                    pokemon_spawn(30,RIGHT_POS[6],120,180,2)
                    pokemon_spawn(30,RIGHT_POS[2],120,180,2)
                    pokemon_spawn(30,RIGHT_POS[3],120,180,2)
                    waiting(360)
                    if while_poke_spawn(20,20,1):
                        pokemon_spawn(27.2,(WIDTH+64,16+sv.stage_repeat_count*15),20,180,6)
                        end_while_poke_spawn(1,20)
                    pokemon_spawn(29.4,RIGHT_POS[4],90,180,6)
                    waiting(90)
                    if while_poke_spawn(20,20,1):
                        pokemon_spawn(27.2,(WIDTH+64,HEIGHT-16-sv.stage_repeat_count*15),20,180,6)
                        end_while_poke_spawn(1,20) 
                    next_challenge(360)
                if sv.stage_challenge == 2:
                    if not sv.boss.appear and not sv.boss.died_next_stage: 
                        boss_spawn(11)  
                
            sv.stage_cline = 0
    else:
        sv.stage_end -= 1