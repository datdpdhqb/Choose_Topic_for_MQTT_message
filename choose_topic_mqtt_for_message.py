from time import sleep
import library_mqtt as mqtt
import tkinter
from tkinter import ttk

class MyDelegate(object):

    def print_message(self, message):
        print("Message received:", message)
def loop1():
    #sleep(10)
    root = tkinter.Tk()
    root.title("Thể thao")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    msg_entry = ttk.Entry(main_frame, width=40)
    msg_entry.grid(row=1, column=0)

    msg_button = ttk.Button(main_frame, text="Gửi")
    msg_button.grid(row=1, column=1)
    msg_button['command'] = lambda: send_message(mqtt_client, msg_entry)
    root.bind('<Return>', lambda event: send_message(mqtt_client, msg_entry))

    q_button = ttk.Button(main_frame, text="Thoát")
    q_button.grid(row=1, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    my_delegate = MyDelegate()
    mqtt_client = mqtt.MqttClient(my_delegate)
    mqtt_client.connect("thethao", "thethao", "test.mosquitto.org")
    root.mainloop()
def loop2():
    #sleep(10)
    root = tkinter.Tk()
    root.title("Âm nhạc")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    msg_entry = ttk.Entry(main_frame, width=40)
    msg_entry.grid(row=1, column=0)

    msg_button = ttk.Button(main_frame, text="Gửi")
    msg_button.grid(row=1, column=1)
    msg_button['command'] = lambda: send_message(mqtt_client, msg_entry)
    root.bind('<Return>', lambda event: send_message(mqtt_client, msg_entry))

    q_button = ttk.Button(main_frame, text="Thoát")
    q_button.grid(row=1, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    my_delegate = MyDelegate()
    mqtt_client = mqtt.MqttClient(my_delegate)
    mqtt_client.connect("amnhac", "amnhac", "test.mosquitto.org")
    root.mainloop()
def loop3():
    #sleep(10)
    root = tkinter.Tk()
    root.title("Giải trí")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    msg_entry = ttk.Entry(main_frame, width=40)
    msg_entry.grid(row=1, column=0)

    msg_button = ttk.Button(main_frame, text="Gửi")
    msg_button.grid(row=1, column=1)
    msg_button['command'] = lambda: send_message(mqtt_client, msg_entry)
    root.bind('<Return>', lambda event: send_message(mqtt_client, msg_entry))

    q_button = ttk.Button(main_frame, text="Thoát")
    q_button.grid(row=1, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    my_delegate = MyDelegate()
    mqtt_client = mqtt.MqttClient(my_delegate)
    mqtt_client.connect("Giaitri", "Giaitri", "test.mosquitto.org")
    root.mainloop()
def loop4():
    #sleep(10)
    root = tkinter.Tk()
    root.title("Thời sự")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    msg_entry = ttk.Entry(main_frame, width=40)
    msg_entry.grid(row=1, column=0)

    msg_button = ttk.Button(main_frame, text="Gửi")
    msg_button.grid(row=1, column=1)
    msg_button['command'] = lambda: send_message(mqtt_client, msg_entry)
    root.bind('<Return>', lambda event: send_message(mqtt_client, msg_entry))

    q_button = ttk.Button(main_frame, text="Thoát")
    q_button.grid(row=1, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    my_delegate = MyDelegate()
    mqtt_client = mqtt.MqttClient(my_delegate)
    mqtt_client.connect("thoisu", "thoisu", "test.mosquitto.org")
    root.mainloop()
def loop5():
    #sleep(10)
    root = tkinter.Tk()
    root.title("")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    msg_entry = ttk.Entry(main_frame, width=40)
    msg_entry.grid(row=1, column=0)

    msg_button = ttk.Button(main_frame, text="Gửi")
    msg_button.grid(row=1, column=1)
    msg_button['command'] = lambda: send_message(mqtt_client, msg_entry)
    root.bind('<Return>', lambda event: send_message(mqtt_client, msg_entry))

    q_button = ttk.Button(main_frame, text="Thoát")
    q_button.grid(row=1, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client))

    nhap=input("Tùy chọn topic:")
    my_delegate = MyDelegate()
    mqtt_client = mqtt.MqttClient(my_delegate)
    mqtt_client.connect(nhap,nhap, "test.mosquitto.org")
    root.mainloop()

def send_message(mqtt_client, msg_entry):
    msg = msg_entry.get()
    msg_entry.delete(0, 'end')
    mqtt_client.send_message("print_message",[msg])

def quit_program(mqtt_client):
    mqtt_client.close()
    print("Ngắt kết nối!!!")
    exit()

bot=int(input("Chọn chủ đề bạn muốn nhắn tin?\n1 - Thể thao\n2 - Âm nhạc\n3 - Giải trí\n4 - Thời sự\n5 - Tùy chọn\n"))
if bot==1:
    loop1()
elif bot==2:
    loop2()
elif bot==3:
    loop3()
elif bot==4:
    loop4()
elif bot==5:
    loop5()
else:
    print("You can insert just 1,2,3,4 or 5")

