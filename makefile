# --- learn_tutorial/ makefile ---

# Set (relative or absolute) path to streambed
streambed_path="../streambed"

# -------------------------------------------------------------------------------

# Make raw HTML content publishable
#    $ make publish folder=<name-of-folder>
# or $ make publish folder="<name-of-folders>"
publish:
	@rm -f publish.log
	@ipython _scripts/publish.py $(folder)

# Show config files 
#    $ make show-config folder=<name-of-folder>
show-config:
	@more $(folder)/published/includes/*/config.json | cat | less

# Show log file
# 	$ make show-log
show-log:
	@more publish.log | cat | less

# Push change to streambed
#    $ make push-to-streambed folder=<name-of-folder>
push-to-streambed:
	@rm -rf $(streambed_path)/shelly/templates/learn/includes/$(folder)/*
	@cp -R $(folder)/published/includes/* $(streambed_path)/shelly/templates/learn/includes/$(folder)/
	@rm -rf $(streambed_path)/shelly/learn/static/learn/images/$(folder)/*
	@cp -R $(folder)/published/static/images/* $(streambed_path)/shelly/learn/static/learn/images/$(folder)/
	@cp $(folder)/published/urls.py $(streambed_path)/shelly/learn/urls/$(folder)/urls.py
	@cp $(folder)/published/sitemaps.py $(streambed_path)/shelly/learn/sitemaps/$(folder)/sitemaps.py

# Clean published folder
#    $ make clean folder=<name-of-folder>
clean:
	@rm -rf $(folder)/published/*

