# goecharger API (WIP)
Python API for accessing the go-eCharger EV-Charger via the local http-Endpoint

Tested with the "[go-eCharger HOME+](https://go-e.co/en/go-echarger-home-2/)" CEE-Version

# Warning: WIP - Braking changes possible
This is the first version of the API so there are still breaking chnages possible eg. output parameter names or values.

# Links
[Product Homepage](https://go-e.co/en/go-echarger-home-2/)

[API-Documentation](https://go-e.co/)

[Project Homepage](https://github.com/cathiele/goecharger)

[PyPi Package](https://pypi.org/project/goecharger/)

[goecharger CLI App](https://github.com/cathiele/goecharger-client) (TBD / WIP)

[Home Assistant Integration](https://github.com/cathiele/homeassistant-goecharger) (TBD / WIP)


# Features
- Query Charger Status
- Set Charger Configuration

# Install

```
pip install goecharger
```

# Example

```python
from goecharger import GoeCharger

charger = GoeCharger('192.168.1.1') # <- change to your charger IP
 
print (charger.requestStatus())
```