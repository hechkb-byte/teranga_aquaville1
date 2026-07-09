# Teranga Aquaville

## Présentation du projet

**Teranga Aquaville** est un site web vitrine développé pour une résidence immobilière de standing située à Saly, au Sénégal. Le projet répond à un besoin réel du client : disposer d'une plateforme professionnelle pour présenter ses villas, attirer des acheteurs et des locataires, et centraliser la gestion des demandes commerciales.

### Contexte

Teranga Aquaville est un complexe résidentiel proposant des villas haut de gamme à la vente et à la location, accompagnées d'un parc aquatique, d'un spa (Peri'Care) et d'une offre de restauration. Le site a pour objectif de remplacer une communication dispersée (réseaux sociaux, bouche-à-oreille) par une présence web structurée et crédible, à la hauteur du positionnement premium du projet.

### Ce que fait l'application

**Côté visiteur (site public) :**
- Présentation du complexe avec hero visuel et galerie photo
- Catalogue des villas disponibles à la vente et à la location, avec photos, superficie, capacité, équipements et tarifs détaillés (dont les appels de fonds pour la vente)
- Pages dédiées aux services : parc aquatique avec tarifs visiteur/résident, spa Peri'Care avec soins et forfaits, restauration, services inclus
- Formulaire de contact avec sélection du type de bien et tranche de budget
- Design responsive, adapté mobile et desktop

**Côté administration (back-office) :**
- Interface d'administration personnalisée accessible à l'adresse `/gestion-teranga/`
- Gestion complète des villas : ajout, modification, galerie photos, archivage
- Gestion des tarifs de vente (avec appels de fonds échelonnés) et des tarifs de location
- Gestion des services : tarifs du parc aquatique, soins et forfaits spa
- Suivi des demandes de contact : statut (en attente / traité), notes internes, archivage
- Gestion des comptes administrateurs

### Stack technique

| Composant | Technologie |
|-----------|-------------|
| Back-end | Python 3.13 · Django 6 |
| Base de données | MySQL |
| Front-end | HTML · SCSS (django-sass-processor) · JavaScript vanilla |
| Administration | Django Admin personnalisé |
| Environnement | python-dotenv · django-environ |

---

## Guide d'installation et d'utilisation

Ce guide explique comment installer et lancer le site sur ton ordinateur Windows, pas à pas.

---

## Ce dont tu as besoin avant de commencer

Installe ces 3 logiciels dans l'ordre :

### 1. Python 3.13
- Va sur [python.org/downloads](https://www.python.org/downloads/)
- Télécharge la version **3.13**
- Lance l'installeur et **coche impérativement** la case **"Add Python to PATH"** avant de cliquer sur Install

### 2. MySQL
- Va sur [dev.mysql.com/downloads/installer/](https://dev.mysql.com/downloads/installer/)
- Télécharge **MySQL Installer for Windows**
- Lors de l'installation, choisis **"Developer Default"**
- Retiens bien le **mot de passe root** que tu définis — tu en auras besoin

### 3. Git (optionnel si tu as reçu le projet en zip)
- Va sur [git-scm.com](https://git-scm.com/) et installe Git

---

## Étape 1 — Récupérer le projet

**Option A — Si tu as un fichier ZIP :**
1. Extrais le dossier où tu veux (ex : `Bureau/teranga_aquaville`)

**Option B — Si tu as un lien Git :**
Ouvre le **Command Prompt** (touche Windows → tape "cmd" → Entrée) et tape :
```
git clone <lien-du-projet>
cd teranga_aquaville
```

---

## Étape 2 — Ouvrir le terminal dans le bon dossier

1. Ouvre le dossier du projet dans l'explorateur Windows
2. Clique dans la barre d'adresse en haut
3. Tape **`cmd`** et appuie sur Entrée
4. Un terminal noir s'ouvre déjà positionné dans le bon dossier

---

## Étape 3 — Créer l'environnement virtuel

Dans le terminal, tape ces commandes **une par une** (appuie sur Entrée après chaque ligne) :

```
python -m venv venv
venv\Scripts\activate
```

> Tu dois voir `(venv)` apparaître au début de la ligne — c'est bon signe.

---

## Étape 4 — Installer les dépendances

```
pip install -r requirements.txt
```

> Attends que tout se télécharge (peut prendre 2-3 minutes).

---

## Étape 5 — Créer la base de données MySQL

1. Ouvre **MySQL Workbench** (installé avec MySQL)
2. Connecte-toi avec ton mot de passe root
3. En haut, clique sur l'icône **"Create new schema"** (cylindre avec un +)
4. Nom du schéma : **`teranga_aquaville`**
5. Clique sur **Apply** puis **Apply** à nouveau

---

## Étape 6 — Configurer le fichier `.env`

Dans le dossier du projet, tu verras un fichier nommé `.env`.
Ouvre-le avec le Bloc-notes et adapte ces lignes selon ta configuration MySQL :

```
SECRET_KEY=une-cle-secrete-longue-et-complexe
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=teranga_aquaville
DB_USER=root
DB_PASSWORD=TON_MOT_DE_PASSE_MYSQL
DB_HOST=127.0.0.1
DB_PORT=3306

ADMIN_URL=gestion-teranga/

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@teranga-aquaville.sn
```

> Remplace uniquement `TON_MOT_DE_PASSE_MYSQL` par ton vrai mot de passe MySQL.

---

## Étape 7 — Initialiser la base de données

Dans le terminal (avec `(venv)` actif) :

```
python manage.py migrate
```

> Tu verras défiler des lignes "Applying …OK" — c'est normal.

---

## Étape 8 — Créer un compte administrateur

```
python manage.py createsuperuser
```

Le terminal va te demander :
- **Username** : choisis un identifiant (ex : `admin`)
- **Email** : ton email (ou laisse vide)
- **Password** : un mot de passe (tu ne le verras pas s'afficher, c'est normal)
- **Password (again)** : retape le même mot de passe

---

## Étape 9 — Lancer le site

```
python manage.py runserver
```

Ouvre ton navigateur et va sur :

| Page | Adresse |
|------|---------|
| **Site principal** | http://127.0.0.1:8000 |
| **Administration** | http://127.0.0.1:8000/gestion-teranga/ |

---

## Utiliser l'administration

1. Va sur http://127.0.0.1:8000/gestion-teranga/
2. Connecte-toi avec le compte créé à l'étape 8
3. Dans le panneau gauche tu peux gérer :
   - **Villas** : ajouter, modifier, archiver des villas
   - **Tarifs vente / location** : gérer les prix
   - **Services** : parc aquatique, spa, services inclus
   - **Demandes contact** : voir et traiter les demandes clients
   - **Utilisateurs** : gérer les comptes admin

---

## Commandes utiles à retenir

| Action | Commande |
|--------|----------|
| Activer l'environnement | `venv\Scripts\activate` |
| Lancer le serveur | `python manage.py runserver` |
| Arrêter le serveur | `Ctrl + C` dans le terminal |
| Créer un admin | `python manage.py createsuperuser` |
| Mettre à jour la BDD | `python manage.py migrate` |

---

## En cas de problème

**Erreur "python n'est pas reconnu"**
→ Python n'est pas dans le PATH. Réinstalle Python en cochant "Add Python to PATH".

**Erreur de connexion à la base de données**
→ Vérifie que MySQL est démarré (cherche "Services" dans Windows → MySQL doit être "En cours d'exécution").
→ Vérifie le mot de passe dans le fichier `.env`.

**Erreur "No module named ..."**
→ L'environnement virtuel n'est pas actif. Tape `venv\Scripts\activate` et réessaie.

**Page blanche ou erreur 500**
→ Regarde le terminal — l'erreur y est affichée en rouge.

---

*Développé par Baye Modou Gestu · Teranga Aquaville 2026*
