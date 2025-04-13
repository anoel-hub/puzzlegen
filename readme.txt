FR

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

EN

This Python script creates an interactive HTML5 puzzle from an image. Here's how to use it:
Features

Install uv (the ultra-fast package manager developed by Astral)
pip install uv

Automatically splits an image into a puzzle
Drag-and-drop interface for moving pieces
Automatically detects when the puzzle is complete
Stopwatch to measure solving time
Buttons to shuffle, reset, and view the original image
Visual marking when a piece is correctly placed

Usage
To generate a puzzle, run the script with the following parameters:

uv run puzgen.py path/to/image.jpg --rows 3 --cols 3 --output my_puzzle.html --lang fr

Parameters

image: Path to the image to be transformed into a puzzle (required)
--rows: Number of rows in the puzzle (default: 3)
--cols: Number of columns in the puzzle (default: 3)
--output or -o: Name of the output HTML file (default: 3) :puzzle.html)
--lang

You can specify the default language with --lang using one of the following values:

fr for French (default)
nl for Dutch
en for English

Once the puzzle is open in the browser, the user can change the language at any time by clicking the language buttons at the top of the page.
This multilingual feature makes your puzzle more accessible to an international audience!

How to Play

Open the generated HTML file in your browser
Drag the pieces from the container to the puzzle board
Position each piece in its correct place
A green border appears when a piece is correctly placed
When all the pieces are correctly placed, a congratulatory message is displayed

Customization
You can easily change the difficulty by changing the number of rows and columns. The more pieces, the more difficult the puzzle.
