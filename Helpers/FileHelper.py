from Constants import LocalFoldersConstants
from Helpers.StringHelper import filenameFormater


def exportToFile(filename: str, ext: str, content: str) -> None:
    with open(LocalFoldersConstants.EXPORTS_FOLDER + filenameFormater(str(filename)) + "." + ext, "w") as outfile:
        outfile.write(content)
