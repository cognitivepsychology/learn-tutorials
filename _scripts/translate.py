from bs4 import BeautifulSoup
import json
import os

import status

# -------------------------------------------------------------------------------
# 
# Translation methods for hyperrefs, sources, etc
# 
# -------------------------------------------------------------------------------

NAME="translate"  # name of this module

# Get dictionary in translate_static.json
def get_translate_static(folder):
    file_path = os.path.join(folder,'translate_static.json')
    with open(file_path) as f:
        translate = json.load(f)
    return translate

# Get dictionary in translate_filename_url.json
def get_translate_filename_url(folder):
    file_path = os.path.join(folder,'translate_filename_url.json')
    with open(file_path) as f:
        translate = json.load(f)
    return translate

# Get the 'new' replacing string 
def get_new(old,s,dir_url):
    if old.endswith(('.png','jpeg','jpg','gif')): 
        new = os.path.join(s,dir_url)+'/'   # => one for each html file
    #elif old.endswith(('.css')): 
    #    new = os.path.join(s,dir_url)+'/'   # => one for each html file
    else:
        new = s
    return new

# Translate image source and make list of image paths
def translate_img_src(soup, path_html, dir_url, translate_static):
    folder_html = os.path.split(path_html)[0]
    Img = soup.findAll('img')
    paths_image = []
    for img in Img:
        if not img.has_attr('src'):
            continue
        for src_head in translate_static.keys():
            if img['src'].startswith(src_head):  # TODO add support for no folder
                status.log(NAME,('src (static) to translate found: ', img['src']))
                paths_image.append(os.path.join(folder_html,img['src']))
                new = get_new(img['src'],translate_static[src_head],dir_url)
                img['src'] = img['src'].replace(src_head,new)
                status.log(NAME,('... translated to: ', img['src']))
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
                status.log(NAME,('src (static) to translate found: ', script['src']))
                new = get_new(script['src'],translate_static[src_head],dir_url)
                script['src'] = script['src'].replace(src_head,new)
                status.log(NAME,('... translated to (but will get stripped): ', script['src']))
                break
    return soup

# Translate link hyperref
def translate_link_href(soup, dir_url, translate_static):
    Link = soup.findAll('link')
    for link in Link:
        if not link.has_attr('href'):
            continue
        for href_head in translate_static.keys():
            if link['href'].startswith(href_head):
                status.log(NAME,('href (static) to translate found: ', link['href']))
                new = get_new(link['href'],translate_static[href_head],dir_url)
                link['href'] = link['href'].replace(href_head,new)
                status.log(NAME,('... translated to: ', link['href']))
                break
    return soup

# Translate anchor hyperref
def translate_a_href(soup, dir_url, translate_static, translate_filename_url):
    A = soup.findAll('a')
    for a in A:
        if not a.has_attr('href'):
            continue
        for href_head in translate_static.keys(): # case 1 
            if a['href'].startswith(href_head):
                status.log(NAME,('href (static) to translate found: ', a['href']))
                new = get_new(a['href'],translate_static[href_head],dir_url)
                a['href'] = a['href'].replace(href_head,new)
                status.log(NAME,('... translated to: ', a['href']))
                break
        if a['href'].startswith('https://plot.ly/'): # case 2
            if a['href'].startswith('https://plot.ly/~'): # but not shareplot!
                continue
            status.log(NAME,('href (filename_url) to translate found: ', a['href']))
            a['href'] = a['href'].replace('https://plot.ly/','/')
            for href_tail in translate_filename_url.keys():
                if href_tail in a['href']:
                    status.log(NAME,('href to translate found: ', a['href']))
                    a['href'] = a['href'].replace(href_head,translate_static[href_tail])
                    break
            status.log(NAME,('... translated to: ', a['href']))
    return soup

# Add target blank attributes to link out of plotly pages
def add_target_blank(soup):
    A = soup.findAll('a')
    for a in A:
        if not a.has_attr('href'):
            continue
        if a['href'].startswith('http://') or a['href'].startswith('https://'):
            a['target'] = '_blank'
    return soup

# -------------------------------------------------------------------------------

def translate(soup, path_html, dir_url, translate_static, translate_filename_url):
    soup, paths_image  = translate_img_src(soup, path_html, dir_url, translate_static)
    soup = translate_script_src(soup, dir_url, translate_static)
    soup = translate_link_href(soup, dir_url, translate_static)
    soup = translate_a_href(soup, dir_url, translate_static, translate_filename_url)
    soup = add_target_blank(soup)
    return soup, paths_image
