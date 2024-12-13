# combined_labels.py
  
from config import * 
from reportlab.pdfgen import canvas  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont  
from reportlab.lib.pagesizes import letter  
from reportlab.lib.utils import simpleSplit  
from PyPDF2 import PdfReader, PdfWriter, PageObject 
from reportlab.lib.utils import ImageReader 
from PIL import Image, ImageDraw, ImageFont 
  
# Barcode font  
fre3of9x_font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'fre3of9x.ttf')  
pdfmetrics.registerFont(TTFont("fre3of9x", fre3of9x_font_path))  
  
# Montserrat font  
Montserrat_font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'Montserrat.ttf')  
pdfmetrics.registerFont(TTFont("CODE Bold", Montserrat_font_path)) 

# Code Bold font  
code_bold_font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'CODE Bold.ttf')  
pdfmetrics.registerFont(TTFont("CODE Bold", code_bold_font_path))
  
def draw_page_number(c, page_number, total_pages, x, y):  
    c.setFont("CODE Bold", 8)  
    c.setFillColorRGB(0, 0, 0)  
    c.drawString(x, y, f"Page {page_number} of {total_pages}")  
  
def combined_label(order_number, items, base_folder_name, timestamp, order_quantities, order_skus, sub_folder_path, first_lineID, customtagID):  
    try:  
        def process_qr_image(qr_img, x, y, new_width, new_height, aspect_ratio=None):  
            img_width, img_height = qr_img.size  
            padding_to_remove = 10  
            crop_box = (padding_to_remove, padding_to_remove, img_width - padding_to_remove, img_height - padding_to_remove)  
            qr_img = qr_img.crop(crop_box)  
            img_width, img_height = qr_img.size  
            if not aspect_ratio:  
                aspect_ratio = float(img_width) / float(img_height)  
            qr_img = qr_img.resize((new_width, new_height), Image.LANCZOS)  
            c.drawImage(ImageReader(qr_img), x, y, new_width, new_height)  
  
        def generate_order_number_qr(first_lineID, box_size=3, border=4.5):  
            qr = qrcode.QRCode(  
                version=1,  
                error_correction=qrcode.constants.ERROR_CORRECT_L,  
                box_size=box_size,  
                border=border,  
            )  
            qr.add_data(first_lineID)  
            qr.make(fit=True)  
            qr_order_number_img = qr.make_image(fill_color="black", back_color="white")  
            return qr_order_number_img  
  
        temp_pdf_path = os.path.join(tempfile.gettempdir(), 'temp_label.pdf')  
        c = canvas.Canvas(temp_pdf_path, pagesize=letter)  
        c.setFont("CODE Bold", 8)  
        c.setFillColorRGB(0, 0, 0)  
  
        qr_order_number_img = generate_order_number_qr(first_lineID)  
        process_qr_image(qr_order_number_img, 21.5, 370, 50, 50, aspect_ratio=1)  
  
        c.saveState()  
  
        expedited_order = order_number[-1].upper() == 'R' or 'EXP' in order_number.upper()  
        y_position = 185  
        items_per_page = 4  
        current_item_count = 0  
        page_number = 1  
        total_pages = (len(items) + items_per_page - 1) // items_per_page  
  
        for item in items:  
            index, row = item  
            sku = row['Item - SKU'].strip()  
            item_qty = int(row['Item - Qty'])  
            item_options = str(row['Item - Options'])  
            item_name = row['Item - Name']  
            order_date = row['Order - Date']  
            custom_field_3 = row['Custom - Field 3']  
            personalization_text = row['Item - Options']  
  
            order_total_qty = int(float(row['Total Order Qty']))  
            location_text = personalization_text.replace('Location:', '').strip()  
  
            duplicate_order = item_qty > 1  
            multi_order = order_total_qty > 1  
  
            if current_item_count >= items_per_page:  
                draw_page_number(c, page_number, total_pages, 10, 10)  
                c.showPage()  
                c.setFont("CODE Bold", 8)  
                c.setFillColorRGB(0, 0, 0)  
                y_position = 185  
                current_item_count = 0  
                page_number += 1  
  
            process_qr_image(qr_order_number_img, 372, 223.5, 50, 50, aspect_ratio=1)  
            c.saveState()  
  
            if not expedited_order:  
                EX_x = 7  
                EX_y = 250  
                EX_square_size = 27  
                c.setFillColorRGB(1, 1, 1)  
                c.setStrokeColorRGB(1, 1, 1)  
                c.rect(EX_x, EX_y, EX_square_size, EX_square_size, fill=1)  
  
            ML_x = 36  
            ML_y = 250  
            ML_square_size = 27  
            c.setFillColorRGB(1, 1, 1)  
            c.setStrokeColorRGB(1, 1, 1)  
            c.rect(ML_x, ML_y, ML_square_size, ML_square_size, fill=1)  
  
            if not multi_order:  
                MO_x = 7  
                MO_y = 219  
                MO_square_size = 27  
                c.setFillColorRGB(1, 1, 1)  
                c.setStrokeColorRGB(1, 1, 1)  
                c.rect(MO_x, MO_y, MO_square_size, MO_square_size, fill=1)  
  
            if not duplicate_order:  
                DO_x = 36  
                DO_y = 219  
                DO_square_size = 27  
                c.setFillColorRGB(1, 1, 1)  
                c.setStrokeColorRGB(1, 1, 1)  
                c.rect(DO_x, DO_y, DO_square_size, DO_square_size, fill=1)  
  
            font_size_custom_field = 8  
            c.setFont("CODE Bold", font_size_custom_field)  
            c.setFillColorRGB(0, 0, 0)  
            wrapped_custom_field_3 = textwrap.wrap(str(custom_field_3), width=10)  
            text_object_custom_field_3 = c.beginText(70, 255)  
            for line in wrapped_custom_field_3:  
                text_object_custom_field_3.textLine(line)  
            c.drawText(text_object_custom_field_3)  
  
            c.drawString(70, 225, order_date)  
            wrapped_sku = textwrap.wrap(str(sku), width=15)  
            text_object_sku = c.beginText(10, y_position)  
            for line in wrapped_sku:  
                text_object_sku.textLine(line)  
            c.drawText(text_object_sku)  
  
            c.drawString(100, y_position, f"{item_qty}")  
  
            outside_inscription = ""  
            inside_inscription = ""  
            if sku.startswith("BCT") or sku.startswith("RWTF") or sku.startswith("DLTH"):  
                outside_match = re.search(r'Outside Inscription:\s*([\s\S]+?)(?:,|$)', item_options)  
                inside_match = re.search(r'Inside Inscription:\s*([\s\S]+?)(?:,|$)', item_options)  
                if outside_match:  
                    outside_inscription = outside_match.group(1).strip()  
                if inside_match:  
                    inside_inscription = inside_match.group(1).strip()  
  
            if sku.startswith("SRN"):  
                item_list_description = f"Personalization: ({personalization_text}), Total Order Amount: ({item_qty} of {order_total_qty}), Type: {item_name}"  
            elif sku.startswith("BNCK"):  
                item_list_description = f"Personalization: ({personalization_text}), Total Order Amount: ({item_qty} of {order_total_qty}), Type: {item_name}"  
            elif sku.startswith("BCT") or sku.startswith("RWTF") or sku.startswith("DLTH"):  
                item_list_description = f"Outside Inscription: ({outside_inscription}) Inside Inscription: ({inside_inscription}), Total Order Amount: ({item_qty} of {order_total_qty}), Type: {item_name}"
            else:  
                item_list_description = f"Total Order Amount: ({item_qty} of {order_total_qty}), Type: {item_name}, Location: ({location_text})"  
  
            bounding_box_width = 300  
            wrapped_item_name = simpleSplit(item_list_description, "CODE Bold", 8, bounding_box_width)  
            text_object = c.beginText(122, y_position)  
            for line in wrapped_item_name:  
                text_object.textLine(line)  
            c.drawText(text_object)  
  
            order_number_str = "*" + str(order_number).strip('"') + "*"  
            font_size_order_number = 42  
            c.setFillColorRGB(0, 0, 0)  
            c.setFont("fre3of9x", font_size_order_number)  
            page_width = letter[0]  
            text_width = c.stringWidth('*' + order_number + '*', "fre3of9x", font_size_order_number)  
            x_coordinate = ((page_width - text_width) // 2) - 95  
            c.drawString(x_coordinate, 240, order_number_str)  
  
            c.setFont("CODE Bold", 15)  
            c.drawString(170, 225, order_number)  
  
            y_position -= 50  
            current_item_count += 1  
  
        draw_page_number(c, page_number, total_pages, 10, 10)  
        c.save()  
  
        background_pdf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'label', 'side_label.pdf')  
        background_reader = PdfReader(background_pdf_path)  
        background_page = background_reader.pages[0]  
  
        label_reader = PdfReader(temp_pdf_path)  
        label_pages = label_reader.pages  
  
        writer = PdfWriter()  
        for label_page in label_pages:  
            new_page = PageObject.create_blank_page(width=background_page.mediabox.width, height=background_page.mediabox.height)  
            new_page.merge_page(background_page)  
            new_page.merge_page(label_page)  
            writer.add_page(new_page)  
  
        label_name = f"{sku}_{first_lineID}_{order_number}.pdf"  
        label_path = os.path.join(sub_folder_path, label_name)  
        os.makedirs(sub_folder_path, exist_ok=True)  
        with open(label_path, 'wb') as f:  
            writer.write(f)  
    except Exception as e:  
        print(f"Error creating label: {e}")  
