# import webbrowser
import os
from tkinter import filedialog
from tkinter import *
from defs import *
import pandas as pd
import ntpath
global password
global err
global frame
global dir_label
global admin_app

font_size = 15
dir_path = os.getcwd()
xl_file_name = 'Statistics'
global machines_lst
global machines
u_type = 0
global back_to_app
global main_screen

def path_leaf(path):
    head, tail = ntpath.split(path)
    ret = tail or ntpath.basename(head)
    return ret.split('.')[0]


def admin_screen(reset_registers, file_path, user_type, main_activate, m_lst, m_info, m_s):
    global main_screen
    global machines_lst
    global machines
    global back_to_app
    global err
    global admin_app
    global u_type
    global xl_file_name
    global dir_path

    main_screen = m_s
    dir_path = os.path.split(file_path)[0]
    machines_lst = m_lst
    machines = m_info
    back_to_app = main_activate
    u_type = user_type
    xl_file_name = path_leaf(file_path)
    admin_app = Tk()
    admin_app.geometry('650x250')
    admin_app.title('Admin')
    admin_app.grid()

    def check_pw():
        if admin_pw.get() == '123':
            label.grid_forget()
            e1.grid_forget()
            ok_button.grid_forget()
            cancel_button.grid_forget()
            admin_set_settings(reset_registers)
        else:
            err.grid(row=2, column=1, sticky=EW)
            admin_app.after(2000, forget, err)
            admin_pw.set('')

    def des():
        main_screen.destroy()
        admin_app.after(len(machines_lst) * 2000, admin_app.destroy)
        back_to_app()

    admin_pw = StringVar(admin_app)
    label = Label(admin_app, text="Insert password", font=(font_of_container, font_size))
    label.grid(row=0, column=0, sticky=W)
    e1 = Entry(admin_app, textvariable=admin_pw, show='*', font=(font_of_container, font_size))
    e1.grid(row=0, column=1, sticky=E)
    fr = Frame(admin_app)
    fr.grid(row=1, column=1, sticky=EW, padx=50)
    ok_button = Button(fr, text='אישור', command=check_pw, font=(font_of_container, font_size))
    ok_button.grid(row=0, column=0, padx=1)
    cancel_button = Button(fr, text='ביטול', command=des, font=(font_of_container, font_size))
    cancel_button.grid(row=0, column=1, padx=1)
    err = Label(admin_app, text="Wrong Password", fg='red', font=(font_of_container, font_size))
    admin_app.mainloop()


def change_dir(path):
    file_exists = os.path.exists(path)
    if not file_exists:
        wr = pd.ExcelWriter(path)
        df = pd.DataFrame({
            'Date': [],
            'Time': [],
            'Machine Hour': [],
            'Count': []
        })
        for name in machines:
            df.to_excel(excel_writer=wr, index=False, sheet_name=name[1])
        wr.close()


def select_folder():
    global dir_path
    dir_path = filedialog.askdirectory()
    dir_label.config(text=dir_path)


# def set_machines():
#     if os.path.exists('machines.txt.txt'):
#         os.remove('machines.txt.txt')
#     machines_f = open('machines.txt', 'w', encoding='utf=8')
#     machines_f.write(machines)

def forget(label):
    label.grid_forget()


def admin_set_settings(reset_registers):
    global admin_app
    global dir_label

    def update_dir():
        path = os.path.join(dir_path, f_name.get() + '.xlsx')
        change_dir(path)
        # th = Thread(target=waiting_screen, args=(path, print_to_excel_flag))
        # th.start()

        defsh = """{}
{}""".format(path.replace('\\', '\\\\'), var.get())
        if os.path.exists('path.txt'):
            os.remove('path.txt')
        f = open('path.txt', 'w', encoding='utf-8')
        f.write(defsh)
        f.close()

    def func():
        main_screen.destroy()
        lb.grid(row=6, sticky=W, column=0)
        update_dir()
        admin_app.after(len(machines_lst) * 2000, admin_app.destroy)
        back_to_app()

    Label(admin_app, text='מנהל תפ"י', font=(font_of_container, title_font_size-5, "bold")).\
        grid(row=0, column=0, sticky=EW, columnspan=5)

    f_name = StringVar(admin_app, value=xl_file_name, name='file_name')
    # print_to_excel_flag = BooleanVar(admin_app)
    fr = Frame(admin_app)
    fr.grid(row=1, sticky=W, columnspan=4)
    Label(fr, text="Insert file name", font=(font_of_container, font_size)).grid(row=0, column=0, sticky=W)
    e1 = Entry(fr, textvariable=f_name, font=(font_of_container, font_size)).grid(row=0, column=1, sticky=W, padx=5)
    Button(fr, text="OK", font=(font_of_container, font_size), command=update_dir)\
        .grid(row=0, column=2, sticky=W)
    Button(admin_app, text="Choose Directory", font=(font_of_container, font_size), command=select_folder)\
        .grid(row=2, column=0, sticky=W)
    dir_label = Label(admin_app, text=dir_path, font=(font_of_container, font_size-5))
    dir_label.grid(row=2, column=1)
    # c1 = Checkbutton(admin_app, text='print stats', variable=print_to_excel_flag, onvalue=True,
    #                  offvalue=False, font=(font_of_container, font_size))
    # c1.grid(row=3, sticky=W)
    radio_buttons = Frame(admin_app)
    radio_buttons.grid(row=3, sticky=W)
    var = IntVar(admin_app, value=u_type)

    fr = Frame(admin_app)
    fr.grid(row=4, column=0, sticky=W, pady=2, columnspan=5)
    shift_lbl = Label(fr, text='reset machine: ', font=(font_of_container, font_size))
    shift_lbl.grid(row=0, column=0, sticky=W, padx=3)
    column_change = 1
    for ma in machines:
        # Reset registers
        bt = Button(fr, text=ma[1], command=lambda x=ma[0]: reset_registers(x), font=(font_of_container, font_size))
        bt.grid(row=0, column=column_change, sticky=W, pady=2, padx=1)
        column_change += 1

    c2 = Checkbutton(admin_app, text='החלפת משמרת אוטומטית 7:00, 19:00', variable=var, onvalue=1,
                     offvalue=0, font=(font_of_container, font_size))
    c2.grid(row=5, sticky=W, pady=2, columnspan=3)

    lb = Label(admin_app, text="Loading machines", fg='green', font=(font_of_container, font_size))
    Button(admin_app, text='אישור', command=func, font=(font_of_container, font_size))\
        .grid(row=6, sticky=W, column=1, padx=60, pady=3)
    admin_app.mainloop()


# def main():
#     global frame
#     global password
#     global err
#     global started_screen
#     started_screen = Tk()
#     started_screen.title('Options')
#     started_screen.grid()
#     Label(started_screen, text="Choose option", font=('Courier', 20)).grid(sticky=EW)
#     frame = Frame(started_screen)
#     frame.grid()
#     Button(frame, text="Set Settings", command=check_pw).grid(row=1, column=0, sticky=W)
#     Button(frame, text="App", command=waiting_screen).grid(row=2, column=0, sticky=W)
#     password = StringVar(frame)
#     Entry(frame, textvariable=password, show='*').grid(row=1, column=1, sticky=W)
#     err = Label(frame, text="Wrong Password", fg='red')
#     started_screen.mainloop()

#
# if __name__ == "__main__":
#     main()




# def waiting_screen():
#     started_screen.destroy()
#     waiting_screed = Tk()
#     waiting_screed.title("waiting for server")
#     waiting_screed.grid()
#
#     pb = ttk.Progressbar(
#         waiting_screed,
#         orient='horizontal',
#         mode='indeterminate',
#         length=280
#     )
#     # place the progressbar
#     pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)
#     pb.start()
#
#     def des_lambda():
#         pb.destroy()
#         waiting_screed.destroy()
#
#     waiting_screed.after(3000 * len(machines), func=des_lambda)
#     waiting_screed.mainloop()
#     main_activate()
#     # webbrowser.open_new("http://127.0.0.1:8040")
