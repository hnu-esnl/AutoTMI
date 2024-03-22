from GraphMatrix import GraphMatrix
class Graph:
    # Get vertex information, pkg names are arranged in order
    def VertexLengh(self, Vertex, arr):
        j = 0
        Vertex.clear()
        #Vertex[0] = arr[0][0]
        Vertex.append(arr[0][0])
        for i in range(1,len(arr)):
            tmp = arr[i][0]
            if not tmp == Vertex[j]:
                j = j + 1
                Vertex.append(tmp)
        return j + 1

    # Get the index of the vertex
    def vertexIndex(self, vertex, name, len):
        index = -1
        for i in range(0, len):
            if vertex[i] == name:
                index = i
        return index

    # To create a relationship matrix, first get the vertex set, and then build the relationship matrix
    def CreatG(self, arr, length, GM):
        #print(length)

        for i in range(0, length):
            k = 1
            count = 0
            shortname = arr[i][1]
            PPortName = ""
            PPortName1 = ""
            index1 = index2 = pIndex = 0
            index = -1
            pkg = []
            for j in range(i + 1, length):
                if arr[j][1] == shortname:
                    if arr[j][2] == "P-PORT-PROTOTYPE" and arr[i][2] =="R-PORT-PROTOTYPE":
                        PPortName  = arr[j][0]
                        PPortName1 = arr[i][0]
                        pkg.append(arr[i][0])
                    if arr[i][2] == "P-PORT-PROTOTYPE" and arr[j][2] =="R-PORT-PROTOTYPE":
                        PPortName = arr[i][0]
                        PPortName1 = arr[j][0]
                        pkg.append(arr[j][0])
            pIndex = self.vertexIndex(GM.getVertex(), PPortName, GM.getVertexNum())
            #GM.EdgeWeight.clear()

            for k in range(len(pkg)):
                rIndex = self.vertexIndex(GM.Vertex, pkg[k], GM.VertexNum)
                GM.EdgeWeight[pIndex][rIndex] = GM.EdgeWeight[pIndex][rIndex] + 1

            '''if arr[i][2] == "P-PORT-PROTOTYPE":
                index1 = i
                PPortName = arr[i][0]
                index += 1
            for j in range(i+1, length):
                if arr[j][1] == shortname:
                    count = count + 1
                    if len(pkg) == 0:
                        pkg.append(arr[i][0])
                    else:
                        pkg[0] = arr[i][0]
                    #pkg.append(arr[i][0])
                    pkg.append(arr[j][0])
                    k = k + 1
                    if arr[j][2] == "P-PORT-PROTOTYPE":
                        PPortName = arr[j][0]
                        index += 1
                        break
                else:
                    continue

            pIndex = self.vertexIndex(GM.getVertex(), PPortName, GM.getVertexNum())
            if pIndex >= 0 and count > 0:
                for p in range(0, k):
                    if pkg[p] != PPortName and len(PPortName) != 0:
                        rIndex = self.vertexIndex(GM.Vertex, pkg[p], GM.VertexNum)
                        GM.EdgeWeight[pIndex][rIndex] = GM.EdgeWeight[pIndex][rIndex] + 1'''
            i = i + count
        return GM.getEdgeWeight()

    #  send receive port
    def getPortGraph(self, arr, length):
        portList = []
        for i in range(0, length):
            k = 1
            count = 0
            shortname = arr[i][1]
            PPortSWCName = ""
            PPortName = ""
            PPortName1 = ""
            pkg = []
            for j in range(i + 1, length):
                if arr[j][1] == shortname:
                    if arr[j][2] == "P-PORT-PROTOTYPE" and arr[i][2] =="R-PORT-PROTOTYPE":
                        PPortName  = arr[j][0]
                        PPortName1 = arr[i][0]
                        PPortSWCName = shortname
                        portarr = [PPortName, PPortName1, PPortSWCName]
                        portList.append(portarr)
                    if arr[i][2] == "P-PORT-PROTOTYPE" and arr[j][2] =="R-PORT-PROTOTYPE":
                        PPortName = arr[i][0]
                        PPortName1 = arr[j][0]
                        PPortSWCName = shortname
                        portarr = [PPortName, PPortName1, PPortSWCName]
                        portList.append(portarr)
        #print(portList)
        return portList
