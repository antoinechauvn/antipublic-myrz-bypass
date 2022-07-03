import winreg
import hashlib
import requests
import colorama
import secrets
import argparse

colorama.init()
cookies = {'login': 'nppr22',
           'user_hash': 'a7ebc0faad8eb7c9dda59b2272226c1f',
           'PHPSESSID': 'kn2pc9s2m17k19o8r7fhbkpio5'}
parser = argparse.ArgumentParser(description='Antipublic.One Tool by Armanta#6184')
parser.add_argument("-g", "--generate", help="Generates a 16 bytes hexadecimal key", action='store_true')
parser.add_argument("-d", "--count", help="Get database size", action='store_true')
parser.add_argument("-c", "--check", help="Check an email address or a key", action='store_true')
parser.add_argument("-k", "--key", help="Check a key", type=str)
parser.add_argument("-e", "--email", help="Check an email", type=str)
args = parser.parse_args()


def key_generate():
    random_key = secrets.token_hex(16)
    print(f"{colorama.Fore.LIGHTYELLOW_EX}[~]Activating {random_key}")
    key_activation(random_key)


def key_default():
    regedit = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    regedit_key = winreg.OpenKey(regedit, "SOFTWARE\Microsoft\Cryptography")
    computer_guid = winreg.QueryValueEx(regedit_key, "MachineGuid")[0]
    data = computer_guid.encode("utf-16-le")
    default_key = hashlib.md5(
        data).hexdigest()  # https://docs.python.org/fr/3/library/hashlib.html#hashlib.hash.hexdigest
    print(f"{colorama.Fore.LIGHTYELLOW_EX}[~]Activating {default_key}")
    key_activation(default_key)


def key_check(key):
    req = requests.get(f'http://antipublic.one/api/check.php?key={key}')
    data = req.json()
    print(data)


def key_activation(key):
    req = requests.post('https://antipublic.one/main/account.php', data={'your_key': key}, cookies=cookies)
    data = req.json()
    if data["success"]:
        print(f"{colorama.Fore.LIGHTGREEN_EX}[+]{key}")
    else:
        print(f"{colorama.Fore.LIGHTRED_EX}[-]Error, key {key} has expired")


def mail_check(email, key):
    req = requests.get(f'https://antipublic.one/api/email_search.php?key={key}&email={email}')
    data = req.json()
    if data["success"]:
        for combo in data["results"]:
            print(f"{colorama.Fore.LIGHTMAGENTA_EX}[+]{combo['line']}")
    else:
        print(f"{colorama.Fore.LIGHTRED_EX}[-]No matching email address")

def count():
    req = requests.get('https://antipublic.one/api/count_lines.php')
    db_size = req.text
    print(f"{colorama.Fore.LIGHTCYAN_EX}[#]{db_size} lines")


if args.generate:
    key_generate()
elif args.check:
    if args.email and args.key:
        mail_check(args.email, args.key)
    else:
        print(f"{colorama.Fore.LIGHTRED_EX}Missing arguments (key, email)")
elif args.count:
    count()
else:
    key_default()
