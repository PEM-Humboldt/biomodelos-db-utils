import click


class Utf8File(click.Path):

    def __init__(self):
        super().__init__(exists=True, dir_okay=False)

    @staticmethod
    def find_utf8_error(file_path):
        with open(file_path, "rb") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    line.decode("utf-8")
                except UnicodeDecodeError as error:
                    return (
                        f"línea {line_number}, byte 0x{line[error.start]:02X}"
                    )
        return None

    def convert(self, value, param, ctx):
        file_path = super().convert(value, param, ctx)
        error = self.find_utf8_error(file_path)
        if error:
            self.fail("The CSV_FILE must have UTF-8 encoding.")
        return file_path
