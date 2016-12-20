# -*- coding: utf-8 -*-

from openprovider.modules import E, OE, common
from openprovider.models import ZoneDetails


def _domain(domain):
    sld, tld = domain.split('.', 1)

    return E.domain(
        E.name(sld),
        E.extension(tld),
    )


def _records(records):
    if not records:
        return None

    fields = ('type', 'name', 'value', 'prio', 'ttl')
    items = [E.item(E(field, record.get(field))) for field in fields for record in records]
    return E.records(E.array(*items))


class NameserverModule(common.Module):
    """Bindings to API methods in the nameserver module."""

    def search_zone_dns_request(self, limit=None, offset=None, extension=None,
                              name_pattern=None, type=None,
                              with_records=None, with_history=None):

        request = E.searchZoneDnsRequest(
            OE('limit', limit),
            OE('offset', offset),
            OE('namePattern', name_pattern),
            OE('type', type),
            OE('withRecords', with_records, transform=int),
            OE('withHistory', with_history, transform=int),
        )
        response = self.request(request)
        return response.as_models(ZoneDetails)

    def retrieve_zone_dns_request(self, name, with_records=None, with_history=None):

        request = E.retrieveZoneDnsRequest(
            E.name(name),
            OE('withRecords', with_records, transform=int),
            OE('withHistory', with_history, transform=int),
        )
        response = self.request(request)
        return response.as_model(ZoneDetails)

    def modify_zone_dns_request(self, domain, type, masterip=None, records=None,
                                is_spamexperts_enabled=None):
        """Modify DNS Records"""

        self.request(
            E.modifyZoneDnsRequest(
                _domain(domain),
                E.type(type),
                OE('masterip', masterip),
                _records(records),
                OE('isSpamexpertsEnabled', is_spamexperts_enabled, transform=int),
            ),
        )

        return True
