import json
import os

import status

# -------------------------------------------------------------------------------
# 
# Makes a django urls file containing all the redirect patterns 
# for a given folder
#
# -------------------------------------------------------------------------------

NAME="make_redirects"  # name of this module
tab = "    "           # tab in space

# Get redirects patterns
def get_redirects(translate_redirects):
    redirects = []
    for current, olds in translate_redirects.items():
        for old in olds:
            redirects += [(
                "r'^{old}/$',\n{tab}{tab}"
                "RedirectView.as_view(\n{tab}{tab}{tab}"
                "url='/{current}/',\n{tab}{tab}{tab}"
                "permanent=True)"
            ).format(old=old, current=current, tab=tab)]
    return redirects

# Generate redirects.py file
# See streambed/shelly/learn/ for more info
def get_redirects_py(redirects):
    redirects_py = (
        "from django.conf.urls import patterns, url\n"
        "from django.views.generic import RedirectView\n\n"
        "import learn.views\n\n\n"
        "urlpatterns = patterns(\n"
        "{tab}'',\n"
    ).format(tab=tab)
    for redirect in redirects: 
        redirects_py += (
            "{tab}url("+redirect+")"
        ).format(tab=tab)
        if redirect != redirects[-1]:
            redirects_py += ",\n"
    redirects_py += "\n)\n"
    return redirects_py

# Overwrite redirects.py
def overwrite_redirects(folder, redirects_py):
    f_redirects = "{}/published/redirects.py".format(folder)
    with open(f_redirects, "w") as f:
        status.log(NAME,('Writes in', f_redirects))
        f.write(redirects_py)
    return

# -------------------------------------------------------------------------------

# Make and overwrite redirects.py file (if redirects are presents)
def make_redirects(folder, translate_redirects):
    redirects = get_redirects(translate_redirects)
    redirects_py = get_redirects_py(redirects)
    overwrite_redirects(folder, redirects_py)

