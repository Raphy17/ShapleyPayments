import matplotlib.pyplot as plt
from definitions import ROOT_DIR



def plot_strategy(file, style="-", color=None):
    with open(file) as fd:
        lines = fd.readlines()
        strategy = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy)):
            if i % 2 == 0:
                a_values.append(float(strategy[i]))
            else:
                bid_values.append(float(strategy[i]))
        if color != None:
            plt.plot(a_values, bid_values,style, color=color)
        else:
            plt.plot(a_values, bid_values)

def plot_strategy_change(files,payment_rule,legend, title):
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color'][1:]

    for i in range(len(files)):
        file = files[i]
        color = colors[i % 5]
        plot_strategy(file+payment_rule+".txt", color=color)
    # for i in range(len(files)-1, 5, -1):
    #     file = files[i]
    #     color = colors[i % 6]
    #     plot_strategy(file+payment_rule+".txt",style="--", color=color)
    # plt.legend(["truthful"]+strats)
    plt.legend(legend)
    plt.title(title)
    #plt.savefig("../figures/" + title)
    plt.xlabel("Value")
    plt.ylabel("Bid")
    plt.show()

def strategy_change_assymetry(payment_rule):
    plt.figure(figsize=(7,7))
    plt.plot([0, 1],[0, 1])
    correlation_files = []
    legend = ["truthful"]
    bounds = [1, 3, 5,7, 9, 10]

    for i in bounds:
        correlation_files.append(llg+varying_assymetry+str(i)+"/")
        #legend.append("[0,1], [0, "+str(round(i*0.1,1))+ "]")

    for i in bounds:
        correlation_files.append(llg+varying_assymetry+str(i)+"o/")
        legend.append("[0, "+str(round(i*0.1,1))+ "], [0, 1]")

    plot_strategy_change(correlation_files, payment_rule,legend, "BNE strategy depending on assymetry for "+payment_rule)


def strategy_change_correlation(payment_rule):
    plt.figure(figsize=(7,7))
    plt.plot([0, 1],[0, 1])
    correlation_files = []
    legend = ["truthful", "0 correlation", "0.25 correlation", "0.5 correlation", "0.75 correlation", "1 correlation"]
    for i in range(0, 101, 25):
        correlation_files.append(llg+correlation+str(i)+"/")
        # legend.append("0."+str(i)+ " correlation")
    plot_strategy_change(correlation_files, payment_rule,legend, "BNE strategy depending on correlation for "+payment_rule)



def strategy_change_varying_locals(payment_rule):
    plt.figure(figsize=(7,7))
    plt.plot([0, 1],[0, 1])
    files = []
    legend = ["truthful"]
    for i in range(0, 10):
        files.append(llg+varying_locals+str(i)+"/")
        legend.append("["+str(round(i*0.1,1))+ ", 1], ["+str(round(i*0.2,1))+ ", 2]")
    plot_strategy_change(files, payment_rule,legend, "BNE strategy depending value range "+payment_rule)

def strategy_change_varying_global(payment_rule):
    plt.figure(figsize=(7,7))
    plt.plot([0.5, 1],[0.5, 1])
    correlation_files = []
    legend = ["truthful"]
    for i in range(0, 15):
        correlation_files.append(llg+varying_global+str(i)+"/")
        legend.append("[0.5,1.0], ["+str(round(i*0.1,1))+ ", " + str(round(3-i*0.1,1))+"]")
    plot_strategy_change(correlation_files, payment_rule,legend, "BNE strategy depending on globals value range "+payment_rule)

def strategy_change_varying_global2(payment_rule):
    plt.figure(figsize=(7,7))
    plt.plot([0, 1],[0, 1])
    correlation_files = []
    legend = ["truthful"]
    for i in range(0, 10):
        correlation_files.append(llg+varying_global2+str(i)+"/")
        legend.append("[0.0,1.0], ["+str(round(i*0.1,1))+ ", " + str(round(2-i*0.1,1))+"]")
    plot_strategy_change(correlation_files, payment_rule,legend, "BNE strategy depending on globals value range "+payment_rule)




def get_strategy_as_lists(file):
    with open(file) as fd:
        lines = fd.readlines()
        strategy = lines[0].split()
        a_values = []
        bid_values = []
        for i in range(len(strategy)):
            if i % 2 == 0:
                a_values.append(float(strategy[i]))
            else:
                bid_values.append(float(strategy[i]))
        return a_values, bid_values


def plot_strategies(path, strats, title):
    plt.figure(figsize=(7,7))
    a_values, bid_values = get_strategy_as_lists(path+strats[0]+".txt")
    print(a_values)
    value_range = a_values[0], a_values[-1]
    plt.plot(value_range,value_range)
    for strat in strats:
        a_values, bid_values = get_strategy_as_lists(path+strat+".txt")
        plt.plot(a_values, bid_values)
    plt.legend(["truthful"]+strats, prop={'size': 15})
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Bid")
    #plt.savefig("../figures/" + title)
    plt.show()

l3g = ROOT_DIR + "/strategyText/L3G/"
llg = ROOT_DIR + "/strategyText/LLG/"
strategies = ["quadratic", "proxy", "shapley", "svcg", "shapley_ratio"]
strategies = ["quadratic", "proxy", "shapley", "svcg", "bid"]
# strategies = ["quadratic", "proxy", "shapley", "bid"]
#strategies = ["quadratic", "proxy", "shapley", "svcg"]
# strategies = ["bid"]
standard = "standard/"
correlation = "correlation/"
varying_locals = "varying_locals/"
varying_assymetry = "varying_assymetry/"
varying_global = "varying_global/"
varying_global2 = "varying_global2/"




plot_strategies(llg+standard, strategies, "BNE strategies standard LLG")
plot_strategies(l3g+standard, strategies, "BNE strategies standard L3G")
plot_strategies(llg+correlation+"50/", strategies, "BNE strategies LLG with 0.5 correlation")

# for some of these plots to look good the plot strategy function needs to be altered (especiialy in the case of asymmetry)
for payment_rule in strategies:
    strategy_change_correlation(payment_rule)
    strategy_change_varying_locals(payment_rule)
    strategy_change_varying_global(payment_rule)
    strategy_change_varying_global2(payment_rule)
    strategy_change_assymetry(payment_rule)

