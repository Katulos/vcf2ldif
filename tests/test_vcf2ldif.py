from __future__ import annotations

import os
import unittest

import pytest
from click.testing import CliRunner

from vcf2ldif.__main__ import main


class TestMain(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_main_with_output_file(self):
        input_file = "test_input.vcf"
        root_dn = "dc=mydomain,dc=com"
        output_file = "test_output.ldif"

        # Create a test input vCard file
        with open(input_file, "w") as f:
            f.write(
                """BEGIN:VCARD
                VERSION:2.1
                FN:John Doe
                N:Doe;John
                TEL;CELL:1234567890
                ORG:Company
                END:VCARD"""
            )

        result = self.runner.invoke(
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

        self.assertEqual(result.exit_code, 0)

        # Check if the output file was created
        self.assertTrue(os.path.exists(output_file))

        # Clean up test files
        os.remove(input_file)
        os.remove(output_file)

    @pytest.mark.filterwarnings("ignore::DeprecationWarning")
    def test_main_without_output_file(self):
        input_file = "test_input.vcf"
        root_dn = "dc=mydomain,dc=com"

        # Create a test input vCard file
        with open(input_file, "w") as f:
            f.write(
                """BEGIN:VCARD
                VERSION:2.1
                FN:John Doe
                N:Doe;John
                TEL;CELL:1234567890
                ORG:Company
                END:VCARD"""
            )

        result = self.runner.invoke(
            main, ["--input-file", input_file, "--root-dn", root_dn]
        )

        self.assertEqual(result.exit_code, 0)

        # Clean up test files
        os.remove(input_file)


if __name__ == "__main__":
    unittest.main()
