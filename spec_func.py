def dif(num):
    return num == difficult
def bullet_clear():
    if spr:
        for bullet in spr.sprites():
            add_effect(bullet.pos,7,bullet.shape[1])
            bullet.kill()
def enemy_clear():
    if enemy_group:
        for i in enemy_group.sprites():
            i.health = -999
def remove_allbullet():
    for i in spr.sprites():
        item_group.add(Item(i.pos,1))
    for i in magic_spr.sprites():
        item_group.add(Item(i.pos,0))
    spr.empty()
    magic_spr.empty()
def bullet(pos,dir,speed,img,col,mode=0,num = (0,0)):
    spr.add(Bullet(pos[0]*2,pos[1]*2,dir,speed,img,col,mode,num))
def sbullet(pos,dir,speed,img,col,mode=0,num = (0,0)):
    spr.add(Bullet(pos[0],pos[1],dir,speed,img,col,mode,num))
def bullet_effect(sound,col,pos,only_sound = False):
    if not sound == 0:
        if sound == s_tan1:tan_channel.play(sound)
        elif sound == s_kira0:kira_channel.play(sound)
        elif sound == s_kira1:kira2_channel.play(sound)
        elif sound == s_tan2:tan2_channel.play(sound)
        else:sound.play()
    if not only_sound:add_effect(pos,2,col)
def sbullet_effect(sound,col,pos,only_sound = False):
    if not sound == 0:
        if sound == s_tan1:tan_channel.play(sound)
        elif sound == s_kira0:kira_channel.play(sound)
        elif sound == s_kira1:kira2_channel.play(sound)
        elif sound == s_tan2:tan2_channel.play(sound)
        else:sound.play()
    if not only_sound:add_effect((pos[0]/2,pos[1]/2),2,col)
def magic_bullet(pos,dir,speed,mode=0,screend=0):
    magic_spr.add(MagicField(pos,dir,speed/2,mode,screend))
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
    else:
        if pos[0] < 32:
            pos[0] = 32
        if pos[0] > WIDTH-32:
            pos[0] = WIDTH-32
        if pos[1] < 32:
            pos[1] = 32
        if pos[1] > HEIGHT-32:
            pos[1] = HEIGHT-32           
    boss.move_time -= 1
    if boss.move_time == 0:
        boss.move_speed = 0
        boss.move_dir = 0
    return pos