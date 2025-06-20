from PIL import Image, ImageDraw, ImageFont
import os
import shutil
from support import *
import math
from colorama import init, Fore, Style

def load_config(config_path="config.txt"):
    config = {}
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                # Try to convert to int if possible
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
                    value = float(value)
                config[key] = value
    return config

# Initialize Colorama for Windows compatibility -- IMPORTANT: Do this first!
init(autoreset=True) # autoreset=True makes sure the color resets after each print

def load_base_image(config):
    img_path = Get_requirements.get_img()
    desired_page_width = int(config["desired_page_width"])
    desired_page_height = int(config["desired_page_height"])
    if img_path and os.path.exists(img_path):
        try:
            loaded_img = Image.open(img_path)
            if loaded_img.size == (desired_page_width, desired_page_height):
                print(f"Loaded base image from '{img_path}'.")
                return loaded_img
            else:
                print(Fore.YELLOW + f"Warning: Base image '{img_path}' has dimensions {loaded_img.size}, but expected {desired_page_width}x{desired_page_height}. \nCreating a blank image instead.")
        except Exception as e:
            print(Fore.YELLOW + f"Warning: Could not load base image '{img_path}'. Reason: {e}. Creating a blank image instead.")
    print(Fore.WHITE + f"Creating a blank base image of {desired_page_width}x{desired_page_height} (white background).")
    return Image.new('RGB', (desired_page_width, desired_page_height), color='white')

def check_fonts(config):
    font_path = config["font_path"]
    H_font_path = config["H_font_path"]
    if not os.path.exists(font_path):
        print(Fore.RED + Style.BRIGHT + f"Error: Font file '{font_path}' not found. Please ensure it's in the 'Input' folder.")
        exit()
    if not os.path.exists(H_font_path):
        print(Fore.RED + Style.BRIGHT + f"Error: Header font file '{H_font_path}' not found. Please ensure it's in the 'Input' folder.")
        exit()

def format_output_folder(output_folder):
    os.makedirs(output_folder, exist_ok=True)
    print(f"\nFormatting output folder: '{output_folder}'...")
    for item in os.listdir(output_folder):
        item_path = os.path.join(output_folder, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
            print(f"  Removed: {item}")
        except Exception as e:
            print(f"  Could not remove {item_path}. Reason: {e}")
    print("Output folder formatted.")

def center_text(draw, text, font, x1, y1, width, height, fill="black"):
    # Use getbbox for accurate text bounding box
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = x1 + (width - text_width) / 2 - bbox[0]
    text_y = y1 + (height - text_height) / 2 - bbox[1]
    draw.text((text_x, text_y), text, fill=fill, font=font)

def main():
    config = load_config()
    # Read config values
    font_path = config["font_path"]
    H_font_path = config["H_font_path"]
    font_size = int(config["font_size"])
    main_header_font_size = int(config["main_header_font_size"])
    sub_header_font_size = int(config["sub_header_font_size"])
    third_header_font_size = int(config["third_header_font_size"])
    header_y_pos1 = int(config["header_y_pos1"])
    header_y_pos2 = int(config["header_y_pos2"])
    header_y_pos3 = int(config["header_y_pos3"])
    col_widths = [int(x) for x in config["col_widths"].split(",")]
    headers = [x.strip() for x in config["headers"].split(",")]
    table_width = int(config["table_width"])
    x_start = int(config["x_start"])
    y_startp1 = int(config["y_startp1"])
    y_startp2 = int(config["y_startp2"])
    max_rows_page1 = int(config["max_rows_page1"])
    max_rows_page2 = int(config["max_rows_page2"])
    max_tables_per_page = int(config["max_tables_per_page"])
    cell_height = int(config["cell_height"])
    gap_between_tables = int(config["gap_between_tables"])
    output_folder = config["output_folder"]
    desired_page_width = int(config["desired_page_width"])
    desired_page_height = int(config["desired_page_height"])

    check_fonts(config)
    base_img = load_base_image(config)
    page_width, page_height = base_img.size

    print(Fore.CYAN + "\n--- First Page Header Text Inputs ---")
    main_header_text = input(Fore.CYAN + "Enter the MAIN header text (eg. Institute name): " + Style.RESET_ALL)
    sub_header_text = input(Fore.CYAN + "Enter the sub-header text (eg. Branch name): " + Style.RESET_ALL)
    third_header_text = input(Fore.CYAN + "Enter the third header text (eg. Gender / Optional): " + Style.RESET_ALL)

    data = Get_requirements.get_csv()
    if data is None:
        print(Fore.RED + Style.BRIGHT + "Error: CSV data not loaded from the 'Input' folder. Please check if the 'Input' folder exists and contains a .csv file. If it exists, try restarting the script.")
        exit()
    print(f"Total number of rows in data: {len(data)}")

    format_output_folder(output_folder)
    font = ImageFont.truetype(font_path, font_size)
    main_header_font = ImageFont.truetype(H_font_path, main_header_font_size)
    sub_header_font = ImageFont.truetype(H_font_path, sub_header_font_size)
    third_header_font = ImageFont.truetype(font_path, third_header_font_size)

    generated_pages_for_pdf = []
    table_count = 0
    current_row_index = 0
    page_count = 0

    # --- Determine y_startp1 dynamically based on third header presence ---
    third_header_present = bool(third_header_text.strip())
    if third_header_present:
        table_y_start = header_y_pos3 + third_header_font_size + 10
    else:
        table_y_start = header_y_pos2 + sub_header_font_size + 20
        max_rows_page1 = max_rows_page1 + 1

    while current_row_index < len(data) or (page_count == 0 and len(data) == 0):
        print(Fore.GREEN + Style.BRIGHT + f"\n--- Starting new page (Page {page_count + 1}) ---")
        img = base_img.copy()
        draw = ImageDraw.Draw(img)

        if page_count == 0:
            # Main header (largest, centered)
            center_text(draw, main_header_text, main_header_font, 0, header_y_pos1, page_width, main_header_font_size)
            # Sub-header (smaller, centered)
            center_text(draw, sub_header_text, sub_header_font, 0, header_y_pos2, page_width, sub_header_font_size)
            # Third header (cell font size, centered, underlined) if present
            if third_header_present:
                center_text(draw, third_header_text, third_header_font, 0, header_y_pos3, page_width, third_header_font_size)
                text_width = draw.textlength(third_header_text, font=third_header_font)
                text_x = (page_width - text_width) / 2
                text_y = header_y_pos3 + third_header_font_size
                draw.line(
                    [(text_x, text_y + 2), (text_x + text_width, text_y + 2)],
                    fill="black", width=2
                )

        tables_with_data_drawn_on_current_page = 0

        for t in range(max_tables_per_page):
            x_offset = x_start + t * (table_width + gap_between_tables)
            if page_count == 0:
                y_offset = table_y_start
                rows_per_table = max_rows_page1
            else:
                y_offset = y_startp2
                rows_per_table = max_rows_page2

            # Draw header row
            for i, header in enumerate(headers):
                x1 = x_offset + sum(col_widths[:i])
                width = col_widths[i]
                draw.rectangle([x1, y_offset, x1 + width, y_offset + cell_height], fill="#00a7e1")
                center_text(draw, header, third_header_font, x1, y_offset, width, cell_height)

            data_to_draw = data[current_row_index : current_row_index + rows_per_table]
            if data_to_draw:
                tables_with_data_drawn_on_current_page += 1
                for row_idx, row in enumerate(data_to_draw):
                    if len(row) < 4:
                        full_row = row + [''] * (4 - len(row))
                    else:
                        full_row = row[:4]
                    y = y_offset + (row_idx + 1) * cell_height
                    # Determine if this row is rank 1 (first position)
                    is_first_position = False
                    try:
                        is_first_position = int(full_row[0]) == 1
                    except Exception:
                        pass
                    for col_idx, item in enumerate(full_row):
                        x1 = x_offset + sum(col_widths[:col_idx])
                        width = col_widths[col_idx]
                        draw.rectangle([x1, y, x1 + width, y + cell_height], outline="black")
                        display_text = str(item)
                        # Default text color
                        text_color = "black"
                        if col_idx == 2:
                            if item is None or (isinstance(item, str) and not item.strip()):
                                display_text = "Absent"
                                text_color = "red"
                            else:
                                try:
                                    num_val = float(item)
                                    if math.isnan(num_val):
                                        display_text = "Absent"
                                        text_color = "red"
                                    elif num_val.is_integer():
                                        display_text = str(int(num_val))
                                    else:
                                        display_text = str(num_val)
                                except (ValueError, TypeError):
                                    display_text = "Absent"
                                    text_color = "red"
                        elif col_idx == 3:
                            display_text = str(item)
                            if not display_text.strip().startswith("#") and display_text.strip():
                                display_text = f"#{display_text}"
                        # If this row is first position, use header blue color
                        if is_first_position:
                            text_color = "#00a7e1"
                        center_text(draw, display_text, font, x1, y, width, cell_height, fill=text_color)
                current_row_index += len(data_to_draw)
                table_count += 1
            else:
                break

        if tables_with_data_drawn_on_current_page > 0 or (page_count == 0 and len(data) == 0):
            page_count += 1
            page_num_text = f"Page {page_count}"
            page_num_font = ImageFont.truetype(font_path, 20)
            page_num_text_width = draw.textlength(page_num_text, font=page_num_font)
            draw.text((page_width - page_num_text_width - 20, page_height - 30), page_num_text, fill="black", font=page_num_font)
            output_file_path = os.path.join(output_folder, f"Page_{page_count}.png")  # Save as PNG
            img.save(output_file_path, format="PNG")
            generated_pages_for_pdf.append(img.convert("RGB"))  # Ensure RGB for PDF
            print(Fore.GREEN + f"Page {page_count} saved to {output_file_path}. Total pages for PDF: {len(generated_pages_for_pdf)}")
        else:
            print(Fore.RED + "No new data was drawn on this page. Stopping page generation.")
            break

    print(Fore.GREEN + Style.BRIGHT + f"\n--- Script finished. Total pages generated: {page_count} ---")

    if generated_pages_for_pdf:
        pdf_path = os.path.join(output_folder, f"{main_header_text} {sub_header_text} {third_header_text}.pdf")
        first_image = generated_pages_for_pdf[0]
        other_images = generated_pages_for_pdf[1:]
        first_image.save(pdf_path, save_all=True, append_images=other_images, quality=95, resolution=100)
        print(Fore.GREEN + Style.BRIGHT + f"\nAll pages compiled into PDF: {pdf_path}")
    else:
        print(Fore.RED + "No pages were generated, so no PDF was created.")

if __name__ == "__main__":
    main()