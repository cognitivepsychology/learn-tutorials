from bs4 import BeautifulSoup
import json
import sys
import os
import shutil

import translate 
import make_urls, make_sitemaps

# -------------------------------------------------------------------------------
# 
# Publish script converting raw html content to plot.ly-ready content
#
# - Argument(s) is/are folder(s) from the learn_tutorials/ repository root.
#   Not that these folders must be published as a whole (hence this format).
#
# step (1) : Make body.html and config.json for each html file 
# step (2) : Copy images in the appropriate published/ subdirectories
# step (3) : Make folder-wide urls and sitemaps files
# 
# -------------------------------------------------------------------------------

NAME="publish"  # name of this script

# Shortcut to print status along with the name of the script
def status(s):
    S = str(("[{}]".format(NAME), s))
    with open('publish.log', 'a') as f:
        f.write(S+"\n")
    return
 
# -------------------------------------------------------------------------------

# Get input arguments 
def get_args():
    args = sys.argv[1:]
    if not args:
        print (
            "Usage:\n"
            "python {NAME}.py folder\n"
            "python {NAME}.py path/to/folder\n"
            "python {NAME}.py folder1 folder2 ... folderN\n"
        )
        sys.exit(0)
    elif not all(os.path.isdir(arg) for arg in args):
        print '** arguments must be directories **'
        sys.exit(0)
    else:
        return args

# Get list of HTML files in folder
def get_paths_html(folder):
    paths_html = []
    folder_raw = os.path.join(folder,'raw')
    if not os.path.isdir(folder_raw):
        print '** folder must contain a raw/ subfolder **'
        sys.exit(0)
    for path_folder, subfolders, files in os.walk(folder_raw):
        for f in files:
            if f.endswith('.html'):
                path_html = os.path.join(path_folder,f)
                paths_html.append(path_html)
    if not paths_html:
        print '** no .html files located inside {} **'.format(folder)
        sys.exit(0)
    return paths_html

# -------------------------------------------------------------------------------

# Get HTML soup from HTML file path
def get_soup(path_html):
    with open(path_html, "r") as f:
        status(("Opening", path_html))
        return BeautifulSoup(f)

# Get HTML <body> and <head>
def get_body_head(soup):
    status('grabs <body> and <head>')
    return soup.body, soup.head

# Get <title> and <meta name="description" > from <head> 
def get_config(head, path_html, tree):

    Title = head.findAll('title')
    if not len(Title):
        print '** There is no <title> in {} **'.format(path_html)
        print '** ... please fill in {}/config.json **'.format(tree)
        title = ""
    elif len(Title)>1:
        print '** There is more than one <title> in {} **'.format(path_html)
        print '** ... picking the last one for {}/config.json **'.format(tree)
        title = Title[-1].string
        status('strip <title> tags from <head>')
        for _title in Title:
            _title.extract()
    else:
        title = Title[0].string
        status('strip <title> tag from <head>')
        Title[0].extract()
    title = title.replace("\n",'')

    Meta = head.findAll('meta')
    Meta_description = [meta for meta in Meta if (meta.has_attr('name') and meta['name']=="description")]
    if not len(Meta_description):
        print '** There is no <meta name="description"> in {} **'.format(path_html)
        print '** ... please fill in {}/config.json **'.format(tree)
        meta_description = ""
    elif len(Meta_description)>1:
        print '** There is more than one <meta name="description"> in {} **'.format(path_html)
        print '** ... picking the last one for {}/config.json **'.format(tree)
        meta_description = Meta_description[-1]['content']
        status('strip <meta name="description"> tags from <head>')
        for _meta_description in Meta_description:
            _meta_description.extract()
    else:
        meta_description = Meta_description[0]['content']
        status('strip <meta name="description"> tag from <head>')
        Meta_description[0].extract()
    meta_description = meta_description.replace("\n",'')

    tutorial_name = ""

    config = dict(
        tutorial_name=tutorial_name,
        tags=dict(title=title, meta_description=meta_description)
    )
    return config

# Strip all attributes, jquery script and <body></body> from body
def strip_body(body):
    for tag in body():
        for attribute in ["class", "id", "name", "style"]:
            del tag[attribute]
    Script = body.findAll('script')
    for script in Script:
        script.extract()
    body = body.prettify().encode('utf8')
    body = body.replace('<body>','')
    body = body.replace('</body>','')
    return body

# -------------------------------------------------------------------------------

# Make directory tree
def make_tree(tree_segments):
    tree = os.path.join(*tree_segments)
    if not os.path.exists(tree):
        status(("[{}]".format(NAME), '... making', tree))
        os.makedirs(tree)
    else:
        status(("[{}]".format(NAME), '...', tree, 'already exists OK'))
    return tree

# Overwrite tree leaf
def overwrite_leaves(tree, leaves):
    for leaf in leaves:
        path_leaf = os.path.join(tree, leaf[1])
        status(('... writing in', path_leaf))
        with open(path_leaf, 'wb') as f:
            if leaf[1].endswith('.json'):
                json.dump(leaf[0], f, indent=4)
                f.write("\n")
            else:
                f.write(str(leaf[0]))
    return

# Copy leaves to tree
def copy_leaves(tree, paths_leaf):
    for path_leaf in paths_leaf:
        shutil.copy(path_leaf, tree)
    return

# -------------------------------------------------------------------------------

def main():

    folders = get_args()

    for folder in folders:

        paths_html = get_paths_html(folder)

        translate_static = translate.get_translate_static(folder)
        translate_filename_url = translate.get_translate_filename_url(folder)

        # (1) Make body.html and config.json for each html file 
        for path_html in paths_html:

            file_html = os.path.split(path_html)[1]

            if file_html not in translate_filename_url.keys():
                print (
                    '** {} not part of {}/translate_filename_url.json **\n'
                    '** please fill it in **'
                ).format(file_html,folder)
                sys.exit(0)
            else:
                file_html_url = translate_filename_url[file_html]
            
            # Get published tree for this html file
            tree_includes= make_tree([folder,'published','includes',file_html_url])
            
            # Get soup and translate its 'href' and 'src' 
            soup = get_soup(path_html)
            soup, paths_image = translate.translate(soup,folder,file_html_url,translate_static,translate_filename_url)

            # Split <body> and <head>, get config info
            body, head = get_body_head(soup) 
            config = get_config(head, path_html, tree_includes)

            # Strip <body> tags and all class attributes
            body = strip_body(body)

            # Overwrite body.html, head.txt and config.json leaves
            overwrite_leaves(tree_includes,[(body,'body.html')])
            #overwrite_leaves(tree_includes,[(body,'body.html'),(config,'config.json')])

            # (2) Copy images in the appropriate published/ subdirectories
            tree_images = make_tree([folder,'published','static','images',file_html_url])
            copy_leaves(tree_images,paths_image)

        # (3) Make folder-wide urls and sitemaps files
        make_urls.make_urls(folder,translate_filename_url)
        make_sitemaps.make_sitemaps(folder,translate_filename_url)

if __name__ == "__main__":
    main()
