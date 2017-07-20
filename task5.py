import psutil
import time
import datetime
import json

class Writer:
    def __init__(self, file):
        self.filename = file

class TextWriter(Writer):
    def open(self):
        self._file = open(self.filename, 'a+')
        self._file.seek(0, 0)
        num = 0
        for line in self._file.readlines():
            if "SNAPSHOT" in line:
                num += 1
        return num
    def write(self, string):
        written = self._file.write(string)
        self._file.close()
        return written == string.__len__()


class JsonWriter(Writer):
    def open(self):
        try:
            self._file = open(self.filename,'a+')
            self._file.seek(0, 0)
            self._info = json.load(self._file)
            num = len(self._info["SYSINFO"])
            self._file.close()
            self._file = open(self.filename,'w')
            return num
        except json.decoder.JSONDecodeError:
            self._info={}
            self._info["SYSINFO"] = []
            return 0
    def write(self, dict):
        self._info["SYSINFO"].append(dict)
        json.dump(self._info, self._file)
        self._file.close()

class StringCollector:
    @classmethod
    def collect(cls, number):
        write = ''
        write += "SNAPSHOT " + str(number + 1) + ": " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n"
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
        return write

class DictCollector:
    @classmethod
    def collect(cls, number):
        write = {}
        write['SNAPSHOT'] = number + 1
        write['TIMESTAMP'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write['CPU'] = psutil.cpu_percent()
        write['Memory'] = psutil.virtual_memory().used // 1024 ** 3
        write['Virtual'] = psutil.swap_memory().used // 1024 ** 3
        write['DiskIO'] = {'Read': psutil.disk_io_counters().read_bytes // 1024 ** 2,
                           'Written': psutil.disk_io_counters().write_bytes // 1024 ** 2}
        network = {}
        data = psutil.net_if_addrs()
        for key in data.keys():
            network[key] = data[key][0].address
        network['Received'] = psutil.net_io_counters().bytes_recv // 1024 ** 2
        network['Sent'] = psutil.net_io_counters().bytes_sent // 1024 ** 2
        write['Network'] = network
        return write

class ConfigGetter:
    @classmethod
    def get(cls, filename):
        config = open(filename)
        data = json.load(config)
        config.close()
        output = data['Output']
        interval = data['Interval']
        return output, interval



output, interval = ConfigGetter.get('config.json')

while True:
    if output == 'text':
        writer = TextWriter("log.txt")
        number = writer.open()
        data = StringCollector.collect(number)
        writer.write(data)
    elif output == 'json':
        writer = JsonWriter("log.json")
        number = writer.open()
        data = DictCollector.collect(number)
        writer.write(data)
    else:
        print("Unsupported output format!")
    time.sleep(interval)
