import json
import sys
import os

# -------------------------------------------------------------------------------
# 
# Makes a django urls file containing all the sitemaps items for a given folder
#
# -------------------------------------------------------------------------------

NAME="make_sitemaps"  # name of this module

# Shortcut to print status along with the name of the script
def status(s):
    S = str(("[{}]".format(NAME), s))
    with open('publish.log', 'a') as f:
        f.write(S+"\n")
    return

# Get sitemaps items
def get_items(folder,translate_filename_url):
    tutorials = translate_filename_url.values()
    locations = []
    lmfiles = []
    for tutorial in tutorials:
        locations += ["'/{}/'".format(tutorial)]
        lmfiles += [("os.path.join("
            "settings.TOP_DIR,"
            "'shelly',"
            "'templates',"
            "'learn',"
            "'includes',"
            "'{folder}',"
            "'{tutorial}',"
            "'body.html')"
        ).format(folder=folder,tutorial=tutorial)]
    return locations, lmfiles

# Generate sitemaps.py file
# See streambed/shelly/learn/ for more info
def get_sitemaps_py(locations, lmfiles):
    sitemaps_py = (
        "import os\n\n"
        "from django.conf import settings\n\n"
        "def items():\n"
        "    items = [\n"
    )
    for location, lmfile in zip(locations,lmfiles):
        sitemaps_py += (
        "        dict(\n"
        "            location={location},\n"
        "            lmfile={lmfile},\n"
        "            priority=0.5\n"
        "        )"
        ).format(location=location,lmfile=lmfile)
        if location != locations[-1]:
            sitemaps_py += ",\n"
    sitemaps_py += (
        "\n    ]"
        "\n    return items"
        "\n"
    )
    return sitemaps_py

# Overwrite sitemaps.py
def overwrite_sitemaps(folder,sitemaps_py):
    f_urls = "{}/published/sitemaps.py".format(folder)
    with open(f_urls, "w") as f:
        f.write(sitemaps_py)
        status(('... writes in', f_urls))
    return

# -------------------------------------------------------------------------------

def make_sitemaps(folder,translate_filename_url):
    locations, lmfiles = get_items(folder,translate_filename_url)
    sitemaps_py = get_sitemaps_py(locations, lmfiles)
    overwrite_sitemaps(folder,sitemaps_py)
