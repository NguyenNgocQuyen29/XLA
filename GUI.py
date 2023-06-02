import tkinter as tk
import subprocess
from PIL import Image, ImageTk

#Đường dẫn đến chương trình python
python_file_path = "demo111.py"

# Tạo GUI
root = tk.Tk()
root.title("Ảnh Bìa")

# Tạo hình nền cho cửa sổ
anhnen_path="anhbiaxla.jpg"
anhnen=Image.open(anhnen_path)
image = ImageTk.PhotoImage(anhnen)
label = tk.Label(root, image=image)
label.pack()

#Lệnh chạy chương trình python 
def runpython():
    subprocess.run(["python", python_file_path])

# Tạo nút "Start"
start_button = tk.Button(root, text="START",command=runpython, width=12, height=3, bg="#FFC0CB", font=("Helvetica", 12, "bold"))
start_button.place(relx=0.5, rely=0.94, anchor="center")

#Hiển thị cửa sổ giao diện
root.mainloop()