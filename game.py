from turtle import position
from cv2 import circle
import pygame, math
from random import randint, uniform, choice
from pygame.locals import *
import cv2
import numpy
import time
import start as st
import stage_var as sv
from start import render_layer, WIDTH, HEIGHT, TITLE, FONT_1, FONT_2, score_font, pokemons, menu_img, monitor_size
from start import s_boom, s_cancel, s_cat1, s_ch0, s_ch2, s_damage0, s_damage1, s_enedead, s_enep1, s_enep2, s_graze, s_item0, s_kira0, s_kira1, s_lazer1, s_ok, s_pause, s_pldead, s_plst0, s_select, s_slash, s_tan1, s_tan2
# 게임에 핵심적인 기능만 주석을 넣었습니다 ##
pygame.init()
pygame.mixer.pre_init(44100,-16,2,512)
screen = pygame.display.set_mode((WIDTH*2,HEIGHT*2))
    # 플레이어
def play_game():
    global screen
    st.music_and_sfx_volume()    
    # global bkgd, time_stop
    # global stage_count, boss_group, screen_shake_count, pause, add_dam, drilling,cur_count,game_clear 
    # 초기 설정


    # 소환 반복 (줄에 stage_line)
    ################################################# 
    while sv.play:
        # 60 프레임
        st.clock.tick(st.clock_fps)
        now = st.time.time()        
        st.dt = (now-st.prev_time)*st.TARGET_FPS        
        prev_time = now
        keys = pygame.key.get_pressed() 
        if sv.cur_screen == 1:
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
                    if not player.died:player_hitbox.update()
                    if beams_group: beams_group.update()                            
                    player_group.update(hit_list)
                    if enemy_group:enemy_group.update()
                    if item_group: item_group.update()
                    if boss.appear: boss_group.update(boss_collide)
                    if effect_group: effect_group.update()
                    if not player.died:player_sub.update()
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
        if sv.cur_screen == 0:
            if sv.frame_count == 0 and not sv.game_clear:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(TITLE)
                pygame.mixer.music.play(-1)
                sv.frame_count -= 1
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    play = False
                if ev.type == pygame.KEYDOWN: 
                    if not sv.game_clear:
                        if ev.key == pygame.K_f:
                            sv.full_on = False if full_on == True else True  
                        if ev.key == pygame.K_UP:
                            sv.curser = curser_max if sv.curser == 0 else sv.curser - 1 # 커서위로
                            st.s_ok.play()
                        if ev.key == pygame.K_DOWN:
                            sv.curser = 0 if sv.curser == curser_max else sv.curser + 1 # 커서밑으로
                            st.s_ok.play()
                        if sv.select_mod == 0: # 시작화면
                            if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                st.s_select.play()
                                if sv.curser == 5: play = False # 게임끄기
                                else:sv.select_mod += 1 ############ 게임시작
                                sv.menu_mod.append(sv.curser) # 현재 어떤 버튼 눌렀는지 저장
                                sv.curser = 0
                                break
                        if sv.select_mod == 1:
                            if sv.menu_mod[0] == 0:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    sv.select_mod += 1
                                    sv.menu_mod.append(sv.curser)
                                    s_select.play()
                                    sv.curser = 0
                                    break 
                                    
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    sv.curser = 0
                                    sv.select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]      
                                    break             
                            if sv.menu_mod[0] == 1:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    sv.select_mod += 1
                                    sv.menu_mod.append(curser)
                                    s_select.play()
                                    sv.curser = 0
                                    break 
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    sv.curser = 0
                                    sv.select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]   
                                    break 
                                if ev.key == pygame.K_RIGHT or ev.key == pygame.K_LEFT:
                                    s_select.play()
                                    sv.character = 41 if sv.character == 0 else 0      
                            if sv.menu_mod[0] == 2:
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    sv.curser = 0
                                    sv.select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]   
                                    break
                            if sv.menu_mod[0] == 3:
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    sv.curser = 0
                                    select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]   
                                    break
                            if sv.menu_mod[0] == 4:
                                if ev.key == pygame.K_RIGHT:
                                    s_ok.play()
                                    if sv.curser == 0:
                                        sv.full_on = 1 if sv.full_on == 0 else 0
                                    if sv.curser == 1:
                                        mmusic_volume = mmusic_volume + 5 if mmusic_volume < 100 else 100
                                    if sv.curser == 2:
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
                                    music_and_sfx_volume()
                                    with open('resources\setting.txt','w',encoding="UTF-8") as f:
                                        f.write("fullscreen"+"="+str(full_on)+"\n")
                                        f.write("sfx"+"="+str(msfx_volume)+"\n")
                                        f.write("bgm"+"="+str(mmusic_volume)+"\n")
                                    curser = 0
                                    select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]     
                                    break                        
                        if sv.select_mod == 2:
                            if sv.menu_mod[0] == 0:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    s_select.play()
                                    character = 0 if curser == 0 else 41
                                    difficult = sv.menu_mod[1]
                                    sv.player.power = 0
                                    cur_screen = 1  
                                    stage_fun = 0
                                    start_fun = stage_fun
                                    frame_count = 0
                                    curser = 0
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    curser = sv.menu_mod[1]
                                    sv.select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]   
                                    break 
                                
                            if sv.menu_mod[0] == 1:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    s_select.play()                                    
                                    sv.player.power = 400
                                    stage_fun = sv.menu_mod[1]                                 
                                    start_fun = stage_fun  
                                    if curser == 1:
                                        if sv.menu_mod[1] == 0:stage_challenge = 5
                                        if sv.menu_mod[1] == 1:stage_challenge = 4
                                        if sv.menu_mod[1] == 2:stage_challenge = 8
                                        if sv.menu_mod[1] == 3:stage_challenge = 7
                                        if sv.menu_mod[1] == 4:stage_challenge = 6
                                        if sv.menu_mod[1] == 5:stage_challenge = 2
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
                                old_score = int(st.score_scroll[0][2:])
                                if old_score < score:
                                    st.score_scroll[0] = "H:"+str(score).zfill(10)
                                    st.score_scroll[0] = st.score_scroll[0]
                            else:
                                old_score = int(st.score_scroll[1][2:])
                                if old_score < score:
                                    st.score_scroll[1] = "F:"+str(score).zfill(10)
                                    st.score_scroll[1] = st.score_scroll[1]
                            with open('resources\score.txt','w',encoding="UTF-8") as f:
                                f.write(st.score_scroll[0]+"\n")
                                f.write(st.score_scroll[1]+"\n")
                                
                            game_restart = True
            if st.game_restart:
                sv.frame_count = 0
                break    
            render_layer.blit(st.background_img,(0,0))            
            ui_x = WIDTH - 180
            ui_y = 20
            if not sv.game_clear:
                if sv.select_mod == 0: # 시작화면
                    curser_max = 5
                    render_layer.blit(st.title_img,(0,0))# 타이틀
                    for i in range(0,6): # 메뉴 그리기
                        menu = pygame.Surface((160,32), SRCALPHA)
                        if sv.curser == i: menu.fill((0,0,255,200))
                        menu.blit(st.menu_img,(0,0),(0,48+32*i,320,48))
                        render_layer.blit(menu,(ui_x,ui_y+32*i))
                    text1 = st.score_font.render(st.score_scroll[0], True, (0,0,0))
                    render_layer.blit(text1,(0,HEIGHT-60))
                    text1 = st.score_font.render(st.score_scroll[1], True, (0,0,0))
                    render_layer.blit(text1,(2,HEIGHT-30))
                if sv.select_mod == 1: # 다음옴션
                    if sv.menu_mod[0] == 0: # 시작>난이도 정하기
                        curser_max = 4
                        for i in range(0,5): # 메뉴 그리기
                            menu = pygame.Surface((160,48), SRCALPHA)
                            if sv.curser == i: menu.fill((0,0,0,200))
                            menu.blit(menu_img,(0,0),(320,0+48*i,160,48))
                            render_layer.blit(menu,(int(WIDTH/2-240),int(HEIGHT/2-30+64*i-64*sv.curser)))
                        # for i in range(0,2): # 메뉴 그리기
                        #     menu = pygame.Surface((208,32), SRCALPHA)
                        #     if curser == i: menu.fill((0,0,0,200))
                        #     menu.blit(menu_img,(0,0),(0,288+32*i,192,32))
                        #     render_layer.blit(menu,(int(WIDTH/2-240),int(HEIGHT/2-30+64*i-64*curser)))
                    if sv.menu_mod[0] == 1:
                        curser_max = 5
                        text_box = ["Stage1","Stage2","Stage3","Stage4","Stage5","Stage6"]
                        for i in range(0,6):
                            text_color = (255,0,255) if i == sv.curser else (0,0,255)
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
                    if sv.menu_mod[0] == 2:
                        font = pygame.font.Font(FONT_2, 30)
                        pygame.draw.rect(render_layer, (0,0,0), (20,20,WIDTH-40,HEIGHT-40), width=0)
                        for texta in range(0,len(st.htp_scroll)):
                            text1 = font.render(st.htp_scroll[texta], True, (255,255,255))
                            render_layer.blit(text1,(40,30*texta+30))
                    if sv.menu_mod[0] == 3:
                        font = pygame.font.Font(FONT_2, 10)
                        pygame.draw.rect(render_layer, (0,0,0), (20,20,WIDTH-40,HEIGHT-40), width=0)
                        for texta in range(0,len(st.credit_scroll)):
                            text1 = font.render(st.credit_scroll[texta], True, (255,255,255))
                            render_layer.blit(text1,(30,10*texta+30))
                    if sv.menu_mod[0] == 4:
                        curser_max = 2
                        text_box = ["화면모드","음악","효과음"]
                        text_box[0] = "화면모드    창모드" if st.full_on == 0 else "화면모드    전체화면"
                        text_box[1] = "음악   " + str(mmusic_volume)
                        text_box[2] = "효과음  " + str(msfx_volume)
                        for i in range(0,3):
                            text_color = (255,0,255) if i == curser else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(200,100+40*i))
                if sv.select_mod == 2:
                    if sv.menu_mod[0] == 0: # 시작>난이도 정하기
                        curser_max = 1
                        render_layer.blit(menu_img,(0,0),(0,240,320,48))
                        for i in range(0,5): # 메뉴 그리기
                            menu = pygame.Surface((160,48), SRCALPHA)
                            if i == sv.menu_mod[1]: menu.fill((0,0,0,200))
                            menu.blit(menu_img,(0,0),(320,0+48*i,160,48))
                            render_layer.blit(menu,(int(WIDTH/2-240),int(HEIGHT/2-30+64*i-64*sv.menu_mod[1])))
                        for i in range(0,2): # 메뉴 그리기
                            menu = pygame.Surface((208,32), SRCALPHA)
                            if sv.curser == i: menu.fill((0,0,0,200))
                            menu.blit(menu_img,(0,0),(0,288+32*i,192,32))
                            render_layer.blit(menu,(int(WIDTH/2-70),int(HEIGHT/2-30+64*i-64*sv.curser)))
                    if sv.menu_mod[0] == 1:
                        curser_max = 1
                        text_box = ["Field","Boss"]
                        for i in range(0,2):
                            text_color = (255,0,255) if i == sv.curser else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(200,50+40*i))
                        text_box = ["Stage1","Stage2","Stage3","Stage4","Stage5","Stage6"]
                        for i in range(0,6):
                            text_color = (255,0,255) if i == sv.menu_mod[1] else (0,0,255)
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




                if sv.frame_count > 0:
                    sv.frame_count -= 1
                    if frame_count == 0:
                        character = 0 if curser == 0 else 41
                        sv.player.power = 0
                        cur_screen = 1  
                        stage_fun = 0
                        start_fun = stage_fun  
                        curser = 0
            else:
                x = 80
                y = 80 + math.sin(math.pi * (frame_count / 180))*5
                y2 = 80 + math.sin(math.pi * (frame_count*2 / 180))*5
                print(math.sin(math.pi * (frame_count / 180))*5)
                print(y)
                font = pygame.font.Font(FONT_1, 20)    
                text1 = font.render("!GAME CLEAR!", True, (0,0,255))   
                render_layer.blit(text1,(0,0))              
                text1 = font.render("HP: "+str(sv.player.health)+"/"+str(sv.player.max_health), True, (0,0,0))   
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
                render_layer.blit(st.pokemons[0],(x+260,y2+100))
                frame_count += 1

            if sv.cur_screen == 0:screen.blit(pygame.transform.scale2x(render_layer),(0,0))
            pygame.display.flip()
        
        if st.full_on != sv.cur_full_mod:
            # if st.full_on:
            #     screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN|pygame.SCALED)
            # else:
            screen = pygame.display.set_mode((WIDTH*2, HEIGHT*2))
            sv.cur_full_mod = st.full_on
    if game_restart:
        game_restart = False
        play_game()

if __name__ == "__main__":
    play_game()

