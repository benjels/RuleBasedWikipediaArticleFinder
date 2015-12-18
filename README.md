An alternative way to harvest.

Use `rules.yml` to scope where you want to extract URLs from & which strings to ignore. https://en.wikipedia.org/wiki/YAML

This is just a base. Could use extension. The example below:
- iterates over two Wikipedia lists (`List_of_towns_in_New_Zealand` & `List_of_cities_in_New_Zealand`)
- restricts the beautifulsoup parser to just sections that fall within each `scopes` list
- ignores topics that contain strings in the `ignore` list.