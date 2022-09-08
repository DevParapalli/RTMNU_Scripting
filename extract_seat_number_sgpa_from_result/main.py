import re
import pathlib
import PyPDF2
import json

current_dir = pathlib.Path(__file__).parent.absolute()

z_result = current_dir / 'result.pdf'

def remove_white_spaces(content: str):
    """Removes all whitespace in the string given"""
    content = content.replace(" ", "")
    content = content.replace("\n", "")
    return content
    

DATA = {}

# PDF contains a bunch of string in the form 
# 325632(543/9.23)
data_regex = re.compile(r'(?P<seat>\d+)\((?P<marks>\d+)/(?P<sgpa>\d*\.\d+\))')

# PDF READER
pdf_reader = PyPDF2.PdfFileReader(str(z_result))
num_pages = pdf_reader.getNumPages()
for i in range(num_pages):
    page = pdf_reader.getPage(i)
    # get page content
    page_content = page.extractText()
    
    content = remove_white_spaces(page_content)
    
    # print(content)
    for match in data_regex.finditer(content):
        _data = match.groupdict()
        DATA[_data['seat']] = {
            "marks": int(_data['marks']),
            "sgpa": float(_data['sgpa'].replace(")", ""))
        }
        

with open(str(current_dir / 'result.json'), 'w') as f:
    json.dump(DATA, f)
    print(len(DATA.keys()))