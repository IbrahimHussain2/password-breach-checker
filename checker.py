import hashlib
import getpass
import sys
import requests

API_URL = "https://api.pwnedpasswords.com/range/"


def hash_password(password):
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


def get_suffixes(prefix):
    # only the first 5 chars of the hash get sent, never the full thing
    response = requests.get(API_URL + prefix, timeout=5)
    response.raise_for_status()
    return response.text.splitlines()


def check_password(password):
    full_hash = hash_password(password)
    prefix = full_hash[:5]
    suffix = full_hash[5:]

    # compare locally - the API never knows which one we wanted
    for line in get_suffixes(prefix):
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)

    return 0


def main():
    password = getpass.getpass("Enter a password to check: ")

    try:
        count = check_password(password)
    except requests.exceptions.RequestException as e:
        print(f"Error: couldn't reach the breach database ({e})")
        sys.exit(1)

    if count > 0:
        print(f"PWNED: seen {count:,} times in breach data. Don't use this password.")
    else:
        print("Not found in any known breaches.")


if __name__ == "__main__":
    main()
