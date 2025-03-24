from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
from numpy import abs
import time
from random import randrange
from perlin_noise import PerlinNoise
from random import random


app =Ursina()

window.color= color.rgb(0, 200, 111)
window.exit_button.visible = False

strokeMonoTex=load_texture('stroke_mono.png')


shootPrep = Entity(model='cube')
shootPrep.visible =False

terrainWidth = 25
freq=30
amp=10
noise = PerlinNoise(octaves=1,seed=1000)


bullets=[]
enemyList=[]


##Terrain gen
for i in range(terrainWidth):
    for j in range(terrainWidth):
        x = i
        z = j
        y = floor(noise([x / freq, z / freq]) * amp)
        terrain = Entity(model='cube',collider='box',color=color.green, position =(x,y,z))
        terrain.texture = strokeMonoTex

def input(key):
    if key == 'q' or key == 'escape':
        quit()
    if key == 'left mouse up':
        shoot()

#sim to minecraft function
def shootingPreperation():
    shootPrep.position = (subject.position +camera.forward * 3)
    shootPrep.y+= 2
    shootPrep.y = (shootPrep.y)
    shootPrep.x =(shootPrep.x)
    shootPrep.z = (shootPrep.z)

#shoot the bullet
def shoot():
    print("shooting")
    bullet = Entity(model='sphere',  color=color.blue,scale=0.2,position=shootPrep.position, collider=None)
    bullet.velocity = camera.forward * 10
    bullets.append(bullet)


#multiple of world gen height
def enemySpawn():
    for i in range(terrainWidth):
        for j in range(terrainWidth):
            if random() < 0.05:
                x = i
                z = j
                y = ((floor(noise([x / freq, z / freq]) * amp)) +2) * 2
                enemy = Entity(model='sphere',collider='sphere',color=color.green,scale=0.5, position =(x,y,z))
                enemyList.append(enemy)


enemySpawn()





def update():
    shootingPreperation()
    #kills bullet leaving area once again to not kill my poor laptop
    for bullet in bullets[:]:
        bullet.position += bullet.velocity * time.dt
        if abs(bullet.position.x)>terrainWidth or abs(bullet.position.z)>terrainWidth:
            destroy(bullet)
            bullets.remove(bullet)
            continue
        else:
            for enemy in enemyList[:]:
                if distance(bullet.position, enemy.position) < 1:
                    print("hit ememy")
                    destroy(enemy)
                    enemyList.remove(enemy)
                    destroy(bullet)  # Destroy the bullet after it hits the enemy as to not kill my laptop
                    bullets.remove(bullet)
                    break




spawn_x = terrainWidth // 2
spawn_z = terrainWidth // 2
spawn_y = floor(noise([spawn_x / freq, spawn_z / freq]) * amp) + 5
subject = FirstPersonController()
subject.gravity = 0.5
subject.position = (spawn_x,spawn_y,spawn_z)
destroy(subject.cursor)
# Create your own cursor
subject.cursor = Entity(parent=camera.ui, model='cube', color=color.red, scale=.001)



app.run()