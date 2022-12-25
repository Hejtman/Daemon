from dataclasses import dataclass
from typing import Callable


@dataclass
class Home:
    """ Generator of home page content. """
    css: str
    generate_status_html: Callable

    def __str__(self) -> str:
        return f"""
            <html><head>{self.css}<title>Demon</title></head>
                <body>
                    {self.generate_status_html()}
                </body>
            </html>
        """
