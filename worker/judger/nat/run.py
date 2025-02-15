from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import OVSBridge
import sys
import os
import time
import json
import filecmp
import http_server
sys.path.append("..")
from tools.tools import getPingResult,fillInInfo,getTraceroutePath,clearIP
from tools.topos import NATTopo,NATNATTopo
import threading

DEBUG = 0

standard_file = "standard.html"
h1_from_h3 = "h1_from_h3.html"
h2_from_h3 = "h2_from_h3.html"
h3_from_h1 = "h3_from_h1.html"
h3_from_h2 = "h3_from_h2.html"
h1_from_h2 = "h1_from_h2.html"


def rewriteStandard(file, myIP, yourIP):
    with open(file, "r") as f1:
        fileContent = f1.read()
    with open(file, "w") as f2:
        f2.write(fileContent.replace('my_ip_here',
                 myIP).replace('your_ip_here', yourIP))

    return file


def recoverStandard(file, originString):
    with open(file, "w") as f:
        f.write(originString)


def removeDownFile(fileList):
    for file in fileList:
        if os.path.isfile(file):
            os.remove(file)


def generateNATTopo(topo):
    net = Mininet(topo=topo, switch=OVSBridge, controller=None)

    h1, h2, h3, s1, n1 = net.get('h1', 'h2', 'h3', 's1', 'n1')

    h1.cmd('ifconfig h1-eth0 10.0.0.1/16')
    h1.cmd('route add default gw 10.0.0.254')

    h2.cmd('ifconfig h2-eth0 10.0.0.2/16')
    h2.cmd('route add default gw 10.0.0.254')

    n1.cmd('ifconfig n1-eth0 10.0.0.254/16')
    n1.cmd('ifconfig n1-eth1 159.226.39.43/24')

    h3.cmd('ifconfig h3-eth0 159.226.39.123/24')

    for h in (h1, h2, h3):
        h.cmd('./scripts/disable_offloading.sh')
        h.cmd('./scripts/disable_ipv6.sh')

    s1.cmd('./scripts/disable_ipv6.sh')

    n1.cmd('./scripts/disable_arp.sh')
    n1.cmd('./scripts/disable_icmp.sh')
    n1.cmd('./scripts/disable_ip_forward.sh')
    n1.cmd('./scripts/disable_ipv6.sh')

    return net, h1, h2, h3, s1, n1


def generateNATNATTopo(topo):
    net = Mininet(topo=topo, switch=OVSBridge, controller=None)

    h1, h2, n1, n2 = net.get('h1', 'h2', 'n1', 'n2')

    h1.cmd('ifconfig h1-eth0 10.0.0.1/16')
    h1.cmd('route add default gw 10.0.0.254')

    h2.cmd('ifconfig h2-eth0 10.0.0.2/16')
    h2.cmd('route add default gw 10.0.0.254')

    n1.cmd('ifconfig n1-eth0 10.0.0.254/16')
    n1.cmd('ifconfig n1-eth1 159.226.39.43/24')

    n2.cmd('ifconfig n2-eth0 10.0.0.254/24')
    n2.cmd('ifconfig n2-eth1 159.226.39.123/24')

    for h in (h1, h2):
        h.cmd('./scripts/disable_offloading.sh')
        h.cmd('./scripts/disable_ipv6.sh')

    for n in (n1, n2):
        n.cmd('./scripts/disable_arp.sh')
        n.cmd('./scripts/disable_icmp.sh')
        n.cmd('./scripts/disable_ip_forward.sh')
        n.cmd('./scripts/disable_ipv6.sh')

    return net, h1, h2, n1, n2

TIMEOUT = 10

def runh3ServerNATTest(execFile):

    net, h1, h2, h3, s1, n1 = generateNATTopo(NATTopo())

    print("before test")

    net.start()

    print(0)

    n1.cmd("./%s exp1.conf &" % execFile)

    h3.cmd("python3 http_server.py &")
    
    print(1)

    h1.cmd("wget http://159.226.39.123:8000 -O %s" % h1_from_h3)
    
    print(2)

    h2.cmd("wget http://159.226.39.123:8000 -O %s" % h2_from_h3)

    print(3)

    net.stop()


def h3ServerNATTest(execFile):

    td = threading.Thread(target=runh3ServerNATTest, args=(execFile, ), daemon=True)
    td.start()

    td.join(timeout=TIMEOUT)
    os.system("sudo pkill -SIGTERM %s > /dev/null 2>&1 " % execFile)
    os.system("ps -ef | grep http_server | grep -v grep | awk '{print $2}' | xargs -I {} sudo kill -9 {}")
    if td.is_alive(): #超时
        os.system("sudo mn -c > /dev/null 2>&1")
        return 2

    rewriteStandard(standard_file, "159.226.39.123", "159.226.39.43")

    ret = filecmp.cmp(standard_file, h1_from_h3) and filecmp.cmp(standard_file, h2_from_h3)

    removeDownFile([h1_from_h3, h2_from_h3])

    recoverStandard(standard_file, http_server.INDEX_PAGE_FMT)

    return ret


def runh1h2ServerNATTest(execFile):

    net, h1, h2, h3, s1, n1 = generateNATTopo(NATTopo())

    net.start()

    n1.cmd("./%s exp2.conf &" % execFile)

    h1.cmd("python3 http_server.py &")

    h2.cmd("python3 http_server.py &")

    h3.cmd("wget http://159.226.39.43:8000 -O %s" % h3_from_h1)

    h3.cmd("wget http://159.226.39.43:8001 -O %s" % h3_from_h2)

    net.stop()


def h1h2ServerNATTest(execFile):

    td = threading.Thread(target=runh1h2ServerNATTest, args=(execFile, ), daemon=True)
    td.start()

    td.join(timeout=TIMEOUT)
    os.system("sudo pkill -SIGTERM %s > /dev/null 2>&1 " % execFile)
    os.system("ps -ef | grep http_server | grep -v grep | awk '{print $2}' | xargs -I {} sudo kill -9 {}")
    if td.is_alive(): #超时
        os.system("sudo mn -c > /dev/null 2>&1")
        return 2

    cmp1 = filecmp.cmp(rewriteStandard(
        standard_file, "10.0.0.1", "159.226.39.123"), h3_from_h1)
    recoverStandard(standard_file, http_server.INDEX_PAGE_FMT)

    cmp2 = filecmp.cmp(rewriteStandard(
        standard_file, "10.0.0.2", "159.226.39.123"), h3_from_h2)
    recoverStandard(standard_file, http_server.INDEX_PAGE_FMT)

    removeDownFile([h3_from_h1, h3_from_h2])

    ret = cmp1 and cmp2

    return ret


def runNATNATTest(execFile):

    net, h1, h2, n1, n2 = generateNATNATTopo(NATNATTopo())

    net.start()

    n1.cmd("./%s exp1.conf &" % execFile)

    n2.cmd("./%s exp3.conf &" % execFile)

    h2.cmd("python3 http_server.py &")

    h1.cmd("wget http://159.226.39.123:8000 -O %s" % h1_from_h2)

    net.stop()


def NATNATTest(execFile):
    
    td = threading.Thread(target=runNATNATTest, args=(execFile, ), daemon=True)
    td.start()

    td.join(timeout=TIMEOUT)
    os.system("sudo pkill -SIGTERM %s > /dev/null 2>&1 " % execFile)
    os.system("ps -ef | grep http_server | grep -v grep | awk '{print $2}' | xargs -I {} sudo kill -9 {}")
    if td.is_alive(): #超时
        os.system("sudo mn -c > /dev/null 2>&1")
        return 2

    rewriteStandard(standard_file, "10.0.0.2", "159.226.39.43")

    ret = filecmp.cmp(standard_file, h1_from_h2)

    removeDownFile([h1_from_h2])

    recoverStandard(standard_file, http_server.INDEX_PAGE_FMT)

    return ret


if __name__ == "__main__":
    if DEBUG:
        result_path = "result"
        exec_file = "nat"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}
    print(result_path, exec_file)
    os.system("chmod 775 %s" % exec_file)

    os.system("sudo service openvswitch-switch restart > /dev/null")

    scores = {
        "SNAT": h3ServerNATTest(exec_file),
        "DNAT": h1h2ServerNATTest(exec_file),
        "SDNAT": NATNATTest(exec_file)
    }
    print(scores)
    if not DEBUG:
        os.remove(exec_file)

    fillInInfo(scores, info)
    
    print(info)
    
    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
