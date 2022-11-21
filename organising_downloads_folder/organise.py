from loguru import logger
import pathlib

DOWNLOADS_FOLDER = (pathlib.Path.home().joinpath('Downloads'))

# define the file categories with dictionary
SUBDIR = {
    "DOCUMENTS": [".pdf", ".docx", ".doc", ".txt", ".ppt"],
    "AUDIO": [".m4a", ".m4b", ".mp3"],
    "IMAGES": [".jpg", ".jpeg", ".png"],
    "DATA": [".csv", ".xls"],
    "SCRIPTS": [".ipynb", ".py"]
}


def pickDir(value):
    '''
    value: str contain extension of the file.
    return name of the category who defined before.
    e.g. value = '.pdf' so the function will return DOCUMENTS.
    '''
    for category, extension in SUBDIR.items():
        for suffix in extension:
            if suffix == value:
                return category


def organizeDir(dir):
    '''
    this function will scan any files in the same directory, and then
    look at every extension of files and move that file to the exact category from calling the pickDir function.


    '''
    unhandled_extensions = set()
    p = dir.glob('**/*')
    for item in p:
        # just looking for file, skip the directory
        if item.is_dir():
            logger.info(f"The item is a folder: {item}")
            continue

        logger.info(f"The file being processed is: {item}")

        filePath = pathlib.Path(item)
        logger.info(f"The file path is: {filePath}")

        fileName = filePath.parts[-1]
        logger.info(f"The file name is: {fileName}")

        fileType = filePath.suffix.lower()
        logger.info(f"The file type is: {fileType}")

        directory = pickDir(fileType)
        logger.info(f"The directory it belongs in is: {directory}")

        # just skip, if the file extension not defined.
        if directory == None:
            unhandled_extensions.add(fileType)
            continue

        directoryPath = dir.joinpath(directory)
        # make new directory if the category's directory not found.
        if directoryPath.is_dir() != True:
            directoryPath.mkdir()
        logger.info(f"The file will be moved to: {directoryPath.joinpath(fileName)}")
        filePath.rename(directoryPath.joinpath(fileName))

    logger.info(f"The following extensions have no home: {unhandled_extensions}")

if __name__ == "__main__":
    organizeDir(DOWNLOADS_FOLDER)