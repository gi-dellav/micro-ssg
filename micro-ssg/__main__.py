from build import build_project
from pathlib import *

import click
import os
import http.server
import sockets

DEFAULT_PROJECT_TOML = '''
[project]
name = {name}
'''
DEFAULT_PAGES_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title> {{SITE_NAME}} </title>
</head>
<body>
  <header>
    <h1><a href="/"> {{SITE_NAME}} </a></h1>
  </header>
  <main>
    <div class="content">
      {{PAGE_CONTENT}}
    </div>
  </main>
</body>
</html>
'''
DEFAULT_HOMEPAGE = '''
### Welcome to micro-ssg!

Now, just go to the `pages/homepage.md` file to change this page!
'''

@click.group()
def cli():
    """A really small Markdown-based SSG."""
    pass

@cli.command()
@click.argument('name')
def new(name):
    """Create a new project with the given NAME."""

    click.echo(f"Creating new project: {name}")

    root_dir = Path(name)
    root_dir.mkdir(parents=True, exist_ok=True)
    print("Created main directory")

    toml_path = root_dir / 'Project.toml'
    toml_path.write_text(DEFAULT_PROJECT_TOML)
    print(f"Created {toml_path}")

    # 2. Create directories
    dirs = ['static', 'templates', 'pages']
    for d in dirs:
        dir_path = root_dir / d
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory {dir_path}")

    # 3. Create _pages.html in templates dir
    pages_template_path = root_dir / 'templates' / '_pages.html'
    pages_template_path.write_text(DEFAULT_PAGES_TEMPLATE)
    print(f"Created template {pages_template_path}")

    # 4. Create homepage.md in pages dir
    homepage_path = root_dir / 'pages' / 'homepage.md'
    homepage_path.write_text(DEFAULT_HOMEPAGE)
    print(f"Created page {homepage_path}")


@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
def build(directory):
    """Build the project located at DIRECTORY."""

    click.echo(f"Building project in: {directory}")
    build_project(directory)


@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option('--port', default=8000, show_default=True, help='Port to serve on')
def serve(directory, port):
    """Serve the project located at DIRECTORY over HTTP."""

    # Build and change to the target directory
    click.echo(f"Building project in: {directory}")
    build_project(directory)
    os.chdir(directory)

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(('', port), handler) as httpd:
        click.echo(f"Serving {directory} at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            click.echo("\nShutting down server...")
            httpd.shutdown()


if __name__ == '__main__':
    cli()
