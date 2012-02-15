import sys, os, shutil
import markdown
from pyquery import PyQuery as pq

j = os.path.join
md = markdown.Markdown(extensions=['toc', 'codehilite'])
up = lambda p: j(*os.path.split(p)[:-1])
dirname = lambda p: os.path.basename(os.path.abspath(p))

BUILD_LOC = './build'
CUSTOM_PATH = './resources'
BASE_PATH = j(up(__file__), 'resources')

PRE = '''\
<!DOCTYPE html>
<html>
    <head>
        <title>{title_tag}</title>
        {resources}
    </head>
    <body class="{page_type}">
        <div class="wrap">
            <header><h1><a href="{project_href}">{project_title}</a></h1></header>
                <div class="markdown">
'''
POST = '''
                </div>
            <footer>{footer}</footer>
        </div>
    </body>
</html>
'''

CSS = '''\
        <link rel="stylesheet" href="{dots}/_dmedia/{resource}"/>
'''
LESS = '''\
        <link rel="stylesheet/less" type="text/css" href="{dots}/_dmedia/{resource}">
'''
JS = '''\
        <script src="{dots}/_dmedia/{resource}" type="text/javascript">
        </script>
'''


def _get_target_url(path):
    return os.path.split(_get_target(path))[-1]

def _get_target(path):
    parts = path.split('-', 1)

    if len(parts) > 1 and all(c in '0123456789' for c in parts[0]):
        target = parts[1]
    else:
        target = path

    return j(BUILD_LOC, target.rsplit('.', 1)[0])

def _get_project_title():
    if os.path.isfile('title'):
        with open('title') as f:
            return f.read().strip()
    else:
        current = dirname('.').lower()
        if current not in ['doc', 'docs', 'documentation']:
            return current
        else:
            return dirname('..').lower()

def _get_resources():
    base_resources = []
    if os.path.isdir(BASE_PATH):
        base_resources = [x for x in os.listdir(BASE_PATH)]
        base_resources.sort()
        # do not copy, may not need.

    custom_resources = []
    if os.path.isdir(CUSTOM_PATH):
        custom_resources = [x for x in os.listdir(CUSTOM_PATH)]
        custom_resources.sort()

        if all(os.path.isfile(j(CUSTOM_PATH, x)) for x in custom_resources):
            # all are files, everything is legit.
            [_copy_raw_file(CUSTOM_PATH, x) for x in custom_resources]
        else:
            raise Exception('Custom resources with subdirectories unsupported')

    resources = []
    if any((os.path.splitext(r)[1] == '.css'
         or os.path.splitext(r)[1] == '.less') for r in custom_resources):
        # there are css or less files, only use those.
        resources = custom_resources

    else:
        # need base resources, no css or less files in custom_resources
        # but first, make sure no files share the same name. such as .js files.
        if any(cr in base_resources for cr in custom_resources) :
            raise Exception('Need base file, but custom one detected')

        [_copy_raw_file(BASE_PATH, x) for x in base_resources]
        resources = base_resources + custom_resources

    return resources

def _find_chapters():
    for filename in os.listdir('.'):
        name, ext = os.path.splitext(filename)
        if ext in ['.markdown', '.md', '.mdown']:
            if name not in ['footer', 'index']:
                yield filename

def _copy_raw_file(path, filename):
    shutil.copyfile(j(path, filename),
                    j(BUILD_LOC, '_dmedia', filename))

def _get_footer():
    if os.path.isfile('./footer.markdown'):
        with open('./footer.markdown') as f:
            return md.convert(f.read())
    elif os.path.isfile('./footer.mdown'):
        with open('./footer.mdown') as f:
            return md.convert(f.read())
    elif os.path.isfile('./footer.md'):
        with open('./footer.md') as f:
            return md.convert(f.read())
    else:
        return ''

def _get_toc(chapters):
    toc = '<h2>Table of Contents</h2>'
    toc += '<ol class="toc">'

    for filename, title in chapters:
        toc += '<li><a href="%s/">%s</a></li>' % (_get_target_url(filename), title)

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

    return unicode(e)

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

def _render_resources(resources, page_type):
    """ Generates html for the given resources based on each resource's
    extension
    """

    # link to the correct folder
    dots = '..'
    if page_type == 'index':
        dots = '.'

    css, less, js = CSS, LESS, JS

    css_str = str()
    less_str = str()
    js_str = str()
    for filename in resources:
        name, ext = os.path.splitext(filename)
        if ext == '.css':
            css_str += css.format(dots=dots, resource=filename)
        elif ext == '.less':
            less_str += less.format(dots=dots, resource=filename)
        elif ext == '.js':
            js_str += js.format(dots=dots, resource=filename)

    res_str = css_str + less_str + js_str
    return res_str.strip()


def _render(title, footer, path, target, resources, page_type, toc=None):
    pre, post = PRE, POST

    with open(path) as f:
        data = f.read()

    fallback_title = _get_fallback_title(path)

    if page_type == 'content':
        page_title = _find_title(data) or fallback_title
        title_tag = page_title + ' / ' + title
        href = '..'
    else:
        page_title = title_tag = title
        href = ''

    content_resources = _render_resources(resources, page_type)

    content = pre.format(title_tag=title_tag,
            resources=content_resources,
            project_href=href,
            project_title=title,
            page_type=page_type)
    content += md.convert(data)
    content += toc or ''
    content += post.format(footer=footer)

    if page_type == 'content':
        content = _linkify_title(_fix_md_toc(content), fallback_title)
        # this is gobbling up the DOCTYPE line for some reason.
        content = "<!DOCTYPE html>\n" + content

    if not os.path.isdir(target):
        os.makedirs(target)

    with open(j(target, 'index.html'), 'w') as f:
        f.write(content)

    return page_title


def render_chapter(title, footer, path, resources):
    target = _get_target(path)
    return _render(title, footer, path, target, resources, 'content')

def render_index(title, footer, chapters, resources):
    if os.path.isfile('index.markdown'):
        path = 'index.markdown'
    elif os.path.isfile('index.mdown'):
        path = 'index.mdown'
    elif os.path.isfile('index.md'):
        path = 'index.md'
    else:
        return

    target = BUILD_LOC
    toc = _get_toc(chapters)

    return _render(title, footer, path, target, resources, 'index', toc)

def render_files():
    _ensure_dir(BUILD_LOC)
    _ensure_dir(j(BUILD_LOC, '_dmedia'))

    title = _get_project_title()
    footer = _get_footer()
    resources = _get_resources()

    chapters = []
    for filename in _find_chapters():
        chapter_title = render_chapter(title, footer, filename, resources)
        chapters.append((filename, chapter_title))

    render_index(title, footer, chapters, resources)


def main():
    if len(sys.argv) > 1:
        sys.stderr.write("d doesn't take any arguments.\n")
        sys.stderr.write("Just cd into your docs/ directory, run d, and move on.\n")
        sys.exit(1)
    else:
        render_files()
