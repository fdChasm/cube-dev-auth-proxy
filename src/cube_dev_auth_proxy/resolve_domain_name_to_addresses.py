from twisted.names import client
from twisted.names.dns import Record_A, Record_AAAA


def extractAddressRepresentation(a):
    payload = a.payload
    if isinstance(payload, Record_A):
        return payload.dottedQuad()
    elif isinstance(payload, Record_AAAA):
        return payload._address

def formatRecords(records):
    answers = filter(lambda a: isinstance(a.payload, (Record_A, Record_AAAA)), records[0])
    address_representations = map(extractAddressRepresentation, answers)
    return filter(None, address_representations)

def resolve_domain_name_to_addresses(domain_name):
    dns_resolver = client.Resolver('/etc/resolv.conf')

    # return defer.gatherResults([
    #    dns_resolver.lookupAddress(domain_name).addCallback(formatRecords),
    #    dns_resolver.lookupIPV6Address(domain_name).addCallback(formatRecords)
    # ])

    return dns_resolver.lookupAddress(domain_name).addCallback(formatRecords)
