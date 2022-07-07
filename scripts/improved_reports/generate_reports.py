#!/usr/bin/env python

'''
REQUIREMENTS:
Generate a Top Times Report of the Improvements for all boys and girls of all ages.  Only use times 'After Since Date' 
of the first swim meet.  Rather than saving the report as a PDF, this time save it as a CSV file.  Set Delimeter 
to empty/blank and Separator to ','.  Name the csv file as boys-girls-all-improved.csv and save it to the same 
directory as this script and run it like the example shows below.

EXAMPLE:
$ python generate_reports.py
07/07/2022 11:08:12AM INFO: There are 449 records found.
07/07/2022 11:08:12AM INFO: Here are the winners!
[('0-6',
  {'Boy': {'age': '4', 'name': 'Harrison Marcus', 'percentage': 38.21},
   'Girl': {'age': '4', 'name': 'Kennedy Willse', 'percentage': 42.43}}),
 ('11-12',
  {'Boy': {'age': '11', 'name': 'Blake Schader', 'percentage': 12.22},
   'Girl': {'age': '11', 'name': 'Taylor Yeats', 'percentage': 6.73}}),
 ('13-14',
  {'Boy': {'age': '13', 'name': 'Connor Yeats', 'percentage': 5.38},
   'Girl': {'age': '13', 'name': 'Courtney White', 'percentage': 6.97}}),
 ('15-18',
  {'Boy': {'age': '15', 'name': 'Sean Gwin', 'percentage': 3.31},
   'Girl': {'age': '18', 'name': 'Megan Campagna', 'percentage': 8.03}}),
 ('7-8',
  {'Boy': {'age': '7', 'name': 'Juyoung Park', 'percentage': 26.9},
   'Girl': {'age': '7', 'name': 'Ajuni Mann', 'percentage': 14.44}}),
 ('9-10',
  {'Boy': {'age': '9', 'name': 'Jeremy Salmon', 'percentage': 12.02},
   'Girl': {'age': '10', 'name': 'Sahaani Mann', 'percentage': 12.84}})]


'''

import pprint
import logging

def parse_csv(csv_file):
    with open(csv_file, 'r') as file:
        values = file.readlines()

    all_records = {}
    all_records_by_swimmer = {}
    index = 0
    for item1 in values:
        record = item1.split(',')
        logging.debug(record)
        all_records[index] = record
        index = index + 1

    logging.info(f"There are {len(all_records)} records found.")
    logging.debug(f"These are all the records: {all_records}")

    # Convert B to Boy and G to Girl
    genders = {
        "B": "Boy",
        "G": "Girl"
    }

    improvement_index = 0

    # Initialize all_records_by_swimmer first
    for key, value in all_records.items():
        logging.debug(f"\n\nFULL RECORD: {all_records[key]}")
        swimmer = all_records[key][12].split()
        improvement = all_records[key][20]

        swimmer_name = ' '.join(swimmer[0:2])
        logging.debug(f"Swimmer name: {swimmer_name}")

        all_records_by_swimmer[swimmer_name] = {}

    # Now populate the records
    for key, value in all_records.items():
        logging.debug(f"\n\nFULL RECORD: {all_records[key]}")
        swimmer = all_records[key][12].split()
        improvement = all_records[key][20]

        swimmer_name = ' '.join(swimmer[0:2])
        logging.debug(f"Swimmer name: {swimmer_name}")


        swimmer_age = ' '.join(swimmer[2:3]).strip('()')
        logging.debug(f"Swimmer age: {swimmer_age}")

        if not swimmer_age.isdigit():
            swimmer_age = ' '.join(swimmer[3:4]).strip('()')
            swimmer_gender = genders[' '.join(swimmer[4:5])]
        else:
            swimmer_gender = genders[' '.join(swimmer[3:4])]

        logging.debug(f"Swimmer gender: {swimmer_gender}")

        swimmer_improvement_percent = improvement

        logging.debug(f"Swimmer improvement: {swimmer_improvement_percent}%")

        try:
            if all_records_by_swimmer[swimmer_name][improvement_index]:
                improvement_index = improvement_index + 1
        except Exception as e:
            logging.debug(f"This is the first entry for this swimmer: {swimmer_name}")
            improvement_index = 0

        logging.debug(f"Improvement_index is: {improvement_index}")

        logging.debug(f"All Records By Swimmer {swimmer_name}: {all_records_by_swimmer[swimmer_name]}")
        all_records_by_swimmer[swimmer_name]['age'] = swimmer_age
        all_records_by_swimmer[swimmer_name]['gender'] = swimmer_gender
        all_records_by_swimmer[swimmer_name][improvement_index] = swimmer_improvement_percent

    logging.debug(f"All records by swimmer: {all_records_by_swimmer}")
    logging.debug(f"There are this many Records By Swimmer: {len(all_records_by_swimmer)}")
    return all_records_by_swimmer

def get_avgs(avg_values):
    for key, value in avg_values.items():
        total_times = len(value) - 2
        for i in range(0,total_times):
            try:
                avg_values[key]['average'] = round(float(avg_values[key]['average']) + float(avg_values[key][i]) / float(total_times), 2)
            except Exception as e:
                logging.debug(f"This is the first avg value for swimmer: {key} ")
                avg_values[key]['average'] = round(float(avg_values[key][i]) / float(total_times), 2)

        logging.debug(f"Avg values at key {key} is: {avg_values[key]}")
        logging.debug(f"There are {total_times} number of improved times percentages for swimmer: {key}")

    logging.debug(f"All avg values are: {avg_values}")

    return avg_values

def print_report(full_averages_report):
    winners = {
        '0-6': {'Boy': {'name': "", "percentage": "", "age": ""}, 'Girl': {'name': "", "percentage": "", "age": ""}},
        '7-8': {'Boy': {'name': "", "percentage": "", "age": ""}, 'Girl': {'name': "", "percentage": "", "age": ""}},
        '9-10': {'Boy': {'name': "", "percentage": "", "age": ""}, 'Girl': {'name': "", "percentage": "", "age": ""}},
        '11-12': {'Boy': {'name': "", "percentage": "", "age": ""}, 'Girl': {'name': "", "percentage": "", "age": ""}},
        '15-18': {'Boy': {'name': "", "percentage": "", "age": ""}, 'Girl': {'name': "", "percentage": "", "age": ""}},
        '13-14': {'Boy': {'name': "", "percentage": "", "age": ""}, 'Girl': {'name': "", "percentage": "", "age": ""}}
    }
    for key, value in full_averages_report.items():

        for x in winners.keys():
            logging.debug(f"Key is: {x}")
            age_list = list(x)
            dash_index = age_list.index('-')
            low_age = ''.join(age_list[0:dash_index])
            high_age = ''.join(age_list[dash_index+1:])

            # AGES 6 & Under Boys
            logging.debug(f"Ages are: low {low_age} and high {high_age}")
            if int(full_averages_report[key]['age']) >= int(low_age) and int(full_averages_report[key]['age']) <= int(high_age): # and full_averages_report[key][gender] == 'Boy':
                try:
                    if full_averages_report[key]['average'] > winners[x][full_averages_report[key]['gender']]['percentage']:
                        winners[x][full_averages_report[key]['gender']]['name'] = key
                        winners[x][full_averages_report[key]['gender']]['percentage'] = value['average']
                        winners[x][full_averages_report[key]['gender']]['age'] = value['age']
                except Exception as e:
                    logging.debug(f"There are no {full_averages_report[key]['gender']} entries in the winners for this age group yet: {full_averages_report[key]['age']}")
                    winners[x][full_averages_report[key]['gender']]['name'] = key
                    winners[x][full_averages_report[key]['gender']]['percentage'] = value['average']

    logging.info(f"Here are the winners!")
    pprint.pprint(sorted(winners.items()))

    return winners

def set_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S%p",
        level=logging.INFO,
    )
    return True

def main():
    set_logging()
    csv_file = 'boys-girls-all-improved.csv'
    raw_values = parse_csv(csv_file)
    averages = get_avgs(raw_values)
    print_report(averages)

if __name__ == '__main__':
    main()
