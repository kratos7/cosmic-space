import random
import sys
import time
from optparse import OptionParser
from marathon import MarathonClient
from marathon.models import MarathonApp

if __name__ == '__main__':
    usage = ('python %prog')
    parser = OptionParser(description='Simple marathon-python based master to launch apps',
                          version="0.1 ", usage=usage)
    (options, args) = parser.parse_args()
    if (len(args) != 0):
        parser.print_help()
        sys.exit(2)


    print "Initiating marathonclient..."
    c = MarathonClient('http://localhost:8080')
    app_cmd = "python /home/abdullah/cosmic-space/test-mesos/py-zmq/sub_client.py --server_ip_ports 10.10.0.2:5556"

    # launch app
    print "Initiating zmq-client app"
    c.create_app('zmq-client', MarathonApp(cmd=app_cmd, mem=16, cpus=0.01))

    # scale
    raw_input("scale_apps upto 400")
    c.scale_app('zmq-client', instances=400)

    # delete
    raw_input("delete apps")
    c.delete_app('zmq-client')
