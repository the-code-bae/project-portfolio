from bs4 import BeautifulSoup
import pathlib
from loguru import logger

DIRECTORY_NAME = "Hello Fresh Web Files"
FILE = "Bacon Linguine Amatriciana.html"
PATH = pathlib.Path(__file__).parent
HF_PATH = PATH.joinpath(DIRECTORY_NAME)
# print out all html files using pathlib
# for f in HF_PATH.iterdir():
#     if f.is_file() and f.suffix == ".html":
#         logger.info(f"file is: {f}, suffix is: {f.suffix}")

html_files = [f for f in HF_PATH.iterdir() if f.is_file() and f.suffix == ".html"]
html_files.sort()

data_dict = {}
for f in html_files[:3]:
    # print(f)
    # print(f.name)
    with open(f) as f_obj:
        contents = f_obj.read()
        # print('done')
        soup = BeautifulSoup(contents, "html.parser")

        # Recipe title
        title = soup.find_all(attrs={"data-test-id": "recipe-preview-title"})[0].contents
        headline = soup.find_all(attrs={"data-test-id": "recipe-preview-headline"})[0].contents
        recipe_title = " ".join(title + headline)
        logger.info(f"The recipe is: {recipe_title}, file name: {f.name}")

        # Get the ingredients
        for c in soup.find_all("span", class_="web-12wkbvj"):
            # print(c.find_next(attrs={"data-test-id": "recipe-preview-ingredient-allergens"}))
            # print(c)
            # print(c.contents)
            if c.contents[0].name == "p":
                # print(c.contents)
                for i in c.contents[:2]:
                    if isinstance(i,str):
                    # print(type(i))
                    # if i.name == "p" or i.name is None:
                        # print(i.name)
                        print(f"Food: {i}")
                    # print(type(i))
                    if i.next.name not in ["span", "div"]:
                        print(f"Units: {i.next}")

