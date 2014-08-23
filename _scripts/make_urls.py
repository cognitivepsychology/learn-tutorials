import json
import sys
import os

# -------------------------------------------------------------------------------
# 
# Makes a django urls file containing all the patterns for a given folder
#
# -------------------------------------------------------------------------------

NAME="make_urls"  # name of this module

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
    for tutorial in tutorials:  # TODO generalize
        urls += [r'(?P<excel_tutorial>{})/$'.format(tutorial)]
    return urls

# Generate rls.py file
# See streambed/shelly/learn/ for more info
def get_urls_py(urls):
    urls_py = (
        "from django.conf.urls import patterns, url\n\n"
        "import learn.views\n\n"
        "urlpatterns = patterns(\n"
        "   '',\n"
    )
    for url in urls:        # TODO generalize!
        urls_py += '    url("'+url+'", learn.views.excel_tutorials_template)'
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
