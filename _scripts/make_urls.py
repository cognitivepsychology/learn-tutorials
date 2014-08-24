import json
import sys
import os

# -------------------------------------------------------------------------------
# 
# Makes a django urls file containing all the patterns for a given folder
#
# -------------------------------------------------------------------------------

NAME="make_urls"  # name of this module

tab = "    "  # tab in space

# Shortcut to print status along with the name of the script
def status(s):
    S = str(("[{}]".format(NAME), s))
    with open('publish.log', 'a') as f:
        f.write(S+"\n")
    return

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
        status(('... writes in', f_urls))
        f.write(urls_py)
    return

# -------------------------------------------------------------------------------

def make_urls(folder, translate_filename_url):
    urls = get_urls(translate_filename_url)
    urls_py = get_urls_py(urls)
    overwrite_urls(folder,urls_py)
