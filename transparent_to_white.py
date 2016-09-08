from PIL import Image
import PyPDF2


def draw_firma_in_pdf(page_in_curr_docf, pdf_reader, pdf_writer, firma_path):
    import StringIO
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4, landscape

    pos_firma = (22, 25, 267, 62)
    existing_pdf = pdf_reader
    packet = StringIO.StringIO()
    can = canvas.Canvas(packet, pagesize=landscape(A4))  # (595,842))

    if firma_path:
        can.drawImage(firma_path, pos_firma[0], pos_firma[1], pos_firma[2], pos_firma[3])
    can.save()
    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    new_page = new_pdf.getPage(0)

    page = existing_pdf.getPage(page_in_curr_docf)
    page.mergePage(new_page)
    pdf_writer.addPage(page)
    return True


def get_main_color(image):
    img = Image.open(image)
    colors = img.getcolors(256) # put a higher value if there are many colors in your image
    max_occurrence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurrence:
                (max_occurrence, most_present) = c
        return most_present[1]
    except TypeError:
        raise Exception("Too many colors in the image")


def is_transparent(color):
    if color == 0:
        print "was transparent"
        return True
    else:
        print "is white"
        return False


def transparent_to_white(convert, file, old_dir, new_dir):
    img = Image.open(file)

    if convert:
        img = img.convert("RGBA")
        data = img.getdata()

        new_data = []
        for item in data:
            if item[3] == 0:
                new_data.append((255, 255, 255))
            else:
                new_data.append(item)

        img.putdata(new_data)

    file = file[len(old_dir):]
    img.save("%s%s" % (new_dir, file), "PNG")


# codi 'main'
for i in range(1, 4):

    original_dir_images = "original_images/"
    original_dir_pdfs = "original_pdfs/"
    new_dir_images = "generated_images/"
    new_dir_pdfs = "generated_pdfs/"

    original_image = "%sfirma%s.png" % (original_dir_images, i)
    original_pdfs = ("%s6691810" % original_dir_pdfs, "%s6680710" % original_dir_pdfs, "%s6694210" % original_dir_pdfs)
    new_image = "%sfirma%s.png" % (new_dir_images, i)

    transparent_to_white(is_transparent(get_main_color(original_image)), original_image, original_dir_images,
                         new_dir_images)

    pdf_reader = PyPDF2.PdfFileReader(open(original_pdfs[i-1], 'rb'))
    pdf_writer = PyPDF2.PdfFileWriter()
    num_pages = pdf_reader.getNumPages()
    for pag in range(0, num_pages):
        if pag == num_pages - 1:
            draw_firma_in_pdf(pag, pdf_reader, pdf_writer, new_image)

    output_stream = file("%s%s.pdf" % (new_dir_pdfs, original_pdfs[i-1][len(original_dir_pdfs):]), "wb")
    pdf_writer.write(output_stream)
    output_stream.close()



