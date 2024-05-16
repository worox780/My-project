Ce dossier contient un programme en cours de développement.

Cet algorithme à pour objectif de gagner au jeu pierre, feuille, ciseau contre un humain.
L'algorithme peut être inspirer de celui dit de Minasi, même si aucune recherche n'ont été faites sur le sujet.

Sur un total de 18 tirrages de 100_000 parties chacun, dans lequel le joueur était simulé par un générateur de valeurs aléatoires, l'algorithme a gagné 9/16 des parties contre 7/16 des parties gagnées par l'algorithme de générations aléatoires de valeurs.

Les scores des victoires des 18 tirrages de 100_000 parties simulés sont :
Quand le résultat est négatif, cela signifi que le joueur a gagné. Dans le cas contraire, l'algorithme a gagné.

|IA|Joueur|Résultat|
| --- | --- | --- |
|33062|33490|`-428`|
|33284|33483|`-199`|
|33416|33403|`13`|
|33397|33428|`-31`|
|33173|33517|`-344`|
|33416|33149|`267`|
|33381|33013|`368`|
|33294|33327|`-33`|
|33145|33071|`74`|
|33009|33562|`-553`|
|33513|33255|`258`|
|33644|33280|`364`|
|33368|33584|`-216`|
|33670|33050|`620`|
|33377|33114|`263`|
|33502|33162|`340`|

Victoire joueur : 7.
Victoire algorithme : 9.
18 tirrages de 100_000 parties chacun.


Sur une série de 10 tirrages de 50 parties chacun, simulés contre un vrai joueur, les résultats sont les suivants :

|IA|Joueur|Résultat|
| --- | --- | --- |
|15|18|`-3`|
|22|12|`10`|
|20|14|`6`|
|9|11|`-2`|
|16|17|`-1`|
|19|15|`4`|
|13|28|`-5`|
|15|16|`-1`|
|21|17|`4`|
|11|20|`-9`|

Victoire joueur : 6.
Victoire algorithme : 4.
Différence totale des écarts de scores finaux : 3. Cela signifie que sur le total de toutes les parties, l'IA a gagné 3 parties de plus avec 10 jeux de données différents. Cela ne démontre en aucun càs l'éfficacité de l'algorithme.
10 tirrages de 50 parties chacun.