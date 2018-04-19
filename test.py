import threading
import time

def DoTheDew():
    print("I did it")
    t = threading.Timer(1, function=DoTheDew)
    t.daemon = True
    t.start()    

if __name__ == '__main__':
    t = threading.Timer(1, function=DoTheDew)
    t.daemon = True
    t.start()
    time.sleep(10)