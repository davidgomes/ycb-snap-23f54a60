"""
Email message and email sending related helper functions.
"""

import socket

from django.utils.encoding import punycode


# Cache the hostname, but do it lazily: socket.getfqdn() can take a couple of
# seconds, which slows down the restart of the server.
class CachedDnsName:
    def __init__(self):
        # None means "not looked up yet". The attribute is always present so
        # the cache can be cleared before the first lookup.
        self._fqdn = None

    def __str__(self):
        return self.get_fqdn()

    def get_fqdn(self):
        if getattr(self, '_fqdn', None) is None:
            self._fqdn = punycode(socket.getfqdn())
        return self._fqdn


DNS_NAME = CachedDnsName()
