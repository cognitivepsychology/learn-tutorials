import bs4
from bs4 import BeautifulSoup
import os

import status

# -------------------------------------------------------------------------------
#
# Methods to update body to publishable-level
#
# -------------------------------------------------------------------------------

NAME = "update_body"  # name of this module

# -------------------------------------------------------------------------------


# Wrap tag around an other
# source: http://stackoverflow.com/a/10192634
def wrap(wrappend, wrap_tag, wrap_attrs):
    _soup = BeautifulSoup()
    wrapper = _soup.new_tag(wrap_tag, **wrap_attrs)
    contents = wrappend.replaceWith(wrapper)
    wrapper.append(contents)
    return


# Strip contents inside tag but keep tag
def strip_contents(tag):
    for content in tag.contents:
        content.extract()
    return


# Insert tag inside an other
# source: http://stackoverflow.com/a/21356230/4068492
def insert(insertend, insert_tag, insert_attrs, insert_content, replace=True):
    _soup = BeautifulSoup()
    to_insert = _soup.new_tag(insert_tag, **insert_attrs)
    to_insert.string = insert_content
    if replace:
        strip_contents(insertend)
    insertend.append(to_insert)
    return

# -------------------------------------------------------------------------------


# Strip all attributes, <script></script> from body
def strip(body):
    attrs_to_rm = ["class", "id", "name", "style"]
    for attr in attrs_to_rm:
        del body[attr]
    for tag in body():
        for attr in attrs_to_rm:
            del tag[attr]
    status.log(NAME, (
        "Striping attributes", ' | '.join(attrs_to_rm), 'inside body !')
    )
    Script = body.findAll('script')
    for script in Script:
        script.extract()
    status.log(NAME, "Striping all <script> inside body !")
    return body


# Add lightbox anchors to images
def add_lightbox(body):
    Img = body.findAll('img')
    wrap_tag = 'a'
    for img in Img:
        status.log(NAME, ('Image found! src:', img['src']))
        # If not <a> around <img />, add lightbox !
        if not img.findParent('a'):  # TODO maybe only lightbox <a>
            src = img['src']
            data = os.path.splitext(os.path.basename(img['src']))[0]
            wrap_attrs = {
                'href': src,
                'data-lightbox': data
            }
            wrap(img, wrap_tag, wrap_attrs)
            status.log(NAME, ('... wrap with lightbox <a>'))
        else:
            status.log(NAME, ("... <a> found around it, doing nothing"))
    return body


# Add anchor to headers (for easy link sharing)
def add_header_anchors(body):
    H_str = ['h1', 'h2', 'h3', 'h4']
    for h_str in H_str:
        H = body.findAll(h_str)
        insert_tag = 'a'
        for h in H:
            text = h.getText(strip=True, separator=u' ')
            status.log(NAME, ('Header found! text:', text.encode('utf8')))
            # If <h{} />  is empty, remove it
            if not text:
                h.extract()
                status.log(NAME, ('... is empty, removing it!'))
                continue
            # Add id attr to <h{}>
            _id = text.replace(' ', '-').lower()
            h['id'] = _id
            status.log(NAME, (
                "... add id: '{}'"
            ).format(_id.encode('utf8')))
            # Add <a href= > around text
            _href = '#' + _id
            insert_attrs = {'href': _href}
            insert(h, insert_tag, insert_attrs, text)
            status.log(NAME, (
                "... insert <a href='{}'>"
            ).format(_href.encode('utf8')))
    return body


# Get inline latex content (i.e. remove html tags)
def get_inline_latex_content(body):
    latex_starts = ("$$", "\\begin{equation}")
    latex_ends = ("$$", "\\end{equation}")
    Span = body.findAll('span')
    for span in Span:
        try:
            # Loop through possible latex starts
            for latex_start in latex_starts:
                if latex_start in span.contents[0]:
                    # Init. latex content and trackers
                    in_latex = True
                    in_latex_content = span.contents
                    in_latex_tags = [span]
                    status.log(NAME, (
                        "<span> containing latex (i.e. {start}) found:"
                    ).format(start=latex_start))
                    # Get next tag, TODO generalize?
                    _next = span.findNext(('p', 'span'))
                    while in_latex:
                        if _next.name != 'span':
                            # If not span, find next span
                            in_latex_tags += [_next]
                            _next = _next.findChild('span')
                            continue
                        # Add content to leading span
                        in_latex_content += _next.contents
                        status.log(NAME, (
                            '... more in-line latex content:',
                            ' '.join((_next.contents)).replace('\n', '')
                        ))
                        for latex_end in latex_ends:
                            # Check if latex end is reached
                            if latex_end in _next.contents[0]:
                                in_latex = False
                        # Add in latex tag, for tracking
                        in_latex_tags += [_next]
                        _next = _next.findNext(('p', 'span'))
                    # Delete in latex tags
                    for in_latex_tag in in_latex_tags[1:]:
                        in_latex_tag.extract()
                    # TODO wrap in latex content in "$$" ?
        except (IndexError, TypeError):  # TODO generalize?
            pass
    return body


# Prettify and remove <body> and </body>
def prettify(body):
    body = body.prettify().encode('utf8')
    body = body.replace('<body>', '')
    body = body.replace('</body>', '')
    return body

# -------------------------------------------------------------------------------


def update_body(body):
    body = strip(body)
    body = add_lightbox(body)
    body = add_header_anchors(body)
    body = get_inline_latex_content(body)
    body = prettify(body)
    return body
