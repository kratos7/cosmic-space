import zmq
import random
import sys
import time
from optparse import OptionParser

if __name__ == '__main__':
    usage = ('python %prog --port=<server port>')
    parser = OptionParser(description='Simple ZeroMQ PUB server',
                          version="0.1 ", usage=usage)
    parser.add_option("--port", dest='port', type='int', default=5556,
                      help='server port')
    parser.add_option("--msg_count", dest='msg_count', type='int', default=1000,
                      help='server port')
    parser.add_option("--delay", dest='delay', type='float', default=0.2,
                      help='delay between publishing messages')
    (options, args) = parser.parse_args()
    if (len(args) != 0):
        parser.print_help()
        sys.exit(2)
    port = options.port
    msg_count = options.msg_count
    delay = options.delay


    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)

    print "PUB server initiating sending all DATA"
    for index in range(msg_count):
        messagedata = "msg%d" % index
        print "%d %s" % (index, messagedata)
        socket.send("%d %s" % (index, messagedata))
        time.sleep(delay)

    print "PUB server finished sending all DATA"
