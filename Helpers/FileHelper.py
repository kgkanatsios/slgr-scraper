import pandas as pd

from Constants import LocalFoldersConstants
from Helpers.StringHelper import filenameFormater


def exportToFile(filename: str, content: str) -> None:
    path = exportToJsonFile(filename, content)
    print("Results: " + path)


def exportToJsonFile(filename: str, content: str) -> str:
    file_path = LocalFoldersConstants.EXPORTS_FOLDER + \
        filenameFormater(str(filename)) + ".json"
    with open(file_path, "w") as outfile:
        outfile.write(content)

    return file_path


def exportToExcelFile(filename: str, content: str) -> str:
    file_path = LocalFoldersConstants.EXPORTS_FOLDER + \
        filenameFormater(str(filename)) + ".xlsx"

    df = pd.read_json(content)
    df.to_excel(file_path)

    return file_path
