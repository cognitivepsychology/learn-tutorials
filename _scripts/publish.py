from bs4 import BeautifulSoup
import json
import sys
import os
import shutil

import translate 
import make_urls
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

# Shortcut to print status along with the name of the script
def status(s):
    S = str(("[{}]".format(NAME), s))
    with open('publish.log', 'a') as f:
        f.write(S+"\n")
    return

# Print important message to screen
def important(s):
    print "[{NAME}] ** IMPORTANT!\n\n{s}\n**\n".format(NAME=NAME,s=s)
    return

# Stop execution
def stop():
    important("Stopping execution here!")
    sys.exit(0)
 
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
        stop()
    elif not all(os.path.isdir(arg) for arg in args):
        important('Arguments must be directories')
        stop()
    else:
        return args

# -------------------------------------------------------------------------------

# Get list of HTML files in folder
def get_paths_html(folder):
    paths_html = []
    folder_raw = os.path.join(folder,'raw')
    if not os.path.isdir(folder_raw):
        important('Folder `{}` must contain a `raw/` subfolder'.format(folder))
        stop()
    for path_folder, subfolders, files in os.walk(folder_raw):
        for f in files:
            if f.endswith('.html'):
                path_html = os.path.join(path_folder,f)
                paths_html.append(path_html)
    if not paths_html:
        important('No .html files located inside `{}`'.format(folder))
        stop()
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
            important((
                "File(s): \n\n {diff}\n\n"
                "{to_be} found from `{folder}/raw/` but {to_have} "
                "no correspondence\n"
                "in `{folder}/translate_filename_url.json`.\n\n"
                "Note that files not listed in "
                "`{folder}/translate_filename_url.json`\n"
                "will NOT be published"
            ).format(diff='\n'.join(diff),folder=folder,
                     to_be=to_be,to_have=to_have))
        else:
            diff = list(set(files_html_translate) - set(files_html))
            to_be = 'is' if len(diff)==1 else 'are'
            to_have = 'has' if len(diff)==1 else 'have'
            important((
                "File(s): \n\n {diff}\n\n"
                "{to_be} listed in "
                "`{folder}/translate_filename_url.json` but {to_have} "
                "no correspondence\n"
                "in `{folder}/raw/`.\n\n"
                "Note that files not found in "
                "`{folder}/raw` CANNOT be published"
            ).format(diff='\n'.join(diff),folder=folder,
                     to_be=to_be,to_have=to_have))
        return [path_html 
                for i,path_html in enumerate(paths_html) 
                if files_html[i] in files_html_translate]

# Check if {folder}/published/ subdirectories corresp. to translate_filename_url
def check_published_subdirectories(folder, translate_filename_url):
    path_includes = os.path.join(folder,'published','includes')
    path_images = os.path.join(folder,'published','static','images')
    try:
        subdirectories_includes = os.listdir(path_includes)
    except:
        subdirectories_includes = []
    try:
        subdirectories_images = os.listdir(path_images)
    except:
        subdirectories_images = []
    dirs_url = translate_filename_url.values()
    if subdirectories_includes != subdirectories_images:
        important((
            "Directories `{}/published/includes/`\n"
            "and `{}/published/images/`\n"
            "do not have to same subdirectories.\n"
            "Please investigate."
        ).format(folder))
    elif not len(subdirectories_includes):
        pass
    elif set(subdirectories_includes) != set(dirs_url):
        diff = list(set(subdirectories_includes) - set(dirs_url))
        to_be = 'is' if len(diff)==1 else 'are'
        important((
            "Subdirectory(ies):\n\n {diff}\n\n"
            "from `{folder}/published/includes/`\n"
            "and `{folder}/published/images/`\n"
            "{to_be} not listed in `{folder}/translate_filename_url.json`.\n"
            "Please investigate."
            ).format(diff='\n'.join(diff),folder=folder,to_be=to_be))
    return

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

# Get <title> from <head>
def get_config_title(head, flags):
    Title = head.findAll('title')
    if not len(Title):
        flags += ['no-title']
        title = ""
    elif len(Title)>1:
        flags += ['multiple-titles']
        title = Title[-1].string
        status('strip <title> tags from <head>')
        for _title in Title:
            _title.extract()
    else:
        title = Title[0].string
        status('strip <title> tag from <head>')
        Title[0].extract()
    title = title.replace("\n",'')
    return title, flags

# Get <meta name="description" > 
def get_meta_description(head, flags):
    Meta = head.findAll('meta')
    Meta_description = [meta for meta in Meta 
                        if (meta.has_attr('name') and 
                            meta['name']=="description")]
    if not len(Meta_description):
        flags += ['no-meta_description']
        meta_description = ""
    elif len(Meta_description)>1:
        flags += ['multiple-meta_descriptions']
        meta_description = Meta_description[-1]['content']
        status('strip <meta name="description"> tags from <head>')
        for _meta_description in Meta_description:
            _meta_description.extract()
    else:
        meta_description = Meta_description[0]['content']
        status('strip <meta name="description"> tag from <head>')
        Meta_description[0].extract()
    meta_description = meta_description.replace("\n",'')
    return meta_description, flags

# Get tutorial name (for breadcrumb) 
def get_tutorial_name(head, flags):  #TODO generalize!
    tutorial_name = ''               
    flags += ['no-tutorial_name']
    return tutorial_name, flags

# Get <title> and <meta name="description" >, print relevant info
def get_config(head, path_html, tree):
    flags = []
    title, flags = get_config_title(head, flags)
    meta_description, flags = get_meta_description(head, flags)
    tutorial_name, flags  = get_tutorial_name(head, flags)
    config = dict(
        tutorial_name=tutorial_name,
        tags=dict(title=title, meta_description=meta_description)
    )
    try:
        flags = []
        path_config = os.path.join(tree,'config.json')
        with open(path_config) as f:
            config_old = json.load(f)
        if config_old != config:
            config = config_old
            status((
                "Not overwriting\n`{}`,\nas modifications were found"
            ).format(path_config))
        if not config['tags']['title']: flag += ['no-title'] 
        if not config['tags']['meta_description']: flag += ['no-meta_description'] 
        if not config['tutorial_name']: flag += ['no-tutorial_name'] 
    except:
        pass
    for flag in flags:
        if flag=='no-title': 
            important((
                "There is no <title> in {}.\n"
                "Please fill in `{}`/config.json"
                ).format(path_html,tree))
        elif flag=='multiple-title':
            important((
                "There is more than one <title> in {}.\n"
                "Picking the last one for `{}`/config.json"
            ).format(path_html,tree))
        elif flag=='no-meta_description':
            important((
                "There is more than one <meta name='description'> in `{}`.\n"
                "Please fill in `{}`/config.json"
            ).format(path_html,tree))
        elif flag=='multiple-meta_descriptions':
            important((
                "There is more than one <meta name='description'> in {}.\n"
                "Picking the last one for `{}`/config.json"
            ).format(path_html,tree))
        elif flag=='no-tutorial_name':
            important((
                "Please fill 'tutorial_name' in `{}`/config.json"
            ).format(tree))
    return config

# Strip all attributes, jquery script and <body></body> from body
def strip_body(body):
    for tag in body():
        for attribute in ["class", "id", "name", "style"]:
            del tag[attribute]
    Script = body.findAll('script')
    for script in Script:
        script.extract()

    # only for excel_tutorials/
    try:
        iframe = body.findAll('iframe')[0]
        iframe_str = str(iframe)
        iframe_soup = BeautifulSoup(iframe_str)
        wrapper = iframe_soup.new_tag("div", **{'class':'text--center'})
        iframe_soup.body.wrap(wrapper)
        iframe_new = iframe_soup.encode('utf8')
        iframe_new = iframe_new.replace('<html>','').replace('</html>','')
        iframe_new = iframe_new.replace('<body>','').replace('</body>','')
        _body = body.encode('utf8')
        _body = _body.replace(iframe_str,iframe_new)
        body = BeautifulSoup(_body).body
    except:
        pass

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

        # Get translate info for folder-specific files
        translate_static = translate.get_translate_static(folder)
        translate_filename_url = translate.get_translate_filename_url(folder)

        # Get paths of all html files in {folder}/raw/
        paths_html = get_paths_html(folder)

        # Check if paths are in translate_filename_url (update if necessary)
        paths_html = check_translate(folder, paths_html, translate_filename_url)

        # Check if {folder}/published/* corresp. to translate_filename_url
        check_published_subdirectories(folder, translate_filename_url)

        # (1) Make body.html and config.json for each html file 
        for path_html in paths_html:

            # Get published files directory url (and name, they are the same!)
            file_html = os.path.split(path_html)[1]
            dir_url = translate_filename_url[file_html]
            
            # Get published tree for this html file
            tree_includes = make_tree([folder,'published','includes',dir_url])
            
            # Get soup and translate its 'href' and 'src' 
            soup = get_soup(path_html)
            soup, paths_image = translate.translate(soup,path_html,dir_url,
                                                    translate_static,
                                                    translate_filename_url)

            # Split <body> and <head>, get config info
            body, head = get_body_head(soup) 
            config = get_config(head, path_html, tree_includes)

            # Strip <body> tags and all class attributes
            body = strip_body(body)

            # Overwrite body.html and config.json leaves
            overwrite_leaves(tree_includes,
                             [(body,'body.html'),(config,'config.json')])

            # (2) Copy images in the appropriate published/ subdirectories
            tree_images = make_tree([folder,'published','static','images',dir_url])
            copy_leaves(tree_images,paths_image)

        # (3) Make folder-wide urls and sitemaps files
        make_urls.make_urls(folder,translate_filename_url)
        make_sitemaps.make_sitemaps(folder,translate_filename_url)

if __name__ == "__main__":
    main()
