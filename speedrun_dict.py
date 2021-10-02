import datetime

class LBDict(dict):
    def dict_from_file(self, filename):
        with open(filename, "r") as f:
            for data in f.readlines():
                name, time, proof, date = data.split(" - ")
                self[name] = [formatTime(time), proof, date]

    def sort(self):
        ordered_lb = sorted(self.items(), key=lambda x: x[1][0])
        self.clear()
        self.update(dict(ordered_lb))

#a = LBDict([('Sausage#6065', [datetime.timedelta(seconds=4148), 'link1', '2021-02-13']), ('vicnet#6472', [datetime.timedelta(seconds=38702), 'link2', '2021-02-9']), ('proce#9069', [datetime.timedelta(seconds=38522), 'link3', '2021-02-9'])])
