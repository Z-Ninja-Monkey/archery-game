from ursina import *
from random import *
import time

app = Ursina()

window.title = 'archery game mabey'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True
window.fps_counter.enabled = False
window.color = color.rgb(100, 150, 250)
window.size = (1100, 600)

frame_count = 0
game_start = False
game_forever = False


def start_game():
  global game_start
  game_start = True

archer_ico = "assets/archer/archer.png"
arrow_ico = "assets/arrow.png"
bow_ico = "assets/archer/bow.png"
target_ico = "assets/archery_target.png"
extra = "assets/archer/animation help.png"
title_ico = "assets/archery.png"
start_model = "assets/button.obj"
start_texture = "assets/button.png"
arrow_follower_ico = "assets/arrow_follower.png"
dot_ico = "assets/dot.png"

title = Sprite(texture=title_ico, scale=2)
title.y = 1.7

start = Entity(model=start_model,texture=start_texture,scale=0.7,on_click=start_game)
start.rotation_x = 180
start.rotation_y = 20
start.rotation_z = 180
start.y = -2
start.collider = "mesh"

archer = Sprite(parent=camera.ui, texture=archer_ico, scale=0.07)
archer.x = -0.8
archer.y = -0.25
archer.z = -0.1
archer.collider = BoxCollider(archer,center=Vec3(0, 0.005, 0),size=Vec3(0, 0.78, 0))

bow = Sprite(parent=camera.ui, texture=bow_ico, scale=0.07)
bow.x = -0.8
bow.y = -0.25
bow.z = -0.2

animation_help = Sprite(parent=camera.ui, texture=extra, scale=0.07)

target = Sprite(parent=camera.ui, texture=target_ico, scale=0.02)
target.collider = BoxCollider(target,center=Vec3(-0.1, 0, 0),size=Vec3(0.6, 0.9, 1))
target.x = 0.8
target.y = -0.35
target.z = -0.00001

arrow = Sprite(parent=camera.ui, texture=arrow_ico, scale=0.01)
arrow.collider = "box"
arrow.rotation_z = 0
arrow.x = -0.8
arrow.y = -0.2
arrow.z = -0.00002
arrow.enabled = False

arrow_follower = Sprite(parent=camera.ui, texture=arrow_follower_ico)
arrow_follower.x = arrow.x
arrow_follower.y = arrow.y
arrow_follower.visible = False

ground = Sprite(parent=camera.ui,model=Quad,color=color.rgb(0, 200, 0),scale=(15, 0.2))
ground.y = -0.5
ground.collider = "box"

ground2 = Sprite(parent=camera.ui,model=Quad,color=color.rgb(0, 200, 0),scale=(15, 0.2))
ground2.z = -0.1
ground2.y = -0.54

archer.enabled = False
ground.enabled = False
ground2.enabled = False
target.enabled = False

light = PointLight(y=2, z=-3, shadows=True, color=color.rgb(300, 300, 300))

dot = Sprite(parent=camera.ui, texture=dot_ico, x=-0.8, y=-0.25, scale=0.05)
dot.enabled = False
dot2 = duplicate(dot)
dot2.enabled = False
dot3 = duplicate(dot)
dot3.enabled = False
dot4 = duplicate(dot)
dot4.enabled = False
dot5 = duplicate(dot)
dot5.enabled = False

dot_stuff = 10


def create_aimer():
    global dot_stuff

    dot.position = Vec2(arrow.x, arrow.y)
    dot2.position = Vec2(arrow.x, arrow.y)
    dot3.position = Vec2(arrow.x, arrow.y)
    dot4.position = Vec2(arrow.x, arrow.y)
    dot5.position = Vec2(arrow.x, arrow.y)
    test = 0
    move_towards_mouse(dot, 15 + test , "none")
    move_towards_mouse(dot2, 35 + test, "none")
    move_towards_mouse(dot3, 57 + test, "none")
    move_towards_mouse(dot4, 80 + test, "none")
    move_towards_mouse(dot5, 100 + test, "none")

    dot.y += 0.2 - 0.2
    dot2.y += 0.2 - 0.13
    dot3.y += 0.2 - 0.1
    dot4.y += 0.2 - 0.11
    dot5.y += 0.2 - 0.15


landing_num = randint(80, 90)


def look_at(thing, looking_at):

    above = looking_at.y - thing.y
    away = looking_at.x - thing.x

    if above == 0 or away == 0:
        away = 0.000000000000001
        above = 0.0000000000000000000000000001

    thing.rotation_z = above / away * -40
    if thing.rotation_z > 90:
        thing.rotation_z = landing_num
    if thing.rotation_z < -90:
        thing.rotation_z = -90


should_update_delta = True


def move_towards_mouse(sprite, amount, type):
    global should_update_delta
    global delta_x
    global delta_y
  
    if should_update_delta == True:
        delta_y = mouse.y - sprite.y
        delta_x = mouse.x - sprite.x

    if delta_x == 0 or delta_y == 0:
        delta_x = 0.00000000000001
        delta_y = 0.00000000000001
    
    stuff = delta_x / 100 * amount
    if type == "none" and (stuff > 0.8 or stuff < 0):
      stuff = 1.2
      dot.visible = False
      dot2.visible = False
      dot3.visible = False
      dot4.visible = False
      dot5.visible = False
      held_keys['left mouse'] = False
    else:
      dot.visible = True
      dot2.visible = True
      dot3.visible = True
      dot4.visible = True
      dot5.visible = True
    
    if stuff > 0.08 and type == "arrow":
        stuff = 0.075
        print (stuff)
    sprite.x += stuff
    sprite.y += delta_y / 125 * amount


first_time = True
gravity = 0
frozen = False
frozen_pos = None
frozen_pos2 = None
check_mouse = False
mouse_click = False


def update():
    global frame_count
    global game_start
    global game_forever
    global should_update_delta
    global first_time
    global gravity
    global frozen
    global frozen_pos
    global frozen_pos2
    global arrow_follower
    global mouse_click
    global check_mouse
    hide_dots = False
    
    look_at(arrow, arrow_follower)
    create_aimer()

    if arrow.x > -0.75 or arrow.y > -0.2:

        arrow.visible = True
    else:
        arrow.visible = False

    if arrow.intersects(target).hit or arrow.intersects(ground).hit:
        arrow.z = -0.00002
        frozen = True
        frozen_pos = arrow.position
        frozen_pos2 = arrow_follower.position

    if game_start == True:
        #runs once on game start
        start.model = "assets/button2.obj"
        game_start = False
        game_forever = True
        light.color = color.rgb(450, 450, 450)

    elif game_forever == True:
        frame_count += 1 * time.dt
        if frame_count > 0.5:
            #runs every frame after game start

            if held_keys['left mouse']:
                check_mouse = True

            if check_mouse == True:
                held_keys['left mouse'] = True

            if held_keys['left mouse']:
                if first_time == True:
                    arrow.enabled = True
                    should_update_delta = True
                    first_time = False
                hide_dots = True
                gravity += 0.003
                move_towards_mouse(arrow_follower, 1, "arrow")
                move_towards_mouse(arrow_follower, 10, "arrow")
                move_towards_mouse(arrow, 10, "arrow")
                arrow.y -= gravity
                arrow_follower.y -= gravity * 1.25
                should_update_delta = False

            if not held_keys['left mouse']:
                should_update_delta = True
                gravity = -0.02

            archer.enabled = True
            ground.enabled = True
            target.enabled = True
            start.enabled = False
            title.enabled = False
            ground2.enabled = True
            if hide_dots == False:
              dot.enabled = True
              dot2.enabled = True
              dot3.enabled = True
              dot4.enabled = True
              dot5.enabled = True
            else:
              dot.enabled = False
              dot2.enabled = False
              dot3.enabled = False
              dot4.enabled = False
              dot5.enabled = False

            if frozen == True:
                arrow.position = frozen_pos
                arrow_follower.position = frozen_pos2
    else:
        #else
        carson_sucks = True


app.run()
