
class BlockInfo:
    """
    Contains information about a block
    """

    def __init__(self):
        # self.service_requests = 0
        self.open_services = 0
        self.closed_services = 0
        self.index = (0, 0)

    def output_csv(self, csvfile):
        csvfile.writerow(list(self.index) +
                         [self.open_services, self.closed_services])

    @staticmethod
    def output_header(csvfile):
        csvfile.writerow(["X", "Y", "Open services", "Closed Services"])
