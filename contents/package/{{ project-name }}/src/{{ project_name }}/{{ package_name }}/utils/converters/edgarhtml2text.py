import logging
from bs4 import BeautifulSoup


class HTMLiXBRL2Text:
    def __init__(self):
        logging.basicConfig(
            format="%(asctime)s %(levelname)s: %(message)s", level=logging.DEBUG
        )
        self.logger = logging.getLogger()

        self.input_file_name = None
        self.output_file_name = None

    def configure(self, input_file_name: str, output_file_name: str):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name

    def convert(self) -> bool:
        if self.input_file_name is None or self.output_file_name is None:
            self.logger.info("HTMLiXBRL2Text.configure() call is missing.")
            return False

        try:
            self.logger.info(f"Converting HTMLiXBRL from {self.input_file_name}.")

            extracted_text = ""

            # Note: SEC files are HTML files with iXBRL embedded in them.
            # soup.get_text() does not work

            with open(self.input_file_name, "r") as html_file:
                soup = BeautifulSoup(html_file, "html.parser")

            # traverse each tag
            for tag in soup.find_all():
                extracted_text += f'\n{tag.name} '
                for attr, value in tag.attrs.items():
                    extracted_text += f'\n{attr} '
                    extracted_text += f'\n{value} '
                extracted_text += f'\n{tag.string if tag.string else tag.get_text(strip=True)} '

            with open(self.output_file_name, "w") as text_file:
                text_file.write(extracted_text)

            self.logger.info(f"{self.output_file_name} is written completely.")
            return True

        except Exception as e:
            self.logger.error(e)
            return False