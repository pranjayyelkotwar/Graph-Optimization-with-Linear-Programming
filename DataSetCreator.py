#This code helps us create the dataset for the model. The input is a csv file with the following format:
# Name, Category, Course1, Course2, Course3, Course4, Course5, Course6, Course7, Course8, Course9, Course10
# The first row is the header row, and the first column is the name of the professor. The second column is the category of the professor. The rest of the columns are the courses that the professor can teach, in order of preference. The output is a csv file with the following format:
# The input file name is hardcoded as input.csv on line 63
# The output file name is hardcoded as DataSet.csv on line 64

import csv
import sys

def parse_data(data):
    # Split the data into rows
    rows = data.split('\n')[0:]

    # Create a dictionary to store the information
    course_preferences = {}
    prof_names = []
    
    for row in rows:
        values = row.split(',')
        name = values[0]
        print(name)
        category = values[1]
        name = category + '_' + name
        if name not in prof_names:
            prof_names.append(name)

        for course in values[2:]:
            course_dict = {'Name': name, 'Preference': values.index(course) - 1, 'Category': values[1]}
            if course in course_preferences:
                course_preferences[course].append(course_dict)
            else:
                course_preferences[course] = [course_dict]

    for course in course_preferences:
        # Sort course_preferences[course] by preference
        course_preferences[course] = sorted(course_preferences[course], key=lambda i: i['Preference'])

    return course_preferences, prof_names

def parse_data_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        data = "\n".join(",".join(row) for row in reader)

    return parse_data(data)

def write_to_csv(course_dict, prof_names, output_file):
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        header_row = ['Courses'] + prof_names
        writer.writerow(header_row)
        #count should store number of courses profs are giving preference to , initialize with number of entries in a row

        # Write data rows
        for course, preferences in course_dict.items():
            row_data = [course]
            for prof_name in prof_names:
                preference = next((pref['Preference'] for pref in preferences if pref['Name'] == prof_name), 0)
                # Change preference from 1 to 10, 2 to 9, and so on
                if preference != 0:
                    preference = 11 - preference
                row_data.append(preference)
            writer.writerow(row_data)

input_file = sys.argv[1]
output_file = sys.argv[2]

course_dict, prof_names = parse_data_from_csv(input_file)
print(prof_names)
write_to_csv(course_dict, prof_names, output_file)
