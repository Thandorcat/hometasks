import psutil
import time
import datetime
import json

config = open('config.json')
data = json.load(config)
config.close()
output = data['Output']
interval = data['Interval']*60
while True:
    if output == 'text':
        file = open("log.txt", 'a+')
        file.seek(0, 0)
        num = 0
        for line in file.readlines():
            if "SNAPSHOT" in line:
                num += 1
        write=''
        write += "SNAPSHOT " + str(num+1) + ": " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n"
        write += "CPU: " + str(psutil.cpu_percent()) + "%" + "\n"
        write += "Memory: " + str(psutil.virtual_memory().used // 1024 ** 3) + "Gb" + "\n"
        write += "Virtual: " + str(psutil.swap_memory().used // 1024 ** 3) + "Gb" + "\n"
        write += "DiskIO: " + "\n"
        write += "\tRead: " + str(psutil.disk_io_counters().read_bytes // 1024 ** 2) + "Mb" + "\n"
        write += "\tWritten: " + str(psutil.disk_io_counters().write_bytes // 1024 ** 2) + "Mb" + "\n"
        write += "Network: " + "\n"
        data = psutil.net_if_addrs()
        for key in data.keys():
            write += "\t" + str(key) + ": " + str(data[key][0].address) + "\n"
        write += "\tReceived: " + str(psutil.net_io_counters().bytes_recv // 1024 ** 2) + "Mb" + "\n"
        write += "\tSent: " + str(psutil.net_io_counters().bytes_sent // 1024 ** 2) + "Mb" + "\n"
        file.write(write)
        file.close()
    elif output == 'json':
        try:
            file = open("log.json",'a+')
            file.seek(0, 0)
            info = json.load(file)
            num = len(info["SYSINFO"])
            file.close()
            file = open("log.json",'w')
        except json.decoder.JSONDecodeError:
            info={}
            info["SYSINFO"] = []
            num = 0
        write={}
        write['SNAPSHOT'] = num + 1
        write['CPU']=psutil.cpu_percent()
        write['Memory'] = psutil.virtual_memory().used//1024 ** 3
        write['Virtual'] = psutil.swap_memory().used // 1024 ** 3
        write['DiskIO'] = {'Read':psutil.disk_io_counters().read_bytes // 1024 ** 2,'Written':psutil.disk_io_counters().write_bytes // 1024 ** 2}
        network={}
        data = psutil.net_if_addrs()
        for key in data.keys():
            network[key] = data[key][0].address
        network['Received']= psutil.net_io_counters().bytes_recv // 1024 ** 2
        network['Sent'] = psutil.net_io_counters().bytes_sent // 1024 ** 2
        write['Network'] = network
        write['TIMESTAMP'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        info["SYSINFO"].append(write)
        json.dump(info, file)
        file.close()
    else:
        print("Unsupported output format!")
    time.sleep(interval)
