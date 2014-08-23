from bs4 import BeautifulSoup
import json
import sys
import os

# -------------------------------------------------------------------------------
# 
# Translation methods for hyperrefs, sources, etc
# 
# -------------------------------------------------------------------------------

NAME="translate"  # name of this module

# Shortcut to print status along with the name of the script
def status(s):
    S = str(("[{}]".format(NAME), s))
    with open('publish.log', 'a') as f:
        f.write(S+"\n")
    return

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
def get_new(old,s,file_html_url):
    if old.endswith(('.png','jpeg','jpg','gif')): 
        new = os.path.join(s,file_html_url)+'/'   # => one for each html file
    #elif old.endswith(('.css')): 
    #    new = os.path.join(s,file_html_url)+'/'   # => one for each html file
    else:
        new = s
    return new

# Translate image source and make list of image paths
def translate_img_scr(soup, folder, file_html_url, translate_static):
    Img = soup.findAll('img')
    paths_image = []
    for img in Img:
        if not img.has_attr('src'):
            continue
        for src_head in translate_static.keys():
            if img['src'].startswith(src_head):
                status(('src (static) to translate found: ', img['src']))
                paths_image.append(os.path.join(folder,'raw',file_html_url,img['src']))
                new = get_new(img['src'],translate_static[src_head],file_html_url)
                img['src'] = img['src'].replace(src_head,new)
                status(('... translated to: ', img['src']))
                break
    return soup, paths_image

# Translate script source
def translate_script_scr(soup, file_html_url, translate_static):
    Script = soup.findAll('script')
    for script in Script:
        if not script.has_attr('src'):
            continue
        for src_head in translate_static.keys():
            if script['src'].startswith(src_head):
                status(('src (static) to translate found: ', script['src']))
                new = get_new(script['src'],translate_static[src_head],file_html_url)
                script['src'] = script['src'].replace(src_head,new)
                status(('... translated to: ', script['src']))
                break
    return soup

# Translate link hyperref
def translate_link_href(soup, file_html_url, translate_static):
    Link = soup.findAll('link')
    for link in Link:
        if not link.has_attr('href'):
            continue
        for href_head in translate_static.keys():
            if link['href'].startswith(href_head):
                status(('href (static) to translate found: ', link['href']))
                new = get_new(link['href'],translate_static[href_head],file_html_url)
                link['href'] = link['href'].replace(href_head,new)
                status(('... translated to: ', link['href']))
                break
    return soup

# Translate anchor hyperref
def translate_a_href(soup, file_html_url, translate_static, translate_filename_url):
    A = soup.findAll('a')
    for a in A:
        if not a.has_attr('href'):
            continue
        for href_head in translate_static.keys(): # case 1 
            if a['href'].startswith(href_head):
               status(('href (static) to translate found: ', a['href']))
               new = get_new(a['href'],translate_static[href_head],file_html_url)
               a['href'] = a['href'].replace(href_head,new)
               break
        if a['href'].startswith('https://plot.ly/') :       # case 2
           status(('href (filename_url) to translate found: ', a['href']))
           a['href'] = a['href'].replace('https://plot.ly/','/')
           for href_tail in translate_filename_url.keys():
               if href_tail in a['href']:
                   status(('href to translate found: ', a['href']))
                   a['href'] = a['href'].replace(href_head,translate_static[href_tail])
                   break
        status(('... translated to: ', a['href']))
    return soup

# -------------------------------------------------------------------------------

def translate(soup, folder, file_html_url, translate_static, translate_filename_url):
    soup, path_image  = translate_img_scr(soup, folder, file_html_url, translate_static)
    soup = translate_script_scr(soup, file_html_url, translate_static)
    soup = translate_link_href(soup, file_html_url, translate_static)
    soup = translate_a_href(soup, file_html_url, translate_static, translate_filename_url)
    return soup, paths_image
