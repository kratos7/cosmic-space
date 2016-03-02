import sys
import zmq
import logging
import time
import json
from optparse import OptionParser
from utility.py_sys_cmd import PySysCommand

log = logging.getLogger('perf_log')

def init_logger(perf_log_file):
    loglevel = logging.DEBUG
    #formatter = logging.Formatter(format, '%j:%H:%M:%S')
    log = logging.getLogger('perf_log')
    log.setLevel(loglevel)
    hdlr = logging.FileHandler(perf_log_file, mode='w')
    #hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    return log

if __name__ == '__main__':
    usage = ('python %prog --server_ip_ports=<server_ip_port list>')
    parser = OptionParser(description='Simple ZeroMQ SUB client',
                          version="0.1 ", usage=usage)
    parser.add_option("--server_ip_ports", dest='server_ip_ports', type='string', default="",
                      help='comma sperated server_ip_ports')
    (options, args) = parser.parse_args()
    if ((len(args) != 0) or (not options.server_ip_ports)):
        parser.print_help()
        sys.exit(2)
    server_ip_ports = options.server_ip_ports

    # prepare PUB server ip_port list
    server_ip_port_list = []
    temp_list = []
    if "," in server_ip_ports:
        temp_list = server_ip_ports.split(",")
    else:
        temp_list.append(server_ip_ports)
    server_ip_port_list = temp_list[:]

    ## Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    topicfilter = ""


    # connect to servers
    # NOTE: currently works with only one SUB server
    for ip_port in server_ip_port_list:
        server_ip = ip_port.split(":")[0]
        port = int(ip_port.split(":")[1])
        print "SUB client connecting to PUB server at [%s:%s]" % (server_ip, port)
        socket.connect ("tcp://%s:%s" % (server_ip, port))
        print "SUB client succesfully connected to PUB server at [%s:%s]" % (server_ip, port)
        socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
        # Ideally socket will have a method to return client id, skimming through
        # /usr/lib/python2.7/dist-packages/zmq/sugar/socket.py didnt yield a quick soln.. hacking...
        client_id = str(socket)
        client_id = client_id[client_id.rfind("0x") + 2:len(client_id) - 1]
        print "Client id [%s] " % client_id

    # init perf logger
    sys_cmd = PySysCommand("mkdir -p /tmp/zmq_client_logs")
    sys_cmd.run()
    perf_log_file = "/tmp/zmq_client_logs/%s.log" % client_id
    log = init_logger(perf_log_file)
    runtime = 0
    print "Client iniating recv"
    while True:
        st_time = time.time()
        string = socket.recv()
        end_time = time.time()
        latency = end_time - st_time
        runtime += latency
        index, messagedata = string.split()
        print index, messagedata
        log.info("client_id=%s,latency=%s,total_runtime=%f,index=%s,messagedata=%s", client_id, latency, runtime, index, messagedata)
