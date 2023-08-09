import glob
import pathlib
import PyPDF2
import json


current_dir = pathlib.Path(__file__).parent.absolute()

pdf_files = glob.glob(str(current_dir) + "/*.pdf")

# We don't need this file right now.
# z_result = pdf_files.pop()

# A list to store the data.
DATA = {}

# We store the PRN, branch, student name into a dict indexed with the seat number.

for pdf_file in pdf_files:
    # open pdf file
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    # get number of pages
    num_pages = pdf_reader.getNumPages()
    # loop through pages
    for i in range(num_pages):
        # get page
        page = pdf_reader.getPage(i)
        # get page content
        page_content = page.extractText()
        # print page content
        # print(content)
        content = page_content.splitlines()

        # Clean up the content
        while ("" in content):
            content.remove("")
        
        # Figure out the branch
        branch = 'UNDEF'
        if "CSE" in content[4] or "CSE" in content[5]:
            branch = "CSE"
        elif "ETC" in content[4] or "ETC" in content[5]:
            branch = "ETC"
        elif "ME" in content[4] or "ME" in content[5]:
            branch = "ME"
        elif "CE" in content[4] or "CE" in content[5]:
            branch = "CE"
        elif "EE" in content[4] or "EE" in content[5]:
            branch = "EE"
        
    
        prn = content[content.index("PRN:") + 1]
        seat_num = content[content.index("Seat Number : ") + 1]
        student_name = content[content.index("Student Name:") + 1]
        
        DATA[int(seat_num)] = {
            "prn":prn,
            "branch":branch,
            "name": student_name
        }
        

with open(str(current_dir / 'hall_ticket.json'), 'w') as f:
    json.dump(DATA, f)
    

