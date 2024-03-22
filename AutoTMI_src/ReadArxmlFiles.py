import os

class ReadArxmlFiles:

    def getAllFiles(self, path, filelist):
        for file in os.listdir(path):
            full_file_path = os.path.join(path, file)
            if os.path.isdir(full_file_path):
                getAllFiles(full_file_path, filelist)
            else:
                if os.path.splitext(full_file_path)[1] == ".arxml":
                    # print(full_file_path)
                    filelist.append(full_file_path)
        return filelist


    def load(self, filename):
        try:
            DOMTree = xml.dom.minidom.parse(filename)
            collection = DOMTree.documentElement
        except:
            print("Error: 没有找到xml文件或读取xml文件失败")
        return collection

    def getSwcName(self):
        swcname = ''
