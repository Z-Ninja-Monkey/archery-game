from ursina import *
import time

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
arrow_follower_ico = "arrow_follower.png"

title = Sprite(texture = title_ico, scale = 2)
title.y = 1.7

start = Entity(model = start_model, texture = start_texture, scale = 0.7, on_click = start_game)
start.rotation_x = 180
start.rotation_y = 20
start.rotation_z = 180
start.y = -2
start.collider = "mesh"

archer = Sprite(parent = camera.ui,texture = archer_ico, scale = 0.07)
archer.x = -0.8
archer.y = 1.5
archer.collider = BoxCollider(archer, center=Vec3(0,0.005,0), size=Vec3(0,0.78,0))

target = Sprite(parent = camera.ui,texture = target_ico, scale = 0.02)
target.collider = BoxCollider(target, center=Vec3(-0.1,0,0), size=Vec3(0.6,0.9,1))  
target.x = 0.8
target.y = -0.34
target.z = -0.00001

arrow = Sprite(parent = camera.ui, texture = arrow_ico, scale = 0.01)
arrow.collider = "box"
arrow.rotation_z = 0
arrow.x = -0.8
arrow.y = -0.2
arrow.z = -0.00002

arrow_follower = Sprite(parent = camera.ui, texture = arrow_follower_ico)

ground = Sprite(parent = camera.ui,model = Quad, color = color.rgb(0,200,0), scale = (15,0.2))
ground.y = -0.5
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
frozen = False
frozen_pos = None

def update():
  global frame_count
  global game_start
  global game_forever
  global should_update_delta
  global first_time
  global gravity
  global frozen
  global frozen_pos

  if arrow.intersects(target).hit:
    frozen = True
    frozen_pos = arrow.position
  
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
        move_towards_mouse(arrow, 10)
        arrow.y -= gravity
        should_update_delta = False

      if not held_keys['left mouse']:
        should_update_delta = True
        gravity = -0.015
        
      archer.enabled = True
      ground.enabled = True
      target.enabled = True
      start.enabled = False
      title.enabled = False

      archer.y -= 0.8 * time.dt
      if archer.intersects(ground).hit:
        archer.y += 0.8 * time.dt

      if target.intersects(arrow_follower, debug=True).hit:
        print("this will never run")
      
      if frozen == True:
        arrow.position = frozen_pos
            
  else:
    #else
    carson_sucks = True
app.run()
