"""
Prepare.py
Prepares the dataset..Merges all the dataset to create one
master dataset
"""
import csv
from collections import defaultdict
from functions import get_box_index
from safecity import BlockInfo


def load_from_csv(filename, lat_index, long_index):
    first = False
    with open('data/' + filename, 'r') as csvfile:
        service_reader = csv.reader(csvfile)
        for row in service_reader:
            if not first:
                first = True
                continue
            try:
                latitude = row[lat_index].strip()
                longitude = row[long_index].strip()

                if len(latitude) < 5 or len(longitude) < 5:
                    continue
                # print(latitude, " and ", longitude)
                latitude = float(latitude)
                longitude = float(longitude)

                index = get_box_index(latitude, longitude)
                yield index, row
            except:
                raise


def load_service_requests(master_dataset):
    for index, row in load_from_csv('service_requests.csv', 13, 14):
        if "OPEN" in row[1].upper():
            master_dataset[index].open_services += 1
        else:
            master_dataset[index].closed_services += 1
    print("Service requests loaded")

def load_redlight_violations(master_dataset):
    """
    Loads the redlight traffic violation data. NOTE: Redlight violation is concentrated
    in crossing and other places. This needs to be spread out by increasing the count
    of surrounding blocks also. Weightage can be given to blocks near the block containing
    traffic light
    """
    for index, row in load_from_csv('redlight_violations.csv', 7, 8):
        master_dataset[index].redlight_violations += 1
    print("Redlight violations dataset loaded")



def prepare_dataset():
    master_table = defaultdict(BlockInfo)
    load_service_requests(master_table)
    load_redlight_violations(master_table)

    # Process the rows if necessary
    for index, block in master_table.items():
        block.index = index

    # Write the master table in csv file
    print("Writing into output file")

    with open('data/master.csv', 'w', newline='') as csvfile:
        scwriter = csv.writer(csvfile)

        BlockInfo.output_header(scwriter)
        for index, block in master_table.items():
            block.output_csv(scwriter)
