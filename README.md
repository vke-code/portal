# PORTAL - Router Bruteforce Tool
_Bruteforce router administration credentials and attempt to enable remote management_

[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

Portal will look for a users.txt and passwords.txt in the current directory, and attempt to login to the router at the provided IP address.

If the program is able to authenticate successfully it uses the discovered credentials and attempts to enable remote management.

For a full analysis and description of the program check out the article I wrote on this process:

- [Bruteforce Router Takeover (Part 1)](http://kai-taylor.com/brute-force-router-takeover/)

## Requirements
Portal requires the following libraries to be installed:
- Requests  

The required packages can be installed with the following command:

```sh
$ pip install -r requirements.txt
```

## Usage
- users.txt - list of usernames to brute force; one per line
- passwords.txt - list of passwords to brute force; one per line

```sh
$ python portal.py <target ip>
```

#### Example
```sh
$ python portal.py 192.168.1.1
```

## Planned Updates
- add command line parameters for user and password files
- implement multithreading for bruteforcing
- perform target device identification

## History
- 09/22/18 - v1.0 initial implementation and testing


## Supported Devices

| Manufacturer | Model    | Verified         |
|:-------------|:---------|:----------------:|
| NETGEAR      | WNDR4300 |:white_check_mark:|

### Developed by
- [SecuringNinja](https://securingninja.com)
