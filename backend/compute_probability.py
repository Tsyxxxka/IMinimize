def sum(ap):
    sum = 0.0
    for i in range(len(ap)):
        sum = sum+ap[i]
    return sum 

def solve(ap,source):
    ap_now = []
    for i in range(0,n):
        ap_now.append(0.0)
    for x in range(0,n):
        if x != source:
            p = 1.0
            for _,tmp in enumerate(edge[x]):
                y,z = tmp
                p = p * (1.0 - z * ap[y])
            ap_now[x] = 1.0 - p
        else:
            ap_now[x] = 1.0
    return ap_now


file = open("output_data.txt", "r")
line = file.readline()
# TODO[source]
n,m,source = [int(i) for i in line.split()]
# source (from filename-totaldata.txt)
edge = []
ap = []
preap = []
for i in range(0,n):
    edge.append([])
    ap.append(0.0)
for i in range(0,m):
    line = file.readline()
    x,y,z = [float(i) for i in line.split()]
    x = int(x)
    y = int(y)
    edge[y].append((x,z))
ap[source]=1.0

# for i in range(0,100):
#     ap = solve(ap,source)
#     print(sum(ap)) 

while abs(sum(ap) - sum(preap)) > 1e-9:
    preap = ap
    ap = solve(ap,source)
    # print(sum(ap))
    # TODO print ap to frontend
# for i in range(0,n):
#     print(i,ap[i])

l = len(ap)
for i in range(l):
    if ap[i] > 0:
        print("{} {}".format(i,ap[i]))

print(sum(ap))