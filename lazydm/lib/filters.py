import re
from pygments import formatters, highlight, lexers
from pygments.lexers import guess_lexer, get_lexer_by_name

def bbcode(value):
    value = re.sub(re.compile('\[i\](.+?)\[\/i\]', re.DOTALL),
                  '<i>\\1</i>',
                  value)
    value = re.sub(re.compile('\[b\](.+?)\[\/b\]', re.DOTALL),
                  '<strong>\\1</strong>',
                  value)
    value = re.sub(re.compile('\[code\](.+?)\[\/code\]', re.DOTALL),
                  highlight_callback,
                  value)
    value = re.sub(re.compile('\[center\](.+?)\[\/center\]', re.DOTALL),
                  '<center>\\1</center>',
                  value)
    value = re.sub(re.compile('\[img\](.+?)\[\/img\]', re.DOTALL),
                  '<img src="\\1" />',
                  value)
    value = re.sub(re.compile('\[img\s*width\s*=\s*(\d+)\](.+?)\[\/img\]', re.DOTALL),
                  '<img src="\\2" style="width: \\1px;" />',
                  value)
    value = re.sub(re.compile('\[url\s*=\s*((https?://)?[^\s]+)\](.+?)\[\/url\]', re.DOTALL),
                  '<a href="\\1">\\3</a>',
                  value)
    value = re.sub(re.compile('\[url\](.+?)\[\/url\]', re.DOTALL),
                  '<a href="\\1">\\1</a>',
                  value)
    return value

def highlight_callback(match_object):
    try:
        lexer = guess_lexer(match_object.group(1))
    except:
        lexer = get_lexer_by_name("python", stripall=True)
    formatter = formatters.HtmlFormatter()
    result = highlight(match_object.group(1), lexer, formatter)
    return result

def slugify(inStr):
    removelist = ["a", "an", "as", "at", "before", "but", "by", "for","from","is", "in", "into", "like", "of", "off", "on", "onto","per","since", "than", "the", "this", "that", "to", "up", "via","with"];
    for a in removelist:
        aslug = re.sub(r'\b'+a+r'\b','',inStr)
    aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
    aslug = re.sub('\s+', '-', aslug)
    return aslug

def plural(val, plural='', single=''):
    if val > 1:
        if plural:
            return plural
        else:
            return u's'
    else:
        return single
