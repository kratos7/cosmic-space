import sys
import zmq
import logging
import time
import json
from optparse import OptionParser

log = logging.getLogger('perf_log')
perf_log_file = "/tmp/test_perf.log"

def init_logger():
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

    # init perf logger
    log = init_logger()
    te = {1: 2, 3 : 5}

    # connect to servers
    for ip_port in server_ip_port_list:
        server_ip = ip_port.split(":")[0]
        port = int(ip_port.split(":")[1])
        print "SUB client connecting to PUB server at [%s:%s]" % (server_ip, port)
        log.info(json.dumps(te))
        socket.connect ("tcp://%s:%s" % (server_ip, port))
        print "SUB client succesfully connected to PUB server at [%s:%s]" % (server_ip, port)

    #
    #print "Collecting updates from weather server..."
    #socket.connect ("tcp://localhost:%s" % port)
    #
    #if len(sys.argv) > 2:
    #    socket.connect ("tcp://localhost:%s" % port1)
    #
    #
    ## Subscribe to zipcode, default is NYC, 10001
    #topicfilter = ""
    #socket.setsockopt(zmq.SUBSCRIBE, topicfilter)
    #
    ## Process 5 updates
    #total_value = 0
    #for update_nbr in range (5):
    #    string = socket.recv()
    #    topic, messagedata = string.split()
    #    total_value += int(messagedata)
    #    print topic, messagedata

    #print "Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr)
