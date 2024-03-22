class BCInfo:
    bcName = ''
    fcNum = 0
    portNum = 0
    pportNum = 0
    rportNum = 0
    runnableNum = 0
    interfaceNum = 0
    SRNum = 0
    CSNum = 0
    nouseInterfaceNum = 0
    intralInNum = 0
    intralOutNum = 0
    extralInNum = 0
    extralOutNum = 0
    extralDependNum = 0
    intralDependNum = 0
    loc = 0  # FC Effective lines of code
    aveFuncLoc = 0  # Average number of function lines of code
    aveFuncCC = 0  # Average function cyclomatic complexity
    maxFuncND = 0  # Maximum function nesting depth
    bcScore = 0
    bcScore1 = 0

    FC = []
    FCList = []
    dependInterBCMap = []  # Interdependence BC, intersection of in- and out-degree sets
    dependUnionBCMap = []   # Depends on the union of in- and out-degrees
    dependInterBCNum = 0    # The number of intersection elements
    dependUnionBCNum = 0    # The number of elements in the union of in- and out-degrees
    inMap = []      # Indegree set
    outMap = []     # Out-degree set
    indegree = 0    # Indegree
    outdegree = 0   # Out-degree
    inWeight = 0    # In-degree weight
    outWeight = 0   # Out-degree weight
    totalIntraNum = 0   # Internal coupling, same as BC
    totalExtraNum = 0   # External coupling, across BC
    totalIndirectExtraNum = 0   # External afferent coupling, indirectBC-FC,，indirectExtra


    norBCIntraCoupling = 0.0    # internal coupling
    norBCExtraCoupling = 0.0    # external coupling
    norBCExtraDependCoupling = 0.0  # interdependent coupling
    norBCPortNum = 0.0
    norBCRunnableNum = 0.0
    norBCInterfaceNum = 0.0
    norBCNoUseInterface = 0.0
    norBCCC = 0.0  # FC Cyclomatic Complexity
    norBCMaxND = 0.0
    norBCLoc = 0.0
    norBCAvgFuncLoc = 0.0  # Average number of function lines of code



    def setbcName(self,bcName):
        self.bcName = bcName

    def getbcName(self):
        return self.bcName

    def setfcNum(self,fcNum):
        self.fcNum = fcNum

    def getfcNum(self):
        return self.fcNum

    def setSRNum(self,SRNum):
        self.SRNum = SRNum

    def getSRNum(self):
        return self.SRNum

    def setCSNum(self,CSNum):
        self.CSNum = CSNum

    def getCSNum(self):
        return self.CSNum

    def setportNum(self,portNum):
        self.portNum = portNum

    def getportNum(self):
        return self.portNum

    def setpportNum(self,pportNum):
        self.pportNum = pportNum

    def getpportNum(self):
        return self.pportNum

    def setrportNum(self,rportNum):
        self.rportNum = rportNum

    def getrportNum(self):
        return self.rportNum

    def setinterfaceNum(self,interfaceNum):
        self.interfaceNum = interfaceNum

    def getinterfaceNum(self):
        return self.interfaceNum

    def setnouseInterfaceNum(self,nouseInterfaceNum):
        self.nouseInterfaceNum = nouseInterfaceNum

    def getnouseInterfaceNum(self):
        return self.nouseInterfaceNum

    def addFC(self,fcname):
        self.FC.append(fcname)

    def getFC(self):
        return self.FC

    def addFCList(self, fc):
        self.FCList.append(fc)

    def getFCList(self):
        return self.FCList

    def setrunnableNum(self,runnableNum):
        self.runnableNum = runnableNum

    def getrunnableNum(self):
        return self.runnableNum

    def setintralInNum(self, intralInNum):
        self.intralInNum = intralInNum

    def getintralInNum(self):
        return self.intralInNum

    def setintralOutNum(self, intralOutNum):
        self.intralOutNum = intralOutNum

    def getintralOutNum(self):
        return self.intralOutNum

    def setextralInNum(self, extralInNum):
        self.extralInNum = extralInNum

    def getextralInNum(self):
        return self.extralInNum

    def setextralOutNum(self, extralOutNum):
        self.extralOutNum = extralOutNum

    def getextralOutNum(self):
        return self.extralOutNum

    def settotalIntraNum(self,totalIntraNum):
        self.totalIntraNum = totalIntraNum

    def gettotalIntraNum(self):
        return self.totalIntraNum

    def settotalExtraNum(self,totalExtraNum):
        self.totalExtraNum = totalExtraNum

    def gettotalExtraNum(self):
        return self.totalExtraNum

    def setintralDependNum(self,intralDependNum):
        self.intralDependNum = intralDependNum

    def getintralDependNum(self):
        return self.intralDependNum

    def setextralDependNum(self,extralDependNum):
        self.extralDependNum = extralDependNum

    def getextralDependNum(self):
        return self.extralDependNum

    def setindegree(self,indegree):
        self.indegree = indegree

    def getindegree(self):
        return self.indegree

    def setoutdegree(self,outdegree):
        self.outdegree = outdegree

    def getoutdegree(self):
        return self.outdegree

    def setloc(self,loc):
        self.loc = loc

    def getloc(self):
        return self.loc

    def setaveFuncLoc(self,aveFuncLoc):
        self.aveFuncLoc = aveFuncLoc

    def getaveFuncLoc(self):
        return self.aveFuncLoc

    def setaveFuncCC(self,aveFuncCC):
        self.aveFuncCC = aveFuncCC

    def getaveFuncCC(self):
        return self.aveFuncCC

    def setmaxFuncND(self,maxFuncND):
        self.maxFuncND = maxFuncND

    def getmaxFuncND(self):
        return self.maxFuncND

    def setbcScore(self,bcScore):
        self.bcScore = bcScore

    def getbcScore(self):
        return self.bcScore

    def setbcScore1(self,bcScore1):
        self.bcScore1 = bcScore1

    def getbcScore1(self):
        return self.bcScore1

    def setnorBCPortNum(self,norBCPortNum):
        self.norBCPortNum = norBCPortNum

    def getnorBCPortNum(self):
        return self.norBCPortNum

    def setnorBCRunnableNum(self,norBCRunnableNum):
        self.norBCRunnableNum = norBCRunnableNum

    def getnorBCRunnableNum(self):
        return self.norBCRunnableNum

    def setnorBCInterfaceNum(self,norBCInterfaceNum):
        self.norBCInterfaceNum = norBCInterfaceNum

    def getnorBCInterfaceNum(self):
        return self.norBCInterfaceNum

    def setnorBCNoUseInterface(self,norBCNoUseInterface):
        self.norBCNoUseInterface = norBCNoUseInterface

    def getnorBCNoUseInterface(self):
        return self.norBCNoUseInterface

    def setnorBCIntraCoupling(self,norBCIntraCoupling):
        self.norBCIntraCoupling = norBCIntraCoupling

    def getnorBCIntraCoupling(self):
        return self.norBCIntraCoupling

    def setnorBCExtraCoupling(self, norBCExtraCoupling):
        self.norBCExtraCoupling = norBCExtraCoupling

    def getnorBCExtraCoupling(self):
        return self.norBCExtraCoupling

    def setnorBCExtraDependCoupling(self, norBCExtraDependCoupling):
        self.norBCExtraDependCoupling = norBCExtraDependCoupling

    def getnorBCExtraDependCoupling(self):
        return self.norBCExtraDependCoupling

    def setnorBCCC(self, norBCCC):
        self.norBCCC = norBCCC

    def getnorBCCC(self):
        return self.norBCCC

    def setnorBCMaxND(self, norBCMaxND):
        self.norBCMaxND = norBCMaxND

    def getnorBCMaxND(self):
        return self.norBCMaxND

    def setnorBCLoc(self, norBCLoc):
        self.norBCLoc = norBCLoc

    def getnorBCLoc(self):
        return self.norBCLoc

    def setnorBCAvgFuncLoc(self, norBCAvgFuncLoc):
        self.norBCAvgFuncLoc = norBCAvgFuncLoc

    def getnorBCAvgFuncLoc(self):
        return self.norBCAvgFuncLoc