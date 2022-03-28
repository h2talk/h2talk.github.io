from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
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
    g = Generator()
    g.generate('index.html', 'index.html')

if __name__ == '__main__':
    main()