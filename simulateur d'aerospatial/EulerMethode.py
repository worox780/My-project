import numpy as np
import matplotlib.pyplot as plt



class Vector2:
  def __init__(self, x:float, y:float) -> None: self.x, self.y = x, y
  def Get(self) -> tuple: return [self.x, self.y]
  def Set(self, x:float, y:float): self.x, self.y = x, y
  def Norme(self) -> float: return np.sqrt(self.x**2 + self.y**2)

class ObjetCelleste:
  def __init__(self, position:Vector2=Vector2(0,0), pousse:Vector2=Vector2(0,0), masse_objet:float=1.0, rayon:float=1.0, energie_mecanique:float=0.0) -> None:
    #----------Vecteur2----------
    #-----Valeurs équation horaires-----
    self.acceleration:Vector2 = Vector2(0,0)
    self.vitesse:Vector2 = Vector2(0,0)
    self.position:Vector2 = position #position actuelle
    #-----------------------------------
    #-----Valeurs caractéristique de la fusée-----
    self.pousse:Vector2 = pousse
    #----------float----------
    self.masse_objet:float = masse_objet
    self.rayon:float = rayon
    self.energie_mecanique:float = energie_mecanique
    #----------list----------
    self.position_x:list = []
    self.position_y:list = []

  def SetAcceleration(self, valeur:Vector2) -> None: self.acceleration = valeur
  def SetVitesse(self, valeur:Vector2) -> None: self.vitesse = valeur
  def SetPosition(self, valeur:Vector2) -> None: self.position = valeur
  def SetPousse(self, valeur:Vector2) -> None: self.pousse = valeur
  def SetEnergieMecanique(self, valeur:float) -> None: self.energie_mecanique = valeur
  def AppendX(self, value) -> None:self.position_x.append(value)
  def AppendY(self, value) -> None:self.position_y.append(value)


class Constante:
  G = 6.67*10**(-11)
  MASSE_TERRE = 5.972*10**24 #en kg
  RAYON_TERRE = 6_371_000 #en mètre
  POS_TERRE = Vector2(0,0) #origine du monde
  RAYON_LUNE = 1_738_000
  MASSE_LUNE = 7.347*10**22
  DELTA = 1


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
  def CalculVitesse(delta:float, acceleration_n:Vector2, acceleration_n1:Vector2, vitesse:Vector2) -> Vector2:
    #equation --> V(i) + 0.5*(a(i)+a(i+1))*delta
    return Vector2(0.5*(acceleration_n.x + acceleration_n1.x)*delta + vitesse.x, 0.5*(acceleration_n.y + acceleration_n1.y)*delta + vitesse.y)
  def CalculPosition(delta:float, acceleration:Vector2, vitesse:Vector2, position:Vector2) -> Vector2:
    #equation --> (1/(2*g))*(V(i)**2 - v(i+1))
    return Vector2(position.x + vitesse.x*delta + 0.5*(acceleration.x*delta**2), position.y + vitesse.y*delta + 0.5*(acceleration.y*delta**2))
  def CalculPositionNew(vitesse_actuelle:Vector2, vitesse_suivante:Vector2, position_actuelle:Vector2, position_suivante:Vector2, gravite:Vector2) -> Vector2:
    #equation --> h(b) = (G*M(terre))/((0.5 * V(i)**2)+(h(i)*g(i))-(0.5*V(i+1)))
    #norme_position = (vitesse_actuelle.Norme()**2 - vitesse_suivante.Norme()**2)/(2*gravite.Norme()) + (position_actuelle.Norme())
    norme_position = 1/( (vitesse_actuelle.Norme()**2)/(2*Constante.G*Constante.MASSE_TERRE) + 1/position_actuelle.Norme() - (vitesse_suivante.Norme()**2)/(2*Constante.G*Constante.MASSE_TERRE))

    pos_x:float = norme_position*(gravite.x/gravite.Norme())
    pos_y:float = norme_position*(gravite.y/gravite.Norme())

    return Vector2(pos_x,pos_y)


    

    


class Energie:
  def EnergieCinetique(masse_objet:float, vitesse:float) -> float:
    return 0.5 * vitesse**2 * masse_objet
  def EnergiePotentielPesenteur(masse_objet:float, altitude:float, pesenteur:float) -> float:
    return pesenteur*altitude*masse_objet
  def EnergieMecanique(Ec:float, Epp:float) -> float:
    return Ec+Epp

fusee:ObjetCelleste = ObjetCelleste(position=Vector2(0, Constante.RAYON_TERRE), pousse=Vector2(0,15_120_000), masse_objet=780000, rayon=2)
terre:ObjetCelleste = ObjetCelleste(position=Vector2(0,0), pousse=Vector2(0,0), masse_objet=Constante.MASSE_TERRE, rayon=Constante.RAYON_TERRE)
lune:ObjetCelleste = ObjetCelleste(position=Vector2(0,Constante.RAYON_TERRE+384_400_000+Constante.RAYON_LUNE), pousse=Vector2(0,0), masse_objet=Constante.MASSE_TERRE, rayon=Constante.RAYON_LUNE)


def ProcessFusee():
  energie = []
  alti_theo = []
  alti_theo2 = []
  alti_actu = []
  for i in range(100_000): #int(226520*3)
    #-----La propulsion de la fusée-----
    gravite:Vector2 = Gravite.IntensitePesenteur(position=fusee.position, masse_attracteur=Constante.MASSE_TERRE, rayon=Constante.RAYON_TERRE, position_attracteur=Constante.POS_TERRE)
    Ec = Energie.EnergieCinetique(masse_objet=fusee.masse_objet, vitesse=fusee.vitesse.Norme())
    Epp = Energie.EnergiePotentielPesenteur(masse_objet=fusee.masse_objet, altitude=(fusee.position.Norme()-Constante.RAYON_TERRE), pesenteur=gravite.Norme())
    energie.append(Ec+Epp)
    if (i <= 350/Constante.DELTA):
      fusee.SetPousse(Vector2(i*100_000*Constante.DELTA,15_120_000))
    elif (i >= (3837//2)) and (i <= (3837//2) + 120/Constante.DELTA):
      fusee.SetPousse(Vector2(100_000,-12_120_000))
    else:fusee.SetPousse(Vector2(0,0))
    
    
    #print(fusee.energie_mecanique == energie[-1])

    accel_inter = Cinematique.CalculAcceleration(masse_objet=fusee.masse_objet, pousse=fusee.pousse, position=fusee.position)
    vit_inter = Cinematique.CalculVitesse(delta=Constante.DELTA, acceleration_n=fusee.acceleration, acceleration_n1=accel_inter, vitesse=fusee.vitesse)
    pos_inter = Cinematique.CalculPosition(delta=Constante.DELTA, acceleration=fusee.acceleration, vitesse=fusee.vitesse, position=fusee.position)
    
    
    #alti_actu.append(fusee.position.Norme()-Constante.RAYON_TERRE)
    if (i <= 350/Constante.DELTA):# or ((i >= (3837//2)) and (i <= (3837//2) + 120*Constante.DELTA)):
      #fusee.energie_mecanique = Ec+Epp
      alti_theo2.append(fusee.position.Norme()-Constante.RAYON_TERRE)
      #alti_theo2.append(fusee.position.Norme()-Constante.RAYON_TERRE)
    else:
      pass
      #pos_inter = Cinematique.CalculPositionNew(vitesse_actuelle=fusee.vitesse, vitesse_suivante=vit_inter, position_actuelle=fusee.position, position_suivante=pos_inter, gravite=gravite)
      #alti_theo2.append(pos_inter.Norme()-Constante.RAYON_TERRE)
      #alti_theo.append(1/( (fusee.vitesse.Norme()**2)/(2*Constante.G*Constante.MASSE_TERRE) + 1/fusee.position.Norme() - (vit_inter.Norme()**2)/(2*Constante.G*Constante.MASSE_TERRE)))
      #print(alti_theo2[-1])
      #print(alti_theo[-1], " : ", alti_theo2[-1])"""
      

    fusee.SetAcceleration(accel_inter)
    fusee.SetVitesse(vit_inter)
    fusee.SetPosition(pos_inter)

    fusee.AppendX(pos_inter.x)
    fusee.AppendY(pos_inter.y)
    
    
    #print(fusee.position.Norme() - Constante.RAYON_TERRE)
    if (fusee.position.Norme() - Constante.RAYON_TERRE) < 0:
      print("i : ", i)
      break
  
  return (energie, alti_actu, alti_theo, alti_theo2)

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


print("lolol")
processe = ProcessFusee()


timee = []
for i in range(100_000): timee.append(i)

print("1er")
print(len(processe[-1]))



resolution = 1000 #number of points used to draw the circle 
a = Constante.POS_TERRE.x #I arbitrary chose a center-x coordinate called a 
b = Constante.POS_TERRE.y #the same for y 
r = Constante.RAYON_TERRE #radius of the circle 

x = [2*r*value/resolution + (a-r) for value in range(resolution-1)] 
x += [a+r] #so that the last point is exactly at the right-end of the circle 
 
y_plus = [(r**2 - (value-a)**2)**0.5 + b for value in x] 
y_minus = [2*b-value for value in y_plus] #y_plus - a = a - y_minus 

fig, (p1,p3) = plt.subplots(2)

p3.plot(x,y_plus)
p3.plot(x,y_minus)
p3.plot(fusee.position_x,fusee.position_y)
p3.plot([a],[b],"x") #draw a cross at the center of the circle 

p1.plot(timee, processe[0])
"""
p1.plot(timee, processe[-1], label="actue")
p1.plot(timee, processe[2], label="theo")
#p1.plot(timee, processe[3], label="theo2")
p1.legend()"""

"""p2.plot(timee, processe[0][0], label="Em")
p2.plot(timee, processe[0][1], label="Ec")
p2.plot(timee, processe[0][2], label="Epp")
p2.legend()"""
plt.show()


# Example file showing a circle moving on screen
"""
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