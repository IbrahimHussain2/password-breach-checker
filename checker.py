import hashlib
import getpass
import sys
import requests

def hash_password(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    return sha1

password = getpass.getpass("Enter a password to check: ")

full_hash = hash_password(password)
prefix = full_hash[:5]
suffix = full_hash[5:]

url = f"https://api.pwnedpasswords.com/range/{prefix}"

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
except requests.exceptions.RequestException as error:
    print(f"Error: could not reach the breach database. ({error})")
    sys.exit(1)

lines = response.text.splitlines()

count = 0
for line in lines:
    returned_suffix, times_seen = line.split(":")
    if returned_suffix == suffix:
        count = int(times_seen)
        break

if count > 0:
    print(f"PWNED: this password has appeared {count:,} times in known breach data. Don't use it.")
else:
    print("Not found in any known breaches.")
