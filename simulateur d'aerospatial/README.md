Simulation d'orbite

L'objectif de se dossier est de vulgariser de la manère la plus simple possible la simulation orbitale.
Il s'agit également de s'amuser à calculer des équations accessibles.

Les problématiques :
  1- Le choix des équations de cinématique.
  2- Les forces à considérer.
  3- La méthode de résolution numérique à choisir.
  4- Comment corriger les erreurs d'orbites dû à la résolution numérique
  5- Comment mettre en place la résoltution partielle du problème à N corp

Problématique 1: -> partiellement résolue.  En cours de résolution.
  Le choix est fait sur les équations de cinématique de Newton.
  La deuxième loi de Newton est utilisé pour calculer les différentes accélérations et vitesses.
  En ce qui concerne la vitesse, le théorême de l'énergie mécanique est utilisé lorsqu'un objet ne fourni aucune force.
  Dans le cas où l'objet émet une poussé, les équations de Newton sont utilisées pour calculer la position.
  Une méthode entière détaillant les calculs sera faite.

Problématique 2: -> Résolue avec les forces actuelles.
  Les forces concidérées actuellement sont le poid et l'accélération de la poussé des objets.
  Une section plus approfondi sera faite par la suite pour également introduire les frottement dû à l'air dans l'atmosphère terrestre par exemple.

Problématique 3: -> partiellement résolue. En cours de résolution.
  Pour l'heure, la méthode d'Euler est utilisée.
  Pour limter les erreurs dans un premier temps, la méthode de Verlet ou saute mouton sera utilisé afin de diviser drastiquement la quantité d'erreurs dû au delta.
  Une partie entière sur la méthode utilisé sera faite.

Problématique 4: -> En cours de résolution.
  Deux cas sont à concidérer :
    1- Lorsque l'objet effectue une poussé. Dans ce càs là, seule une méthode de résolution numérique performante me semble obligatoire à trouver.
    2- Lorsque le corp n'effectue plus de poussé. L'utilisation du théorème de l'énergie mécanique est utile.
       Une problématique se pose sur la manière de récuperer la position exacte après le calcul de la nouvelle norme du vecteur position.
    Tout cela sera expliqué dans une partie indépendante.

Problématique 5: -> Non résolue. Il s'agit d'un problème secondaire.
  Pour la résolution partielle du problème à N corp, les calculs vont se faire sur l'accélération et par conséquent l'intensité du champ de pensenteur "g".
  Une partie entière sera élaboré sur le sujet plus tard.
