from LLG.payments import *
from strategies import *
from collections import defaultdict


def sensitivity_shapley_without_seller_of_a(bids):
    a, b, g = bids
    if a + b < g:
        return 0
    if a < g:       # wl, sl2
        return 0.5
    else:
        return 0

def sensitivity_shapley_with_seller_of_a(bids):
    a, b, g = bids
    if a + b < g:
        return 0
    if a < g:       # wl, sl2
        return 5/6
    else:
        return 1/2

def sensitivity_shapley_payoff_with_seller_of_a(bids):
    a, b, g = bids
    if a + b < g:
        return 0
    if a < g:       # wl, sl2
        return 1/6
    else:
        return 1/2

def sensitivity_shapvcg_of_a(bids):
    a, b, g = bids
    if a + b < g:
        return 0
    if a < g:
        return 1/3
    else:
        return 0

def sensitivity_bid_of_a(bids):
    a, b, g = bids
    if  g >= a + b:
        return 0
    elif b > g + a or b < a - g:
        return 0
    else:
        return 1

def sensitivity_vcg_zero_middle_of_a(bids):
    a, b, g = bids
    if a < g:
        return 0.5
    else:
        return 0

def sensitivity_vcg_of_a(bids):
    a, b, g = bids
    if a < g:
        return 1
    else:
        return 0

def sensitivity_zero_of_a(bids):
    a, b, g = bids
    return 0

def derivative_of_payment_of_a(bids, payment_reference_point, sensitivity_of_a):
    a, b, g = bids
    if a + b < g:
        return 0
    pa, pb, pg = payment_reference_point(bids)
    if pa > pb + 2*a - g:       # IR constraint of a binding
        return 1 # (1, 0, 0)
    elif pa < pb + g - 2*b:     # IR constraint of b binding
        return 0 # (0, 1, 0)
    else:
        return sensitivity_of_a(bids)/2

def derivative_slice_zero(b, g):
    if b > g:
        return (((0, g/2), 1), ((g/2, 1), 0))
    elif b > g/2:
        return (((0, g-b), 0),((g-b, g/2), 1), ((g/2, 1), 0))
    else:
        return (((0, 1), 0),)

def derivative_slice_vcg(b, g):
    if b > g:
        return (((0, g), 1/2), ((g, 1), 0))
    else:
        return (((0, g-b), 0),((g-b, g), 1/2), ((g, 1), 0))

def derivative_slice_shapley_wo(b, g):
    if b > g:
        return (((0, g/3), 1), ((g/3, g), 1/4), ((g, 1), 0))
    elif b > g/2:
        x = 2*g/3-b/3
        return (((0, g-b), 0),((g-b, x), 1), ((x, g), 1/4), ((g, 1), 0))
    elif b > g/3:
        x = 2*g - 3*b
        return (((0, x), 0), ((x, g), 1/4), ((g, 1), 0))
    else:
        return (((0, 1), 0),)

# assumed start_a >= end_a and both in [0, 1]
def slice_to_derivative_decomposition(start_a, end_a, slice):
    if start_a < end_a or start_a < 0 or end_a > 1:
        print("Wrong input for slice utility decomposition!")
    utility_composition = defaultdict(int)
    left_i = 0
    while end_a > slice[left_i][0][1]:
        left_i += 1
    right_i = len(slice)-1
    while start_a < slice[right_i][0][0]:
        right_i -= 1
    if left_i == right_i:
        utility_composition[slice[left_i][1]] += start_a - end_a
    else:
        utility_composition[slice[left_i][1]] += slice[left_i][0][1] - end_a
        utility_composition[slice[right_i][1]] += start_a - slice[right_i][0][0]
        for i in range(left_i+1, right_i):
            utility_composition[slice[i][1]] += slice[i][0][1] - slice[i][0][0]
    return utility_composition

def sensitivity_shapley_without_seller(bids):
    a, b, g = bids
    if a + b < g:
        return (0, 0, 0)
    elif a < g and b < g:       # wl,
        return (0.5, 0.5, 0)
    elif b < g:                 # sl1
        return (0, 0.5, 0)
    elif a < g:                 # sl2
        return (0.5, 0, 0)
    else:                       # sl
        return (0, 0, 0)

def sensitivity_vcg(bids):
    a, b, g = bids
    if a + b < g:
        return (0, 0, 0)
    elif a < g and b < g:       # wl
        return (1, -1, 0)
    elif b < g:                 # sl1
        return (0, -1, 0)
    elif a < g:                 # sl2
        return (1, 0, 0)
    else:                       # sl
        return (0, 0, 0)

def plot_derivatives(payment_reference_point, sens_of_a, name):
    aas = [i for i in np.arange(0, 1, 0.01) for j in range(1000)]
    bbs = list(np.arange(0, 1, 0.01))*1000
    colors = []
    for a, b in zip(aas, bbs):
        bids = (a, b, 0.5)
        colors.append(derivative_of_payment_of_a(bids, payment_reference_point, sens_of_a))
    fig, ax = plt.subplots()
    scatter = ax.scatter(aas, bbs, c=colors, alpha=0.5)
    legend1 = ax.legend(*scatter.legend_elements(),
                        loc="upper right", title="Derivatives")
    ax.add_artist(legend1)
    ax.set_aspect('equal', 'box')
    plt.xlabel("A")
    plt.ylabel("B")
    plt.title("Different derivatives for "+name+" (g = 0.5)")
    # plt.savefig("./plots1/Different derivatives for shapley payment with seller (g = 0.5)")
    plt.show()


def plot_derivatives_fix_v(payment_reference_point, sens_of_a, name):
    ggs = list(np.arange(0, 2, 0.01))*1000
    bbs = [i for i in np.arange(0, 2, 0.01) for j in range(1000)]
    colors = []
    for b, g in zip(bbs, ggs):
        bids = (0.5, b, g)
        colors.append(derivative_of_payment_of_a(bids, payment_reference_point, sens_of_a))
    fig, ax = plt.subplots()
    scatter = ax.scatter(bbs, ggs, c=colors, alpha=0.5)
    legend1 = ax.legend(*scatter.legend_elements(), loc="upper right", title="Derivatives")
    #ax.add_artist(legend1)
    ax.set_aspect('equal', 'box')
    plt.xlabel("A")
    plt.ylabel("B")
    plt.title("Different derivatives for "+name+" (g = 0.5)")
    # plt.savefig("./plots1/Different derivatives for shapley payment with seller (g = 0.5)")
    plt.show()

# plot_derivatives(payment_shapley_with_seller, sensitivity_shapley_with_seller_of_a, "Shapley w/-nearest payments")
# plot_derivatives(payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, "Shapley w/o-nearest payments")
# plot_derivatives(payment_shapley_vcg, sensitivity_shapvcg_of_a, "Shapvcg nearest payments")

# plot_derivatives(payment_vcg, sensitivity_vcg_of_a, "vcg-nearest payments")
# plot_derivatives(payment_zero, sensitivity_zero_of_a, "Zero-nearest payments")
# plot_derivatives(payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, "Shapleynearest")
# plot_derivatives(payment_bid, sensitivity_bid_of_a, "bid nearest")
# plot_derivatives(payment_shapley_vcg, sensitivity_shapvcg_of_a, "Svcg-nearest")


# plot_derivatives_fix_v(payment_bid, sensitivity_bid_of_a, "bid nearest")
# plot_derivatives_fix_v(payment_vcg, sensitivity_vcg_of_a, "vcg-nearest payments")
# plot_derivatives_fix_v(payment_zero, sensitivity_zero_of_a, "Zero-nearest payments")
#plot_derivatives_fix_v(payment_shapley_without_seller, sensitivity_shapley_without_seller_of_a, "Shaple-nearest")
#plot_derivatives_fix_v(payment_shapley_vcg, sensitivity_shapvcg_of_a, "Svcg-nearest")
