from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import json
import os

class Generator:
    def __init__(self, **fields):
        """ fields is a dict which can be accessed in the template """
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=select_autoescape('html')
        )
        self.fields = fields

    @staticmethod
    def rel_path_to_root(path):
        depth = len(Path(path).parents) - 1
        return '/'.join(['..'] * depth) + '/' if depth else ''
        
    def generate(self, page, template, **fields):
        """ Build page from template """
        # Make parent directories as needed
        os.makedirs(Path(page).parent.absolute(), exist_ok=True)
        with open(page, 'w') as fd:
            tmpl = self.env.get_template(template)
            tmpl.globals['rel_path_to_root'] = Generator.rel_path_to_root
            fd.write(
                tmpl.render(
                    **self.fields,
                    **fields,
                    destination_path=page
                )
            )

def main():

    with open('stations.json', 'r') as fd:
        stations = json.load(fd)
    with open('regions.json') as fd:
        regions = json.load(fd)
    with open('vehicles.json') as fd:
        vehicles = json.load(fd)

    g = Generator()

    # Index
    g.generate('index.html', 'index.html', items=stations, item="station", subdir="s")

    # Station pages
    g.generate('s/index.html', 'stations.html', items=stations, item="station", subdir="s")
    for info in stations:
        g.generate(f"s/{info['slug']}/index.html", 'channel.html', **info)

    # Region pages
    g.generate('r/index.html', 'regions.html', items=regions, item="region", subdir="r")
    for info in regions:
        g.generate(f"r/{info['slug']}/index.html", 'channel.html', **info)

    # Vehicle pages
    g.generate('v/index.html', 'vehicles.html', items=vehicles, item="vehicle", subdir="v")
    for info in vehicles:
        g.generate(f"v/{info['slug']}/index.html", 'channel.html', **info)

if __name__ == '__main__':
    main()
