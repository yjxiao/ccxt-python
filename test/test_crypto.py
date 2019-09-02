import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

# ----------------------------------------------------------------------------

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

# ----------------------------------------------------------------------------

import ccxt  # noqa: F402

Exchange = ccxt.Exchange
hash = Exchange.hash
ecdsa = Exchange.ecdsa
jwt = Exchange.jwt
encode = Exchange.encode


def equals(a, b):
    return a == b


exchange = Exchange()

# ---------------------------------------------------------------------------------------------------------------------

assert(hash(encode(''), 'sha256', 'hex') == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
assert(hash(encode('cheese'), 'sha256', 'hex') == '873ac9ffea4dd04fa719e8920cd6938f0c23cd678af330939cff53c3d2855f34')

assert(hash(encode(''), 'md5', 'hex') == 'd41d8cd98f00b204e9800998ecf8427e')
assert(hash(encode('sexyfish'), 'md5', 'hex') == 'c8a35464aa9d5683585786f44d5889f8')

assert(hash(encode(''), 'sha1', 'hex') == 'da39a3ee5e6b4b0d3255bfef95601890afd80709')
assert(hash(encode('nutella'), 'sha1', 'hex') == 'b3d60a34b744159793c483b067c56d8affc5111a')

# ---------------------------------------------------------------------------------------------------------------------

privateKey = '1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a'

assert(equals(ecdsa('1a', privateKey, 'p256', 'sha256'), {
    'r': '3f4537ef9e72240cdefaea19d68fd483b5e10227e89747c58a3b543bfaf9cc46',
    's': '278d65adebd8d52dac34820c02cee0a0e3348f9aee91a21b8e9bfa0a23b40001',
    'v': 1
}))


assert(equals(ecdsa(privateKey, privateKey, 'p256', None), {
    'r': '9aadbfe7feca28a8b665731abd8fdd19f8b1be5fcdd1264d111b291a01c8dea2',
    's': '5084765e08e169fbba470ed1f573c9fed8d68a9d883049054b601f66a6648912',
    'v': 0,
}))

assert(equals(ecdsa('1a', privateKey, 'secp256k1', 'sha256'), {
    'r': '23dcb2a2a3728a35eb1a35cc01743c4609550d9cceaf2083550f13a9eb135f9f',
    's': '317963fcac18e4ec9f7921b97d7ea0c82a873dd6299cbfb6af016e08ef5ed667',
    'v': 0,
}))


assert(equals(ecdsa(privateKey, privateKey, 'secp256k1', None), {
    'r': 'b84a36a6fbabd5277ede578448b93d48e70b38efb5b15b1d4e2a298accf938b1',
    's': '66ebfb8221cda925526e699a59cd221bb4cc84bdc563024b1802c4d9e1d8bbe9',
    'v': 1,
}))

# ---------------------------------------------------------------------------------------------------------------------

assert(exchange.hashMessage(privateKey) == '0x59ea5d98c3500c3729f95cf98aa91663f498518cc401360df2912742c232207f')

assert(equals(exchange.signHash('0x59ea5d98c3500c3729f95cf98aa91663f498518cc401360df2912742c232207f', privateKey), {
    'r': '0x6f684aa41c02da83dac3039d8805ddbe79a03b1297e247c7742cab8dfc19d341',
    's': '0x62473881674550563cb028ff40a7846fd53620ddf40a20cc1003b8484a109a4a',
    'v': 27
}))

assert(equals(exchange.signMessage(privateKey, privateKey), {
    'r': '0x6f684aa41c02da83dac3039d8805ddbe79a03b1297e247c7742cab8dfc19d341',
    's': '0x62473881674550563cb028ff40a7846fd53620ddf40a20cc1003b8484a109a4a',
    'v': 27
}))

# ---------------------------------------------------------------------------------------------------------------------

pemKeyArray = [
    '-----BEGIN RSA PRIVATE KEY-----',
    'MIIEpAIBAAKCAQEAqUtXQXv2uSm9zPvdJTRpu5/65rBjAoHmIiowAs+u7fY0QP9O',
    '+T8CZRQjvZrfPomBiccjCxDo8mm7GkmL67rs9s7VOMQFvpTTtMBeglNSEbXJ3wTt',
    '7WM5gD3ZAbhfGtwWdGpcOMX0hV5/d/fiw1zQk0+AooayTryZ7HV+DQcD1sGTYYir',
    'LePUGkKV2NCvKtGOQfRAtuo0ccigMxMvEhWuExCc9Fhd077OpXMc0n7OiFqA2JWN',
    'jlocM9S71Srvw/lDos8a7lGaFUV8gP1CsQY/4qTju6hhsRd4lFujVr5J9FqmDbnv',
    'wQ79SSu6+lT0+ToFdDHiYOorBK2ESFR7EzlyLwIDAQABAoIBAEobQMbZjNbg/sSM',
    'O/HdT6tiDGKPM8gVNLgf34RbhSeFbrpFCDzy6Al3F24YLUEi0CGPmjdt34q93blU',
    'GHvIB5LCV3PR2vHiFAo7ayOBdZtrCEMn1T7lAHaynBu0qW0IiovLQzNW9AKtqv7I',
    '8+qw5lyVoKmEbOkqhfaMN/Fb8MJAo3yEVyhyp4EjtFhqDQ9DuHEjp1jGthnMgm+4',
    'qFyELf0DXZSAN+R9IGDqWPyo78lOcPW4pgeLuoLQ6Nn/2JAEGHFt1a7zMEw5yYbR',
    'XB89Bh0dheSmopBN6Heay4YuhnNKua37OlL1/nhKpLGUNE3z/UOXeiUiMeE1C2i+',
    'GjK+xgECgYEA4XH63rJ3VYDHHWUGlWffFWkEpgR4BDEkZ8MyVYQoUjQA2TpCvQ2+',
    'bR7aAIGXhBnRTrIBNu9m4+am0aUfi1hVmVHqt1b2vFgEb9uKuO4U62tCFpeji+Rz',
    '8C8QJyu5v5OUWdQZ4EA0d7ljeoTl50g8tpcGsDhnImLt+/jvJuFt8dECgYEAwD0n',
    'rhlkEjKVHxu1xwKeczxYCqqcUV9Quq8HnPh4VJQ77ljfZ57V7sAKrFDi5XfVD9jS',
    'oJPwxjw6za134VobhdvCM6WNs6AJmbR8E/b5kDMbGaZn27vt+/8JfnGaWBqpDi6W',
    'a5xoJOqmcMBQBK1YleZDoY4PLbk+onVKLMfGI/8CgYEAkyUIv8euGdGWpHnm5SdJ',
    'tLi5vv4Vs267uzntJWG/y3+DukTLgIdy7dgAI+pxkVgkg/+syUVSW5eU9CqZPyLl',
    'o8+Sqh2Jp36vTq71iSRj5RA5r3ND3K+8eFzPZzGj6AWUA1lrljFxzV7kLfiF8gH1',
    'FpvWUrhNoGT/vcFJno/uabECgYAecRC5hxfLserfVDoC261PvjyK492BHUDhbxob',
    'h1U2v4qGAdjOxd5Gwm5uPxjPEZzRt5oTB5pXKe5953xWWTiGh/hGyW6ZBTy/9E65',
    'sqBub0lZVHqZ1zamcwqD1WWFkiM3NbVoMQpk3iuhKzMAqpqekiofiSlqKi16+GvY',
    'j4IW7QKBgQCrIUckPZ6IY3ERIN1IL4TIcK2gOJcznp7fLWpC+sv35ya3OhtDXKFt',
    'GjIHmwLuiUNc0iPzA9Rw89W0zIkKWmWcxM88/ithdxh3MEeNDUGSnd4hQ9SECwxB',
    'Wem3eBT7I4VtFYoaTE3/bX1SKfgBdTzIRqWKSDpgBNZg/P2Tc+s11g==',
    '-----END RSA PRIVATE KEY-----',
]

pemKey = "\n".join(pemKeyArray)

assert(jwt({'chicken': 'salad'}, encode(pemKey), 'RS256') == 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjaGlja2VuIjoic2FsYWQifQ.FSKD5Y6RNzkHTuHdvG3753U7QNZ-u-GUSPfP1FMjEaK0Rr_iyQTSSmHhkdYSFFnmBvrrN_l-UwKwir52WlsgmQm9HYm0kidxbj7fWwrK2E1oe0P7OjupFjv1BZxc5W69WeaHtOPWe28tiHiON1LCnax6HgfI5lcIBsESGIIBZMVeaioQn9gDVwea7JxJvAlrhDIWZowIHTIdCQocXip7g5jREWHeEIuJNug67mwnfAFxCjvTRiTd0Bw6oBwjM3FLya-RyEyWrejQOWSuC8CNWVUHISaSmEyZ7uM6wTi2m_58TaE9mQwlef32OPErPvvBpgL5pZIyQ4ymwrCIFQLBQQ')
assert(jwt({'lil': 'xan'}, encode('betrayed'), 'HS256') == 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsaWwiOiJ4YW4ifQ.md-oFvZagA-NXmZoRNyJOQ7zwK-PWUMmMQ_LI9ZOKaM')
