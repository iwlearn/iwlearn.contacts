# vocabularies
from plone.i18n.locales.countries import _countrylist

def get_countries():
    countries =[]
    for c  in _countrylist:
        countries.append(_countrylist[c]['name'])
    countries.sort()
    return countries

