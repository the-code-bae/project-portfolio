from bs4 import BeautifulSoup
import pathlib
from loguru import logger

DIRECTORY_NAME = "Hello Fresh Web Files"
FILE = "Bacon Linguine Amatriciana.html"
PATH = pathlib.Path(__file__).parent
HF_PATH = PATH.joinpath(DIRECTORY_NAME)
# print out all html files using pathlib
for f in HF_PATH.iterdir():
    if f.is_file() and f.suffix == ".html":
        logger.info(f"file is: {f}, suffix is: {f.suffix}")

html_files = [f for f in HF_PATH.iterdir() if f.is_file() and f.suffix == ".html"]
html_files.sort()

data_dict = {}
for f in html_files[:3]:
    # print(f)
    print(f.name)
    with open(f) as f_obj:
        contents = f_obj.read()
        # print('done')
        soup = BeautifulSoup(contents, "html.parser")
        print(soup.find_all(attrs={"data-test-id": "recipe-preview-title"})[0].contents)
        print(soup.find_all(attrs={"data-test-id": "recipe-preview-headline"})[0].contents)
