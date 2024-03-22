from queue import Empty
import sys
import os
from enum import Enum
import time
from unittest.mock import patch
import threading

import lizard
import multiprocessing


class LineCounter:
    def __init__(self):


        self.Line_numbers = 0
        self.Code = 0
        self.total_comment_numbers = 0
        self.Blanks = 0
        self.fileInfo = []
        self.filelist = []
        self.calllist = []
        self.headerlist = []
        self.file_list = []
        self.dircalllist = []
        self.classfunctionlist = []
        self.importlist = []
        self.class_list = []
        self.parentclass_list = []
        self.classfunction_counts = {}
        self.classdatamember_counts = {}

    def setfilelist(self,file_list):
        self.file_list = file_list

    def getfilelist(self):
        return self.file_list

    def get_filelist(self,path, filelist):
        extendList = ['.c', '.h', '.cpp', '.hpp']
        extendList1 = ['.c','.cpp','.java']
        newPath = path

        if os.path.isfile(path) and os.path.splitext(path)[1] in extendList1:
            filelist.append(path)
        elif os.path.isdir(path):
            for s in os.listdir(path):
                newPath = os.path.join(path, s)
                self.get_filelist(newPath, filelist)

        return filelist
    '''def get_filelist(self,path, Filelist, filelist):
        extendList = ['.c', '.h', '.cpp', '.hpp']
        extendList1 = ['.c','.cpp']
        newPath = path
        if os.path.isfile(path) and os.path.splitext(path)[1] == ".h":
            filelist.append(path)
        if os.path.isfile(path) and os.path.splitext(path)[1] in extendList1:
            Filelist.append(path)
        elif os.path.isdir(path):
            for s in os.listdir(path):
                newPath = os.path.join(path, s)
                self.get_filelist(newPath, Filelist, filelist)

        return Filelist,filelist'''

    def fileAnalyse(self):
        cpu_count = multiprocessing.cpu_count()
        p = multiprocessing.Pool(cpu_count)
        result = p.imap(CodeCounter, self.getfilelist())
        lastfile = None
        result_list = list(result)
        for fileinfo in result_list:
            self.filelist.append(fileinfo)
            self.calllist.append(fileinfo.__dict__['call_list'])
            if lastfile != None:
                if os.path.dirname(fileinfo.__dict__['filename'].replace('\\','/')) != os.path.dirname(lastfile):
                    self.dircalllist.append([os.path.dirname(fileinfo.__dict__['filename'].replace('\\','/'))])
            else:
                self.dircalllist.append([os.path.dirname(fileinfo.__dict__['filename'].replace('\\', '/'))])
            self.dircalllist[len(self.dircalllist) - 1].append(fileinfo.__dict__['call_list'])
            self.headerlist.append(fileinfo.__dict__['header_list'])
            self.importlist.append(fileinfo.__dict__["import_list"])


            lastfile = fileinfo.__dict__['filename'].replace('\\','/')

            for classinfo in fileinfo.__dict__["class_list"]:
                found_match = False
                found_match1 = False
                if classinfo[2] != "":
                    for classinfo1 in fileinfo.__dict__["class_list"]:
                        if classinfo[0] != classinfo1[0] and fileinfo.__dict__["packagename"]+"."+classinfo[2] == classinfo1[0]:
                            classinfo[2] = fileinfo.__dict__["packagename"]+"."+classinfo[2]
                            found_match = True
                            break
                    if found_match == False:
                        '''if classinfo[0] != classinfo1[0] and classinfo[2] == classinfo1[0]:
                            classinfo[2] = fileinfo.__dict__["packagename"]+"."+classinfo1[0]'''

                        for file1 in result_list:
                            if fileinfo.__dict__["packagename"] == file1.__dict__["packagename"] and fileinfo.__dict__["filename"] != file1.__dict__["filename"]:
                                for samepackageclass in file1.__dict__["class_list"]:
                                    if fileinfo.__dict__["packagename"]+"."+classinfo[2] == samepackageclass[0]:
                                        classinfo[2] = file1.__dict__["packagename"] + "." + classinfo[2]
                                        found_match1 = True  # 设置标志变量为 True
                                        break

                            elif fileinfo.__dict__["packagename"] != file1.__dict__["packagename"] and (file1.__dict__["packagename"] + '.' + os.path.basename(file1.__dict__["filename"].split(".")[0])) in fileinfo.__dict__["import_list"]:
                                for samepackageclass in file1.__dict__["class_list"]:
                                    if classinfo[2] == samepackageclass[0].split('.')[-1]:
                                        classinfo[2] = file1.__dict__["packagename"] + "." + classinfo[2]
                                        found_match1 = True
                                        break
                            if found_match1:
                                break
                            else:
                                continue
                #classinfo[0] = fileinfo.__dict__['packagename'] +"."+classinfo[0]
                self.parentclass_list.append(classinfo[2])
                self.class_list.append(classinfo)
            for function in fileinfo.__dict__["function_list"]:
                for classfunction1 in function.__dict__["classfunction"]:
                    if classfunction1[0] == "super":
                        for classrelation in fileinfo.__dict__["class_list"]:
                            if fileinfo.__dict__['packagename'] + "." + function.__dict__['name'].split("::")[-2] == classrelation[0] and classrelation[2] != "":
                                classfunction1[0] = classrelation[2]
                                fileinfo.__dict__["classfunction_list"].append(classfunction1)
                    elif classfunction1[0] == "this":
                        classfunction1[0] = fileinfo.__dict__['packagename'] + "." + function.__dict__['name'].split("::")[-2]
                        fileinfo.__dict__["classfunction_list"].append(classfunction1)
                if "::" in function.__dict__['name']:
                    if fileinfo.__dict__['packagename'] + "." + function.__dict__['name'].split("::")[-2] in self.classfunction_counts:
                        self.classfunction_counts[fileinfo.__dict__['packagename'] + "." + function.__dict__['name'].split("::")[-2]] += 1
                    else:
                        self.classfunction_counts[fileinfo.__dict__['packagename'] + "." + function.__dict__['name'].split("::")[-2]] = 1
            for classinfo in fileinfo.__dict__["class_list"]:
                if classinfo[0] in self.classfunction_counts:
                    classinfo[1] += self.classfunction_counts[classinfo[0]]
                self.classdatamember_counts[classinfo[0]] = classinfo[1]
            for classfunction in fileinfo.__dict__["classfunction_list"]:
                for classobject in fileinfo.__dict__["classobject_list"]:
                    if classfunction[0] == classobject[0]:
                        classfunction[0] = classobject[1]
                '''for sonclass in fileinfo.__dict__["class_list"]:
                    if classfunction[0] == sonclass[0]:
                        classfunction[0] = classfunction[2] + "." + classfunction[0]'''
            self.classfunctionlist.append(fileinfo.__dict__["classfunction_list"])
        print(self.classfunction_counts)
        p.close()
        p.join()

def CodeCounter(filename):
    #lineCounter = LineCounter()
    codes_numbers = 0
    empty = 0
    comment_numbers = 0
    fileinfo = lizard.analyze_file(filename)
    fp = open(filename, encoding='gbk', errors='ignore')
    lines = fp.readlines()

    row_cur_status = Status.Common
    temp = ""

    for line in lines:
        line = temp + line
        line = line.strip("\r\t ")
        if line[-1] == "\\":
            temp += line[:-1]
            continue
        else:
            temp = ""

        lineLen = len(line)

        if lineLen == 1 and line == '\n':
            empty += 1
            continue

        skipStep = 0
        is_effective_code = False

        for i in range(lineLen):

            if skipStep != 0:
                skipStep -= 1
                continue

            if row_cur_status == Status.Common:
                # 普通状态下

                if line[i] == '"' or line[i] == "'":
                    row_cur_status = Status.CharString
                    CharStringStart = line[i]
                    continue


                if i + 1 < lineLen and line[i:i + 2] == '//':
                    row_cur_status = Status.LineComment
                    skipStep = 1
                    continue


                if i + 1 < lineLen and line[i:i + 2] == '/*':
                    row_cur_status = Status.BlockComments
                    skipStep = 1
                    continue

                if line[i] == '\n':
                    continue
                if line[i] == ' ':
                    continue
                else:
                    is_effective_code = True
                    continue

            elif row_cur_status == Status.CharString:

                if line[i] == CharStringStart:
                    row_cur_status = Status.Common
                    is_effective_code = True
                    continue
                else:
                    continue

            elif row_cur_status == Status.BlockComments:

                if i + 1 < lineLen and line[i:i + 2] == '*/':
                    comment_numbers += 1
                    row_cur_status = Status.Common
                    skipStep = 1
                    continue
                else:
                    continue


        if is_effective_code == True:
            codes_numbers += 1


        if row_cur_status in (Status.BlockComments, Status.LineComment):
            comment_numbers += 1


        if row_cur_status != Status.BlockComments:
            row_cur_status = Status.Common

    total = len(lines)

    if (lines[-1][-1] == '\n'):
        total += 1
        empty += 1

    fp.close()



    '''lineCounter.fileInfo.append([filename.replace('\\','/'), total,empty, codes_numbers, comment_numbers])
    LineCounter.Line_numbers += total
    LineCounter.Blanks += empty
    LineCounter.Code += codes_numbers
    LineCounter.total_comment_numbers += comment_numbers'''
    fileinfo.__dict__['lines_of_code'] = total
    fileinfo.__dict__['lines_of_effective_code'] = codes_numbers
    fileinfo.__dict__['lines_of_code_comment'] = comment_numbers
    fileinfo.__dict__['lines_of_empty'] = empty
    '''lineCounter.filelist.append(fileinfo)
    lineCounter.calllist.append(fileinfo.__dict__['call_list'])
    lineCounter.headerlist.append(fileinfo.__dict__['header_list'])'''
    return fileinfo


            # Common
            # CharString
            # LineComment
            # BlockComments
Status = Enum('Status', 'Init Common CharString LineComment BlockComments')

