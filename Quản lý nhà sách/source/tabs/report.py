import tkinter
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tksheet
from datetime import datetime
from datasystem import data_loader
import calendar

def get_number_of_days(month, year):
    # Sử dụng hàm monthrange để lấy ra số ngày trong tháng
    days_in_month = calendar.monthrange(year, month)[1]
    return list(range(1, days_in_month+1))

now_date = datetime.now()
month = now_date.month
prev_month = 1 if month == 12 else month - 1

class Report(tkinter.Frame):
    def __init__(self, notebook: ttk.Notebook):
        super().__init__(notebook)

        tkinter.Label(self, text=f'Tổng kết tài chính trong tháng {prev_month}', font=("Arial", 16)).pack()
        self.generate_sheet_salary_per_month()

        tong_thunhap = sum(hoadon.tongtien for hoadon in self.list_hoadon_by_month(prev_month))
        tkinter.Label(self, text=f'Tổng thu nhập trong tháng : {tong_thunhap:,.0f} VNĐ').pack()

        self.generate_sheet_pay_per_month()
        tong_chitra = sum(dnh.tongtien for dnh in self.list_donnhaphang_by_month(prev_month))
        tkinter.Label(self, text=f'Tổng chi trả trong tháng : {tong_chitra:,.0f} VNĐ').pack()

        tkinter.Button(self, text='Xem biểu đồ', command=self.draw_chart).pack()

    def list_hoadon_by_month(self, month):
        list_hoadon = [hoadon for hoadon in data_loader.hoadon if
                       datetime.strptime(hoadon.ngaylap, "%d-%m-%Y").month == month]
        return list_hoadon

    def list_donnhaphang_by_month(self, month):
        list_donnhaphang = [dnh for dnh in data_loader.donnhaphang if
                       datetime.strptime(dnh.ngaynhap, "%d-%m-%Y").month == month]
        return list_donnhaphang

    def generate_sheet_salary_per_month(self):
        # Lọc theo tháng hiện tại
        list_hoadon = self.list_hoadon_by_month(prev_month)

        # Đếm tổng số lượng sách trong một hóa đơn
        dict_number = {hoadon.mahd: 0 for hoadon in list_hoadon}
        for cthd in data_loader.chitiethoadon:
            if cthd.mahd in dict_number:
                dict_number[cthd.mahd] += cthd.soluong

        # Sắp xếp tăng dần danh sách đã lọc
        datatable = [[hoadon.mahd, hoadon.ngaylap, dict_number[hoadon.mahd],
                      f'{hoadon.tongtien:,.0f}']
                     for hoadon in list_hoadon]
        datatable.sort(key=lambda item: datetime.strptime(item[1], "%d-%m-%Y").day)
        datatable.reverse()

        self.sheet_salary = tksheet.Sheet(self, width=800, height=200, data=datatable)
        self.sheet_salary.headers(['Mã hóa đơn', 'Ngày lập', 'Số lượng mua', 'Tổng tiền'])
        self.sheet_salary.set_all_cell_sizes_to_text()
        self.sheet_salary.pack()

    def generate_sheet_pay_per_month(self):
        # Lọc theo tháng hiện tại
        list_donnhaphang = self.list_donnhaphang_by_month(prev_month)

        # Đếm tổng số lượng sách trong một hóa đơn
        dict_number = {dnh.madnh: 0 for dnh in list_donnhaphang}
        for ctdnh in data_loader.chitietdonnhaphang:
            if ctdnh.madnh in dict_number:
                dict_number[ctdnh.madnh] += ctdnh.soluong

        # Sắp xếp tăng dần danh sách đã lọc
        datatable = [[dnh.madnh, dnh.ngaynhap, dict_number[dnh.madnh],
                      f'{dnh.tongtien:,.0f}']
                     for dnh in list_donnhaphang]


        self.sheet_pay = tksheet.Sheet(self, width=800, height=200, data=datatable)
        self.sheet_pay.headers(['Mã đơn nhập hàng', 'Ngày nhập', 'Số lượng nhập', 'Tổng tiền'])
        self.sheet_pay.set_all_cell_sizes_to_text()
        self.sheet_pay.pack()

    def list_salary_per_day(self):
        days = get_number_of_days(prev_month, now_date.year)
        sales = [0] * len(days)

        list_hoadon = self.list_hoadon_by_month(prev_month)
        for hoadon in list_hoadon:
            ngaylap = datetime.strptime(hoadon.ngaylap, "%d-%m-%Y").day
            sales[ngaylap - 1] += hoadon.tongtien
        return sales

    def list_pay_per_day(self):
        days = get_number_of_days(prev_month, now_date.year)
        expenses = [0] * len(days)

        list_donnhaphang = self.list_donnhaphang_by_month(prev_month)
        for dnh in list_donnhaphang:
            ngaylap = datetime.strptime(dnh.ngaynhap, "%d-%m-%Y").day
            expenses[ngaylap - 1] += dnh.tongtien
        return expenses

    def draw_chart(self):
        days = get_number_of_days(prev_month, now_date.year)
        sales = self.list_salary_per_day()
        expenses = self.list_pay_per_day()

        fig, ax = plt.subplots()
        ax.plot(days, sales, label='Tổng bán ra', color='blue', marker='o')
        ax.plot(days, expenses, label='Tổng chi ra', color='red', marker='x')
        ax.set_xlabel('Ngày trong tháng')
        ax.set_ylabel('Tổng tiền')
        ax.legend()

        # Tạo cửa sổ mới và thêm biểu đồ vào cửa sổ
        chart_window = tkinter.Toplevel(self)
        chart_window.title('Biểu đồ tài chính trong tháng')
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack()
