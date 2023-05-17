from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Backend.backend import Scrap
import csv
import os

app = FastAPI()

# Mount the static files directory to serve CSS and other assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    csv_file = "static/data.csv"
    if os.path.exists(csv_file):

        data = []
        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    else:
        data = {}
    return templates.TemplateResponse("index.html", {"request": request, "data": data})


@app.post("/")
async def process_input(request: Request):
    form_data = await request.form()
    user_input = form_data.get("input")
    csv_file = 'static/data.csv'
    # Process the input data and return a dictionary
    with Scrap() as Bot:
        print("Starting...")
        Bot.land_first_page(user_input)
        l = Bot.run()

        if len(l) == 2:
            name = l[0]
            current_date = l[1]
            check = True
            dic = {'name': name[:len(name) - 1], 'current_date': current_date, 'check': check}
        else:
            check = False
            dic = {'name': '', 'current_date': '', 'check': check}

    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)

        # Check if the file is empty
        is_empty = file.tell() == 0

        # Write the header row if the file is empty
        if is_empty:
            writer.writerow(dic.keys())

        # Check if the name value already exists in the CSV
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            names = [row["name"] for row in reader]

        if dic["name"] not in names:
            # Write the values row
            writer.writerow(dic.values())
            print("Data appended to CSV file successfully.")
        else:
            print("Name already exists in the CSV file. Skipping the duplicate entry.")

    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)

        # Get the field names from the first row
        field_names = next(reader)

        # Get the values from the remaining rows
        values = list(reader)

        # Populate the dictionary with all the data
        dic_list = []
        for row in values:
            dic_list.append(dict(zip(field_names, row)))

    print(dic_list)

    # Do something with the user_input (e.g., send it to a Python file)

    return templates.TemplateResponse("index.html", {"request": request, "user_input": dic_list})
