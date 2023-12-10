from __future__ import annotations

import os

from vcf2ldif.vcf2ldif import main


def get_vcard():
    script_path = os.path.abspath(__file__)

    script_directory = os.path.dirname(script_path)
    vcf_file = os.path.join(script_directory, "test_input.vcf")

    with open(vcf_file, encoding="utf-8") as source_file:
        text = source_file.read()
    return text


def test_main_with_output_file(cli_runner):
    # Set up test data
    input_file = "test_input.vcf"
    root_dn = "ou=addressbook,dc=mydomain,dc=com"
    output_file = "test_output.ldif"

    # Create a test input vCard file
    with open(input_file, "w") as f:
        f.write(get_vcard())
        result = cli_runner.invoke(
            main,
            [
                "--input-file",
                input_file,
                "--root-dn",
                root_dn,
                "--output-file",
                output_file,
            ],
        )
        assert result.exit_code == 0
        assert os.path.exists(output_file)

        os.remove(input_file)
        os.remove(output_file)


def test_main_without_output_file(cli_runner):
    # Set up test data
    input_file = "test_input.vcf"
    root_dn = "ou=addressbook,dc=mydomain,dc=com"

    # Create a test input vCard file
    with open(input_file, "w") as f:
        f.write(get_vcard())

    result = cli_runner.invoke(
        main, ["--input-file", input_file, "--root-dn", root_dn]
    )

    assert "dn: cn=John Doe,ou=addressbook,dc=mydomain,dc=com" in result.output
    assert "changetype: add" in result.output
    assert "objectClass: inetOrgPerson" in result.output
    assert "cn: John Doe" in result.output
    assert "givenName: John" in result.output
    assert "telephoneNumber: +1(6010)640-4100" in result.output
    assert "mobile: +1(235)223-4573" in result.output
    assert "o: Example.com Inc." in result.output
    assert "sn: Doe" in result.output
    assert "\n" in result.output

    os.remove(input_file)
