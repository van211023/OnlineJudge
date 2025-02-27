from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
import sys
import os
import time
import json
sys.path.append("..")
from tools.tools import getPingResult,fillInInfo,getTraceroutePath
from tools.topos import hop3RouterTopo,simpleRouterTopo
import threading
DEBUG = 0

def generateSimpleRouterTopo(topo):
    net = Mininet(topo=topo, controller=None)

    h1, h2, h3, r1 = net.get('h1', 'h2', 'h3', 'r1')
    h1.cmd('ifconfig h1-eth0 10.0.1.11/24')
    h2.cmd('ifconfig h2-eth0 10.0.2.22/24')
    h3.cmd('ifconfig h3-eth0 10.0.3.33/24')

    h1.cmd('route add default gw 10.0.1.1')
    h2.cmd('route add default gw 10.0.2.1')
    h3.cmd('route add default gw 10.0.3.1')

    for h in (h1, h2, h3):
        h.cmd('./scripts/disable_offloading.sh')
        h.cmd('./scripts/disable_ipv6.sh')

    r1.cmd('ifconfig r1-eth0 10.0.1.1/24')
    r1.cmd('ifconfig r1-eth1 10.0.2.1/24')
    r1.cmd('ifconfig r1-eth2 10.0.3.1/24')

    r1.cmd('./scripts/disable_arp.sh')
    r1.cmd('./scripts/disable_icmp.sh')
    r1.cmd('./scripts/disable_ip_forward.sh')
    r1.cmd('./scripts/disable_ipv6.sh')

    return net, h1, h2, h3, r1


def generateHop3RouterTopo(topo):
    net = Mininet(topo=topo, controller=None)

    h1, h2, r1, r2 = net.get('h1', 'h2', 'r1', 'r2')

    h1.cmd('ifconfig h1-eth0 10.0.1.11/24')
    h2.cmd('ifconfig h2-eth0 10.0.3.33/24')

    r1.cmd('ifconfig r1-eth0 10.0.1.1/24')
    r1.cmd('ifconfig r1-eth1 10.0.2.1/24')

    r2.cmd('ifconfig r2-eth0 10.0.2.2/24')
    r2.cmd('ifconfig r2-eth1 10.0.3.1/24')

    h1.cmd('route add default gw 10.0.1.1')
    h2.cmd('route add default gw 10.0.3.1')
    r1.cmd('route add -net 10.0.3.0/24 gw 10.0.2.2 dev r1-eth1')
    r2.cmd('route add -net 10.0.1.0/24 gw 10.0.2.1 dev r2-eth0')

    h1.cmd('./scripts/disable_offloading.sh')
    h1.cmd('./scripts/disable_firewall.sh')
    h2.cmd('./scripts/disable_offloading.sh')
    h2.cmd('./scripts/disable_firewall.sh')

    r1.cmd('./scripts/disable_arp.sh')
    r1.cmd('./scripts/disable_icmp.sh')
    r1.cmd('./scripts/disable_ip_forward.sh')
    r1.cmd('./scripts/disable_firewall.sh')

    r2.cmd('./scripts/disable_arp.sh')
    r2.cmd('./scripts/disable_icmp.sh')
    r2.cmd('./scripts/disable_ip_forward.sh')
    r2.cmd('./scripts/disable_firewall.sh')

    return net, h1, h2, r1, r2

tdrt = 2
TIMEOUT = 11

def runrouterSimpleTest(execFile, testType):
    global tdrt
    net, h1, h2, h3, r1 = generateSimpleRouterTopo(simpleRouterTopo())

    net.start()
    r1.cmd("./%s &" % execFile)
    time.sleep(1)

    if testType == "h1_ping_r1":
        pingResult = getPingResult(h1, "10.0.1.1")
        tdrt = "0% packet loss" in pingResult
    elif testType == "h1_ping_h2":
        pingResult = getPingResult(h1, "10.0.2.22")
        tdrt = "0% packet loss" in pingResult
    elif testType == "h1_ping_h3":
        pingResult = getPingResult(h1, "10.0.3.33")
        tdrt = "0% packet loss" in pingResult
    elif testType == "h1_ping_uh":
        pingResult = getPingResult(h1, "10.0.2.33")
        print(pingResult)
        tdrt = "Destination Host Unreachable" in pingResult
    elif testType == "h1_ping_un":
        pingResult = getPingResult(h1, "10.0.4.1")
        tdrt = "Destination Net Unreachable" in pingResult
    
    net.stop()


def routerSimpleTest(execFile, testType):
    global tdrt

    td = threading.Thread(target=runrouterSimpleTest, args=(execFile, testType), daemon=True)
    tdrt = 2
    td.start()

    td.join(timeout=TIMEOUT)
    tdrt_tmp = tdrt
    os.system("sudo pkill -SIGTERM %s" % execFile)
    if td.isAlive(): #超时
        os.system("sudo mn -c > /dev/null 2>&1")
    return tdrt_tmp


def runrouterHop3Test(execFile, testType):
    global tdrt
    net, h1, h2, r1, r2 = generateHop3RouterTopo(hop3RouterTopo())

    net.start()
    r1.cmd("./%s &" % execFile)
    r2.cmd("./%s &" % execFile)
    time.sleep(1)

    if testType == "hop3_ping":
        pingResult1 = getPingResult(h1, "10.0.1.1")
        pingResult2 = getPingResult(h1, "10.0.2.2")
        tdrt = "0% packet loss" in pingResult1 and "0% packet loss" in pingResult2
    elif testType == "hop3_traceroute":
        tracerouteRes = getTraceroutePath(h1, "10.0.3.33")
        tdrt = (tracerouteRes == ["10.0.1.1", "10.0.2.2", "10.0.3.33"] \
            or tracerouteRes == ["_gateway", "10.0.2.2", "10.0.3.33"])
        
    net.stop()


def routerHop3Test(execFile, testType):
    global tdrt

    td = threading.Thread(target=runrouterHop3Test, args=(execFile, testType), daemon=True)
    tdrt = 2
    td.start()

    td.join(timeout=TIMEOUT)
    tdrt_tmp = tdrt
    os.system("sudo pkill -SIGTERM %s" % execFile)
    if td.isAlive(): #超时
        os.system("sudo mn -c > /dev/null 2>&1")
    return tdrt_tmp


if __name__ == '__main__':
    if DEBUG:
        result_path = "result"
        exec_file = "router"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}

    scores = {
        "h1_ping_r1":      routerSimpleTest(exec_file, "h1_ping_r1"),
        "h1_ping_h2":      routerSimpleTest(exec_file, "h1_ping_h2"),
        "h1_ping_h3":      routerSimpleTest(exec_file, "h1_ping_h3"),
        "h1_ping_uh":      routerSimpleTest(exec_file, "h1_ping_uh"),
        "h1_ping_un":      routerSimpleTest(exec_file, "h1_ping_un"),
        "hop3_ping":       routerHop3Test(exec_file, "hop3_ping"),
        "hop3_traceroute": routerHop3Test(exec_file, "hop3_traceroute")
    }
    if not DEBUG:
        os.remove(exec_file)

    print(scores)

    fillInInfo(scores, info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
