import Queue
q = Queue.Queue(10)
for i in range(10):
    myData = 'A'
    q.put(myData)
    myData = 'B'

while not q.empty():
    data = q.get()
    print data
