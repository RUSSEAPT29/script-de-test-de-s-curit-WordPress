Voici un fichier bien structuré pour votre script de test de sécurité WordPress. Ce fichier explique l'objectif du script, les fonctionnalités disponibles, les prérequis, ainsi que les instructions d'utilisation.README.md

Scanner de sécurité WordPress
Un outil Python avancé pour tester la sécurité des sites WordPress. Ce script permet de détecter les vulnérabilités courantes, telles que les versions obsolètes, les identifiants par défaut, les plugins et thèmes vulnérables, et bien plus encore.

Table des matières
Introduction
Fonctionnalités
Prérequis
Installation
Utilisation
Exemples
Contributeur
Avertissements
Licence
Introduction
Ce script est conçu pour aider les administrateurs de sites WordPress à identifier les vulnérabilités potentielles dans leur installation. Il utilise une combinaison de techniques automatiques (comme l'API WPScan) et manuelles pour fournir un rapport détaillé sur la sécurité du site.

Fonctionnalités
Vérification de la version de WordPress : Détectez la version actuelle de WordPress et vérifiez si elle est à jour.
Test des identifiants par défaut : Tente de se connecter avec des identifiants par défaut tels que .admin/admin
Scan des plugins vulnérables : Utilisez l'API WPScan pour lister les plugins installés et vérifier leurs vulnérabilités.
Scan des thèmes vulnérables : Identifier les thèmes sécurisés et vérifier s'ils contiennent des vulnérabilités connues.
Vérification des fichiers sensibles : Recherche des fichiers critiques accessibles publiquement (par exemple, ).wp-config.php
Analyse derobots.txt : Affiche le contenu de pour détecter des répertoires ou fichiers sensibles.robots.txt
Analyse desitemap.xml : Vérifie le fichier pour identifier les pages exposées.sitemap.xml
Exportation des résultats : Enregistrez les résultats du scan dans un fichier JSON pour une analyse ultérieure.
Prérequis
Avant d'utiliser ce script, assurez-vous d'avoir les éléments suivants :

Python 3 installé sur votre système.
Les modules Python nécessaires :
requests
beautifulsoup4
colorama
urllib3
Installez-les en exécutant la commande suivante :
frapper
Photocopieuse
1
pip install requests beautifulsoup4 colorama urllib3
Une clé API valide de WPScan pour accéder aux fonctionnalités premium (plugins/thèmes vulnérables). Obtenez-en une sur WPScan .
Installation
Clonez ce dépôt ou téléchargez le script directement.
Installer les dépendances en exécutant :
frapper
Photocopieuse
1
pip install -r requirements.txt
Remplacez dans le script par votre clé API WPScan."YOUR_WPSCAN_API_KEY"
Utilisation
Lancez le script en utilisant Python :
frapper
Photocopieuse
1
python wordpress_scanner.py
Entrez l'URL du site WordPress que vous souhaitez analyser.
Utilisez le menu interactif pour choisir les options suivantes :
Option 1 : Vérifier la version de WordPress.
Option 2 : Tester les identifiants par défaut.
Option 3 : Scanner les plugins vulnérables.
Option 4 : Scanner les thèmes vulnérables.
Option 5 : Vérifier les fichiers sensibles.
Option 6 : Scanner les vulnérabilités via .robots.txt
Option 7 : Scanner les vulnérabilités via .sitemap.xml
Option 8 : Exporter les résultats dans un fichier JSON.
Option 9 : Quitter le programme.
Exemples
Exemple 1 : Vérifier la version de WordPress
texte en clair
Photocopieuse
1
2
3
4
Entrez l'URL du site WordPress : https://example.com
Choisissez une option (1-9) : 1
[+] Version de WordPress trouvée : 5.9
[-] Attention : La version 5.9 est obsolète. La dernière version est 6.2.
Exemple 2 : Scanner les plugins vulnérables
texte en clair
Photocopieuse
1
2
3
4
Choisissez une option (1-9) : 3
[*] Recherche des plugins vulnérables...
- akismet : 4.1.7 (Vulnérabilités : 3)
- contact-form-7 : 5.5.2 (Vulnérabilités : 1)
Contributeur
Si vous souhaitez contribuer à ce projet, suivez ces étapes :

Clonez le dépôt.
Créez une branche pour vos modifications ( ).git checkout -b feature/nouvelle-fonctionnalité
Soumettez vos modifications via une pull request.
Avertissements
Éthique d'utilisation : Ce script doit être utilisé uniquement avec l'autorisation explicite du propriétaire du site cible. Toute utilisation abusive est strictement interdite.
Limitation de responsabilité : L'auteur de ce script n'est pas responsable des dommages causés par son utilisation incorrecte.
Licence
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.

Contact
Pour toute question ou suggestion, contactez-moi à l'adresse suivante : GoupeAPT29@tomorjerry.com .

Ce script est un outil puissant pour améliorer la sécurité de vos installations WordPress. Bonne analyse ! 🚀
