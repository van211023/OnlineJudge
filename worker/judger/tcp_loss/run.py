from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import sys
import os
import time
import json
import filecmp
sys.path.append("..")
from tools.topos import TCPLossTopo
from tools.tools import fillInInfo

DEBUG = 0
send_time = 40
client_file = "client-input.dat"
server_file = "server-output.dat"


def generateBulkTopo(topo):
    net = Mininet(topo=topo, controller=None, link=TCLink)

    h1, h2 = net.get('h1', 'h2')
    h1.cmd('ifconfig h1-eth0 10.0.0.1/24')
    h2.cmd('ifconfig h2-eth0 10.0.0.2/24')

    for h in (h1, h2):
        # h.cmd('scripts/disable_arp.sh')
        # h.cmd('scripts/disable_icmp.sh')
        # h.cmd('scripts/disable_ip_forward.sh')
        h.cmd('scripts/disable_ipv6.sh')
        h.cmd('scripts/disable_offloading.sh')
        h.cmd('scripts/disable_tcp_rst.sh')
        
    return net, h1, h2


def CSendCTest(execFile):
    net, h1, h2 = generateBulkTopo(TCPLossTopo())

    net.start()

    h1.cmd("./%s server 10001 > cc-server.log 2>&1 &" % execFile)
    
    time.sleep(10)

    h2.cmd("./%s client 10.0.0.1 10001 > cc.log 2>& 1 &" % execFile)

    time.sleep(send_time)  # waiting server recv

    os.system("sudo pkill -SIGTERM %s" % execFile)
    net.stop()

    os.system('cp server-output.dat outputcc.dat')

    try:
        ret = filecmp.cmp(client_file, server_file)
        os.remove(server_file)
        return ret
    except:
        return False

# server python

def CSendPythonTest(execFile):
    net, h1, h2 = generateBulkTopo(TCPLossTopo())

    net.start()

    h1.cmd("python3 -u bulk.py server 10001 > cp-server.log 2>&1 &")
    
    time.sleep(10)

    h2.cmd("./%s client 10.0.0.1 10001 > cp.log 2>&1 &" % execFile)

    time.sleep(send_time)  # waiting server recv

    os.system("sudo pkill -SIGTERM %s" % execFile)
    os.system("ps -ef | grep bulk | grep -v grep | awk '{print $2}' | xargs sudo kill")
    net.stop()

    os.system('cp server-output.dat outputcp.dat')

    try:
        ret = filecmp.cmp(client_file, server_file)
        os.remove(server_file)
        return ret
    except:
        return False
# server C


def pythonSendCTest(execFile):
    net, h1, h2 = generateBulkTopo(TCPLossTopo())

    net.start()

    h1.cmd("./%s server 10001 &" % execFile)
    
    time.sleep(5)
    #CLI(net)
    h2.cmd("python bulk.py client 10.0.0.1 10001 &")

    time.sleep(send_time)  # waiting server recv

    os.system("sudo pkill -SIGTERM %s" % execFile)
    os.system("ps -ef | grep bulk | grep -v grep | awk '{print $2}' | xargs sudo kill")
    net.stop()

    try:
        ret = filecmp.cmp(client_file, server_file)
        # if ret == False:
        #     sys.exit(0)
        os.remove(server_file)
        return ret
    except Exception as ex:
        return False
    
def pythonSendPythonTest(execFile):
    net, h1, h2 = generateBulkTopo(TCPLossTopo())

    net.start()

    h1.cmd("python3 bulk.py server 10001 &")
    
    time.sleep(5)

    h2.cmd("python3 bulk.py client 10.0.0.1 10001 &")

    time.sleep(send_time)  # waiting server recv

    net.stop()

    try:
        ret = filecmp.cmp(client_file, server_file)
        os.remove(server_file)
        return ret
    except Exception as ex:
        print(ex)
        return False


if __name__ == "__main__":
    if DEBUG:
        result_path = "result"
        exec_file = "tcp_bulk"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}

    # 3 tests (client sends bulk to server, server save the bulk as server-output.dat)
    # 1: client: C server: C
    # 2: client: python server: C
    # 3: client: C server: python
    # h1: server
    # h2: client
    scores = {
        "CSendC": CSendCTest(exec_file),
        "CSendPython": CSendPythonTest(exec_file),
        "pythonSendC": pythonSendCTest(exec_file),
        #"pythonSendPython": pythonSendPythonTest(exec_file)
    }
    if not DEBUG:
        os.remove(exec_file)
    print(scores)
    # if scores["CSendC"] == 1 or scores["CSendPython"] == 1 or scores["pythonSendC"] == 1:
    #     scores["CSendC"] = 1
    #     scores["CSendPython"] = 1
    #     scores["pythonSendC"] = 1
    fillInInfo(scores, info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
