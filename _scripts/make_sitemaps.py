import json
import os

import status

# -------------------------------------------------------------------------------
# 
# Makes a django urls file containing all the sitemaps items for a given folder
#
# -------------------------------------------------------------------------------

NAME="make_sitemaps" # name of this module
tab = "    "         # tab in space

# Get sitemaps items
def get_items(folder,translate_filename_url):
    tutorials = translate_filename_url.values()
    locations = []
    lmfiles = []
    for tutorial in tutorials:
        locations += ["'/{}/'".format(tutorial)]
        lmfiles += [("os.path.join(\n{tab}{tab}{tab}{tab}"
            "settings.TOP_DIR, "
            "'shelly',\n{tab}{tab}{tab}{tab}"
            "'templates', "
            "'learn', "
            "'includes',\n{tab}{tab}{tab}{tab}"
            "'{folder}',\n{tab}{tab}{tab}{tab}"
            "'{tutorial}',\n{tab}{tab}{tab}{tab}"
            "'body.html')"
        ).format(folder=folder,tutorial=tutorial,tab=tab)]
    return locations, lmfiles

# Generate sitemaps.py file
# See streambed/shelly/learn/ for more info
def get_sitemaps_py(locations, lmfiles):
    sitemaps_py = (
        "import os\n\n"
        "from django.conf import settings\n\n\n"
        "def items():\n"
        "{tab}items = [\n"
    ).format(tab=tab)
    for location, lmfile in zip(locations,lmfiles):
        sitemaps_py += (
        "{tab}{tab}dict(\n"
        "{tab}{tab}{tab}location={location},\n"
        "{tab}{tab}{tab}lmfile={lmfile},\n"
        "{tab}{tab}{tab}priority=0.5\n"
        "{tab}{tab})"
        ).format(location=location,lmfile=lmfile,tab=tab)
        if location != locations[-1]:
            sitemaps_py += ",\n"
    sitemaps_py += (
        "\n{tab}]"
        "\n{tab}return items"
        "\n"
    ).format(tab=tab)
    return sitemaps_py

# Overwrite sitemaps.py
def overwrite_sitemaps(folder,sitemaps_py):
    f_urls = "{}/published/sitemaps.py".format(folder)
    with open(f_urls, "w") as f:
        f.write(sitemaps_py)
        status.log(NAME,('Writes in', f_urls))
    return

# -------------------------------------------------------------------------------

def make_sitemaps(folder,translate_filename_url):
    locations, lmfiles = get_items(folder,translate_filename_url)
    sitemaps_py = get_sitemaps_py(locations, lmfiles)
    overwrite_sitemaps(folder,sitemaps_py)
