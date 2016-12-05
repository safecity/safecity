class BlockInfo:
    """
    Contains information about a block
    """

    def __init__(self, latitude = -1, longitude = -1):
        # self.service_requests = 0
        self.open_services = 0
        self.closed_services = 0
        self.average_service_days = 0

        self.redlight_violations = 0

        self.index = (0, 0)

        self.average_traffic_count = 0
        self.police_stations = 0
        self.crimes_count = 0

        self.latitude = latitude
        self.longitude = longitude

    def output_csv(self, csvfile):
        csvfile.writerow(list(self.index) +
                         [self.open_services, self.closed_services, self.average_service_days, self.redlight_violations,
                          self.average_traffic_count, self.crimes_count])

    @staticmethod
    def output_header(csvfile):
        csvfile.writerow(["X", "Y", "Open services",
                          "Closed Services", "Average service complete days", "Traffic light violations",
                          "Avearge traffic volume count", "Number of crimes"])
