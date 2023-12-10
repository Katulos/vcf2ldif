from __future__ import annotations

import pytest
import vobject

from vcf2ldif import vcf2ldif


def test_get_cn():
    """Testing get_cn function"""
    # Test case 1: vCard with common name "John Doe"
    vcard1 = vobject.vCard()
    vcard1.add("fn").value = "John Doe"
    assert vcf2ldif.get_cn(vcard1) == "John Doe"

    # Test case 2: vCard with common name "Jane Smith"
    vcard2 = vobject.vCard()
    vcard2.add("fn").value = "Jane Smith"
    assert vcf2ldif.get_cn(vcard2) == "Jane Smith"

    # Test case 3: vCard with common name "Foo Bar"
    vcard3 = vobject.vCard()
    vcard3.add("fn").value = "Foo Bar"
    assert vcf2ldif.get_cn(vcard3) == "Foo Bar"


def test_get_given_name():
    # Test case 1: vCard with given name "John"
    vcard1 = vobject.vCard()
    vcard1.add("n")
    vcard1.n.value.given = "John"
    assert vcf2ldif.get_given_name(vcard1) == "John"

    # Test case 2: vCard with given name "Jane"
    vcard2 = vobject.vCard()
    vcard2.add("n")
    vcard2.n.value.given = "Jane"
    assert vcf2ldif.get_given_name(vcard2) == "Jane"

    # Test case 3: vCard with empty given name
    vcard3 = vobject.vCard()
    vcard3.add("n")
    assert vcf2ldif.get_given_name(vcard3) == ""

    # Test case 4: vCard without 'n' attribute
    vcard4 = vobject.vCard()
    with pytest.raises(Exception) as attre:
        vcf2ldif.get_given_name(vcard4)
    assert attre.type == AttributeError
    assert str(attre.value) == "n"


def test_get_phone(capsys):
    # Test case 1: vCard with a single mobile number
    vcard1 = vobject.vCard()
    tel1 = vcard1.add("tel")
    tel1.type_param = "CELL"
    tel1.value = "1234567890"
    assert vcf2ldif.get_phone(vcard1, tel1.type_param) == "1234567890"

    # Test case 2: vCard with multiple telephone numbers but no mobile number
    vcard2 = vobject.vCard()
    tel2_1 = vcard2.add("tel")
    tel2_1.type_param = "HOME"
    tel2_1.value = "1111111111"
    tel2_2 = vcard2.add("tel")
    tel2_2.type_param = "WORK"
    tel2_2.value = "2222222222"
    assert vcf2ldif.get_phone(vcard2, tel2_1.type_param) == "1111111111"

    # Test case 3: vCard with multiple telephone
    # numbers including a mobile number
    vcard3 = vobject.vCard()
    tel3_1 = vcard3.add("tel")
    tel3_1.type_param = "HOME"
    tel3_1.value = "1111111111"
    tel3_2 = vcard3.add("tel")
    tel3_2.type_param = "CELL"
    tel3_2.value = "3333333333"
    tel3_3 = vcard3.add("tel")
    tel3_3.type_param = "WORK"
    tel3_3.value = "2222222222"
    assert vcf2ldif.get_phone(vcard3, tel3_2.type_param) == "3333333333"

    # Test case 4: vCard with no telephone numbers
    vcard4 = vobject.vCard()
    vcard4.type_param = "CELL"
    with pytest.raises(Exception) as attre:
        vcf2ldif.get_phone(vcard4, vcard4.type_param)
    assert attre.type == KeyError
    assert str(attre.value) == "'tel'"


def test_get_org_with_org_attribute():
    # Test when vCard has org attribute
    vcard = vobject.vCard()
    vcard.add("fn").value = "John Doe"
    vcard.add("org").value = ["Organization"]
    assert vcf2ldif.get_org(vcard) == "Organization"


def test_get_org_without_org_attribute():
    # Test when vCard does not have org attribute
    vcard = vobject.vCard()
    assert vcf2ldif.get_org(vcard) != ""


def test_get_org_with_multiple_org_values():
    # Test when vCard has multiple org values
    vcard = vobject.vCard()
    vcard.add("org").value = ["Organization", "Company"]
    assert vcf2ldif.get_org(vcard) == "Organization;Company"


def test_family_name():
    vcard = vobject.vCard()
    vcard.add("fn").value = "John Smith"
    vcard.add("n").value = vobject.vcard.Name(family="Smith", given="John")
    assert vcf2ldif.get_sn(vcard) == "Smith"


def test_no_family_name():
    vcard = vobject.vCard()
    vcard.add("n").value = "John"
    # assert vcf2ldif.get_sn(vcard) == "John"
    with pytest.raises(Exception) as attre:
        vcf2ldif.get_sn(vcard)
    assert attre.type == AttributeError
    assert str(attre.value) == "'str' object has no attribute 'family'"
