from bs4 import BeautifulSoup

import sys
import status

# -------------------------------------------------------------------------------
#
# Script that un-minify Google docs outputs (not part of $ make publish)
#
# -------------------------------------------------------------------------------

NAME = "unminify_raw"  # name of this module

# -------------------------------------------------------------------------------


# Get input arguments
def get_args():
    _args = sys.argv[1:]
    if not _args:
        print (
            "[{NAME}]\n\n"
            "Usage:\n"
            "python {NAME}.py path/to/file\n"
            "python {NAME}.py path/to/file1 path/to/file2 "
            "... path/to/fileN\n"
        ).format(NAME=NAME)
        status.stop(NAME)
    return _args


# Get HTML soup from HTML file path
def get_soup(path_raw):
    with open(path_raw, "r") as f:
        status.log(NAME, ("Opening", path_raw))
        return BeautifulSoup(f)


# Prettify soup
def prettify(soup):
    soup = soup.prettify().encode('utf8')
    return soup


# Overwrite raw file
def overwrite(path_raw, soup):
    with open(path_raw, 'wb') as f:
        f.write(str(soup))

# -------------------------------------------------------------------------------


def main():
    paths_raw = get_args()
    for path_raw in paths_raw:
        soup = get_soup(path_raw)
        soup = prettify(soup)
        overwrite(path_raw, soup)

if __name__ == "__main__":
    main()
