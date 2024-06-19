import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Đường dẫn tới các file JSON
DATA_DIR = 'database'
DON_NHAP_HANG_FILE = os.path.join(DATA_DIR, 'donnhaphang.json')
CHI_TIET_DON_NHAP_HANG_FILE = os.path.join(DATA_DIR, 'chitietdonnhaphang.json')
DON_DAT_HANG_FILE = os.path.join(DATA_DIR, 'dondathang.json')
CUON_SACH_FILE = os.path.join(DATA_DIR, 'cuonsach.json')


def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def update_book_quantity(book_id, quantity):
    books_data = load_json(CUON_SACH_FILE)
    for book in books_data:
        if book['madausach'] == book_id:
            book['soluongton'] += quantity
            break
    save_json(CUON_SACH_FILE, books_data)


class Delivery(ttk.Frame):
    def __init__(self, notebook: ttk.Notebook):
        super().__init__(notebook)
        self.init_ui()

    def init_ui(self):
        self.pack(fill=tk.BOTH, expand=True)

        tk.Label(self, text='Mã đơn nhập hàng').grid(row=0, column=0, padx=5, pady=5)
        self.madnh_entry = tk.Entry(self)
        self.madnh_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self, text='Mã đơn đặt hàng').grid(row=1, column=0, padx=5, pady=5)
        self.maddh_combobox = ttk.Combobox(self)
        self.maddh_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.load_dondathang_options()

        tk.Label(self, text='Ngày nhập').grid(row=2, column=0, padx=5, pady=5)
        self.ngaynhap_entry = tk.Entry(self)
        self.ngaynhap_entry.grid(row=2, column=1, padx=5, pady=5)
        self.ngaynhap_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))

        # Tổng tiền không cần nhập, sẽ tính sau khi nhập chi tiết
        self.tongtien_label = tk.Label(self, text='Tổng tiền: 0')
        self.tongtien_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        tk.Button(self, text='Tạo đơn nhập hàng', command=self.create_delivery).grid(row=4, column=0, columnspan=2,
                                                                                     pady=10)

    def load_dondathang_options(self):
        try:
            dondathang_data = load_json(DON_DAT_HANG_FILE)
            dondathang_ids = [dondathang['maddh'] for dondathang in dondathang_data]
            self.maddh_combobox['values'] = dondathang_ids
        except FileNotFoundError:
            messagebox.showerror('Lỗi', f'Không tìm thấy tệp {DON_DAT_HANG_FILE}')
        except json.JSONDecodeError:
            messagebox.showerror('Lỗi', 'Lỗi đọc tệp JSON')

    def create_delivery(self):
        madnh = self.madnh_entry.get().strip()
        maddh = self.maddh_combobox.get().strip()
        ngaynhap = self.ngaynhap_entry.get().strip()

        if not (madnh and maddh and ngaynhap):
            messagebox.showerror('Lỗi', 'Vui lòng điền đầy đủ thông tin!')
            return

        don_nhap_hang_data = load_json(DON_NHAP_HANG_FILE)

        new_delivery = {
            'madnh': madnh,
            'maddh': maddh,
            'ngaynhap': ngaynhap,
            'tongtien': 0  # Khởi tạo tổng tiền là 0
        }

        don_nhap_hang_data.append(new_delivery)
        save_json(DON_NHAP_HANG_FILE, don_nhap_hang_data)

        messagebox.showinfo('Thành công', 'Đơn nhập hàng đã được tạo thành công!')
        self.reset_form()

    def reset_form(self):
        self.madnh_entry.delete(0, tk.END)
        self.maddh_combobox.set('')
        self.ngaynhap_entry.delete(0, tk.END)
        self.ngaynhap_entry.insert(0, datetime.now().strftime('%d-%m-%Y'))


class DeliveryDetail(ttk.Frame):
    def __init__(self, notebook: ttk.Notebook):
        super().__init__(notebook)
        self.init_ui()

    def init_ui(self):
        self.pack(fill=tk.BOTH, expand=True)

        tk.Label(self, text='Mã đơn nhập hàng').grid(row=0, column=0, padx=5, pady=5)
        self.madnh_combobox = ttk.Combobox(self)
        self.madnh_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.load_donnhaphang_options()

        tk.Button(self, text='Thêm chi tiết', command=self.add_detail).grid(row=0, column=2, padx=5, pady=5)

        self.details_frame = tk.Frame(self)
        self.details_frame.grid(row=2, column=0, columnspan=2)

        self.detail_entries = []

        tk.Button(self, text='Lưu chi tiết đơn nhập hàng', command=self.save_details).grid(row=3, column=0,
                                                                                           columnspan=2, pady=10)

    def load_donnhaphang_options(self):
        try:
            donnhaphang_data = load_json(DON_NHAP_HANG_FILE)
            donnhaphang_ids = [donnhaphang['madnh'] for donnhaphang in donnhaphang_data]
            self.madnh_combobox['values'] = donnhaphang_ids
        except FileNotFoundError:
            messagebox.showerror('Lỗi', f'Không tìm thấy tệp {DON_NHAP_HANG_FILE}')
        except json.JSONDecodeError:
            messagebox.showerror('Lỗi', 'Lỗi đọc tệp JSON')

    def load_books_options(self):
        try:
            books_data = load_json(CUON_SACH_FILE)
            book_ids = [book['madausach'] for book in books_data]
            self.madausach_combobox['values'] = book_ids
        except FileNotFoundError:
            messagebox.showerror('Lỗi', f'Không tìm thấy tệp {CUON_SACH_FILE}')
        except json.JSONDecodeError:
            messagebox.showerror('Lỗi', 'Lỗi đọc tệp JSON')

    def add_detail(self):
        madnh = self.madnh_combobox.get().strip()

        if not madnh:
            messagebox.showerror('Lỗi', 'Vui lòng chọn mã đơn nhập hàng!')
            return

        detail_frame = tk.Frame(self.details_frame)
        detail_frame.pack(pady=5)

        tk.Label(detail_frame, text='Mã sách').grid(row=0, column=0, padx=5, pady=5)
        tk.Label(detail_frame, text='Số lượng').grid(row=1, column=0, padx=5, pady=5)
        tk.Label(detail_frame, text='Tổng tiền').grid(row=2, column=0, padx=5, pady=5)

        self.madausach_combobox = ttk.Combobox(self)
        self.madausach_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.load_books_options()  # Tải danh sách mã sách vào Combobox

        soluong_entry = tk.Entry(detail_frame)
        soluong_entry.grid(row=1, column=1, padx=5, pady=5)

        tongtien_entry = tk.Entry(detail_frame)
        tongtien_entry.grid(row=2, column=1, padx=5, pady=5)

        self.detail_entries.append((madnh, self.madausach_combobox, soluong_entry, tongtien_entry))

    def save_details(self):
        for detail in self.detail_entries:
            madnh = detail[0]
            madausach = detail[1].get().strip()
            soluong = int(detail[2].get().strip())
            tongtien = int(detail[3].get().strip()) if detail[3].get().strip() else 0

            if not (madausach and soluong):
                messagebox.showerror('Lỗi', 'Vui lòng điền đầy đủ thông tin chi tiết!')
                return

            new_detail = {
                'madnh': madnh,
                'madausach': madausach,
                'soluong': soluong,
                'tongtien': tongtien
            }

            chitiet_don_nhap_hang_data = load_json(CHI_TIET_DON_NHAP_HANG_FILE)
            chitiet_don_nhap_hang_data.append(new_detail)
            save_json(CHI_TIET_DON_NHAP_HANG_FILE, chitiet_don_nhap_hang_data)

            update_book_quantity(madausach, soluong)
            don_nhap_hang_data = load_json(DON_NHAP_HANG_FILE)
            for don_nhap_hang in don_nhap_hang_data:
                if don_nhap_hang['madnh'] == madnh:
                    don_nhap_hang['tongtien'] += tongtien
                    break
            save_json(DON_NHAP_HANG_FILE, don_nhap_hang_data)

        messagebox.showinfo('Thành công', 'Chi tiết đơn nhập hàng đã được lưu thành công!')
        self.reset_form()

    def reset_form(self):
        self.madnh_combobox.set('')
        for detail_frame in self.details_frame.winfo_children():
            detail_frame.destroy()
        self.detail_entries = []
        self.madausach_combobox.grid_remove()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Quản lý đơn nhập hàng")
    notebook = ttk.Notebook(root)

    delivery_tab = Delivery(notebook)
    notebook.add(delivery_tab, text="Tạo đơn nhập hàng")

    delivery_detail_tab = DeliveryDetail(notebook)
    notebook.add(delivery_detail_tab, text="Thêm chi tiết đơn nhập hàng")

    notebook.pack(expand=True, fill=tk.BOTH)

    root.mainloop()




