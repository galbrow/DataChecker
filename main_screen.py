from multiprocessing import Process
from threading import Thread, Timer
from tkinter import *
from tkinter import messagebox

from defs import *
from Machine import Machine
from openpyxl import load_workbook
import schedule
from admin_screen import admin_screen
from loading import loading_start
import time
from datetime import datetime, timedelta

ticks = 1
machines_lst = []
global file_path
timer = None
user_type = 2
on_reset = False


def write_to_excel(m_ip=''):
    try:
        global on_reset
        m_lst = machines_lst if m_ip == '' else [x for x in machines_lst if x.machine_ip == m_ip]
        # m_lst = machines_lst
        wb = load_workbook(file_path)
        now = datetime.now()
        current_date = now.strftime("%m/%d/%Y")
        current_time = now.strftime("%H:%M:%S")
        for m in m_lst:
            write_machine(m, current_date, current_time, wb[m.name])
            m.client_write_to_register(command_reg, 2)
        wb.save(file_path)
        wb.close()
        if m_ip == '':
            on_reset = False
    except Exception:
        # def err():
        error_msg = """תקלה בהחלפת משמרת
נא לוודא שקובץ האסקסל סגור"""
        messagebox.showwarning(title=None, message=error_msg)
        # Thread(target=err).start()
        write_to_excel(m_ip)


def write_to_excel_with_timer():
    write_to_excel()
    while_func()


def while_func(h=7):
    global on_reset
    global timer
    if user_type != 1:
        on_reset = False
    else:
        if not on_reset:
            on_reset = True
            x = datetime.today()
            hour = 19 if (7 < x.hour < 19) else 7
            y = x.replace(day=x.day, hour=hour, minute=0, second=0, microsecond=0)
            delta_t = y - x

            secs = delta_t.total_seconds()

            timer = Timer(secs, write_to_excel_with_timer)
            timer.start()

    # global on_reset
    # if not on_reset:
    #     on_reset = True
    #     for hour in hours:
    #         job = schedule.every().day.at(hour).do(write_to_excel)
    #     while on_reset:
    #         schedule.run_pending()
    #         if user_type != 1:
    #             schedule.cancel_job(job)
    #             on_reset = False
    #         time.sleep(60)  # wait one minute


def write_machine(machine, current_date, current_time, sheet):
    machine_hour = machine.read_hour()
    count = machine.read_register(counter_reg)
    sheet.append([current_date, current_time, machine_hour, count])


def load_machines():
    machines_lst.clear()
    # while len(machines) < 3:
    #     machines.append(['150.10.10.10', '$$$'])
    for machine in machines:
        m = Machine(machine[0], machine[1], file_path)
        machines_lst.append(m)


def clock(app):
    global ticks
    try:
        for machine in machines_lst:
            if ticks % 10 == 0:
                machine.reload()
            machine.update()
        ticks = ticks + 1
        Timer(1, lambda: clock(app)).start()
    except Exception as e:
        print(e)


def load_vars():
    global file_path
    global user_type

    # global machines
    f = open('path.txt', 'r', encoding='utf-8')
    file_path = f.readline().replace('\n', '')
    user_type = int(f.readline().replace('\n', ''))
    f.close()
    # machines_f = open('path.txt', 'r', encoding='utf-8')
    # machines = machines_f.readlines()
    # machines_f.close()


def main_activate():
    global timer
    # Process(target=loading_start(len(machines))).start()
    load_vars()
    load_machines()
    pad = 3
    main_screen = Tk()
    main_screen.title('Ashplast')
    x_screen = main_screen.winfo_screenwidth() - pad
    y_screen = main_screen.winfo_screenheight() - pad
    main_screen.geometry("{0}x{1}+0+0".format(x_screen, y_screen))
    main_screen.grid()

    if user_type == 1:
        Thread(target=while_func, args=(["07:00", "19:00"], )).start()
    else:
        if timer is not None:
            timer.cancel()

    # Label(main_screen, text="Server status", width=20, justify=CENTER).pack()
    Label(main_screen, text='Ashplast', font=(font_of_container, title_font_size-5, "bold")).\
        grid(row=0, sticky=EW, columnspan=5)
    row = 1
    col = 0
    for machine in machines_lst:
        color = 'red' if not machine.flag else 'green' if machine.speed > 0 else 'black'
        frame = Frame(main_screen, highlightbackground=color, highlightthicknes=3)
        machine.frame = frame
        frame.grid(row=row, column=(col % 3), padx=10, pady=10, ipadx=10, ipady=0, sticky="nsew")
        # name
        Label(frame, text=machine.name, font=(font_of_container, title_font_size, "bold"))\
            .grid(row=0, column=0, sticky=EW, columnspan=2)

        # speed
        Label(frame, text="Speed(bags/min)", font=(font_of_container, font_size))\
            .grid(row=1, column=0, sticky=W)
        machine.speed_label = Label(frame, text=machine.speed, font=(font_of_container, font_size))
        machine.speed_label.grid(row=1, column=1, sticky=W)
        # counter
        Label(frame, text="Counter(bags)", font=(font_of_container, font_size)).grid(row=2, column=0, sticky=W)
        machine.counter_label = Label(frame, text=machine.counter, font=(font_of_container, font_size))
        machine.counter_label.grid(row=2, column=1, sticky=W)
        # time
        Label(frame, text="Hour Meter", font=(font_of_container, font_size)).grid(row=3, column=0, sticky=W)
        m_secs = '0' + str(machine.secs) if machine.secs < 10 else str(machine.secs)
        m_minutes = '0' + str(machine.minutes) if machine.minutes < 10 else str(machine.minutes)
        m_hours = '0' + str(machine.hours) if machine.hours < 10 else str(machine.hours)
        machine_time = m_hours + ':' + m_minutes + ':' + m_secs
        machine.time_label = Label(frame, text=machine_time, font=(font_of_container, font_size))
        machine.time_label.grid(row=3, column=1, sticky=W)
        # ip
        Label(frame, text=machine.machine_ip).grid(row=4, sticky=W)
        row = row + (1 if (col % 3) == 2 else 0)
        col = col + 1

    def forget(label):
        label.grid_forget()

    # Admin settings
    def call_admin():
        load_vars()
        admin_screen(write_to_excel, file_path, user_type, main_activate, machines_lst, machines, main_screen)

    Button(main_screen, text='מנהל תפ"י', command=call_admin, font=(font_of_container, font_size))\
        .grid(row=row + 4, column=0, sticky=W, padx=10, pady=10)

    # Messages
    err = Label(main_screen, text="Wrong Password", fg='red')
    succ = Label(main_screen, text="Successfully Printed", fg='green')

    # Clock
    thr = Thread(target=clock, args=(main_screen, ))
    thr.start()
    # Thread(target=replay).start()
    main_screen.mainloop()
    del main_screen


if __name__ == "__main__":
    main_activate()
