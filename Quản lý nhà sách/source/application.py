import tkinter
from tkinter import ttk, messagebox

from tabs.report import Report
from tabs.inventory import Inventory
from tabs.delivery import Delivery, DeliveryDetail
from tabs.showdelivery import ShowDelivery
from tabs.order import Order
from tabs.sell import Sell


class Application:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Quản lý nhà sách')
        self.root.geometry('800x600')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.notebook = self.init_tabs()
        self.notebook.bind("<<NotebookTabChanged>>", self.handle_tab_change)

    def on_closing(self):
        if messagebox.askokcancel("Thoát", "Bạn có chắc chắn muốn thoát ?"):
            self.root.destroy()

    def handle_tab_change(self, event):
        index = event.widget.index("current")
        # selected_tab = event.widget.tab(index, "text")
        # print(f"Selected tab {selected_tab_idx}: {selected_tab}")

        selected_tab = self.tabs[index]
        if hasattr(selected_tab, 'reset'):
            selected_tab.reset()

    def init_tabs(self):
        notebook = ttk.Notebook(self.root)

        self.inventory_tab = Inventory(notebook)
        self.sell_tab = Sell(notebook)
        self.report_tab = Report(notebook)
        self.order_tab = Order(notebook)
        self.delivery_tab = Delivery(notebook)
        self.delivery_detail_tab = DeliveryDetail(notebook)
        self.show_delivery_tab = ShowDelivery(notebook)

        self.tabs = [self.inventory_tab, self.sell_tab, self.report_tab,
                     self.order_tab, self.delivery_tab, self.delivery_detail_tab,
                     self.show_delivery_tab]

        notebook.add(self.inventory_tab, text='Tồn kho')
        notebook.add(self.sell_tab, text='Bán hàng')
        notebook.add(self.report_tab, text='Báo cáo')
        notebook.add(self.order_tab, text='Đơn đặt hàng')
        notebook.add(self.delivery_tab, text='Tạo đơn nhập hàng')
        notebook.add(self.delivery_detail_tab, text='Tạo chi tiết đơn nhập hàng')
        notebook.add(self.show_delivery_tab, text='Hiển thị đơn nhập hàng')
        return notebook

    def run(self):
        self.notebook.place(x=0, y=0)
        self.root.mainloop()