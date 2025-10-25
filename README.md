# vCard to ldif converter

![PyPI - Wheel](https://img.shields.io/pypi/wheel/vcf2ldif?logo=pypi)
![PyPI - Version](https://img.shields.io/pypi/v/vcf2ldif?logo=pypi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vcf2ldif?logo=pypi)
![PyPI - License](https://img.shields.io/pypi/l/vcf2ldif?logo=pypi)
![release](https://github.com/Katulos/vcf2ldif/actions/workflows/on_release.yml/badge.svg)
![develop](https://github.com/Katulos/vcf2ldif/actions/workflows/on_develop.yml/badge.svg?branch=develop)
[![codecov](https://codecov.io/gh/Katulos/vcf2ldif/graph/badge.svg?token=XG6VSRHY3B)](https://codecov.io/gh/Katulos/vcf2ldif)

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
* national (e.g.: (e.g.: `(886) 888-6421`) by adding the option `--format-number national`

You can learn more by invoking the command with the `--help` option
```
vcf2ldif --help
```


