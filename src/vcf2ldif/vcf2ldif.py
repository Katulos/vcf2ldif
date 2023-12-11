"""vcf2ldif"""
from __future__ import annotations

import re
import uuid

import click
import phonenumbers
import vobject


def get_cn(vcard: vobject.vCard) -> str:
    """Returns the common name of the vCard"""
    return vcard.fn.value


def get_given_name(vcard: vobject.vCard) -> str:
    """Returns the given name of the vCard"""
    return vcard.n.value.given


def get_phone(vcard: vobject.vCard, phone_type: str) -> str | None:
    """Returns the mobile number of the vCard"""
    phone_type = phone_type.lower()
    for tel in vcard.contents["tel"]:
        if tel.type_param.lower() == phone_type:
            return tel.value
    return None


def get_org(vcard: vobject.vCard) -> str:
    """Returns the organization name of the vCard"""
    if hasattr(vcard, "org"):
        org = re.split(":|\n", vcard.org.serialize().strip())
        return org[1]
    return None


def get_sn(vcard: vobject.vCard) -> str:
    """Returns the family name of the vCard"""
    if vcard.n.value.family:
        sn_str = vcard.n.value.family
    else:
        sn_str = vcard.n.value
    return sn_str


@click.command()
@click.option(
    "--input-file",
    "-i",
    help="local vCard file",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--root-dn",
    "-r",
    help="root DN of the address book in the OpenLDAP server",
    required=True,
)
@click.option("--output-file", "-o", help="output ldif file")
@click.option(
    "--format-number",
    "-f",
    type=click.Choice(["e164", "international", "national"]),
    help="format phone number e164/international/national",
)
def main(
    input_file: str,
    root_dn: str,
    output_file: str = None,
    format_number: str = None,
):
    """
    vCard to ldif converter

    This tool is designed to convert *.vcf (vCard) contact files to *.ldif
    file, for further creation of shared phone books on LDAP server.

    You can import the resulting ldif file into your LDAP server
    (e.g. OpenLDAP) with the following command:

    ldapmodify -c -D "cn=admin,dc=example,dc=com" -W -f output_file.ldif
    """
    ldif_map = []
    format_mapping = {
        "e164": phonenumbers.PhoneNumberFormat.E164,
        "international": phonenumbers.PhoneNumberFormat.INTERNATIONAL,
        "national": phonenumbers.PhoneNumberFormat.NATIONAL,
    }
    with open(input_file, encoding="utf-8") as source_file:
        for vcard in vobject.readComponents(source_file, validate=True):
            if not hasattr(vcard, "uid"):
                vcard.add("uid")
                vcard.uid.value = str(uuid.uuid4())
            if format_number:
                phone_home = phonenumbers.format_number(
                    phonenumbers.parse(get_phone(vcard, phone_type="home")),
                    format_mapping.get(format_number, None),
                )
                phone_mobile = phonenumbers.format_number(
                    phonenumbers.parse(get_phone(vcard, phone_type="cell")),
                    format_mapping.get(format_number, None),
                )
            else:
                phone_home = get_phone(vcard, phone_type="home")
                phone_mobile = get_phone(vcard, phone_type="cell")

            org = get_org(vcard)

            ldif_map.append(
                {
                    "dn": "cn=" + get_cn(vcard) + "," + root_dn,
                    "changetype": "add",
                    "objectClass": "inetOrgPerson",
                    "cn": get_cn(vcard),
                    "givenName": get_given_name(vcard),
                    **({"telephoneNumber": phone_home} if phone_home else {}),
                    **({"mobile": phone_mobile} if phone_mobile else {}),
                    **({"o": org} if org else {}),
                    "sn": get_sn(vcard),
                    "uid": vcard.uid.value,
                }
            )
    if output_file:
        with open(output_file, "w", encoding="utf-8") as target_file:
            for ldif in ldif_map:
                for key, value in ldif.items():
                    click.echo(f"{key}: {value}", file=target_file)
                click.echo(file=target_file)  # new line
    else:
        for ldif in ldif_map:
            for key, value in ldif.items():
                click.echo(f"{key}: {value}")
            click.echo()  # new line
