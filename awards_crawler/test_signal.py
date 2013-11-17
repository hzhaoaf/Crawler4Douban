#coding=utf8
import sys, signal, time

def test_try_except():
    print 'test try_except...'
    while True:
        try:
            time.sleep(2)
            pass
        except KeyboardInterrupt:
            print 'catch KeyboardInterrupt!!!'
            sys.exit()

def signal_handler(signal, frame):
    print 'you press Ctrl+C'
    sys.exit(0)

def test_signal():
    signal.signal(signal.SIGINT, signal_handler)
    print 'press the Ctrl+C'
    sys.pause()


if __name__ == '__main__':
    #test_try_except()
    test_signal()
