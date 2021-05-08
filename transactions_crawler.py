import functions
start = "0"
size = "2000"

for i in range(5):
    tra_into_db = functions.transactions(start,size)

    start = int(start) + int(size)
    start = str(start)
