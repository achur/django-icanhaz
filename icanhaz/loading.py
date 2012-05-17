from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from .conf import conf



def find(name):
    for finder in finders:
        filepath = finder.find(name)
        if filepath is not None:
            return filepath

    raise ICanHazTemplateNotFound(name)



def findAll(dir, regex):
    result = []
    for finder in regexfinders:
        paths = finder.findAll(dir, regex)
        if paths is not None:
            result += paths
    return result



def _get_finders(finder_conf):
    ret = []
    for finder_path in finder_conf:
        modpath, cls_name = finder_path.rsplit(".", 1)
        try:
            mod = import_module(modpath)
        except ImportError, e:
            raise ImproperlyConfigured(
                "ImportError %s: %s" % (modpath, e.args[0]))

        try:
            cls = getattr(mod, cls_name)
        except AttributeError, e:
            raise ImproperlyConfigured(
                "AttributeError %s: %s" % (cls_name, e.args[0]))

        ret.append(cls())

    return ret



# Instantiate finders
finders = _get_finders(conf.ICANHAZ_FINDERS)
regexfinders = _get_finders(conf.ICANHAZ_REGEX_FINDERS)



class ICanHazTemplateNotFound(Exception):
    pass
