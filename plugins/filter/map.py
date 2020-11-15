from ansible import errors
import re


def key_filter(d, find='.+'):
    target = {}

    for key in d.keys():
        if re.match(find, key):
            target[key] = d[key]

    return target


def key_replace(d, find='(.+)', replace='\1'):
    target = {}
    for key in d.keys():
        target[re.sub(find, replace, key)] = d[key]

    return target


class FilterModule(object):
    ''' utility filters for operating on dictionary '''

    def filters(self):
        return {
            'key_filter': key_filter,
            'key_replace': key_replace
        }
