from L3G.utility import *
from decimal import *
from valueCreator import *

def payment_nearest(payment, bids):
    a, b,c, g = bids
    if g > a + b+c:
        return (0, 0,0, a+b+c)
    else:
        payments = payment(bids)

        delta = (g - payments[0] - payments[1] - payments[2])/3
        mrc_payments = [payments[0]+delta, payments[1]+delta,payments[2]+delta, 0]
        if mrc_payments[0] > a:
            mrc_payments[0] = a
            delta = (g-a-payments[1]-payments[2])/2
            mrc_payments[1] = payments[1] + delta
            mrc_payments[2] = payments[2] + delta
            if mrc_payments[1] > b:
                return (a, b, g-a-b, 0)
            if mrc_payments[2] > c:
                return (a, g-a-c, c, 0)
            return tuple(mrc_payments)
        if mrc_payments[1] > b:
            mrc_payments[1] = b
            delta = (g - b - payments[0] - payments[2]) / 2
            mrc_payments[0] = payments[0] + delta
            mrc_payments[2] = payments[2] + delta
            if mrc_payments[0] > a:
                return (a, b, g - a - b, 0)
            if mrc_payments[2] > c:
                return (g - b - c, b, c, 0)
            return tuple(mrc_payments)
        if mrc_payments[2] > c:
            mrc_payments[2] = c
            delta = (g-c-payments[0]-payments[1])/2
            mrc_payments[0] = payments[0] + delta
            mrc_payments[1] = payments[1] + delta
            if mrc_payments[0] > a:
                return (a, g-a-c, c, 0)
            if mrc_payments[1] > b:
                return (g-b-c, b, c, 0)
            return tuple(mrc_payments)

        if mrc_payments[0] < 0:
            mrc_payments[0] = 0
            delta = (g-payments[1]-payments[2])/2
            mrc_payments[1] = payments[1] + delta
            mrc_payments[2] = payments[2] + delta
            if mrc_payments[1] < 0:
                return (0, 0, g, 0)
            if mrc_payments[2] < 0:
                return (0, g, 0, 0)
            return tuple(mrc_payments)
        if mrc_payments[1] < 0:
            mrc_payments[1] = 0
            delta = (g-payments[0]-payments[2])/2
            mrc_payments[0] = payments[0] + delta
            mrc_payments[2] = payments[2] + delta
            if mrc_payments[0] < 0:
                return (0, 0, g, 0)
            if mrc_payments[2] < 0:
                return (g, 0, 0, 0)
            return tuple(mrc_payments)
        if mrc_payments[2] < 0:
            mrc_payments[2] = 0
            delta = (g-payments[0]-payments[1])/2
            mrc_payments[0] = payments[0] + delta
            mrc_payments[1] = payments[1] + delta
            if mrc_payments[0] < 0:
                return (0, g, 0, 0)
            if mrc_payments[1] < 0:
                return (g, 0, 0, 0)
            return tuple(mrc_payments)




        return tuple(mrc_payments)

def payoff_shapley(bids):
    a,b,c,g= bids
    if g > a+b+c:
        return (0,0,0,g-(a+b+c)) # not actualy payoff of g
    area = get_area(bids)
    shapley_dict = {}
    shapley_dict["wxyz"] = lambda a, b, c, g:((3*a+b+c-g)/4, (a+3*b+c-g)/4, (a+b+3*c-g)/4, 0)
    shapley_dict["wxy"] = lambda a, b, c, g:(3*a/4, a/4+5*b/6+c/3-g/3, a/4+b/3+5*c/6-g/3, 0)
    shapley_dict["wxz"] = lambda a, b, c, g:(5*a/6+b/4+c/3-g/3, 3*b/4, a/3+b/4+5*c/6-g/3, 0)
    shapley_dict["wyz"] = lambda a, b, c, g:(5*a/6+b/3+c/4-g/3, a/3+5*b/6+c/4-g/3, 3*c/4, 0)
    shapley_dict["wx"] = lambda a, b, c, g:(5*a/6+c/12-g/12, 5*b/6+c/12-g/12, a/3+b/3+11*c/12-5*g/12, 0)
    shapley_dict["wy"] = lambda a, b, c, g:(5*a/6+b/12-g/12, a/3+11*b/12+c/3-5*g/12, 5*c/6+b/12-g/12, 0)
    shapley_dict["wz"] = lambda a, b, c, g:(11*a/12+b/3+c/3-5*g/12, 5*b/6+a/12-g/12, 5*c/6+a/12-g/12, 0)
    shapley_dict["w"] = lambda a, b, c, g:(11*a/12+b/12+c/12-g/6, a/12+11*b/12+c/12-g/6, a/12+b/12+11*c/12-g/6, 0)

    shapley_dict["sxyq"] = lambda a, b, c, g:(5*a/6, 5*b/6, a/3+b/3+c-g/2, 0)
    shapley_dict["sxy"] = lambda a, b, c, g:(11*a/12+b/12-g/12, 11*b/12+a/12-g/12, a/12+b/12+c-g/4, 0)
    shapley_dict["sxzq"] = lambda a, b, c, g:(5*a/6, a/3+b+c/3-g/2, 5*c/6, 0)
    shapley_dict["sxz"] = lambda a, b, c, g:(11*a/12+c/12-g/12, a/12+b+c/12-g/4, 11*c/12+a/12-g/12, 0)
    shapley_dict["syzq"] = lambda a, b, c, g:(a+b/3+c/3-g/2, 5*b/6, 5*c/6, 0)
    shapley_dict["syz"] = lambda a, b, c, g:(a+b/12+c/12-g/4, 11*b/12+c/12-g/12, 11*c/12+b/12-g/12, 0)
    shapley_dict["sx"] = lambda a, b, c, g:(11*a/12, a/12+b-g/6, a/12+c-g/6, 0)
    shapley_dict["sy"] = lambda a, b, c, g:(a+b/12-g/6, 11*b/12, b/12+c-g/6, 0)
    shapley_dict["sz"] = lambda a, b, c, g:(a+c/12-g/6, b+c/12-g/6, 11*c/12, 0)
    shapley_dict["s"] = lambda a, b, c, g:(a-g/12, b-g/12, c-g/12, 0)

    return shapley_dict[area](*bids)

def create_payoff_shapley():
    shapley_dict = {}
    shapley_dict["wxyz"] = lambda a, b, c, g:((3*a+b+c-g)/4, (a+3*b+c-g)/4, (a+b+3*c-g)/4, 0)
    shapley_dict["wxy"] = lambda a, b, c, g:(3*a/4, a/4+5*b/6+c/3-g/3, a/4+b/3+5*c/6-g/3, 0)
    shapley_dict["wxz"] = lambda a, b, c, g:(5*a/6+b/4+c/3-g/3, 3*b/4, a/3+b/4+5*c/6-g/3, 0)
    shapley_dict["wyz"] = lambda a, b, c, g:(5*a/6+b/3+c/4-g/3, a/3+5*b/6+c/4-g/3, 3*c/4, 0)
    shapley_dict["wx"] = lambda a, b, c, g:(5*a/6+c/12-g/12, 5*b/6+c/12-g/12, a/3+b/3+11*c/12-5*g/12, 0)
    shapley_dict["wy"] = lambda a, b, c, g:(5*a/6+b/12-g/12, a/3+11*b/12+c/3-5*g/12, 5*c/6+b/12-g/12, 0)
    shapley_dict["wz"] = lambda a, b, c, g:(11*a/12+b/3+c/3-5*g/12, 5*b/6+a/12-g/12, 5*c/6+a/12-g/12, 0)
    shapley_dict["w"] = lambda a, b, c, g:(11*a/12+b/12+c/12-g/6, a/12+11*b/12+c/12-g/6, a/12+b/12+11*c/12-g/6, 0)

    shapley_dict["sxyq"] = lambda a, b, c, g:(5*a/6, 5*b/6, a/3+b/3+c-g/2, 0)
    shapley_dict["sxy"] = lambda a, b, c, g:(11*a/12+b/12-g/12, 11*b/12+a/12-g/12, a/12+b/12+c-g/4, 0)
    shapley_dict["sxzq"] = lambda a, b, c, g:(5*a/6, a/3+b+c/3-g/2, 5*c/6, 0)
    shapley_dict["sxz"] = lambda a, b, c, g:(11*a/12+c/12-g/12, a/12+b+c/12-g/4, 11*c/12+a/12-g/12, 0)
    shapley_dict["syzq"] = lambda a, b, c, g:(a+b/3+c/3-g/2, 5*b/6, 5*c/6, 0)
    shapley_dict["syz"] = lambda a, b, c, g:(a+b/12+c/12-g/4, 11*b/12+c/12-g/12, 11*c/12+b/12-g/12, 0)
    shapley_dict["sx"] = lambda a, b, c, g:(11*a/12, a/12+b-g/6, a/12+c-g/6, 0)
    shapley_dict["sy"] = lambda a, b, c, g:(a+b/12-g/6, 11*b/12, b/12+c-g/6, 0)
    shapley_dict["sz"] = lambda a, b, c, g:(a+c/12-g/6, b+c/12-g/6, 11*c/12, 0)
    shapley_dict["s"] = lambda a, b, c, g:(a-g/12, b-g/12, c-g/12, 0)

    def payoff(bids):
        a,b,c,g= bids
        if g > a+b+c:
            return (0,0,0,g-(a+b+c)) # not actualy payoff of g
        area = get_area(bids)
        return shapley_dict[area](*bids)

    return payoff

def payment_vcg(bids):
    a, b, c, g = bids
    if g > a + b + c:
        return (0, 0,0, a+b+c)
    else:
        return (max(0, g-b-c), max(0, g-a-c), max(0, g-a-b), 0)

def payment_zero(bids):
    return (0,0,0,0)

def payment_bid(bids):
    return bids

def payment_shapley(bids):
    a, b,c, g = bids
    if a + b+c < g:
        return (a-a, b-b,c-c, a+b+c)
    ps = payoff_shapley(bids)
    return (a-ps[0], b-ps[1],c-ps[2], g-g)

def payment_shapvcg(bids):
    a,b,c,g= bids
    if g > a+b+c:
        return (0,0,0,(a+b+c)) # not actual payment of g
    area = get_area(bids)
    shapvcg_dict = {}
    shapvcg_dict["wxyz"] = lambda a, b, c, g:((g-b-c)/4, (g-a-c)/4, (g-a-b)/4, 0)
    shapvcg_dict["wxy"] = lambda a, b, c, g:(0, (g-c)/3-a/4, (g-b)/3-a/4, 0)
    shapvcg_dict["wxz"] = lambda a, b, c, g:((g-c)/3-b/4, 0, (g-a)/3-a/4, 0)
    shapvcg_dict["wyz"] = lambda a, b, c, g:((g-b)/3-c/4, (g-a)/3-c/4, 0, 0)
    shapvcg_dict["wx"] = lambda a, b, c, g:((g-c)/12, (g-c)/12, 5*g/12-(a+b/3), 0)
    shapvcg_dict["wy"] = lambda a, b, c, g:((g-b)/12, 5*g/12-(a+c)/3, (g-b)/12, 0)
    shapvcg_dict["wz"] = lambda a, b, c, g:(5*g/12-(b+c)/3, (g-a)/12, (g-a)/12, 0)
    shapvcg_dict["w"] = lambda a, b, c, g:(g/6-(b+c)/12, g/6-(a+c)/12, g/6-(a+b)/12, 0)

    shapvcg_dict["sxyq"] = lambda a, b, c, g:(0, 0, g/2-(a+b)/3, 0)
    shapvcg_dict["sxy"] = lambda a, b, c, g:((g-b)/12, (g-a)/12, g/4-(a+b)/12, 0)
    shapvcg_dict["sxzq"] = lambda a, b, c, g:(0, g/2-(a+c)/3, 0, 0)
    shapvcg_dict["sxz"] = lambda a, b, c, g:((g-c)/12, g/4-(a+c)/12,(g-a)/12, 0)
    shapvcg_dict["syzq"] = lambda a, b, c, g:(g/2-(b+c)/3, 0, 0, 0)
    shapvcg_dict["syz"] = lambda a, b, c, g:(g/4-(b+c)/12, (g-c)/12, (g-b)/12, 0)
    shapvcg_dict["sx"] = lambda a, b, c, g:(0, g/6-a/12, g/6-a/12, 0)
    shapvcg_dict["sy"] = lambda a, b, c, g:(g/6-b/12, 0, g/6-b/12, 0)
    shapvcg_dict["sz"] = lambda a, b, c, g:(g/6-c/12, g/6-c/12, 0, 0)
    shapvcg_dict["s"] = lambda a, b, c, g:(g/12, g/12, g/12, 0)
    return shapvcg_dict[area](*bids)

def payment_quadratic(bids):
    return payment_nearest(payment_vcg, bids)

def payment_proxy(bids):
    return payment_nearest(payment_zero, bids)

def payment_bid_nearest(bids):
    return payment_nearest(payment_bid, bids)

def payment_shapley_nearest(bids):
    return payment_nearest(payment_shapley, bids)

def create_payment_shapley_nearest():
    payoff = create_payoff_shapley()

    def reference_point(bids):
        a, b,c, g = bids
        if a + b+c < g:
            return (a-a, b-b,c-c, g-a-b-c)
        ps = payoff_shapley(bids)
        return (a-ps[0], b-ps[1],c-ps[2], g-g)

    def payment(bids):
        return payment_nearest(reference_point, bids)

    return payment

def avg_payment(bid_a, strategy, payment):
    Ns = (50, 50, 150)
    ranges = ((0,1), (0,1), (0,3))
    N = Ns[0]*Ns[1]*Ns[2]
    bids = get_perfectly_uniform_values(ranges, Ns)
    #bids = get_random_uniform_values_decimal(ranges, N)
    total_payment = 0
    for b,c,g in bids:
        bid_b = strategy(b)
        bid_c = strategy(c)
        if g < bid_a + bid_b + bid_c:
            ps = payment((bid_a,bid_b,bid_c,g))
            total_payment += ps[0]



    return total_payment/N

def payment_shapvcg_nearest(bids):
    return payment_nearest(payment_shapvcg, bids)




