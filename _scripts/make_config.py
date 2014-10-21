import json
import os
import shutil

import status

# -------------------------------------------------------------------------------
#
# Make config.json file for each tutorial with meta info
#
# - config.tutorial_name : breadcrumb header label
# - config.banner_image : iframe url or static image file name for the banner
# - config.tags.title : page and meta title
# - config.tags.meta_description : meta description
#
# -------------------------------------------------------------------------------

NAME = "make_config"  # name of this script


# Get <title> from <head> (the default)
def get_config_title(head, flags):
    Title = head.findAll('title')
    if not len(Title):
        flags += ['no-title']
        title = ""
    elif len(Title) > 1:
        flags += ['multiple-titles']
        title = Title[-1].string.replace("\n", '')
    else:
        title = Title[0].string.replace("\n", '')
    return title, flags


# Get <meta name="description" > (the default)
def get_config_meta_description(head, flags):
    Meta = head.findAll('meta')
    Meta_description = [meta for meta in Meta
                        if (meta.has_attr('name') and
                            meta['name'] == "description")]
    if not len(Meta_description):
        flags += ['no-meta_description']
        meta_description = ""
    elif len(Meta_description) > 1:
        flags += ['multiple-meta_descriptions']
        meta_description = Meta_description[-1]['content'].replace("\n", '')
    else:
        meta_description = Meta_description[0]['content'].replace("\n", '')
    return meta_description, flags


# Check if config.json in tree was modified
def check_tree_config(tree, config, flags):
    try:
        path_config = os.path.join(tree, 'config.json')
        with open(path_config) as f:
            config_old = json.load(f)
        if config_old != config:
            config = config_old
            status.log(NAME, (
                "Not overwriting `{}`, as modifications "
                "from default were found"
            ).format(path_config))
        flags = ['show-config']
        if not config['tags']['title']:
            flags += ['no-title']
        if not config['tags']['meta_description']:
            flags += ['no-meta_description']
        if not config['tutorial_name']:
            flags += ['no-tutorial_name']
        if config['banner_image'] == "":
            flags += ['no-banner_image']
    except:
        pass
    return config, flags


# Check if banner image file in config.json exist in published/
def check_tree_banner_image(tree, config, flags):
    file_image = config['banner_image']
    if file_image:
        if file_image.endswith(('.png', 'jpeg', 'jpg', 'gif')):
            tree_image = tree.replace('includes', 'static/images')
            path_image = os.path.join(tree_image, file_image)
            if not os.path.isfile(path_image):
                flags += ['missing-banner_image']
    return flags


# Print important flags to screen
def print_flags(flags, config, path_html, tree):
    for flag in flags:
        if flag == 'show-config':
            status.log(NAME, (
                "{}/config.json ['tutorial_name']:\n\t'{}'"
            ).format(tree, config['tutorial_name']))
            status.log(NAME, (
                "{}/config.json ['banner_image']:\n\t'{}'"
            ).format(tree, config['banner_image']))
            status.log(NAME, (
                "{}/config.json ['tags']['title']:\n\t'{}'"
            ).format(tree, config['tags']['title']))
            status.log(NAME, (
                "{}/config.json ['tags']['meta_description']:\n\t'{}'"
            ).format(tree, config['tags']['meta_description']))
        elif flag == 'no-title':
            status.important(NAME, (
                "There is no <title>\nin `{}`.\n"
                "Please fill in\n`{}/config.json`"
                ).format(path_html, tree))
        elif flag == 'multiple-title':
            status.important(NAME, (
                "There is more than one <title>\nin `{}`.\n"
                "Picking the last one for\n`{}/config.json`"
            ).format(path_html, tree))
            status.log(NAME, (
                'With last <title> tag, set meta'
                'title to "{}"'
            ).format(config['tags']['title']))
        elif flag == 'no-meta_description':
            status.important(NAME, (
                "There is more than one <meta name='description'> in\n`{}`.\n"
                "Please fill in\n`{}/config.json`"
            ).format(path_html, tree))
        elif flag == 'multiple-meta_descriptions':
            status.important(NAME, (
                "There is more than one <meta name='description'> in\n`{}`.\n"
                "Picking the last one for\n`{}/config.json`"
            ).format(path_html, tree))
            status.log(NAME, (
                'With last <meta name="description"> tag, '
                'set meta description to "{}"'
            ).format(config['tags']['meta_description']))
        elif flag == 'no-tutorial_name':
            status.important(NAME, (
                "Please fill 'tutorial_name' in\n`{}/config.json`"
            ).format(tree))
        elif flag == 'no-banner_image':
            status.important(NAME, (
                "Please fill 'banner_image' in\n`{tree}/config.json`:\n"
                "- For an iframe: set 'banner_image' to the url\n"
                "- For a static image: set 'banner_image' "
                "to the image file name\n"
                "      AND copy the image to:\n"
                "      ``{tree_image}``/\n"
                "- For no banner image, set 'banner_image' to false"
            ).format(tree=tree,
                     tree_image=tree.replace('includes', 'static/images')))
        elif flag == 'missing-banner_image':
            status.important(NAME, (
                "The static banner image linked to 'banner_image'  "
                "({image}) in\n  "
                "`{tree}/config.json`\n  "
                "is not found in\n  "
                "`{tree_image}`/\n  "
                "Please copy it over."
            ).format(image=config['banner_image'], tree=tree,
                     tree_image=tree.replace('includes', 'static/images')))
        else:
            status.log(NAME, (
                'With <title> tag, set meta title to:\n\t"{}"'
            ).format(config['tags']['title']))
            status.log(NAME, (
                'With <meta name="description"> tag, '
                'set meta description to:\n\t"{}"'
            ).format(config['tags']['meta_description']))
    return

# -------------------------------------------------------------------------------


# Make config dictionaries (don't print it here!)
def make_config(head, path_html, tree):
    flags = []
    title, flags = get_config_title(head, flags)
    meta_description, flags = get_config_meta_description(head, flags)
    # make default config dict
    config = dict(
        tutorial_name='',
        banner_image='',   # N.B.
        tags=dict(
            title=title,
            meta_description=meta_description
        )
    )
    config, flags = check_tree_config(tree, config, flags)
    flag = check_tree_banner_image(tree, config, flags)
    print_flags(flags, config, path_html, tree)
    return config
