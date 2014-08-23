# Set (relative or absolute) path to streambed
streambed_path="../streambed"

# -------------------------------------------------------------------------------

# 
publish-excel_tutorials:
	@rm -f publish.log
	@ipython _scripts/publish.py excel_tutorials

# 
push-to-streambed:
	@cp -R excel_tutorials/published/includes/* $(streambed_path)/shelly/templates/learn/includes/excel_tutorials/
	@cp -R excel_tutorials/published/static/images/* $(streambed_path)/shelly/learn/static/learn/images/excel_tutorials/
	@cp excel_tutorials/published/urls.py $(streambed_path)/shelly/learn/urls/excel_tutorials/
	@cp excel_tutorials/published/sitemaps.py $(streambed_path)/shelly/learn/sitemaps/excel_tutorials/
	
# 
clean:
	@rm -rf excel_tutorials/published/*



