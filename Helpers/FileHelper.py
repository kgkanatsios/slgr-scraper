import pandas as pd

from Constants import LocalFoldersConstants
from Helpers.StringHelper import filenameFormater


def exportToFile(filename: str, content: str) -> None:
    exportToJsonFile(filename, content)
    exportToExcelFile(filename, content)


def exportToJsonFile(filename: str, content: str) -> None:
    with open(LocalFoldersConstants.EXPORTS_FOLDER + filenameFormater(str(filename)) + ".json", "w") as outfile:
        outfile.write(content)


def exportToExcelFile(filename: str, content: str) -> None:
    df = pd.read_json(content)
    df.to_excel(LocalFoldersConstants.EXPORTS_FOLDER +
                filenameFormater(str(filename)) + ".xlsx")
