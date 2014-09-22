from bs4 import BeautifulSoup, Tag
import os

import status

# -------------------------------------------------------------------------------
# 
# Methods to update body to publishable-level
# 
# -------------------------------------------------------------------------------

NAME="update_body"  # name of this module

# -------------------------------------------------------------------------------

# Wrap tag around an other
# source: http://stackoverflow.com/a/10192634
def wrap(wrappend, wrap_tag, wrap_attrs):
    _soup = BeautifulSoup()
    wrapper = _soup.new_tag(wrap_tag, **wrap_attrs)
    contents = wrappend.replaceWith(wrapper)
    wrapper.append(contents)
    return 

# -------------------------------------------------------------------------------

# Strip all attributes, <script></script> and <body></body> from body
def strip(body):
    attrs_to_rm = ["class", "id", "name", "style"]
    for attr in attrs_to_rm:
        del body[attr]
    for tag in body():
        for attr in attrs_to_rm:
            del tag[attr]
    Script = body.findAll('script')
    for script in Script:
        script.extract()
    return body

# Add lightbox anchors to images
def add_lightbox(body):
    Img = body.findAll('img')
    wrap_tag = 'a'
    for img in Img:
        status.log(NAME, ('Image found! src:', img['src']))
        # If not <a> around <img />, add lightbox !
        if not img.findParent('a'):
            wrap_attrs = {
                'href': img['src'],
                'data-lightbox': os.path.splitext(os.path.basename(img['src']))[0]
            }
            wrap(img, wrap_tag, wrap_attrs)
            status.log(NAME, ('... wrap with lightbox <a>'))
        else:
            status.log(NAME, ("... <a> found around it, doing nothing"))
    return body

# Prettify and remove <body>
def prettify(body):
    body = body.prettify().encode('utf8')
    body = body.replace('<body>','')
    body = body.replace('</body>','')
    return body

# -------------------------------------------------------------------------------

def update_body(body):
    body = strip(body)
    body = add_lightbox(body)
    body = prettify(body)
    return body
