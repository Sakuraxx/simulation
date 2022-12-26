dn = [0 for i in range(100)]

filename = './data/dn_10_0.txt'
with open(filename) as f:
    for line in f.readlines():
        print(line)
        x = line.split(' ')
        dn[int(x[1])] += int(x[2]) + int(x[3])

dn.sort()
print(dn, sum(dn))
