#!/usr/bin/env python3
"""
Static Site Generator for Portfolio
Renders the Flask template with portfolio data to create static HTML files
"""

from flask import Flask, render_template
import json
from pathlib import Path
import shutil

# Use the same default portfolio data as app.py
from app import DEFAULT_PORTFOLIO


def generate_static_site():
    """Generate static HTML files for GitHub Pages"""

    app = Flask(__name__, 
                template_folder=str(Path(__file__).parent / 'templates'),
                static_folder=str(Path(__file__).parent / 'static'))

    app.config['SERVER_NAME'] = 'localhost'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'

    with app.app_context():
        view_count = 0
        view_counter_file = Path(__file__).parent / 'view_count.json'
        if view_counter_file.exists():
            try:
                with open(view_counter_file, 'r', encoding='utf-8') as vcf:
                    view_count = int(json.load(vcf).get('views', 0))
            except Exception:
                view_count = 0

        rendered_html = render_template('index.html', portfolio=DEFAULT_PORTFOLIO, view_count=view_count)

        rendered_html = rendered_html.replace('http://localhost/static/css/style.css', 'static/css/style.css')
        rendered_html = rendered_html.replace('http://localhost/static/js/main.js', 'static/js/main.js')
        rendered_html = rendered_html.replace('http://localhost/static/', 'static/')
        rendered_html = rendered_html.replace('/static/css/style.css', 'static/css/style.css')
        rendered_html = rendered_html.replace('/static/js/main.js', 'static/js/main.js')
        rendered_html = rendered_html.replace('/static/', 'static/')

        docs_dir = Path(__file__).parent / 'docs'
        docs_dir.mkdir(exist_ok=True)

        with open(docs_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(rendered_html)

        static_src = Path(__file__).parent / 'static'
        static_dest = docs_dir / 'static'

        if static_dest.exists():
            shutil.rmtree(static_dest)
        if static_src.exists():
            shutil.copytree(static_src, static_dest)

        print('Static site generated successfully!')
        print(f'Files created in: {docs_dir}')
        print('You can now commit and push these files to deploy to GitHub Pages')


if __name__ == '__main__':
    generate_static_site()
