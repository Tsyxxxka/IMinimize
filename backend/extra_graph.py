file = open("facebook_in.txt", "r")
line = file.readline()
# TODO[source]
n,m,source = [int(i) for i in line.split()]
edge = []
edge_to = []
preap = []
output_edge = []
for i in range(0,n):
    edge.append([])
    edge_to.append([])
    output_edge.append([])
for i in range(0,m):
    line = file.readline()
    x,y,z = [float(i) for i in line.split()]
    x = int(x)
    y = int(y)
    edge[y].append((x,z))
    edge_to[x].append((y,z))

vector_list = []
vector_list.append(source)
number_nodes = 40 #number of nodes to show in the frontend
for idx,tmp in enumerate(edge_to[source]):
    x,_ = tmp
    if x in vector_list:
        continue
    else:
        vector_list.append(x)
        for idy,tmp2 in enumerate(edge_to[x]):
            y,__ = tmp2
            if y in vector_list:
                continue
            else:
                vector_list.append(y)
                if len(vector_list) > number_nodes:
                    break
        if len(vector_list) > number_nodes:
            break

lenm = 0
for idx,x in enumerate(vector_list):
    for idy,tmp2 in enumerate(edge_to[x]):
        y,z = tmp2
        if y in vector_list:
            output_edge[x].append((y,z))
            lenm = lenm + 1
output_file = open('output_data.txt','w')
output_file.write(str(len(vector_list))+' '+str(lenm)+'\n')
for idx,x in enumerate(vector_list):
    for idy,tmp2 in enumerate(edge_to[x]):
        y = tmp2[0]
        z = tmp2[1]
        if y in vector_list:
            output_file.write(str(x)+' '+str(y)+' '+str(z)+'\n')