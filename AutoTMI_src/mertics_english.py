import multiprocessing
import re

import lizard
from main_UI1_english import *

import sys
import os

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QUrl,QModelIndex
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtGui import QFontMetrics, QBrush
import main_metrics_english as Extract
from pyecharts.charts import Bar, Page
from pyecharts.charts import Graph as pyGraph
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import igraph as ig
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QCheckBox
from GraphMatrix import GraphMatrix
from lineofcode import LineCounter
from queue import Empty
from enum import Enum
import time
from unittest.mock import patch
import threading
from FCInfo import FCInfo
from BCInfo import BCInfo
import math
import ComplexityAnalyse as ComplexityAnalyse
from multiprocessing import Pool
import lizard
from FCCodeInfo import FCCodeInfo
from collections import Counter
from multiprocessing import Process

reserved_word = ["const","void","volatile","enum","struct","union",
                 "if","else","goto","switch","case","do","while","for","continue","break","return","default","typedef",
                 "auto","register","extern","static","sizeof",
                 "asm","_asm","__asm","ASM","_ASM","__ASM",
                 "public","protected","private","class","interface","abstract","implements","extends","new",
                 "import","package","null","true","false","boolean",
                 "final","super","this","native","stricttfp","synchronized","transient","volatile",
                 "catch","try","finally","throw","throws","assert","malloc","free","delete"
                 ]
datareserved_word = ["int", "long", "short", "float", "double", "char", "intptr_t", "uintptr_t", "unsigned", "signed","String"]
datareserved_word_size = [4, 4, 2, 4, 8, 1, 4, 4]


class mainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_mainUI()
        self.ui.setupUi(self)
        self.setWindowTitle("Automotive software maintainability index measurement")
        self.setWindowIcon(QIcon("images/icon/icons8-car-60.png"))
        self.input = 0
        self.bcNum = 0
        self.fcNum = 0
        self.ifNum = 0
        self.ruNum = 0
        self.match1 = 0
        self.match2 = 0
        self.view = 0
        self.viewindex = 0
        self.clusteringindex = 0
        #self.vertex_list = []
        # Threads
        self.background_thread = None
        self.widget_project = self.ui.tabWidget.widget(1)
        self.widget_metrics = self.ui.tabWidget.widget(2)
        self.ui.OpenProject.triggered.connect(self.open_fileDirectory)
        self.ui.OpenInfo.triggered.connect(lambda: self.add_tab(1))
        self.ui.OpenMetrics.triggered.connect(lambda: self.add_tab(2))
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget.tabBar().setTabButton(0, QTabBar.RightSide, None)
        for i in range(3,0,-1):
            self.ui.tabWidget.removeTab(i)
        self.ui.OpenInfo.setEnabled(False)
        self.ui.OpenMetrics.setEnabled(False)
        self.ui.pushButton_metrics_key.clicked.connect(lambda: self.changePage(20))
        self.ui.pushButton_metrics_nokey.clicked.connect(lambda: self.changePage(21))
        self.ui.pushButton_fc_report.clicked.connect(self.selectReport1)
        self.ui.pushButton_bc_report.clicked.connect(self.selectReport2)
        self.ui.tableWidget_bc_report.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_bc_report.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tableWidget_bc_report.verticalHeader().setVisible(False)
        self.ui.tableWidget_bc_report.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_bc_report.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.tableWidget_bc_report.setShowGrid(False)
        self.ui.tableWidget_bc_report.setRowCount(9)
        self.ui.tableWidget_bc_report.verticalHeader().setDefaultSectionSize(50)
        self.ui.tableWidget_bc_report.setMinimumHeight(500)
        self.ui.label_report_bc_conclusion.setWordWrap(True)
        self.ui.label_report_bc_conclusion_size.setWordWrap(True)
        self.ui.label_report_bc_conclusion_coupling.setWordWrap(True)
        self.ui.label_report_bc_conclusion_code.setWordWrap(True)
        self.ui.label_report_bc_advice_size.setWordWrap(True)
        self.ui.label_report_bc_advice_coupling.setWordWrap(True)
        self.ui.label_report_bc_advice_code.setWordWrap(True)
        self.ui.tableWidget_fc_report.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_fc_report.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.ui.tableWidget_fc_report.verticalHeader().setVisible(False)
        self.ui.tableWidget_fc_report.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget_fc_report.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.tableWidget_fc_report.setShowGrid(False)
        self.ui.tableWidget_fc_report.setRowCount(9)
        self.ui.tableWidget_fc_report.verticalHeader().setDefaultSectionSize(50)
        self.ui.tableWidget_fc_report.setMinimumHeight(500)
        self.ui.label_report_fc_conclusion.setWordWrap(True)
        self.ui.label_report_fc_conclusion_size.setWordWrap(True)
        self.ui.label_report_fc_conclusion_coupling.setWordWrap(True)
        self.ui.label_report_fc_conclusion_code.setWordWrap(True)
        self.ui.label_report_fc_advice_size.setWordWrap(True)
        self.ui.label_report_fc_advice_coupling.setWordWrap(True)
        self.ui.label_report_fc_advice_code.setWordWrap(True)

        self.ui.stackedWidget_metrics.setCurrentIndex(0)





        self.ui.label_27.setScaledContents(True)


        self.ui.label_25.setFixedSize(350, 250)
        projectDemo = QPixmap(':/icon/images/images/project.png')
        self.ui.label_25.setPixmap(projectDemo)
        self.ui.label_25.setScaledContents(True)
        self.ui.label_25.setStyleSheet('margin:5px;')

        self.ui.textEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ui.tabWidget.setCurrentIndex(0)




        keymetrics1 = ['IMC', 'EMC', 'IDC', 'NOR', 'NOI', 'NOFI',
                       'LOC', 'CC', 'MND']
        keymetrics2 = ['< 30', '< 20', '< 5', '< 5', '< 80', '< 10', '< 1000', '< 30', '< 5']
        keymetrics3 = ['Dependencies between elements within a component/module',
                       'Dependencies between different components/modules',
                       'Interdependencies between two or more components/modules',
                       'Number of runnable entity in a component/module',
                       'Number of interface in a component/module', 'Number of free interface in a component/module',
                       'Total number of lines of code in a component/module',
                       'Average cyclomatic complexity of elements in a component/module',
                       'Maximum nesting depth of control structures in a component/module']
        keymetrics4 = ['Dependencies between elements within a module',
                       'Dependencies between different modules',
                       'Interdependencies between two or more modules',
                       'Number of runnable entity in a module',
                       'Number of interface in a module', 'Number of free interface in a module',
                       'Total number of lines of code in a module',
                       'Average cyclomatic complexity of elements in a module',
                       'Maximum nesting depth of control structures in a module']
        keymetrics5 = ['< 200', '< 120', '< 5', '< 20', '< 600', '< 50', '< 8000', '< 30', '< 5']
        keyindex = keyindex1 = 0
        for i, j, k in zip(keymetrics1, keymetrics2, keymetrics3):
            item1 = QTableWidgetItem(i)
            item1.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_report.setItem(keyindex, 0, item1)
            item2 = QTableWidgetItem(j)
            item2.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_report.setItem(keyindex, 2, item2)
            item3 = QTableWidgetItem(k)
            item3.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_report.setItem(keyindex, 3, item3)
            keyindex += 1

        for i, j, k in zip(keymetrics1, keymetrics5, keymetrics4):
            item1 = QTableWidgetItem(i)
            item1.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_report.setItem(keyindex1, 0, item1)
            item2 = QTableWidgetItem(j)
            item2.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_report.setItem(keyindex1, 2, item2)
            item3 = QTableWidgetItem(k)
            item3.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_report.setItem(keyindex1, 3, item3)
            keyindex1 += 1

        self.ui.treeWidget_key.setStyleSheet(
            '''#treeWidget_key::item{height:40px;}#treeWidget_key{background-color:rgb(197,197,197);}''')
        self.ui.treeWidget_key.clicked.connect(lambda: self.onTreeWidgetClicked1(0))
        self.ui.treeWidget_key.invisibleRootItem().child(0).child(0).setSelected(True)
        self.ui.treeWidget_key.expandAll()
        self.ui.treeWidget_nokey.setStyleSheet(
            '''#treeWidget_nokey::item{height:40px;}#treeWidget_nokey{background-color:rgb(197,197,197);}''')
        self.ui.treeWidget_nokey.clicked.connect(lambda: self.onTreeWidgetClicked1(1))
        self.ui.treeWidget_nokey.invisibleRootItem().child(0).child(0).setSelected(True)
        self.ui.treeWidget_nokey.expandAll()


        keyList1 = ['BC', 'FC\nNum', 'Port\nNum', 'Interface\nNum', 'Runnable\nNum', 'Intra\nNum', 'Extra\nNum',
                    'Intra Depend\nInter FC', 'Extra Depend\nInter FC',
                    'Average Cyclomatic\nComplexity', 'Max Nesting Depth\nof Control Structures', 'Lines of\nCode',
                    'BMI', 'BC ASMI']
        keyListCount1 = len(keyList1)

        keyList2 = ['BC', 'NOP', 'NOI', 'NOFI', 'IMC', 'EMC', 'IDC', 'LOC', 'CC', 'MNDOCS', 'AFC', 'BC AMI', 'BMI']
        keyListCount2 = len(keyList2)

        keyList3 = ['BC\nName', 'FC\nName', 'Port\nNum', 'Interface\nScale', 'No Use\nInterface', 'intraInNum',
                    'intraOutNum', 'extraInNum', 'extraOutNum', 'Extra Depend\nInter EC',
                    'LOC', 'Avg Function\nLoc', 'Cyclomatic\nComplexity', 'Max Nesting\nDepth', 'BMI', 'FC ASMI',
                    'Review']
        keyListCount3 = len(keyList3)

        keyList4 = ['BC Name', 'FC Name', 'NOP', 'NOR', 'NOI', 'NDFI', 'IMC', 'EMC', 'IDC', 'LOC', 'AFC', 'CC',
                    'MNDOCS', 'BMI', 'FC ASMI', 'FC ASMI', 'Review']
        keyListCount4 = len(keyList4)

        keycodeList1 = ['Path', 'BC Name', 'Sum of\nfunctions', 'Sum of\nlines', 'Sum of FC',
                        'Ave\ncyclomatic\ncomplexity\nof functions',
                        'Max nesting\ndepth of\ncontrol\nstructures', 'Ave BMI\nof functions', 'The min BMI\nof FCs',
                        'Average\nFunction\nComplexity']
        keycodeListCount1 = len(keycodeList1)
        self.ui.tableWidget_BC_code.setColumnCount(keycodeListCount1)
        self.ui.tableWidget_BC_code.setHorizontalHeaderLabels(keycodeList1)
        self.ui.tableWidget_BC_code.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        #self.ui.tableWidget_BC_code.horizontalHeader().setStyleSheet("QHeaderView::section{background-color:rgb(197, 197, 197);};")
        #self.ui.tableWidget_BC_code.verticalHeader().setStyleSheet("QHeaderView::section{background-color:rgb(197, 197, 197);};")
        self.ui.tableWidget_BC_code.setShowGrid(False)
        keycodeList2 = ['Path', 'BC Name', 'FC Name', 'Sum of\nfunctions', 'Sum of\nlines', 'Sum of\nfiles',
                        'Ave\ncyclomatic\ncomplexity\nof functions',
                        'Max nesting\ndepth of\ncontrol\nstructures', 'The min BMI\nof FC\nfunctions',
                        'Ave BMI\nof functions', 'Average\nFunction\nComplexity'
                        ]
        keycodeListCount2 = len(keycodeList2)
        self.ui.tableWidget_FC_code.setColumnCount(keycodeListCount2)
        self.ui.tableWidget_FC_code.setHorizontalHeaderLabels(keycodeList2)
        self.ui.tableWidget_FC_code.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_FC_code.setShowGrid(False)
        keycodeList3 = ['Path', 'FC Name', ' Function Name', 'Lines of\ncode\nwithout\ncomment', 'Lines of\ncode',
                        'Lines of\ncode\ncomment',
                        'Cyclomatic\ncomplexity', 'Maxinum\nnesting of\ncontrol\nstructures', 'BMI', 'Start line',
                        'End line', 'Normalized\nComplexity', 'Comment\ndensity',
                        'Number of\nFunction\nParameter', 'Num of\nCallers', 'Num of\nDirect Calls']
        keycodeListCount3 = len(keycodeList3)
        self.ui.tableWidget_Function.setColumnCount(keycodeListCount3)
        self.ui.tableWidget_Function.setHorizontalHeaderLabels(keycodeList3)
        self.ui.tableWidget_Function.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_Function.setShowGrid(False)
        keycodeList4 = ['Path', 'Number of\nfunctions', 'Lines of\ncode', 'Lines of\nEffective Code',
                        'Lines of\nCode Comment', 'Comment\ndensity',
                        'Sum of\nCyclomatic\ncomplexity', 'Average\nCyclomatic\ncomplexity',
                        'Maxinum\nnesting of\ncontrol\nstructures', 'The min BMI\nof File\nfunctions',
                        'Ave BMI for\nfunctions',
                        ]
        keycodeListCount4 = len(keycodeList4)
        self.ui.tableWidget_File.setColumnCount(keycodeListCount4)
        self.ui.tableWidget_File.setHorizontalHeaderLabels(keycodeList4)
        self.ui.tableWidget_File.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_File.setShowGrid(False)
        keycodeList5 = ['Path', 'Name', 'Sum of\nfunctions', 'Sum of Lines', 'Sum of BCs', 'Sum of FCs',
                        'Average\nCyclomatic\ncomplexity of functions',
                        'Max\nnesting depth of\ncontrol\nstructures',
                        'Ave BMI for\nfunctions', 'The min BMI\nof File\nfunctions',
                        ]
        keycodeListCount5 = len(keycodeList5)
        self.ui.tableWidget_Project.setColumnCount(keycodeListCount5)
        self.ui.tableWidget_Project.setHorizontalHeaderLabels(keycodeList5)
        self.ui.tableWidget_Project.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_Project.setShowGrid(False)
        keyarxmlList1 = ['BC', 'FC\nNum', 'Port\nNum', 'Interface\nNum', 'No Use\nInterface', 'Runnable\nNum',
                         'Intra\nNum', 'Extra\nNum',
                         'Intra Depend\nInter FC', 'Extra Depend\nInter FC', ]
        keyarxmlListCount1 = len(keyarxmlList1)
        self.ui.tableWidget_BC_arxml.setColumnCount(keyarxmlListCount1)
        self.ui.tableWidget_BC_arxml.setHorizontalHeaderLabels(keyarxmlList1)
        self.ui.tableWidget_BC_arxml.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_BC_arxml.setShowGrid(False)
        # self.ui.tableWidget_BC_arxml.setStyleSheet("QTableWidget::Item{border-bottom:1px solid rgb(229, 229, 229);background-color:white;}")
        keyarxmlList2 = ['BC\nName', 'FC\nName', 'Port\nNum', 'Interface\nScale', 'No Use\nInterface', 'intraInNum',
                         'intraOutNum', 'extraInNum', 'extraOutNum', 'Extra Depend\nInter EC', 'Runnable\nNum']
        keyarxmlListCount2 = len(keyarxmlList2)
        self.ui.tableWidget_FC_arxml.setColumnCount(keyarxmlListCount2)
        self.ui.tableWidget_FC_arxml.setHorizontalHeaderLabels(keyarxmlList2)
        self.ui.tableWidget_FC_arxml.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_FC_arxml.setShowGrid(False)
        # asmi1 = ['BC Name','FC Name','NOP','NOR','NOI','NOFI','IMC','EMC','IDC','LOC','AFC','CC','MNDOCS','BMI','FC ASMI']
        asmi1 = ['BC', 'FC', 'Port\nNum', 'Runnable\nNum', 'Interface\nNum', 'No use\nInterface', 'Intra\nCoupling',
                 'Extra\nCoupling', 'Depend\nCoupling', 'LOC', 'Avg\nFunction\nLOC', 'Average\nCyclomatic\nComplexity',
                 'Max\nNesting\nDepth', 'FC ASMI', 'Review']
        asmiCount1 = len(asmi1)
        self.ui.tableWidget_fc_ASMI.setColumnCount(asmiCount1)
        self.ui.tableWidget_fc_ASMI.setHorizontalHeaderLabels(asmi1)
        self.ui.tableWidget_fc_ASMI.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_fc_ASMI.setShowGrid(False)
        # asmi2 = ['BC','NOP','NOI','NOFI','IMC','EMC','IDC','LOC','CC','MNDOCS','BMI','BC ASMI']
        '''asmi2 = ['BC', 'FC\nNum', 'Port\nNum', 'Interface\nNum', 'Runnable\nNum', 'Intra\nCoupling', 'Extra\nCoupling',
                 'Depend\nCoupling', 'Average\nCyclomatic\nComplexity', 'Max Nesting\nDepth of\nControl Structures',
                 'LOC', 'BC ASMI', 'Review']'''
        asmi2 = ['BC', 'FC\nNum', 'Port\nNum', 'NOI', 'NOR','NOFI', 'IMC', 'EMC',
                 'IDC', 'CC', 'MND',
                 'LOC', 'TMI', 'Review']
        asmiCount2 = len(asmi2)
        self.ui.tableWidget_bc_ASMI.setColumnCount(asmiCount2)
        self.ui.tableWidget_bc_ASMI.setHorizontalHeaderLabels(asmi2)
        self.ui.tableWidget_bc_ASMI.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_bc_ASMI.setShowGrid(False)
        # self.ui.tableWidget_bc_ASMI.setStyleSheet("QTableWidget::Item{border-bottom:1px solid gray;background-color:white;}")
        nokeybcarxml = ['BC', 'Number of\nS/R Interface', 'Number of\nC/S Interface', 'Number of\nProvide Port',
                        'Number of\nRequire Port',
                        'intraInNum', 'intraOutNum', 'extraInNum', 'extraOutNum', 'Inter-Depend\nCoupling', 'Indegree',
                        'Outdegree', 'Instability']
        nokeybcarxmlCount = len(nokeybcarxml)
        self.ui.tableWidget_nokeyBC_arxml.setColumnCount(nokeybcarxmlCount)
        self.ui.tableWidget_nokeyBC_arxml.setHorizontalHeaderLabels(nokeybcarxml)
        self.ui.tableWidget_nokeyBC_arxml.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_nokeyBC_arxml.setShowGrid(False)
        nokeyfcarxml = ['BC Name', 'FC Name', 'Number of\nS/R Interface', 'Number of\nC/S Interface',
                        'Number of\nProvide Port', 'Number of\nRequire Port',
                        'Intra\nNum', 'Extra\nNum', 'Intra Depend\nInter EC', 'Inter-Depend\nCoupling', 'Indegree',
                        'Outdegree', 'Instability']
        nokeyfcarxmlCount = len(nokeyfcarxml)
        self.ui.tableWidget_nokeyFC_arxml.setColumnCount(nokeyfcarxmlCount)
        self.ui.tableWidget_nokeyFC_arxml.setHorizontalHeaderLabels(nokeyfcarxml)
        self.ui.tableWidget_nokeyFC_arxml.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_nokeyFC_arxml.setShowGrid(False)
        nokeyproject = ['Path', 'Name', 'Sum of\nEffective\nLines', 'Num of\nStatement', 'Num of\nBranch',
                        'Num of\nToken',
                        'Num of\nGlobal\nVariable', 'Num of\nStatic Global\nVariable',
                        'Num of\nNon-static\nGlobal\nVariable', 'Sum of\nCalls', 'Sum of\nRecursion', ]
        nokeyprojectCount = len(nokeyproject)
        self.ui.tableWidget_project_nokey.setColumnCount(nokeyprojectCount)
        self.ui.tableWidget_project_nokey.setHorizontalHeaderLabels(nokeyproject)
        self.ui.tableWidget_project_nokey.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_project_nokey.setShowGrid(False)

        nokeyfunction = ['Path', 'FC Name', 'Function Name', 'Num of tokens', 'Num of if', 'Num of equal',
                         'Num of\nfor', 'Num of\nwhile', 'Num of\ngoto',
                         'Num of\ncatch', 'Num of\nbreak', 'Num of\ncontinue', 'Num of\nreturn',
                         'Num of\nNon-structured\nStatement', 'Number of\nViolations in\nStructured\nProgramming',
                         'Num of\ntotal\noperator', 'Num of\ntotal\noprand',
                         'Num of\ndifferent\noperator', 'Num of\ndifferent\noprand', 'Num of\nStatements',
                         'Length of\nVocabulary', 'Length of\nProgram', 'Calculated\nlength of\nProgram',
                         'Program\nVolume', 'Program\nLevel',
                         'Program\nDifficulty', 'Program\nEffort', 'Language\nLevel', 'Program\nTime',
                         'Ave\nStatement\nSize', 'Calculated\nnum of Program Effort', 'Frequency\nVocabulary',
                         'Num of\nStatements', 'Num of\nBranches', 'Percent Branch\nStatements',
                         'Num of\nLocal Variable', 'Num of\nStatic Local\nvariable',
                         'Num of\nNon-static\nLocal Variable', 'Num of\nRecusion', 'Number of\nDangling\nElse-Ifs','Size of\nstack']
        nokeyfunctionCount = len(nokeyfunction)
        self.ui.tableWidget_Function_nokey.setColumnCount(nokeyfunctionCount)
        self.ui.tableWidget_Function_nokey.setHorizontalHeaderLabels(nokeyfunction)
        self.ui.tableWidget_Function_nokey.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_Function_nokey.setShowGrid(False)
        nokeyfile = ['Path', 'Num of\nStatement', 'Num of\nBranch', 'Percent Branch\nStatements',
                     'Ave Statements\nper Function', 'Num of\nToken', 'Num of\nGlobal\nVariable',
                     'Num of\nStatic Global\nVariable',
                     'Num of\nNon-static\nGlobal\nVariable', 'Sum of\nCalls', 'Sum of\nRecursion',
                     'Percent of\nRecursion Calls', ]
        nokeyfileCount = len(nokeyfile)
        self.ui.tableWidget_File_nokey.setColumnCount(nokeyfileCount)
        self.ui.tableWidget_File_nokey.setHorizontalHeaderLabels(nokeyfile)
        self.ui.tableWidget_File_nokey.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_File_nokey.setShowGrid(False)
        nokeyfc = ['Path', 'BC Name', 'FC Name', 'Num of\nStatement', 'Num of\nBranch', 'Num of\nToken',
                   'Num of\nGlobal\nVariable', 'Num of\nStatic Global\nVariable',
                   'Num of\nNon-static\nGlobal\nVariable', 'Sum of\nCalls', 'Sum of\nRecursion', ]
        nokeyfcCount = len(nokeyfc)
        self.ui.tableWidget_nokeyFC_code.setColumnCount(nokeyfcCount)
        self.ui.tableWidget_nokeyFC_code.setHorizontalHeaderLabels(nokeyfc)
        self.ui.tableWidget_nokeyFC_code.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_nokeyFC_code.setShowGrid(False)
        nokeybc = ['Path', 'BC Name', 'Num of\nStatement', 'Num of\nBranch',   'Num of\nToken',
                   'Num of\nGlobal\nVariable', 'Num of\nStatic Global\nVariable',
                   'Num of\nNon-static\nGlobal\nVariable', 'Sum of\nCalls', 'Sum of\nRecursion', ]
        nokeybcCount = len(nokeybc)
        self.ui.tableWidget_nokeyBC_code.setColumnCount(nokeybcCount)
        self.ui.tableWidget_nokeyBC_code.setHorizontalHeaderLabels(nokeybc)
        self.ui.tableWidget_nokeyBC_code.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
        self.ui.tableWidget_nokeyBC_code.setShowGrid(False)


        self.show()

    def close_tab(self,index):
        tabindex = self.ui.tabWidget.widget(index).objectName()
        if tabindex == 'tab_project':
            self.widget_project = self.ui.tabWidget.widget(index)
        elif tabindex == 'tab_view':
            self.widget_view = self.ui.tabWidget.widget(index)
        elif tabindex == 'tab_metrics':
            self.widget_metrics = self.ui.tabWidget.widget(index)
        elif tabindex == 'tab_cluster':
            self.widget_cluster = self.ui.tabWidget.widget(index)
        self.ui.tabWidget.widget(index).destroy()
        self.ui.tabWidget.removeTab(index)

    def add_tab(self,index):

        if index == 1:
            self.ui.tabWidget.addTab(self.widget_project,'Basic Information')
            self.ui.tabWidget.setCurrentWidget(self.widget_project)
        elif index == 2:

            self.ui.tabWidget.addTab(self.widget_metrics, 'Maintainability measurement')
            self.ui.tabWidget.setCurrentWidget(self.widget_metrics)


    def changePage(self, index):
        if index // 10 == 0:
            if index == 0:
                self.ui.stackedWidget.setCurrentIndex(index)
            elif index == 4:
                self.ui.stackedWidget.setCurrentIndex(index)
            elif self.input == 0:
                QMessageBox.critical(self, "Error", "Please import file first!")
            else:
                if index == 1:
                    self.ui.stackedWidget.setCurrentIndex(index)
                elif index == 2:
                    self.ui.stackedWidget.setCurrentIndex(index)
                elif index == 3:
                    self.ui.stackedWidget.setCurrentIndex(index)
        elif index // 10 == 1:
            if index % 10 == 0:
                self.ui.stackedWidget_view.setCurrentIndex(index%10)
                self.ui.pushButton_view_BC.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.pushButton_view_FC.setStyleSheet("color: rgb(121, 121, 121);")
                self.ui.pushButton_view_all.setStyleSheet("color: rgb(121, 121, 121);")
                self.ui.pushButton_view_runnable.setStyleSheet("color: rgb(121, 121, 121);")
            elif index % 10 == 1:
                self.ui.stackedWidget_view.setCurrentIndex(index % 10)
                self.ui.pushButton_view_FC.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.pushButton_view_BC.setStyleSheet("color: rgb(121, 121, 121);")
                self.ui.pushButton_view_all.setStyleSheet("color: rgb(121, 121, 121);")
                self.ui.pushButton_view_runnable.setStyleSheet("color: rgb(121, 121, 121);")
        elif index // 10 == 2:
            if index % 10 == 0:
                self.ui.stackedWidget_metrics.setCurrentIndex(index%10)
                self.ui.pushButton_metrics_key.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.pushButton_metrics_nokey.setStyleSheet("color: rgb(121, 121, 121);")
            elif index % 10 == 1:
                self.ui.stackedWidget_metrics.setCurrentIndex(index%10)
                self.ui.pushButton_metrics_nokey.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.pushButton_metrics_key.setStyleSheet("color: rgb(121, 121, 121);")
        elif index // 10 == 3:
            if index % 10 == 0:
                self.ui.stackedWidget_cluster.setCurrentIndex(index%10)
                self.ui.pushButton_cluster_main.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.pushButton_cluster_report.setStyleSheet("color: rgb(121, 121, 121);")
            elif index % 10 == 1:
                self.ui.stackedWidget_cluster.setCurrentIndex(index % 10)
                self.ui.pushButton_cluster_report.setStyleSheet("color: rgb(0, 0, 0);")
                self.ui.pushButton_cluster_main.setStyleSheet("color: rgb(121, 121, 121);")


    def onTreeWidgetClicked1(self, index):
        if index == 0:
            item1 = self.ui.treeWidget_key.currentItem()
            if item1.text(0) == 'BC':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(0)
            elif item1.text(0) == 'FC':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(1)
            elif item1.text(0) == 'Project':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(2)
            elif item1.text(0) == 'Module':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(3)
            elif item1.text(0) == 'SWC':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(4)
            elif item1.text(0) == 'File':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(5)
            elif item1.text(0) == 'Function':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(6)
            elif item1.text(0) == 'BC report':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(7)
            elif item1.text(0) == 'FC report':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(8)
            elif item1.text(0) == 'BC ASMI':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(9)
            elif item1.text(0) == 'FC ASMI':
                self.ui.stackedWidget_metrics_key.setCurrentIndex(10)
        elif index == 1:
            item1 = self.ui.treeWidget_nokey.currentItem()
            if item1.text(0) == "BC":
                self.ui.stackedWidget_metrics_nokey.setCurrentIndex(0)
            elif item1.text(0) == "FC":
                self.ui.stackedWidget_metrics_nokey.setCurrentIndex(1)
            elif item1.text(0) == "Project":
                self.ui.stackedWidget_metrics_nokey.setCurrentIndex(2)
            elif item1.text(0) == "Module":
                self.ui.stackedWidget_metrics_nokey.setCurrentIndex(3)
            elif item1.text(0) == "SWC":
                self.ui.stackedWidget_metrics_nokey.setCurrentIndex(4)
            elif item1.text(0) == "File":
                self.ui.stackedWidget_metrics_nokey.setCurrentIndex(5)
            elif item1.text(0) == "Function":
                self.ui.stackedWidget_metrics_nokey.setCurrentIndex(6)

    def open_fileDirectory(self, Filepath):
        m = QtWidgets.QFileDialog.getExistingDirectory(None, "Select File", "C:/")
        if m != '':
            self.ui.textEdit.append(
                '<font>' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + " "+ m + ' is selected.' + '\n')
            self.ui.textEdit.append(
                '<font>' + time.strftime('%Y-%m-%d %H:%M:%S',
                                         time.localtime()) + ' Import successfully···</font>' + '\n')
            from PyQt5.QtWidgets import QApplication
            QApplication.processEvents()
            self.analyseProject(m)

    def analyseProject(self,projectDirection):
        self.input = 1
        self.ui.OpenInfo.setEnabled(True)
        self.ui.OpenView.setEnabled(True)
        self.ui.OpenMetrics.setEnabled(True)
        self.ui.ModuleCluster.setEnabled(True)
        # self.fileInfo(projectDirection)
        for file in os.listdir(projectDirection):
            full_file_path = os.path.join(projectDirection, file)
            full_file_path = full_file_path.replace('/', '\\')
            if os.path.isdir(full_file_path):
                if os.path.basename(full_file_path) == "ASW":
                    self.fileInfo(full_file_path)
                    self.analyseArxml(full_file_path)
                    self.ui.textEdit.append('<font>' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + ' Analyse successfully!</font>' + '\n')

    def analyseArxml(self, ASWDirection):
        QApplication.processEvents()
        filelist = []
        softwareName = ''
        arxmlDirection = ASWDirection
        arxmlDirection = arxmlDirection.replace('/', '\\')
        softwareName = arxmlDirection.split('\\')[-2]
        self.ui.softwareName.setText(softwareName)
        self.softwarename = softwareName
        arxmlDirection1 = os.path.split(arxmlDirection)[0]
        swc = Extract.extractPortInfo(arxmlDirection)
        arxmlInfo = swc[0]
        swcNum = swc[1]
        runnableNum = swc[2]
        ifNum = swc[3]
        ifList = swc[4]
        self.ifNum = ifNum
        self.fcNum = swcNum
        self.ruNum = runnableNum
        self.ifList = ifList
        self.interfaceList = swc[5]
        self.nouseinterfaceList = swc[6]
        self.modulemap = swc[7]
        portNum = len(arxmlInfo)
        arxmlInfo1 = Extract.portList2Array(arxmlInfo)
        self.port = arxmlInfo1
        portnum1 = len(self.port)
        arr = Extract.topSwc(self.port)

        self.arr = arr
        metrix = Extract.getMetrix(self.port)
        self.matrix = metrix
        swcnum = Extract.getNum(metrix)
        self.vertex_list = Extract.getVertex(metrix)
        module = [i[1] for i in self.modulemap]
        modules = []
        for i in self.vertex_list:
            mindex = module.index(i)
            modules.append(self.modulemap[mindex][0])
        dicmodule = dict(zip(self.vertex_list, modules))
        self.bc_fc = dicmodule
        rolelist = set([v for k, v in dicmodule.items()])
        rolelist = sorted(rolelist)
        self.modulelist = rolelist
        fcNumList = []
        self.ui.Number_BC_Total.setText(str(len(self.modulelist)))
        self.ui.Number_FC_Total.setText(str(len(self.vertex_list)))

        self.ui.listWidget_fc_report.clear()
        for i in self.vertex_list:
            box = QRadioButton(i)
            item = QListWidgetItem()
            self.ui.listWidget_fc_report.addItem(item)
            self.ui.listWidget_fc_report.setItemWidget(item, box)
            self.ui.listWidget_fc_report.setSpacing(5)
        self.ui.listWidget_fc_report.setStyleSheet("color:gray;font-size: 15px")

        self.ui.listWidget_bc_report.clear()
        for i in self.modulelist:
            box = QRadioButton(i)
            item = QListWidgetItem()
            self.ui.listWidget_bc_report.addItem(item)
            self.ui.listWidget_bc_report.setItemWidget(item, box)
            self.ui.listWidget_bc_report.setSpacing(5)
        self.ui.listWidget_bc_report.setStyleSheet("color:gray;font-size: 15px")


        arr = []
        fcIntralIn = []
        fcIntralOut = []
        fcExtralIn = []
        fcExtralOut = []
        fcIntralDepend = []
        fcExtralDepend = []
        inswc = []
        outswc = []
        num = self.matrix.getVertexNum()
        for a in range(0, num):
            arr.append([])
            fcIntralIn.append(0)
            fcIntralOut.append(0)
            fcExtralIn.append(0)
            fcExtralOut.append(0)
            fcIntralDepend.append(0)
            fcExtralDepend.append(0)
            inswc.append(0)
            outswc.append(0)
        for i in range(0, self.matrix.getVertexNum()):
            for j in range(0, self.matrix.getVertexNum()):
                arr[i].append(self.matrix.getEdgeWeight1(i, j))

        for i in range(0, self.matrix.getVertexNum()):
            for j in range(0, self.matrix.getVertexNum()):
                if arr[i][j] != 0:
                    sendSwc = self.vertex_list[i]
                    receiveSwc = self.vertex_list[j]
                    outswc[i] += 1
                    inswc[j] += 1
                    if self.bc_fc[sendSwc] == self.bc_fc[receiveSwc]:
                        fcIntralOut[i] += arr[i][j]
                        fcIntralIn[j] += arr[i][j]
                    else:
                        fcExtralOut[i] += arr[i][j]
                        fcExtralIn[j] += arr[i][j]
                    if arr[j][i] != 0:
                        if self.bc_fc[sendSwc] == self.bc_fc[receiveSwc]:
                            fcIntralDepend[i] += 1
                        else:
                            fcExtralDepend[i] += 1

        self.fcInfoList = []
        self.fcInfoTable = []
        totalPortNum = 0
        totalInterfaceNum = 0
        totalRunnableNum = 0
        for i in range(0, self.matrix.getVertexNum()):
            fcInfo = FCInfo()
            fcInfo.setbcName(self.bc_fc[self.vertex_list[i]])
            fcInfo.setfcName(self.vertex_list[i])
            fcInfo.setportNum(self.ifList[i][1])
            fcInfo.setinterfaceNum(self.ifList[i][2])
            fcInfo.setCSNum(self.ifList[i][4])
            fcInfo.setSRNum(self.ifList[i][5])
            fcInfo.setpportNum(self.ifList[i][6])
            fcInfo.setrportNum(self.ifList[i][7])
            fcInfo.setintralInNum(fcIntralIn[i])
            fcInfo.setintralOutNum(fcIntralOut[i])
            fcInfo.setextralInNum(fcExtralIn[i])
            fcInfo.setextralOutNum(fcExtralOut[i])
            fcInfo.setnouseInterfaceNum(
                len([element for element in self.nouseinterfaceList if element.getSWCName() == self.vertex_list[i]]))
            fcInfo.setintralDependNum(fcIntralDepend[i])
            fcInfo.setextralDependNum(fcExtralDepend[i])
            fcInfo.setrunnableNum(self.ifList[i][3])
            fcInfo.setindegree(inswc[i])
            fcInfo.setoutdegree(outswc[i])

            fcInfo.setloc(self.fcList[i]['lines_of_effective_code'])
            fcInfo.setaveFuncLoc(self.fcList[i]['ave_function_complexity'])
            fcInfo.setaveFuncCC(self.fcList[i]['ave_cyclomatic_complexity'])
            fcInfo.setmaxFuncND(self.fcList[i]['max_nested_structures'])
            if fcInfo.getintralInNum() + fcInfo.getintralOutNum() + fcInfo.getextralInNum() + fcInfo.getextralOutNum() == 0:
                instability = 0
            else:
                instability = (fcInfo.getintralOutNum() + fcInfo.getextralOutNum()) / (
                        fcInfo.getintralInNum() + fcInfo.getintralOutNum() + fcInfo.getextralInNum() + fcInfo.getextralOutNum())

            self.fcInfoList.append(fcInfo)
            self.fcInfoTable.append(
                [fcInfo.getbcName(), fcInfo.getfcName(), fcInfo.getportNum(), fcInfo.getinterfaceNum(),
                 fcInfo.getnouseInterfaceNum(), fcInfo.getintralInNum(), fcInfo.getintralOutNum(),
                 fcInfo.getextralInNum(), fcInfo.getextralOutNum(), fcInfo.getextralDependNum(),
                 fcInfo.getintralDependNum(), fcInfo.getrunnableNum(), fcInfo.getSRNum(), fcInfo.getCSNum(),
                 fcInfo.getpportNum(), fcInfo.getrportNum(),
                 fcInfo.getintralInNum() + fcInfo.getintralOutNum(), fcInfo.getextralInNum() + fcInfo.getextralOutNum(),
                 fcInfo.getintralDependNum(), fcInfo.getintralDependNum() + fcInfo.getextralDependNum(),
                 fcInfo.getindegree(), fcInfo.getoutdegree(),
                 instability])
            totalPortNum += fcInfo.getportNum()
            totalInterfaceNum += fcInfo.getinterfaceNum()
            totalRunnableNum += fcInfo.getrunnableNum()
        self.ui.Number_Port_Total.setText(str(totalPortNum))
        self.ui.Number_Interface_Total.setText(str(totalInterfaceNum))
        self.ui.Number_Runnable_Total.setText(str(totalRunnableNum))
        for i in range(0, self.matrix.getVertexNum()):
            row = self.ui.tableWidget_FC_arxml.rowCount()
            self.ui.tableWidget_FC_arxml.insertRow(row)
            for j in range(0, 11):
                item = QTableWidgetItem(str(self.fcInfoTable[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_arxml.setItem(row, j, item)
            row = self.ui.tableWidget_nokeyFC_arxml.rowCount()
            self.ui.tableWidget_nokeyFC_arxml.insertRow(row)
            item = QTableWidgetItem(str(self.fcInfoTable[i][0]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 0, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][1]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 1, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][12]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 2, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][13]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 3, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][14]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 4, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][15]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 5, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][16]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 6, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][17]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 7, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][18]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 8, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][19]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 9, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][20]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 10, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][21]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 11, item)
            item = QTableWidgetItem(str(self.fcInfoTable[i][22]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyFC_arxml.setItem(row, 12, item)

        self.ui.tableWidget_FC_arxml.resizeColumnsToContents()
        self.ui.tableWidget_FC_arxml.sortItems(0, Qt.AscendingOrder)
        self.ui.tableWidget_nokeyFC_arxml.resizeColumnsToContents()
        self.ui.tableWidget_nokeyFC_arxml.sortItems(0, Qt.AscendingOrder)
        self.calcuFCASMI()

        self.bcInfoTable = []
        self.bcInfoList = []
        bcindex = 0
        for i in self.modulelist:
            bcInfo = BCInfo()
            bcInfo.setbcName(i)
            bcname = ''
            norBCIntraCoupling = 0.0
            norBCExtraCoupling = 0.0
            norBCExtraDependCoupling = 0.0
            norBCPortNum = 0.0
            norBCRunnableNum = 0.0
            norBCInterfaceNum = 0.0
            norBCNoUseInterface = 0.0
            norBCCC = 0.0
            norBCMaxND = 0.0
            norBCLoc = 0.0
            bcScore = 0.0
            for j in self.fcInfoList:
                if i == j.getbcName():
                    bcInfo.setfcNum(bcInfo.getfcNum() + 1)
                    bcInfo.setportNum(bcInfo.getportNum() + j.getportNum())
                    bcInfo.setpportNum(bcInfo.getpportNum() + j.getpportNum())
                    bcInfo.setrportNum(bcInfo.getrportNum() + j.getrportNum())
                    bcInfo.setinterfaceNum(bcInfo.getinterfaceNum() + j.getinterfaceNum())
                    bcInfo.setnouseInterfaceNum(bcInfo.getnouseInterfaceNum() + j.getnouseInterfaceNum())
                    bcInfo.setCSNum(bcInfo.getCSNum() + j.getCSNum())
                    bcInfo.setSRNum(bcInfo.getSRNum() + j.getSRNum())
                    bcInfo.setrunnableNum(bcInfo.getrunnableNum() + j.getrunnableNum())
                    bcInfo.setintralInNum(bcInfo.getintralInNum() + j.getintralInNum())
                    bcInfo.setintralOutNum(bcInfo.getintralOutNum() + j.getintralOutNum())
                    bcInfo.setextralInNum(bcInfo.getextralInNum() + j.getextralInNum())
                    bcInfo.setextralOutNum(bcInfo.getextralOutNum() + j.getextralOutNum())
                    bcInfo.settotalIntraNum(bcInfo.gettotalIntraNum() + j.getintralInNum() + j.getintralOutNum())
                    bcInfo.settotalExtraNum(bcInfo.gettotalExtraNum() + j.getextralInNum() + j.getextralOutNum())
                    bcInfo.setintralDependNum(bcInfo.getintralDependNum() + j.getintralDependNum())
                    bcInfo.setextralDependNum(bcInfo.getextralDependNum() + j.getextralDependNum())
                    bcInfo.setindegree(bcInfo.getindegree() + j.getindegree())
                    bcInfo.setoutdegree(bcInfo.getoutdegree() + j.getoutdegree())

                    norBCPortNum += j.getnorFCPortNum()
                    norBCRunnableNum += j.getnorFCRunnableNum()
                    norBCInterfaceNum += j.getnorFCInterfaceNum()
                    norBCNoUseInterface += j.getnorFCNoUseInterface()
                    norBCIntraCoupling += j.getnorFCIntraCoupling()
                    norBCExtraCoupling += j.getnorFCExtraCoupling()
                    norBCExtraDependCoupling += j.getnorFCExtraDependCoupling()
                    norBCCC += j.getnorFCCC()
                    norBCLoc += j.getnorFCLoc()
                    norBCMaxND += j.getnorFCMaxND()
                    bcScore += j.getfcScore()

                    if bcInfo.getintralInNum() + bcInfo.getintralOutNum() + bcInfo.getextralInNum() + bcInfo.getextralOutNum() == 0:
                        instability = 0
                    else:
                        instability = (bcInfo.getintralOutNum() + bcInfo.getextralOutNum()) / (
                                bcInfo.getintralInNum() + bcInfo.getintralOutNum() + bcInfo.getextralInNum() + bcInfo.getextralOutNum())
            bcInfo.setloc(self.bcList[bcindex]['lines_of_code'])
            bcInfo.setaveFuncLoc(self.bcList[bcindex]['ave_function_complexity'])
            bcInfo.setaveFuncCC(self.bcList[bcindex]['ave_cyclomatic_complexity'])
            bcInfo.setmaxFuncND(self.bcList[bcindex]['max_nested_structures'])
            bcindex += 1

            self.bcInfoTable.append(
                [bcInfo.getbcName(), bcInfo.getfcNum(), bcInfo.getportNum(), bcInfo.getinterfaceNum(),
                 bcInfo.getnouseInterfaceNum(), bcInfo.getrunnableNum(),
                 bcInfo.gettotalIntraNum(), bcInfo.gettotalExtraNum(), bcInfo.getintralDependNum(),
                 bcInfo.getextralDependNum(), bcInfo.getSRNum(), bcInfo.getCSNum(), bcInfo.getpportNum(),
                 bcInfo.getrportNum(),
                 bcInfo.getintralInNum(), bcInfo.getintralOutNum(), bcInfo.getextralInNum(), bcInfo.getextralOutNum(),
                 bcInfo.getintralDependNum() + bcInfo.getextralDependNum(), bcInfo.getindegree(), bcInfo.getoutdegree(),
                 (bcInfo.getintralOutNum() + bcInfo.getextralOutNum()) / (
                             bcInfo.getintralInNum() + bcInfo.getintralOutNum() + bcInfo.getextralInNum() + bcInfo.getextralOutNum())])
            if bcInfo.getfcNum() > 0:
                bcInfo.setnorBCIntraCoupling(norBCIntraCoupling / bcInfo.getfcNum())
                bcInfo.setnorBCExtraCoupling(norBCExtraCoupling / bcInfo.getfcNum())
                bcInfo.setnorBCExtraDependCoupling(norBCExtraDependCoupling / bcInfo.getfcNum())
                bcInfo.setnorBCPortNum(norBCPortNum / bcInfo.getfcNum())
                bcInfo.setnorBCRunnableNum(norBCRunnableNum / bcInfo.getfcNum())
                bcInfo.setnorBCInterfaceNum(norBCInterfaceNum / bcInfo.getfcNum())
                bcInfo.setnorBCNoUseInterface(norBCNoUseInterface / bcInfo.getfcNum())
                bcInfo.setnorBCLoc(norBCLoc / bcInfo.getfcNum())
                bcInfo.setnorBCCC(norBCCC / bcInfo.getfcNum())
                bcInfo.setnorBCMaxND(norBCMaxND / bcInfo.getfcNum())
                bcInfo.setbcScore(bcScore / bcInfo.getfcNum())
                bcInfo.setbcScore1((bcScore / bcInfo.getfcNum()) * 50)
            self.bcInfoList.append(bcInfo)
        for i in range(0, len(self.bcInfoTable)):
            row = self.ui.tableWidget_BC_arxml.rowCount()
            self.ui.tableWidget_BC_arxml.insertRow(row)
            for j in range(0, 10):
                item = QTableWidgetItem(str(self.bcInfoTable[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_arxml.setItem(row, j, item)
            row = self.ui.tableWidget_nokeyBC_arxml.rowCount()
            self.ui.tableWidget_nokeyBC_arxml.insertRow(row)
            # self.ui.tableWidget_nokeyBC_arxml.setItem(row,0,QTableWidgetItem(str(self.bcInfoTable[i][0])).setTextAlignment(Qt.AlignCenter))
            item = QTableWidgetItem(str(self.bcInfoTable[i][0]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 0, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][10]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 1, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][11]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 2, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][12]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 3, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][13]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 4, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][14]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 5, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][15]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 6, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][16]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 7, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][17]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 8, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][18]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 9, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][19]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 10, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][20]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 11, item)
            item = QTableWidgetItem(str(self.bcInfoTable[i][21]))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_nokeyBC_arxml.setItem(row, 12, item)
        self.ui.tableWidget_BC_arxml.resizeColumnsToContents()
        self.ui.tableWidget_BC_arxml.sortItems(0, Qt.AscendingOrder)
        self.ui.tableWidget_nokeyBC_arxml.resizeColumnsToContents()
        self.ui.tableWidget_nokeyBC_arxml.sortItems(0, Qt.AscendingOrder)
        self.ui.label_14.setText("Number of ports, interfaces, and Runnable of BCS in "+self.softwarename)
        arrindex = sorted(self.bcInfoTable, key = (lambda x:x[2]))
        bar = (
            Bar()
            .add_xaxis([i[0] for i in arrindex])
            .add_yaxis("Port Number", [i[2] for i in arrindex], itemstyle_opts=opts.ItemStyleOpts(color="rgb(84, 112, 198)"))
            .add_yaxis("Interface Number", [i[3] for i in arrindex],itemstyle_opts=opts.ItemStyleOpts(color="rgb(145, 204, 117)"))
            .add_yaxis("Runnable Number", [i[5] for i in arrindex],itemstyle_opts=opts.ItemStyleOpts(color="rgb(250, 200, 88)"))
            .reversal_axis()
            .set_global_opts(title_opts=opts.TitleOpts(title="BC\nName"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False, position="right"))
        )
        bar.render(path='BC_info.html')
        self.ui.webEngineView_info.setUrl(QUrl('file:///BC_info.html'))
        for i in range(0, len(self.bcInfoList)):
            row = self.ui.tableWidget_bc_ASMI.rowCount()
            self.ui.tableWidget_bc_ASMI.insertRow(row)
            item = QTableWidgetItem(str(self.bcInfoList[i].getbcName()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 0, item)
            # item = QTableWidgetItem(str("%.4f" % self.bcInfoList[i].getnorBCPortNum()))
            item = QTableWidgetItem(str(self.bcInfoList[i].getfcNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 1, item)
            # item = QTableWidgetItem(str("%.4f" % self.bcInfoList[i].getnorBCInterfaceNum()))
            item = QTableWidgetItem(str(self.bcInfoList[i].getportNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 2, item)
            # item = QTableWidgetItem(str("%.4f" % self.bcInfoList[i].getnorBCNoUseInterface()))
            item = QTableWidgetItem(str(self.bcInfoList[i].getinterfaceNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 3, item)
            # item = QTableWidgetItem(str("%.4f" % self.bcInfoList[i].getnorBCIntraCoupling()))
            item = QTableWidgetItem(str(self.bcInfoList[i].getrunnableNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 4, item)
            # item = QTableWidgetItem(str("%.4f" % self.bcInfoList[i].getnorBCExtraCoupling()))
            item = QTableWidgetItem(str(self.bcInfoList[i].getnouseInterfaceNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 5, item)
            item = QTableWidgetItem(str(self.bcInfoList[i].getintralInNum() + self.bcInfoList[i].getintralOutNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 6, item)
            # item = QTableWidgetItem(str("%.4f" % self.bcInfoList[i].getnorBCExtraDependCoupling()))
            item = QTableWidgetItem(str(self.bcInfoList[i].getextralInNum() + self.bcInfoList[i].getextralOutNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 7, item)
            item = QTableWidgetItem(str(self.bcInfoList[i].getextralDependNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 8, item)
            item = QTableWidgetItem(str("%.2f" % self.bcInfoList[i].getaveFuncCC()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 9, item)
            item = QTableWidgetItem(str(self.bcInfoList[i].getmaxFuncND()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 10, item)
            item = QTableWidgetItem(str(self.bcInfoList[i].getloc()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 11, item)
            #item = QTableWidgetItem(str("%.2f" % self.bcInfoList[i].getbcScore1()))
            item = QTableWidgetItem(str("%.2f" % self.bcInfoList[i].getbcScore()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_bc_ASMI.setItem(row, 12, item)
            widget = QWidget()
            if self.bcInfoList[i].getbcScore1() <= -50:
                reviewButton = QPushButton('E')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(255,0,0);color:white;width:30px;height:30px;border-style: outset;border-radius: 10px;''')
            elif -50 < self.bcInfoList[i].getbcScore1() <= 0:
                reviewButton = QPushButton('D')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(255, 192, 0);width:30px;height:30px;color:white;border-style: outset;border-radius: 10px;''')
            elif 0 < self.bcInfoList[i].getbcScore1() <= 50:
                reviewButton = QPushButton('C')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(165, 165, 165);color:white;width:30px;height:30px;border-style: outset;border-radius: 10px;''')
            elif 50 < self.bcInfoList[i].getbcScore1() <= 80:
                reviewButton = QPushButton('B')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(0, 112, 192);color:white;width:30px;height:30px;border-style: outset;border-radius: 10px;''')
            elif 80 < self.bcInfoList[i].getbcScore1():
                reviewButton = QPushButton('A')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(0, 176, 80);color:white;width:30px;height:30px;border-style: outset;border-radius: 10px;''')
            hLayout = QHBoxLayout()
            hLayout.addWidget(reviewButton)
            hLayout.setContentsMargins(10, 5, 10, 5)
            widget.setLayout(hLayout)
            self.ui.tableWidget_bc_ASMI.setCellWidget(row, 13, widget)

        self.ui.tableWidget_bc_ASMI.resizeColumnsToContents()
        self.ui.tableWidget_bc_ASMI.sortItems(0, Qt.AscendingOrder)

    def fileInfo(self, filepath):
        filelist = []
        calllist = []
        headerlist = []
        if (filepath == ""):
            QMessageBox.critical(self, "Error", "Import path is empty")
        else:
            filepath = filepath.replace('/', '\\')
            # bclist = ComplexityAnalyse.getAllBC(filepath)
            self.fcList = []
            self.bcList = []
            fileCounter = LineCounter()
            file_list = fileCounter.get_filelist(filepath, [])
            for rowNum in range(0, self.ui.tableWidget_BC_arxml.rowCount())[::-1]:
                self.ui.tableWidget_BC_arxml.removeRow(rowNum)
            self.ui.tableWidget_BC_arxml.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_FC_arxml.rowCount())[::-1]:
                self.ui.tableWidget_FC_arxml.removeRow(rowNum)
            self.ui.tableWidget_FC_arxml.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_Project.rowCount())[::-1]:
                self.ui.tableWidget_Project.removeRow(rowNum)
            self.ui.tableWidget_Project.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_BC_code.rowCount())[::-1]:
                self.ui.tableWidget_BC_code.removeRow(rowNum)
            self.ui.tableWidget_BC_code.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_FC_code.rowCount())[::-1]:
                self.ui.tableWidget_FC_code.removeRow(rowNum)
            self.ui.tableWidget_FC_code.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_File.rowCount())[::-1]:
                self.ui.tableWidget_File.removeRow(rowNum)
            self.ui.tableWidget_File.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_Function.rowCount())[::-1]:
                self.ui.tableWidget_Function.removeRow(rowNum)
            self.ui.tableWidget_Function.verticalScrollBar().setValue(0)
            for i in range(9):
                item = QTableWidgetItem(str(''))
                self.ui.tableWidget_fc_report.setItem(i,1,item)
                item = QTableWidgetItem(str(''))
                self.ui.tableWidget_bc_report.setItem(i,1,item)
            self.ui.label_report_bc_conclusion.clear()
            self.ui.label_report_bc_conclusion_size.clear()
            self.ui.label_report_bc_conclusion_coupling.clear()
            self.ui.label_report_bc_conclusion_code.clear()
            self.ui.label_report_bc_advice_code.clear()
            self.ui.label_report_bc_advice_coupling.clear()
            self.ui.label_report_bc_advice_size.clear()
            self.ui.label_report_fc_conclusion.clear()
            self.ui.label_report_fc_conclusion_code.clear()
            self.ui.label_report_fc_conclusion_size.clear()
            self.ui.label_report_fc_conclusion_coupling.clear()
            self.ui.label_report_fc_advice_code.clear()
            self.ui.label_report_fc_advice_size.clear()
            self.ui.label_report_fc_advice_coupling.clear()
            for rowNum in range(0, self.ui.tableWidget_fc_ASMI.rowCount())[::-1]:
                self.ui.tableWidget_fc_ASMI.removeRow(rowNum)
            self.ui.tableWidget_fc_ASMI.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_bc_ASMI.rowCount())[::-1]:
                self.ui.tableWidget_bc_ASMI.removeRow(rowNum)
            self.ui.tableWidget_bc_ASMI.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_nokeyBC_arxml.rowCount())[::-1]:
                self.ui.tableWidget_nokeyBC_arxml.removeRow(rowNum)
            self.ui.tableWidget_nokeyBC_arxml.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_nokeyFC_arxml.rowCount())[::-1]:
                self.ui.tableWidget_nokeyFC_arxml.removeRow(rowNum)
            self.ui.tableWidget_nokeyFC_arxml.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_project_nokey.rowCount())[::-1]:
                self.ui.tableWidget_project_nokey.removeRow(rowNum)
            self.ui.tableWidget_project_nokey.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_Function_nokey.rowCount())[::-1]:
                self.ui.tableWidget_Function_nokey.removeRow(rowNum)
            self.ui.tableWidget_Function_nokey.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_nokeyBC_code.rowCount())[::-1]:
                self.ui.tableWidget_nokeyBC_code.removeRow(rowNum)
            self.ui.tableWidget_nokeyBC_code.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_nokeyFC_code.rowCount())[::-1]:
                self.ui.tableWidget_nokeyFC_code.removeRow(rowNum)
            self.ui.tableWidget_nokeyFC_code.verticalScrollBar().setValue(0)
            for rowNum in range(0, self.ui.tableWidget_File_nokey.rowCount())[::-1]:
                self.ui.tableWidget_File_nokey.removeRow(rowNum)
            self.ui.tableWidget_File_nokey.verticalScrollBar().setValue(0)
            if self.ui.treeWidget_key.currentItem() != None:
                self.ui.treeWidget_key.currentItem().setSelected(False)
            if self.ui.treeWidget_nokey.currentItem() != None:
                self.ui.treeWidget_nokey.currentItem().setSelected(False)
            self.ui.treeWidget_key.invisibleRootItem().child(0).child(0).setSelected(True)
            self.ui.treeWidget_nokey.invisibleRootItem().child(0).child(0).setSelected(True)
            self.ui.stackedWidget_metrics_key.setCurrentIndex(0)
            self.ui.stackedWidget_metrics_nokey.setCurrentIndex(0)
            self.ui.stackedWidget_metrics.setCurrentIndex(0)


            threads = []
            fileCounter.setfilelist(file_list)
            fileCounter.fileAnalyse()
            fileindex = 0
            filefcindex = ''
            max_nested_structures_fileindex = 0
            min_bmi_fileindex = 0

            for file in fileCounter.filelist:
                if os.path.splitext(file.__dict__['filename'])[1] != ".h" and \
                        os.path.splitext(file.__dict__['filename'])[1] != ".hpp":
                    cyclomatic_complexity = 0
                    sum_bmi = 0
                    lizarderror = 0
                    # filerow = fileCounter.filelist.index(file)
                    filename = file.__dict__['filename'].replace('\\', '/')
                    filerow = self.ui.tableWidget_File.rowCount()
                    self.ui.tableWidget_File.insertRow(filerow)
                    item1 = QTableWidgetItem(filename)
                    item1.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 0, item1)
                    item2 = QTableWidgetItem(str(file.__dict__['lines_of_code']))
                    item2.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 2, item2)
                    item3 = QTableWidgetItem(str(file.__dict__['lines_of_effective_code']))
                    item3.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 3, item3)
                    item4 = QTableWidgetItem(str(file.__dict__['lines_of_code_comment']))
                    item4.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 4, item4)
                    commentdensity = round((file.__dict__['lines_of_code_comment'] / (
                                file.__dict__['lines_of_code'] - file.__dict__['lines_of_empty'])) * 100, 2)
                    item5 = QTableWidgetItem(str("%.2f%%" % commentdensity))
                    item5.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 5, item5)
                    if len(file.__dict__['function_list']) > 0:
                        max_nested_structures = file.__dict__['function_list'][0].__dict__['max_nested_structures']
                        min_bmi = 93.06 - 0.11 * file.__dict__['function_list'][0].__dict__['nloc'] - 0.13 * \
                                  file.__dict__['function_list'][0].__dict__[
                                      'max_nested_structures'] - 4.31 * math.log2(
                            file.__dict__['function_list'][0].__dict__['cyclomatic_complexity'])
                    else:
                        max_nested_structures = 0
                        min_bmi = 0
                    for function in file.__dict__['function_list']:
                        if function.__dict__['name'] in datareserved_word or function.__dict__[
                            'name'] in reserved_word:
                            lizarderror += 1
                            continue
                        row = self.ui.tableWidget_Function.rowCount()
                        self.ui.tableWidget_Function.insertRow(row)
                        path = function.__dict__['filename'].replace('\\', '/')
                        function.__dict__['path'] = path
                        fcname = os.path.splitext(path.split('/')[-1])[0]
                        function.__dict__['fcname'] = fcname
                        item1 = QTableWidgetItem(path)
                        item1.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 0, item1)
                        item2 = QTableWidgetItem(function.__dict__['fcname'])
                        item2.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 1, item2)
                        item3 = QTableWidgetItem(function.__dict__['name'])
                        item3.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 2, item3)
                        item4 = QTableWidgetItem(str(function.__dict__['nloc']))
                        item4.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 3, item4)
                        loc = function.__dict__['end_line'] - function.__dict__['start_line'] + 1
                        item5 = QTableWidgetItem(str(loc))
                        item5.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 4, item5)
                        commentline = loc - function.__dict__['nloc']
                        item6 = QTableWidgetItem(str(commentline))
                        item6.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 5, item6)
                        item7 = QTableWidgetItem(str(function.__dict__['cyclomatic_complexity']))
                        item7.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 6, item7)
                        item8 = QTableWidgetItem(str(function.__dict__['max_nested_structures']))
                        item8.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 7, item8)
                        bmi = 93.06 - 0.11 * function.__dict__['nloc'] - 0.13 * function.__dict__[
                            'max_nested_structures'] - 4.31 * math.log2(function.__dict__['cyclomatic_complexity'])
                        function.__dict__['bmi'] = bmi
                        item9 = QTableWidgetItem(str("%.2f" % bmi))
                        item9.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 8, item9)
                        item10 = QTableWidgetItem(str(function.__dict__['start_line']))
                        item10.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 9, item10)
                        item11 = QTableWidgetItem(str(function.__dict__['end_line']))
                        item11.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 10, item11)
                        normalized_complexity = function.__dict__['cyclomatic_complexity'] / function.__dict__[
                            'nloc']
                        item = QTableWidgetItem(str("%.2f" % normalized_complexity))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 11, item)
                        comment_density = commentline / loc
                        item = QTableWidgetItem(str("%.2f" % comment_density))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 12, item)
                        item = QTableWidgetItem(str(len(function.__dict__['full_parameters'])))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 13, item)
                        caller_count = file.__dict__['call_list'].count(function.__dict__['name'])
                        function.__dict__['caller_count'] = caller_count
                        if function.__dict__['staticindex'] == 1:
                            item = QTableWidgetItem(str(caller_count))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.ui.tableWidget_Function.setItem(row, 14, item)
                        else:
                            for call in fileCounter.calllist:
                                if function.__dict__['name'] in call and file.__dict__['filename'].replace("\\",
                                                                                                           "/") in \
                                        fileCounter.headerlist[fileCounter.calllist.index(call)]:
                                    caller_count = call.count(function.__dict__['name'])
                                    function.__dict__['caller_count'] += caller_count
                            item = QTableWidgetItem(str(function.__dict__['caller_count']))
                            item.setTextAlignment(Qt.AlignCenter)
                            self.ui.tableWidget_Function.setItem(row, 14, item)

                        item = QTableWidgetItem(str(function.__dict__['sum_call']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function.setItem(row, 15, item)
                        cyclomatic_complexity += function.__dict__['cyclomatic_complexity']
                        sum_bmi += bmi
                        if function.__dict__['max_nested_structures'] >= max_nested_structures:
                            max_nested_structures = function.__dict__['max_nested_structures']
                        if bmi <= min_bmi:
                            min_bmi = bmi

                        row1 = self.ui.tableWidget_Function_nokey.rowCount()
                        self.ui.tableWidget_Function_nokey.insertRow(row1)
                        item = QTableWidgetItem(path)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 0, item)
                        item = QTableWidgetItem(function.__dict__['fcname'])
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 1, item)
                        item = QTableWidgetItem(function.__dict__['name'])
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 2, item)
                        item = QTableWidgetItem(str(function.__dict__['token_count']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 3, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_if']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 4, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_equal']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 5, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_for']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 6, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_while']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 7, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_goto']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 8, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_catch']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 9, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_break']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 10, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_continue']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 11, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_return']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 12, item)
                        sum_non_structured_statement = function.__dict__['sum_goto'] + function.__dict__[
                            'sum_break'] + function.__dict__['sum_continue']
                        item = QTableWidgetItem(str(sum_non_structured_statement))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 13, item)
                        sum_violations = sum_non_structured_statement + function.__dict__[
                            'sum_return']
                        item = QTableWidgetItem(str(sum_violations))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 14, item)
                        reservedwords = dict(Counter(function.__dict__['reservedwords']))
                        calls = dict(Counter(function.__dict__['calls']))
                        operatores = dict(
                            Counter(function.__dict__['operatores']))
                        variables = dict(Counter(function.__dict__['variables']))
                        constants = dict(Counter(function.__dict__['constants']))
                        function.__dict__['sum_variables'] = len(function.__dict__['variables'])
                        function.__dict__['sum_opratores'] = function.__dict__['sum_reservedword'] + \
                                                             function.__dict__['sum_call'] + function.__dict__[
                                                                 'sum_operator']
                        function.__dict__['sum_oprands'] = function.__dict__['sum_variables'] + function.__dict__[
                            'sum_constant']
                        function.__dict__['sum_different_opratores'] = len(reservedwords) + len(calls) + len(
                            operatores)
                        function.__dict__['sum_different_oprands'] = len(variables) + len(constants)
                        n1 = function.__dict__['sum_different_opratores']
                        N1 = function.__dict__['sum_opratores']
                        n2 = function.__dict__['sum_different_oprands']
                        N2 = function.__dict__['sum_oprands']
                        item = QTableWidgetItem(str(function.__dict__['sum_opratores']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 15, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_oprands']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 16, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_different_opratores']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 17, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_different_oprands']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 18, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_statement']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 19, item)
                        length_vocabulary = n1 + n2
                        length_program = N1 + N2
                        if length_vocabulary != 0:
                            if n1 == 0:
                                calculated_length_program = n2 * math.log2(n2)
                            elif n2 == 0:
                                calculated_length_program = n1 * math.log2(n1)
                            else:
                                calculated_length_program = n1 * math.log2(n1) + n2 * math.log2(n2)
                            program_volume = length_program * math.log2(length_vocabulary)
                        else:
                            calculated_length_program = 0
                            program_volume = 0
                        if n1 != 0 and N2 != 0:
                            program_level = (2 * n2) / (n1 * N2)
                        else:
                            program_level = 0
                        if program_level != 0:
                            program_difficulty = 1 / program_level
                        else:
                            program_difficulty = 0

                        program_effort = program_volume * program_difficulty
                        language_level = program_level * program_level * program_volume
                        program_time = program_effort / (3600 * 18)
                        if function.__dict__['sum_statement'] != 0:
                            average_statement_size = length_program / function.__dict__['sum_statement']
                        else:
                            average_statement_size = 0
                        calculated_num_program_error = program_volume / 3000
                        if length_vocabulary != 0:
                            frequency_vocabulary = length_program / length_vocabulary
                        else:
                            frequency_vocabulary = 0
                        item = QTableWidgetItem(str(length_vocabulary))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 20, item)
                        item = QTableWidgetItem(str(length_program))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 21, item)
                        item = QTableWidgetItem(str("%.4f" % calculated_length_program))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 22, item)
                        item = QTableWidgetItem(str("%.4f" % program_volume))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 23, item)
                        item = QTableWidgetItem(str("%.4f" % program_level))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 24, item)
                        item = QTableWidgetItem(str("%.4f" % program_difficulty))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 25, item)
                        item = QTableWidgetItem(str("%.4f" % program_effort))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 26, item)
                        item = QTableWidgetItem(str("%.4f" % language_level))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 27, item)
                        item = QTableWidgetItem(str("%.4f" % program_time))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 28, item)
                        item = QTableWidgetItem(str("%.4f" % average_statement_size))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 29, item)
                        item = QTableWidgetItem(str("%.4f" % calculated_num_program_error))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 30, item)
                        item = QTableWidgetItem(str("%.4f" % frequency_vocabulary))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 31, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_statement']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 32, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_branch']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 33, item)
                        if function.__dict__['sum_statement'] == 0:
                            percent_branches = 0
                        else:
                            percent_branches = function.__dict__['sum_branch'] / function.__dict__['sum_statement']
                        item = QTableWidgetItem(str("%.4f" % percent_branches))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 34, item)
                        for i in function.__dict__['full_parameters']:
                            if re.search(r'\s', i):
                                function.__dict__['sum_localvariable'] += 1

                        item = QTableWidgetItem(str(function.__dict__['sum_localvariable']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 35, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_staticvariable']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 36, item)
                        item = QTableWidgetItem(
                            str(function.__dict__['sum_localvariable'] - function.__dict__['sum_staticvariable']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 37, item)
                        recursion = function.__dict__['calls'].count(function.__dict__['name'])
                        item = QTableWidgetItem(str(recursion))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 38, item)
                        item = QTableWidgetItem(str(function.__dict__['sum_if'] - function.__dict__['sum_else']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 39, item)
                        item = QTableWidgetItem(str(function.__dict__['stacksize']))
                        item.setTextAlignment(Qt.AlignCenter)
                        self.ui.tableWidget_Function_nokey.setItem(row1, 40, item)

                    functionnum = len(file.__dict__['function_list']) - lizarderror
                    file.__dict__['functionNum'] = functionnum
                    item = QTableWidgetItem(str(functionnum))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 1, item)
                    if functionnum == 0:
                        ave_cyclomatic_complexity = 0
                        ave_bmi = 0
                    else:
                        ave_cyclomatic_complexity = cyclomatic_complexity / functionnum
                        ave_bmi = sum_bmi / functionnum
                    file.__dict__['sum_cyclomatic_complexity'] = cyclomatic_complexity
                    file.__dict__['ave_cyclomatic_complexity'] = ave_cyclomatic_complexity
                    file.__dict__['max_nested_structures'] = max_nested_structures
                    file.__dict__['min_bmi'] = min_bmi
                    file.__dict__['ave_bmi'] = ave_bmi
                    item = QTableWidgetItem(str(cyclomatic_complexity))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 6, item)
                    item = QTableWidgetItem(str(ave_cyclomatic_complexity))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 7, item)
                    item = QTableWidgetItem(str(max_nested_structures))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 8, item)
                    item = QTableWidgetItem(str("%.2f" % min_bmi))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 9, item)
                    item = QTableWidgetItem(str("%.2f" % ave_bmi))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File.setItem(filerow, 10, item)

                    filerownokey = self.ui.tableWidget_File_nokey.rowCount()
                    self.ui.tableWidget_File_nokey.insertRow(filerownokey)
                    filepath = file.__dict__['filename'].replace('\\', '/')
                    item = QTableWidgetItem(str(filepath))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 0, item)
                    item = QTableWidgetItem(str(file.__dict__['statement_count']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 1, item)
                    item = QTableWidgetItem(str(file.__dict__['branch_count']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 2, item)
                    if file.__dict__['statement_count'] == 0:
                        file_percent_branches = 0
                    else:
                        file_percent_branches = file.__dict__['branch_count'] / file.__dict__['statement_count']
                    item = QTableWidgetItem(str("%.4f" % file_percent_branches))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 3, item)
                    if functionnum == 0:
                        ave_statement_perfunction = 0
                    else:
                        ave_statement_perfunction = file.__dict__['statement_count'] / functionnum
                    item = QTableWidgetItem(str("%.4f" % ave_statement_perfunction))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 4, item)
                    item = QTableWidgetItem(str(file.__dict__['token_count']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 5, item)
                    item = QTableWidgetItem(str(file.__dict__['global_count']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 6, item)
                    item = QTableWidgetItem(str(file.__dict__['static_count']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 7, item)
                    item = QTableWidgetItem(str(file.__dict__['global_count'] - file.__dict__['static_count']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 8, item)
                    item = QTableWidgetItem(str(file.__dict__['calls_count']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 9, item)
                    item = QTableWidgetItem(str(file.__dict__['recursion_count']))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 10, item)
                    if file.__dict__['recursion_count'] == 0:
                        percent_recursion = 0
                    else:
                        percent_recursion = file.__dict__['recursion_count'] / file.__dict__['calls_count']
                    if percent_recursion == 0:
                        item = QTableWidgetItem(str(percent_recursion))
                    else:
                        item = QTableWidgetItem(str("%.4f" % percent_recursion))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.ui.tableWidget_File_nokey.setItem(filerownokey, 11, item)

                    if file.__dict__['statement_count'] == 0:
                        file_percent_branches = 0
                    else:
                        file_percent_branches = file.__dict__['branch_count'] / file.__dict__['statement_count']

                    file_fc = filename.split('/')[-2]
                    file_bc = filename.split('/')[-3]
                    if len(self.fcList) == 0:
                        self.fcList.append(
                            {'fcname': file_fc, 'path': filename.rsplit('/', 1)[0], 'file_list': [file],
                             'function_num': functionnum, 'bcname': file_bc,
                             'lines_of_code': file.__dict__['lines_of_code'],
                             'sum_cyclomatic_complexity': cyclomatic_complexity,
                             'max_nested_structures': max_nested_structures, 'min_bmi': min_bmi, 'sum_bmi': sum_bmi,
                             'lines_of_effective_code': file.__dict__['lines_of_effective_code'],
                             'num_of_statement': file.__dict__['statement_count'],
                             'num_of_branch': file.__dict__['branch_count'],
                             'num_of_token': file.__dict__['token_count'],
                             'num_of_globalvariable': file.__dict__['global_count'],
                             'num_of_staticvariable': file.__dict__['static_count'],
                             'num_of_nonstaticvariable': file.__dict__['global_count'] - file.__dict__[
                                 'static_count'],
                             'num_of_calls': file.__dict__['calls_count'],
                             'num_of_recusion': file.__dict__['recursion_count']})
                        max_nested_structures_fileindex = max_nested_structures
                        min_bmi_fileindex = min_bmi
                    elif filename.rsplit('/', 1)[0] == filefcindex:
                        self.fcList[len(self.fcList) - 1]['file_list'].append(file)
                        self.fcList[len(self.fcList) - 1]['function_num'] += functionnum
                        self.fcList[len(self.fcList) - 1]['lines_of_code'] += file.__dict__['lines_of_code']
                        self.fcList[len(self.fcList) - 1]['sum_cyclomatic_complexity'] += cyclomatic_complexity
                        self.fcList[len(self.fcList) - 1]['sum_bmi'] += sum_bmi
                        self.fcList[len(self.fcList) - 1]['lines_of_effective_code'] += file.__dict__[
                            'lines_of_effective_code']
                        self.fcList[len(self.fcList) - 1]['num_of_statement'] += file.__dict__['statement_count']
                        self.fcList[len(self.fcList) - 1]['num_of_branch'] += file.__dict__['branch_count']
                        self.fcList[len(self.fcList) - 1]['num_of_token'] += file.__dict__['token_count']
                        self.fcList[len(self.fcList) - 1]['num_of_globalvariable'] += file.__dict__['global_count']
                        self.fcList[len(self.fcList) - 1]['num_of_staticvariable'] += file.__dict__['static_count']
                        self.fcList[len(self.fcList) - 1]['num_of_nonstaticvariable'] += (
                                    file.__dict__['global_count'] - file.__dict__['static_count'])
                        self.fcList[len(self.fcList) - 1]['num_of_calls'] += file.__dict__['calls_count']
                        self.fcList[len(self.fcList) - 1]['num_of_recusion'] += file.__dict__['recursion_count']
                        if max_nested_structures >= max_nested_structures_fileindex:
                            max_nested_structures_fileindex = max_nested_structures
                            self.fcList[len(self.fcList) - 1]['max_nested_structures'] = max_nested_structures
                        if min_bmi <= min_bmi_fileindex:
                            min_bmi_fileindex = min_bmi
                            self.fcList[len(self.fcList) - 1]['min_bmi'] = min_bmi

                    else:
                        self.fcList.append(
                            {'fcname': file_fc, 'path': filename.rsplit('/', 1)[0], 'file_list': [file],
                             'function_num': functionnum, 'bcname': file_bc,
                             'lines_of_code': file.__dict__['lines_of_code'],
                             'sum_cyclomatic_complexity': cyclomatic_complexity,
                             'max_nested_structures': max_nested_structures, 'min_bmi': min_bmi, 'sum_bmi': sum_bmi,
                             'lines_of_effective_code': file.__dict__['lines_of_effective_code'],
                             'num_of_statement': file.__dict__['statement_count'],
                             'num_of_branch': file.__dict__['branch_count'],
                             'num_of_token': file.__dict__['token_count'],
                             'num_of_globalvariable': file.__dict__['global_count'],
                             'num_of_staticvariable': file.__dict__['static_count'],
                             'num_of_nonstaticvariable': file.__dict__['global_count'] - file.__dict__[
                                 'static_count'],
                             'num_of_calls': file.__dict__['calls_count'],
                             'num_of_recusion': file.__dict__['recursion_count']})
                        max_nested_structures_fileindex = max_nested_structures
                        min_bmi_fileindex = min_bmi
                    filefcindex = filename.rsplit('/', 1)[0]

            funcindex = 0

            max_nested_structures_fcindex = 0
            min_bmi_fcindex = 0
            for fc in self.fcList:
                fc_bc = fc['path'].split('/')[-2]
                row = self.ui.tableWidget_FC_code.rowCount()
                self.ui.tableWidget_FC_code.insertRow(row)
                item = QTableWidgetItem(fc['path'])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 0, item)
                item = QTableWidgetItem(fc['bcname'])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 1, item)
                item = QTableWidgetItem(fc['fcname'])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 2, item)
                item = QTableWidgetItem(str(fc['function_num']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 3, item)
                item = QTableWidgetItem(str(fc['lines_of_code']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 4, item)
                item = QTableWidgetItem(str(len(fc['file_list'])))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 5, item)
                if fc['function_num'] == 0:
                    fc['ave_cyclomatic_complexity'] = 0
                    fc['ave_function_complexity'] = 0
                    fc['ave_bmi'] = 0
                else:
                    fc['ave_cyclomatic_complexity'] = fc['sum_cyclomatic_complexity'] / fc['function_num']
                    fc['ave_function_complexity'] = fc['lines_of_effective_code'] / fc['function_num']
                    fc['ave_bmi'] = fc['sum_bmi'] / fc['function_num']
                item = QTableWidgetItem(str("%.2f" % fc['ave_cyclomatic_complexity']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 6, item)
                item = QTableWidgetItem(str(fc['max_nested_structures']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 7, item)
                item = QTableWidgetItem(str("%.2f" % fc['min_bmi']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 8, item)
                item = QTableWidgetItem(str("%.2f" % fc['ave_bmi']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 9, item)
                item = QTableWidgetItem(str("%.2f" % fc['ave_function_complexity']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_FC_code.setItem(row, 10, item)

                row = self.ui.tableWidget_nokeyFC_code.rowCount()
                self.ui.tableWidget_nokeyFC_code.insertRow(row)
                item = QTableWidgetItem(fc['path'])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 0, item)
                item = QTableWidgetItem(fc['bcname'])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 1, item)
                item = QTableWidgetItem(fc['fcname'])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 2, item)
                item = QTableWidgetItem(str(fc['num_of_statement']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 3, item)
                item = QTableWidgetItem(str(fc['num_of_branch']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 4, item)
                item = QTableWidgetItem(str(fc['num_of_token']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 5, item)
                item = QTableWidgetItem(str(fc['num_of_globalvariable']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 6, item)
                item = QTableWidgetItem(str(fc['num_of_staticvariable']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 7, item)
                item = QTableWidgetItem(str(fc['num_of_nonstaticvariable']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 8, item)
                item = QTableWidgetItem(str(fc['num_of_calls']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 9, item)
                item = QTableWidgetItem(str(fc['num_of_recusion']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyFC_code.setItem(row, 10, item)
                if len(self.bcList) == 0:
                    self.bcList.append({'path': fc['path'].rsplit('/', 1)[0], 'bcname': fc_bc, 'fc_list': [fc],
                                        'function_num': fc['function_num'], 'lines_of_code': fc['lines_of_code'],
                                        'sum_cyclomatic_complexity': fc['sum_cyclomatic_complexity'],
                                        'max_nested_structures': fc['max_nested_structures'],
                                        'sum_bmi': fc['sum_bmi'], 'min_bmi': fc['min_bmi'],
                                        'lines_of_effective_code': fc['lines_of_effective_code'],
                                        'num_of_statement': fc['num_of_statement'],
                                        'num_of_branch': fc['num_of_branch'], 'num_of_token': fc['num_of_token'],
                                        'num_of_globalvariable': fc['num_of_globalvariable'],
                                        'num_of_staticvariable': fc['num_of_staticvariable'],
                                        'num_of_nonstaticvariable': fc['num_of_nonstaticvariable'],
                                        'num_of_calls': fc['num_of_calls'],
                                        'num_of_recusion': fc['num_of_recusion']})
                    max_nested_structures_fcindex = fc['max_nested_structures']
                    min_bmi_fcindex = fc['min_bmi']
                elif fc['path'].rsplit('/', 1)[0] == fcbcindex:
                    self.bcList[len(self.bcList) - 1]['fc_list'].append(fc)
                    self.bcList[len(self.bcList) - 1]['function_num'] += fc['function_num']
                    self.bcList[len(self.bcList) - 1]['lines_of_code'] += fc['lines_of_code']
                    self.bcList[len(self.bcList) - 1]['sum_cyclomatic_complexity'] += fc[
                        'sum_cyclomatic_complexity']
                    self.bcList[len(self.bcList) - 1]['sum_bmi'] += fc['sum_bmi']
                    self.bcList[len(self.bcList) - 1]['lines_of_effective_code'] += fc['lines_of_effective_code']
                    self.bcList[len(self.bcList) - 1]['num_of_statement'] += fc['num_of_statement']
                    self.bcList[len(self.bcList) - 1]['num_of_branch'] += fc['num_of_branch']
                    self.bcList[len(self.bcList) - 1]['num_of_token'] += fc['num_of_token']
                    self.bcList[len(self.bcList) - 1]['num_of_globalvariable'] += fc['num_of_globalvariable']
                    self.bcList[len(self.bcList) - 1]['num_of_staticvariable'] += fc['num_of_staticvariable']
                    self.bcList[len(self.bcList) - 1]['num_of_nonstaticvariable'] += fc['num_of_nonstaticvariable']
                    self.bcList[len(self.bcList) - 1]['num_of_calls'] += fc['num_of_calls']
                    self.bcList[len(self.bcList) - 1]['num_of_recusion'] += fc['num_of_recusion']
                    if fc['max_nested_structures'] >= max_nested_structures_fcindex:
                        max_nested_structures_fcindex = fc['max_nested_structures']
                        self.bcList[len(self.bcList) - 1]['max_nested_structures'] = fc['max_nested_structures']
                    if fc['min_bmi'] <= min_bmi_fcindex:
                        min_bmi_fcindex = fc['min_bmi']
                        self.bcList[len(self.bcList) - 1]['min_bmi'] = fc['min_bmi']
                else:
                    self.bcList.append({'path': fc['path'].rsplit('/', 1)[0], 'bcname': fc_bc, 'fc_list': [fc],
                                        'function_num': fc['function_num'], 'lines_of_code': fc['lines_of_code'],
                                        'sum_cyclomatic_complexity': fc['sum_cyclomatic_complexity'],
                                        'max_nested_structures': fc['max_nested_structures'],
                                        'sum_bmi': fc['sum_bmi'], 'min_bmi': fc['min_bmi'],
                                        'lines_of_effective_code': fc['lines_of_effective_code'],
                                        'num_of_statement': fc['num_of_statement'],
                                        'num_of_branch': fc['num_of_branch'], 'num_of_token': fc['num_of_token'],
                                        'num_of_globalvariable': fc['num_of_globalvariable'],
                                        'num_of_staticvariable': fc['num_of_staticvariable'],
                                        'num_of_nonstaticvariable': fc['num_of_nonstaticvariable'],
                                        'num_of_calls': fc['num_of_calls'],
                                        'num_of_recusion': fc['num_of_recusion']})
                    max_nested_structures_fcindex = fc['max_nested_structures']
                    min_bmi_fcindex = fc['min_bmi']
                fcbcindex = fc['path'].rsplit('/', 1)[0]
            self.project = {}
            max_nested_structures_bcindex = 0
            min_bmi_bcindex = 0
            for bc in self.bcList:
                row = self.ui.tableWidget_BC_code.rowCount()
                self.ui.tableWidget_BC_code.insertRow(row)
                item = QTableWidgetItem(bc['path'])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 0, item)
                item = QTableWidgetItem(bc['bcname'])
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 1, item)
                item = QTableWidgetItem(str(bc['function_num']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 2, item)
                item = QTableWidgetItem(str(bc['lines_of_code']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 3, item)
                item = QTableWidgetItem(str(len(bc['fc_list'])))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 4, item)
                if bc['function_num'] == 0:
                    bc['ave_cyclomatic_complexity'] = 0
                    bc['ave_function_complexity'] = 0
                    bc['ave_bmi'] = 0
                else:
                    bc['ave_cyclomatic_complexity'] = bc['sum_cyclomatic_complexity'] / bc['function_num']
                    bc['ave_function_complexity'] = bc['lines_of_effective_code'] / bc['function_num']
                    bc['ave_bmi'] = bc['sum_bmi'] / bc['function_num']
                item = QTableWidgetItem(str("%.2f" % bc['ave_cyclomatic_complexity']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 5, item)
                item = QTableWidgetItem(str(bc['max_nested_structures']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 6, item)

                item = QTableWidgetItem(str("%.2f" % bc['ave_bmi']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 7, item)
                item = QTableWidgetItem(str("%.2f" % bc['min_bmi']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 8, item)
                item = QTableWidgetItem(str("%.2f" % bc['ave_function_complexity']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_BC_code.setItem(row, 9, item)

                row = self.ui.tableWidget_nokeyBC_code.rowCount()
                self.ui.tableWidget_nokeyBC_code.insertRow(row)
                item = QTableWidgetItem(str(bc['path']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 0, item)
                item = QTableWidgetItem(str(bc['bcname']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 1, item)
                item = QTableWidgetItem(str(bc['num_of_statement']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 2, item)
                item = QTableWidgetItem(str(bc['num_of_branch']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 3, item)
                item = QTableWidgetItem(str(bc['num_of_token']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 4, item)
                item = QTableWidgetItem(str(bc['num_of_globalvariable']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 5, item)
                item = QTableWidgetItem(str(bc['num_of_staticvariable']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 6, item)
                item = QTableWidgetItem(str(bc['num_of_nonstaticvariable']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 7, item)
                item = QTableWidgetItem(str(bc['num_of_calls']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 8, item)
                item = QTableWidgetItem(str(bc['num_of_recusion']))
                item.setTextAlignment(Qt.AlignCenter)
                self.ui.tableWidget_nokeyBC_code.setItem(row, 9, item)

                if len(self.project) == 0:
                    self.project = {'path': bc['path'].rsplit('/', 2)[0], 'projectname': bc['path'].split('/')[-3],
                                    'function_num': bc['function_num'], 'lines_of_code': bc['lines_of_code'],
                                    'bc_num': len(self.bcList), 'fc_num': len(self.fcList),
                                    'sum_cyclomatic_complexity': bc['sum_cyclomatic_complexity'],
                                    'max_nested_structures': bc['max_nested_structures'],
                                    'sum_bmi': bc['sum_bmi'], 'min_bmi': bc['min_bmi'],
                                    'lines_of_effective_code': bc['lines_of_effective_code'],
                                    'num_of_statement': bc['num_of_statement'],
                                    'num_of_branch': bc['num_of_branch'], 'num_of_token': bc['num_of_token'],
                                    'num_of_globalvariable': bc['num_of_globalvariable'],
                                    'num_of_staticvariable': bc['num_of_staticvariable'],
                                    'num_of_nonstaticvariable': bc['num_of_nonstaticvariable'],
                                    'num_of_calls': bc['num_of_calls'], 'num_of_recusion': bc['num_of_recusion']}
                    max_nested_structures_bcindex = bc['max_nested_structures']
                    min_bmi_bcindex = bc['min_bmi']
                else:
                    self.project['function_num'] += bc['function_num']
                    self.project['lines_of_code'] += bc['lines_of_code']
                    self.project['sum_cyclomatic_complexity'] += bc['sum_cyclomatic_complexity']
                    self.project['sum_bmi'] += bc['sum_bmi']
                    self.project['lines_of_effective_code'] += bc['lines_of_effective_code']
                    self.project['num_of_statement'] += bc['num_of_statement']
                    self.project['num_of_branch'] += bc['num_of_branch']
                    self.project['num_of_token'] += bc['num_of_token']
                    self.project['num_of_globalvariable'] += bc['num_of_globalvariable']
                    self.project['num_of_staticvariable'] += bc['num_of_staticvariable']
                    self.project['num_of_nonstaticvariable'] += bc['num_of_nonstaticvariable']
                    self.project['num_of_calls'] += bc['num_of_calls']
                    self.project['num_of_recusion'] += bc['num_of_recusion']
                    if bc['max_nested_structures'] >= max_nested_structures_bcindex:
                        max_nested_structures_bcindex = bc['max_nested_structures']
                        self.project['max_nested_structures'] = max_nested_structures_bcindex
                    if bc['min_bmi'] <= min_bmi_bcindex:
                        min_bmi_bcindex = bc['min_bmi']
                        self.project['min_bmi'] = min_bmi_bcindex
            print(self.project)
            self.ui.tableWidget_Project.insertRow(0)
            item = QTableWidgetItem(self.project['path'])
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 0, item)
            item = QTableWidgetItem(self.project['projectname'])
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 1, item)
            item = QTableWidgetItem(str(self.project['function_num']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 2, item)
            item = QTableWidgetItem(str(self.project['lines_of_code']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 3, item)
            item = QTableWidgetItem(str(self.project['bc_num']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 4, item)
            item = QTableWidgetItem(str(self.project['fc_num']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 5, item)
            if self.project['function_num'] == 0:
                self.project['ave_cyclomatic_complexity'] = 0
                self.project['ave_bmi'] = 0
            else:
                self.project['ave_cyclomatic_complexity'] = self.project['sum_cyclomatic_complexity'] / \
                                                            self.project['function_num']
                self.project['ave_bmi'] = self.project['sum_bmi'] / self.project['function_num']
            item = QTableWidgetItem(str(self.project['ave_cyclomatic_complexity']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 6, item)
            item = QTableWidgetItem(str(self.project['max_nested_structures']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 7, item)
            item = QTableWidgetItem(str("%.2f" % self.project['ave_bmi']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 8, item)
            item = QTableWidgetItem(str("%.2f" % self.project['min_bmi']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_Project.setItem(0, 9, item)
            # project的非关键指标
            self.ui.tableWidget_project_nokey.insertRow(0)
            item = QTableWidgetItem(self.project['path'])
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 0, item)
            item = QTableWidgetItem(self.project['projectname'])
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 1, item)
            item = QTableWidgetItem(str(self.project['lines_of_effective_code']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 2, item)
            item = QTableWidgetItem(str(self.project['num_of_statement']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 3, item)
            item = QTableWidgetItem(str(self.project['num_of_branch']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 4, item)
            item = QTableWidgetItem(str(self.project['num_of_token']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 5, item)
            item = QTableWidgetItem(str(self.project['num_of_globalvariable']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 6, item)
            item = QTableWidgetItem(str(self.project['num_of_staticvariable']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 7, item)
            item = QTableWidgetItem(str(self.project['num_of_nonstaticvariable']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 8, item)
            item = QTableWidgetItem(str(self.project['num_of_calls']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 9, item)
            item = QTableWidgetItem(str(self.project['num_of_recusion']))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_project_nokey.setItem(0, 10, item)

    def selectReport1(self):
        arr = []
        num = self.matrix.getVertexNum()
        for a in range(0, num):
            arr.append([])
        for i in range(0, self.matrix.getVertexNum()):
            for j in range(0, self.matrix.getVertexNum()):
                arr[i].append(self.matrix.getEdgeWeight1(i, j))
        count = self.ui.listWidget_fc_report.count()
        cb_list = [self.ui.listWidget_fc_report.itemWidget(self.ui.listWidget_fc_report.item(i))
                   for i in range(count)]
        chooses = []
        view = []
        for cb in cb_list:
            if cb.isChecked():
                chooses.append(cb.text())
        if (len(chooses) == 0):
            QMessageBox.critical(self, "Error", "Select SWC")
        else:
            for i in self.fcInfoList:
                if chooses[0] == i.getfcName():
                    conclusion = None
                    item1 = QTableWidgetItem(str(i.getintralInNum() + i.getintralOutNum()))
                    item1.setTextAlignment(Qt.AlignCenter)
                    if i.getintralInNum() + i.getintralOutNum() > 30:
                        item1.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(0, 1, item1)
                    item2 = QTableWidgetItem(str(i.getextralInNum() + i.getextralOutNum()))
                    item2.setTextAlignment(Qt.AlignCenter)
                    if i.getextralInNum() + i.getextralOutNum() > 20:
                        item2.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(1, 1, item2)
                    item3 = QTableWidgetItem(str(i.getextralDependNum()))
                    item3.setTextAlignment(Qt.AlignCenter)
                    if i.getextralDependNum() > 5:
                        item3.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(2, 1, item3)
                    item4 = QTableWidgetItem(str(i.getrunnableNum()))
                    item4.setTextAlignment(Qt.AlignCenter)
                    if i.getrunnableNum() > 5:
                        item4.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(3, 1, item4)
                    item5 = QTableWidgetItem(str(i.getinterfaceNum()))
                    item5.setTextAlignment(Qt.AlignCenter)
                    if i.getinterfaceNum() > 80:
                        item5.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(4, 1, item5)
                    item6 = QTableWidgetItem(str(i.getnouseInterfaceNum()))
                    item6.setTextAlignment(Qt.AlignCenter)
                    if i.getnouseInterfaceNum() > 10:
                        item6.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(5, 1, item6)
                    item7 = QTableWidgetItem(str(i.getloc()))
                    item7.setTextAlignment(Qt.AlignCenter)
                    if i.getloc() > 1000:
                        item7.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(6, 1, item7)
                    item8 = QTableWidgetItem(str("%.2f" % i.getaveFuncCC()))
                    item8.setTextAlignment(Qt.AlignCenter)
                    if i.getaveFuncCC() > 30:
                        item8.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(7, 1, item8)
                    item9 = QTableWidgetItem(str(i.getmaxFuncND()))
                    item9.setTextAlignment(Qt.AlignCenter)
                    if i.getmaxFuncND() > 5:
                        item9.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_fc_report.setItem(8, 1, item9)
                    self.ui.label_report_fc_conclusion.setText('TMI of '+
                        str(i.getfcName()) + ' is ' +str("%.2f" % i.getfcScore1()) + '.')
                    if i.getintralInNum() + i.getintralOutNum() > 30 or i.getextralInNum() + i.getextralOutNum() > 20 or i.getextralDependNum() > 10:

                        conclusion = 'Among the coupling indexes of '+chooses[0]+', the ones on the high side are:'
                        if i.getintralInNum() + i.getintralOutNum() > 30:
                            conclusion += 'internal coupling of components;'
                        if i.getextralInNum() + i.getextralOutNum() > 20:
                            conclusion += 'external coupling of components;'
                        if i.getextralDependNum() > 10:
                            conclusion += 'interdependent coupling of components;'
                        conclusion += 'High coupling indicates that a component has more interactions with other components. ' \
                                      'At this time, it is necessary to make a specific analysis according to the component function, ' \
                                      'whether the current component is responsible for implementing too many functions, and whether there are unnecessary interactions.'

                        self.ui.label_report_fc_conclusion_coupling.setText(conclusion)
                        self.ui.label_report_fc_advice_coupling.setText(
                            'The specific approach is to analyze the basic information of the software, analyze the dependencies between modules and the dependencies between the underlying components.'
                            'Locate the specific components that lead to too strong coupling between modules, and suggest software designers and developers to reduce the coupling between these components.'
                            'Internal coupling: encapsulating interfaces (e.g., with arrays) External coupling: Due to the coupling of components, from the perspective of reducing the coupling between components.')
                    else:

                        self.ui.label_report_fc_conclusion_coupling.setText('Indexes are normal.')
                        self.ui.label_report_fc_advice_coupling.setText('No.')
                    if i.getinterfaceNum() > 80 or i.getnouseInterfaceNum() > 10:
                        self.ui.label_report_fc_conclusion_size.setText(
                            'Component '+chooses[0] + ' has a high NOIC or NOFIC index, which indicates that the interface size or unused interface size of the component is relatively large.'
                                         'The reasons for the large scale of the interface are as follows: ① the component implements more function points; ② The data dimension passed by the interface of the component is low, and the same type of data is not encapsulated into an array.'
                                         'The reasons for the large scale of unused interfaces are as follows: ① inheriting interfaces from historical versions of components without deleting redundant interfaces; ② Interface definition error, resulting in interface connection failure.')
                        self.ui.label_report_fc_advice_size.setText(
                            '①Split components: the components with larger scale or more files are split, and the parts with stronger cohesion in the components are split out and become a new component.'
                            '②Extract components: The cohesive parts of multiple components are extracted to a new component.'
                            'The core of these two operations is to extract the parts with strong cohesion in the components, so as to improve the component cohesion and reduce the coupling between components.')
                    else:
                        self.ui.label_report_fc_conclusion_size.setText('Indexes are nomal.')
                        self.ui.label_report_fc_advice_size.setText('No.')
                    if i.getloc() > 1000 or i.getmaxFuncND() > 5 or i.getaveFuncCC() > 30.0:

                        conclusion = 'Among the scale indicators of '+chooses[0] + ', the higher ones are:'
                        if i.getaveFuncCC() > 30.0:
                            conclusion += 'the cyclomatic complexity of components is large;'
                        if i.getmaxFuncND() > 5:
                            conclusion += 'the cyclomatic complexity of components is large;'
                        if i.getloc() > 1000:
                            conclusion += 'components with too many lines of code;'
                        conclusion += 'In fact, too much complexity makes components less testable, less analysiable, and less understandable, resulting in lower maintainability and higher maintenance costs.'
                        self.ui.label_report_fc_conclusion_code.setText(conclusion)
                        self.ui.label_report_fc_advice_code.setText(
                            'In order to improve the measurement results of complexity indicators, it is necessary to reduce the complexity of software. The specific approach is to analyze and compare the basic information of the file,'
                            'it locates the files with high complexity, and advises software designers and developers to reduce the complexity of these files.'
                            '①Cyclomatic complexity: There are three types of methods to reduce cyclomatic complexity that engineers can refer to.'
                            '②Depth of nesting: Avoid inappropriate nesting and overly complex logic.'
                            '③Average function complexity: When organizing functions, try to avoid too many lines of code for a function. Refining functions and encapsulating functions can effectively reduce complexity.')
                    else:

                        self.ui.label_report_fc_conclusion_code.setText('Indexes are normal.')
                        self.ui.label_report_fc_advice_code.setText('No.')

    def selectReport2(self):
        count = self.ui.listWidget_bc_report.count()
        cb_list = [self.ui.listWidget_bc_report.itemWidget(self.ui.listWidget_bc_report.item(i))
                   for i in range(count)]
        chooses = []
        view = []
        for cb in cb_list:
            if cb.isChecked():
                chooses.append(cb.text())
        if (len(chooses) == 0):
            QMessageBox.critical(self, "Error", "Select BC")
        else:
            for i in self.bcInfoList:
                if chooses[0] == i.getbcName():
                    conclusion = None
                    item1 = QTableWidgetItem(str(i.gettotalIntraNum()))
                    item1.setTextAlignment(Qt.AlignCenter)
                    if i.gettotalIntraNum() > 200:
                        item1.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(0, 1, item1)
                    item2 = QTableWidgetItem(str(i.gettotalExtraNum()))
                    item2.setTextAlignment(Qt.AlignCenter)
                    if i.gettotalExtraNum() > 120:
                        item2.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(1, 1, item2)
                    item3 = QTableWidgetItem(str(i.getextralDependNum()))
                    item3.setTextAlignment(Qt.AlignCenter)
                    if i.getextralDependNum() > 5:
                        item3.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(2, 1, item3)
                    item4 = QTableWidgetItem(str(i.getrunnableNum()))
                    item4.setTextAlignment(Qt.AlignCenter)
                    if i.getrunnableNum() > 20:
                        item4.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(3, 1, item4)
                    item5 = QTableWidgetItem(str(i.getinterfaceNum()))
                    item5.setTextAlignment(Qt.AlignCenter)
                    if i.getinterfaceNum() > 600:
                        item5.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(4, 1, item5)
                    item6 = QTableWidgetItem(str(i.getnouseInterfaceNum()))
                    item6.setTextAlignment(Qt.AlignCenter)
                    if i.getnouseInterfaceNum() > 50:
                        item6.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(5, 1, item6)
                    item7 = QTableWidgetItem(str(i.getloc()))
                    item7.setTextAlignment(Qt.AlignCenter)
                    if i.getloc() > 8000:
                        item7.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(6, 1, item7)
                    item8 = QTableWidgetItem(str("%.2f" % i.getaveFuncCC()))
                    item8.setTextAlignment(Qt.AlignCenter)
                    if i.getaveFuncCC() > 30:
                        item8.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(7, 1, item8)
                    item9 = QTableWidgetItem(str(i.getmaxFuncND()))
                    item9.setTextAlignment(Qt.AlignCenter)
                    if i.getmaxFuncND() > 5:
                        item9.setForeground(QBrush(QColor(255, 0, 0)))
                    self.ui.tableWidget_bc_report.setItem(8, 1, item9)
                    self.ui.label_report_bc_conclusion.setText('TMI of ' +
                                                               str(i.getbcName()) + ' is ' + str(
                        "%.2f" % i.getbcScore1()) + '.')
                    if i.getinterfaceNum() > 600 or i.getnouseInterfaceNum() > 50:
                        self.ui.label_report_bc_conclusion_size.setText(
                            'BC ' + chooses[
                                0] + ' has a high NOIC or NOFIC index, which indicates that the interface size or unused interface size of the BC is relatively large.'
                                     'The reasons for the large scale of the interface are as follows: ① the BC implements more function points; ② The data dimension passed by the interface of the BC is low, and the same type of data is not encapsulated into an array.'
                                     'The reasons for the large scale of unused interfaces are as follows: ① inheriting interfaces from historical versions of BCs without deleting redundant interfaces; ② Interface definition error, resulting in interface connection failure.')
                        self.ui.label_report_bc_advice_size.setText(
                            '①Split: the BCs with larger scale or more files are split, and the parts with stronger cohesion in the BCs are split out and become a new BC.'
                            '②Extract: The cohesive parts of multiple BCs are extracted to a new BC.'
                            'The core of these two operations is to extract the parts with strong cohesion in the BCs, so as to improve the BC cohesion and reduce the coupling between BCs.')

                    else:
                        self.ui.label_report_bc_conclusion_size.setText('Indexes are normal.')
                        self.ui.label_report_bc_advice_size.setText('No.')
                    if i.gettotalIntraNum() > 200 or i.gettotalExtraNum() > 120 or i.getextralDependNum() > 5:
                        conclusion = 'Among the coupling indexes of ' + chooses[0] + ', the ones on the high side are:'
                        if i.gettotalIntraNum() > 200:
                            conclusion += 'internal coupling of BC.'
                        if i.gettotalExtraNum() > 120:
                            conclusion += 'external coupling of BC.'
                        if i.getextralDependNum() > 5:
                            conclusion += 'interdependent coupling of BC.'

                        conclusion += 'High coupling indicates that a BC has more interactions with other BCs. ' \
                                      'At this time, it is necessary to make a specific analysis according to the function, ' \
                                      'whether the current is responsible for implementing too many functions, and whether there are unnecessary interactions.'

                        self.ui.label_report_bc_conclusion_coupling.setText(conclusion)
                        self.ui.label_report_bc_advice_coupling.setText(
                            'The specific approach is to analyze the basic information of the software, analyze the dependencies between modules and the dependencies between the underlying components.'
                            'Locate the specific components that lead to too strong coupling between modules, and suggest software designers and developers to reduce the coupling between these components.'
                            'Internal coupling: encapsulating interfaces (e.g., with arrays) External coupling: Due to the coupling of components, from the perspective of reducing the coupling between components.')
                    else:
                        self.ui.label_report_bc_conclusion_coupling.setText('Indexes are normal.')
                        self.ui.label_report_bc_advice_coupling.setText('No.')
                    if i.getloc() > 8000 or i.getaveFuncCC() > 30.0 or i.getmaxFuncND() > 5:
                        conclusion = 'Among the scale indicators of ' + chooses[0] + ', the higher ones are:'
                        if i.getaveFuncCC() > 30.0:
                            conclusion += 'the cyclomatic complexity of BC is large;'
                        if i.getmaxFuncND() > 5:
                            conclusion += 'the cyclomatic complexity of BC is large;'
                        if i.getloc() > 8000:
                            conclusion += 'BC with too many lines of code;'
                        conclusion += 'In fact, too much complexity makes BCs less testable, less analysiable, and less understandable, resulting in lower maintainability and higher maintenance costs.'
                        self.ui.label_report_bc_conclusion_code.setText(conclusion)
                        self.ui.label_report_bc_advice_code.setText(
                            'In order to improve the measurement results of complexity indicators, it is necessary to reduce the complexity of software. The specific approach is to analyze and compare the basic information of the file,'
                            'it locates the files with high complexity, and advises software designers and developers to reduce the complexity of these files.'
                            '①Cyclomatic complexity: There are three types of methods to reduce cyclomatic complexity that engineers can refer to.'
                            '②Depth of nesting: Avoid inappropriate nesting and overly complex logic.'
                            '③Average function complexity: When organizing functions, try to avoid too many lines of code for a function. Refining functions and encapsulating functions can effectively reduce complexity.')
                    else:
                        self.ui.label_report_bc_conclusion_code.setText('Indexes are normal.')
                        self.ui.label_report_bc_advice_code.setText('No.')

    def calcuFCASMI(self):
        avgFCIntraCoupling = 0
        avgFCExtraCoupling = 0
        avgFCExtraDependCoupling = 0
        avgFCPortNum = 0
        avgFCRunnableNum = 0
        avgFCInterfaceNum = 0
        avgFCNoUseInterface = 0
        avgFCCC = 0
        avgFCMaxND = 0
        avgFCLoc = 0
        avgFCAvgFuncLoc = 0
        for i in self.fcInfoList:
            avgFCPortNum += i.getportNum()
            avgFCRunnableNum += i.getrunnableNum()
            avgFCInterfaceNum += i.getinterfaceNum()
            avgFCNoUseInterface += i.getnouseInterfaceNum()
            avgFCIntraCoupling += i.getintralInNum() + i.getintralOutNum()
            avgFCExtraCoupling += i.getextralInNum() + i.getextralOutNum()
            avgFCExtraDependCoupling += i.getextralDependNum()
            avgFCCC += i.getaveFuncCC()
            avgFCMaxND += i.getmaxFuncND()
            avgFCLoc += i.getloc()
            avgFCAvgFuncLoc += i.getaveFuncLoc()
        if len(self.fcInfoList) > 0:
            avgFCPortNum /= len(self.fcInfoList)
            avgFCRunnableNum /= len(self.fcInfoList)
            avgFCInterfaceNum /= len(self.fcInfoList)
            avgFCNoUseInterface /= len(self.fcInfoList)
            avgFCIntraCoupling /= len(self.fcInfoList)
            avgFCExtraCoupling /= len(self.fcInfoList)
            avgFCExtraDependCoupling /= len(self.fcInfoList)
            avgFCCC /= len(self.fcInfoList)
            avgFCMaxND /= len(self.fcInfoList)
            avgFCLoc /= len(self.fcInfoList)
            avgFCAvgFuncLoc /= len(self.fcInfoList)
        # 求标准差
        sumFCIntraCoupling = 0
        sumFCExtraCoupling = 0
        sumFCExtraDependCoupling = 0
        sumFCPortNum = 0
        sumFCRunnableNum = 0
        sumFCInterfaceNum = 0
        sumFCNoUseInterface = 0
        sumFCCC = 0
        sumFCMaxND = 0
        sumFCLoc = 0
        sumFCAvgFuncLoc = 0

        for i in self.fcInfoList:
            sumFCIntraCoupling += math.pow(i.getintralInNum() + i.getextralOutNum() - avgFCIntraCoupling, 2)
            sumFCExtraCoupling += math.pow(i.getextralInNum() + i.getextralOutNum() - avgFCExtraCoupling, 2)
            sumFCExtraDependCoupling += i.getextralDependNum()
            sumFCPortNum += math.pow(i.getportNum() - avgFCPortNum, 2)
            sumFCRunnableNum += math.pow(i.getrunnableNum() - avgFCRunnableNum, 2)
            sumFCInterfaceNum += math.pow(i.getinterfaceNum() - avgFCInterfaceNum, 2)
            sumFCNoUseInterface += math.pow(i.getnouseInterfaceNum() - avgFCNoUseInterface, 2)
            sumFCCC += math.pow(i.getaveFuncCC() - avgFCCC, 2)
            sumFCMaxND += math.pow(i.getmaxFuncND() - avgFCMaxND, 2)
            sumFCLoc += math.pow(i.getloc() - avgFCLoc, 2)
            sumFCAvgFuncLoc += math.pow(i.getaveFuncLoc() - avgFCAvgFuncLoc, 2)
        if len(self.fcInfoList) > 0:
            sumFCPortNum = math.sqrt(sumFCPortNum / len(self.fcInfoList))
            sumFCRunnableNum = math.sqrt(sumFCRunnableNum / len(self.fcInfoList))
            sumFCInterfaceNum = math.sqrt(sumFCInterfaceNum / len(self.fcInfoList))
            sumFCNoUseInterface = math.sqrt(sumFCNoUseInterface / len(self.fcInfoList))
            sumFCIntraCoupling = math.sqrt(sumFCIntraCoupling / len(self.fcInfoList))
            sumFCExtraCoupling = math.sqrt(sumFCExtraCoupling / len(self.fcInfoList))
            sumFCExtraDependCoupling = math.sqrt(sumFCExtraDependCoupling / len(self.fcInfoList))
            sumFCCC = math.sqrt(sumFCCC / len(self.fcInfoList))
            sumFCMaxND = math.sqrt(sumFCMaxND / len(self.fcInfoList))
            sumFCLoc = math.sqrt(sumFCLoc / len(self.fcInfoList))
            sumFCAvgFuncLoc = math.sqrt(sumFCAvgFuncLoc / len(self.fcInfoList))
        for i in self.fcInfoList:
            try:
                i.setnorFCPortNum((0 - (i.getportNum() - avgFCPortNum)) / sumFCPortNum)
                i.setnorFCRunnableNum((0 - (i.getrunnableNum() - avgFCRunnableNum)) / sumFCRunnableNum)
                i.setnorFCInterfaceNum((0 - (i.getinterfaceNum() - avgFCInterfaceNum)) / sumFCInterfaceNum)
                i.setnorFCNoUseInterface(
                    (0 - (i.getnouseInterfaceNum() - avgFCNoUseInterface)) / sumFCNoUseInterface)
                i.setnorFCIntraCoupling(
                    (0 - (i.getintralInNum() + i.getintralOutNum() - avgFCIntraCoupling)) / sumFCIntraCoupling)
                i.setnorFCExtraCoupling(
                    (0 - (i.getextralInNum() + i.getextralOutNum() - avgFCExtraCoupling)) / sumFCExtraCoupling)
                i.setnorFCExtraDependCoupling(
                    (0 - (i.getextralDependNum() - avgFCExtraDependCoupling)) / sumFCExtraDependCoupling)
                i.setnorFCCC((0 - (i.getaveFuncCC() - avgFCCC)) / sumFCCC)
                i.setnorFCMaxND((0 - (i.getmaxFuncND() - avgFCMaxND)) / sumFCMaxND)
                i.setnorFCLoc((0 - (i.getloc() - avgFCLoc)) / sumFCLoc)
                i.setnorFCAvgFuncLoc((0 - (i.getaveFuncLoc() - avgFCAvgFuncLoc)) / sumFCAvgFuncLoc)
            except IndexError as e:
                print(e)
            fcScore = 0
            fcScore1 = 0
            fcScore = 1 + (
                        i.getnorFCPortNum() * 0.041 + i.getnorFCInterfaceNum() * 0.046 + i.getnorFCNoUseInterface() * 0.08 + i.getnorFCIntraCoupling() * 0.095 + i.getnorFCExtraCoupling() * 0.136
                        + i.getnorFCExtraDependCoupling() * 0.168 + i.getnorFCCC() * 0.176 + i.getnorFCMaxND() * 0.176 + i.getnorFCLoc() * 0.082)
            #fcScore1 = fcScore * 50
            fcScore1 = fcScore
            i.setfcScore(fcScore)
            i.setfcScore1(fcScore1)
        for i in range(0, self.matrix.getVertexNum()):
            row = self.ui.tableWidget_fc_ASMI.rowCount()
            self.ui.tableWidget_fc_ASMI.insertRow(row)

            item = QTableWidgetItem(str(self.fcInfoList[i].getbcName()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 0, item)
            item = QTableWidgetItem(str(self.fcInfoList[i].getfcName()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 1, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCPortNum()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getportNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 2, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCRunnableNum()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getrunnableNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 3, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCInterfaceNum()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getinterfaceNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 4, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCNoUseInterface()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getnouseInterfaceNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 5, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCIntraCoupling()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getintralInNum() + self.fcInfoList[i].getintralOutNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 6, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCExtraCoupling()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getextralInNum() + self.fcInfoList[i].getextralOutNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 7, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCExtraDependCoupling()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getextralDependNum()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 8, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCLoc()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getloc()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 9, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCAvgFuncLoc()))
            item = QTableWidgetItem(str(math.ceil(self.fcInfoList[i].getaveFuncLoc())))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 10, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCCC()))
            item = QTableWidgetItem(str("%.2f" % self.fcInfoList[i].getaveFuncCC()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 11, item)
            # item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getnorFCMaxND()))
            item = QTableWidgetItem(str(self.fcInfoList[i].getmaxFuncND()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 12, item)
            item = QTableWidgetItem(str("%.4f" % self.fcInfoList[i].getfcScore1()))
            item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_fc_ASMI.setItem(row, 13, item)
            widget = QWidget()
            if self.fcInfoList[i].getfcScore1() <= -50:
                reviewButton = QPushButton('E')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(255,0,0);color:white;width:30px;height:30px;border-style: outset;border-radius: 10px;''')
            elif -50 < self.fcInfoList[i].getfcScore1() <= 0:
                reviewButton = QPushButton('D')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(255, 192, 0);width:30px;height:30px;color:white;border-style: outset;border-radius: 10px;''')
            elif 0 < self.fcInfoList[i].getfcScore1() <= 50:
                reviewButton = QPushButton('C')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(165, 165, 165);color:white;width:30px;height:30px;border-style: outset;border-radius: 10px;''')
            elif 50 < self.fcInfoList[i].getfcScore1() <= 80:
                reviewButton = QPushButton('B')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(0, 112, 192);color:white;width:30px;height:30px;border-style: outset;border-radius: 10px;''')
            elif 80 < self.fcInfoList[i].getfcScore1():
                reviewButton = QPushButton('A')
                reviewButton.setDown(True)
                reviewButton.setStyleSheet(
                    '''background-color:rgb(0, 176, 80);color:white;width:30px;height:30px;border-style: outset;border-radius: 10px;''')
            hLayout = QHBoxLayout()
            hLayout.addWidget(reviewButton)
            hLayout.setContentsMargins(10, 5, 10, 5)
            widget.setLayout(hLayout)
            self.ui.tableWidget_fc_ASMI.setCellWidget(row, 14, widget)
        self.ui.tableWidget_fc_ASMI.resizeColumnsToContents()
        self.ui.tableWidget_fc_ASMI.sortItems(0, Qt.AscendingOrder)


def main():
    app = QApplication(sys.argv)
    win = mainUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    multiprocessing.freeze_support()
    if not os.path.exists("Log"):
        os.makedirs("Log")
    main()
