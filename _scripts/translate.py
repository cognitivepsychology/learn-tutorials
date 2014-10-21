from bs4 import BeautifulSoup
import json
import os

import status

# -------------------------------------------------------------------------------
#
# Translation methods for hyperrefs, sources, etc
#
# -------------------------------------------------------------------------------

NAME = "translate"  # name of this module


# Get dictionary in translate_static.json
def get_translate_static(folder):
    file_path = os.path.join(folder, 'translate_static.json')
    with open(file_path) as f:
        translate_static = json.load(f)
    return translate_static


# Get dictionary in translate_filename_url.json
def get_translate_filename_url(folder):
    file_path = os.path.join(folder, 'translate_filename_url.json')
    with open(file_path) as f:
        translate = json.load(f)
    translate_filename_url = dict()
    translate_redirects = dict()
    for k, v in translate.items():
        if isinstance(v, list) and isinstance(v[-1], (str, unicode)):
            translate_filename_url[k] = v[-1]
            translate_redirects[v[-1]] = v[0:-1]
        elif isinstance(v, (str, unicode)):
            translate_filename_url[k] = v
        else:
            status.important(NAME, (
                "object values in {}/translate_filename_url.json\n"
                "must be either a string (the urls)\n"
                "or a list of strings (to handle redirects)"
            ).format(folder))
            status.stop(NAME)
    return translate_filename_url, translate_redirects

# -------------------------------------------------------------------------------


# Get the 'new' replacing string
def get_new(old, s, dir_url):
    if old.endswith(('.png', 'jpeg', 'jpg', 'gif')):
        new = os.path.join(s, dir_url)+'/'   # => one for each html file
#     elif old.endswith(('.css')):
#         new = os.path.join(s,dir_url)+'/'   # => one for each html file
    else:
        new = s
    return new

# -------------------------------------------------------------------------------


# Add alt attribute to images
def add_img_alt(img):
    src = img['src']
    alt = os.path.split(os.path.split(src)[0])[1] + '/' + os.path.basename(src)
    img['alt'] = alt
    status.log(NAME, (
        "... img, add alt='{}'").format(alt))
    return img


# Add target blank attribute to anchors with outbound href
def add_a_target_blank(a):
    if a.has_attr('href'):
        if a['href'].startswith('http://') or a['href'].startswith('https://'):
            a['target'] = '_blank'
            status.log(NAME, (
                "... an outbound link, add target='_blank' tag"))
    return a


# Add 'link--impt' class to anchor
def add_a_class(a):
    _class = "link--impt"
    if a.has_attr('href'):
        if not a['href'].startswith('/static'):
            a['class'] = _class
            status.log(NAME, (
                "... add class '{}' to anchor"
            ).format(_class))
    return a

# -------------------------------------------------------------------------------


# Translate image source and make list of image paths
def translate_img_src(soup, path_html, dir_url, translate_static):
    folder_html = os.path.split(path_html)[0]
    Img = soup.findAll('img')
    paths_image = []
    for img in Img:
        if not img.has_attr('src'):
            continue
        for src_head in translate_static.keys():
            if img['src'].startswith(src_head):
                status.log(NAME, (  # TODO add support for no folder
                    'src (static) to translate found: ',
                    img['src']))
                paths_image.append(os.path.join(folder_html, img['src']))
                new = get_new(img['src'], translate_static[src_head], dir_url)
                img['src'] = img['src'].replace(src_head, new)
                status.log(NAME, (
                    '... translated to: ', img['src']))
                img = add_img_alt(img)
                break
    return soup, paths_image


# Translate script source
def translate_script_src(soup, dir_url, translate_static):
    Script = soup.findAll('script')
    for script in Script:
        if not script.has_attr('src'):
            continue
        for src_head in translate_static.keys():
            if script['src'].startswith(src_head):
                status.log(NAME, (
                    'src (static) to translate found: ', script['src']))
                new = get_new(script['src'],
                              translate_static[src_head], dir_url)
                script['src'] = script['src'].replace(src_head, new)
                status.log(NAME, (
                    '... translated to (but will get stripped): ',
                    script['src']))
                break
    return soup


# Translate link href
def translate_link_href(soup, dir_url, translate_static):
    Link = soup.findAll('link')
    for link in Link:
        if not link.has_attr('href'):
            continue
        for href_head in translate_static.keys():
            if link['href'].startswith(href_head):
                status.log(NAME, (
                    'href (static) to translate found: ', link['href']))
                new = get_new(link['href'],
                              translate_static[href_head], dir_url)
                link['href'] = link['href'].replace(href_head, new)
                status.log(NAME, (
                    '... translated to: ', link['href']))
                break
    return soup


# Translate anchor href
def translate_a_href(soup, dir_url,
                     translate_static, translate_filename_url):
    A = soup.findAll('a')
    for a in A:
        is_translated = False  # to log relevant output
        # Clean up case
        if not a.getText(strip=True) and not a.findChildren():
            a.extract()
            status.log(NAME, (
                'Anchor with nothing in it found, removing it!'))
            continue
        if not a.has_attr('href'):
            a.extract()
            status.log(NAME, (
                'Anchor without href found, removing it!!'))
            continue
        # Now if 'real' anchor found
        status.log(NAME, ('Anchor found! href: ', a['href']))
        # Case 1: <a> to static location (translated from streambed)
        for href_head in translate_static.keys():
            if a['href'].startswith(href_head):
                status.log(NAME, (
                    '... href has a *static* start: ', href_head))
                new = get_new(a['href'], translate_static[href_head], dir_url)
                a['href'] = a['href'].replace(href_head, new)
                is_translated = True
                break
        # Case *: handle Google redirects
        google_start = 'https://www.google.com/url?q='
        google_end = '&'  # TODO could this be more strict?
        if a['href'].startswith(google_start):
            status.log(NAME, ('... href has a google redirect'))
            _s = a['href'].find(google_start) + len(google_start)
            _e = a['href'].find(google_end)
            a['href'] = (
                a['href'][_s:_e].replace('%3A', ':')
                                .replace('%2F', '/')
            )
        # Case 2: <a> to url location (translated to relative domain)
        href_starts = ['https://plot.ly/', 'plot.ly/', 'http://plot.ly/', '/']
        for href_start in href_starts:
            if a['href'].startswith(href_start):
                # 2.1 href to shareplot should have full URI
                if a['href'].startswith(href_start+'~'):
                    status.log(NAME, (
                        '... href links to shareplot:', a['href']))
                    status.log(NAME, (
                        '... guessing this is referring to a plot on prod'))
                    a['href'] = a['href'].replace(
                        href_start, 'https://plot.ly/', 1)
                    is_translated = True
                    continue
                # 2.2 Translate href start to django root
                if not a['href'].startswith('/'):
                    status.log(NAME, ('... href *url* start: ', href_start))
                    a['href'] = a['href'].replace(href_start, '/', 1)
                    is_translated = True
                # 2.3 Translate href to other docs using translate_filename_url
                for href_tail in translate_filename_url.keys():
                    if href_tail in a['href']:
                        status.log(NAME, ('... href has tail: ', a['href']))
                        a['href'] = a['href'].replace(
                            href_head, translate_static[href_tail])
                        is_translated = True
                        break

        # Log output
        if is_translated:
            status.log(NAME, ('... translated to: ', a['href']))
        else:
            status.log(NAME, ('... no translation required'))
        # Add attributes
        a = add_a_class(a)
        a = add_a_target_blank(a)
    return soup


# Translate script source
def translate_script_src(soup, dir_url, translate_static):
    Script = soup.findAll('script')
    for script in Script:
        if not script.has_attr('src'):
            continue
        for src_head in translate_static.keys():
            if script['src'].startswith(src_head):
                status.log(NAME, (
                    'src (static) to translate found: ', script['src']))
                new = get_new(script['src'],
                              translate_static[src_head], dir_url)
                script['src'] = script['src'].replace(src_head, new)
                status.log(NAME, (
                    '... translated to (but will get stripped): ',
                    script['src'])
                )
                break
    return soup

# -------------------------------------------------------------------------------


def translate(soup, path_html, dir_url,
              translate_static, translate_filename_url):
    soup, paths_image = translate_img_src(soup, path_html, dir_url,
                                          translate_static)
    soup = translate_script_src(soup, dir_url, translate_static)
    soup = translate_link_href(soup, dir_url, translate_static)
    soup = translate_a_href(soup, dir_url,
                            translate_static, translate_filename_url)
    return soup, paths_image
