# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import shutil
import json
import time
import socket
import collections
from judger.tools import tools

DEBUG = 0

decompressPath = "decompressDir"
downloadDir = "downloadDir"

# reload(sys)
# sys.setdefaultencoding("utf-8")

expIdDict = {
    1: "judger/http_server",
    2: "judger/tcp_echo",
    3: "judger/tcp_bulk",
    4: "judger/tcp_loss",
    5: "judger/broadcast",
    6: "judger/switch",
    7: "judger/router",
    8: "judger/ip_lookup",
    9: "judger/mospf",
    11: "judger/nat"
}


def initRetInfo(fileId, expId, userId, filePath):
    retInfo = collections.OrderedDict()
    retInfo["fileId"]      = fileId
    retInfo["expId"]       = expId
    retInfo["userId"]      = userId
    retInfo["filePath"]    = filePath
    retInfo["status"]      = None
    retInfo["statusDescr"] = ""
    retInfo["test"]        = None
    return retInfo


def writeLog(log, extraInfo=""):
    with open("worker.log", "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()))
        f.write(extraInfo)
        f.write(log)
        f.write("\r\n")
 

def main(fileId, expId, userId, filePath):
    tools.removeDir(decompressPath)
    # 初始化要返回的数据
    retInfo = initRetInfo(fileId, expId, userId, filePath)
    # 得出最终要解压的地方
    basename = os.path.basename(filePath)
    
    if expId not in expIdDict.keys():
        tools.removeDir(decompressPath)
        os.remove(basename)
        retInfo["status"] = "200"
        retInfo["statusDescr"] = "请在正确的位置提交作业"
        return retInfo
    
    workDir = expIdDict[expId]

    if not tools.decompress(basename, decompressPath):
        tools.removeDir(decompressPath)
        os.remove(basename)
        retInfo["status"] = "200"
        retInfo["statusDescr"] = "解压失败，请上传正确的文件格式"
        return retInfo

    makefilePath = tools.findMakefilePath(decompressPath)
    
    if not makefilePath:
        tools.removeDir(decompressPath)
        os.remove(basename)
        retInfo["status"] = "200"
        retInfo["statusDescr"] = "没有检测到Makefile"
        return retInfo
 
    shutil.copy(os.path.join(workDir, "Makefile"),makefilePath)

    # get the name of target form Makefile
    targetNameFromMakefile = tools.getTargetName(makefilePath)
    # create the whole path of the targetName
    targetName = os.path.join(makefilePath, targetNameFromMakefile)

    # avoid the students' trick
    if os.path.exists(targetName):
        os.remove(targetName)

    makeResult = tools.compileMakefile(makefilePath)

    if not makeResult or not os.path.exists(targetName):
        tools.removeDir(decompressPath)
        os.remove(basename)
        retInfo["status"] = "200"
        retInfo["statusDescr"] = "编译失败"
        return retInfo
    # 改变权限并且移过去
    shutil.copy2(targetName, workDir)
    # 切换工作目录
    origin_cwd = os.getcwd()
    os.chdir(workDir)
    print(os.getcwd())
    # 执行
    print("sudo python3 -u run.py %s %s" % (origin_cwd, targetNameFromMakefile))
    child = subprocess.Popen("sudo python3 run.py %s %s" % (
        origin_cwd, targetNameFromMakefile), shell=True)
    # child = subprocess.Popen("sudo python3 run.py %s %s" % (
    #     origin_cwd, targetNameFromMakefile), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    child.wait()
    # print("#####")
    # for line in child.stdout.readlines():
    #     print(line)
    # print("#####")
    # 切回工作目录并处理文件
    os.chdir(origin_cwd)
    tools.removeDir(decompressPath)
    os.remove(basename)

    # 读取文件
    try:
        with open("result.json", "r") as f:
            result = f.read()
            if not DEBUG:
                os.remove("result.json")
    except:
        with open("internal_error.json", "r") as f:
            result = f.read()
     
    resultJson = json.loads(result)
    retInfo["status"] = resultJson["status"]
    retInfo["statusDescr"] = resultJson["statusDescr"]

    print("finish")
    return retInfo
 
 
def sendBackToMaster(ip, port, result):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    s.send(result.encode())
    s.close()


if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", 9999))
        s.listen(20)
        print("0.0.0.0:9999 listening......")
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    while 1:
        conn, addr = s.accept()
        print("connect")

        writeLog("", "connect to master")
        data = conn.recv(65535)
        data = json.loads(data)

        fileId = data["fileId"]
        expId = int(data["expId"])
        userId = data["userId"]
        filePath = data["filePath"] 

        os.system("scp -r xxx@ip:%s ." % filePath) #FIXME

        writeLog("", "download finish")

        returnData = main(fileId, expId, userId, filePath)

        returnData["ip"] = "ip" #FIXME
        returnData["port"] = "port" #FIXME
        # returnData["ip"] = str(socket.gethostbyname(socket.gethostname()))

        returnData = json.dumps(returnData, indent=4, ensure_ascii=False)

        print("returnData ", returnData)

        writeLog(returnData, "returnData ")

        sendBackToMaster("master_ip", 4320, returnData) #FIXME

        conn.close()
