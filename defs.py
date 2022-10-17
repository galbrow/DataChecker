# server defs
import os

server_port = 502

sec = 3000

# enter [machine_ip, machine_name]

machines = []
f = open('machines.txt', 'r', encoding='utf-8')
m_read = f.readlines()
for mac in m_read:
    mac = mac.replace('\n', '')
    mac = mac.split(',')
    machines.append(mac)
f.close()

# registers of machine
speed_reg = 12
counter_reg = 118
hour_reg = 115
min_reg = 113
sec_reg = 110
command_reg = 100
refresh_time = 10

# fonts
title_font_size = 22
font_size = 15
font_of_container = 'Courier'

