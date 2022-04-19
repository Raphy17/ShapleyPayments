
def get_area(bids):
    a, b, c, g = bids
    if g > a+b+c:
        return "G"
    if g > max(a, b, c):
        # wls
        area = "w"
        if g > a+b:
            area += "x"
        if g > a+c:
            area += "y"
        if g > b+c:
            area += "z"
    else:
        # sls
        area = "s"
        if g > a:
            area += "x"
        if g > b:
            area += "y"
        if g > c:
            area += "z"
        if g > min(a+b, a+c, b+c):
            area += "q"
    return area
