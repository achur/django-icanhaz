from django import template

from ..conf import conf
from ..loading import find, findAll, ICanHazTemplateNotFound



register = template.Library()



class ICanHazNode(template.Node):
    def __init__(self, name):
        self.name = template.Variable(name)


    def render(self, context):
        name = self.name.resolve(context)

        try:
            filepath = find(name)
            fp = open(filepath, "r")
            output = fp.read().decode(conf.FILE_CHARSET)
            fp.close()
            output = ('<script id="%s" type="text/html">\n'
                      % name) + output + "\n</script>\n"
        except (IOError, ICanHazTemplateNotFound):
            output = ""
            if conf.DEBUG:
                raise

        return output



class ICanHazRegexNode(template.Node):
    def __init__(self, dir, regex):
        self.dir = template.Variable(dir)
        self.regex = template.Variable(regex)


    def render(self, context):
        dir = self.dir.resolve(context)
        regex = self.regex.resolve(context)

        pairs = findAll(dir, regex)
        result = ""

        for (name, filepath) in pairs:
            try:
                fp = open(filepath, "r")
                output = fp.read().decode(conf.FILE_CHARSET)
                fp.close()
                result += ('<script id="%s" type="text/html">\n'
                           % name) + output + "\n</script>\n"
            except IOError:
                if conf.DEBUG:
                    raise

        return result



@register.tag
def icanhaz(parser, token):
    """
    Finds the ICanHaz template for the given name and renders it surrounded by
    the requisite ICanHaz <script> tags.

    """
    bits = token.contents.split()
    if len(bits) not in [2, 3]:
        raise template.TemplateSyntaxError("""
            'icanhaz' tag takes either
              one argument: the name/id of the template
            or
              two arguments: the name of a subdirectory to search and
                             a regular expression of files to search for
            """)
    if len(bits) == 3:
        return ICanHazRegexNode(bits[1], bits[2])
    return ICanHazNode(bits[1])
