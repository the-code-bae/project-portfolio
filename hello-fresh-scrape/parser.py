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
for f in html_files[:1]:
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
            if c.contents[0].name == "p":
                for i in c.contents[:2]:
                    if isinstance(i,str):
                        print(f"Food: {i}")
                    if i.next.name not in ["span", "div"]:
                        print(f"Units: {i.next}")

        # Get the nutrients

        # Row headings
        print("row headings")
        nutrient_row_headings = soup.find_all("p", class_="web-9z87v7")
        row_headings_flattened = []
        for c in nutrient_row_headings[1:]:
            # print(c.contents)
            row_headings_flattened.extend(c.contents)
        print(row_headings_flattened)


        # per portion
        print("per portion")
        nutritional_values_per_portion = soup.find_all(attrs={"data-test-id": "nutritional-values-amount"})
        per_portion_flattened = []
        for c in nutritional_values_per_portion:
            per_portion_flattened.extend(c.contents)
        print(dict(zip(row_headings_flattened,per_portion_flattened)))

        # per 100g
        print("per 100g")
        nutritional_values_per_100g = soup.find_all(attrs={"data-test-id": "nutritional-values-amount-100g"})
        per_100g_flattened = []
        for c in nutritional_values_per_100g:
            per_100g_flattened.extend(c.contents)
        print(dict(zip(row_headings_flattened,per_100g_flattened)))

