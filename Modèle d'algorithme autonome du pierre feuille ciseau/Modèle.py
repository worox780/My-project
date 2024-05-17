import random

victoire_ia = 0
victoire_joueur = 0

"""
pierre = 22
feuille = 9
ciseau = 10
joueur = 9
last_coup = 0
ia = 14

lst_pierre_suite = [[8, 2, 3], [3, 1, 5], [3, 1, 1], [2, 1, 2], [2, 1, 1], [1, 1, 2]]
lst_feuille_suite = [[6, 2, 2], [2, 1, 1]]
lst_ciseau_suite = [[3, 7, 1]]
suite_de_coup = [2,1] #nb répétition et le coup joué
"""

pierre = 0
feuille = 0
ciseau = 0
joueur = 0
last_coup = 0
ia = 0

lst_pierre_suite = [[1,1,1]]
lst_feuille_suite = [[1, 1, 1]]
lst_ciseau_suite = [[1, 1, 1]]
suite_de_coup = [0,1] #nb répétition et le coup joué

def CoeficientOrientationPierre():
  if (suite_de_coup[1] > len(lst_pierre_suite)): lst_pierre_suite.append([1,1,1])

def CoeficientOrientationFeuille():
  if (suite_de_coup[1] > len(lst_feuille_suite)): lst_feuille_suite.append([1,1,1])

def CoeficientOrientationCiseau():
  if (suite_de_coup[1] > len(lst_ciseau_suite)): lst_ciseau_suite.append([1,1,1])


def Probabilite():
  global ia
  p0 = 0
  p1 = 0
  p2 = 0
  #print(ia)
  if suite_de_coup[0] == 0:
    p0 = lst_pierre_suite[suite_de_coup[1]-1][0]/(sum(lst_pierre_suite[suite_de_coup[1]-1])*suite_de_coup[1])
    p1 = ((1-p0)*(lst_pierre_suite[suite_de_coup[1]-1][1]))/(lst_pierre_suite[suite_de_coup[1]-1][1]+lst_pierre_suite[suite_de_coup[1]-1][2])
    p2 = ((1-p0)*(lst_pierre_suite[suite_de_coup[1]-1][2]))/(lst_pierre_suite[suite_de_coup[1]-1][1]+lst_pierre_suite[suite_de_coup[1]-1][2])
    if ia < p1 * 100: ia = 1 #jouer feuille
    elif ia < (p0+p1) * 100: ia = 2 #jouer feuille
    else: ia = 0 #jouer ciseau

  elif suite_de_coup[0] == 1:
    p1 = lst_feuille_suite[suite_de_coup[1]-1][1]/(sum(lst_feuille_suite[suite_de_coup[1]-1])*suite_de_coup[1])
    p0 = ((1-p1)*(lst_feuille_suite[suite_de_coup[1]-1][0]))/(lst_feuille_suite[suite_de_coup[1]-1][0]+lst_feuille_suite[suite_de_coup[1]-1][2])
    p2 = ((1-p1)*(lst_feuille_suite[suite_de_coup[1]-1][2]))/(lst_feuille_suite[suite_de_coup[1]-1][0]+lst_feuille_suite[suite_de_coup[1]-1][2])
    if ia < p0 * 100: ia = 2 #jouer pierre
    elif ia < (p0+p1) * 100: ia = 0 #jouer feuille
    else: ia = 1 #jouer siceau
    
  else:
    p2 = lst_ciseau_suite[suite_de_coup[1]-1][2]/(sum(lst_ciseau_suite[suite_de_coup[1]-1])*suite_de_coup[1])
    p0 = ((1-p2)*(lst_ciseau_suite[suite_de_coup[1]-1][0]))/(lst_ciseau_suite[suite_de_coup[1]-1][0]+lst_ciseau_suite[suite_de_coup[1]-1][1])
    p1 = ((1-p2)*(lst_ciseau_suite[suite_de_coup[1]-1][1]))/(lst_ciseau_suite[suite_de_coup[1]-1][0]+lst_ciseau_suite[suite_de_coup[1]-1][1])
    if ia < p0 * 100: ia = 2 #jouer feuille
    elif ia < (p0+p2) * 100: ia = 1 #jouer ciseau
    else: ia = 0 #jouer pierre


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
  else: lst_ciseau_suite[suite_de_coup[1]-1][joueur] += 1


while joueur >= 0:
  try:
    joueur = int(input()) #coup du joueur --> 0 = pierre --> 1 = feuille --> 2 = ciseau
  except: break
  if joueur > 2: joueur = 2
  if joueur < 0: break
  #----- Section choix du coup de l'ia -----
  ia = random.random()*100 #coup de l'ia entre 0 et 100
  proba = Probabilite() #Choix du coup pour l'ia

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
    ciseau += 1
    SelectionListe(last_coup=last_coup)
    if suite_de_coup[0] == 2: #Verification si une série est en cours
      suite_de_coup[1] += 1
      CoeficientOrientationCiseau()
    else: #Sinon on modifie les informations de la suite de répétition
      suite_de_coup[0], suite_de_coup[1] = 2, 1
  
  last_coup = joueur
  print(Winer())

print(lst_pierre_suite)
print(lst_feuille_suite)
print(lst_ciseau_suite)

print(pierre, feuille, ciseau)

print(victoire_ia, victoire_joueur)