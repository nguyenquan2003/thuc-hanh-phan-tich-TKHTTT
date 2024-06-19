import tkinter
from tkinter import ttk
import tksheet

from datasystem import data_loader

class Inventory(tkinter.Frame):
    def __init__(self, notebook: ttk.Notebook):
        super().__init__(notebook)

        tkinter.Label(self, text='Hàng tồn kho', font=("Arial", 16)).pack()
        self.sheet_sach = tksheet.Sheet(self, width=800, height=300,
                                        headers=['Mã sách', 'Tên sách', 'Tên tác giả', 'Nhà cung cấp', 'Số lượng tồn'])
        self.sheet_sach.set_all_cell_sizes_to_text()
        self.generate_sheet_sach()
        self.sheet_sach.pack()

        tkinter.Label(self, text='Đơn đặt hàng', font=("Arial", 16)).pack()
        self.sheet_ddh = tksheet.Sheet(self, width=800, height=300,
                                       headers=['Mã đơn', 'Nhà cung cấp', 'Ngày đặt', 'Trạng thái nhập hàng'])
        self.sheet_ddh.set_all_cell_sizes_to_text()
        self.generate_sheet_dondathang()
        self.sheet_ddh.pack()

    def generate_sheet_sach(self):
        dict_dausach = {dausach.madausach: dausach
                                 for dausach in data_loader.dausach}
        dict_nhacungcap = {ncc['mancc']: ncc
                                 for ncc in data_loader.nhacungcap}

        datatable = [[sach.macuonsach, dict_dausach[sach.madausach].tendausach,
                      dict_dausach[sach.madausach].tacgia,
                      dict_nhacungcap[sach.mancc].tenncc, sach.soluongton]
                     for sach in data_loader.cuonsach]
        self.sheet_sach.data_reference(datatable)

    def generate_sheet_dondathang(self):
        dict_ctddh = {dondathang.maddh: [] for dondathang in data_loader.dondathang}
        for ctddh in data_loader.chitietdondathang:
            dict_ctddh[ctddh.maddh].append(ctddh)

        dict_ncc = {ncc.mancc: ncc.tenncc for ncc in data_loader.nhacungcap}

        datatable = [[ddh.maddh, dict_ncc[ddh.mancc], ddh.ngaydat, ddh.trangthai]
                     for ddh in data_loader.dondathang]
        self.sheet_ddh.data_reference(datatable)

        for i in range(len(datatable)):
            is_checked = datatable[i][3]
            self.sheet_ddh.checkbox(f'D{i + 1}', checked=is_checked,
                                    text= 'Hoàn tất' if is_checked else 'Còn thiếu')

    def reset(self):
        self.generate_sheet_sach()
        self.generate_sheet_dondathang()
