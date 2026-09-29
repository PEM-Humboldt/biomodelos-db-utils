"""
Custom click parameter types shared by bmdbutils commands.
"""

import click


def find_utf8_error(file_path):
    """
    Find the first byte of a file that is not valid UTF-8

    Parameters
    ----------
    file_path : str
                Path of the file to check

    Returns
    -------
    str or None
        location of the first invalid byte, None if the file is valid UTF-8
    """
    with open(file_path, "rb") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                line.decode("utf-8")
            except UnicodeDecodeError as error:
                return f"línea {line_number}, byte 0x{line[error.start]:02X}"
    return None


class Utf8File(click.Path):
    """
    Existing file path whose content must be UTF-8 encoded.
    """

    def __init__(self):
        super().__init__(exists=True, dir_okay=False)

    def convert(self, value, param, ctx):
        file_path = super().convert(value, param, ctx)
        error = find_utf8_error(file_path)
        if error:
            self.fail(
                f"El archivo '{click.format_filename(file_path)}' no está "
                f"codificado en UTF-8 ({error}). "
                "Guárdelo como 'CSV UTF-8' y vuelva a intentar"
            )
        return file_path
