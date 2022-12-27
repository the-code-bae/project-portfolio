from bs4 import BeautifulSoup
import pathlib
from loguru import logger

DIRECTORY_NAME = "Hello Fresh Web Files"
FILE = "Bacon Linguine Amatriciana.html"
PATH = pathlib.Path(__file__).parent
HF_PATH = PATH.joinpath(DIRECTORY_NAME)

# Create list of filepaths for all hello fresh html files which have the recipes
html_files = [f for f in HF_PATH.iterdir() if f.is_file() and f.suffix == ".html"]
html_files.sort()

ingredients_data = []
for f in html_files[:2]:
    with open(f) as f_obj:
        contents = f_obj.read()
        soup = BeautifulSoup(contents, "html.parser")

        recipe_dict = {}

        # Recipe title
        title = soup.find_all(attrs={"data-test-id": "recipe-preview-title"})[0].contents
        headline = soup.find_all(attrs={"data-test-id": "recipe-preview-headline"})[0].contents
        recipe_title = " ".join(title + headline)
        logger.info(f"The recipe is: {recipe_title}, file name: {f.name}")
        recipe_dict["title"] = recipe_title

        # Get the ingredients
        for c in soup.find_all("span", class_="web-12wkbvj"):
            if c.contents[0].name == "p":
                for i in c.contents[:2]:
                    if isinstance(i, str):
                        food = i
                        recipe_dict["ingredient"] = food
                    if i.next.name not in ["span", "div"]:
                        units = i.next
                        recipe_dict["unit"] = units

                # Add tuple to list
                ingredients_data.append((recipe_title, food, units))
print(ingredients_data)
# for d in ingredients_data:
#     print(d)

        # Get the nutrients

        # Row headings
        # print("row headings")
        # nutrient_row_headings = soup.find_all("p", class_="web-9z87v7")
        # row_headings_flattened = []
        # for c in nutrient_row_headings[1:]:
        #     # print(c.contents)
        #     row_headings_flattened.extend(c.contents)
        # print(row_headings_flattened)
        #
        # # per serving
        # print("per serving")
        # nutritional_values_per_serving = soup.find_all(attrs={"data-test-id": "nutritional-values-amount"})
        # per_serving_flattened = []
        # for c in nutritional_values_per_serving:
        #     per_serving_flattened.extend(c.contents)
        # print(dict(zip(row_headings_flattened, per_serving_flattened)))
        #
        # # per 100g
        # print("per 100g")
        # nutritional_values_per_100g = soup.find_all(attrs={"data-test-id": "nutritional-values-amount-100g"})
        # per_100g_flattened = []
        # for c in nutritional_values_per_100g:
        #     per_100g_flattened.extend(c.contents)
        # print(dict(zip(row_headings_flattened, per_100g_flattened)))

        # prep time

        # difficulty

