from geopy.distance import vincenty

top_left = (42.187280, -88.043792)
top_right = (42.187280, -87.454202)
bottom_left = (41.591199, -88.043792)
bottom_right = (41.591199, -87.454202)

total_box_width = 1000
total_box_height = 1000

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


if __name__ == "__main__":
    # We assume that fixed value increase of latitude and longitude correspond to fixed
    # increase in distance. That is not true. But, for a small geographical error,
    # like a city, the error is negligible

    print(vincenty(bottom_left, (bottom_left[0]+lat_inc, bottom_left[1]))," increase per block")
    print(vincenty(bottom_left, (bottom_left[0], bottom_left[1] + long_inc))," increase per block")

    print(vincenty(bottom_right, (bottom_right[0] + 24000 * 0.00001, bottom_right[1])))
    print(vincenty(top_left, (top_left[0] - 24000 * 0.00001, top_left[1])))
    print()
    print(vincenty(bottom_left, (bottom_left[0], bottom_left[1] - 2400 * 0.00001)))
    print(vincenty(top_left, (top_left[0], top_left[1] - 2400 * 0.00001)))


    print(get_box_index(*top_right))
    print(get_box_index(*top_left))
    print(get_box_index(*bottom_left))
    print(get_box_index(*bottom_right))

