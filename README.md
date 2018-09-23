# PORTAL
Brute force router administration credentials and enable remote management

Portal will look for a users.txt and passwords.txt in the current directory, and attempt to login to the router at the provided IP address.

If the program is able to authenticate successfully it uses the discovered credentials and attempts to enable remote management.  


# Usage
- users.txt - list of usernames to brute force; one per line
- passwords.txt - list of passwords to brute force; one per line

```
python portal.py <target ip>
```

#### Example
```
python portal.py 192.168.1.1
```

### Verified On
- NETGEAR Router WNDR4300
