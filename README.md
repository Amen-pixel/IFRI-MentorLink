# 🎓 IFRI MentorLink

<p align="center">
  <strong>Connecter les étudiants. Partager les connaissances. Réussir ensemble.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Socket.IO-Real--time%20Messaging-010101?logo=socketdotio" alt="Socket.IO">
  <img src="https://img.shields.io/badge/Status-In%20Development-orange" alt="Statut">
  <img src="https://img.shields.io/badge/Institution-IFRI%20%7C%20UAC-green" alt="IFRI">
</p>

---

## 📌 1. Présentation du projet

**IFRI MentorLink** est une plateforme web de mise en relation entre mentors et mentorés, conçue pour faciliter l'entraide académique, le partage de compétences et l'accompagnement entre étudiants de l'Institut de Formation et de Recherche en Informatique (IFRI), à l'Université d'Abomey-Calavi (UAC).

Dans un environnement universitaire où les étudiants possèdent des compétences, des expériences et des niveaux de maîtrise différents, il peut être difficile de trouver rapidement une personne capable de les accompagner dans leur progression.

IFRI MentorLink répond à ce besoin en proposant un système intelligent de recommandation qui identifie les mentors les plus adaptés aux besoins des mentorés, en tenant compte des compétences recherchées, de la proximité des filières et des disponibilités horaires.

La plateforme intègre également une messagerie instantanée permettant aux utilisateurs de communiquer plus facilement.

### 🎯 Objectif général

Créer un environnement numérique collaboratif qui favorise la transmission des connaissances, l'entraide entre étudiants et la réussite académique à l'IFRI.

### 🎯 Objectifs spécifiques

- Faciliter la recherche de mentors en fonction des besoins académiques.
- Mettre en relation les étudiants selon leurs compétences et leurs objectifs.
- Valoriser les connaissances et l'expérience des étudiants.
- Favoriser la collaboration entre les différentes filières.
- Simplifier la communication entre mentors et mentorés grâce à la messagerie instantanée.
- Encourager une culture d'entraide et de partage des connaissances au sein de l'IFRI.

---

## ✨ 2. Fonctionnalités principales

### 👤 2.1. Gestion des utilisateurs

La plateforme prévoit un système d'authentification permettant aux étudiants de créer un compte et d'accéder à leur espace personnel.

Fonctionnalités :

- Inscription des étudiants.
- Connexion et déconnexion sécurisées.
- Gestion de session avec Flask-Login.
- Hachage des mots de passe avec Flask-Bcrypt.
- Gestion des informations personnelles.
- Définition du rôle de l'utilisateur : mentor ou mentoré, selon les règles de l'application.

### 📝 2.2. Gestion des profils

Chaque utilisateur dispose d'un profil permettant de présenter son parcours et ses besoins.

Le profil peut notamment contenir :

- Nom et prénom.
- Filière ou spécialité.
- Compétences maîtrisées.
- Compétences à acquérir.
- Objectifs d'apprentissage.
- Disponibilités horaires.
- Présentation personnelle.

Ces informations servent de base au processus de mise en relation.

### 🧠 2.3. Système intelligent de matching

Le système de matching constitue l'une des fonctionnalités centrales d'IFRI MentorLink.

Il analyse les informations du mentoré et les compare aux profils des mentors disponibles afin de proposer les correspondances les plus pertinentes.

Le score de compatibilité est calculé à partir de trois critères :

| Critère | Pondération |
|---|---:|
| Couverture des lacunes du mentoré par les compétences du mentor | 50 % |
| Proximité des filières | 30 % |
| Compatibilité des disponibilités horaires | 20 % |
| **Total** | **100 %** |

Les résultats permettent de classer les mentors selon leur pertinence par rapport aux besoins du mentoré.

### 💬 2.4. Messagerie instantanée

Grâce à Flask-SocketIO, IFRI MentorLink prévoit une communication en temps réel entre les utilisateurs.

Fonctionnalités visées :

- Envoi et réception de messages.
- Communication sans rechargement complet de la page.
- Échanges entre mentors et mentorés.
- Intégration de la messagerie à l'espace utilisateur.

### 📚 2.5. Tableau de bord

Le tableau de bord permet à l'utilisateur de retrouver les principales informations relatives à son activité sur la plateforme.

Il peut notamment regrouper :

- Les informations du profil.
- Les compétences déclarées.
- Les suggestions de mentors.
- Les offres ou propositions d'accompagnement.
- L'accès à la messagerie.

Les fonctionnalités effectivement disponibles dépendent de l'état d'implémentation de l'application.

---

## 🛠️ 3. Stack technique

Le projet repose sur une architecture web utilisant Python côté serveur, MySQL pour la persistance des données et des technologies adaptées à l'authentification et à la communication en temps réel.

| Technologie | Rôle |
|---|---|
| Python | Langage principal du backend |
| Flask | Framework web |
| Flask-SocketIO | Communication en temps réel |
| MySQL | Système de gestion de base de données |
| SQLAlchemy | Mapping objet-relationnel (ORM) |
| PyMySQL | Connecteur Python pour MySQL |
| Flask-Login | Gestion de l'authentification et des sessions |
| Flask-Bcrypt | Hachage des mots de passe |
| Jinja2 | Génération des pages HTML dynamiques |
| HTML5 | Structure des pages |
| CSS3 | Mise en forme et design |
| JavaScript | Interactions côté client |
| Git et GitHub | Gestion de versions et collaboration |

---

## 🏗️ 4. Architecture du projet

L'application est organisée en plusieurs modules afin de séparer les responsabilités et de faciliter la maintenance.

```text
ifri_mentorlink/
│
├── app.py
├── models.py
├── matching.py
├── schema.sql
├── requirements.txt
├── .env.example
├── .gitignore
│
├── routes/
│   ├── auth.py
│   ├── profil.py
│   ├── matching.py
│   └── messages.py
│
├── templates/
│
└── static/
    ├── css/
    ├── js/
    └── images/
```

### Rôle des fichiers et dossiers

- **`app.py`** : point d'entrée de l'application Flask, configuration générale et enregistrement des routes.
- **`models.py`** : définition des modèles de données et des relations entre les entités.
- **`matching.py`** : logique de calcul des scores de compatibilité entre mentors et mentorés.
- **`schema.sql`** : script SQL de création du schéma de base de données.
- **`requirements.txt`** : liste des dépendances Python nécessaires au projet.
- **`.env.example`** : modèle de configuration des variables d'environnement.
- **`.gitignore`** : fichiers et dossiers exclus du suivi Git.
- **`routes/auth.py`** : routes liées à l'inscription, à la connexion et à la déconnexion.
- **`routes/profil.py`** : gestion des profils, des compétences et du tableau de bord.
- **`routes/matching.py`** : accès aux suggestions de mentors et aux offres d'accompagnement.
- **`routes/messages.py`** : gestion des échanges et des événements de messagerie.
- **`templates/`** : pages HTML rendues avec Jinja2.
- **`static/`** : fichiers CSS, JavaScript et ressources graphiques.

---

## 🧮 5. Fonctionnement de l'algorithme de matching

### 5.1. Principe général

L'objectif est de sélectionner les mentors les plus pertinents pour un mentoré donné.

Pour chaque mentor candidat, l'algorithme évalue trois dimensions :

1. La capacité du mentor à couvrir les lacunes du mentoré.
2. La proximité entre leurs filières.
3. La compatibilité de leurs disponibilités.

Chaque critère est converti en un score compris entre 0 et 100, puis pondéré selon son importance.

### 5.2. Formule de calcul

Le score global de compatibilité est défini par :

\[
S = 0{,}50C + 0{,}30F + 0{,}20D
\]

Où :

- \(S\) : score global de compatibilité.
- \(C\) : score de couverture des lacunes.
- \(F\) : score de proximité des filières.
- \(D\) : score de compatibilité des disponibilités.

Le score final est compris entre 0 et 100 si les trois scores individuels respectent cette même échelle.

### 5.3. Exemple illustratif

Considérons un mentor présentant les scores suivants :

| Critère | Score | Poids | Contribution |
|---|---:|---:|---:|
| Couverture des lacunes | 90/100 | 50 % | 45 points |
| Proximité des filières | 80/100 | 30 % | 24 points |
| Disponibilités | 70/100 | 20 % | 14 points |
| **Score final** | | | **83/100** |

Le score de compatibilité obtenu est donc de **83/100**.

### 5.4. Classement des mentors

Le système peut ensuite :

1. Comparer le profil du mentoré aux profils des mentors disponibles.
2. Calculer un score pour chaque candidat.
3. Trier les mentors par ordre décroissant de compatibilité.
4. Présenter les meilleures correspondances au mentoré.

Cette approche permet de privilégier les mentors dont les compétences et les disponibilités correspondent le mieux aux besoins exprimés.

> **Note technique :** les pondérations présentées décrivent la logique fonctionnelle retenue pour le projet. Le calcul exact des scores élémentaires dépend de leur implémentation dans `matching.py`.

---

## 🗄️ 6. Base de données

La base de données MySQL assure le stockage et la gestion des informations de la plateforme.

Le schéma doit notamment prendre en charge les besoins suivants :

- Gestion des comptes utilisateurs.
- Stockage des profils et des filières.
- Enregistrement des compétences maîtrisées et recherchées.
- Gestion des disponibilités.
- Conservation des informations nécessaires aux suggestions de matching.
- Stockage des messages et de leurs métadonnées.

Les tables exactes, leurs clés étrangères et leurs contraintes sont définies dans `schema.sql` et les modèles SQLAlchemy du projet.

---

## 🚀 7. Installation et configuration

### Prérequis

Avant de commencer, assurez-vous de disposer de :

- Python 3.
- Git.
- MySQL Server.
- `pip`, le gestionnaire de paquets Python.

### Étape 1 — Cloner le dépôt

```bash
git clone https://github.com/Amen-pixel/IFRI-MentorLink.git
cd IFRI-MentorLink
```

> Vérifiez que le nom du dossier correspond bien à celui créé par Git. Si le dépôt utilise un autre nom, adaptez la commande `cd`.

### Étape 2 — Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv venv
venv\Scripts\activate
```

Sous Linux ou macOS :

```bash
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 — Installer les dépendances

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Étape 4 — Configurer les variables d'environnement

Sous Linux ou macOS :

```bash
cp .env.example .env
```

Sous PowerShell :

```powershell
Copy-Item .env.example .env
```

Ouvrez ensuite le fichier `.env` et renseignez les valeurs nécessaires, notamment les paramètres de connexion à MySQL et la clé secrète Flask.

Exemple indicatif :

```dotenv
SECRET_KEY=remplacer_par_une_cle_secrete
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ifri_mentorlink
DB_USER=root
DB_PASSWORD=votre_mot_de_passe
```

**Important :** les noms des variables doivent correspondre à ceux réellement utilisés par l'application. Ces noms sont un exemple de configuration, pas une garantie sur le contenu actuel du projet.

Ne publiez jamais votre fichier `.env` ni vos mots de passe sur GitHub.

### Étape 5 — Créer la base de données

Connectez-vous à MySQL :

```bash
mysql -u root -p
```

Puis exécutez :

```sql
CREATE DATABASE ifri_mentorlink
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Quittez MySQL, puis importez le schéma :

```bash
mysql -u root -p ifri_mentorlink < schema.sql
```

Si `schema.sql` crée lui-même la base de données, adaptez cette étape pour éviter de créer deux fois le même objet.

### Étape 6 — Lancer l'application

À la racine du projet :

```bash
python app.py
```

Ouvrez ensuite votre navigateur à l'adresse :

**http://localhost:5000**

Si le port ou l'adresse d'écoute diffère dans votre configuration Flask, utilisez les valeurs effectivement définies dans l'application.

---

## 🔐 8. Sécurité et bonnes pratiques

La sécurité est essentielle pour une plateforme qui manipule des comptes étudiants et des conversations privées.

Les bonnes pratiques à appliquer comprennent :

- Hacher les mots de passe avant leur stockage.
- Utiliser des variables d'environnement pour les secrets.
- Vérifier les données soumises par les formulaires.
- Protéger les routes nécessitant une authentification.
- Contrôler les autorisations d'accès aux profils et aux messages.
- Vérifier l'identité des utilisateurs autorisés à rejoindre les salons Socket.IO.
- Protéger les formulaires contre les attaques CSRF lorsque cela est applicable.
- Éviter d'exposer les messages privés à des utilisateurs non autorisés.
- Utiliser HTTPS en production.
- Ne jamais versionner les secrets ou les fichiers contenant des données sensibles.

Ces éléments constituent des recommandations de sécurité ; leur niveau d'implémentation doit être vérifié dans le code avant de présenter la plateforme comme entièrement sécurisée.

---

## 🧪 9. Tests et validation

Les tests sont indispensables pour vérifier la fiabilité de l'application.

Les principaux scénarios à tester sont :

- Création d'un compte étudiant.
- Connexion avec des identifiants valides et invalides.
- Modification d'un profil.
- Ajout et mise à jour des compétences.
- Calcul correct des scores de matching.
- Classement des mentors selon leur compatibilité.
- Gestion des disponibilités.
- Envoi et réception de messages.
- Contrôle des accès aux routes protégées.
- Gestion des erreurs de connexion à la base de données.

Des tests automatisés avec `pytest` peuvent être ajoutés afin de faciliter la validation des différentes fonctionnalités.

---

## 👥 10. Équipe du projet et répartition des responsabilités

IFRI MentorLink est un projet collaboratif réalisé par une équipe de six membres.

La répartition ci-dessous propose une organisation du travail qui valorise particulièrement la contribution technique d'**Amen QUENUM**, tout en attribuant à chaque membre un domaine de responsabilité.

### 1. Amen QUENUM — Lead Developer & Architecte logiciel

**Responsabilité principale : architecture, backend et intégration globale.**

Missions proposées :

- Définition de l'architecture générale de l'application.
- Mise en place et organisation du backend Flask.
- Conception de la logique générale de l'application.
- Développement et intégration des principales fonctionnalités.
- Conception et implémentation du système de matching.
- Intégration de SQLAlchemy et de la base de données.
- Coordination technique entre les différents modules.
- Révision du code et résolution des problèmes d'intégration.
- Vérification de la cohérence entre les fonctionnalités.
- Participation à la documentation technique et à la préparation de la présentation finale.

### 2. Trésor ELOGBODE — Responsable base de données

Missions proposées :

- Participation à la conception du modèle de données.
- Définition des tables et des relations.
- Contribution au script `schema.sql`.
- Gestion des contraintes et de l'intégrité des données.
- Vérification des relations entre utilisateurs, profils, compétences et messages.
- Tests des opérations de lecture et d'écriture dans MySQL.

### 3. Faris BOHO — Responsable authentification et gestion des comptes

Missions proposées :

- Contribution au module d'inscription et de connexion.
- Intégration de Flask-Login.
- Utilisation de Flask-Bcrypt pour le hachage des mots de passe.
- Gestion des sessions utilisateur.
- Validation des formulaires d'authentification.
- Vérification de l'accès aux routes protégées.

### 4. Prince MIDAHUEN — Responsable profils et interface utilisateur

Missions proposées :

- Contribution aux pages de profil.
- Développement des interfaces avec HTML, CSS et Jinja2.
- Mise en place des formulaires de gestion des compétences.
- Participation au tableau de bord.
- Amélioration de la navigation et de l'expérience utilisateur.
- Vérification de l'affichage des suggestions de mentors.

### 5. Luther — Responsable messagerie temps réel

Missions proposées :

- Contribution au module de messagerie.
- Intégration des événements Flask-SocketIO.
- Gestion des échanges entre utilisateurs.
- Participation à la conception des interfaces de discussion.
- Vérification de la réception et de l'affichage des messages.
- Contribution aux contrôles d'accès aux conversations.

### 6. Aristide — Responsable tests, qualité et documentation

Missions proposées :

- Préparation des scénarios de test.
- Vérification des fonctionnalités principales.
- Tests des cas limites du matching.
- Vérification de la cohérence des résultats.
- Documentation des procédures d'installation et d'utilisation.
- Préparation des exemples de démonstration.
- Contribution à la présentation du projet.

**Remarque :** cette répartition est une proposition d'organisation. Elle doit être adaptée au travail réellement effectué par chacun avant d'être utilisée comme compte rendu officiel des contributions individuelles.

---

## 📈 11. Perspectives d'évolution

Plusieurs améliorations peuvent être envisagées pour enrichir la plateforme :

- Système de notation et d'avis sur les séances de mentorat.
- Historique des accompagnements réalisés.
- Planification des séances.
- Notifications en temps réel.
- Recherche avancée de mentors.
- Tableau de bord statistique.
- Système de signalement et de modération.
- Tests automatisés et intégration continue avec GitHub Actions.
- Déploiement sur un serveur accessible aux étudiants.
- API documentée avec OpenAPI.
- Extension éventuelle à d'autres établissements universitaires.

Ces pistes pourront être priorisées en fonction des besoins des utilisateurs et des ressources disponibles.

---

## 🤝 12. Contribution au projet

Les contributions peuvent être organisées avec Git et GitHub.

Workflow recommandé :

1. Créer une branche pour chaque fonctionnalité.
2. Effectuer les modifications dans cette branche.
3. Tester le code avant de le proposer.
4. Créer une Pull Request.
5. Faire relire les changements.
6. Fusionner les modifications validées dans la branche principale.

Exemple :

```bash
git checkout -b feature/nom-de-la-fonctionnalite
git add .
git commit -m "feat: ajout d'une fonctionnalite"
git push origin feature/nom-de-la-fonctionnalite
```

---

## 📄 13. Licence

Le projet est développé dans un cadre académique à l'IFRI.

La licence de distribution doit être choisie par l'équipe et ajoutée dans un fichier `LICENSE` avant toute redistribution formelle du code.

---

## 🙏 14. Remerciements

Nous remercions l'Institut de Formation et de Recherche en Informatique (IFRI) et l'Université d'Abomey-Calavi (UAC) pour le cadre de formation qui favorise l'apprentissage, la collaboration et la réalisation de projets informatiques.

Nous remercions également toutes les personnes qui contribuent à promouvoir l'entraide académique et le partage de compétences entre étudiants.

---

<p align="center">
  <strong>IFRI MentorLink — Apprendre ensemble, progresser ensemble. 🚀</strong>
</p>

<p align="center">
  Développé avec passion par l'équipe IFRI MentorLink.
</p>
