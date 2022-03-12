import pygame, math
import random 
import start as st
import cv2
import numpy

def get_new_pos(pos,x=0,y=0):
    return (round(pos[0] + x), round(pos[1] + y))

def big_small(val,min,max):
    return min < val and val < max

def when_time(val,time):
    return val == time

def while_time(val,time):
    return val % time == 0

def calculate_new_xy(old_xy, speed, angle_in_degrees, no_delta = False):
    move_vec = pygame.math.Vector2()
    move_vec.from_polar((speed/2, angle_in_degrees))
    if not no_delta: move_vec = (move_vec[0]*st.dt,move_vec[1]*st.dt)
    return (old_xy[0] + move_vec[0],old_xy[1] + move_vec[1])

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

def randfloat(min,max):
    return round(random.uniform(min,max),1)