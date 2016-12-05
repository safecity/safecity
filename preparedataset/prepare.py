"""
Prepare.py
Prepares the dataset..Merges all the dataset to create one
master dataset
"""
import csv
from collections import defaultdict
from functions import get_box_index
from safecity import BlockInfo

from datetime import datetime

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
    """
    Loads the service requests data. We only take three things into consideration : the
    number of open and closed service requests in a block, and if the request is closed,
    then the number of days it took to complete the request.
    """
    for index, row in load_from_csv('service_requests.csv', 13, 14):
        if "OPEN" in row[1].upper():
            master_dataset[index].open_services += 1
        else:
            master_dataset[index].closed_services += 1
            # Find the number of days it took to complete the request
            start_date = datetime.strptime(row[0], "%m/%d/%Y")
            complete_date = datetime.strptime(row[2], "%m/%d/%Y")

            number_days = (complete_date-start_date).days

            # Update the average service days
            master_dataset[index].average_service_days = (
                master_dataset[index].average_service_days + number_days) / 2

    print("Service requests loaded")


def load_average_traffic_count(master_dataset):
    """
    TODO: For average traffic count, it is better to increase the traffic volume count
    of surrounding blocks also...maybe create a gradient for certain distance.
    """
    for index, row in load_from_csv('avg_daily_traffic_count.csv', 6, 7):
        master_dataset[index].average_traffic_count += int(row[4])
    print("Average Traffic Count updated")


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


def load_police_stations(master_dataset):
    """
    Loads the police stations data
    """
    for index, row in load_from_csv('police_stations.csv', 12, 13):
        master_dataset[index].police_stations += 1
    print("Police Station dataset loaded")


def load_public_schools(master_dataset):
    """
    Loads the public school data
    """
    for index, row in load_from_csv('public_school_data.csv', 72, 73):
        pass
    print("Public school progress dataset loaded")


def load_affordable_housing(master_dataset):
    """
    Loads the affordable housing data
    """
    for index, row in load_from_csv('affordable_housing.csv', 11, 12):
        pass
    print("Affordable Housing dataset loaded")


def prepare_dataset():
    master_table = defaultdict(BlockInfo)
    load_service_requests(master_table)
    # load_redlight_violations(master_table)
    # load_average_traffic_count(master_table)
    # load_police_stations(master_table)
    # load_affordable_housing(master_table)
    # load_public_schools(master_table)
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
