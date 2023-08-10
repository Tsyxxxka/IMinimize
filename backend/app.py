import os
import subprocess

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
CORS(app)
api = Api(app)

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/upload/'
NODE_INFO_FILE_FOLDER = os.path.dirname(os.path.abspath(__file__))+'/upload-nodeinfo/'
ALLOWED_EXTENSIONS = {'txt'}

   
@app.route('/', methods=["GET"])
def index():
    return "Welcome to Influence Control System."

class Form(Resource):
    @staticmethod
    def post_data(hasEdgeAc: False, hasNodeInfo: False, node_info_file_name: None, source: None, fileName: None, AcModel: None, shownodeInfo: True, showedgeInfo: True):
        datafile = ''
        totalData = {"source": source}
        if hasEdgeAc:
            totalData["hasEdgeAc"] = 1
            datafile = UPLOAD_FOLDER + fileName
        else:
            totalData["hasEdgeAc"] = 0
            totalData['AcModel'] = AcModel
            if AcModel == 'WC':
                model = 1
            else:
                model = 0
            all_seeds = ''
            for i in source:
                all_seeds += str(i) + ' '
            _command = '{{\necho "{}"\necho "{}"\necho "{}"\necho "{}"\n}} | ./edge'.format(
                        'upload/'+fileName, model, len(source), all_seeds
            )
            subprocess.check_call(_command, shell=True)
            datafile = './edges-upload/'+fileName
                
        node_info = {}
        if hasNodeInfo:
            totalData["hasNodeInfo"] = 1
            with open(NODE_INFO_FILE_FOLDER + node_info_file_name) as f:
                lines = f.readlines()
                for line in lines:
                    node_id = int(line.split('\t')[0])
                    other_info = line.split('\t')[1]
                    node_info[node_id] = other_info

        data = {"nodes": [], "edges": []}
        # n = set()
        nodes = []
        edges = []
        num_of_nodes, num_of_edges = 0,0
        with open(datafile) as f:
            num_of_nodes, num_of_edges = [int(i) for i in f.readline().split()]
            for i in range(num_of_edges):
                line = f.readline()
                lst = line.split()
                start, end = [int(i) for i in lst[:2]]
                p = float(lst[2])
                
                # n.add(start)
                # n.add(end)

                if showedgeInfo:
                    edges.append({"source": str(start), "target": str(end), "prob": str(p), "label": str(p)})
                else:
                    edges.append({"source": str(start), "target": str(end), "prob": str(p)})

        for i in range(num_of_nodes):
            if shownodeInfo and hasNodeInfo: # has sup info
                # totalData["showNodeInfo"] = 1
                nodes.append({"id": str(i), "label": str(i), "nodeInfo": node_info[i]})
            elif shownodeInfo:
                # totalData["showNodeInfo"] = 1
                nodes.append({"id": str(i), "label": str(i)})
            else:
                # totalData["showNodeInfo"] = 0
                nodes.append({"id": str(i)})

        data["nodes"] = nodes
        data["edges"] = edges
        totalData["data"] = data
        fname = fileName.split('.')[0]

        with open(UPLOAD_FOLDER + fname + "-totaldata.txt", 'w+') as f:
            f.write(str(totalData))

        return

    @staticmethod
    def post():
        # upload the form 
        # 1. write the processed initial data for UI in a 'totaldata' file
        # 2. return success info to the frontend
        file = request.files.get("file")
        if file is None:
            return {
                'message': "upload file failed"
            }
        file_name = file.filename
        if file_name.split('.')[-1] not in ALLOWED_EXTENSIONS:
            raise Exception("Not Allowed Extension: .{}".format(file_name.split('.')[-1]))
        print("The name of the uploaded file is [%s]\n" % file_name)
        file.save(UPLOAD_FOLDER + file_name)

        hasEdgeAc = True if request.values.get("edgeActivation") == 'Yes' else False
        AcModel = request.values.get("edgeActivation")
        hasNodeInfo = True if request.values.get("nodeInfo") == 'Yes' else False
        node_info_file_name = None
        if hasNodeInfo:
            nodeInfoFile = request.files.get("nodeInfoFile")
            if file is None:
                return {
                    'message': "upload vertex info file failed"
                }
            node_info_file_name = nodeInfoFile.filename
            if node_info_file_name.split('.')[-1] not in ALLOWED_EXTENSIONS:
                raise Exception("Not Allowed Extension: .{}".format(node_info_file_name.split('.')[-1]))
            nodeInfoFile.save(NODE_INFO_FILE_FOLDER + node_info_file_name)

        source_nodes = request.values.get("source")
        source_nodes = [int(i) for i in source_nodes.split()]
        shownodeInfo = True if request.values.get("shownodeInfo") == 'Yes' else False
        showedgeInfo = True if request.values.get("showedgeInfo") == 'Yes' else False
        # preprocess raw data
        Form.post_data(hasEdgeAc, hasNodeInfo, node_info_file_name, source_nodes, file_name, AcModel, shownodeInfo, showedgeInfo)

        return {
            'code': 200,
            'messsge': "File upload successfully",
            'fileName': file_name,
        }


class Hello(Resource):
    @staticmethod
    def post():
        filename = request.values.get("filename")
        totaldata = ''
        fname = filename.split('.')[0]

        with open(UPLOAD_FOLDER + fname + "-totaldata.txt") as f:
            totaldata = f.read()
            totaldata = eval(totaldata)

        return totaldata

class Mute(Resource):
    @staticmethod
    def sum(ap):
        sum = 0.0
        for i in range(len(ap)):
            sum = sum+ap[i]
        return sum 


    @staticmethod
    def solve(ap, source, block, edge, n):
        ap_now = []
        for i in range(0,n):
            ap_now.append(0.0)
        for x in range(0,n):
            if x in source:
                ap_now[x] = 1.0
            elif x in block:
                ap_now[x] = 0.0
            else:
                p = 1.0
                for _,tmp in enumerate(edge[x]):
                    y,z = tmp
                    p = p * (1.0 - z * ap[y])
                ap_now[x] = 1.0 - p
        return ap_now


    @staticmethod
    def compute(source, block, n, edge):
        preap = []
        ap = []
        for i in range(0,n):
            ap.append(0.0)
            preap.append(0.0)
        for _, x in enumerate(source):
            ap[x]=1.0
        while abs(Mute.sum(ap) - Mute.sum(preap)) > 1e-9:
            preap = ap
            ap = Mute.solve(ap,source,block,edge,n)
        return ap


    @staticmethod
    def gener_hex_str(fnum):
        # float to color_hex
        int_color = int(255 - fnum * 255)
        if int_color//16 < 10:
            first = str(int_color//16)  
        else:
            first = chr(int_color//16 + 55) 
        if int_color % 16 < 10:
            second = str(int_color%16) 
        else:
            second = chr(int_color%16 + 55) 
        return first + second


    @staticmethod
    def post():# 返回和Run.post()格式相同的数据更新前端颜色，以及返回具体的点的编号
        # {
        # echo "sample_graph.txt"
        # echo "2"
        # echo "1"
        # echo "1"
        # echo "2"
        # } | ./main
        _command = '{{\necho "{}"\necho "{}"\necho "{}"\necho "{}"\necho "{}"\n}} | ./main'
        mute_num = int(request.values.get("mute"))
        filename = request.values.get("filename")
        fname = filename.split('.')[0]

        source = []
        with open(UPLOAD_FOLDER + fname + "-totaldata.txt") as file:
            totaldata = file.read()
            totaldata = eval(totaldata)
            source = totaldata["source"]
            source_str = ''
            for i in source:
                source_str += str(i)+' '
            if totaldata["hasEdgeAc"] == 1:
                model = 2
            else:
                if totaldata["AcModel"] == 'WC':
                    model = 1
                else:
                    model = 0
            _command=_command.format('upload/'+filename, model, len(source),
                                     source_str, mute_num)

        subprocess.check_call(_command, shell=True)
        with open('./results-upload/'+filename) as f:
            line = f.readline()
            node_num, initial_exp, after_exp = [float(i) for i in line.split()]
            node_num = int(node_num)

            line = f.readline()
            block_nodes = [int(i) for i in line.split()]

            nodes_color = []
            for i in range(node_num):
                line = f.readline()
                node_id = int(line.split()[0])
                node_prob = float(line.split()[1])
                if i in source:
                    color_str = 'blue'
                else:
                    color_str = Mute.gener_hex_str(node_prob)
                nodes_color.append({"id": node_id, "color": color_str, "prob": node_prob})

            returnData = {}
            returnData['nodesColor'] = nodes_color
            returnData['muteNodes'] = block_nodes
            returnData['afterexp'] = after_exp
            returnData['initialexp'] = initial_exp
            return returnData
            

        # with open(UPLOAD_FOLDER + filename) as file:
        #     line = file.readline()
        #     n,m = [int(i) for i in line.split()]
        #     source.append(0)
        #     budget = mute_num
        #     # TODO exception
        #     edge = []
        #     exist = []
        #     ap = []
        #     for i in range(0,n):
        #         edge.append([])
        #         exist.append(0)
        #     for i in range(0,m):
        #         line = file.readline()
        #         x,y,z = [float(i) for i in line.split()]
        #         x = int(x)
        #         y = int(y)
        #         exist[x] = 1
        #         exist[y] = 1
        #         edge[y].append((x,z))

        #     block = []
        #     ap = Mute.compute(source, block, n, edge)

        #     print("original: {}".format(Mute.sum(ap)))

        #     for i in range(0,budget):
        #         Min = Mute.sum(ap)
        #         block_node = 0
        #         for x in range(0,n):
        #             if x in block and x not in source:
        #                 continue
        #             elif exist[x] > 0 :
        #                 block.append(x)
        #                 ap = Mute.compute(source, block, n, edge)
        #                 tmp = Mute.sum(ap)
        #                 if tmp < Min:
        #                     Min = tmp
        #                     block_node = x
        #                 del block[i]
        #         block.append(block_node)
        #     ap = Mute.compute(source, block, n, edge)
        #     print("now: {}".format(Mute.sum(ap)))

        #     returnData = {}
        #     nodes = []
        #     l = len(ap)
        #     for i in range(l):
        #         if exist[i] > 0:
        #             color_str = Mute.gener_hex_str(ap[i])
        #             nodes.append({"id": i, "color": color_str})

        #     returnData['nodesColor'] = nodes
        #     returnData['muteNodes'] = block
        #     returnData['afterexp'] = Mute.sum(ap)
        #     return returnData


class Activate(Resource):
    @staticmethod
    def sum(ap):
        sum = 0.0
        for i in range(len(ap)):
            sum = sum+ap[i]
        return sum 

    @staticmethod
    def solve(ap, source, block, edge, n):
        ap_now = []
        for i in range(0,n):
            ap_now.append(0.0)
        for x in range(0,n):
            if x in source:
                ap_now[x] = 1.0
            elif x in block:
                ap_now[x] = 0.0
            else:
                p = 1.0
                for _,tmp in enumerate(edge[x]):
                    y,z = tmp
                    p = p * (1.0 - z * ap[y])
                ap_now[x] = 1.0 - p
        return ap_now

    @staticmethod
    def compute(source, block, n, edge):
        preap = []
        ap = []
        for i in range(n):
            ap.append(0.0)
            preap.append(0.0)
        for _, x in enumerate(source):
            ap[x]=1.0
        while abs(Activate.sum(ap) - Activate.sum(preap)) > 1e-9:
            preap = ap
            ap = Activate.solve(ap,source,block,edge,n)
        return ap

    @staticmethod
    def gener_hex_str(fnum):
        # float to color_hex
        int_color = int(255 - fnum * 255)
        if int_color//16 < 10:
            first = str(int_color//16)  
        else:
            first = chr(int_color//16 + 55) 
        if int_color % 16 < 10:
            second = str(int_color%16) 
        else:
            second = chr(int_color%16 + 55) 
        return first + second

    @staticmethod
    def post():# 返回和Run.post()格式相同的数据更新前端颜色，以及返回具体的点的编号
        activate_num = int(request.values.get("activate"))
        filename = request.values.get("filename")

        with open(UPLOAD_FOLDER + filename) as file:
            line = file.readline()
            n,m = [int(i) for i in line.split()]
            budget = activate_num
            edge = []
            ap = []
            exist = []
            for i in range(n):
                edge.append([])
                exist.append(0)
            for i in range(0,m):
                line = file.readline()
                x,y,z = [float(i) for i in line.split()]
                x = int(x)
                y = int(y)
                exist[x] = 1
                exist[y] = 1
                edge[y].append((x,z))
            source = []
            block = []
            ap = Activate.compute(source, block, n, edge)

            for i in range(budget):
                Max = Activate.sum(ap)
                seed_node = 0
                for x in range(0,n):
                    if x in source:
                        continue
                    elif exist[x] == 1 :
                        source.append(x)
                        ap = Activate.compute(source, block, n, edge)
                        tmp = sum(ap)
                        if tmp > Max:
                            Max = tmp
                            seed_node = x
                        del source[i]
                source.append(seed_node)
            
            ap = Activate.compute(source, block, n, edge)

            returnData = {}
            nodes = []
            l = len(ap)
            for i in range(l):
                if exist[i] > 0:
                    color_str = Activate.gener_hex_str(ap[i])
                    nodes.append({"id": i, "color": color_str})

            returnData['nodesColor'] = nodes
            returnData['seedNodes'] = source
            returnData['afterexp'] = Activate.sum(ap)
            return returnData



api.add_resource(Hello, '/hello') # get base image
api.add_resource(Form, '/form_rec') # upload and save settings
# api.add_resource(Run, '/run') # get color for original source (only for min)
api.add_resource(Mute, '/mute')  # mute nodes (only for min)
api.add_resource(Activate, '/activate')  # mute nodes (only for min)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8010)
