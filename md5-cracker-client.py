import md5
import socket, sys
import threading, time

def keep_alive(sock):
    while True:
        sock.send("keep-alive")
        time.sleep(1)

def check(start, end, password):
    while ''.join(start) != end:
        if md5.new(''.join(start)).hexdigest() == password:
            return "found:" + ''.join(start)
        char = ord(start[len(start) - 1]) + 1
        start[len(start) - 1] = chr(char)
        if ''.join(start[1:]) == 'zzzzz':
            start = chr(ord(start[0]) + 1)
            start += 'aaaaa'
        if start.count('{') > 0:
            index = start.index('{')
            start[index] = 'a'
            if index - 1 > -1:
                start[index - 1] = chr(ord(start[index - 1]) + 1)
            
    return "not found"

def main():
    # Create a UDP socket
    sock = socket.socket()
    sock.connect(('localhost', 2212))
    message = 'name: gabyimyagay'

    try:

        # Send data
        print >>sys.stderr, 'sending "%s"' % message
        sock.send(message)

        # Receive response
        print >>sys.stderr, 'waiting to receive'
        data = sock.recv(4096)
        print >>sys.stderr, 'received "%s"' % data

        # Format received data to be able to work it
        start, stop, md5 = data.split(",")
        start = start[6:]
        stop = stop[5:]
        md5 = md5[4:]

        t = threading.Thread(target=keep_alive, args=(sock,))
        t.start()

        start = list(start)
        a = check(start, stop, md5)
        print """\n==============="
             FOUND: """, a 
        print "==============="
        sock.send(a)

        
    finally:
        print >>sys.stderr, 'closing socket'
        sock.close()
    
if __name__ == '__main__':
    main()
