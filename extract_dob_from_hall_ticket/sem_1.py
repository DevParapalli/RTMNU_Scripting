import glob
import pathlib
import PyPDF2
import json
import csv

current_dir = pathlib.Path(__file__).parent.absolute()

# the pdfs are named sem_1_code.pdf, They contain the password thingy
pdf_files = glob.glob(str(current_dir) + "/sem_1_*.pdf")

DATA = []

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

        while ("" in content):
            content.remove("")

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
        username = content[content.index("UserName: ") + 1]
        password = content[content.index("Password: ") + 1]
        # Password is a string of the format YYMMDD
        # split the string into YY, MM, DD
        _password = [password[4:], password[2:4], '20'+password[:2]]
        date_of_birth = "/".join(_password)
        DATA.append({
            "prn": prn,
            "branch": branch,
            "seat_num": seat_num,
            "student_name": student_name,
            "username": username,
            "password": password,
            "date_of_birth": date_of_birth
        })
        print(f"Processed {student_name}")

with open(str(current_dir / "sem_1_data.json"), "w") as f:
    f.write(json.dumps(DATA))
    print(f"Dumped data into data.json")

# Create a google calendar csv.
with open(str(current_dir / "sem_1_data.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Subject", "Start Date", "Start Time", "End Date", "End Time","All Day Event", "Description", "Location", "Private"])
    for person in DATA:
        current_sub = f"Birthday: {person['student_name']} - {person['branch']} - 25"
        x, y, z = person['date_of_birth'].split("/")
        start_date = f"{x}/{y}/2022"
        writer.writerow([current_sub, start_date, "00:00", start_date, "00:00", "True", "Desc.", "Loc.", "False"])
    print(f"Dumped data into data.csv")