#!/usr/local/bin/python3

#
#   Basic port scanner, scans a set of ports on a specific host or range of hosts.
#   Takes as input an IP host or network (range) and port list or port range.  
#   Run "python tdkNMap.py --help" for usage info.
#

import getopt
import ipaddress
import os
import re
import socket
import sys
import traceback

scriptName = ""
scanPorts = [80,21,443]
scanOpts = {}
timeout = 5
debug = False

#
# Print usage to cmd line, optionally exit here with return value. 
#
def ShowUsage(returnFromCall = False, returnValue = 1):

    global scriptName

    usage = str.format("Usage: python {0} [-p portRange] [-t timeoutSeconds] [-d|--debug] [-v|--verbose] [-h|--help] targetIPRange", scriptName)
    sample1 = str.format("\tsample 1 -> python {0} -p 0-443 192.168.1.0/24 (scan an ip address range, ports 0 through 443)", scriptName)
    sample2 = str.format("\tsample 2 -> python {0} -t 1 -p 80,443 192.168.1.5 (scan one ip address and ports 80 & 443, socket timeout is 1 second)", scriptName)

    print("\n" + usage)
    print(sample1)
    print(sample2)
    print()

    #myPrint(traceback.print_tb(traceback.extract_stack()))       

    if ( False == returnFromCall ): 
        exit(returnValue)

    return

#
# Assume the first element in the tuple is the command line parameter, return a list of items 2..N
#
def ParseCmdLine(args, opts):

    global scanPorts

    scanOpts["portRange"] = [80,443] # default port list here

    for t in opts:
        if ( 0 == len(t)):
            print("Unexpected command like parameter: " + str(t))
            ShowUsage()
        elif (t[0] in ('-h', '--help')):
                ShowUsage()
        elif (t[0] in ('-p','--ports')):
            scanOpts["portRange"] = ParsePortRange(t)
        elif (t[0] in ('--verbose', '-v', '--debug', '-d')):    # maybe in the future we'll distinguish between verbose and debug
            global debug
            debug = True
        elif (t[0] in ('-t')):
            global timeout
            timeout = int(t[1])

    if ( 1 <= len(args)):
        scanOpts["ipAddress"] = args[0]
    else:
        print("No IP address or range specified.")
        exit(1)

    return scanOpts

#
# Expects a string in the format "start_port_number-end_port_number" or "port1,port2,port3"
#
# Returns a list of integers
#
def ParsePortRange(t):

    global scanPorts

    if ( 1 == len(t)):
        print(str.format("Warning: Empty port list provided. Using default {0}", scanPorts))
        return scanPorts

    elif ( 2 == len(t)):
        scanPorts.clear()
        portStr = str(t[1])

        try:
            # String is expected to be "N-M" or "P1,P2,P3,...,PN", N and M are some natural numbers, N < M
            if ( -1 != portStr.find(',')):      # must be comma separated port numbers
                portStrings = portStr.split(',')
                for x in portStrings:
                    scanPorts.append(int(x))
            elif( -1 != portStr.find('-')):       # must be two natural numbers separated by a hyphen
                ports = portStr.split('-')
                for x in range(int(ports[0]), int(ports[1]) + 1):
                    scanPorts.append(x)
            else:                               # must be one natural number
                scanPorts.append(int(portStr))
                    
            return scanPorts
        except:
            print("Error parsing {0}.", portStr)
            ShowUsage()
    else:
        print("Unexpected command line parameter: " + str(t))
        ShowUsage()
        return []   # should be unreachable, purely defensive programming.
#
# Expects a host ip, or a range (e.g. 192.168.1.1 or 192.168.1.0/24 for a range)
# Returns an ipaddress object
#
def ParseIPAddress(ipAddrStr):
    try:
        ipa = ipaddress.ip_interface(ipAddrStr)
        return ipa
    except Exception:
        print(str.format("Problem with ipaddress/range argument: {0}\n", ipAddrStr))


#
#
#
def runScan(scanOpts):

    interface = ipaddress.ip_interface(scanOpts["ipAddress"])
    failures = 0
    successes = 0
    hosts = []
    if (1 == interface.network.num_addresses):
        hosts.append(interface.network.network_address.compressed)
    else:
        hosts = list(interface.network.hosts())

    for host in  hosts:
            for port in scanOpts["portRange"]:
                with socket.socket() as s:     # s/b AF_INET, type=SOCK_STREAM
                    global timeout
                    s.settimeout(timeout)

                    try:
                        try:
                            s.connect((str(host),port))
                            myPrint(str.format("{0} port {1} : Connected", host, port))
                            successes += 1
                        except socket.error as sockErr:
                            myPrint(str.format("{0} port {1} : Failed to connect -> {2}", host, port, sockErr))
                            failures += 1
                            continue

                        try:
                            s.send(b'\n')
                            banner = s.recv(512)
                            myPrint(str.format("{0} port {1} : Returned banner -> {2}", host, port, banner))
                            successes += 1
                        except socket.error as sockErr:
                            myPrint(str.format("{0} port {1} : Failed to read banner -> {2}", host, port, sockErr))
                            failures += 1
                    except Exception as genExcept:
                        myPrint(str.format("{0} port {1} : Unknown error -> ", host, port, genExcept))
                        failures += 1

    print(str.format("\n{0} successful connections, {1} failures.\n", successes, failures))
    return

def myPrint(outStr):
    if (debug):
        print(outStr)

#
#
#
def main(argv, sname):

    try:
        global scriptName
        scriptName = sname

        opts, args = getopt.getopt(argv, 'dhvp:t:', ['debug', 'help', 'ports', 'verbose'])
        scanOpts = ParseCmdLine(args, opts)

        myPrint(scanOpts)

        runScan(scanOpts)
    except SystemExit as se:
        return
    
    return

if __name__ == "__main__":
    main(sys.argv[1:], os.path.basename(__file__))
    exit(0)
