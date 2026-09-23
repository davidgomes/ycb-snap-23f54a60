"""
Email message and email sending related helper functions.
"""

import socket


# Cache the hostname, but do it lazily: socket.getfqdn() can take a couple of
# seconds, which slows down the restart of the server.
class CachedDnsName:
    def __str__(self):
        return self.get_fqdn()

    def get_fqdn(self):
        if not hasattr(self, '_fqdn'):
            self._fqdn = punycode(socket.getfqdn())
        return self._fqdn


def punycode(domain):
    """Return the Punycode of the given domain if it's non-ASCII."""
    return str(domain).encode('idna').decode('ascii')


DNS_NAME = CachedDnsName()
