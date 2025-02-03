import requests
from colorama import Fore, init, Style
import argparse

init(autoreset=True)

banner = f'''{Fore.YELLOW}
__        ______        _ ____   ___  _   _ 
\ \      / /  _ \      | / ___| / _ \| \ | |
 \ \ /\ / /| |_) |  _  | \___ \| | | |  \| |
  \ V  V / |  __/  | |_| |___) | |_| | |\  |
   \_/\_/  |_|      \___/|____/ \___/|_| \_|
                                            
            {Fore.CYAN}github.com/foxzinnx                              
                                            '''

print(banner)

def main_menu():
    print(banner)

def format_url(site):
    if not site.startswith(("http://", "https://")):
        return "http://" + site
    return site


def check_wp_json_endpoint(site):
    site = format_url(site)
    url = f"{site.rstrip('/')}/wp-json/wp/v2/users"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:

        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            print(f'{Fore.YELLOW}{site} -> {Fore.GREEN}Endpoint found! ({site}/wp-json/wp/v2/users)')

        elif response.status_code == 403:
            print(f'{Fore.YELLOW}{site} -> {Fore.RED}Access denied (403)')

        elif response.status_code == 404:
            print(f'{Fore.YELLOW}{site} -> {Fore.RED}Endpoint not found (404)')
        
        else:
            print(f'{Fore.YELLOW}{site} -> Returned status code {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'{Fore.RED}Failed to access {site}')

def main():
    parser =argparse.ArgumentParser(description='Scans WordPress sites for exposure of the /wp-json/wp/v2/users endpoint.')
    parser.add_argument("-w", "--wordlist", required=True, help="Wordlist path")

    args = parser.parse_args()

    try:
        with open(args.wordlist, "r") as file:
            sites = file.readlines()
        
        for site in sites:
            check_wp_json_endpoint(site.strip())
    
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Error: The file '{args.wordlist}' was not found")

if __name__ == "__main__":
    main()