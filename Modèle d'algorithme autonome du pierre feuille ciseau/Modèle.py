import random

victoire_ia = 0
victoire_joueur = 0

pierre = 22
feuille = 9
sisceau = 10
joueur = 9
last_coup = 0
ia = 14

lst_pierre_suite = [[8, 2, 3], [3, 1, 5], [3, 1, 1], [2, 1, 2], [2, 1, 1], [1, 1, 2]]
lst_feuille_suite = [[6, 2, 2], [2, 1, 1]]
lst_sisceau_suite = [[3, 7, 1]]
suite_de_coup = [2,1] #nb répétition et le coup joué

def CoeficientOrientationPierre():
  if (suite_de_coup[1] > len(lst_pierre_suite)): lst_pierre_suite.append([1,1,1])

def CoeficientOrientationFeuille():
  if (suite_de_coup[1] > len(lst_feuille_suite)): lst_feuille_suite.append([1,1,1])

def CoeficientOrientationSisceau():
  if (suite_de_coup[1] > len(lst_sisceau_suite)): lst_sisceau_suite.append([1,1,1])

"""
Pour p0, pierre concerné par la répétition, la formule est :

p0 = n0/(n*r) avec r la répétition
p1 = ((1-p0)*n1)/(n1+n2)
p2 = ((1-p0)*n2)/(n1+n2)
"""

def Probabilite():
  p0 = 0
  p1 = 0
  p2 = 0
  if suite_de_coup[0] == 0:
    p0 = lst_pierre_suite[suite_de_coup[1]-1][0]/(sum(lst_pierre_suite[suite_de_coup[1]-1])*suite_de_coup[1])
    p1 = ((1-p0)*(lst_pierre_suite[suite_de_coup[1]-1][1]))/(lst_pierre_suite[suite_de_coup[1]-1][1]+lst_pierre_suite[suite_de_coup[1]-1][2])
    p2 = ((1-p0)*(lst_pierre_suite[suite_de_coup[1]-1][2]))/(lst_pierre_suite[suite_de_coup[1]-1][1]+lst_pierre_suite[suite_de_coup[1]-1][2])
  elif suite_de_coup[0] == 1:
    p1 = lst_feuille_suite[suite_de_coup[1]-1][1]/(sum(lst_feuille_suite[suite_de_coup[1]-1])*suite_de_coup[1])
    p0 = ((1-p1)*(lst_feuille_suite[suite_de_coup[1]-1][0]))/(lst_feuille_suite[suite_de_coup[1]-1][0]+lst_feuille_suite[suite_de_coup[1]-1][2])
    p2 = ((1-p1)*(lst_feuille_suite[suite_de_coup[1]-1][2]))/(lst_feuille_suite[suite_de_coup[1]-1][0]+lst_feuille_suite[suite_de_coup[1]-1][2])
  else:
    p2 = lst_sisceau_suite[suite_de_coup[1]-1][2]/(sum(lst_sisceau_suite[suite_de_coup[1]-1])*suite_de_coup[1])
    p0 = ((1-p2)*(lst_sisceau_suite[suite_de_coup[1]-1][0]))/(lst_sisceau_suite[suite_de_coup[1]-1][0]+lst_sisceau_suite[suite_de_coup[1]-1][1])
    p1 = ((1-p2)*(lst_sisceau_suite[suite_de_coup[1]-1][1]))/(lst_sisceau_suite[suite_de_coup[1]-1][0]+lst_sisceau_suite[suite_de_coup[1]-1][1])
  
  return (p0,p1,p2)
  


print()
def Winer(): #Qui gagner
  global victoire_ia, victoire_joueur
  if (ia == 1) and (joueur == 0):
    victoire_ia += 1
    return "Victoire IA"
  elif (ia == 0) and (joueur == 2):
    victoire_ia += 1
    return "Victoire IA"
  elif (ia == 2) and (joueur == 1):
    victoire_ia += 1
    return "Victoire IA"
  elif (ia == joueur): return "Nulle"
  else:
    victoire_joueur += 1
    return "Victoire Joueur"


def SelectionListe(last_coup:int) -> None:
  if last_coup == 0: lst_pierre_suite[suite_de_coup[1]-1][joueur] += 1
  elif last_coup == 1: lst_feuille_suite[suite_de_coup[1]-1][joueur] += 1
  else: lst_sisceau_suite[suite_de_coup[1]-1][joueur] += 1


for i in range(100_000):
  try:
    joueur = random.randint(0,2) #coup du joueur --> 0 = pierre --> 1 = feuille --> 2 = ciseau
  except: break
  if joueur > 2: break
  ia = random.random()*100 #coup de l'ia entre 0 et 100

  #----- Section choix du coup de l'ia -----
  #print(Probabilite())
  proba = Probabilite()
  if ia < proba[1] * 100: ia = 1 #jouer feuille
  elif ia < (proba[0]+proba[1]) * 100: ia = 2 #jouer ciseau
  else: ia = 0 #jouer pierre

  #print(joueur)
  #----- Section pour le traitement du coup du joueur -----
  if joueur == 0: #Si pierre
    pierre += 1 
    SelectionListe(last_coup=last_coup)
    if suite_de_coup[0] == 0: #Verification si une série est en cours
      suite_de_coup[1] += 1
      CoeficientOrientationPierre()
    else: #Sinon on modifie les informations de la suite de répétition
      suite_de_coup[0], suite_de_coup[1] = 0, 1
  
  elif joueur == 1:
    feuille += 1
    SelectionListe(last_coup=last_coup)
    if suite_de_coup[0] == 1: #Verification si une série est en cours
      suite_de_coup[1] += 1
      CoeficientOrientationFeuille()
    else: #Sinon on modifie les informations de la suite de répétition
      suite_de_coup[0], suite_de_coup[1] = 1, 1

  else:
    sisceau += 1
    SelectionListe(last_coup=last_coup)
    if suite_de_coup[0] == 2: #Verification si une série est en cours
      suite_de_coup[1] += 1
      CoeficientOrientationSisceau()
    else: #Sinon on modifie les informations de la suite de répétition
      suite_de_coup[0], suite_de_coup[1] = 2, 1
  
  last_coup = joueur
  Winer()
  #print()

print(lst_pierre_suite)
print(lst_feuille_suite)
print(lst_sisceau_suite)

print(pierre, feuille, sisceau)

print(victoire_ia, victoire_joueur)