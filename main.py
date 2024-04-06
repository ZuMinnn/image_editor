# app sử dụng thư viện tkinter làm giao diện: pip install tk
# app sử dụng thư viện PIl (gói pillow) để xử lí ảnh: pip install pillow 
# from mvu with luv <3

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageEnhance

class ImageEditorUI:
    # Khởi tạo ứng dụng
    def __init__(self, master):
        self.master = master
        self.master.title('Image Editor - Advanced UI')
        self.master.geometry('900x700')
        self.master.configure(bg='#2C3E50')  # Thiết lập màu nền
        
# Lưu giá trị mặc định của các bộ lọc
        self.default_brightness = 1.0
        self.default_contrast = 1.0
        self.default_saturation = 1.0
        
        self.original_image = None
        self.processed_image = None
        self.img_display = None

        # Tạo các widget (nút, thanh trượt, v.v.)
        self.create_widgets()

    # Tạo các widget
    def create_widgets(self):
        # Tạo header và footer
        self.create_header_footer()
        # Tạo khu vực hiển thị ảnh
        self.create_image_display()
        # Tạo các nút điều khiển
        self.create_controls()

    # Tạo header và footer
    def create_header_footer(self):
        header_frame = tk.Frame(self.master, bg='#34495E', height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        # Tiêu đề ứng dụng
        title_label = tk.Label(header_frame, text='Image Editor', font=('Arial', 24, 'bold'), bg='#34495E', fg='white')
        title_label.place(relx=0.5, rely=0.5, anchor='center')

        # Footer chứa các thanh trượt điều chỉnh
        footer_frame = tk.Frame(self.master, bg='#34495E', height=120)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))

        # Tạo thanh trượt điều chỉnh độ sáng, độ tương phản và độ bão hòa
        self.brightness_slider = self.create_slider(footer_frame, "Brightness", 0.0, 2.0, 1.0, self.adjust_brightness)
        self.contrast_slider = self.create_slider(footer_frame, "Contrast", 0.0, 2.0, 1.0, self.adjust_contrast)
        self.saturation_slider = self.create_slider(footer_frame, "Saturation", 0.0, 2.0, 1.0, self.adjust_saturation)

    # Tạo một thanh trượt
    def create_slider(self, parent, label, from_, to, initial, command):
        frame = tk.Frame(parent, bg='#34495E')
        frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        tk.Label(frame, text=label, bg='#34495E', fg='white').pack()
        slider = tk.Scale(frame, from_=from_, to=to, resolution=0.1, orient=tk.HORIZONTAL, command=command, bg='#16A085', fg='white', troughcolor='#34495E')
        slider.set(initial)
        slider.pack(fill=tk.X, padx=5)
        return slider

    # Tạo khu vực hiển thị ảnh
    def create_image_display(self):
        self.main_frame = tk.Frame(self.master, bg='#2C3E50')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(self.main_frame, text='No Image Loaded', bg='#2C3E50', fg='#95A5A6', font=('Arial', 20))
        self.image_label.pack(pady=20, expand=True)

    # Tạo các nút điều khiển
    def create_controls(self):
        controls_frame = tk.Frame(self.master, bg='#34495E', height=50)
        controls_frame.pack(fill=tk.X, side=tk.BOTTOM, before=self.main_frame)

        # Nút mở ảnh
        open_button = tk.Button(controls_frame, text='Open Image', command=self.open_image, font=('Arial', 12), bg='#16A085', fg='white')
        open_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Nút lưu ảnh
        save_button = tk.Button(controls_frame, text='Save Image', command=self.save_image, font=('Arial', 12), bg='#E67E22', fg='white')
        save_button.pack(side=tk.LEFT, padx=10)

    # Mở ảnh
    def open_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.processed_image = self.original_image.copy()
            self.show_image(self.processed_image)

    # Lưu ảnh
    def save_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg;*.jpeg"),
                                                                ("All files", "*.*")])
            if file_path:
                self.processed_image.save(file_path)
        else:
            messagebox.showinfo("Error", "No image to save.")
    # Hiển thị ảnh
    def show_image(self, img):
        img.thumbnail((self.main_frame.winfo_width(), self.main_frame.winfo_height()))
        self.imgtk = ImageTk.PhotoImage(image=img)
        self.image_label.config(image=self.imgtk)
        self.image_label.image = self.imgtk  # Giữ tham chiếu

    # Điều chỉnh độ sáng
    def adjust_brightness(self, value):
        self.apply_adjustment(ImageEnhance.Brightness, float(value))

    # Điều chỉnh độ tương phản
    def adjust_contrast(self, value):
        self.apply_adjustment(ImageEnhance.Contrast, float(value))

    # Điều chỉnh độ bão hòa màu
    def adjust_saturation(self, value):
        self.apply_adjustment(ImageEnhance.Color, float(value))

    # Áp dụng điều chỉnh lên ảnh
    def apply_adjustment(self, enhancer_class, value):
        if self.original_image:
            enhancer = enhancer_class(self.original_image)
            self.processed_image = enhancer.enhance(value)
            self.show_image(self.processed_image)


    def create_controls(self):
        controls_frame = tk.Frame(self.master, bg='#34495E', height=50)
        controls_frame.pack(fill=tk.X, side=tk.BOTTOM, before=self.main_frame)

        open_button = tk.Button(controls_frame, text='Open Image', command=self.open_image, font=('Arial', 12), bg='#16A085', fg='white')
        open_button.pack(side=tk.LEFT, padx=10, pady=10)

        save_button = tk.Button(controls_frame, text='Save Image', command=self.save_image, font=('Arial', 12), bg='#E67E22', fg='white')
        save_button.pack(side=tk.LEFT, padx=10)

        # Các nút cho xoay và lật ảnh
        rotate_button = tk.Button(controls_frame, text='Rotate', command=self.rotate_image, font=('Arial', 12), bg='#3498DB', fg='white')
        rotate_button.pack(side=tk.LEFT, padx=10)

        flip_left_button = tk.Button(controls_frame, text='Flip Right/Left', command=lambda: self.flip_image('left'), font=('Arial', 12), bg='#9B59B6', fg='white')
        flip_left_button.pack(side=tk.LEFT, padx=10)

        flip_right_button = tk.Button(controls_frame, text='Flip Up/Down', command=lambda: self.flip_image('right'), font=('Arial', 12), bg='#9B59B6', fg='white')
        flip_right_button.pack(side=tk.LEFT, padx=10)
        
        reset_button = tk.Button(controls_frame, text='Reset', command=self.reset_image, font=('Arial', 12), bg='#2ECC71', fg='white')
        reset_button.pack(side=tk.LEFT, padx=10)


    def rotate_image(self):
        # Xoay ảnh
        if self.processed_image:
            self.processed_image = self.processed_image.rotate(-90, expand=True)
            self.show_image(self.processed_image)
        else:
            messagebox.showinfo("Error", "No image loaded.")

    def flip_image(self, direction):
        # Lật ảnh
        if self.processed_image:
            if direction == 'left':
                self.processed_image = self.processed_image.transpose(Image.FLIP_LEFT_RIGHT)
            elif direction == 'right':
                self.processed_image = self.processed_image.transpose(Image.FLIP_TOP_BOTTOM)
            self.show_image(self.processed_image)
        else:
            messagebox.showinfo("Error", "No image loaded.")
   
   # đưa ảnh cùng giá trị các bộ lọc về giá trị ban đầu
    def reset_image(self):
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.show_image(self.processed_image)
            # Đặt lại các thanh trượt về giá trị mặc định
            self.brightness_slider.set(self.default_brightness)
            self.contrast_slider.set(self.default_contrast)
            self.saturation_slider.set(self.default_saturation)
        else:
            messagebox.showinfo("Error", "No original image to reset to.")

        
#hàm
if __name__ == '__main__':
    root = tk.Tk()
    app = ImageEditorUI(root)
    root.mainloop()
