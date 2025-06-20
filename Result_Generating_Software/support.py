from PIL import Image, ImageDraw, ImageFont
import os
import pandas as pd


class Get_requirements:
    def get_csv():
        # Use os.path.join for cross-platform path handling
        input_dir = os.path.join(os.getcwd(), "Input")
        
        # Add a check to ensure the directory exists before listing
        if not os.path.isdir(input_dir):
            print(f"Error: Input directory not found at {input_dir}")
            return None # Or raise an error
            
        for file in os.listdir(input_dir):
            if file.endswith(".csv"):
                csv_name = os.path.join(input_dir, file)
                print("CSV File Found!")
                return Get_requirements.sort_csv(csv_name)
        print(f"Error: No CSV file found in {input_dir}\nTry to RESTART SCRIPT after putting the CSV File")
        return None # Return None or raise an exception if no CSV is found
    
    def get_img():
        # Use os.path.join for cross-platform path handling
        input_dir = os.path.join(os.getcwd(), "Input")

        # Add a check to ensure the directory exists before listing
        if not os.path.isdir(input_dir):
            print(f"Error: Input directory not found at {input_dir}")
            return None # Or raise an error

        for file in os.listdir(input_dir):
            # Corrected the condition to properly check for .png OR .jpg
            if file.endswith(".png") or file.endswith(".jpg"):
                img_name = os.path.join(input_dir, file)
                print("Image File Found!")
                return img_name
        print(f"Error: No image file (.png or .jpg) found in {input_dir}")
        return None # Return None or raise an exception if no image is found
            
    def sort_csv(name):
        # Your existing pandas sorting logic (which is cross-platform)
        df = pd.read_csv(name)
        df['Marks'] = pd.to_numeric(df['Marks'], errors='coerce')
        df = df.sort_values(by='Marks', ascending=False).reset_index(drop=True)

        ranked_data = []
        current_rank = 1
        previous_marks = None

        for idx, row in df.iterrows():
            marks = row['Marks']
            full_name = row['Full Name']
            gr_no = row['GR.No']

            if idx > 0 and marks < previous_marks:
                current_rank = idx + 1
            
            ranked_data.append([current_rank, full_name, marks, gr_no])
            previous_marks = marks

        print("CSV File Sorted with Positions!")
        return ranked_data