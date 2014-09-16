from bs4 import BeautifulSoup
import json
import sys
import os
import shutil

import status
import translate 
import make_config
import make_urls
import make_redirects
import make_sitemaps

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

# -------------------------------------------------------------------------------

# Get input arguments 
def get_args():
    _args = sys.argv[1:]
    if not _args:
        print (
            "[{NAME}]\n\n"
            "Usage:\n"
            "python {NAME}.py folder\n"
            "python {NAME}.py path/to/folder\n"
            "python {NAME}.py folder1 folder2 ... folderN\n"
        ).format(NAME=NAME)
        status.stop(NAME)
    elif not all(os.path.isdir(_arg) for _arg in _args):
        dirs_available = [i for i in os.listdir(os.getcwd()) 
                          if (os.path.isdir(i) and 
                              not i.startswith('.') and 
                              not i.startswith('_'))]
        status.important(NAME,(
            'Arguments must be directories from the repo root.\n\n'
            'The available directories are:\n'
            '  {}'.format('\n  '.join(dirs_available))
        ))
        status.stop(NAME)
    else:
        args = [os.path.dirname(_arg+'/') for _arg in _args]
        return args

# -------------------------------------------------------------------------------

# Get list of HTML files in folder
def get_paths_html(folder):
    paths_html = []
    folder_raw = os.path.join(folder,'raw')
    if not os.path.isdir(folder_raw):
        status.important(NAME,(
            'Folder `{}` must contain a `raw/` subfolder'.format(folder)
        ))
        status.stop(NAME)
    for path_folder, subfolders, files in os.walk(folder_raw):
        for subfolder in subfolders:
            if subfolder == '__MACOSX':
                path_MACOSX = os.path.join(path_folder, subfolder)
                status.important(NAME,(
                    "Removing `{}`\n - Not needed (this is no big deal)"
                ).format(path_MACOSX))
                shutil.rmtree(path_MACOSX)
    for path_folder, subfolders, files in os.walk(folder_raw):
        for f in files:
            if f.endswith('.html'):
                path_html = os.path.join(path_folder,f)
                paths_html.append(path_html)
    if not paths_html:
        status.important(NAME,(
            'No .html files located inside `{}`'.format(folder)
        ))
        status.stop(NAME)
    return paths_html

# Check if paths are in translate_filename_url (update if necessary)
def check_translate(folder, paths_html, translate_filename_url):
    files_html_translate = translate_filename_url.keys()
    files_html = [os.path.split(path_html)[1] for path_html in paths_html]
    if set(files_html_translate) == set(files_html):
        return paths_html
    else:
        if len(files_html_translate) < len(files_html):
            diff = list(set(files_html) - set(files_html_translate))
            to_be = 'was' if len(diff)==1 else 'were'
            to_have = 'has' if len(diff)==1 else 'have'
            status.important(NAME,(
                "File(s): \n\n {diff}\n\n"
                "{to_be} found from `{folder}/raw/` but {to_have} "
                "no correspondence\n"
                "in `{folder}/translate_filename_url.json`.\n\n"
                "Note that files not listed in "
                "`{folder}/translate_filename_url.json`\n"
                "will NOT be published"
            ).format(diff='\n'.join(diff),folder=folder,
                     to_be=to_be,to_have=to_have))
            return [path_html for path_html in paths_html
                   if (path_html in files_html)]
        else:
            diff = list(set(files_html_translate) - set(files_html))
            to_be = 'is' if len(diff)==1 else 'are'
            to_have = 'has' if len(diff)==1 else 'have'
            status.important(NAME,(
                "File(s): \n\n {diff}\n\n"
                "{to_be} listed in "
                "`{folder}/translate_filename_url.json` but {to_have} "
                "no correspondence\n"
                "in `{folder}/raw/`.\n\n"
                "Note that files not found in "
                "`{folder}/raw` CANNOT be published"
            ).format(diff='\n'.join(diff),folder=folder,
                     to_be=to_be,to_have=to_have))
            status.stop(NAME)

# Check if there are directories to redirect, copy them over if so.
def check_redirects(folder, translate_redirects):
    paths_subdirs = [
        os.path.join(folder,'published','includes'),
        os.path.join(folder,'published','static','images')
    ]
    for path_subdirs in paths_subdirs:
        for new, olds in translate_redirects.items():
            path_subdir_new = os.path.join(path_subdirs, new) + '/'
            path_subdir_old = os.path.join(path_subdirs, olds[-1]) + '/'
            if (os.path.isdir(path_subdir_old) and 
                not os.path.isdir(path_subdir_new)):
                status.log(NAME,('Making', path_subdir_new))
                os.makedirs(path_subdir_new)
                for item in os.listdir(path_subdir_old):
                    path_item = os.path.join(path_subdir_old, item)
                    shutil.copy(path_item, path_subdir_new)
                    status.log(NAME,(
                        'Copying {} to {}'
                    ).format(path_item, path_subdir_new))
                shutil.rmtree(path_subdir_old)
                status.log(NAME,(
                    'Removing directory {}'
                ).format(path_subdir_old))
    return

# Check if {folder}/published/ subdirectories corresp. to translate_filename_url
def check_published_subdirectories(folder, translate_filename_url):
    path_includes = os.path.join(folder, 'published', 'includes')
    path_images = os.path.join(folder, 'published', 'static', 'images')
    try:
        subdirectories_includes = os.listdir(path_includes)
    except:
        subdirectories_includes = []
    try:
        subdirectories_images = os.listdir(path_images)
    except:
        subdirectories_images = []
    dirs_url = translate_filename_url.values()
    if set(subdirectories_includes) != set(subdirectories_images):
        status.important(NAME,(
            "Directories `{folder}/published/includes/`\n"
            "and `{folder}/published/static/images/`\n"
            "do not have to same subdirectories.\n\n"
            "Please investigate (that's a weird one)."
        ).format(folder=folder))
    elif len(subdirectories_includes) > len(dirs_url): 
        diff = list(set(subdirectories_includes) - set(dirs_url))
        to_be = 'is' if len(diff)==1 else 'are'
        status.important(NAME,(
            "Subdirectory(ies):\n\n {diff}\n\n"
            "from `{folder}/published/includes/`\n"
            "and `{folder}/published/static/images/`\n"
            "{to_be} not listed in `{folder}/translate_filename_url.json`.\n\n"
            "Please investigate:\n\n"
            "  - Did you change a url in {folder}/translate_filename_url.json\n"
            "    not meant to be redirected (e.g. you fixed a typo)?\n\n"
            "    Then, please remove\n"
            "    {folder}/published/includes/{diff}/ and\n"
            "    {folder}/published/static/images/{diff}/\n\n"
            "  - If you removed a url in {folder}/translate_filename_url.json\n"
            "    to not publish some raw/ HTML file just yet,\n"
            "    ignore this warning."
            ).format(diff='\n'.join(diff),folder=folder,to_be=to_be))
    elif not len(subdirectories_includes) <= len(dirs_url):
        pass
    return

# -------------------------------------------------------------------------------

# Get HTML soup from HTML file path
def get_soup(path_html):
    with open(path_html, "r") as f:
        status.log(NAME,("Opening", path_html))
        return BeautifulSoup(f)

# Get HTML <body> and <head>
def get_body_head(soup):
    status.log(NAME,'Grabs <body> and <head>')
    return soup.body, soup.head

# Strip all attributes, <script></script> and <body></body> from body
def strip_body(body):
    for attribute in ["class", "id", "name", "style"]:
        del body[attribute]
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

#    plotly_classes = [  # TODO generalize!
#        ['heading'], ["section__inner"], ['link--bold', 'link--impt'], 
#        ['beta', 'push--ends'],  
#        ['media', 'push--bottom'], ['media__body'], ["media__img--rev"],
#        ['img-with-caption'], ['img-caption'], ['img--border push--bottom']
#    ]
# -------------------------------------------------------------------------------

# Make directory tree
def make_tree(tree_segments):
    tree = os.path.join(*tree_segments)
    if not os.path.exists(tree):
        status.log(NAME,('Making', tree))
        os.makedirs(tree)
    else:
        status.log(NAME,('Tree', tree, 'already exists OK'))
    return tree

# Overwrite tree leaf
def overwrite_leaves(tree, leaves):
    for leaf in leaves:
        path_leaf = os.path.join(tree, leaf[1])
        status.log(NAME,('Writing in', path_leaf))
        with open(path_leaf, 'wb') as f:
            if leaf[1].endswith('.json'):
                json.dump(leaf[0], f, indent=4)
                f.write("\n")
            else:
                f.write(str(leaf[0]))
    return

# Copy leaves to tree
def copy_leaves(tree, paths_leaf):
    status.log(NAME,('Copying leaves to', tree))
    for path_leaf in paths_leaf:
        shutil.copy(path_leaf, tree)
    return

# -------------------------------------------------------------------------------

def main():

    folders = get_args()

    for folder in folders:

        # Get translate info for folder-specific files
        translate_static = translate.get_translate_static(folder)
        translate_filename_url, translate_redirects = (
            translate.get_translate_filename_url(folder))

        # Get paths of all html files in {folder}/raw/
        paths_html = get_paths_html(folder)

        # Check if paths are in translate_filename_url (update if necessary)
        paths_html = check_translate(folder, paths_html, translate_filename_url)

        # Check if there are directories to redirect
        check_redirects(folder, translate_redirects)

        # Check if {folder}/published/* corresp. to translate_filename_url
        check_published_subdirectories(folder, translate_filename_url)

        # (1) Make body.html and config.json for each html file 
        for path_html in paths_html:

            # Get published files directory url (and name, they are the same!)
            file_html = os.path.split(path_html)[1]
            dir_url = translate_filename_url[file_html]
            
            # Get published tree for this html file
            tree_includes = make_tree([folder,'published','includes',dir_url])
            
            # Get soup and split <body> and <head>
            soup = get_soup(path_html)
            body, head = get_body_head(soup) 

            # Translate 'href' and 'src' in body 
            body, paths_image = translate.translate(body,path_html,dir_url,
                                                    translate_static,
                                                    translate_filename_url)

            # Get config info from head
            config = make_config.make_config(head, path_html, tree_includes)

            # Strip <body> tags and all class attributes
            body = strip_body(body)

            # Overwrite body.html and config.json leaves
            overwrite_leaves(tree_includes,
                             [(body,'body.html'),(config,'config.json')])

            # (2) Copy images in the appropriate published/ subdirectories
            tree_images = make_tree([folder,'published','static','images',dir_url])
            copy_leaves(tree_images,paths_image)

            status.log(NAME,'---- done with `{}`\n'.format(dir_url))

        # (3) Make folder-wide urls, redirects and sitemaps files
        make_urls.make_urls(folder, translate_filename_url)
        make_redirects.make_redirects(folder, translate_redirects)
        make_sitemaps.make_sitemaps(folder, translate_filename_url)

if __name__ == "__main__":
    main()
