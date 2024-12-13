# create_labels.py
  
from config import *  
from reportlab.pdfgen import canvas  
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont  
from reportlab.lib.pagesizes import letter  
from reportlab.lib.utils import simpleSplit  
from PyPDF2 import PdfReader, PdfWriter  
from reportlab.lib.utils import ImageReader  
from wand.image import Image as WandImage  
from PIL import Image as PILImage 

# Barcode font  
IDAutomationHC39M_font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'IDAutomationHC39M.ttf')  
pdfmetrics.registerFont(TTFont("IDAutomationHC39M", IDAutomationHC39M_font_path))  
  
# Montserrat font  
Montserrat_font_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts', 'Montserrat.ttf')  
pdfmetrics.registerFont(TTFont("Montserrat-Regular", Montserrat_font_path))  
  
def create_label(order_number, sku, qty_index, base_folder_name, custom_field_3, timestamp, item_qty, order_quantities, order_skus, personalization_text, outside_inscription, inside_inscription, item_name, order_date, lineID, sub_folder_path, image_path=None):  
    try:  
        # Draw a QR code image on the canvas  
        def process_qr_image(qr_img, x, y, new_width, new_height, aspect_ratio=None):  
            img_width, img_height = qr_img.size  
            padding_to_remove = 10  
            crop_box = (padding_to_remove, padding_to_remove, img_width - padding_to_remove, img_height - padding_to_remove)  
            qr_img = qr_img.crop(crop_box)  
            img_width, img_height = qr_img.size  
  
            if not aspect_ratio:  
                aspect_ratio = float(img_width) / float(img_height)  
  
            qr_img = qr_img.resize((new_width, new_height), PILImage.LANCZOS)  
            c.drawImage(ImageReader(qr_img), x, y, new_width, new_height)  
  
        def generate_order_number_qr(lineID, box_size=3, border=4.5):  
            qr = qrcode.QRCode(  
                version=1,  
                error_correction=qrcode.constants.ERROR_CORRECT_L,  
                box_size=box_size,  
                border=border,  
            )  
            qr.add_data(lineID)  
            qr.make(fit=True)  
            qr_order_number_img = qr.make_image(fill_color="black", back_color="white")  
            return qr_order_number_img  
  
        # Create a temporary PDF to draw the label on  
        temp_pdf_path = os.path.join(tempfile.gettempdir(), 'temp_label.pdf')  
        c = canvas.Canvas(temp_pdf_path, pagesize=letter)  
        c.setFont("Montserrat-Regular", 8)  
        c.setFillColorRGB(0, 0, 0)  
  
        # Generate the QR code for the lineID  
        qr_order_number_img = generate_order_number_qr(lineID)  
  
        # Draw the order number QR code on the canvas with the desired size  
        process_qr_image(qr_order_number_img, 21.5, 370, 50, 50, aspect_ratio=1)  # (x, y, width, height)  
  
        # Save the current state of the canvas  
        c.saveState()  
  
        # Initialize common variables  
        order_total_qty = order_quantities.get(order_number, 0)  
        expedited_order = order_number[-1].upper() == 'R' or 'EXP' in order_number.upper()  
        duplicate_order = item_qty > 1  
        multi_order = order_total_qty > 1  
        processed_font_color = (0, 0, 0)  
  
        if sku.startswith("NCK") or sku.startswith("RNG"):  
            # Load the background PDF  
            background_pdf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'background', 'label', 'blank_clabel.pdf')  
  
            # EXPEDITED white square  
            if not expedited_order:  
                EX_x = 211  
                EX_y = 397  
                EX_square_size = 27  
                c.setFillColorRGB(1, 1, 1)  
                c.setStrokeColorRGB(1, 1, 1)  
                c.rect(EX_x, EX_y, EX_square_size, EX_square_size, fill=1)  
  
            # MULTI LINE white square  
            ML_x = 241  
            ML_y = 397  
            ML_square_size = 27  
            c.setFillColorRGB(1, 1, 1)  
            c.setStrokeColorRGB(1, 1, 1)  
            c.rect(ML_x, ML_y, ML_square_size, ML_square_size, fill=1)  
  
            # MULTI ORDER white square  
            if not multi_order:  
                MO_x = 211  
                MO_y = 367  
                MO_square_size = 27  
                c.setFillColorRGB(1, 1, 1)  
                c.setStrokeColorRGB(1, 1, 1)  
                c.rect(MO_x, MO_y, MO_square_size, MO_square_size, fill=1)  
  
            # DUPLICATE ORDER white square  
            if not duplicate_order:  
                DO_x = 241  
                DO_y = 367  
                DO_square_size = 27  
                c.setFillColorRGB(1, 1, 1)  
                c.setStrokeColorRGB(1, 1, 1)  
                c.rect(DO_x, DO_y, DO_square_size, DO_square_size, fill=1)  
  
            # Draw the custom field 3  
            font_size_custom_field = 8  
            c.setFont("Montserrat-Regular", font_size_custom_field)  
            c.setFillColorRGB(*processed_font_color)  
            c.drawString(20, 340, str(custom_field_3))  
  
            # Draw the date  
            c.drawString(210, 340, order_date)  
  
            # Draw the quantity  
            font_size_qty = 8  
            c.setFont("Montserrat-Regular", font_size_qty)  
            c.setFillColorRGB(*processed_font_color)  
            c.drawString(20, 137, f"{item_qty}")  
  
            # Draw the item name  
            font_size_item_name = 8  
            c.setFont("Montserrat-Regular", font_size_item_name)  
            c.setFillColorRGB(*processed_font_color)  
            if "Modern" in item_name:  
                item_list_description = f"SKU: {sku}, Personalization: ({personalization_text}), Total Order Amount: ({item_qty} of {order_total_qty}), Type: {item_name}, BOX CHAIN"  
            else:  
                item_list_description = f"SKU: {sku}, Personalization: ({personalization_text}), Total Order Amount: ({item_qty} of {order_total_qty}), Type: {item_name}"  
            bounding_box_width = 200  
            wrapped_item_name = simpleSplit(item_list_description, "Montserrat-Regular", font_size_item_name, bounding_box_width)  
            text_object = c.beginText(50, 137)  
            for line in wrapped_item_name:  
                text_object.textLine(line)  
            c.drawText(text_object)  
  
            # Draw the order number  
            order_number_str = "*" + str(order_number).strip('"') + "*"  
            font_size_order_number = 16  
            c.setFillColorRGB(*processed_font_color)  
            c.setFont("IDAutomationHC39M", font_size_order_number)  
            page_width = letter[0]  
            text_width = c.stringWidth('*' + order_number + '*', "IDAutomationHC39M", font_size_order_number)  
            x_coordinate = ((page_width - text_width) // 2) - 160  
            c.drawString(x_coordinate, 15, order_number_str)  
  
            c.save()  
  
            # Read the background PDF  
            background_reader = PdfReader(background_pdf_path)  
            background_page = background_reader.pages[0]  
  
            # Read the temporary PDF with the drawn elements  
            label_reader = PdfReader(temp_pdf_path)  
            label_page = label_reader.pages[0]  
  
            # Merge the temporary PDF with the background PDF  
            background_page.merge_page(label_page)  
  
            # Save the final label PDF in the specified subfolder path  
            label_name = f"{sku}_{lineID}_{order_number}.pdf"  
            label_path = os.path.join(sub_folder_path, label_name)  
  
            os.makedirs(sub_folder_path, exist_ok=True)  
  
            # Overlay the downloaded image if provided  
            if image_path:  
                with WandImage(filename=image_path, resolution=300) as img:  
                    overlay_image = img.convert('png')  
  
                    # Calculate the aspect ratio and determine the new dimensions within the bounding box  
                    fetched_width, fetched_height = img.size  
                    aspect_ratio = float(fetched_width) / float(fetched_height)  
                    if sku.startswith("NCK"):  
                        new_width = min(fetched_width, 180)  # bounding box width  
                        new_height = int(new_width / aspect_ratio)  
  
                        if new_height > 180:  # bounding box height  
                            new_height = 180  
                            new_width = int(new_height * aspect_ratio)  
  
                        # Convert Wand Image to PIL.Image  
                        overlay_image_blob = overlay_image.make_blob('png')  
                        overlay_image_pil = PILImage.open(io.BytesIO(overlay_image_blob)).convert("RGBA")  
  
                        # Save the PIL.Image to a temporary file  
                        temp_image_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')  
                        overlay_image_pil.save(temp_image_file.name)  
  
                        # Create a canvas for the resized PDF
                        if sku.startswith("NCKGLD") or sku.startswith("NCKSIL") or sku.startswith("NCKRSG"): 
                            position_x, position_y = 55, 115   
                        elif sku.startswith("NCK02"): 
                            position_x, position_y = 55, 135
                        elif sku.startswith("NCK03"): 
                            position_x, position_y = 55, 155   
                        else:
                            position_x, position_y = 55, 165  
                        
                        c = canvas.Canvas("temp_overlay.pdf", pagesize=letter) 

                    elif sku.startswith("RNG"):  
                        new_width = min(fetched_width, 200)  # bounding box width  
                        new_height = int(new_width / aspect_ratio)  
  
                        if new_height > 200:  # bounding box height  
                            new_height = 200  
                            new_width = int(new_height * aspect_ratio)  
  
                        # Convert Wand Image to PIL.Image  
                        overlay_image_blob = overlay_image.make_blob('png')  
                        overlay_image_pil = PILImage.open(io.BytesIO(overlay_image_blob)).convert("RGBA")  
  
                        # Save the PIL.Image to a temporary file  
                        temp_image_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')  
                        overlay_image_pil.save(temp_image_file.name)  
  
                        # Create a canvas for the resized PDF  
                        position_x, position_y = 40, 240  
                        c = canvas.Canvas("temp_overlay.pdf", pagesize=letter)  
                    else:  
                        new_width = min(fetched_width, 320)  # bounding box width  
                        new_height = int(new_width / aspect_ratio)  
  
                        if new_height > 320:  # bounding box height  
                            new_height = 320  
                            new_width = int(new_height * aspect_ratio)  
  
                        # Convert Wand Image to PIL.Image  
                        overlay_image_blob = overlay_image.make_blob('png')  
                        overlay_image_pil = PILImage.open(io.BytesIO(overlay_image_blob)).convert("RGBA")  
  
                        # Save the PIL.Image to a temporary file  
                        temp_image_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')  
                        overlay_image_pil.save(temp_image_file.name)  
  
                        # Create a canvas for the resized PDF  
                        position_x, position_y = -15, 210  
                        c = canvas.Canvas("temp_overlay.pdf", pagesize=letter)  
  
                    # Draw the overlaying PDF image on the canvas within the bounding box  
                    c.drawImage(temp_image_file.name, position_x, position_y, width=new_width, height=new_height, mask='auto')  
                    c.save()  
  
                    # Merge the temporary overlay PDF with the original PDF  
                    overlay_reader = PdfReader("temp_overlay.pdf")  
                    overlay_page = overlay_reader.pages[0]  
                    background_page.merge_page(overlay_page)  
  
                    # Clean up the temporary file  
                    overlay_image_pil.close()  
                    os.close(temp_image_file.file.fileno())  
                    os.remove(temp_image_file.name)  
                    os.remove("temp_overlay.pdf")  
  
            with open(label_path, 'wb') as f:  
                writer = PdfWriter()  
                writer.add_page(background_page)  
                writer.write(f)  
  
    except Exception as e:  
        print(f"Error creating label: {e}") 
