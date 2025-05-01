# Documentation du Projet CuveLabo Client

## Présentation

Ce projet est une solution logicielle destinée à contrôler à distance deux laboratoires didactiques de régulation de niveau :

- **Tortank** : le laboratoire à trois cuves.
- **Carapuce** : le laboratoire à une cuve.

Le projet a été réalisé de **début février à début mai 2025** par un **stagiaire de la HEH, département technique, option bachelier en électronique**.

⚠️ **Sécurité importante** :  
**Il est strictement interdit d'ouvrir la boîte du laboratoire "Tortank" ou "Carapuce" lorsqu'ils sont branchés au secteur.**

Pour toute question, vous pouvez me contacter à l'adresse suivante : [trioen.loic@gmail.com](mailto:trioen.loic@gmail.com).

---

## Installation & Utilisation

### Prérequis

- **Python 3.11 ou supérieur** (idéalement 3.13)

### Installation

1. Ouvrir le dossier dans un terminal de commande
2. Executer `pip install .`, le projet devrait télécharger toutes les librairies nécessaire.

### Exemple d'utilisation

Voici un exemple simple montrant comment utiliser la classe `Tortank`.

```python
from Tortank.Tortank import Tortank, PIDController2Tanks
import time

# Initialisation du système
tortank = Tortank()

# Création du contrôleur PID
control = PIDController2Tanks(
        Kp1 = 1,
        Ki1 = 0.1,
        Kd1 = 0.01,
        Kp2 = 1,
        Ki2 = 0.1,
        Kd2 = 0.01,
        dt = 1,
        Qmin = 0.0,
        Qmax = 1.0
)

# Fonction de mise à jour appelée en boucle par le système
@tortank.UpdateFunc()
def update():
    # Lecture des niveaux d’eau
    waterLevels = tortank.GetWaterLevels()

    # Calcul des vitesses des moteurs via le régulateur PID
    motorspeeds = control.update(
        h1_k=waterLevels[0],
        h2_k=waterLevels[2],
        h1_setpoint=0.5,
        h2_setpoint=0.75
    )

    # Application des vitesses calculées
    tortank.SetMotorsSpeed(motorspeeds)

    time.sleep(1)

# Démarrage de la boucle de régulation
tortank.Run("Tortank Test")
```

Voici un exemple simple montrant comment utiliser la classe `Carapuce`.
```python
from Carapuce.Carapuce import Carapuce
import time

carapuce : Carapuce = Carapuce()

@carapuce.UpdateFunc()
def funcTest():
    waterLevel = carapuce.GetWaterLevel()

    if(waterLevel < 0.18):
        carapuce.SetMotorSpeed(1)
    else:
        carapuce.SetMotorSpeed(0.82 - ( waterLevel - 0.18) * 15 / 0.82)

    if(waterLevel > 0.6):
        # Stop et quitte la boucle
        carapuce.Stop()


carapuce.Run("Carapuce Test") 

```

---

## Arborescence des dossiers

Contient tous les fichiers sources nécessaires au fonctionnement du projet :

- `src/Carapuce/Carapuce.py`  
  Script principal de gestion du laboratoire à une cuve ("Carapuce").

- `src/Tortank/Tortank.py`  
  Script principal de gestion du laboratoire à trois cuves ("Tortank").

- `src/Common/CuveLaboClient.py`  
  Bibliothèque cliente à utiliser pour controller le coté client.

- `src/Common/CuveLaboAPI.py`  
  Contient les constantes et fonctions utilitaires pour l’API pour interagir avec le serveur web.

- `pyproject.toml`  
  Fichier de configuration du projet Python.

---

## Bonnes pratiques

- Ne jamais exécuter les scripts si le laboratoire n’est pas correctement alimenté ou branché.
- Toujours vérifier la communication avec les capteurs avant de démarrer des tests automatiques.
- Ne pas modifier le serveur sans validation préalable : il gère des accès concurrents via une file d’attente.

---

## Notes supplémentaires

- Le projet utilise une architecture modulaire.
- L’interface client est conçue pour être réutilisée dans d’autres projets.
- Des fichiers d'exemples peuvent être ajoutés dans un futur `_Examples`.

