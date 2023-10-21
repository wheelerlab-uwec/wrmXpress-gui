from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def convert_png_to_pdf(png_file, pdf_file):
    # Open the PNG image
    image = Image.open(png_file)

    # Create a PDF canvas
    c = canvas.Canvas(pdf_file, pagesize=letter)

    # Set the width and height of the PDF page to match the image
    pdf_width, pdf_height = letter
    img_width, img_height = image.size

    # Calculate scaling factors to fit the image within the page
    if img_width > pdf_width or img_height > pdf_height:
        img_width, img_height = pdf_width, pdf_height
    else:
        pdf_width, pdf_height = img_width, img_height

    # Draw the image on the PDF canvas
    c.drawImage(png_file, 0, 0, width=img_width, height=img_height)

    # Save the PDF file
    c.save()

if __name__ == "__main__":
    input_png_file = "/Users/zach/avacado_analytics/funny-venn-diagram-8.png"
    output_pdf_file = "/Users/zach/avacado_analytics/funny-venn-diagram-8.pdf"

    convert_png_to_pdf(input_png_file, output_pdf_file)