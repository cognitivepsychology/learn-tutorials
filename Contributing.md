# How to contribute


### Before all cases

#### 1. Clone or pull `learn_tutorials/`

From the directory of your choice, clone `learn_tutorials/` by running:

```
$ git clone https://github.com/plotly/learn-tutorials.git
```

**OR** 

If you already have a copy of `learn_tutorials/` on your machine, then pull
in the latest version by running from `learn_tutorials/` with

```
$ git checkout master
$ git pull origin master
```

#### 2. Make a new branch in `learn_tutorials/`

> For completeness, call this new branch "my-branch".

Form `learn_tutorials/`, run

```
$ git branch my-branch
```

and then checkout to your new branch with

```
$ git checkout my-branch
```

#### 3. Go to

- [#Case-A:-Update-content-of-an-existing-page](Case A: Update content of an existing page)
- [#Case-B:-Update-meta-information-of-an-existing-page](Case B: Update meta information of an existing page)
- [#Case-C:-Add-a-new-tutorial-page](Case C: Add a new tutorial page)
- [#Case-D:-Modify-the-URL-of-an-existing-page](Case D: Modify the URL of an existing page)


### Case A: Update content of an existing page

### 0. Find corresponding *raw* HTML file

Each tutorial page has a corresponding *raw* (i.e. not-publishable) HTML file.
Raw HTML files are part of the output folder when exporting a Google document to
HTML. 

If you don't know which raw HTML file correspond to a given page, search through
each content directory's `translate_filename_url.json` file, where the name of
the raw HTML are listed on the left-hand column.

> For completeness, say you are updating the page corresponding to the
`web_app_tutorials/raw/BarChartTutorial/BarChartTutorial.html` raw HTML file.

#### 1. Update raw HTML content

**Either**:

- Update the up-to-date Google document, convert to HTML and overwrite
  folder `web_app_tutorials/raw/BarChartTutorial/` with the generated output
  folder. 

**OR**

- Update `web_app_tutorials/raw/BarChartTutorial/BarChartTutorial.html`
  directly in HTML.

#### 2. Publish the updated content

From `learn_tutorials/`, run

```
$ make publish folder=web_app_tutorials
```

where `web_app_tutorials` is the content directory name in this case.

#### 3. Go to

- [After-all-cases](After all cases)


### Case B: Update meta information of an existing page

*more coming soon*

That is, a page's title, meta description 


All the meta information is in JSON file located

```
learn_tutorials/<content-dir>/published/includes/<tutorial-url>/config.json
```

#### 1. Open the `config.json` in question

and modify the fields 

- `tutorial_name` : is the name that appears in the header (or breadcrumb)
- `tags.title` : is the page title that appears at the top of your browser window
- `tags.meta_description` : is the meta description

### Case C: Add a new tutorial page

*coming soon* 

### Case D: Modify the URL of an existing page

*coming soon*


### After all cases

#### 1. Commit and push to the `learn_tutorial/` on Github 

From `learn_tutorials/`, run

```
$ git add --all
$ git commit -m "a commit message describing the modifications made"
$ git push origin my-branch
```

where `my-branch` is the name of the branch created [Before-all-cases](before
all cases).

#### 2. Make a pull request on online `learn_tutorials/` repository

See this [tutorial](https://help.github.com/articles/creating-a-pull-request) on
how to make a pull request on Github.

- If only minor modifications were made (like in
  [#Case-A:-Update-content-of-an-existing-page](case A) or
  [#Case-B:-Update-meta-information-of-an-existing-page](case B)), you can merge
  the changes right away. 

- If major modifications were made, mention a few potential reviewers and wait
  for a review before merging.

#### 3. Clone or pull `streambed/`

We recommend placing `streambed/` one level down relative to `learn_tutorials/`.
If you choose otherwise, update the `streambed_path`
[variable](https://github.com/plotly/learn-tutorials/blob/master/makefile#L4) in
the `learn_tutorials` `makefile`.

So, clone `streambed/` by running:

```
$ git clone https://github.com/plotly/learn-tutorials.git
```

**OR** 

If you already have a copy of `streambed` on your machine, then pull
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

#### 4. Sync published `learn_tutorials` content with `streambed/` !

From `learn_tutorials/`, run

```
$ make push-to-streambed folder=web_app_tutorials
```

where `web_app_tutorials` is an example of a content directory name.

If you made modifications in more than one content directory, run `$ make
push-to-streambed` in sequence with the appropriate `folder` tag.


#### 5. Preview/Test new or updated content

**Either**:

- Use the stage environment by typing "plot, deploy my-branch to stage" in the
  Plotly Hipchat room.

**OR**

- Use a local instance of plotly (the installation guidelines are
  [here](https://github.com/plotly/deployment/tree/ansible#local-vagrant-development-environment)).


#### 6. Make a pull request on online `learn_tutorials/` repository

See this [tutorial](https://help.github.com/articles/creating-a-pull-request) on
how to make a pull request on Github.

- Mention a few potential reviewers and wait for a review before merging.

#### 7. Deploy to prod! 
