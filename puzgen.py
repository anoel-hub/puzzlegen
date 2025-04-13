# /// script
# dependencies = [
#   "pillow",
#   "argparse"
# ]
# ///

import argparse
import random
import base64
import io
from pathlib import Path
from PIL import Image


def split_image(image_path, rows, cols):
    """Découpe image en morceaux pour le puzzle."""
    with Image.open(image_path) as img:
        # Récupérer les dimensions de image
        width, height = img.size
        
        # Calculer la taille de chaque pièce
        piece_width = width // cols
        piece_height = height // rows
        
        pieces = []
        for i in range(rows):
            for j in range(cols):
                # Coordonnées de découpage
                left = j * piece_width
                upper = i * piece_height
                right = left + piece_width
                lower = upper + piece_height
                
                # Découper la pièce
                piece = img.crop((left, upper, right, lower))
                
                # Sauvegarder les informations sur la pièce
                pieces.append({
                    "img": piece,
                    "original_position": i * cols + j,
                    "current_position": i * cols + j
                })
        
        # Mélanger les positions actuelles
        random.shuffle([piece["current_position"] for piece in pieces])
        
        return pieces, piece_width, piece_height, width, height


def encode_image_base64(img):
    """Encode une image PIL en base64 pour intégrer dans le HTML."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def generate_html(pieces, piece_width, piece_height, original_width, original_height, rows, cols, image_path):
    """Génère le code HTML pour le puzzle."""
    image_data = [encode_image_base64(piece["img"]) for piece in pieces]
    
    # Encoder image complète en base64 pour aperçu
    with Image.open(image_path) as full_img:
        full_image_base64 = encode_image_base64(full_img)
    
    # Traductions pour les différentes langues
    translations = {
        'fr': {
            'title': 'Puzzle HTML5',
            'time': 'Temps',
            'shuffle': 'Mélanger',
            'reset': 'Réinitialiser',
            'show_preview': 'Voir image originale',
            'win_message': 'Félicitations ! Vous avez terminé le puzzle !'
        },
        'nl': {
            'title': 'HTML5 Puzzel',
            'time': 'Tijd',
            'shuffle': 'Schudden',
            'reset': 'Resetten',
            'show_preview': 'Toon originele afbeelding',
            'win_message': 'Gefeliciteerd! Je hebt de puzzel voltooid!'
        },
        'en': {
            'title': 'HTML5 Puzzle',
            'time': 'Time',
            'shuffle': 'Shuffle',
            'reset': 'Reset',
            'show_preview': 'Show original image',
            'win_message': 'Congratulations! You completed the puzzle!'
        }
    }
    
    # Template HTML avec JavaScript pour interactivité
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puzzle HTML5</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f0f0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
        .container {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            justify-content: center;
        }}
        .puzzle-board {{
            width: {original_width}px;
            height: {original_height}px;
            border: 2px solid #000;
            position: relative;
            background-color: #fff;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        .piece-container {{
            width: {original_width}px;
            min-height: {original_height}px;
            border: 2px solid #000;
            position: relative;
            background-color: #eee;
            display: flex;
            flex-wrap: wrap;
            padding: 10px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }}
        .puzzle-piece {{
            width: {piece_width}px;
            height: {piece_height}px;
            position: absolute;
            cursor: grab;
            transition: box-shadow 0.2s;
            box-sizing: border-box;
        }}
        .puzzle-piece:hover {{
            box-shadow: 0 0 10px rgba(0, 0, 255, 0.5);
        }}
        .puzzle-piece.correct {{
            border: 2px solid green;
        }}
        .puzzle-slot {{
            width: {piece_width}px;
            height: {piece_height}px;
            position: absolute;
            border: 1px dotted #999;
            box-sizing: border-box;
        }}
        .controls {{
            margin: 20px 0;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            justify-content: center;
        }}
        button {{
            padding: 10px 15px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            margin: 0 5px;
        }}
        button:hover {{
            background-color: #45a049;
        }}
        .timer {{
            font-size: 24px;
            margin: 10px 0;
        }}
        .win-message {{
            font-size: 24px;
            color: green;
            font-weight: bold;
            margin: 20px 0;
            display: none;
        }}
        .language-selector {{
            margin: 10px 0;
            display: flex;
            gap: 10px;
        }}
        .language-btn {{
            padding: 5px 10px;
            background-color: #ddd;
            border: 1px solid #999;
            border-radius: 3px;
            cursor: pointer;
        }}
        .language-btn.active {{
            background-color: #4CAF50;
            color: white;
        }}
    </style>
</head>
<body>
    <h1 id="title">Puzzle HTML5</h1>
    <div class="language-selector">
        <button class="language-btn active" data-lang="fr">Français</button>
        <button class="language-btn" data-lang="nl">Nederlands</button>
        <button class="language-btn" data-lang="en">English</button>
    </div>
    <div class="timer"><span id="time-label">Temps</span>: <span id="minutes">00</span>:<span id="seconds">00</span></div>
    <div class="controls">
        <button id="shuffle">Mélanger</button>
        <button id="reset">Réinitialiser</button>
        <button id="show-preview">Voir image originale</button>
    </div>
    <div class="container">
        <div class="puzzle-board" id="puzzle-board">
            <!-- Les emplacements du puzzle seront créés par JavaScript -->
        </div>
        <div class="piece-container" id="piece-container">
            <!-- Les pièces du puzzle seront créées par JavaScript -->
        </div>
    </div>
    <div class="win-message" id="win-message">Félicitations ! Vous avez terminé le puzzle !</div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // Traductions
            const translations = {{
                fr: {{
                    title: 'Puzzle HTML5',
                    time: 'Temps',
                    shuffle: 'Mélanger',
                    reset: 'Réinitialiser',
                    show_preview: 'Voir image originale',
                    win_message: 'Félicitations ! Vous avez terminé le puzzle !'
                }},
                nl: {{
                    title: 'HTML5 Puzzel',
                    time: 'Tijd',
                    shuffle: 'Schudden',
                    reset: 'Resetten',
                    show_preview: 'Toon originele afbeelding',
                    win_message: 'Gefeliciteerd! Je hebt de puzzel voltooid!'
                }},
                en: {{
                    title: 'HTML5 Puzzle',
                    time: 'Time',
                    shuffle: 'Shuffle',
                    reset: 'Reset',
                    show_preview: 'Show original image',
                    win_message: 'Congratulations! You completed the puzzle!'
                }}
            }};
            
            // Éléments de l'interface
            const titleElement = document.getElementById('title');
            const timeLabel = document.getElementById('time-label');
            const shuffleButton = document.getElementById('shuffle');
            const resetButton = document.getElementById('reset');
            const showPreviewButton = document.getElementById('show-preview');
            const winMessage = document.getElementById('win-message');
            const languageButtons = document.querySelectorAll('.language-btn');
            
            // Fonction pour changer la langue
            function changeLanguage(lang) {{
                document.documentElement.lang = lang;
                titleElement.textContent = translations[lang].title;
                timeLabel.textContent = translations[lang].time;
                shuffleButton.textContent = translations[lang].shuffle;
                resetButton.textContent = translations[lang].reset;
                showPreviewButton.textContent = translations[lang].show_preview;
                winMessage.textContent = translations[lang].win_message;
                
                // Mettre à jour le bouton de langue actif
                languageButtons.forEach(btn => {{
                    if (btn.dataset.lang === lang) {{
                        btn.classList.add('active');
                    }} else {{
                        btn.classList.remove('active');
                    }}
                }});
            }}
            
            // Ajouter des écouteurs d'événements pour les boutons de langue
            languageButtons.forEach(btn => {{
                btn.addEventListener('click', function() {{
                    changeLanguage(this.dataset.lang);
                }});
            }});
            
            const pieces = [
                {", ".join([f"""{{
                    id: {i},
                    img: "data:image/png;base64,{image_data[i]}",
                    originalPosition: {pieces[i]["original_position"]},
                    currentPosition: null
                }}""" for i in range(len(pieces))])}
            ];
            
            const puzzleBoard = document.getElementById('puzzle-board');
            const pieceContainer = document.getElementById('piece-container');
            
            let draggingPiece = null;
            let startX, startY;
            let timerInterval;
            let seconds = 0;
            let minutes = 0;
            
            // Création des emplacements du puzzle
            for (let i = 0; i < {rows * cols}; i++) {{
                const row = Math.floor(i / {cols});
                const col = i % {cols};
                
                const slot = document.createElement('div');
                slot.className = 'puzzle-slot';
                slot.style.left = (col * {piece_width}) + 'px';
                slot.style.top = (row * {piece_height}) + 'px';
                slot.dataset.position = i;
                puzzleBoard.appendChild(slot);
            }}
            
            // Initialisation des pièces
            initializePieces();
            
            // Démarrer le chronomètre
            startTimer();
            
            // Fonction pour trouver une position disponible dans la réserve
            function getAvailablePositionInReserve() {{
                // Trouver une position disponible dans la réserve
                const usedPositions = Array.from(pieceContainer.querySelectorAll('.puzzle-piece')).map(p => {{
                    return {{
                        x: parseInt(p.style.left) || 0,
                        y: parseInt(p.style.top) || 0
                    }};
                }});
                
                // Calculer une grille de positions possibles
                const cols = Math.floor(pieceContainer.clientWidth / ({piece_width} + 5));
                let row = 0;
                let col = 0;
                
                // Trouver la première position libre
                while (true) {{
                    const x = col * ({piece_width} + 5);
                    const y = row * ({piece_height} + 5);
                    
                    // Vérifier si cette position est déjà occupée
                    const isOccupied = usedPositions.some(pos => 
                        Math.abs(pos.x - x) < {piece_width} / 2 && 
                        Math.abs(pos.y - y) < {piece_height} / 2
                    );
                    
                    if (!isOccupied) {{
                        return {{ x, y }};
                    }}
                    
                    // Passer à la position suivante
                    col++;
                    if (col >= cols) {{
                        col = 0;
                        row++;
                    }}
                    
                    // Éviter une boucle infinie si aucune position nest trouvée
                    if (row > 20) {{
                        return {{ x: Math.random() * 100, y: Math.random() * 100 }};
                    }}
                }}
            }}
            
            // Fonctions
            function initializePieces() {{
                pieceContainer.innerHTML = '';
                
                // Mélanger les pièces
                const shuffledPieces = [...pieces];
                shuffleArray(shuffledPieces);
                
                // Placer les pièces dans le conteneur
                shuffledPieces.forEach((piece, index) => {{
                    const pieceElement = document.createElement('div');
                    pieceElement.className = 'puzzle-piece';
                    pieceElement.style.backgroundImage = `url("${{piece.img}}")`;
                    pieceElement.style.backgroundSize = `{piece_width}px {piece_height}px`;
                    pieceElement.dataset.id = piece.id;
                    
                    // Positionner les pièces de manière aléatoire dans le conteneur
                    const row = Math.floor(index / 4);
                    const col = index % 4;
                    pieceElement.style.left = (col * ({piece_width} + 5)) + 'px';
                    pieceElement.style.top = (row * ({piece_height} + 5)) + 'px';
                    
                    // Ajouter les écouteurs dévénements pour le glisser-déposer
                    pieceElement.addEventListener('mousedown', startDrag);
                    pieceElement.addEventListener('touchstart', startDrag);
                    
                    pieceContainer.appendChild(pieceElement);
                    
                    // Réinitialiser la position actuelle
                    piece.currentPosition = null;
                }});
                
                document.addEventListener('mousemove', onDrag);
                document.addEventListener('touchmove', onDrag);
                document.addEventListener('mouseup', endDrag);
                document.addEventListener('touchend', endDrag);
            }}
            
            function startDrag(e) {{
                e.preventDefault();
                
                // Mettre la pièce en avant-plan
                draggingPiece = this;
                draggingPiece.style.zIndex = '1000';
                
                const rect = draggingPiece.getBoundingClientRect();
                
                if (e.type === 'mousedown') {{
                    startX = e.clientX - rect.left;
                    startY = e.clientY - rect.top;
                }} else if (e.type === 'touchstart') {{
                    startX = e.touches[0].clientX - rect.left;
                    startY = e.touches[0].clientY - rect.top;
                }}
                
                draggingPiece.style.cursor = 'grabbing';
            }}
            
            function onDrag(e) {{
                if (!draggingPiece) return;
                e.preventDefault();
                
                let clientX, clientY;
                
                if (e.type === 'mousemove') {{
                    clientX = e.clientX;
                    clientY = e.clientY;
                }} else if (e.type === 'touchmove') {{
                    clientX = e.touches[0].clientX;
                    clientY = e.touches[0].clientY;
                }}
                
                // Calculer la nouvelle position
                const parentRect = draggingPiece.parentElement.getBoundingClientRect();
                const newLeft = clientX - parentRect.left - startX;
                const newTop = clientY - parentRect.top - startY;
                
                // Mettre à jour la position
                draggingPiece.style.left = newLeft + 'px';
                draggingPiece.style.top = newTop + 'px';
            }}
            
            function endDrag(e) {{
                if (!draggingPiece) return;
                
                let clientX, clientY;
                
                if (e.type === 'mouseup') {{
                    clientX = e.clientX;
                    clientY = e.clientY;
                }} else if (e.type === 'touchend') {{
                    clientX = e.changedTouches[0].clientX;
                    clientY = e.changedTouches[0].clientY;
                }}
                
                // Vérifier si la pièce est placée dans un emplacement du puzzle
                const puzzleBoardRect = puzzleBoard.getBoundingClientRect();
                
                if (
                    clientX >= puzzleBoardRect.left &&
                    clientX <= puzzleBoardRect.right &&
                    clientY >= puzzleBoardRect.top &&
                    clientY <= puzzleBoardRect.bottom
                ) {{
                    // La pièce est sur le tableau de puzzle
                    const pieceRect = draggingPiece.getBoundingClientRect();
                    const pieceId = parseInt(draggingPiece.dataset.id);
                    const piece = pieces.find(p => p.id === pieceId);
                    
                    // Trouver emplacement le plus proche
                    let closestSlot = null;
                    let minDistance = Infinity;
                    
                    const slots = document.querySelectorAll('.puzzle-slot');
                    slots.forEach(slot => {{
                        const slotRect = slot.getBoundingClientRect();
                        const distance = Math.sqrt(
                            Math.pow(pieceRect.left + pieceRect.width/2 - (slotRect.left + slotRect.width/2), 2) +
                            Math.pow(pieceRect.top + pieceRect.height/2 - (slotRect.top + slotRect.height/2), 2)
                        );
                        
                        if (distance < minDistance) {{
                            minDistance = distance;
                            closestSlot = slot;
                        }}
                    }});
                    
                    if (closestSlot && minDistance < {piece_width / 2}) {{
                        // Placer la pièce dans emplacement
                        const position = parseInt(closestSlot.dataset.position);
                        
                        // Vérifier si une pièce est déjà présente à cet emplacement
                        const existingPiece = Array.from(puzzleBoard.querySelectorAll('.puzzle-piece')).find(p => {{
                            const pieceId = parseInt(p.dataset.id);
                            const piece = pieces.find(item => item.id === pieceId);
                            return piece.currentPosition === position;
                        }});
                        
                        // Si une pièce existe déjà à cet emplacement, la déplacer vers la réserve
                        if (existingPiece) {{
                            // Réinitialiser la position actuelle de la pièce existante
                            const existingPieceId = parseInt(existingPiece.dataset.id);
                            const existingPieceData = pieces.find(p => p.id === existingPieceId);
                            existingPieceData.currentPosition = null;
                            
                            // Déplacer visuellement la pièce vers la réserve
                            const reservePosition = getAvailablePositionInReserve();
                            existingPiece.style.left = reservePosition.x + 'px';
                            existingPiece.style.top = reservePosition.y + 'px';
                            existingPiece.classList.remove('correct');
                            
                            // Déplacer la pièce dans le DOM
                            pieceContainer.appendChild(existingPiece);
                        }}
                        
                        // Déplacer la pièce vers emplacement
                        draggingPiece.style.left = closestSlot.style.left;
                        draggingPiece.style.top = closestSlot.style.top;
                        draggingPiece.style.zIndex = '10';
                        
                        // Mettre à jour la position actuelle de la pièce
                        piece.currentPosition = position;
                        
                        // Ajouter la pièce à emplacement
                        puzzleBoard.appendChild(draggingPiece);
                        
                        // Vérifier si la pièce est à la bonne position
                        if (position === piece.originalPosition) {{
                            draggingPiece.classList.add('correct');
                        }} else {{
                            draggingPiece.classList.remove('correct');
                        }}
                        
                        // Vérifier si le puzzle est terminé
                        checkPuzzleCompletion();
                    }}
                }}
                
                draggingPiece.style.cursor = 'grab';
                draggingPiece.style.zIndex = '';
                draggingPiece = null;
            }}
            
            function checkPuzzleCompletion() {{
                const puzzlePieces = puzzleBoard.querySelectorAll('.puzzle-piece');
                let isComplete = true;
                
                if (puzzlePieces.length === {rows * cols}) {{
                    puzzlePieces.forEach(pieceElement => {{
                        const pieceId = parseInt(pieceElement.dataset.id);
                        const piece = pieces.find(p => p.id === pieceId);
                        
                        if (piece.currentPosition !== piece.originalPosition) {{
                            isComplete = false;
                        }}
                    }});
                    
                    if (isComplete) {{
                        winMessage.style.display = 'block';
                        clearInterval(timerInterval);
                    }}
                }}
            }}
            
            function shuffleArray(array) {{
                for (let i = array.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    [array[i], array[j]] = [array[j], array[i]];
                }}
                return array;
            }}
            
            function startTimer() {{
                timerInterval = setInterval(function() {{
                    seconds++;
                    if (seconds === 60) {{
                        minutes++;
                        seconds = 0;
                    }}
                    
                    document.getElementById('seconds').textContent = seconds.toString().padStart(2, '0');
                    document.getElementById('minutes').textContent = minutes.toString().padStart(2, '0');
                }}, 1000);
            }}
            
            // Événements des boutons
            shuffleButton.addEventListener('click', function() {{
                const boardPieces = puzzleBoard.querySelectorAll('.puzzle-piece');
                boardPieces.forEach(piece => {{
                    pieceContainer.appendChild(piece);
                }});
                
                initializePieces();
                winMessage.style.display = 'none';
            }});
            
            resetButton.addEventListener('click', function() {{
                clearInterval(timerInterval);
                seconds = 0;
                minutes = 0;
                document.getElementById('seconds').textContent = '00';
                document.getElementById('minutes').textContent = '00';
                
                const boardPieces = puzzleBoard.querySelectorAll('.puzzle-piece');
                boardPieces.forEach(piece => {{
                    pieceContainer.appendChild(piece);
                }});
                
                initializePieces();
                startTimer();
                winMessage.style.display = 'none';
            }});
            
            showPreviewButton.addEventListener('mousedown', function() {{
                // Créer une div temporaire pour afficher aperçu
                const preview = document.createElement('div');
                preview.style.position = 'fixed';
                preview.style.top = '50%';
                preview.style.left = '50%';
                preview.style.transform = 'translate(-50%, -50%)';
                preview.style.width = '{original_width}px';
                preview.style.height = '{original_height}px';
                preview.style.backgroundImage = `url("data:image/png;base64,{full_image_base64}")`;
                preview.style.backgroundSize = 'cover';
                preview.style.border = '2px solid black';
                preview.style.boxShadow = '0 0 20px rgba(0,0,0,0.5)';
                preview.style.zIndex = '2000';
                
                document.body.appendChild(preview);
                
                showPreviewButton.addEventListener('mouseup', function removePreview() {{
                    document.body.removeChild(preview);
                    showPreviewButton.removeEventListener('mouseup', removePreview);
                }});
            }});
            
            // Définir la langue par défaut au chargement
            changeLanguage('fr');
        }});
    </script>
</body>
</html>
"""
    return html


def main():
    parser = argparse.ArgumentParser(description='Générateur de puzzle HTML5 à partir dune image')
    parser.add_argument('image', help='Chemin vers image à transformer en puzzle')
    parser.add_argument('--rows', type=int, default=3, help='Nombre de lignes du puzzle (défaut: 3)')
    parser.add_argument('--cols', type=int, default=3, help='Nombre de colonnes du puzzle (défaut: 3)')
    parser.add_argument('--output', '-o', default='puzzle.html', help='Fichier HTML de sortie (défaut: puzzle.html)')
    parser.add_argument('--lang', default='fr', choices=['fr', 'nl', 'en'], help='Langue par défaut (défaut: fr)')
    
    args = parser.parse_args()
    
    # Utiliser pathlib pour gérer les chemins
    image_path = Path(args.image)
    output_path = Path(args.output)
    
    # Vérifier que image existe
    if not image_path.is_file():
        print(f"Erreur: Limage '{image_path}' nexiste pas.")
        return 1
    
    # Découper image en pièces
    pieces, piece_width, piece_height, original_width, original_height = split_image(
        str(image_path), args.rows, args.cols
    )
    
    # Générer le HTML
    html = generate_html(
        pieces, piece_width, piece_height, original_width, original_height,
        args.rows, args.cols, str(image_path)
    )
    
    # Écrire le fichier HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Puzzle généré avec succès: {output_path}")
    print(f"Dimensions: {args.rows}x{args.cols} pièces ({args.rows * args.cols} au total)")
    print(f"Taille dune pièce: {piece_width}x{piece_height} pixels")
    print(f"Taille originale: {original_width}x{original_height} pixels")
    
    return 0


if __name__ == "__main__":
    exit(main())