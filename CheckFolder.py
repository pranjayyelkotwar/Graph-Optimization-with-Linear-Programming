import csv
import sys
import os 
import shutil

def process_csv(csv_file_path):
    # Create dictionaries
    course_dict = {}
    prof_dict = {}

    # Read data from CSV file, skipping the header
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row

        # First loop: Build Course dictionary
        for row in csv_reader:
            course_name, prof_info = row[0], row[1]

            # Extracting prof category and name

            # Update Course dictionary
            if course_name not in course_dict:
                course_dict[course_name] = [prof_info]
            else:
                course_dict[course_name].append(prof_info)
        
        # Second loop: Build Prof dictionary
        for course_name, profs_list in course_dict.items():
            for prof_name in profs_list:
                if prof_name not in prof_dict:
                    prof_dict[prof_name] = 0.5 if len(profs_list) == 2 else 1.0
                else:
                    prof_dict[prof_name] += 0.5 if len(profs_list) == 2 else 1.0
    
    # Check if limit for every prof is equal to their category_limit
    for prof_name, limit in prof_dict.items():
        category = prof_name[:2]
        category_limit = 0.5 if category == 'X1' else 1.0 if category == 'X2' else 1.5

        if limit != category_limit:
            return 0

    return 1

# Function to check if a file is a valid CSV file
def is_valid_csv(file_path):
    try:
        return process_csv(file_path)
    except Exception as e:
        print(f"Invalid CSV file: {file_path} - {str(e)}")
        return False

# Function to process all CSV files in a directory
def process_directory(input_directory):
    # Check if the directory exists
    if not os.path.exists(input_directory):
        print(f"Directory not found: {input_directory}")
        return
    
    # Create a new directory for valid files
    output_directory = f"{input_directory}_final"
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over each file in the directory
    for file_name in os.listdir(input_directory):
        input_file_path = os.path.join(input_directory, file_name)

        # Check if the file is a CSV file and if it's valid
        if file_name.endswith(".csv") and is_valid_csv(input_file_path):
            print(f"Valid CSV file: {file_name}")

            # Copy the valid file to the output directory
            output_file_path = os.path.join(output_directory, file_name)
            shutil.copyfile(input_file_path, output_file_path)

# Example usage:
if len(sys.argv) != 2:
    print("Usage: python script.py <input_directory>")
    sys.exit(1)

input_directory = sys.argv[1]
process_directory(input_directory)
