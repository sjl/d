import sys, os, shutil
import markdown
from pyquery import PyQuery as pq

j = os.path.join
md = markdown.Markdown(extensions=['toc', 'codehilite'])
up = lambda p: j(*os.path.split(p)[:-1])
dirname = lambda p: os.path.basename(os.path.abspath(p))

extensions = ['md', 'mdown', 'markdown']

INDEX_PRE = '''\
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>{title_tag}</title>
        <link rel="stylesheet" href="./_dmedia/bootstrap.css"/>
        <link rel="stylesheet" href="./_dmedia/tango.css"/>
        <link rel="stylesheet/less" type="text/css" href="./_dmedia/style.less">
        <script src="./_dmedia/less.js" type="text/javascript">
        </script>
    </head>
    <body class="index">
        <div class="wrap">
            <header><h1><a href="">{project_title}</a></h1></header>
                <div class="markdown">
'''
CONTENT_PRE = '''\
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>{title_tag}</title>
        <link rel="stylesheet" href="../_dmedia/bootstrap.css"/>
        <link rel="stylesheet" href="../_dmedia/tango.css"/>
        <link rel="stylesheet/less" type="text/css" href="../_dmedia/style.less">
        <script src="../_dmedia/less.js" type="text/javascript">
        </script>
    </head>
    <body class="content">
        <div class="wrap">
            <header><h1><a href="..">{project_title}</a></h1></header>
                <div class="markdown">
'''
POST = '''
                </div>
            <footer>{footer}</footer>
        </div>
    </body>
</html>
'''



def _read(f):
    return f.read().decode('utf-8')

def _write(f, content):
    return f.write(content.encode('utf-8'))


def _get_target_url(path, destination):
    return os.path.split(_get_target(path, destination))[-1]


def _get_target(filename, destination):
    parts = filename.split('-', 1)

    if len(parts) > 1 and all(c in '0123456789' for c in parts[0]):
        filename = parts[1]

    return j(destination, filename.rsplit('.', 1)[0])


def _get_project_title(source):
    if os.path.isfile(j(source, 'title')):
        with open(j(source, 'title')) as f:
            return _read(f).strip()
    else:
        current = dirname(source).lower()
        if current not in ['doc', 'docs', 'documentation']:
            return current
        else:
            return dirname(j(source, '..')).lower()

def _find_chapters(source):
    for filename in sorted(os.listdir(source)):
        name, ext = os.path.splitext(filename)
        if ext[1:] in extensions:
            if name not in ['footer', 'index']:
                yield filename


def _get_footer(source):
    for ext in extensions:
        filename = 'footer.' + ext
        target = j(source, filename);
        if os.path.isfile(target):
            with open(target) as f:
                return md.convert(_read(f))

    return ''


def _get_toc(chapters, destination):
    toc = '<h2>Table of Contents</h2>'
    toc += '<ol class="toc">'

    for filename, title in chapters:
        toc += '<li><a href="%s/">%s</a></li>' % (_get_target_url(filename, destination), title)

    toc += '</ol>'

    return toc

def _fix_md_toc(content):
    """Remove the first heading level from the Markdown-generated TOC.

    Only do so if it's on its own, though.

    """
    e = pq(content)
    if not e('.toc'):
        return content

    lis = e('.toc > ul > li')
    if len(lis) > 1:
        return content

    subtoc = e('.toc > ul > li > ul').html()
    e('.toc > ul').html(subtoc)
    return unicode(e)

def _linkify_title(content, fallback_title):
    e = pq(content)

    title = e('.markdown h1').text()
    if title:
        e('.markdown h1').html('<a href="">' + title + '</a>')
    else:
        e('.markdown').prepend('<h1><a href="">' + fallback_title + '</a></h1>')

    # What the fuck, pyquery?
    return u'<!DOCTYPE html>\n' + unicode(e)

def _ensure_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def _get_fallback_title(path):
    title = path.split('.', 1)[0]
    if '-' in title and all([c in '0123456789' for c in title.split('-', 1)[0]]):
        title = title.split('-', 1)[1]

    title = title.replace('-', ' ').replace('_', ' ')

    if title.lower() == title:
        title = title.capitalize()

    return title

def _find_title(content):
    # TODO: Make this less ugly.
    lines = content.splitlines()

    if len(lines) == 0:
        return None
    first_line = lines[0].strip()

    if first_line.startswith('#'):
        return first_line.lstrip('#')

    if len(lines) == 1:
        return None

    second_line = lines[1].strip()

    if second_line and all(c == '=' for c in second_line):
        return first_line

    return None


def _render(title, header, footer, source, destination, page_type, toc=None):
    with open(source) as f:
        data = _read(f)

    fallback_title = _get_fallback_title(source)

    if page_type == 'content':
        page_title = _find_title(data) or fallback_title
        title_tag = page_title + ' / ' + title
    else:
        page_title = title_tag = title

    content = header.format(title_tag=title_tag, project_title=title)
    content += md.convert(data)
    content += toc or ''
    content += POST.format(footer=footer)

    if page_type == 'content':
        content = _linkify_title(_fix_md_toc(content), fallback_title)

    if not os.path.isdir(destination):
        os.makedirs(destination)

    with open(j(destination, 'index.html'), 'w') as f:
        _write(f, content)

    return page_title


def render_index(title, footer, chapters, source, destination):
    index_file = None
    for ext in extensions:
        filename = 'index.' + ext
        if os.path.isfile(j(source, filename)):
            index_file = j(source, filename)

    if index_file is None:
        return

    toc = _get_toc(chapters, destination)

    return _render(title, INDEX_PRE, footer, index_file, destination, 'index', toc)


def render_files(source, destination):
    _ensure_dir(destination)
    _ensure_dir(j(destination, '_dmedia'))

    title = _get_project_title(source)
    footer = _get_footer(source)

    resources = j(up(__file__), 'resources')
    for filename in os.listdir(resources):
        shutil.copyfile(j(resources, filename), j(destination, '_dmedia', filename))

    chapters = []
    for filename in _find_chapters(source):
        chapter_title = _render(title, CONTENT_PRE, footer,
                j(source, filename), _get_target(filename, destination), 'content')
        chapters.append((filename, chapter_title))

    render_index(title, footer, chapters, source, destination)
