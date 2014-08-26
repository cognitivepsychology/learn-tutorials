import json
import os

import status

# -------------------------------------------------------------------------------
# 
# Makes a django urls file containing all the patterns for a given folder
#
# -------------------------------------------------------------------------------

NAME="make_urls"  # name of this module
tab = "    "      # tab in space

# Get urls patterns
def get_urls(translate_filename_url):
    tutorials = translate_filename_url.values()
    urls = []
    for tutorial in tutorials:  
        urls += [r'(?P<tutorial>{})/$'.format(tutorial)]
    return urls

# Generate urls.py file
# See streambed/shelly/learn/ for more info
def get_urls_py(urls):
    urls_py = (
        "from django.conf.urls import patterns, url\n\n"
        "import learn.views\n\n\n"
        "urlpatterns = patterns(\n"
        "{tab}'',\n"
    ).format(tab=tab)
    for url in urls: # TODO generalize views!
        urls_py += (
            '{tab}url("'+url+'",\n'
            '{tab}{tab}learn.views.excel_tutorials_template)'
        ).format(tab=tab)
        if url != urls[-1]:
            urls_py += ",\n"
    urls_py += "\n)\n"
    return urls_py

# Overwrite urls.py
def overwrite_urls(folder,urls_py):
    f_urls = "{}/published/urls.py".format(folder)
    with open(f_urls, "w") as f:
        status.log(NAME,('Writes in', f_urls))
        f.write(urls_py)
    return

# -------------------------------------------------------------------------------

# Make and overwrite urls.py file
def make_urls(folder, translate_filename_url):
    urls = get_urls(translate_filename_url)
    urls_py = get_urls_py(urls)
    overwrite_urls(folder,urls_py)
