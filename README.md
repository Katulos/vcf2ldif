# vCard to ldif converter


This tool is designed to convert `*.vcf` (vCard) contact files to `*.ldif` file, for further creation of shared phone books on `LDAP` server.

## Installation
`pip install vcf2ldif`

## Usage
```
vcf2ldif \
    --input-file path/to/input_file.vcf \
    --root-dn ou=adressbook,dc=example,dc=com \
    --output-file path/to/output_file.ldif
```
You can import the resulting ldif file into your LDAP server (e.g. OpenLDAP) with the following command:
```
 ldapmodify -c -D "cn=admin,dc=example,dc=com" -W -f path/to/output_file.ldif
```
When converting, you can also format phone numbers according to the following standards:

* e164 (e.g.: `+18868886421`) by adding the option `--format-number e164`
* international (e.g.: `+1 886-888-6421`) by adding the option `--format-number international`
* national (e.g.: (e.g.: `(886) 888-6421`) by adding the option `--format-number rnational`

You can learn more by invoking the command with the `--help` option
```
vcf2ldif --help
```


