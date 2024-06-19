import tkinter as tk
from tkinter import ttk, messagebox
import json

class ShowDelivery(tk.Frame):
    def __init__(self, notebook: ttk.Notebook):
        super().__init__(notebook)
        self.notebook = notebook
        self.init_ui()

    def init_ui(self):
        self.pack(fill=tk.BOTH, expand=True)


        delivery_frame = ttk.Frame(self)
        delivery_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

 
        self.delivery_tree = ttk.Treeview(delivery_frame, columns=("maddh", "ngaynhap", "tongtien"))
        self.delivery_tree.heading("#0", text="Mã Đơn Nhập Hàng")
        self.delivery_tree.heading("maddh", text="Mã Đơn Đặt Hàng")
        self.delivery_tree.heading("ngaynhap", text="Ngày Nhập")
        self.delivery_tree.heading("tongtien", text="Tổng Tiền")
        self.delivery_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        scrollbar = ttk.Scrollbar(delivery_frame, orient="vertical", command=self.delivery_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.delivery_tree.config(yscrollcommand=scrollbar.set)

        self.show_delivery_list()

      
        detail_frame = ttk.Frame(self)
        detail_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.detail_tree = ttk.Treeview(detail_frame, columns=("madausach", "soluong", "tongtien"))
        self.detail_tree.heading("#0", text="Mã Đơn Nhập Hàng")
        self.detail_tree.heading("madausach", text="Mã Đầu Sách")
        self.detail_tree.heading("soluong", text="Số Lượng")
        self.detail_tree.heading("tongtien", text="Tổng Tiền")
        self.detail_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        scrollbar = ttk.Scrollbar(detail_frame, orient="vertical", command=self.detail_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.detail_tree.config(yscrollcommand=scrollbar.set)
        self.show_detail_list()
        self.delivery_tree.bind("<<TreeviewSelect>>", self.show_selected_delivery_details)

    def show_delivery_list(self):
        self.delivery_tree.delete(*self.delivery_tree.get_children())
        try:
            with open('database/donnhaphang.json', 'r', encoding='utf-8') as file:
                delivery_data = json.load(file)
                for delivery in delivery_data:
                    self.delivery_tree.insert("", "end", text=delivery['madnh'], values=(delivery['maddh'], delivery['ngaynhap'], delivery['tongtien']))
        except FileNotFoundError:
            messagebox.showerror('Lỗi', 'Không tìm thấy tệp donnhaphang.json')
        except json.JSONDecodeError:
            messagebox.showerror('Lỗi', 'Lỗi đọc tệp JSON')

    def show_detail_list(self):
        self.detail_tree.delete(*self.detail_tree.get_children())
        try:
            with open('database/chitietdonnhaphang.json', 'r', encoding='utf-8') as file:
                detail_data = json.load(file)
                for detail in detail_data:
                    self.detail_tree.insert("", "end", text=detail['madnh'], values=(detail['madausach'], detail['soluong'], detail['tongtien']))
        except FileNotFoundError:
            messagebox.showerror('Lỗi', 'Không tìm thấy tệp chitietdonnhaphang.json')
        except json.JSONDecodeError:
            messagebox.showerror('Lỗi', 'Lỗi đọc tệp JSON')

    def show_selected_delivery_details(self, event):
        selected_item = self.delivery_tree.selection()[0]
        selected_delivery_madnh = self.delivery_tree.item(selected_item, "text")
        self.detail_tree.delete(*self.detail_tree.get_children())
        try:
            with open('database/chitietdonnhaphang.json', 'r', encoding='utf-8') as file:
                detail_data = json.load(file)
                for detail in detail_data:
                    if detail['madnh'] == selected_delivery_madnh:
                        self.detail_tree.insert("", "end", text=detail['madnh'], values=(detail['madausach'], detail['soluong'], detail['tongtien']))
        except FileNotFoundError:
            messagebox.showerror('Lỗi', 'Không tìm thấy tệp chitietdonnhaphang.json')
        except json.JSONDecodeError:
            messagebox.showerror('Lỗi', 'Lỗi đọc tệp JSON')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hiển thị danh sách đơn nhập hàng và chi tiết đơn nhập hàng")
    notebook = ttk.Notebook(root)
    ShowDelivery(notebook)
    notebook.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
