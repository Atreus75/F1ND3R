from requests import get
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser 
from colorama import init, Fore

# Initializes colorama and argument parser
init(autoreset=True)
parser = ArgumentParser(usage='finder.py [-h] -u URL -w WORDLIST -t THREADS', exit_on_error=True)


# Presentation
print(f'{Fore.CYAN}[+]{Fore.WHITE}  F1ND3R  {Fore.CYAN}[+]{Fore.WHITE}\n'.center(20))



class Finder:
    def __init__(self):
        # Define default arguments
        parser.add_argument('-u', '--url', help = 'Target url', required=True)
        parser.add_argument('-w', '--wordlist', help = 'The wordlist to be used during the enumeration', required=True)
        parser.add_argument('-t', '--threads', help = 'Number of threads to perform the enumeration. Default: 10', required=False, default=10)
        parser.add_argument('-fc', '--filterCode', help = 'Response code to treat as unwanted ex: -fc 404', required=False, default=404)
        args = parser.parse_args()
        
        # Check if the wordlist exists
        try:
            args.wordlist = open(f'{args.wordlist}', 'r', encoding='utf-8').readlines()
        except:
            parser.error(f'{Fore.RED}[+]{Fore.WHITE} Wordlist not found. Check the path to it.')
            
         # Check if the url was correctly writed
        if 'http://' not in args.url and 'https://' not in args.url:
            args.url = f'http://{args.url}'
        if args.url[-1] != '/':
            args.url = f'{args.url}/'
        
        try:
            get(args.url)
        except:
            parser.error(f'{Fore.RED}[+]{Fore.WHITE} Cannot to URL')
        self.url, self.wordlist, self.threads, self.filter_code = args.url, args.wordlist, int(args.threads), int(args.filterCode)
    
    
    def directory_enumeration(self, wordlist):
        url = self.url
        wordlist = wordlist.strip()
        # Enumeration 
        req = get(f'{url}{wordlist}')
        finded_msg = f'{Fore.GREEN}    --> {url}{wordlist:<20} | Code {req.status_code}{Fore.WHITE}'
        print(finded_msg, end='\n') if req.status_code != self.filter_code else print('...', end='\r')
        


    def start_attack(self):
        print(f'\n{Fore.CYAN}[+]{Fore.WHITE} Starting Directory Enumeration:\n Enumerating...')
        wordlist, threads = self.wordlist, self.threads
        with ThreadPoolExecutor(max_workers=threads) as pool:
            pool.map(self.directory_enumeration, wordlist)
        
            


finder = Finder()

try:
    finder.start_attack()
except KeyboardInterrupt:
    print(f'{Fore.RED}[+]{Fore.WHITE} Press {Fore.RED}CTRL+C{Fore.WHITE} again to exit.')
    exit()

print(f'{Fore.CYAN}[+]{Fore.WHITE}Successful enumeration')