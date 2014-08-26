# How to contribute


### Before all cases

#### 1. Clone or pull

From the directory of your choice, run

```
$ git clone https://github.com/plotly/learn-tutorials.git
```

If you already have a copy of this repo on your machine, then pull in the latest
version by running from `learn_tutorials/`:

```
$ git pull origin master
```

#### 2. Make a new branch in `learn_tutorials/`

Run

```
$ git branch <name-of-your-branch>
```

and then checkout to your new branch

```
$ git checkout <name-of-your-branch>
```


### Case A: Fix typo or update on existing page

#### 1. Either

- fix the typo in the up-to-date google document, convert to HTML and overwrite

```
learn_tutorials/<name-of-content-dir>/raw/<name-of-tutorial>/
```  

- or fix the typo directly in the HTML file in question

#### 2. Run script make publish 

From the `learn_tutorials/`, run

```
$ make publish folder=<name-of-content-dir>
```

### Case B: Fix typo or update meta a page's information

All the meta information is in JSON file located

```
learn_tutorials/<name-of-content-dir>/published/includes/<tutorial-url>/config.json
```

#### 1. Open the `config.json` in question

and modify the fields 

- `tutorial_name` : is the name that appears in the header (or breadcrumb)
- `tags.title` : is the page title that appears at the top of your browser window
- `tags.meta_description` : is the meta description

### Case D: Add a new tutorial

coming soon

### Case E: Add a new content directory

coming soon

### Case F: Modify the url of a tutorial

coming soon

### After all cases

#### 1. Commit and push to the `learn_tutorial/` on github 

Run

```
$ git add --all
$ git commit -m "some nice commit message
$ git push origin <name-of-your-branch>
```

#### 2. Make a pull request, wait for reviews and merge

See this [tutorial](https://help.github.com/articles/creating-a-pull-request).

### Update streambed!!!

#### 3. Clone or pull Make a new branch in `streambed/`

#### 4.  ...








