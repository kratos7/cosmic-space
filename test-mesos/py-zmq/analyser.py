import zmq
import random
import sys
import time
import logging
from optparse import OptionParser
from os import listdir
from os.path import isfile, join
from utility.py_sys_cmd import PySysCommand

log = logging.getLogger('analyser_log')

def init_logger(log_file):
    loglevel = logging.DEBUG
    #formatter = logging.Formatter(format, '%j:%H:%M:%S')
    log = logging.getLogger('analyser_log')
    log.setLevel(loglevel)
    hdlr = logging.FileHandler(log_file, mode='w')
    #hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    return log

if __name__ == '__main__':
    usage = ('python %prog')
    parser = OptionParser(description='zmq data analyser',
                          version="0.1 ", usage=usage)
    parser.add_option("--log_path", dest='log_path', type='string', default="/tmp/zmq_client_logs",
                      help='log path to analyse')
    parser.add_option("--expected_msg_count", dest='expected_msg_count', type='int', default=1000,
                      help='Expected msg count that should be received by all clients')
    (options, args) = parser.parse_args()
    if (len(args) != 0):
        parser.print_help()
        sys.exit(2)
    log_path = options.log_path
    expected_msg_count  = options.expected_msg_count

    print "zmq client log analyser initiated..."
    print "Sifting the log directory..."
    all_files = ["%s/%s" % (log_path, f) for f in listdir(log_path) if isfile(join(log_path, f))]
    print "Analysing %d zmq client files" % len(all_files)
    #print all_files

    # extract message info from each client file
    client_perf_info = {}
    log_file = "/tmp/py_analyser"
    sys_cmd = PySysCommand("rm -rf %s" % log_file)
    sys_cmd.run(no_assert=True)
    log = init_logger(log_file)
    print "Dumping stats to %s" % log_file
    for zmq_file in all_files:
        with open(zmq_file) as f:
            content = f.read().splitlines()
            index_list = []
            for msg_info in content:
                msg_info = msg_info.split(",")
                # msg_info format:
                # ['client_id=7fe65cb21c18', 'latency=0.0101451873779', 'total_runtime=22.126667', 'index=999', 'messagedata=msg999']
                if len(msg_info) < 5:
                    print "Malformed message... (this is the most useless message ever printed by this program)"
                client_id = msg_info[0].split("=")[1]
                t_time  = msg_info[2].split("=")[1]
                index = msg_info[3].split("=")[1]
                index_list.append(index)
                if index not in client_perf_info:
                    client_perf_info[client_id] = {}
            client_perf_info[client_id].update({"all_received_messages": index_list, "total_time_taken": t_time})

    #print client_perf_info
    for client, info in client_perf_info.items():
        # TODO (AbdullahS): Do more intelligent parsing e-g check message contents, soon....
        message_list = info["all_received_messages"]
        total_time  = info["total_time_taken"]
        log.info("Expected no of messages                                    = %d" % (expected_msg_count))
        log.info("Total messages received by client [%s]           = %d" % (client, len(message_list)))
        log.info("Message delta                                              = %d" % (expected_msg_count - len(message_list)))
        log.info("Total time taken by client [%s] for all messages = %s" % (client, total_time))
        log.info("====================================================================================")
    print "Successfully anlaysed %d zmq client files" % len(all_files)
