[![TastyRoad CI/CD](https://github.com/Pipatchies/tastyroad_api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Pipatchies/tastyroad_api/actions/workflows/ci-cd.yml)

# 🍕 TastyRoad API — Application de Randos Gourmandes 🌳

**TastyRoad API** est le backend REST et **GeoJSON** de l'application **TastyRoad**, permettant de créer, explorer et partager des itinéraires de randonnées et roadtrips gastronomiques à travers les régions françaises.

## 🌐 API Déployée en Production (Render)

- **URL de base de l'API** : [https://tastyroad-api.onrender.com/api/](https://tastyroad-api.onrender.com/api/)
- **Documentation Swagger UI (Live)** : [https://tastyroad-api.onrender.com/api/schema/swagger-ui/](https://tastyroad-api.onrender.com/api/schema/swagger-ui/)
- **Documentation ReDoc (Live)** : [https://tastyroad-api.onrender.com/api/schema/redoc/](https://tastyroad-api.onrender.com/api/schema/redoc/)
- **Administration Django** : [https://tastyroad-api.onrender.com/admin/](https://tastyroad-api.onrender.com/admin/)

---

## 🛠️ Stack Technique

| Brique | Technologie |
| :--- | :--- |
| **Langage & Framework** | Python 3.15 / Django 6.1 / Django REST Framework (DRF) |
| **Données Géospatiales (SIG)** | PostgreSQL 18 + **PostGIS 3.6** / GeoDjango / `djangorestframework-gis` (GeoJSON) |
| **Authentification & Sécurité** | JWT (`djangorestframework-simplejwt`), Permissions DRF, CORS, Throttling |
| **Documentation API** | OpenAPI 3 / Swagger UI & ReDoc (`drf-spectacular`) |
| **Qualité & Tests** | `pytest`, `pytest-django`, `pytest-cov`, `Faker`, `Ruff`, `pip-audit` |
| **Conteneurisation & Déploiement** | Docker (Multi-stage), Docker Compose, Nginx, Gunicorn, WhiteNoise, Render (CI/CD GitHub Actions) |

---

## 📂 Architecture du Projet

Le projet est découpé par domaines métiers (*Bounded Contexts*) :

```text
tastyroad_api/
├── config/          # Configuration globale Django (settings, urls, wsgi/asgi)
├── core/            # Briques transverses et permissions partagées (IsAuthorOrAdminOrReadOnly)
├── users/           # Authentification JWT, inscription, profil utilisateur & droit à l'oubli (RGPD)
├── places/          # Lieux gastronomiques (FoodPlace : producteurs, marchés, restaurants - Point PostGIS)
├── itineraries/     # Itinéraires (LineString PostGIS), étapes (Step), avis (Comment), favoris & vue SQL brute
├── nginx/           # Configuration du reverse-proxy Nginx (développement local)
├── Dockerfile       # Image Docker multi-stage (builder, development, production non-root)
└── entrypoint.sh    # Script d'initialisation (attente PostGIS, migrations, collectstatic)
```

---

## 🚀 Installation & Démarrage rapide (Docker)

### 1. Cloner le dépôt
```bash
git clone https://github.com/Pipatchies/tastyroad_api.git
cd tastyroad_api
```

### 2. Configurer les variables d'environnement
Créer un fichier `.env` à la racine du projet :

```env
DJANGO_SECRET_KEY=votre_cle_secrete_locale
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1

POSTGRES_DB=tastyroad_db
POSTGRES_USER=admin_tastyroad
POSTGRES_PASSWORD=votre_mot_de_passe_postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

APP_PORT=8000
```

### 3. Lancer les conteneurs (PostGIS + API + Nginx)
```bash
docker compose up --build -d
```
*(Les migrations et la collecte des fichiers statiques s'exécutent automatiquement au démarrage via `entrypoint.sh`).*

### 4. Peupler la base de données avec des données de démonstration (`seed`)
Une commande personnalisée génère 5 utilisateurs, 10 lieux gastronomiques (`FoodPlace`) et 15 itinéraires complets en France (avec tracés GPS `LineString`, étapes gourmandes/touristiques, avis et favoris) :

```bash
docker compose exec api python manage.py seed
```

### 5. Créer un compte administrateur (Superuser)
```bash
docker compose exec api python manage.py createsuperuser
```

---

## 📡 Principaux Endpoints de l'API

### 📖 Documentation Interactive (Local & Production)
- **Swagger UI** : `http://localhost:8000/api/schema/swagger-ui/` | [Production](https://tastyroad-api.onrender.com/api/schema/swagger-ui/)
- **ReDoc** : `http://localhost:8000/api/schema/redoc/` | [Production](https://tastyroad-api.onrender.com/api/schema/redoc/)
- **Schéma OpenAPI** : `http://localhost:8000/api/schema/` | [Production](https://tastyroad-api.onrender.com/api/schema/)
- **Back-office Django Admin (avec cartes PostGIS)** : `http://localhost:8000/admin/` | [Production](https://tastyroad-api.onrender.com/admin/)

### 🔐 Authentification & Utilisateurs (`users`)
| Méthode | Endpoint | Accès | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/users/register/` | Public | Inscription d'un nouvel utilisateur |
| `POST` | `/api/token/` | Public | Connexion — renvoie la paire JWT (`access` + `refresh`) |
| `POST` | `/api/token/refresh/` | Public | Rafraîchissement du token `access` |
| `GET / PATCH` | `/api/users/me/` | Authentifié | Consultation et modification du profil connecté |
| `DELETE` | `/api/users/me/` | Authentifié | **Droit à l'oubli (RGPD)** — Suppression du compte et des traces GPS en cascade |

### 🗺️ Itinéraires, Étapes, Avis & Favoris (`itineraries`)
| Méthode | Endpoint | Accès | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/itineraries/` | Public | Liste des itinéraires au format **GeoJSON** (`FeatureCollection`) |
| `POST` | `/api/itineraries/` | Authentifié | Création d'un itinéraire (tracé `LineString` PostGIS) |
| `GET` | `/api/itineraries/{id}/` | Public | Détail d'un itinéraire (inclut `steps` et `comments`) |
| `PUT / PATCH / DELETE` | `/api/itineraries/{id}/` | Auteur ou Admin | Modification ou suppression d'un itinéraire |
| `GET` | `/api/raw/itineraries/?limit=5` | Public | **Vue SQL brute & DTO** — Top des itinéraires les mieux notés (`average_rating`, `steps_count`) |
| `GET / POST` | `/api/steps/` | Lecture publique / Écriture auth | Étapes d'un itinéraire (`Point` PostGIS) |
| `GET / POST` | `/api/comments/` | Lecture publique / Écriture auth | Avis et notes (1 à 5 ⭐) sur les itinéraires |
| `GET / POST / DELETE` | `/api/favorites/` | Authentifié | Favoris personnels de l'utilisateur connecté |

### 🧀 Lieux Gastronomiques (`places`)
| Méthode | Endpoint | Accès | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/foodplaces/` | Public | Liste des commerces/producteurs au format **GeoJSON** (`Point`) |
| `POST` | `/api/foodplaces/` | Authentifié | Ajout d'un lieu gastronomique |

---

## 🧪 Tests, Qualité de Code & CI/CD

### Lancer la suite de tests (Pytest + Coverage)
```bash
docker compose exec api pytest
```

### Vérifier le linter et le formatage (Ruff)
```bash
docker compose exec api ruff check .
docker compose exec api ruff format --check .
```

### Pipeline CI/CD (GitHub Actions)
Le workflow [`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml) automatise :
1. **CI (sur chaque Pull Request vers `main`)** :
   - Audit des vulnérabilités des dépendances (`pip-audit`).
   - Analyse statique et vérification du formatage (`ruff check` & `ruff format`).
   - Exécution des tests unitaires et d'intégration sur un service conteneurisé **PostGIS**.
2. **CD (lors d'un merge/push sur `main`)** :
   - Déclenchement automatique du déploiement en production sur **Render** via Deploy Hook.

---

## 🔒 Sécurité & Conformité RGPD

- **Mots de passe** : Hachage robuste via `PBKDF2` et validateurs natifs de Django.
- **Contrôle d'accès** : Lecture publique (`IsAuthenticatedOrReadOnly`), écriture protégée par JWT, et permission objet [`IsAuthorOrAdminOrReadOnly`](core/permissions.py) empêchant la modification/suppression des ressources d'autrui.
- **Protection contre les injections SQL** : Utilisation de l'ORM Django et de requêtes préparées paramétrées (`cursor.execute(query, [limit])`) sur la vue SQL brute [`raw_views.py`](itineraries/raw_views.py).
- **Rate Limiting (Throttling)** : Limitation à `10 req/min` pour les visiteurs anonymes et `1000 req/jour` pour les utilisateurs authentifiés.
- **Droit à l'oubli (RGPD)** : L'endpoint `DELETE /api/users/me/` supprime définitivement le compte ainsi que l'ensemble de ses traces GPS et contributions associées.
