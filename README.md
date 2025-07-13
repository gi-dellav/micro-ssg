# micro-ssg
A really small Markdown-based SSG

## I. Install Dependencies

`pip install -r requirements.txt`

## II. Create New Project

`micro_ssg new [NAME]` 

This will create 
- Site.toml
- `static` directory for files/assets that should always be built with the site (ex. images, videos, JS libraries)
- `templates` directory for *.HTML templates
- `pages` directory for *.MD files that uses the `_pages` template.

If you want to create new templates, add a `_*.HTML` file in `templates` and create a new directory with the same name for the MD files that will use said template.

## III. Build Static Files

`micro_ssg build`

This will create in the `build` directory a series of HTML files, an `index.html` for the homepage and all assets contained in the `static` directory.

## IV. Serve files over static server (Useful for testing)

`micro_ssg serve`

This will run the `build` command and serve the built files on port 8080.
