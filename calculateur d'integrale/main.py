import math

somme_trapeze = 0
borne_a = int(input("Borne a ?"))
borne_b = int(input("Borne b ?"))
delta_a_b = float(input("La distance qui sépare a de b ?"))

def Calcul(x): return math.exp(-x**2) #Fonction qui renvoie l'image de la fonction à approximer

while borne_a <= borne_b:
  somme_trapeze += (Calcul(borne_a)+(Calcul(borne_a+delta_a_b)))*(delta_a_b)/2
  borne_a += delta_a_b

print(f"L'intégrale entre {borne_a} et {borne_b} = ", somme_trapeze)