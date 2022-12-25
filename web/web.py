from .content import Home


class Web:
    """ All Web content holder. """
    css = '''<style>table { border: 1px solid black; }</style>'''

    def __init__(self, generate_status_html) -> None:
        """ All the data used for generating the web content are passed and distributed here. """
        self.pages = {
            '': Home(Web.css, generate_status_html),
        }
