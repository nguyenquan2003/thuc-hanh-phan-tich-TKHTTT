import tkinter as tk
from tkinter import ttk, messagebox
from tksheet import Sheet
from datasystem import data_loader, DonDatHang, ChiTietDonDatHang

from random import randrange
from datetime import datetime
import json

FILE_DONDATHANG = 'database/dondathang.json'
FILE_CHITIETDONDATHANG = 'database/chitietdondathang.json'

def save_file(path: str, data):
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=2)


class Order(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.supplier_label = ttk.Label(self, text="Nhà cung cấp")

        self.current_selected = tk.StringVar()
        self.supplier_combobox = ttk.Combobox(self, values=self.get_suppliers(),
                                                 textvariable=self.current_selected)
        self.supplier_combobox.current(0)

        self.items_label = ttk.Label(self, text="Chi tiết đơn đặt hàng:")

        self.dausach_selected = []
        self.items_sheet = Sheet(self, headers=["Mã đầu sách", "Tên đầu sách", "Số lượng"])

        self.items_sheet.enable_bindings(("edit_cell",
            "single_select",
            "row_select",
            "column_select",
            "arrowkeys",
            "row_height_resize",
            "double_click_column_resize",
            "right_click_popup_menu",
            "rc_select"
        ))
        self.items_sheet.popup_menu_add_command("Xóa", self.xoa_chi_tiet_don_dat_hang)

        self.submit_button = ttk.Button(self, text="Lưu đơn đặt hàng", command=self.submit_order)

        # Layout
        self.supplier_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.supplier_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.items_label.grid(row=1, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.items_sheet.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        self.submit_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

        # -----
        self.dausach_table = [[dausach.madausach, dausach.tendausach, dausach.tacgia]
                              for dausach in data_loader.dausach]

        ttk.Label(self, text='Đầu sách').grid(column=2, row=0)
        self.dausach_sheet = Sheet(self, header=['Mã đầu sách', 'Tên đầu sách', 'Tác giả'],
                                   data_reference=self.dausach_table)
        self.dausach_sheet.set_all_cell_sizes_to_text()
        self.dausach_sheet.enable_bindings(("single_select",
                                    "drag_select",
                                    "select_all",
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select"
                                    ))
        self.dausach_sheet.popup_menu_add_command("Thêm chi tiết", self.them_chi_tiet_don_dat_hang)
        self.dausach_sheet.grid(column=2, row=1, columnspan=2, rowspan=3)

        # self.columnconfigure(2, weight=1)
        # self.rowconfigure(5, weight=1)

    def them_chi_tiet_don_dat_hang(self, event = None):
        selected = self.dausach_sheet.get_currently_selected()
        row_index = selected.row
        data_selected = self.dausach_table[row_index]


        exist = False
        for i in range(len(self.dausach_selected)):
            if data_selected[0] == self.dausach_selected[i][0]:
                exist = True
                self.dausach_selected[i][2] = int(self.dausach_selected[i][2]) + 1
                break

        if not exist:
            self.dausach_selected.append([data_selected[0], data_selected[1], 1])
        self.items_sheet.data_reference(self.dausach_selected)

    def xoa_chi_tiet_don_dat_hang(self, event=None):
        selected = self.items_sheet.get_currently_selected()
        row_index = selected.row
        self.dausach_selected.pop(row_index)
        self.items_sheet.data_reference(self.dausach_selected)

    def get_suppliers(self):
        suppliers = data_loader.nhacungcap
        return [f'{supplier.mancc} {supplier.tenncc}' for supplier in suppliers]

    def submit_order(self):
        new_dondathang = {
            "maddh": None,
            "ngaydat": datetime.now().strftime('%d-%m-%Y'),
            "mancc": self.current_selected.get()[:7],
            "trangthai": False
          }

        # Gán mã đơn đặt hàng
        maddh_set = {ddh.maddh for ddh in data_loader.dondathang}
        while True:
            new_dondathang['maddh'] = f'DDH-{randrange(100, 999)}-{randrange(100, 999)}'
            if new_dondathang['maddh'] not in maddh_set:
                break

        list_ctddh = []
        for dausach in self.dausach_selected:
            new_ctddh = {
                "maddh": new_dondathang['maddh'],
                "madausach": dausach[0],
                "soluong": int(dausach[2])
              }
            list_ctddh.append(new_ctddh)

        # Thêm đơn đặt hàng
        data_loader.dondathang.append(DonDatHang(new_dondathang))
        # Thêm chi tiết đơn đặt hàng
        data_loader.chitietdondathang.extend(ChiTietDonDatHang(ctddh) for ctddh in list_ctddh)

        # Lưu tệp
        save_file(FILE_DONDATHANG, [ddh.dictionary for ddh in data_loader.dondathang])
        save_file(FILE_CHITIETDONDATHANG, [ctddh.dictionary for ctddh in data_loader.chitietdondathang])

        messagebox.showinfo('Thông báo', 'Thêm đơn đặt hàng thành công !')
