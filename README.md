# Sha256 Python

SHA256 python3 implementation for Cryptography and Information security subject at University.
Doesn't require any additional libraries.


## Usage
```
python sha256.py [-h] [--file [FILE]] [--test] [text]

positional arguments:
  text                  Text to be hashed

optional arguments:
  -h, --help            show this help message and exit
  --file [FILE], -f [FILE]
                        Allows to specify the file from which the data will be hashed
  --test, -t            Runs tests for the program
```
## Examples
Text from command line:
```sh
$ python3 sha256.py abcd
88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589
```

Passing the file to hash its contents:
```sh
$ python3 sha256.py -f "filename"
88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589
```

Running the tests:
```sh
$ python3 sha256.py -t
...
```
