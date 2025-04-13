Ce script Python crée un puzzle interactif HTML5 à partir d'une image. Voici comment l'utiliser :
Fonctionnalités

Installer uv (le gestionnaire de paquets ultra-rapide développé par Astral)
pip install uv


Découpe automatique d'une image en puzzle
Interface glisser-déposer pour déplacer les pièces
Détection automatique lorsque le puzzle est terminé
Chronomètre pour mesurer le temps de résolution
Boutons pour mélanger, réinitialiser et voir l'image originale
Marquage visuel lorsqu'une pièce est correctement placée

Utilisation
Pour générer un puzzle, exécutez le script avec les paramètres suivants :

uv run puzgen.py chemin/vers/image.jpg --rows 3 --cols 3 --output mon_puzzle.html --lang fr


Paramètres

image : Chemin vers l'image à transformer en puzzle (obligatoire)
--rows : Nombre de lignes du puzzle (défaut : 3)
--cols : Nombre de colonnes du puzzle (défaut : 3)
--output ou -o : Nom du fichier HTML de sortie (défaut : puzzle.html)
--lang

Vous pouvez spécifier la langue par défaut avec --lang en utilisant l'une des valeurs suivantes :

fr pour le français (défaut)
nl pour le néerlandais
en pour l'anglais

Une fois le puzzle ouvert dans le navigateur, l'utilisateur peut changer de langue à tout moment en cliquant sur les boutons de langue en haut de la page.
Cette fonctionnalité multilingue rend votre puzzle plus accessible à un public international !

Comment jouer

Ouvrez le fichier HTML généré dans votre navigateur
Faites glisser les pièces du conteneur vers le tableau de puzzle
Positionnez chaque pièce à sa place correcte
Une bordure verte apparaît lorsqu'une pièce est bien placée
Quand toutes les pièces sont correctement placées, un message de félicitation s'affiche

Personnalisation
Vous pouvez facilement modifier la difficulté en changeant le nombre de lignes et de colonnes. Plus il y a de pièces, plus le puzzle est difficile.