class FCInfo:
    bcName = ''
    fcName = ''
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
    indegree = 0
    outdegree = 0
    loc = 0
    aveFuncLoc = 0
    aveFuncCC = 0
    maxFuncND = 0
    fcScore = 0
    fcScore1 = 0

    # Normalized indicator naming

    norFCIntraCoupling = 0.0
    norFCExtraCoupling = 0.0
    norFCExtraDependCoupling = 0.0
    norFCPortNum = 0.0
    norFCRunnableNum = 0.0
    norFCInterfaceNum = 0.0
    norFCNoUseInterface = 0.0
    norFCCC = 0.0 # FC Cyclomatic Complexity
    norFCMaxND = 0.0
    norFCLoc = 0.0
    norFCAvgFuncLoc = 0.0

    def setbcName(self,bcName):
        self.bcName = bcName

    def getbcName(self):
        return self.bcName

    def setfcName(self,fcName):
        self.fcName = fcName

    def getfcName(self):
        return self.fcName

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

    def setCSNum(self,CSNum):
        self.CSNum = CSNum

    def getCSNum(self):
        return self.CSNum

    def setSRNum(self,SRNum):
        self.SRNum = SRNum

    def getSRNum(self):
        return self.SRNum

    def setinterfaceNum(self,interfaceNum):
        self.interfaceNum = interfaceNum

    def getinterfaceNum(self):
        return self.interfaceNum

    def setnouseInterfaceNum(self,nouseInterfaceNum):
        self.nouseInterfaceNum = nouseInterfaceNum

    def getnouseInterfaceNum(self):
        return self.nouseInterfaceNum

    def setnouseInterfaceNum(self,nouseInterfaceNum):
        self.nouseInterfaceNum = nouseInterfaceNum

    def getnouseInterfaceNum(self):
        return self.nouseInterfaceNum

    def setintralInNum(self,intralInNum):
        self.intralInNum = intralInNum

    def getintralInNum(self):
        return self.intralInNum

    def setintralOutNum(self,intralOutNum):
        self.intralOutNum = intralOutNum

    def getintralOutNum(self):
        return self.intralOutNum

    def setextralInNum(self,extralInNum):
        self.extralInNum = extralInNum

    def getextralInNum(self):
        return self.extralInNum

    def setextralOutNum(self,extralOutNum):
        self.extralOutNum = extralOutNum

    def getextralOutNum(self):
        return self.extralOutNum

    def setextralDependNum(self,extralDependNum):
        self.extralDependNum = extralDependNum

    def getextralDependNum(self):
        return self.extralDependNum

    def setintralDependNum(self,intralDependNum):
        self.intralDependNum = intralDependNum

    def getintralDependNum(self):
        return self.intralDependNum

    def setrunnableNum(self,runnableNum):
        self.runnableNum = runnableNum

    def getrunnableNum(self):
        return self.runnableNum

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

    def setnorFCPortNum(self,norFCPortNum):
        self.norFCPortNum = norFCPortNum

    def getnorFCPortNum(self):
        return self.norFCPortNum

    def setnorFCRunnableNum(self,norFCRunnableNum):
        self.norFCRunnableNum = norFCRunnableNum

    def getnorFCRunnableNum(self):
        return self.norFCRunnableNum

    def setnorFCInterfaceNum(self,norFCInterfaceNum):
        self.norFCInterfaceNum = norFCInterfaceNum

    def getnorFCInterfaceNum(self):
        return self.norFCInterfaceNum

    def setnorFCNoUseInterface(self,norFCNoUseInterface):
        self.norFCNoUseInterface = norFCNoUseInterface

    def getnorFCNoUseInterface(self):
        return self.norFCNoUseInterface

    def setnorFCIntraCoupling(self,norFCIntraCoupling):
        self.norFCIntraCoupling = norFCIntraCoupling

    def getnorFCIntraCoupling(self):
        return self.norFCIntraCoupling

    def setnorFCExtraCoupling(self, norFCExtraCoupling):
        self.norFCExtraCoupling = norFCExtraCoupling

    def getnorFCExtraCoupling(self):
        return self.norFCExtraCoupling

    def setnorFCExtraDependCoupling(self, norFCExtraDependCoupling):
        self.norFCExtraDependCoupling = norFCExtraDependCoupling

    def getnorFCExtraDependCoupling(self):
        return self.norFCExtraDependCoupling

    def setnorFCCC(self,norFCCC):
        self.norFCCC = norFCCC

    def getnorFCCC(self):
        return self.norFCCC

    def setnorFCMaxND(self, norFCMaxND):
        self.norFCMaxND = norFCMaxND

    def getnorFCMaxND(self):
        return self.norFCMaxND

    def setnorFCLoc(self, norFCLoc):
        self.norFCLoc = norFCLoc

    def getnorFCLoc(self):
        return self.norFCLoc

    def setnorFCAvgFuncLoc(self, norFCAvgFuncLoc):
        self.norFCAvgFuncLoc = norFCAvgFuncLoc

    def getnorFCAvgFuncLoc(self):
        return self.norFCAvgFuncLoc

    def setfcScore(self, fcScore):
        self.fcScore = fcScore

    def getfcScore(self):
        return self.fcScore

    def setfcScore1(self, fcScore1):
        self.fcScore1 = fcScore1

    def getfcScore1(self):
        return self.fcScore1