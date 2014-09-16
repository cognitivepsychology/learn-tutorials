# How to contribute

*Please don't be scared by the length of this document, most of the steps
are git commands.*


### Before all cases

#### 0. What you need to install 

- [IPython](http://ipython.org/install.html) (easier with pip)

```
$ pip install ipython[all]
```

- [BeautifulSoup](http://www.pythonforbeginners.com/python-on-the-web/web-scraping-with-beautifulsoup/)

#### 1. Clone or pull `learn-tutorials/`

From the directory of your choice, clone `learn-tutorials/` by running:

```
$ git clone https://github.com/plotly/learn-tutorials.git
```

**OR** 

If you already have a copy of `learn-tutorials/` on your machine, then pull
in the latest version by running from `learn-tutorials/` with

```
$ git checkout master
$ git pull origin master
```

#### 2. Make a new branch in `learn-tutorials/`

> For completeness, call this new branch "my-branch".

Form `learn-tutorials/`, run

```
$ git branch my-branch
```

and then checkout to your new branch with

```
$ git checkout my-branch
```

#### 3. Go to

- [Case A: Update content of an existing page](#case-a-update-content-of-an-existing-page)
- [Case B: Update meta information of an existing page](#case-b-update-meta-information-of-an-existing-page)
- [Case C: Add a new tutorial page](#case-c-add-a-new-tutorial-page)
- [Case D: Modify the URL of an existing page](#case-d-modify-the-url-of-an-existing-page)

-------------------------------------------------------------------------------

### Case A: Update content of an existing page

#### A-0. Find corresponding *raw* HTML file

Each tutorial page has a corresponding *raw* (i.e. not-publishable) HTML file.
Raw HTML files are part of the output folder when exporting a Google document to
HTML. 

If you don't know which raw HTML file correspond to a given page, search through
each content directory's `translate_filename_url.json` file, where the name of
the raw HTML are listed on the left-hand column.

> For completeness, say we are updating the bar chart web app tutorial
 [page](https://plot.ly/how-to-make-a-bar-chart-online/). The corresponding raw
 HTML file is: `web_app_tutorials/raw/BarChartTutorial/BarChartTutorial.html`
 and set
 [here](https://github.com/plotly/learn-tutorials/blob/master/web_app_tutorials/translate_filename_url.json).

#### A-1. Update raw HTML content

**Either**:

Update the up-to-date Google document, convert to HTML and overwrite folder
`web_app_tutorials/raw/BarChartTutorial/` with the generated output folder. 

**OR**:

Update `web_app_tutorials/raw/BarChartTutorial/BarChartTutorial.html` directly
in HTML.

#### A-2. Publish the updated content

From `learn-tutorials/`, run

```
$ make publish folder=web_app_tutorials
```

where "web_app_tutorials" is the content directory name in this case.

#### A-3. Go to

- [After all cases](#after-all-cases)


### Case B: Update meta information of an existing page

That is, a page's title (seen in browsers' window header), meta description and
breadcrumb title (and maybe more fields in the future).

#### B-0. Find corresponding `config.json` JSON file

All meta information of a given page is stored in one `config.json` JSON file
located in the `published/` subfolder. The full path is given by:

```
learn-tutorials/<content-directory>/published/includes/<url-of-tutorial-page>/config.json
```

Each `config.json` JSON file has:

- `tutorial_name` : is the name that appears in the header (or breadcrumb)
- `tags.title` : is the page title that appears at the top of your browser window
- `tags.meta_description` : is the meta description

> For completeness, say we are updating meta information for the bar chart web
 app tutorial [page](https://plot.ly/how-to-make-a-bar-chart-online/). The
 corresponding `config.json` JSON file is:
 `web_app_tutorials/published/includes/how-to-make-a-bar-chart-online/config.json`.

#### B-1. Modify the `config.json` JSON file in question

Then, save and close.

#### B-2. Go to

- [After all cases](#after-all-cases)

### Case C: Add a new tutorial page

#### C-1. Choose a content directory 

Each content directory corresponds to an individual Django template. Each Django
template inserts breadcrumb, link and layout unique to each content directory.

#### C-2. Export Google document to `raw/` 

Note that the name of the output folder makes no difference in the publish
process. You just have to keep track of the name of the raw HTML file.

#### C-3. Pick a URL, add a key-value pair in `translate_filename_url.json`

In the content directory in question (e.g. `web_app_tutorials`), open
`translate_filename_url.json` and add a key-value pair, where the key (i.e. the
left-hand side) is the name of the raw HTML file and the value (i.e. the
right-hand side) is the URL of the tutorial page.

#### C-4. Publish the new tutorial page 

From `learn-tutorials/`, run

```
$ make publish folder=web_app_tutorials
```

where "web_app_tutorials" is the content directory name in this case.

#### C-5 Modify the `config.json` JSON file of the new tutorial page

See [case B](#case-B-update-meta-information-of-an-existing-page)

#### C-6. Go to

- [After all cases](#after-all-cases)

### Case D: Modify the URL of an existing page

*coming soon*

#### 3. Go to

- [After all cases](#after-all-cases)

-------------------------------------------------------------------------------

### After all cases

#### 1. Commit and push to the `learn-tutorials/` on Github 

From `learn-tutorials/`, run

```
$ git add --all
$ git commit -m "a commit message describing the modifications made"
$ git push origin my-branch
```

where `my-branch` is the name of the branch created [before all
cases](#before-all-cases).

#### 2. Make a pull request on the online `learn-tutorials/` repository

See this [tutorial](https://help.github.com/articles/creating-a-pull-request) on
how to make a pull request on Github.

- If only minor modifications were made (like in [case
  A](#case-a-update-content-of-an-existing-page) or [case
  B](#case-b-update-meta-information-of-an-existing-page)), you can merge the
  changes right away. 

- If major modifications were made, mention a few potential reviewers and wait
  for a review before merging.

#### 3. Clone or pull `streambed/` 

*The subsequent step can only be made by Plotly organization members.*

We recommend placing `streambed/` one level down relative to `learn-tutorials/`.
If you choose otherwise, update the `streambed_path` variable (see
[here](https://github.com/plotly/learn-tutorials/blob/master/makefile#L4)) in
the `learn-tutorials/` `makefile`.

So, clone `streambed/` by running:

```
$ git clone https://github.com/plotly/streambed.git
```

**OR** 

If you already have a copy of `streambed/` on your machine, then pull
in the latest version by running from `streambed/` with

```
$ git checkout master
$ git pull origin master
```

#### 4. Make a new branch in `streambed/`

> For completeness, call this new branch "my-branch".

Form `streambed/`, run

```
$ git branch my-branch
```

and then checkout to your new branch with

```
$ git checkout my-branch
```

#### 4. Sync published `learn-tutorials` content with `streambed/` !

From `learn-tutorials/`, run

```
$ git checkout master
$ git pull origin master
$ make push-to-streambed folder=web_app_tutorials
```

where "web_app_tutorials" is an example of a content directory name.

If you made modifications in more than one content directory, run `$ make
push-to-streambed` in sequence with the appropriate `folder` tag.

#### 5. Preview/Test new or updated content

**Either**:

Use the stage environment by:

1. Committing your modifications and pushing to the online repo:

From `streambed/`, run

```
$ git add --all
$ git commit -m "a commit message describing the modifications made"
$ git push origin my-branch
```

2. Deploying to stage, by typing "plot, deploy my-branch to stage" in the Plotly
   Hipchat room.

**OR**:

- Use a local instance of plotly (the installation guidelines are
  [here](https://github.com/plotly/deployment/tree/ansible#local-vagrant-development-environment)).


#### 6. Make a pull request on online `learn-tutorials/` repository

See this [tutorial](https://help.github.com/articles/creating-a-pull-request) on
how to make a pull request on Github.

- Mention a few potential reviewers and wait for a review before merging.

#### 7. Deploy to prod! 
