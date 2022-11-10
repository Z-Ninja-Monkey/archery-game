from ursina import *
import time
#testingfgdjkhgdfg
app = Ursina()

window.title = 'archery game mabey'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False
window.color = color.rgb(100,150,250)

frame_count = 0
game_start = False
game_forever = False
def start_game():
  global game_start
  game_start = True

archer_ico = "assets/frame0.png"
arrow_ico = "assets/arrow.png"
target_ico = "assets/archery_target.png"
title_ico = "assets/archery.png"
start_model = "assets/button.obj"
start_texture = "assets/button.png"

title = Sprite(texture = title_ico, scale = 2)
title.y = 1.7

start = Entity(model = start_model, texture = start_texture, scale = 0.7, on_click = start_game)
start.rotation_x = 180
start.rotation_y = 20
start.rotation_z = 180
start.y = -2
start.collider = "mesh"

archer = Sprite(texture = archer_ico, scale = 0.6)
archer.x = -5
archer.y = 8
archer.collider = BoxCollider(archer, center=Vec3(0,0,0), size=Vec3(0,0.78,0))

target = Sprite(texture = target_ico, scale = 0.2)
target.x = 5
target.y = -2.3
target.z = -0.001

arrow = Sprite(parent = camera.ui, texture = arrow_ico, scale = 0.016)
arrow.collider = "box"
arrow.rotation_z = 0
arrow.x = -0.8
arrow.y = -0.2


ground = Sprite(model = Quad, color = color.rgb(0,255,0), scale = (15,1.5))
ground.y = -3.6
ground.collider = "box"

archer.enabled = False
ground.enabled = False
target.enabled = False

light = PointLight(y=2, z=-3, shadows=True, color = color.rgb(300,300,300))

should_update_delta = True
def move_towards_mouse(sprite, amount):
  global should_update_delta
  global delta_x
  global delta_y
  
  if should_update_delta == True:
    delta_y = mouse.y - sprite.y
    delta_x = mouse.x - sprite.x
  
  if delta_x == 0 or delta_y == 0:
    delta_x = 0.00000000000001
    delta_y = 0.00000000000001 

  
  sprite.x += delta_x /100*amount
  sprite.y += delta_y /100*amount
  
first_time = True
gravity = 0

def update():
  global frame_count
  global game_start
  global game_forever
  global should_update_delta
  global first_time
  global gravity
  
  if game_start == True:
    #runs once on game start
    start.model = "assets/button2.obj"
    game_start = False
    game_forever = True
    light.color = color.rgb(450,450,450)
    
  elif game_forever == True:
    frame_count += 1 * time.dt
    if frame_count > 0.5:
      #runs every frame after game start

      if held_keys['left mouse']:
        if first_time == True:
          should_update_delta = True
          first_time = False
        gravity += 0.003
        if gravity > 0.036:
          gravity = 0.036
        move_towards_mouse(arrow, 10)
        arrow.y -= gravity
        should_update_delta = False

      if not held_keys['left mouse']:
        should_update_delta = True
        gravity = 0
        
      archer.enabled = True
      ground.enabled = True
      target.enabled = True
      start.enabled = False
      title.enabled = False

      archer.y -= 5 * time.dt
      if archer.intersects(ground).hit:
        archer.y += 5 * time.dt
        
      if arrow.intersects(ground).hit:
        arrow.enabled = False
        print("this ran")
            
  else:
    #else
    carson_sucks = True
app.run()
