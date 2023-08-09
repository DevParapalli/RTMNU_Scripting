import fitz
import re
import json

ROLLNO_REGEX = r"\|15\d\d\d\d"
NAME_REGEX = r"(?P<_>\|Name\|of\|Student\|:)(?P<name>\|[A-Z|]*\|)(?P<__>|Mother's)"
doc = fitz.open("CSE.pdf")  # example document
# page = doc[0]  # first page
# words = page.get_text("words", sort=True)  # extract sorted words

LOOKUP = {}

for page in doc:
    text = "|".join([word[4] for word in page.get_text("words")])
    roll = re.findall(ROLLNO_REGEX, text)[0].strip("|").strip()
    name = re.findall(NAME_REGEX, text)[0][1].replace("|", " ").strip()
    LOOKUP[roll] = name

with open("lookup.json", "w") as f:
    json.dump(LOOKUP, f)