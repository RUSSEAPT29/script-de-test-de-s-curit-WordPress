import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import sys
import concurrent.futures
import json
import urllib3
from urllib.parse import urljoin

# Initialisation de Colorama
init(autoreset=True)

# Désactiver les avertissements SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuration des couleurs
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
RESET = Style.RESET_ALL

# Configuration de l'API WPScan (remplacez par votre clé)
WPSCAN_API_KEY = "votre clé API valide"  # Remplacez par votre clé API valide
WPSCAN_API_URL = "https://wpscan.com/api/v3/"

# Fonction pour afficher le menu
def display_menu():
    print(f"{YELLOW}=== Menu Principal ==={RESET}")
    print("1. Vérifier la version de WordPress")
    print("2. Tester les identifiants par défaut")
    print("3. Scanner les plugins vulnérables")
    print("4. Scanner les thèmes vulnérables")
    print("5. Vérifier les fichiers sensibles")
    print("6. Scanner les vulnérabilités via robots.txt")
    print("7. Scanner les vulnérabilités via sitemap.xml")
    print("8. Exporter les résultats")
    print("9. Quitter")
    choice = input(f"{YELLOW}Choisissez une option (1-9) : {RESET}")
    return choice

# Fonction pour vérifier la version de WordPress
def check_wordpress_version(url):
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        version_tag = soup.find('meta', attrs={'name': 'generator'})
        if version_tag and 'WordPress' in version_tag['content']:
            version = version_tag['content'].split(' ')[1]
            print(f"{GREEN}[+] Version de WordPress trouvée : {version}{RESET}")
            latest_version = get_latest_wordpress_version()
            if version < latest_version:
                print(f"{RED}[-] Attention : La version {version} est obsolète. La dernière version est {latest_version}.{RESET}")
            else:
                print(f"{GREEN}[+] La version de WordPress est à jour.{RESET}")
        else:
            print(f"{RED}[-] Aucune version de WordPress trouvée.{RESET}")
    except Exception as e:
        print(f"{RED}[-] Erreur lors de la vérification de la version : {e}{RESET}")

# Fonction pour obtenir la dernière version de WordPress
def get_latest_wordpress_version():
    try:
        response = requests.get("https://api.wordpress.org/core/version-check/1.7/", verify=False)
        data = response.json()
        return data['offers'][0]['version']
    except Exception as e:
        print(f"{RED}[-] Erreur lors de la récupération de la dernière version de WordPress : {e}{RESET}")
        return "6.0"  # Version par défaut si l'API échoue

# Fonction pour tester un identifiant
def test_login(url, username, password):
    login_url = urljoin(url, "/wp-login.php")
    try:
        session = requests.Session()
        login_data = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': urljoin(url, "/wp-admin/"),
            'testcookie': '1'
        }
        response = session.post(login_url, data=login_data, verify=False)
        if 'wp-admin' in response.url:
            return True, username, password
        else:
            return False, username, password
    except Exception as e:
        print(f"{RED}[-] Erreur lors de la tentative de connexion : {e}{RESET}")
        return False, username, password

# Fonction pour tester les identifiants par défaut avec multithreading
def check_default_logins(url):
    default_credentials = [
        ('admin', 'admin'),
        ('admin', 'password'),
        ('admin', '123456'),
        ('admin', 'qwerty'),
        ('admin', 'letmein')
    ]
    print(f"{YELLOW}[*] Test des identifiants par défaut...{RESET}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(test_login, url, user, pwd) for user, pwd in default_credentials]
        for future in concurrent.futures.as_completed(futures):
            success, user, pwd = future.result()
            if success:
                print(f"{GREEN}[+] Connexion réussie avec : {user}/{pwd}{RESET}")
            else:
                print(f"{RED}[-] Échec de la connexion avec : {user}/{pwd}{RESET}")

# Fonction pour scanner les plugins vulnérables
def scan_vulnerable_plugins(url):
    try:
        print(f"{YELLOW}[*] Recherche des plugins vulnérables...{RESET}")
        headers = {'Authorization': f'Token token={WPSCAN_API_KEY}'}
        response = requests.get(f"{WPSCAN_API_URL}plugins", headers=headers, verify=False)
        if response.status_code == 200:
            plugins = response.json().get('items', [])
            for plugin in plugins:
                print(f"{YELLOW}- {plugin['slug']} : {plugin['latest_version']} (Vulnérabilités : {len(plugin['vulnerabilities'])}){RESET}")
        elif response.status_code == 403:
            print(f"{RED}[-] Accès refusé. Vérifiez votre clé API ou passez à un compte premium.{RESET}")
        else:
            print(f"{RED}[-] Erreur lors de la récupération des plugins vulnérables : {response.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Erreur lors du scan des plugins : {e}{RESET}")

# Fonction pour scanner les thèmes vulnérables
def scan_vulnerable_themes(url):
    try:
        print(f"{YELLOW}[*] Recherche des thèmes vulnérables...{RESET}")
        headers = {'Authorization': f'Token token={WPSCAN_API_KEY}'}
        response = requests.get(f"{WPSCAN_API_URL}themes", headers=headers, verify=False)
        if response.status_code == 200:
            themes = response.json().get('items', [])
            for theme in themes:
                print(f"{YELLOW}- {theme['slug']} : {theme['latest_version']} (Vulnérabilités : {len(theme['vulnerabilities'])}){RESET}")
        elif response.status_code == 403:
            print(f"{RED}[-] Accès refusé. Vérifiez votre clé API ou passez à un compte premium.{RESET}")
        else:
            print(f"{RED}[-] Erreur lors de la récupération des thèmes vulnérables : {response.status_code}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Erreur lors du scan des thèmes : {e}{RESET}")

# Fonction pour vérifier les fichiers sensibles
def check_sensitive_files(url):
    sensitive_files = [
        "wp-config.php",
        "wp-admin/admin-ajax.php",
        "wp-login.php",
        "readme.html"
    ]
    print(f"{YELLOW}[*] Vérification des fichiers sensibles...{RESET}")
    for file in sensitive_files:
        try:
            response = requests.get(urljoin(url, file), verify=False)
            if response.status_code == 200:
                print(f"{RED}[-] Fichier accessible : {file}{RESET}")
            else:
                print(f"{GREEN}[+] Fichier non accessible : {file}{RESET}")
        except Exception as e:
            print(f"{RED}[-] Erreur lors de la vérification du fichier {file} : {e}{RESET}")

# Fonction pour scanner les vulnérabilités via robots.txt
def scan_robots_txt(url):
    try:
        robots_url = urljoin(url, "/robots.txt")
        response = requests.get(robots_url, verify=False)
        if response.status_code == 200:
            print(f"{YELLOW}[*] Contenu de robots.txt :{RESET}")
            print(response.text)
        else:
            print(f"{RED}[-] robots.txt n'est pas accessible.{RESET}")
    except Exception as e:
        print(f"{RED}[-] Erreur lors de la lecture de robots.txt : {e}{RESET}")

# Fonction pour scanner les vulnérabilités via sitemap.xml
def scan_sitemap(url):
    try:
        sitemap_url = urljoin(url, "/sitemap.xml")
        response = requests.get(sitemap_url, verify=False)
        if response.status_code == 200:
            print(f"{YELLOW}[*] Contenu de sitemap.xml :{RESET}")
            print(response.text)
        else:
            print(f"{RED}[-] sitemap.xml n'est pas accessible.{RESET}")
    except Exception as e:
        print(f"{RED}[-] Erreur lors de la lecture de sitemap.xml : {e}{RESET}")

# Fonction pour exporter les résultats
def export_results(results, filename="results.json"):
    with open(filename, "w") as file:
        json.dump(results, file, indent=4)
    print(f"{GREEN}[+] Résultats exportés dans {filename}{RESET}")

# Fonction principale
def main():
    url = input(f"{YELLOW}Entrez l'URL du site WordPress : {RESET}")
    if not url.startswith(('http://', 'https://')):
        print(f"{RED}[-] L'URL doit commencer par http:// ou https://.{RESET}")
        sys.exit()
    if not url.endswith('/'):
        url += '/'

    results = {}
    while True:
        choice = display_menu()
        if choice == "1":
            check_wordpress_version(url)
        elif choice == "2":
            check_default_logins(url)
        elif choice == "3":
            scan_vulnerable_plugins(url)
        elif choice == "4":
            scan_vulnerable_themes(url)
        elif choice == "5":
            check_sensitive_files(url)
        elif choice == "6":
            scan_robots_txt(url)
        elif choice == "7":
            scan_sitemap(url)
        elif choice == "8":
            export_results(results)
        elif choice == "9":
            print(f"{YELLOW}[*] Fermeture du programme...{RESET}")
            sys.exit()
        else:
            print(f"{RED}[-] Option invalide. Veuillez réessayer.{RESET}")

if __name__ == "__main__":
    main()
