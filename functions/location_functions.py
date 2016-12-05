from geopy.distance import vincenty

top_left = (42.187280, -88.043792)
top_right = (42.187280, -87.454202)
bottom_left = (41.591199, -88.043792)
bottom_right = (41.591199, -87.454202)

total_box_width = 1000
total_box_height = 1000

lat_inc = (top_left[0] - bottom_left[0]) / total_box_height
long_inc = (bottom_right[1] - bottom_left[1]) / total_box_width


def get_box_index(latitude, longitude):
    """
    splits the area around chicago into boxes...returns the box index from
    latitude and longitude

    return (x,y) where x increases with longitude and y increases with latitude
    """
    x = int((longitude - bottom_left[1]) / long_inc)
    y = int((latitude - bottom_left[0]) / lat_inc)
    return (x, y)


def get_latitude_longitude(x, y):
    """
    Returns latitude and longitude vlaue from block index values
    """
    longitude = bottom_left[1] + (x * long_inc) + (long_inc / 2)
    latitude = bottom_left[0] + (y * lat_inc) + (lat_inc / 2)

    return (latitude, longitude)


if __name__ == "__main__":
    # We assume that fixed value increase of latitude and longitude correspond to fixed
    # increase in distance. That is not true. But, for a small geographical error,
    # like a city, the error is negligible

    print(vincenty(bottom_left, (bottom_left[
          0] + lat_inc, bottom_left[1])), " increase per block")
    print(vincenty(bottom_left, (bottom_left[0], bottom_left[
          1] + long_inc)), " increase per block")

    print(vincenty(bottom_right, (bottom_right[
          0] + 24000 * lat_inc, bottom_right[1])))
    print(vincenty(top_left, (top_left[0] - 24000 * lat_inc, top_left[1])))
    print()
    print(vincenty(bottom_left, (bottom_left[
          0], bottom_left[1] - 2400 * 0.00001)))
    print(vincenty(top_left, (top_left[0], top_left[1] - 2400 * 0.00001)))

    print(get_box_index(*top_right))
    print(get_box_index(*top_left))
    print(get_box_index(*bottom_left))
    print(get_box_index(*bottom_right))

    print("Testing reverse")

    position = (42.007280, -87.943792)
    print("Position is ", position)
    index = get_box_index(*position)
    print("Index is ", index)
    position = get_latitude_longitude(*index)
    print("Calculated position is ", position)
