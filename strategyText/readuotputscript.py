from definitions import ROOT_DIR

llg = ROOT_DIR + "/strategyText/LLG/"
varying_global = "varying_global2/"

def main_loop(file):
    with open(file) as fd:
        nr = 1
        cnt = 0
        for line in fd:
            if line[0] =='-' or len(line) < 18000:
                continue
            start = 0
            print(line)
            while line[start] != '|':
                start += 1
            strategy = line[start+1:]
            end = 0
            while line[end] != ' ':
                end += 1
            name = line[0:end]
            path = llg+varying_global+str(nr)+"/"+name+".txt"
            f = open(path, "w")
            f.write(strategy)
            f.close()
            cnt += 1
            if cnt == 5:
                cnt = 0
                nr += 1
        print(nr)



#main_loop("out.txt")



