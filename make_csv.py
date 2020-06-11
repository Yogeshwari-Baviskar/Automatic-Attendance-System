import csv
from csv import writer


def writedata_to_csv(course_id,records):
    filename = str(course_id) + '.csv'
    lines = [["Roll_no", "Name"]]
    for data in records:
        temp= [data['student_id'],data['student_name']]
        lines.append(temp)

    with open(filename, 'w') as w:
        writer = csv.writer(w, lineterminator='\n')
        writer.writerows(lines)

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def update_to_csv(course_id,records):
    filename = str(course_id) + '.csv'
    lines=records

    append_list_as_row(filename, lines)
