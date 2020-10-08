
# cashaddress
`cashaddress` is python library which is able to convert legacy BCH address to new format.

# Installation
To install this library and its dependencies use:

    pip install cashaddress-regtest
    
# Usage examples
The first thing you need to do is import the library via:

```python
from cashaddress-regtest import convert
```
## Converting address
**It does not matter if you use legacy or new address as input.**

Then you can convert your address via:

```python
address = convert.to_cash_address('155fzsEBHy9Ri2bMQ8uuuR3tv1YzcDywd4')
```

or

```python
address = convert.to_legacy_address('bitcoincash:qqkv9wr69ry2p9l53lxp635va4h86wv435995w8p2h')
```

In the case that you are using "regtest" mode on a local node, you should also pass the following parameter:

```python
address = convert.to_cash_addres('2MwSNRexxm3uhAKF696xq3ztdiqgMj36rJo', regtest=True)
```

which is necessary since testnet and regtest legacy address formats are identical, and the library cannot differentiate them.

## Validating address
You can also validate address via:

```python
convert.is_valid('155fzsEBHy9Ri2bMQ8uuuR3tv1YzcDywd4')
```

or

```python
convert.is_valid('bitcoincash:qqkv9wr69ry2p9l53lxp635va4h86wv435995w8p2h')
```

# Development

1. Clone the repository
2. Create virtualenv
4. Do your thing
5. Run tests


    pytest
