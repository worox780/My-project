import numpy as np
import matplotlib.pyplot as plt



class Vector2:
  def __init__(self, x:float, y:float) -> None: self.x, self.y = x, y
  def Get(self) -> tuple: return [self.x, self.y]
  def Set(self, x:float, y:float): self.x, self.y = x, y
  def Norme(self) -> float: return np.sqrt(self.x**2 + self.y**2)

class ObjetCelleste:
  def __init__(self, position:Vector2, pousse:Vector2, masse_objet:float, rayon:float) -> None:
    #----------Vecteur2----------
    #-----Valeurs équation horaires-----
    self.acceleration:Vector2 = Vector2(0,0)
    self.vitesse:Vector2 = Vector2(0,0)
    self.position:Vector2 = position
    #-----------------------------------
    #-----Valeurs caractéristique de la fusée-----
    self.pousse:Vector2 = pousse
    #----------float----------
    self.masse_objet:float = masse_objet
    self.rayon:float = rayon
    #----------list----------
    self.position_x:list = []
    self.position_y:list = []

  def SetAcceleration(self, valeur:Vector2) -> None: self.acceleration = valeur
  def SetVitesse(self, valeur:Vector2) -> None: self.vitesse = valeur
  def SetPosition(self, valeur:Vector2) -> None: self.position = valeur
  def SetPousse(self, valeur:Vector2) -> None: self.pousse = valeur
  def AppendX(self, value) -> None:self.position_x.append(value)
  def AppendY(self, value) -> None:self.position_y.append(value)
  def GetPosX(self) -> list: return self.position_x
  def GetPosY(self) -> list: return self.position_y


class Constante:
  G = 6.67*10**(-11)
  MASSE_TERRE = 5.972*10**24 #en kg
  RAYON_TERRE = 6_371_000 #en mètre
  POS_TERRE = Vector2(0,0) #origine du monde
  RAYON_LUNE = 1_738_000
  MASSE_LUNE = 7.347*10**22
  DELTA = 0.1


class Gravite:
  def IntensitePesenteur(position:Vector2, masse_attracteur:float, rayon:float, position_attracteur:Vector2) -> Vector2:
    position_plan_attracteur:Vector2 = Vector2(position.x, position.y)
    if position.Norme() < rayon: gravite:float = (position_plan_attracteur.Norme()/rayon) * ((Constante.G*masse_attracteur)/((rayon)**2)) #la gravité sur l'axe x est proportionnel à la profondeur, le rayon et l'intensité à la surface en fonction de la profondeur s'il on est dans la planète
    else: gravite:float = (Constante.G*masse_attracteur)/(position_plan_attracteur.Norme()**2)

    gravite **=2

    pos_x:float = gravite*(position_plan_attracteur.x/position_plan_attracteur.Norme())
    pos_y:float = gravite*(position_plan_attracteur.y/position_plan_attracteur.Norme())

    if pos_x != 0: pos_x = np.sqrt(abs(pos_x))*(pos_x/abs(pos_x))
    if pos_y != 0: pos_y = np.sqrt(abs(pos_y))*(pos_y/abs(pos_y))

    return Vector2(pos_x,pos_y)
  def ForceInteraction(masse_objet1:float, masse_objet2:float, position_objet1:Vector2, position_objet2:Vector2):
    distance:Vector2 = Vector2(position_objet1.x-position_objet2.x, position_objet1.y-position_objet2.y).Norme()
    return (Constante.G*masse_objet1*masse_objet2)/(distance**2)

class Cinematique:
  def CalculAcceleration(masse_objet, pousse:Vector2, position:Vector2):
    gravite:Vector2 = Gravite.IntensitePesenteur(position=position, masse_attracteur=Constante.MASSE_TERRE, rayon=Constante.RAYON_TERRE, position_attracteur=Constante.POS_TERRE)
    acceleration = Vector2((pousse.x)/masse_objet - gravite.x, (pousse.y)/masse_objet - gravite.y)
    return acceleration
  def CalculVitesse(delta:float, acceleration:Vector2, vitesse:Vector2) -> Vector2:
    return Vector2(acceleration.x*delta + vitesse.x, acceleration.y*delta + vitesse.y)
  def CalculPosition(delta:float, acceleration:Vector2, vitesse:Vector2, position:Vector2) -> Vector2:
    return Vector2((acceleration.x*delta**2)/2 + vitesse.x*delta + position.x, (acceleration.y*delta**2)/2 + vitesse.y*delta + position.y)

fusee:ObjetCelleste = ObjetCelleste(position=Vector2(0, Constante.RAYON_TERRE), pousse=Vector2(0,15_120_000), masse_objet=780000, rayon=2)
terre:ObjetCelleste = ObjetCelleste(position=Vector2(0,0), pousse=Vector2(0,0), masse_objet=Constante.MASSE_TERRE, rayon=Constante.RAYON_TERRE)
lune:ObjetCelleste = ObjetCelleste(position=Vector2(0,Constante.RAYON_TERRE+384_400_000+Constante.RAYON_LUNE), pousse=Vector2(0,0), masse_objet=Constante.MASSE_TERRE, rayon=Constante.RAYON_LUNE)


print(Constante.RAYON_TERRE+384_400_000+Constante.RAYON_LUNE)
print(Gravite.IntensitePesenteur(position=Vector2(0, Constante.RAYON_TERRE), masse_attracteur=Constante.MASSE_TERRE, rayon=Constante.RAYON_TERRE, position_attracteur=Constante.POS_TERRE).Get())
print(Gravite.IntensitePesenteur(position=Vector2(0, Constante.RAYON_TERRE*2), masse_attracteur=Constante.MASSE_TERRE, rayon=Constante.RAYON_TERRE, position_attracteur=Vector2(0,0)).Get())

def ProcessFusee():
  for i in range(500_000): #int(226520*3)
    #-----La propulsion de la fusée-----
    if (i <= 350/Constante.DELTA): fusee.SetPousse(Vector2(i*10_000,15_120_000))
    elif (i >= (37801//2)) and (i <= ((37801//2) + 200/Constante.DELTA)): fusee.SetPousse(Vector2(5_000_00,-12_120_000))
    else: fusee.SetPousse(Vector2(0,0))
    
    fusee.SetAcceleration(Cinematique.CalculAcceleration(masse_objet=fusee.masse_objet, pousse=fusee.pousse, position=fusee.position))
    fusee.SetVitesse(Cinematique.CalculVitesse(delta=Constante.DELTA, acceleration=fusee.acceleration, vitesse=fusee.vitesse))
    fusee.SetPosition(Cinematique.CalculPosition(delta=Constante.DELTA, acceleration=fusee.acceleration, vitesse=fusee.vitesse, position=fusee.position))
    fusee.AppendX(fusee.position.x)
    fusee.AppendY(fusee.position.y)
    if (fusee.position.Norme() - Constante.RAYON_TERRE) < 0:
      print("i : ", i)
      break

def ProcessLune():
  pousse_lune = Gravite.ForceInteraction(masse_objet1=terre.masse_objet, masse_objet2=lune.masse_objet, position_objet1=terre.position, position_objet2=lune.position)
  for i in range(1_000_000): #int(226520*3)
    
    #-----La propulsion de la fusée-----
    if (i == 0): lune.SetPousse(Vector2(((10523.96404)*Constante.MASSE_LUNE),pousse_lune))
    else: lune.SetPousse(Vector2(0,0))

    lune.SetAcceleration(Cinematique.CalculAcceleration(masse_objet=lune.masse_objet, pousse=lune.pousse, position=lune.position))
    lune.SetVitesse(Cinematique.CalculVitesse(delta=Constante.DELTA, acceleration=lune.acceleration, vitesse=lune.vitesse))
    lune.SetPosition(Cinematique.CalculPosition(delta=Constante.DELTA, acceleration=lune.acceleration, vitesse=lune.vitesse, position=lune.position))
    lune.AppendX(lune.position.x)
    lune.AppendY(lune.position.y)
    
    if (lune.position.Norme() - Constante.RAYON_TERRE) < 0:
      print("i : ", i)
      break

#ProcessFusee()
print("1er")
#ProcessLune()


"""
print(fusee.position.Norme()-Constante.RAYON_TERRE)
print(Constante.RAYON_TERRE)
print(fusee.position.Norme() - Constante.RAYON_TERRE)
print(fusee.position.Get())
print(fusee.vitesse.Norme())


resolution = 1000 #number of points used to draw the circle 
a = Constante.POS_TERRE.x #I arbitrary chose a center-x coordinate called a 
b = Constante.POS_TERRE.y #the same for y 
r = Constante.RAYON_TERRE #radius of the circle 

x = [2*r*value/resolution + (a-r) for value in range(resolution-1)] 
x += [a+r] #so that the last point is exactly at the right-end of the circle 
 
y_plus = [(r**2 - (value-a)**2)**0.5 + b for value in x] 
y_minus = [2*b-value for value in y_plus] #y_plus - a = a - y_minus 

plt.figure(figsize=(6,6)) #so that the aspect ratio of circle is respected 
plt.plot(x,y_plus)
plt.plot(x,y_minus)
plt.plot(fusee.position_x,fusee.position_y)
plt.plot([a],[b],"x") #draw a cross at the center of the circle 
plt.show()


# Example file showing a circle moving on screen

import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
turn = 0
position_camera:Vector2 = Vector2(0,0)
facteur_reduction:float = 150/Constante.RAYON_TERRE

obj_terre = ObjetCelleste(position=Vector2(screen.get_width() / 2, screen.get_height() / 2), pousse=Vector2(0,0), masse_objet=Constante.MASSE_TERRE, rayon=Constante.RAYON_TERRE)

pos_x, pos_y = fusee.GetPosX(), fusee.GetPosY()

def Move(pos_before, dt):
  keys = pygame.key.get_pressed()
  if keys[pygame.K_UP]: pos_before[1] += 300 * dt
  if keys[pygame.K_DOWN]: pos_before[1] -= 300 * dt
  if keys[pygame.K_LEFT]: pos_before[0] += 300 * dt
  if keys[pygame.K_RIGHT]: pos_before[0] -= 300 * dt

  return Vector2(pos_before[0], pos_before[1])

print((lune.position.x*(facteur_reduction)+terre.position.x+position_camera.x, lune.position.y*(facteur_reduction)+terre.position.y+position_camera.y))

#input("lancer la simulation")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
          facteur_reduction = ((facteur_reduction*Constante.RAYON_TERRE)-(event.y))/Constante.RAYON_TERRE

    # fill the screen with a color to wipe away anything from last frame
    
    if turn+1000 < len(pos_x):
      turn += 1000

    screen.fill("black")

    #dessin de la Terre
    pygame.draw.circle(surface=screen, color="blue", center=(terre.position.x+position_camera.x, terre.position.y+position_camera.y), radius=(facteur_reduction)*Constante.RAYON_TERRE)
    #dessin de la fusée
    pygame.draw.circle(surface=screen, color="green", center=(fusee.position_x[turn]*(facteur_reduction)+terre.position.x+position_camera.x, fusee.position_y[turn]*(facteur_reduction)+terre.position.y+position_camera.y), radius=2)
    #dessin de la lune
    #pygame.draw.circle(surface=screen, color="white", center=(lune.position_x[turn]*(facteur_reduction)+terre.position.x+position_camera.x, lune.position_y[turn]*(facteur_reduction)+terre.position.y+position_camera.y), radius=(lune.rayon)*facteur_reduction)
    
    position_camera = Move(position_camera.Get(), dt=dt)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

"""