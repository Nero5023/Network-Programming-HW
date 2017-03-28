import optparse
from ping import Pinger
def parse_args():
    usage = """ NAME:
    ping -- send ICMP ECHO_REQUEST packets to network hosts

usage: %prog [options] host ...
Run it like this:

    python main.py host ...
"""
    p = optparse.OptionParser(usage)

    help = "The count of package to."
    p.add_option('-c', '--count', type='int', help=help, default=4)

    help = "The timeout of ping."
    p.add_option('-t', '--timeout', type='int', help=help, default=2)

    options, args = p.parse_args()

    if options.count <= 0:
        p.error("The count of package to send should be larger than 0")

    if options.timeout <= 0:
        p.error("The timeout should be larger than 0")

    if len(args) == 0:
        p.error("Provide at least one host")

    return options, args

if __name__ == '__main__':
    options, hosts = parse_args()
    for host in hosts:
        pinger = Pinger(target_host=host, count=options.count, timeout=options.timeout)
        pinger.ping()
        print("------------")
