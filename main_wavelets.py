import os
import sys
import datetime
import time

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
import cv2
import numpy as np
import ctypes
import matplotlib.pyplot as plt
import math

image_path = ""
folder_path = ""
data = []
num_scale = 0
rows, cols = 0, 0
scales = []
result = []
points_max_by_row = []
points_min_by_row = []
points_max_by_column = []
points_min_by_column = []
extremum_row_min_array = []
extremum_row_max_array = []
extremum_col_min_array = []
extremum_col_max_array = []


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("950x750")
        self.title("Wavelets and other")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)
        self.label_load = ctk.CTkLabel(self, text="Загрузить изображение")
        self.label_load.grid(row=0, column=0, padx=20, sticky="w")
        self.label_load.configure(font=ctk.CTkFont(size=14, weight="bold"))
        self.load_button = ctk.CTkButton(self, text="Загрузить",
                                         command=self.load_image_callback)
        self.load_button.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.print_load_image = ctk.CTkLabel(self, text="")
        self.print_load_image.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.label_col_channel = ctk.CTkLabel(self, text="Выберите канал изображения")
        self.label_col_channel.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.label_col_channel.configure(font=ctk.CTkFont(size=14, weight="bold"))
        self.radio_var = tk.IntVar(value=0)
        self.red_rbut = ctk.CTkRadioButton(self, text="Red channel", command=lambda: self.radiobutton_event(1),
                                           variable=self.radio_var, value=1)
        self.red_rbut.grid(row=4, column=0, sticky="w", padx=20, pady=5)
        self.blue_rbut = ctk.CTkRadioButton(self, text="Blue channel", command=lambda: self.radiobutton_event(2),
                                            variable=self.radio_var, value=2)
        self.blue_rbut.grid(row=5, column=0, sticky="w", padx=20, pady=5)
        self.green_rbut = ctk.CTkRadioButton(self, text="Green channel", command=lambda: self.radiobutton_event(3),
                                             variable=self.radio_var, value=3)
        self.green_rbut.grid(row=6, column=0, sticky="w", padx=20, pady=5)
        self.grayscale_rbut = ctk.CTkRadioButton(self, text="Gray channel", command=lambda: self.radiobutton_event(4),
                                                 variable=self.radio_var, value=4)
        self.grayscale_rbut.grid(row=7, column=0, sticky="w", padx=20, pady=5)
        self.data = tk.StringVar()

        self.label_scales = ctk.CTkLabel(self, text="Масштабы")
        self.label_scales.configure(font=ctk.CTkFont(size=16, weight="bold"))
        self.label_scales.grid(row=8, column=0, sticky="w", padx=15, pady=10)
        self.label_start = ctk.CTkLabel(self, text="От:")
        self.label_start.grid(row=9, column=0, padx=15, sticky="w")
        self.entry_start = ctk.CTkEntry(self)
        self.entry_start.grid(row=9, column=0, padx=45, sticky="w")
        self.label_end = ctk.CTkLabel(self, text="До:")
        self.label_end.grid(row=10, column=0, padx=15, sticky="w")
        self.entry_end = ctk.CTkEntry(self)
        self.entry_end.grid(row=10, column=0, padx=45, sticky="w")
        self.label_step = ctk.CTkLabel(self, text="Шаг:")
        self.label_step.grid(row=11, column=0, padx=15, sticky="w")
        self.entry_step = ctk.CTkEntry(self)
        self.entry_step.grid(row=11, column=0, padx=45, sticky="w")
        self.button_save_scales = ctk.CTkButton(self, text="Сохранить значения", command=self.load_scales)
        self.button_save_scales.grid(row=12, column=0, padx=45, sticky="w")

        self.label_custom_scale = ctk.CTkLabel(self, text="")
        self.label_custom_scale.grid(row=14, column=0, sticky="w")
        self.button_load_scales_file = ctk.CTkButton(self, text="Загрузить из файла",
                                                     command=self.load_scales_from_file)
        self.button_load_scales_file.grid(row=13, column=0, padx=45, pady=10, sticky="w")

        self.label_t_extr = ctk.CTkLabel(self, text="Точки экстремумов:")
        self.label_t_extr.grid(row=15, column=0, padx=20, pady=10, sticky="w")
        self.label_t_extr.configure(font=ctk.CTkFont(size=16, weight="bold"))

        self.row_var = tk.BooleanVar(value=True)
        self.col_var = tk.BooleanVar(value=True)
        self.max_var = tk.BooleanVar(value=True)
        self.min_var = tk.BooleanVar(value=True)

        self.row_checkbox = ctk.CTkCheckBox(self, text="По строкам", variable=self.row_var, onvalue=True,
                                            offvalue=False)
        self.row_checkbox.grid(row=16, column=0, padx=20, sticky="w")
        self.col_checkbox = ctk.CTkCheckBox(self, text="По столбцам", variable=self.col_var, onvalue=True,
                                            offvalue=False)
        self.col_checkbox.grid(row=17, column=0, padx=20, sticky="w")
        self.max_checkbox = ctk.CTkCheckBox(self, text="Максимум", variable=self.max_var, onvalue=True, offvalue=False)
        self.max_checkbox.grid(row=16, column=1, padx=20, sticky="w")
        self.min_checkbox = ctk.CTkCheckBox(self, text="Минимум", variable=self.min_var, onvalue=True, offvalue=False)
        self.min_checkbox.grid(row=17, column=1, padx=20, sticky="w")

        self.num_near_point = ctk.CTkLabel(self, text="Введите количество ближайших точек")
        self.num_near_point.grid(row=18, column=0, padx=20, pady=10, sticky="w")
        self.entry_var = tk.StringVar()
        self.entry_var.set("n (ex. 5)")
        self.entry_near_point = ctk.CTkEntry(self, textvariable=self.entry_var)
        self.entry_near_point.grid(row=18, column=1, sticky="w")
        self.entry_near_point.configure(text_color="gray")
        self.entry_near_point.bind("<Button-1>", self.on_entry_click)

        # output gui
        self.output_label = ctk.CTkLabel(self, text="Выберите варианты вывода вычислений")
        self.output_label.configure(font=ctk.CTkFont(size=16, weight="bold"))
        self.output_label.grid(row=0, column=3, padx=20, sticky="w")

        self.wp_var1 = tk.BooleanVar(value=True)
        self.wp_var2 = tk.BooleanVar(value=True)
        self.p_ex_var1 = tk.BooleanVar(value=True)
        self.p_ex_var2 = tk.BooleanVar(value=True)
        self.dist_angle_var = tk.BooleanVar(value=True)

        self.wp_label = ctk.CTkLabel(self, text="1) Вейвлет преобразование (Морле)")
        self.wp_label.grid(row=1, column=3, padx=20, sticky="w")
        self.wp1_checkbox = ctk.CTkCheckBox(self, text="В виде .txt файла (по 1 .txt на каждый масштаб)",
                                            variable=self.wp_var1)
        self.wp1_checkbox.grid(row=2, column=3, padx=40, sticky="w")
        self.wp2_checkbox = ctk.CTkCheckBox(self, text="В виде изображений (по 1 .jpg на каждый масштаб)",
                                            variable=self.wp_var2)
        self.wp2_checkbox.grid(row=3, column=3, padx=40, sticky="w")

        self.p_ex_label = ctk.CTkLabel(self, text="2) Точки экстремума:")
        self.p_ex_label.grid(row=4, column=3, padx=20, sticky="w")
        self.p_ex1_checkbox = ctk.CTkCheckBox(self, text="В виде .txt файла (по 1 .txt на каждый масштаб)",
                                              variable=self.p_ex_var1)
        self.p_ex1_checkbox.grid(row=5, column=3, padx=40, sticky="w")
        self.p_ex2_checkbox = ctk.CTkCheckBox(self, text="В виде изображений (по 1 .jpg на каждый масштаб)",
                                              variable=self.p_ex_var2)
        self.p_ex2_checkbox.grid(row=6, column=3, padx=40, sticky="w")

        self.dist_angle_label = ctk.CTkLabel(self, text="3) Алгоритм нахождения расстояний и углов")
        self.dist_angle_label.grid(row=7, column=3, padx=20, sticky="w")
        self.dist_angle_checkbox = ctk.CTkCheckBox(self, text="В виде .txt файла (по 1 .txt на каждый масштаб)",
                                                   variable=self.dist_angle_var)
        self.dist_angle_checkbox.grid(row=8, column=3, padx=40, sticky="w")

        self.app_start_button = ctk.CTkButton(self, text="Вычислить", command=self.compute)
        self.app_start_button.grid(row=16, column=3, sticky="s")
        self.app_start_button.configure(width=200, height=50, border_width=3, border_color="black")

    def load_image_callback(self):
        global image_path
        filetypes = (
            ("Image files", "*.img *.jpeg *.jpg *.png"),
            ("All files", "*.*")
        )
        filename = tk.filedialog.askopenfilename(
            title="Open an image file",
            initialdir="/",
            filetypes=filetypes)

        if filename:
            image_path = f"{filename}"
            print('Selected image file:', image_path)
            self.load_button.configure(text="Загружено", text_color="black", fg_color="white", border_color="black",
                                       border_width=2)
            text = "Выбранный файл:\n" + image_path
            self.print_load_image.configure(text=text)
        else:
            print('No file selected')
            self.load_button.configure(text="Ошибка", fg_color="red")
            self.print_load_image.configure(text="No file selected")

    def radiobutton_event(self, selected_value):
        for widget in [self.red_rbut, self.blue_rbut, self.green_rbut, self.grayscale_rbut]:
            if widget.cget('value') != str(selected_value):
                widget.configure(state='disabled')

        radio_var = self.radio_var.get()

        global image_path
        image = cv2.imread(image_path)
        b, g, r = cv2.split(image)
        global data
        if radio_var == 1:
            data = r
        elif radio_var == 2:
            data = b
        elif radio_var == 3:
            data = g
        elif radio_var == 4:
            data = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print("current value:", self.radio_var.get())

    def load_scales(self):
        start = int(self.entry_start.get())
        end = int(self.entry_end.get())
        step = int(self.entry_step.get())
        global scales, num_scale
        scales = np.arange(start=start, stop=end + 1, step=step, dtype=np.double)
        num_scale = scales.shape[0]
        self.button_save_scales.configure(text="Сохранено", text_color="black", fg_color="white", border_color="black",
                                          border_width=2)
        self.button_load_scales_file.configure(state='disabled')

    def load_scales_from_file(self):
        self.entry_start.configure(state='disabled')
        self.entry_step.configure(state='disabled')
        self.entry_end.configure(state='disabled')
        filetypes = (
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        filename = tk.filedialog.askopenfilename(
            title='Open an image file',
            initialdir='/',
            filetypes=filetypes)
        global scales
        with open(filename, 'r') as f:
            for line in f:
                numbers = [np.double(x) for x in line.split()]
                scales = np.append(scales, numbers)
        scales = np.array(scales, dtype=np.double)

        global num_scale
        num_scale = len(scales)
        if num_scale <= 7:
            self.label_custom_scale.configure(text=str(scales))

        self.button_load_scales_file.configure(text="Загружено", text_color="black", fg_color="white",
                                               border_color="black", border_width=2)
        self.button_save_scales.configure(text="Сохранено", text_color="black", fg_color="white", border_color="black",
                                          border_width=2)
            
        f.close()

    def on_entry_click(self, event):
        self.entry_near_point.delete(0, ctk.END)

    @staticmethod
    def create_scale_folder(scale):
        global folder_path
        scale_folder_path = os.path.join(folder_path, f"Масштаб_{scale}")
        os.makedirs(scale_folder_path, exist_ok=True)
        return scale_folder_path

    def compute_wavelets(self, info_out):
        global num_scale, rows, cols, data, scales, result
        t_compute_wavelet_start = time.time()
        lib = ctypes.CDLL("./dll_wavelets.dll")
        lib.morlet_wavelet.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                                       ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

        data = np.array(data, dtype=np.double)
        rows = data.shape[0]
        cols = data.shape[1]

        # Выделение памяти для результата
        result_shape = (num_scale, rows, cols)
        result = np.empty(result_shape, dtype=np.double)

        print(f"num_scale: {num_scale}")
        print(f"rows: {rows}")
        print(f"cols: {cols}")
        print(f"data: {data}")
        print(f"scales: {scales}")
        lib.morlet_wavelet(num_scale, rows, cols, data.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                           scales.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                           result.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

        if info_out == 0:
            for scale in range(num_scale):
                scale_folder_path = self.create_scale_folder(scales[scale])

                filename = f"Рассчет_вейвлетов_Масштаб_{scales[scale]}.txt"
                array_2d = result[scale]
                file_path = os.path.join(scale_folder_path, filename)
                np.savetxt(file_path, array_2d, delimiter=",")
                print(f"Сохранено в файл: {file_path}")

                plt.figure()
                plt.imshow(result[scale], cmap='viridis')
                plt.title(f'Wavelets:Scale = {scales[scale]}')
                plt.colorbar()
                image_path = os.path.join(scale_folder_path, f'График_расчетов_В_П_Масштаб_{scales[scale]}.png')
                plt.savefig(image_path)
                plt.close()

        if info_out == 1:
            for scale in range(num_scale):
                scale_folder_path = self.create_scale_folder(scales[scale])
                filename = f"Рассчет_вейвлетов_Масштаб_{scales[scale]}.txt"
                array_2d = result[scale]
                file_path = os.path.join(scale_folder_path, filename)
                np.savetxt(file_path, array_2d, delimiter=",")
                print(f"Сохранено в файл: {file_path}")

        if info_out == 10:
            for scale in range(num_scale):
                scale_folder_path = self.create_scale_folder(scales[scale])
                plt.figure()
                plt.imshow(result[scale], cmap='viridis')
                plt.title(f'Wavelets:Scale = {scales[scale]}')
                plt.colorbar()
                image_path = os.path.join(scale_folder_path, f'График_расчетов_В_П_Масштаб_{scales[scale]}.png')
                plt.savefig(image_path)
                plt.close()

        if info_out == 11:
            mb.showerror("Ошибка", message="Выберите хотя бы один вариант вывода")
            sys.exit(0)
        t_wavelet_end = time.time() - t_compute_wavelet_start
        print('The wavelets have been successfully calculated, the elapsed time:' + str(t_wavelet_end))

    @staticmethod
    def find_max_points_by_rows(coefs):
        for i in range(len(coefs)):
            row = coefs[i]
            max = np.where(row == row.max())
            max = [max[0][0], i]
            points_max_by_row.append(max)
        return points_max_by_row

    @staticmethod
    def find_min_points_by_rows(coefs):
        for i in range(len(coefs)):
            row = coefs[i]
            min = np.where(row == row.min())
            min = [min[0][0], i]
            points_min_by_row.append(min)
        return points_min_by_row

    @staticmethod
    def find_max_points_by_column(coefs):
        for i in range(len(coefs[0])):
            column = coefs[:, i]
            max = np.where(column == column.max())
            max = [i, max[0][0]]
            points_max_by_column.append(max)
        return points_max_by_column

    @staticmethod
    def find_min_points_by_column(coefs):
        for i in range(len(coefs[0])):
            column = coefs[:, i]
            min = np.where(column == column.min())
            min = [i, min[0][0]]
            points_min_by_column.append(min)
        return points_min_by_column

    def find_extremum(self):
        global scales, result, extremum_row_max_array, extremum_row_min_array, folder_path, num_scale
        global extremum_col_min_array, extremum_col_max_array
        if self.row_checkbox.get() is True:
            if (self.max_checkbox.check_state is True) and (self.min_checkbox.check_state is False):
                for scale in range(num_scale):
                    matrix = self.find_max_points_by_rows(result[scale])
                    extremum_row_max_array.append(matrix)
                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is False):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix, '(максимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is False) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_picture(matrix, '(максимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix, '(максимум_по_строкам)', scales[scale], scale_folder_path)
                        self.save_extremum_picture(matrix, '(максимум_по_строкам)', scales[scale], scale_folder_path)

            if (self.max_checkbox.check_state is False) and (self.min_checkbox.check_state is True):
                for scale in range(num_scale):
                    matrix = self.find_min_points_by_rows(result[scale])
                    extremum_row_min_array.append(matrix)
                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is False):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix, '(минимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is False) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_picture(matrix, '(минимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix, '(минимум_по_строкам)', scales[scale], scale_folder_path)
                        self.save_extremum_picture(matrix, '(минимум_по_строкам)', scales[scale], scale_folder_path)

            if (self.max_checkbox.check_state is True) and (self.min_checkbox.check_state is True):
                for scale in range(num_scale):
                    matrix1 = self.find_min_points_by_rows(result[scale])
                    matrix2 = self.find_max_points_by_rows(result[scale])
                    extremum_row_min_array.append(matrix1)
                    extremum_row_max_array.append(matrix2)
                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is False):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix1, '(минимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is False) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_picture(matrix1, '(минимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix1, '(минимум_по_строкам)', scales[scale], scale_folder_path)
                        self.save_extremum_picture(matrix1, '(минимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is False):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix2, '(максимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is False) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_picture(matrix2, '(максимум_по_строкам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix2, '(максимум_по_строкам)', scales[scale], scale_folder_path)
                        self.save_extremum_picture(matrix2, '(максимум_по_строкам)', scales[scale], scale_folder_path)

        if self.col_checkbox.check_state is True:
            if (self.max_checkbox.check_state is True) and (self.min_checkbox.check_state is False):
                for scale in range(num_scale):
                    matrix3 = self.find_max_points_by_column(result[scale])
                    extremum_col_max_array.append(matrix3)
                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is False):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix3, '(максимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is False) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_picture(matrix3, '(максимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix3, '(максимум_по_столбцам)', scales[scale], scale_folder_path)
                        self.save_extremum_picture(matrix3, '(максимум_по_столбцам)', scales[scale], scale_folder_path)

            if (self.max_checkbox.check_state is False) and (self.min_checkbox.check_state is True):
                for scale in range(num_scale):
                    matrix4 = self.find_min_points_by_column(result[scale])
                    extremum_col_min_array.append(matrix4)
                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is False):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix4, '(минимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is False) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_picture(matrix4, '(минимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix4, '(минимум_по_столбцам)', scales[scale], scale_folder_path)
                        self.save_extremum_picture(matrix4, '(минимум_по_столбцам)', scales[scale], scale_folder_path)

            if (self.max_checkbox.check_state is True) and (self.min_checkbox.check_state is True):
                for scale in range(num_scale):
                    matrix5 = self.find_min_points_by_column(result[scale])
                    matrix6 = self.find_max_points_by_column(result[scale])
                    extremum_col_min_array.append(matrix5)
                    extremum_col_max_array.append(matrix6)
                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is False):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix5, '(минимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is False) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_picture(matrix5, '(минимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix5, '(минимум_по_столбцам)', scales[scale], scale_folder_path)
                        self.save_extremum_picture(matrix5, '(минимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is False):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix6, '(максимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is False) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_picture(matrix6, '(максимум_по_столбцам)', scales[scale], scale_folder_path)

                    if (self.p_ex1_checkbox.check_state is True) and (self.p_ex2_checkbox.check_state is True):
                        scale_folder_path = self.create_scale_folder(scales[scale])
                        self.save_extremum_txt(matrix6, '(максимум_по_столбцам)', scales[scale], scale_folder_path)
                        self.save_extremum_picture(matrix6, '(максимум_по_столбцам)', scales[scale], scale_folder_path)

    @staticmethod
    def save_extremum_txt(matrix, title, scale, scale_folder_path):
        global folder_path
        main_title = 'Точки_экстремумов_' + title + '_Масштаб_' + str(scale)
        matrix_str = '\n'.join(' '.join(map(str, row)) for row in matrix)
        file_path = os.path.join(scale_folder_path, main_title + '.txt')

        with open(file_path, "w") as file:
            file.write(matrix_str)

    @staticmethod
    def save_extremum_picture(matrix, title, scale, folder_path):
        data = np.array(matrix)
        main_title = 'Точки_экстремумов_' + title + '_Масштаб_' + str(scale)
        x = data[:, 0]
        y = data[:, 1]

        plt.figure(figsize=(7, 8))
        plt.title(main_title)
        plt.scatter(x, y, alpha=0.5, marker=".")
        plt.gca().invert_yaxis()

        name = main_title.replace(' ', '_') + '.png'
        file_path = os.path.join(folder_path, name)
        plt.savefig(file_path)
        plt.close()

    def compute_dist_angle(self, points, text, scale):
        def distance(p1, p2):
            return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        def sort(point, points):
            l = list(points)
            l.sort(key=lambda coord: distance(point, coord))
            points = np.array(l)
            dist = [round(distance(point, coord), 2) for coord in points]
            return points, dist

        def angle(P1, P2):
            P1_v = [P1[0], P1[1] + 1]
            ang1 = math.atan2(P1_v[1] - P1[1], P1_v[0] - P1[0])
            ang2 = math.atan2(P2[1] - P1[1], P2[0] - P1[0])
            return np.rad2deg((ang1 - ang2) % (2 * np.pi))

        n = int(self.entry_near_point.get())  # число ближайших точек
        result_dist_angle = []
        for i in range(len(points)):
            p0 = points[i]
            points_sort, dist = sort(p0, points)
            angles = [round(angle(p0, p_i)) for p_i in points_sort[1:n + 1]]
            result_dist_angle.append([p0, dist[1:n + 1], angles, points_sort[1:n + 1]])
        scale_folder_path = self.create_scale_folder(scale)
        file_name = text + f'Масштаб_{scale}.txt'
        file_path = os.path.join(scale_folder_path, file_name)
        with open(file_path, "w") as file:
            for value in result_dist_angle:
                line = f"point{value[0]}\t:  dist = {value[1]}\t angle = {value[2]}, points \n {value[3]}\n"
                file.write(line)
            file.close()

    @staticmethod
    def create_downloads_folder(folder_name):
        global folder_path
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        folder_path = os.path.join(downloads_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Папка '{folder_name}' создана в папке 'Загрузки'.")
        print(f"Путь к папке: {folder_path}")

    def compute(self):
        global folder_path
        current_date = datetime.datetime.now()
        date_str = current_date.strftime("%d_%m_%Y_%H_%M_%S")
        folder_name = f"Вейвлет_преобразования_{date_str}"
        self.create_downloads_folder(folder_name)
        if (self.wp_var1.get() is True) and (self.wp_var2.get() is True):
            self.compute_wavelets(0)
        if (self.wp_var1.get() is True) and (self.wp_var2.get() is False):
            self.compute_wavelets(1)
        if (self.wp_var1.get() is False) and (self.wp_var2.get() is True):
            self.compute_wavelets(10)
        if (self.wp_var1.get() is False) and (self.wp_var2.get() is False):
            self.compute_wavelets(11)

        self.find_extremum()
        if self.dist_angle_checkbox.check_state is True:
            global scales, num_scale, extremum_col_min_array, extremum_col_max_array
            global extremum_row_max_array, extremum_row_min_array
            for scale in range(num_scale):
                if len(extremum_col_min_array) > 0:
                    self.compute_dist_angle(extremum_col_min_array[scale],
                                            text="Расстояния_и_углы_минимальные_по_столбцам_",
                                            scale=scales[scale])
                if len(extremum_col_max_array) > 0:
                    self.compute_dist_angle(extremum_col_max_array[scale],
                                            text="Расстояния_и_углы_максимальные_по_столбцам_", scale=scales[scale])
                if len(extremum_row_min_array) > 0:
                    self.compute_dist_angle(extremum_row_min_array[scale],
                                            text="Расстояния_и_углы_минимальные_по_строкам_", scale=scales[scale])
                if len(extremum_row_max_array) > 0:
                    self.compute_dist_angle(extremum_row_max_array[scale],
                                            text="Расстояния_и_углы_максимальные_по_строкам_", scale=scales[scale])
        mb.showinfo(title="Информация", message="Вычисления выполнены успешно. \n" 
                                                "Все файлы сохранены в папку: \n" + folder_path + ".")
        sys.exit(0)


app = App()
app.mainloop()
