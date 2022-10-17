from pyModbusTCP.client import ModbusClient
from defs import *


class Machine:
    def __init__(self, machine_ip, name, path):
        self.flag = True
        self.machine = ModbusClient(host=machine_ip, timeout=2)
        self.machine_ip = machine_ip
        self.name = name
        self.hours = self.read_register(hour_reg)
        self.minutes = self.read_register(min_reg)
        self.secs = self.read_register(sec_reg)
        self.counter = self.read_counter(counter_reg)
        self.speed = self.read_register(speed_reg)
        self.on_off = self.speed > 0
        self.path = path
        self.frame = None
        self.speed_label = None
        self.counter_label = None
        self.time_label = None

    def change_timer(self, h, m, s):
        self.client_write_to_register(hour_reg, h)
        self.client_write_to_register(min_reg, m)
        self.client_write_to_register(sec_reg, s)

    def change_counter(self, c1):
        self.client_write_to_register(counter_reg, c1 & 0xff00 >> 16)
        self.client_write_to_register(counter_reg - 1, c1 & 0x00ff)

    def change_speed(self, c1):
        self.client_write_to_register(speed_reg, c1)

    def update(self):
        if self.flag:
            self.machine = ModbusClient(host=self.machine_ip, timeout=2)
            self.hours = self.read_register(hour_reg)
            self.minutes = self.read_register(min_reg)
            self.secs = self.read_register(sec_reg)
            self.counter = self.read_counter(counter_reg)
            self.speed = self.read_register(speed_reg)
            self.on_off = self.speed > 0
            color = 'red' if not self.flag else 'green' if self.speed > 0 else 'black'
            self.frame.config(highlightbackground=color, highlightthicknes=2)
            self.speed_label.config(text=self.speed)
            self.counter_label.config(text=self.counter)
            machine_time = str(self.hours) + ':' + str(self.minutes) + ':' + str(self.secs)
            self.time_label.config(text=machine_time)
        else:
            self.frame.config(highlightbackground='red', highlightthicknes=2)
            self.speed_label.config(text='$$$')
            self.counter_label.config(text='$$$')
            self.time_label.config(text='$$$')

    def read_register(self, address):
        if self.name != '$$$':
            if self.flag:
                value = self.machine.read_holding_registers(address, 1)
                if value is None:
                    self.flag = False
                return 0 if value is None else value[0]
        return 0

    def reload(self):
        if self.name != '$$$':
            self.machine = ModbusClient(host=self.machine_ip, timeout=2)
            value = self.machine.read_holding_registers(0, 1)
            self.flag = True if value is not None else False

    def read_hour(self):
        hours = str(self.read_register(hour_reg))
        minutes = str(self.read_register(min_reg))
        secs = str(self.read_register(sec_reg))
        return hours + ":" + minutes + ":" + secs

    def write_machine(self, cl_num, current_date, current_time, sheet):
        machine_hour = self.read_hour()
        count = self.read_register(cl_num, counter_reg)
        sheet.append([current_date, current_time, machine_hour, count])

    def read_counter(self, address):
        return (self.read_register(address) << 16) + self.read_register(address - 1)

    def client_write_to_register(self, address, value):
        if self.flag:
            self.machine.write_single_register(address, value)

