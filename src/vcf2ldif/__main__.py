from __future__ import annotations

import sys

from colorama import Fore, Style, just_fix_windows_console

just_fix_windows_console()


def print_help():
    print("Usage: " + Fore.GREEN + "vcf2ldif " + Fore.YELLOW + "[options]")
    print(
        Fore.WHITE
        + "Example:"
        + Fore.YELLOW
        + " vcf2ldif "
        + Fore.YELLOW
        + "--file="
        + Fore.WHITE
        + "contacts.vcf "
        + Fore.YELLOW
        + "--root="
        + Fore.WHITE
        + '"ou=user,ou=adressbook-personal,dc=example,dc=com" > '
        + Fore.YELLOW
        + "contacts.ldif"
    )
    print(
        Fore.GREEN
        + "--file="
        + Fore.YELLOW
        + "contacts.vcf"
        + Fore.WHITE
        + " local vCard file"
    )
    print(
        Fore.GREEN
        + "--root"
        + Fore.WHITE
        + " root DN of the address book in the OpenLDAP server"
    )
    print(Fore.GREEN + "--help" + Fore.WHITE + " this help message")

    print(Style.RESET_ALL)


def main():
    print_help()


if __name__ == "__main__":
    sys.exit(main())
