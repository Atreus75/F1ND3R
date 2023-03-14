from requests import Session, get
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser 
from colorama import init, Fore
from time import time

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
        self.cache, self.session = [], Session()
    
    
    # This function checks if the current path has not been repeated, so the program shouldn't repeat the request and can do a faster enumeration
    def was_not_repeated(self, path):
        if path not in self.cache:
            self.cache.append(path)
            return True
        else:
            return False
        
    
    # That function performs the requests as quickly as possible.
    def enumeration(self, path):  
        url, path = self.url, path.strip()
        if self.was_not_repeated(path):
            # Enumeration 
            req = self.session.get(f'{url}{path}', allow_redirects=True, timeout=1, headers={'user-agent': 'headers="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'})
            finded_msg = f'{Fore.GREEN}    --> {url}{path:<20} | Code {req.status_code}{Fore.WHITE}'
            print(finded_msg, end='\n') if req.status_code != self.filter_code else print('..', end='\r')
        else:
            pass
    

    # This function makes use of a Thread pool to separate the wordlist for each thread, so that the program can run more efficiently.
    # This also shutdown the threads if the user presses CTRL+C
    def start_attack(self):
        print(f'\n{Fore.CYAN}[+]{Fore.WHITE} Starting Directory Enumeration:\n Enumerating...')
        wordlist, threads = self.wordlist, self.threads
        try:
            with ThreadPoolExecutor(max_workers=threads) as pool: 
                pool.map(self.enumeration, wordlist)
        except KeyboardInterrupt:
            print(f'{Fore.RED}[+]{Fore.WHITE} Keyboard Interrupt. Shutting down all threads...')
            pool.shutdown(cancel_futures=True)
            print('Bye bye.. :)')
            exit()


finder = Finder()
start_time = time()
finder.start_attack()
end_time = time()
print(f'{Fore.CYAN}[+]{Fore.WHITE}Successful enumeration in {end_time - start_time:.2f}')