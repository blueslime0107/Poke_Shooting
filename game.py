import pygame, math
from random import randint
from pygame.locals import *

import time
import start as st
import stage_var as sv
from norm_func import *
from spec_func import remove_allbullet, background_scroll
from start import render_layer, WIDTH, HEIGHT, TITLE, FONT_1, FONT_2, score_font, menu_img, monitor_size, up_render_layer,skill_surface
from start import s_boom, s_cancel, s_cat1, s_ch0, s_ch2, s_damage0, s_damage1, s_enedead, s_enep1, s_enep2, s_graze, s_item0, s_kira0, s_kira1, s_lazer1, s_ok, s_pause, s_pldead, s_plst0, s_select, s_slash, s_tan1, s_tan2
from stage import stage_manager
# 게임에 핵심적인 기능만 주석을 넣었습니다 ##

screen = pygame.display.set_mode((WIDTH*2,HEIGHT*2))
    # 플레이어
def music_and_sfx_volume(m,s):
    try:s = s/100
    except:s = 0
    try:m = m/100
    except:m = 0
    pygame.mixer.music.set_volume(m)
    s_lazer1.set_volume(s)
    s_tan1.set_volume(s)
    s_tan2.set_volume(s)
    s_ch2.set_volume(s)
    s_ch0.set_volume(s)
    s_cat1.set_volume(s)
    s_enep1.set_volume(s)
    s_enep2.set_volume(s)
    s_slash.set_volume(s)
    s_pldead.set_volume(s)
    s_plst0.set_volume(s)
    s_damage0.set_volume(s)
    s_damage1.set_volume(s)
    s_graze.set_volume(s)
    s_kira0.set_volume(s)
    s_kira1.set_volume(s)
    s_boom.set_volume(s)
    s_item0.set_volume(s)
    s_enedead.set_volume(s)
    s_ok.set_volume(s)
    s_cancel.set_volume(s)
    s_select.set_volume(s)
    s_pause.set_volume(s)
def all_reset():
    sv.play = True
    sv.cur_full_mod = False
    sv.pause = False
    sv.frame_count = 0
    sv.cur_count = 0
    sv.time_stop = False
    sv.stage_count = 0
    sv.screen_shake_count = 0
    sv.add_dam = 0
    sv.drilling = False
    sv.game_clear = False   
    sv.curser = 0
    sv.select_mod = 0
    sv.menu_mod = []
    sv.character = 0
    sv.difficult = 0
    sv.cur_screen = 0
    sv.stage_fun = 0
    sv.stage_line = 0
    sv.stage_cline = 0
    sv.stage_repeat_count = 0
    sv.stage_condition = 1
    sv.stage_challenge = 0
    sv.stage_end = 0
    sv.skill_activating = []
    sv.practicing = False
    # 게임 시작전 메뉴 변수들
    sv.boss = sv.Boss_Enemy(-99,-99)
    sv.boss_group = pygame.sprite.Group(sv.boss)
    sv.enemy_group = pygame.sprite.Group()
    sv.spr = pygame.sprite.Group()
    sv.magic_spr = pygame.sprite.Group()
    sv.player = sv.Player(-125,-125,5,500)
    sv.player_group = pygame.sprite.Group(sv.player)
    sv.player_hitbox = sv.Player_hit()
    sv.player_sub = sv.Player_sub(1)
    sv.skillobj_group = pygame.sprite.Group()
    sv.title = sv.Tittle(1)
    sv.ui = sv.UI(1)
    sv.under_ui = sv.Under_PI()
    sv.text = sv.TextBox()
    sv.beams_group = pygame.sprite.Group()
    sv.effect_group = pygame.sprite.Group()
    sv.item_group = pygame.sprite.Group()

    sv.starting = True
    sv.read_end = False

    sv.player.skill_list.append(sv.Skill(3,5,"저리가람","바람일으키기",10,60,30))
    sv.player.skill_list.append(sv.Skill(0,7,"Press C key!","몸부림",30,60,10))
    sv.player.skill_list.append(sv.Skill(0,7,"Press C key!","몸부림",30,60,10))


def play_game():
    global screen
    music_and_sfx_volume(st.music_volume,st.sfx_volume)    
    continued = 0
    start_fun = [0,0]
    bgx = 0

    ################################################# 
    while sv.play:
        # 60 프레임
        st.clock.tick(st.clock_fps)
        now = st.time.time()        
        st.dt = (now-st.prev_time)*st.TARGET_FPS        
        st.prev_time = now
        keys = pygame.key.get_pressed() 
        if sv.cur_screen == 1:
            # 키 이벤트
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: # 게임끄기
                    pygame.quit()
                    exit()
                if ev.type == pygame.KEYDOWN:    
                    if not sv.pause:                
                        if ev.key == pygame.K_f:
                            st.full_on = False if st.full_on == True else True
                        if ev.key == pygame.K_ESCAPE and not (sv.text.started and not sv.text.pause) and sv.frame_count >= 60:
                            s_pause.play()
                            sv.pause = True
                            pygame.mixer.music.pause()                        
                        if ev.key == pygame.K_z and sv.text.started and sv.text.count > 50 and not sv.text.pause:
                            sv.text.next_text()
                        if (sv.text.started and sv.text.pause) or not sv.text.started:
                            if ev.key == pygame.K_z and sv.player.gatcha >= sv.player.gatcha_max:
                                if sv.player.shoot_gatcha > 0:
                                    sv.beams_group.add(sv.Beam(get_new_pos(sv.player.pos,5),4))
                                if sv.player.shoot_gatcha == 0:
                                    sv.player.shoot_gatcha = 10                            
                        if (sv.text.started and sv.text.pause) or not sv.text.started:
                            if ev.key == pygame.K_x and sv.player.mp > 0:
                                sv.skill_activating.append(sv.Skill_Core(26,295))
                                sv.boss.spell_clear = False
                                sv.player.mp -= 1      
                            if ev.key == pygame.K_c and sv.player.skill_list[sv.player.skill_pointer].pp > 0:
                                sv.player.skill_list[sv.player.skill_pointer].pp -= 1    
                                sv.skill_activating.append(sv.Skill_Core(sv.player.skill_list[sv.player.skill_pointer].num,sv.player.skill_list[sv.player.skill_pointer].cool))
                        if ev.key == pygame.K_d:
                            sv.player.skill_list.append(sv.player.skill_list.pop(0))
                    else:
                        if ev.key == pygame.K_UP:
                            s_ok.play()
                            sv.curser = 2 if sv.curser == 0 else sv.curser-1
                        if ev.key == pygame.K_DOWN:
                            s_ok.play()
                            sv.curser = 0 if sv.curser == 2 else sv.curser+1
                        if ev.key == pygame.K_z:
                            s_select.play()
                            if sv.curser == 0: 
                                if sv.practicing and sv.boss.died_next_stage:
                                    pass
                                elif sv.player.died:
                                    sv.player.health = sv.player.max_health
                                    sv.player.power = 400
                                    sv.player.count = 0
                                    sv.player.mp = 4
                                    sv.player.died = False
                                    sv.pause = False
                                    continued += 1
                                    pygame.mixer.music.unpause()
                                else:
                                    sv.pause = False
                                    pygame.mixer.music.unpause()
                            if sv.curser == 1:
                                sv.boss = sv.Boss_Enemy(-99,-99)
                                sv.boss_group = pygame.sprite.Group(sv.boss)
                                sv.enemy_group = pygame.sprite.Group()
                                sv.spr = pygame.sprite.Group()
                                sv.magic_spr = pygame.sprite.Group()
                                sv.player = sv.Player(-125,-125,5,500)
                                sv.player_group = pygame.sprite.Group(sv.player)
                                sv.player_hitbox = sv.Player_hit()
                                sv.player_sub = sv.Player_sub(1)
                                sv.skillobj_group = pygame.sprite.Group()
                                sv.title = sv.Tittle(1)
                                sv.ui = sv.UI(1)
                                sv.under_ui = sv.Under_PI()
                                sv.text = sv.TextBox()
                                sv.beams_group = pygame.sprite.Group()
                                sv.effect_group = pygame.sprite.Group()
                                sv.item_group = pygame.sprite.Group()
                                sv.stage_fun = start_fun[0]
                                sv.stage_challenge = start_fun[1]
                                sv.stage_line = 0
                                sv.stage_cline = 0
                                sv.stage_repeat_count = 0
                                sv.stage_condition = 1
                                sv.player.skill_list = []
                                sv.player.skill_list.append(sv.Skill(0,7,"Press C key!","몸부림",30,60))
                                sv.player.skill_list.append(sv.Skill(0,7,"Press C key!","몸부림",30,60))
                                sv.player.skill_list.append(sv.Skill(0,7,"Press C key!","몸부림",30,60))
                                if sv.practicing: sv.player.power = 400
                                st.score = 0
                                sv.skill_activating = []
                                sv.pause = False
                                pygame.mixer.music.unpause()              
                                continued = 0             
                            if sv.curser == 2: st.game_restart = True
                        if ev.key == pygame.K_ESCAPE:
                            sv.pause = False
                            pygame.mixer.music.unpause()
            if keys[pygame.K_LCTRL] and sv.text.started and sv.text.count > 50 and not sv.text.pause:
                sv.text.next_text()
            if st.game_restart:
                sv.frame_count = 0
                break
            
            # 탄에 박았는가
            hit_list = pygame.sprite.spritecollide(sv.player_hitbox, sv.spr, not sv.player.godmod, pygame.sprite.collide_circle)
            beam_collide = pygame.sprite.groupcollide(sv.beams_group, sv.enemy_group, False, False, pygame.sprite.collide_circle)
            if beam_collide.items():
                for beam, enemy in beam_collide.items():                 
                    for i in range(0,len(enemy)): 
                        if not beam.died:
                            enemy[i].health -= beam.damage
                            if beam.num == 4 and enemy[i].health <= 0:
                                sv.player.skill_list[sv.player.skill_pointer] = enemy[i].skill   
                                st.score+=st.score_setting[4] 
                            beam.died = True                       
            if sv.boss.appear: boss_collide = pygame.sprite.spritecollide(sv.boss, sv.beams_group, False, pygame.sprite.collide_circle)
            # 연산 업데이트
            if not sv.pause:      
                if sv.magic_spr.sprites():sv.magic_spr.update(screen)    
                if sv.boss.appear and sv.boss.health <= 0: remove_allbullet()  
                if sv.boss.fire_field_radius > 0:
                    for item in sv.spr.sprites():
                        if distance(item.pos,(sv.boss.pos[0]*2,sv.boss.pos[1]*2)) <= sv.boss.fire_field_radius*2 and not item.shape[1]==4:
                            item.speed += 0.1
                if sv.skill_activating:
                    for skill in sv.skill_activating[:]:
                        skill.update(sv.boss)
                        if skill.cool <= 0 and skill.draw_cool <= 0: sv.skill_activating.remove(skill)
                if sv.skillobj_group: sv.skillobj_group.update(screen)
                sv.spr.update(screen)
                if not sv.player.died:sv.player_hitbox.update()
                if sv.beams_group: sv.beams_group.update()                            
                sv.player_group.update(hit_list,keys)
                if sv.enemy_group:sv.enemy_group.update()
                if sv.item_group: sv.item_group.update()
                if sv.boss.appear: sv.boss_group.update(boss_collide)
                if sv.effect_group: sv.effect_group.update()
                if not sv.player.died:sv.player_sub.update()
                if sv.text.started and not sv.text.pause: sv.text.update()
                stage_manager()
                if sv.practicing and sv.boss.died_next_stage:
                    sv.pause = True
                sv.frame_count += 1
                sv.stage_count += 1
                if not st.bkgd_list == []:
                    for i in st.bkgd_list:i.update()
            if sv.boss.died_next_stage and sv.stage_fun == 6 and sv.stage_challenge == 2 and not sv.game_clear:
                pygame.mixer.music.fadeout(9000)
                sv.stage_count = 0
                cur_count = sv.frame_count
                sv.game_clear = True 
            if sv.game_clear:
                if sv.frame_count - cur_count > 600:
                    sv.cur_screen = 0
                    sv.frame_count = 0
            # 그리기 시작
            #배경 스크롤
            if sv.frame_count >= 60:
                if not sv.pause:
                    background_scroll()               
                    if sv.boss.fire_field_radius > 0:
                        fire_layer = pygame.Surface((WIDTH,HEIGHT), SRCALPHA)
                        pygame.draw.circle(fire_layer, (255,0,0,150), sv.boss.pos, sv.boss.fire_field_radius)
                        render_layer.blit(fire_layer,(0,0))
                    skill_surface.fill((0,0,0,0))
                    if sv.skill_activating:                    
                        for skill in sv.skill_activating[:]:
                            skill.draw(skill_surface)
                    if sv.skillobj_group: sv.skillobj_group.draw(skill_surface)
                    render_layer.blit(skill_surface,(0,0))              
                    sv.item_group.draw(render_layer)
                    sv.magic_spr.draw(render_layer)      
                    sv.beams_group.draw(render_layer)  
                    if not sv.player.died and not sv.drilling:sv.player_group.draw(render_layer) 
                    if not sv.player.died and not sv.drilling:sv.player_sub.draw()
                    sv.enemy_group.draw(render_layer)            
                    if not sv.starting or sv.read_end: sv.enemy_group.draw(render_layer)
                    if sv.boss.appear: sv.boss_group.draw(render_layer)
                    sv.under_ui.draw(keys)
                    scaled = pygame.transform.scale2x(render_layer)
                    screen.blit(scaled,(0,0))                    
                    sv.spr.draw(screen)
                    up_render_layer.fill((255,255,255,0))
                    sv.effect_group.draw(up_render_layer)   
                    sv.player.skill_list[sv.player.skill_pointer].draw()                  
                    if sv.title.count < 460: sv.title.draw()
                    if sv.text.started:sv.text.draw()
                    sv.ui.draw()
                    if sv.boss.spell and sv.boss.appear and sv.boss.spell[0].spellcard:
                        sv.boss.spell[0].draw()
                    if sv.game_clear:
                        if sv.frame_count-cur_count > 300:
                            up_render_layer.fill((255,255,255,sv.frame_count-300-cur_count if sv.frame_count-300-cur_count < 256 else 255))                    
                    screen.blit(pygame.transform.scale2x(up_render_layer),(0,0))
                    if sv.screen_shake_count > 0:
                        screen.blit(screen,(randint(-20,20),randint(-20,20)))
                        sv.screen_shake_count -= 1
                else: 
                    screen.blit(pygame.transform.scale2x(render_layer),(0,0))
                    sv.spr.draw(screen)
                    screen.blit(pygame.transform.scale2x(up_render_layer),(0,0))
                    pause_menu = pygame.Surface((WIDTH,HEIGHT), SRCALPHA)  
                    pause_menu.fill((255, 0, 85,100))
                    pause_menu.blit(menu_img,(10,100),(160,48,160,32))
                    for i in range(0,3): # 메뉴 그리기
                        menu = pygame.Surface((160,32), SRCALPHA)
                        if sv.curser == i: menu.fill((0,0,0,200))
                        menu.blit(menu_img,(0,0),(160,80+32*i,160,32))
                        if i == 0 and sv.practicing and sv.boss.died_next_stage: 
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
                    sv.play = False
                if ev.type == pygame.KEYDOWN: 
                    if not sv.game_clear:
                        if ev.key == pygame.K_f:
                            sv.st.full_on = False if st.full_on == True else True  
                        if ev.key == pygame.K_UP:
                            sv.curser = curser_max if sv.curser == 0 else sv.curser - 1 # 커서위로
                            st.s_ok.play()
                        if ev.key == pygame.K_DOWN:
                            sv.curser = 0 if sv.curser == curser_max else sv.curser + 1 # 커서밑으로
                            st.s_ok.play()
                        if sv.select_mod == 0: # 시작화면
                            if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                st.s_select.play()
                                if sv.curser == 5: sv.play = False # 게임끄기
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
                                    sv.select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]   
                                    break
                            if sv.menu_mod[0] == 4:
                                if ev.key == pygame.K_RIGHT:
                                    s_ok.play()
                                    if sv.curser == 0:
                                        sv.st.full_on = 1 if sv.st.full_on == 0 else 0
                                    if sv.curser == 1:
                                        st.music_volume = st.music_volume + 5 if st.music_volume < 100 else 100
                                    if sv.curser == 2:
                                        st.sfx_volume = st.sfx_volume + 5 if st.sfx_volume < 100 else 100                                
                                if ev.key == pygame.K_LEFT:
                                    s_ok.play()
                                    if sv.curser == 0:
                                        st.full_on = 1 if st.full_on == 0 else 0
                                    if sv.curser == 1:
                                        st.music_volume = st.music_volume - 5 if st.music_volume > 0 else 0
                                    if sv.curser == 2:
                                        st.sfx_volume = st.sfx_volume - 5 if st.sfx_volume > 0 else 0
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    music_and_sfx_volume(st.music_volume,st.sfx_volume)
                                    with open('resources\setting.txt','w',encoding="UTF-8") as f:
                                        f.write("fullscreen"+"="+str(st.full_on)+"\n")
                                        f.write("sfx"+"="+str(st.sfx_volume)+"\n")
                                        f.write("bgm"+"="+str(st.music_volume)+"\n")
                                    sv.curser = 0
                                    sv.select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]     
                                    break                        
                        if sv.select_mod == 2:
                            if sv.menu_mod[0] == 0:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    s_select.play()
                                    sv.character = 0 if sv.curser == 0 else 41
                                    sv.difficult = sv.menu_mod[1]
                                    sv.player.power = 0
                                    sv.cur_screen = 1  
                                    sv.stage_fun = 0
                                    start_fun = [0,0]
                                    sv.frame_count = 0
                                    sv.curser = 0
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    sv.curser = sv.menu_mod[1]
                                    sv.select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]   
                                    break                                
                            if sv.menu_mod[0] == 1:
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
                                if ev.key == pygame.K_RIGHT or ev.key == pygame.K_LEFT:
                                    s_select.play()
                                    sv.character = 41 if sv.character == 0 else 0                          
                        if sv.select_mod == 3:
                            if sv.menu_mod[0] == 1:
                                if ev.key == pygame.K_z or ev.key == pygame.K_RETURN:
                                    s_select.play()                                    
                                    sv.player.power = 400
                                    sv.stage_fun = sv.menu_mod[2]                                 
                                    if sv.curser == 1:
                                        if sv.menu_mod[2] == 0:sv.stage_challenge = 5
                                        if sv.menu_mod[2] == 1:sv.stage_challenge = 4
                                        if sv.menu_mod[2] == 2:sv.stage_challenge = 8
                                        if sv.menu_mod[2] == 3:sv.stage_challenge = 7
                                        if sv.menu_mod[2] == 4:sv.stage_challenge = 6
                                        if sv.menu_mod[2] == 5:sv.stage_challenge = 2
                                    start_fun = [sv.stage_fun,sv.stage_challenge]
                                    sv.difficult = sv.menu_mod[1]
                                    sv.curser = 0
                                    sv.cur_screen = 1 
                                    sv.practicing = True
                                    sv.frame_count = 0
                                if ev.key == pygame.K_x or ev.key == pygame.K_ESCAPE:
                                    s_cancel.play()
                                    sv.curser = sv.menu_mod[1]
                                    sv.select_mod -= 1
                                    del sv.menu_mod[len(sv.menu_mod)-1]   
                                    break  
                    
                    
                    else:
                        if ev.key == K_x or ev.key == K_ESCAPE or ev.key == K_z:
                            old_score = 0
                            if sv.character == 0:
                                old_score = int(st.score_scroll[0][2:])
                                if old_score < st.score:
                                    st.score_scroll[0] = "H:"+str(st.score).zfill(10)
                                    st.score_scroll[0] = st.score_scroll[0]
                            else:
                                old_score = int(st.score_scroll[1][2:])
                                if old_score < st.score:
                                    st.score_scroll[1] = "F:"+str(st.score).zfill(10)
                                    st.score_scroll[1] = st.score_scroll[1]
                            with open('resources\st.score.txt','w',encoding="UTF-8") as f:
                                f.write(st.score_scroll[0]+"\n")
                                f.write(st.score_scroll[1]+"\n")
                                
                            st.game_restart = True
            if st.game_restart:
                sv.frame_count = 0
                break    

            rel_x = bgx % WIDTH
            render_layer.blit(st.background_img, (rel_x - WIDTH,0))
            if rel_x < WIDTH:
                render_layer.blit(st.background_img,(rel_x,0))  
            bgx += 1         
            ui_x = WIDTH - 180
            ui_y = 20
            if not sv.game_clear: # 메뉴
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
                        curser_max = 3
                        for i in range(0,4): # 메뉴 그리기
                            menu = pygame.Surface((160,48), SRCALPHA)
                            if sv.curser == i: menu.fill((0,0,0,200))
                            menu.blit(menu_img,(0,0),(320,0+48*i,160,48))
                            render_layer.blit(menu,(int(WIDTH/2-240),int(HEIGHT/2-30+64*i-64*sv.curser)))
                    if sv.menu_mod[0] == 1:
                        curser_max = 2
                        for i in range(0,3): # 메뉴 그리기
                            menu = pygame.Surface((160,48), SRCALPHA)
                            if sv.curser == i: menu.fill((0,0,0,200))
                            menu.blit(menu_img,(0,0),(320,0+48*i,160,48))
                            render_layer.blit(menu,(int(WIDTH/2-240),int(HEIGHT/2-30+64*i-64*sv.curser)))                        
                    if sv.menu_mod[0] == 2: # 설명
                        font = pygame.font.Font(FONT_2, 30)
                        pygame.draw.rect(render_layer, (0,0,0), (20,20,WIDTH-40,HEIGHT-40), width=0)
                        for texta in range(0,len(st.htp_scroll)):
                            text1 = font.render(st.htp_scroll[texta], True, (255,255,255))
                            render_layer.blit(text1,(40,30*texta+30))
                    if sv.menu_mod[0] == 3: # 크레딧
                        font = pygame.font.Font(FONT_2, 10)
                        pygame.draw.rect(render_layer, (0,0,0), (20,20,WIDTH-40,HEIGHT-40), width=0)
                        for texta in range(0,len(st.credit_scroll)):
                            text1 = font.render(st.credit_scroll[texta], True, (255,255,255))
                            render_layer.blit(text1,(30,10*texta+30))
                    if sv.menu_mod[0] == 4: # 설정
                        curser_max = 2
                        text_box = ["화면모드","음악","효과음"]
                        text_box[0] = "화면모드    창모드" if st.full_on == 0 else "화면모드    전체화면"
                        text_box[1] = "음악   " + str(st.music_volume)
                        text_box[2] = "효과음  " + str(st.sfx_volume)
                        for i in range(0,3):
                            text_color = (255,0,255) if i == sv.curser else (0,0,255)
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
                        curser_max = 5
                        text_box = ["Stage1","Stage2","Stage3","Stage4","Stage5","Stage6"]
                        for i in range(0,6):
                            text_color = (255,0,255) if i == sv.curser else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(100,50+40*i))
                        if sv.character == 0:
                            text_color = (0,0,0)
                            text1 = score_font.render("Homing", True, text_color)                        
                            render_layer.blit(text1,(300,100))  
                        else:  
                            text_color = (0,0,0)
                            text1 = score_font.render("FFocus", True, text_color)                        
                            render_layer.blit(text1,(300,100))    
                if sv.select_mod == 3:
                    if sv.menu_mod[0] == 1:
                        curser_max = 1
                        text_box = ["Field","Boss"]
                        for i in range(0,2):
                            text_color = (255,0,255) if i == sv.curser else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(200,50+40*i))
                        text_box = ["Stage1","Stage2","Stage3","Stage4","Stage5","Stage6"]
                        for i in range(0,6):
                            text_color = (255,0,255) if i == sv.menu_mod[2] else (0,0,255)
                            text1 = score_font.render(text_box[i], True, text_color)
                            render_layer.blit(text1,(100,50+40*i))
                        if sv.character == 0:
                            text_color = (0,0,0)
                            text1 = score_font.render("Homing", True, text_color)                        
                            render_layer.blit(text1,(300,100))  
                        else:  
                            text_color = (0,0,0)
                            text1 = score_font.render("FFocus", True, text_color)                        
                            render_layer.blit(text1,(300,100)) 
                    
                if sv.frame_count > 0:
                    sv.frame_count -= 1
                    if sv.frame_count == 0:
                        sv.character = 0 if sv.curser == 0 else 41
                        sv.player.power = 0
                        sv.cur_screen = 1  
                        sv.stage_fun = 0
                        sv.start_fun = sv.stage_fun  
                        sv.curser = 0
            else: # 게임 끝났을때 화면
                x = 80
                y = 80 + math.sin(math.pi * (sv.frame_count / 180))*5
                y2 = 80 + math.sin(math.pi * (sv.frame_count*2 / 180))*5
                font = pygame.font.Font(FONT_1, 20)    
                text1 = font.render("!GAME CLEAR!", True, (0,0,255))   
                render_layer.blit(text1,(0,0))              
                text1 = font.render("HP: "+str(sv.player.health)+"/"+str(sv.player.max_health), True, (0,0,0))   
                render_layer.blit(text1,(x,y)) 
                if sv.character == 0:text1 = font.render("Weapon:"+"Homing", True, (0,0,0))
                else: text1 = font.render("Weapon:"+"FFocus", True, (0,0,0))  
                render_layer.blit(text1,(x+10,y+30)) 
                text1 = font.render("Continue:"+str(continued), True, (0,0,0))   
                render_layer.blit(text1,(x+20,y+60)) 
                text1 = font.render("Final Score", True, (0,0,0))   
                render_layer.blit(text1,(x+60,y+90)) 
                text1 = font.render(str(st.score).zfill(10), True, (0,0,0))   
                render_layer.blit(text1,(x+60,y+120))
                render_layer.blit(st.pokemons[0],(x+260,y2+100))
                sv.frame_count += 1

            if sv.cur_screen == 0:screen.blit(pygame.transform.scale2x(render_layer),(0,0))
            pygame.display.flip()

        # 전체화면
        if st.full_on != sv.cur_full_mod:
            if st.full_on:
                screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN|pygame.SCALED)
            else:
                screen = pygame.display.set_mode((WIDTH*2, HEIGHT*2))
            sv.cur_full_mod = st.full_on
    if st.game_restart:
        st.game_restart = False
        all_reset()
        play_game()

if __name__ == "__main__":
    play_game()

