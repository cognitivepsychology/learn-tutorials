import json
import os
import shutil

import status

# -------------------------------------------------------------------------------
# 
# Make config.json file for each tutorial with meta info
#
# - config.userguide_chapter_name : breadcrumb header label
# - config.tags.title : page title
# - config.tags.meta_description : meta description
#
# -------------------------------------------------------------------------------

NAME="make_config"  # name of this script


# Get <title> from <head>
def get_config_title(head, flags):
    Title = head.findAll('title')
    if not len(Title):
        flags += ['no-title']
        title = ""
    elif len(Title)>1:
        flags += ['multiple-titles']
        title = Title[-1].string.replace("\n",'')
    else:
        title = Title[0].string.replace("\n",'')
    return title, flags

# Get <meta name="description" > 
def get_config_meta_description(head, flags):
    Meta = head.findAll('meta')
    Meta_description = [meta for meta in Meta 
                        if (meta.has_attr('name') and 
                            meta['name']=="description")]
    if not len(Meta_description):
        flags += ['no-meta_description']
        meta_description = ""
    elif len(Meta_description)>1:
        flags += ['multiple-meta_descriptions']
        meta_description = Meta_description[-1]['content'].replace("\n",'')
    else:
        meta_description = Meta_description[0]['content'].replace("\n",'')
    return meta_description, flags

# Get tutorial name (for breadcrumb) 
def get_config_tutorial_name(head, flags):  #TODO generalize!
    tutorial_name = ''               
    flags += ['no-tutorial_name']
    return tutorial_name, flags

# Check if config.json in tree was modified
def check_tree_config(tree, config, flags):
    try:
        path_config = os.path.join(tree,'config.json')
        with open(path_config) as f:
            config_old = json.load(f)
        if config_old != config:
            config = config_old
            status.log(NAME,(
                "Not overwriting `{}`, as modifications were found"
            ).format(path_config))
        flags = ['show-config']
        if not config['tags']['title']: flags += ['no-title'] 
        if not config['tags']['meta_description']: flags += ['no-meta_description'] 
        if not config['tutorial_name']: flags += ['no-tutorial_name'] 
    except:
        pass
    return config, flags

# Print important flags to screen
def print_flags(flags, config, path_html, tree):
    for flag in flags:
        if flag=='show-config':
            status.log(NAME,(
                "{}/config.json ['tutorial_name']:\n\t'{}'"
            ).format(tree,config['tutorial_name']))
            status.log(NAME,(
                "{}/config.json ['tags']['title']:\n\t'{}'"
            ).format(tree,config['tags']['title']))
            status.log(NAME,(
                "{}/config.json ['tags']['meta_description']:\n\t'{}'"
            ).format(tree,config['tags']['meta_description']))
        elif flag=='no-title': 
            status.important(NAME,(
                "There is no <title>\nin `{}`.\n"
                "Please fill in\n`{}/config.json`"
                ).format(path_html,tree))
        elif flag=='multiple-title':
            status.important(NAME,(
                "There is more than one <title>\nin `{}`.\n"
                "Picking the last one for\n`{}/config.json`"
            ).format(path_html,tree))
            status.log(NAME,(
                'With last <title> tag, set meta'
                'title to "{}"'
           ).format(title))
        elif flag=='no-meta_description':
            status.important(NAME,(
                "There is more than one <meta name='description'> in\n`{}`.\n"
                "Please fill in\n`{}/config.json`"
            ).format(path_html,tree))
        elif flag=='multiple-meta_descriptions':
            status.important(NAME,(
                "There is more than one <meta name='description'> in\n`{}`.\n"
                "Picking the last one for\n`{}/config.json`"
            ).format(path_html,tree))
            status.log(NAME,(
                'With last <meta name="description"> tag, '
                'set meta description to "{}"'
            ).format(meta_description))
        elif flag=='no-tutorial_name':
            status.important(NAME,(
                "Please fill 'tutorial_name' in\n`{}/config.json`"
            ).format(tree))
        else:
            status.log(NAME,(
                'With <title> tag, set meta title to:\n\t"{}"'
            ).format(title))
            status.log(NAME,(
                'With <meta name="description"> tag, set meta description to:\n\t"{}"'
           ).format(meta_description))
    return

# -------------------------------------------------------------------------------

# Make config dictionaries (don't print it here!)
def make_config(head, path_html, tree):
    flags = []
    title, flags = get_config_title(head, flags)
    meta_description, flags = get_config_meta_description(head, flags)
    tutorial_name, flags  = get_config_tutorial_name(head, flags)
    config = dict(
        tutorial_name=tutorial_name,
        tags=dict(title=title, meta_description=meta_description)
    )
    config, flags = check_tree_config(tree, config, flags)
    print_flags(flags, config, path_html, tree)
    return config
