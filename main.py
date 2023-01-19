import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton
from PyPDF2 import PdfFileWriter, PdfReader
from PIL import Image
import json

class FormFiller(QWidget):
    def __init__(self):
        super().__init__()

        # Create labels and line edits for form fields
        self.name_label = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.address_label = QLabel("Address:")
        self.address_edit = QLineEdit()
        self.city_label = QLabel("City:")
        self.city_edit = QLineEdit()
        self.state_label = QLabel("State:")
        self.state_edit = QLineEdit()
        self.zip_label = QLabel("Zip:")
        self.zip_edit = QLineEdit()

        # Create a "Save" button and connect it to the fill_pdf function
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(lambda: fill_pdf(self))

        # Create a layout and add the form fields
        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_edit)
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_edit)
        layout.addWidget(self.state_label)
        layout.addWidget(self.state_edit)
        layout.addWidget(self.zip_label)
        layout.addWidget(self.zip_edit)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        # Set the form title
        self.setWindowTitle("ATF Form 1")
        self.show()

def init_form_data(config_path: str) -> dict:
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
    return config

def fill_pdf(form_filler: FormFiller):
    # Open the PDF form
    with open("f_5320._1_application_to_make_and_register_a_firearm.pdf", "rb") as form_file:
        form = PdfReader(form_file)

    # Get the user's form data
    name = form_filler.name_edit.text()
    address = form_filler.address_edit.text()
    city = form_filler.city_edit.text()
    state = form_filler.state_edit.text()
    zip = form_filler.zip_edit.text()

    # Fill out the form fields
    form.getField("name").value = name
    form.getField("address").value = address
    form.getField("city").value = city
    form.getField("state").value = state
    form.getField("zip").value = zip

    # Save the filled-out form
    with open("filled_form1.pdf", "wb") as output_file:
        form.write(output_file)


def fill_pdf_form(form_data: dict):
    # Open the PDF form
    with open("f_5320._1_application_to_make_and_register_a_firearm.pdf", "rb") as form_file:
        form = PdfReader(form_file)

    # Fill out the form fields
    for field, value in form_data.items():
        form.getField(field).value = value

    # Save the filled-out form
    with open("filled_form5320.1.pdf", "wb") as output_file:
        form.write(output_file)

# Example usage:
# form_data = {
#     "name": "John Doe",
#     "address": "123 Main St",
#     "city": "Anytown",
#     "state": "CA",
#     "zip": "12345",
#     # other fields...
# }

def embed_photo(img_path: str, pdf_path: str):
    # Open the PDF form
    with open(pdf_path, "rb") as form_file:
        form = PdfFileWriter()
        form.appendPagesFromReader(PdfFileReader(form_file))

    # Open the image
    img = Image.open(img_path)

    # Convert the image to a PDF
    img_pdf = PdfFileWriter()
    img_pdf.addPage(img.convert('RGB').im.id)

    # Append the image to the form
    form.appendPagesFromReader(img_pdf)

    # Save the filled-out form
    with open("filled_form5320.1.pdf", "wb") as output_file:
        form.write(output_file)

# Example usage:
# embed_photo("headshot.jpg", "form5320.1.pdf")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = FormFiller()
    form.show()
    sys.exit(app.exec_())
