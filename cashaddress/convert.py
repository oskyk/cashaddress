from cashaddress.crypto import *
from cashaddress.base58 import b58decode_check, b58encode_check
import sys
from functools import partial


class InvalidAddress(Exception):
    pass


class Address(object):
    VERSION_MAP = {
        'legacy': [
            ('P2SH', 5, False),
            ('P2PKH', 0, False),
            ('P2SH-TESTNET', 196, True),
            ('P2PKH-TESTNET', 111, True)
        ],
        'cash': [
            ('P2SH', 8, False),
            ('P2PKH', 0, False),
            ('P2SH-TESTNET', 8, True),
            ('P2PKH-TESTNET', 0, True)
        ]
    }
    VERSION_MAP['slp'] = VERSION_MAP['cash']

    MAINNET_PREFIX = 'bitcoincash'
    TESTNET_PREFIX = 'bchtest'
    SLP_PREFIX = 'simpleledger'

    def __init__(self, version, payload, prefix=None):
        self.version = version
        self.payload = payload
        if prefix:
            self.prefix = prefix
        else:
            if Address._address_type('cash', self.version)[2]:
                self.prefix = self.TESTNET_PREFIX
            else:
                self.prefix = self.MAINNET_PREFIX

    def __str__(self):
        return 'version: {}\npayload: {}\nprefix: {}'.format(self.version, self.payload, self.prefix)


    def _wrapper(self, body):
        return self.prefix + ':' + b32encode(body)


    def __getattr__(self, attr):
        if attr == 'legacy_address':
            version_int = Address._address_type('legacy', self.version)[1]
            return partial(b58encode_check, Address.code_list_to_string([version_int] + self.payload))
        else:
            addr_type = attr.split("_")[0]
            if addr_type not in self.VERSION_MAP:
                raise AttributeError()
            version_int = Address._address_type('cash', self.version)[1]
            payload = [version_int] + self.payload
            payload = convertbits(payload, 8, 5)
            if addr_type == 'slp':
                self.prefix = self.SLP_PREFIX
            checksum = calculate_checksum(self.prefix, payload)
            return partial(self._wrapper, (payload + checksum))


    @staticmethod
    def code_list_to_string(code_list):
        if sys.version_info > (3, 0):
            output = bytes()
            for code in code_list:
                output += bytes([code])
        else:
            output = ''
            for code in code_list:
                output += chr(code)
        return output

    @staticmethod
    def _address_type(address_type, version):
        for mapping in Address.VERSION_MAP[address_type]:
            if mapping[0] == version or mapping[1] == version:
                return mapping
        raise InvalidAddress('Could not determine address version')

    @staticmethod
    def from_string(address_string):
        try:
            address_string = str(address_string)
        except Exception:
            raise InvalidAddress('Expected string as input')
        if ':' not in address_string:
            return Address._legacy_string(address_string)
        else:
            if address_string.startswith(Address.MAINNET_PREFIX) or address_string.startswith(Address.TESTNET_PREFIX):
                return Address._cash_string(address_string, 'cash')
            elif address_string.startswith(Address.SLP_PREFIX):
                return Address._cash_string(address_string, 'slp')
            else:
                raise InvalidAddress('Unexpected Prefix')


    @staticmethod
    def _legacy_string(address_string):
        try:
            decoded = bytearray(b58decode_check(address_string))
        except ValueError:
            raise InvalidAddress('Could not decode legacy address')
        version = Address._address_type('legacy', decoded[0])[0]
        payload = list()
        for letter in decoded[1:]:
            payload.append(letter)
        return Address(version, payload)


    @staticmethod
    def _cash_string(address_string, address_type='cash'):
        if address_string.upper() != address_string and address_string.lower() != address_string:
            raise InvalidAddress('Cash address contains uppercase and lowercase characters')
        address_string = address_string.lower()
        colon_count = address_string.count(':')
        if colon_count == 0:
            address_string = Address.MAINNET_PREFIX + ':' + address_string
        elif colon_count > 1:
            raise InvalidAddress('Cash address contains more than one colon character')
        prefix, base32string = address_string.split(':')
        decoded = b32decode(base32string)
        if not verify_checksum(prefix, decoded):
            raise InvalidAddress('Bad cash address checksum')
        converted = convertbits(decoded, 5, 8)
        version = Address._address_type(address_type, converted[0])[0]
        if prefix == Address.TESTNET_PREFIX:
            version += '-TESTNET'
        payload = converted[1:-6]
        return Address(version, payload, prefix)


def to_cash_address(address):
    return Address.from_string(address).cash_address()


def to_legacy_address(address):
    return Address.from_string(address).legacy_address()


def to_slp_address(address):
    return Address.from_string(address).slp_address()


def is_valid(address):
    try:
        Address.from_string(address)
        return True
    except InvalidAddress:
        return False
