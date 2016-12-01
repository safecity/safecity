top_left = (42.187280, -88.043792)
top_right = (42.187280, -87.454202)
bottom_left = (41.591199, -88.043792)
bottom_right = (41.591199, -87.454202)

total_box_width = 10000
total_box_height = 10000

long_inc = (top_right[1] - top_left[1]) / total_box_width
lat_inc = (top_left[0] - bottom_left[0]) / total_box_height


# TODO: This is not a good method for partitioning. Search for a better method
# that divides the area equally

def get_box_index(latitude, longitude):
    """
    splits the area around chicago into boxes...returns the box index from
    latitude and longitude
    """
    x = int((longitude - top_left[1]) / long_inc)
    y = int((latitude - bottom_left[0]) / lat_inc)
    return (x, y)
