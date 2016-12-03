#SafeCity

##Instructions
Create a "data" directory and place the following files inside the directory (rename the files
as needed)

* [service_requests.csv](https://data.cityofchicago.org/Service-Requests/311-Service-Requests-Sanitation-Code-Complaints/me59-5fac)
* [redlight_violations.csv](https://data.cityofchicago.org/Transportation/Red-Light-Camera-Violations/spqx-js37)
* [avg_daily_traffic_count.csv](https://data.cityofchicago.org/Transportation/Average-Daily-Traffic-Counts/pfsx-4n4m)
* [police_stations.csv](https://data.cityofchicago.org/Public-Safety/Police-Stations/z8bn-74gv)
* [affordable_housing.csv](https://data.cityofchicago.org/Community-Economic-Development/Affordable-Rental-Housing-Developments/s6ha-ppgi)
* [public_school_data.csv](https://data.cityofchicago.org/Education/Chicago-Public-Schools-Progress-Report-Cards-2011-/9xs2-f89t)


Install python requirements

    pip3 install -r requirements.txt

Prepare the data

    python3 safecity.py --preparedata

This should create master.csv file inside "data" directory
