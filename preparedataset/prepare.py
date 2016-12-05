"""
Prepare.py
Prepares the dataset..Merges all the dataset to create one
master dataset
"""
import csv
from collections import defaultdict
from functions import get_box_index, total_box_width, total_box_height
from safecity import BlockInfo
import os

from datetime import datetime


class DataLoader:

    def __init__(self, datadir="data"):
        self.datadir = datadir

        # Initialize the empty cells
        self.master_table = dict()
        for i in range(0, total_box_width + 1):
            for j in range(0, total_box_height + 1):
                self.master_table[(i, j)] = BlockInfo()
                self.master_table[(i,j)].index = (i,j)

                # Calculate and store the latitude and longitude of each block info
                # self.master_table[(i,j)] = BlockInfo

    def load_from_csv(self, filename, lat_index, long_index):
        """Loads the csv file lazily"""
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
                    # Make sure index is within bounds
                    x,y = index
                    if x<0 or x > total_box_width or y < 0 or y > total_box_height:
                        continue
                    yield index, row
                except:
                    # continue?
                    raise

    def load_service_requests(self):
        """
        Loads the service requests data. We only take three things into consideration : the
        number of open and closed service requests in a block, and if the request is closed,
        then the number of days it took to complete the request.
        """
        for index, row in self.load_from_csv('service_requests.csv', 13, 14):
            if "OPEN" in row[1].upper():
                self.master_table[index].open_services += 1
            else:
                self.master_table[index].closed_services += 1
                # Find the number of days it took to complete the request
                start_date = datetime.strptime(row[0], "%m/%d/%Y")
                complete_date = datetime.strptime(row[2], "%m/%d/%Y")

                number_days = (complete_date - start_date).days

                # Update the average service days
                self.master_table[index].average_service_days = (
                    self.master_table[index].average_service_days + number_days) / 2
        print("Service requests loaded")

    def load_average_traffic_count(self):
        """
        Loads the average traffic count of any block. Increases the count of surrounding blocks also
        """
        for index, row in self.load_from_csv('avg_daily_traffic_count.csv', 6, 7):
            x, y = index
            traffic_count = int(row[4])
            block_radius = 3
            neighbours = [(a, b) for a in
                          range(max(0, x - block_radius),
                                min(total_box_width, x + block_radius))
                          for b in
                          range(max(0, y - block_radius),
                                min(total_box_height, y + block_radius))
                          ]

            for neighbour in neighbours:
                if neighbour != index:
                    self.master_table[
                        neighbour].average_traffic_count += traffic_count / 2
                else:
                    self.master_table[
                        index].average_traffic_count += traffic_count
        print("Average Traffic Count Loaded")

    def load_redlight_violations(self):
        """
        Loads the redlight traffic violation data.
        """
        for index, row in self.load_from_csv('redlight_violations.csv', 7, 8):
            x, y = index
            block_radius = 3
            neighbours = [(a, b) for a in
                          range(max(0, x - block_radius),
                                min(total_box_width, x + block_radius))
                          for b in
                          range(max(0, y - block_radius),
                                min(total_box_height, y + block_radius))
                          ]

            for neighbour in neighbours:
                self.master_table[neighbour].redlight_violations += 1

        print("Redlight violations dataset loaded")

    def load_police_stations(self):
        """
        Loads the police stations data
        """
        for index, row in self.load_from_csv('police_stations.csv', 12, 13):
            self.master_table[index].police_stations += 1
        print("Police Station dataset loaded")

    def load_public_schools(self):
        """
        Loads the public school data
        """
        for index, row in self.load_from_csv('public_school_data.csv', 72, 73):
            pass
        print("Public school progress dataset loaded")

    def load_affordable_housing(self):
        """
        Loads the affordable housing data
        """
        for index, row in self.load_from_csv('affordable_housing.csv', 11, 12):
            pass
        print("Affordable Housing dataset loaded")

    def load_criminal_data(self):
        """
        Load the criminal dataset
        """
        for index, row in self.load_from_csv('crimes.csv', 19, 20):
            self.master_table[index].crimes_count += 1
            if(row[8].lower() == "true"):
                self.master_table[index].arrest_count += 1
            if(row[9].lower() == "true"):
                self.master_table[index].domestic_crimes += 1
        print("Crimes dataset loaded")

    def load_all(self):
        self.load_service_requests()
        self.load_average_traffic_count()
        self.load_redlight_violations()
        self.load_police_stations()
        self.load_public_schools()
        self.load_affordable_housing()
        self.load_criminal_data()
        print("All datasets loaded")

    def process(self):
        """Process the master table. For example, we can calculate the minimum distance
        from nearest school and police station here"""
        pass

    def write_all(self, filename="master.csv"):
        filepath = os.path.join(self.datadir, filename)
        with open(filepath, 'w', newline='') as csvfile:
            scwriter = csv.writer(csvfile)
            BlockInfo.output_header(scwriter)
            for i in range(0, total_box_width + 1):
                for j in range(0, total_box_height + 1):
                    index = (i,j)
                    block = self.master_table[index]
                    block.output_csv(scwriter)
        print("Output file written")


def prepare_dataset():
    data_loader = DataLoader()
    data_loader.load_all()
    # Write to file
    data_loader.write_all()
