import numpy as np

import matplotlib.pyplot as plt


class Vector2:
  def __init__(self, x:float, y:float) -> None: self.x, self.y = x, y
  def Get(self) -> tuple: return [self.x, self.y]
  def Set(self, x:float, y:float): self.x, self.y = x, y
  def Norme(self) -> float: return np.sqrt(self.x**2 + self.y**2)


class Constante:
  G = 6.67*10**(-11)
  MASSE_TERRE = 5.972*10**24 #en kg
  RAYON_TERRE = 6_371_000 #en mètre
  POS_TERRE = Vector2(0,0) #origine du monde
  RAYON_LUNE = 1_738_000
  MASSE_LUNE = 7.347*10**22
  DELTA = 1


class Gravite:
  def IntensitePesenteur(
      position_:Vector2, masse_attracteur_:float, rayon_:float
      ) -> Vector2:
    if position_.Norme() < rayon_: gravite:float = ((position_.Norme()/rayon_) * ((Constante.G*masse_attracteur_)/((rayon_)**2)))**2 #la gravité sur l'axe x est proportionnel à la profondeur, le rayon et l'intensité à la surface en fonction de la profondeur s'il on est dans la planète
    else: gravite:float = ((Constante.G*masse_attracteur_)/(position_.Norme()**2))**2

    pos_x:float = gravite*(position_.x/position_.Norme())
    pos_y:float = gravite*(position_.y/position_.Norme())

    if pos_x != 0: pos_x = np.sqrt(abs(pos_x))*(pos_x/abs(pos_x))
    if pos_y != 0: pos_y = np.sqrt(abs(pos_y))*(pos_y/abs(pos_y))

    return Vector2(pos_x,pos_y)
  def ForceInteraction(
      masse_objet1_:float, masse_objet2_:float,
      position_objet1_:Vector2, position_objet2_:Vector2
      ) -> float:
    distance:Vector2 = Vector2(position_objet1_.x-position_objet2_.x, position_objet1_.y-position_objet2_.y).Norme()
    return (Constante.G*masse_objet1_*masse_objet2_)/(distance**2)


class EquationHoraire:
  def CalculAcceleration(
      masse_objet_:float, pousse_:Vector2, position_:Vector2
      )-> Vector2:
    gravite:Vector2 = Gravite.IntensitePesenteur(
      position_=position_, masse_attracteur_=Constante.MASSE_TERRE,
      rayon_=Constante.RAYON_TERRE
      )
    acceleration = Vector2((pousse_.x)/masse_objet_ - gravite.x, (pousse_.y)/masse_objet_ - gravite.y)
    return acceleration
  def CalculVitesse(
      acceleration_n_:Vector2, vitesse_:Vector2
      ) -> Vector2:
    #equation --> formule de la vitesse de Newton
    return Vector2(acceleration_n_.x*Constante.DELTA + vitesse_.x, acceleration_n_.y*Constante.DELTA + vitesse_.y)
  def CalculPosition(
      acceleration_:Vector2, vitesse_:Vector2, position_:Vector2, delta=Constante.DELTA
      ) -> Vector2:
    #equation --> formule de la position de Newton
    return Vector2(0.5*(acceleration_.x*delta**2) + vitesse_.x*delta + position_.x, 0.5*(acceleration_.y*delta**2) + vitesse_.y*delta + position_.y)


class EquationEnergie:
  def CalculPosition(position_:Vector2, vitesse_actuelle_:Vector2, vitesse_future_:Vector2)-> Vector2:
    gravite:Vector2 = Gravite.IntensitePesenteur(
      position_=position_, masse_attracteur_=Constante.MASSE_TERRE,
      rayon_=Constante.RAYON_TERRE
      )
    #print(0.5 * vitesse_actuelle_.Norme()**2 * 780000 + gravite.Norme()*(position_.Norme()-Constante.RAYON_TERRE)*780000)
    delta_polynome = 2*vitesse_actuelle_.Norme()**2 - vitesse_future_.Norme()**2
    #print(delta_polynome)
    if delta_polynome < 0: return 1
    temps_delta = (-vitesse_actuelle_.Norme()+np.sqrt(delta_polynome))/gravite.Norme()
    if temps_delta < 0: return Constante.DELTA
    return temps_delta
    """
    distance **= 2
    
    pos_x:float = distance*(gravite.x/gravite.Norme())
    pos_y:float = distance*(gravite.y/gravite.Norme())

    if pos_x != 0: pos_x = np.sqrt(abs(pos_x))*(pos_x/abs(pos_x))
    if pos_y != 0: pos_y = np.sqrt(abs(pos_y))*(pos_y/abs(pos_y))
    #print(Vector2(pos_x, pos_y).Norme())
    return Vector2(pos_x, pos_y)"""

  def CalculPositionNew(masse_:float, vitesse_now_:Vector2, vitesse_future_:Vector2, position_:Vector2, gravite_:Vector2):
    em_a = 0.5 * vitesse_now_.Norme()**2 * masse_ + gravite_.Norme() * masse_ * (position_.Norme()-Constante.RAYON_TERRE)
    coef_a = (em_a - 0.5 * vitesse_future_.Norme()**2 * masse_)/(Constante.G * Constante.MASSE_TERRE * masse_)
    coef_b = (2 * Constante.RAYON_TERRE * em_a - Constante.RAYON_TERRE * masse_ * vitesse_future_.Norme()**2 - Constante.G * Constante.MASSE_TERRE * masse_)/(Constante.G * Constante.MASSE_TERRE * masse_)
    coef_c = (Constante.RAYON_TERRE**2 * em_a - Constante.RAYON_TERRE**2 * 0.5 * masse_ * vitesse_future_.Norme()**2)

    return (abs(coef_b**2), (4 * coef_a * coef_c))

class ObjetCelleste:
  def __init__(self, position:Vector2=Vector2(0,0),
               pousse:Vector2=Vector2(0,0), masse_objet:float=1.0,
               rayon:float=1.0, energie_mecanique:float=0.0
               ) -> None:
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


def CalculDelta(Em_a, m, v_b):

  denominateur = Constante.G*Constante.MASSE_TERRE*m

  coef_a = (Em_a-0.5*m*v_b**2)/denominateur
  numerateur_b = (2*Constante.RAYON_TERRE*Em_a-Constante.RAYON_TERRE*m*v_b**2-Constante.G*Constante.MASSE_TERRE*m)
  coef_b = numerateur_b/denominateur
  coef_c = (Constante.RAYON_TERRE**2 *Em_a- Constante.RAYON_TERRE**2 * 0.5*m*v_b**2)/denominateur

  delta = coef_b**2 - 4*coef_a*coef_c
  print(delta)
  if delta > 0:
    valeur_recherche = (-coef_b + np.sqrt(delta))/(2*coef_a)
    if valeur_recherche > 0: return valeur_recherche
  return 1
  



    

    


class Energie:
  def EnergieCinetique(masse_objet:float, vitesse:float) -> float:
    return 0.5 * vitesse**2 * masse_objet
  def EnergiePotentielPesenteur(masse_objet:float, altitude:float, pesenteur:float) -> float:
    return pesenteur*altitude*masse_objet
  def EnergieMecanique(Ec:float, Epp:float) -> float:
    return Ec+Epp

fusee:ObjetCelleste = ObjetCelleste(position=Vector2(0, Constante.RAYON_TERRE), pousse=Vector2(0,15_120_000), masse_objet=780000, rayon=2)
terre:ObjetCelleste = ObjetCelleste(position=Vector2(0,0), pousse=Vector2(0,0), masse_objet=Constante.MASSE_TERRE, rayon=Constante.RAYON_TERRE)
#lune:ObjetCelleste = ObjetCelleste(position=Vector2(0,Constante.RAYON_TERRE+384_400_000+Constante.RAYON_LUNE), pousse=Vector2(0,0), masse_objet=Constante.MASSE_TERRE, rayon=Constante.RAYON_LUNE)


def ProcessFusee():
  lst_em = []
  for i in range(10_000): #int(226520*3)
    #-----La propulsion de la fusée-----
    if (i <= 350/Constante.DELTA):
      fusee.SetPousse(Vector2(i*100_000*Constante.DELTA,15_120_000))
    elif (i >= (2000//2)) and (i <= (2000//2) + 1_00/Constante.DELTA):
      fusee.SetPousse(Vector2(10_000_000,-12_120_000))
    else:fusee.SetPousse(Vector2(0,0))
    

    accel_inter = EquationHoraire.CalculAcceleration(masse_objet_=fusee.masse_objet, pousse_=fusee.pousse, position_=fusee.position)
    vit_inter = EquationHoraire.CalculVitesse(acceleration_n_=fusee.acceleration, vitesse_=fusee.vitesse)
    inter_lol = Constante.DELTA
    if fusee.pousse.Get() == [0,0]:
      gravite:Vector2 = Gravite.IntensitePesenteur(
        position_=fusee.position, masse_attracteur_=Constante.MASSE_TERRE,
        rayon_=Constante.RAYON_TERRE
        )
      lst_em.append(0.5*fusee.position.Norme()**2*fusee.masse_objet + fusee.masse_objet*gravite.Norme()*(fusee.position.Norme()-Constante.RAYON_TERRE))
    

      inter_lol = CalculDelta(
        Em_a=lst_em[-1], m=fusee.masse_objet, v_b=fusee.vitesse.Norme())
      #print(inter_lol)
      #inter_lol = EquationEnergie.CalculPosition(position_=fusee.position, vitesse_actuelle_=fusee.vitesse, vitesse_future_=vit_inter)
    pos_inter = EquationHoraire.CalculPosition(acceleration_=fusee.acceleration, vitesse_=fusee.vitesse, position_=fusee.position, delta=inter_lol)
    
    
    fusee.SetAcceleration(accel_inter)
    fusee.SetVitesse(vit_inter)
    fusee.SetPosition(pos_inter)

    fusee.AppendX(pos_inter.x)
    fusee.AppendY(pos_inter.y)
    
    
    #print(fusee.position.Norme() - Constante.RAYON_TERRE)
    if (fusee.position.Norme() - Constante.RAYON_TERRE) < 0:
      print("i : ", i)
      break
  return lst_em


processe = ProcessFusee()
lst_t = []
for i in range(len(processe)):
  lst_t.append(i)

resolution = 1000 #number of points used to draw the circle 
a = Constante.POS_TERRE.x #I arbitrary chose a center-x coordinate called a 
b = Constante.POS_TERRE.y #the same for y 
r = Constante.RAYON_TERRE #radius of the circle 

x = [2*r*value/resolution + (a-r) for value in range(resolution-1)] 
x += [a+r] #so that the last point is exactly at the right-end of the circle 
 
y_plus = [(r**2 - (value-a)**2)**0.5 + b for value in x] 
y_minus = [2*b-value for value in y_plus] #y_plus - a = a - y_minus 

fig, (p3) = plt.subplots(1)

p3.plot(x,y_plus)
p3.plot(x,y_minus)
p3.plot(fusee.position_x,fusee.position_y)
p3.plot([a],[b],"x") #draw a cross at the center of the circle 

fig, (p1) = plt.subplots(1)
#p1.plot(timee, processe[0])
p1.plot(lst_t, processe, label="actue")
p1.legend()
"""
"""

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