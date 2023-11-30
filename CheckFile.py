import csv , os , sys


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

if len(sys.argv) != 2:
    print("Usage: python script.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
if process_csv(input_file) == 1:
    print("Valid CSV file")
else:
    print("Invalid CSV file")
