from L3G.utility import *
from L3G.payments import *
def dot(v1, v2):
    sum = 0
    for x, y in zip(v1, v2):
        sum += x*y
    return sum

def derivative_of_payment_of_a(bids, payment, sensitivity_of_a):
    a, b, c, g = bids
    if a + b + c < g:
        return 0
    pa, pb, pc, pg = payment(bids)
    if pa == a:       # IR constraint of a binding
        return 1 # (1, 0, 0)
    elif pa == 0:
        return 0
    elif (pb == b or pb == 0) and (pc == c or pc == 0):     # IR constraint of b and c binding
        return 0
    elif pb == b or pb == 0:
        return dot(sensitivity_of_a(bids), (0.5, 0, -0.5))
    elif pc == c or pc == 0:
        return dot(sensitivity_of_a(bids), (0.5, -0.5, 0))
    else:
        return dot(sensitivity_of_a(bids), (2/3, -1/3, -1/3))

def sensitivity_vcg_of_a(bids):
    area = get_area(bids)
    if area in ["wxyz", "wxy"]:
        return (0, -1, -1)
    elif area in ["wxz", "sxyq"]:
        return (0, 0, -1)
    elif area in ["wyz", "sxzq"]:
        return (0, -1, 0)
    else:
        return (0, 0, 0)

def sensitivity_zero_of_a(bids):
    return (0, 0, 0)

def sensitivity_bid_of_a(bids):
    return (1, 0, 0)




def create_sensitivity_shapley_of_a():
    sens_shapley_dict = {}
    sens_shapley_dict["wxyz"] = (1 / 4, -1 / 4, -1 / 4)
    sens_shapley_dict["wxy"] = (1 / 4, -1 / 4, -1 / 4)
    sens_shapley_dict["wxz"] = (1 / 6, 0, -1 / 3)
    sens_shapley_dict["wyz"] = (1 / 6, -1 / 3, 0)
    sens_shapley_dict["wx"] = (1 / 6, 0, -1 / 3)
    sens_shapley_dict["wy"] = (1 / 6, -1 / 3, 0)
    sens_shapley_dict["wz"] = (1 / 12, -1 / 12, -1 / 12)
    sens_shapley_dict["w"] = (1 / 12, -1 / 12, -1 / 12)

    sens_shapley_dict["sxyq"] = (1 / 6, 0, -1 / 3)
    sens_shapley_dict["sxy"] = (1 / 12, -1 / 12, -1 / 12)
    sens_shapley_dict["sxzq"] = (1 / 6, -1 / 3, 0)
    sens_shapley_dict["sxz"] = (1 / 12, -1 / 12, -1 / 12)
    sens_shapley_dict["syzq"] = (0, 0, 0)
    sens_shapley_dict["syz"] = (0, 0, 0)
    sens_shapley_dict["sx"] = (1 / 12, -1 / 12, -1 / 12)
    sens_shapley_dict["sy"] = (0, 0, 0)
    sens_shapley_dict["sz"] = (0, 0, 0)
    sens_shapley_dict["s"] = (0, 0, 0)

    def sensitivity_shapley_of_a(bids):
        area = get_area(bids)
        return sens_shapley_dict[area]

    return sensitivity_shapley_of_a

def create_sensitivity_shapvcg_of_a():
    sens_shapley_dict = {}
    sens_shapley_dict["wxyz"] = (0, -1 / 4, -1 / 4)
    sens_shapley_dict["wxy"] = (0, -1 / 4, -1 / 4)
    sens_shapley_dict["wxz"] = (0, 0, -1 / 3)
    sens_shapley_dict["wyz"] = (0, -1 / 3, 0)
    sens_shapley_dict["wx"] = (0, 0, -1 / 3)
    sens_shapley_dict["wy"] = (0, -1 / 3, 0)
    sens_shapley_dict["wz"] = (0, -1 / 12, -1 / 12)
    sens_shapley_dict["w"] = (0, -1 / 12, -1 / 12)

    sens_shapley_dict["sxyq"] = (0, 0, -1 / 3)
    sens_shapley_dict["sxy"] = (0, -1 / 12, -1 / 12)
    sens_shapley_dict["sxzq"] = (0, -1 / 3, 0)
    sens_shapley_dict["sxz"] = (0, -1 / 12, -1 / 12)
    sens_shapley_dict["syzq"] = (0, 0, 0)
    sens_shapley_dict["syz"] = (0, 0, 0)
    sens_shapley_dict["sx"] = (0, -1 / 12, -1 / 12)
    sens_shapley_dict["sy"] = (0, 0, 0)
    sens_shapley_dict["sz"] = (0, 0, 0)
    sens_shapley_dict["s"] = (0, 0, 0)

    def sensitivity_shapley_of_a(bids):
        area = get_area(bids)
        return sens_shapley_dict[area]

    return sensitivity_shapley_of_a
