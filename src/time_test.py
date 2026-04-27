import datetime as dt

start_time = "06:00:00"
random_time_new_start = 20
start_time_1 = dt.datetime.strptime(start_time, "%H:%M:%S")+ dt.timedelta(minutes = random_time_new_start)
print(start_time_1.time())

now = dt.datetime.now()
current_time = now.time()
print(current_time)

if(current_time > start_time_1.time()):
    print(" we have success")   
else:
    print(" we have failure")