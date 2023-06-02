import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import numpy as np
from keras.models import load_model

#Đường dẫn tới file h5 đã huấn luyện
model_path = 'kidneynew.h5'

#Load model
model = load_model(model_path)
class_members = ['Cyst', 'Normal', 'Stone', 'Tumor','Unknown']

def predict_member(image):
    # Chuẩn bị dữ liệu để dự đoán
    face_image = cv2.resize(image, (40, 30))
    face_image = np.expand_dims(face_image, axis=0)
    face_image = face_image / 255.0

    # Dự đoán class label
    predictions = model.predict(face_image)
    confidence  = np.max(predictions)
    if confidence > 0.8:
        predicted_class_label = class_members[np.argmax(predictions)]
    else:
        predicted_class_label = 'Unknown'

    return predicted_class_label
def draw_text(image, text, position):
    # Thiết lập font, kích thước và màu sắc
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 255, 0) # Màu trắng
    thickness = 2
    # Vẽ văn bản lên hình ảnh
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

def capture_and_predict():
    # Chụp ảnh từ camera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    # Hiển thị khung hình trong cửa sổ
    cv2.imshow("Capture Face", frame)
    image_path = None  # Khởi tạo biến image_path

    while True:
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Lưu ảnh vào đường dẫn đã chỉ định
            image_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            cv2.imwrite(image_path, frame)
            break

        # Tiếp tục đọc khung hình mới
        ret, frame = cap.read()
        cv2.imshow("Capture Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Đóng cửa sổ "Capture Face"
    cv2.destroyWindow("Capture Face")

    if image_path:
        # Hiển thị ảnh chụp
        img = Image.open(image_path)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        label_image.configure(image=img)
        label_image.image = img

        # Dự đoán bệnh trong ảnh
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        predicted_member = predict_member(image)

        # Vẽ tên bệnh lên hình ảnh
        draw_text(frame, predicted_member, (50, 50))
        label_result.configure(text=f"Kết quả dự đoán: {predicted_member}")
        # Hiển thị ảnh chụp và vẽ tên thành viên
        cv2.imshow("Captured Image", frame)
    # Đóng kết nối camera
    cap.release()

def select_image():
    # Chọn hình ảnh từ file dialog
    image_path = filedialog.askopenfilename(filetypes=[("Image files", ".jpg;.jpeg;*.png")])

    if image_path:
        # Đọc hình ảnh và dự đoán bệnh
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        predicted_member = predict_member(image)
        # Kiểm tra kích thước của hình ảnh
        height, width, _ = image.shape
        if width > 1366 and height > 768:
            # Resize hình ảnh thành kích thước mới
            image = cv2.resize(image, (800, 600))

        # Hiển thị hình ảnh đã chọn
        img = Image.fromarray(image)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        label_image.configure(image=img)
        label_image.image = img
        predicted_member = predict_member(image)

        # Vẽ tên bệnh lên hình ảnh
        draw_text(image, predicted_member, (50, 50))

        # Hiển thị hình ảnh với tên bệnh 
        cv2.imshow("Selected Image", image)
        label_result.configure(text=f"Kết quả dự đoán: {predicted_member}")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def details_button_clicked():
    # Lấy tên bệnh được dự đoán
    predicted_disease = label_result.cget("text").split(": ")[-1]
    # Đường dẫn đến tệp tin văn bản chứa chi tiết bệnh
    details_file_path = f'{predicted_disease.lower()}.txt'

    try:
        # Mở tệp tin văn bản và đọc nội dung với mã hóa utf-8
        with open(details_file_path, "r", encoding="utf-8") as file:
            details_content = file.read()
        # Tạo cửa sổ mới để hiển thị chi tiết
        details_window = tk.Toplevel()
        details_window.title("Chi tiết bệnh")
        details_window.geometry("1700x500")

        # Hiển thị nội dung chi tiết trong cửa sổ
        details_label = tk.Label(details_window, text=details_content, font=("bold", 8), justify=tk.LEFT)
        details_label.place(x=20, y=20)
    except FileNotFoundError:
        # Tạo cửa sổ mới để hiển thị chi tiết
        details_window = tk.Toplevel()
        details_window.title("Chi tiết bệnh")
        details_window.geometry("1700x500")
        # Xử lý trường hợp không tìm thấy tệp tin
        error_message = 'Không xác định được loại bệnh '
        error_label = tk.Label(details_window, text=error_message, font=("bold", 12))
        error_label.place(x=20, y=20)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Tạo GUI
root = tk.Tk()
root.title("DETECTING KIDNEY STONES")
root.geometry("600x500")

#Tạo nút Chụp ảnh và dự đoán
btn_capture = tk.Button(root, text="Capture and Predict", command=capture_and_predict, width=18, height=2, bg="blue", fg="white")
btn_capture.place(x=40, y=100) # Tùy chỉnh vị trí của nút

#Tạo nút Chọn hình ảnh
btn_select = tk.Button(root, text="Select Image", command=select_image, width=18, height=2, bg="blue", fg="white")
btn_select.place(x=40, y=200) # Tùy chỉnh vị trí của nút

#Tạo nút "Chi tiết"
details_button = tk.Button(root, text="Chi tiết", command=details_button_clicked, width=12, height=2, bg="blue", fg="white")
details_button.place(x=400, y=410)

#Hiển thị ảnh
label_image = tk.Label(root)
label_image.place(x=200, y=100)

#Kết quả dự đoán
label_result = tk.Label(root, text="Kết quả dự đoán:", font=("Helvetica", 16, "bold"))
label_result.place(x=200, y=50)

#một số nguyên nhân bệnh 
details_label = tk.Label(root, text="Các nguyên nhân:", font=("Helvetica", 16, "bold"))
details_label.place(x=200, y=415)

root.mainloop()