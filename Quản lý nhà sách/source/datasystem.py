import json

class EntityBase:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def id(self):
        return self

    def __eq__(self, other):
        return self.id() == other.id()

    def __ne__(self, other):
        return self.id() != other.id()

    def __getitem__(self, __key: str):
        return self.dictionary[__key]

    def __getattr__(self, __key: str):
        return self.dictionary[__key]

class NhaCungCap(EntityBase):
    def id(self):
        return self.dictionary['mancc']

class TheLoaiSach(EntityBase):
    def id(self):
        return self.dictionary['matheloai']

class DauSach(EntityBase):
    def id(self):
        return self.dictionary['madausach']

class CuonSach(EntityBase):
    def id(self):
        return self.dictionary['macuonsach']

class HoaDon(EntityBase):
    def id(self):
        return self.dictionary['mahd']

class ChiTietHoaDon(EntityBase):
    def id(self):
        return self.dictionary['mahd'], self.dictionary['macuonsach']

class DonDatHang(EntityBase):
    def id(self):
        return self.dictionary['maddh']

class ChiTietDonDatHang(EntityBase):
    def id(self):
        return self.dictionary['maddh'], self.dictionary['madausach']

class DonNhapHang(EntityBase):
    def id(self):
        return self.dictionary['madnh']

class ChiTietDonNhapHang(EntityBase):
    def id(self):
        return self.dictionary['madnh'], self.dictionary['madausach']


mapping_from_key_to_class = {
    'nhacungcap': NhaCungCap,
    'theloaisach': TheLoaiSach,
    'dausach': DauSach,
    'cuonsach': CuonSach,
    'hoadon': HoaDon,
    'chitiethoadon': ChiTietHoaDon,
    'dondathang': DonDatHang,
    'chitietdondathang': ChiTietDonDatHang,
    'donnhaphang': DonNhapHang,
    'chitietdonnhaphang': ChiTietDonNhapHang,
}


class DataLoader:
    def __init__(self):
        self.tables = dict()

    def generate_table(self, __key, data):
        self.tables[__key] = [mapping_from_key_to_class[__key](item)
                              for item in data]

    def __getattr__(self, __key):
        if __key not in self.tables:
            # Loading data
            path = f'database/{__key}.json'
            with open(path, 'r', encoding='UTF-8') as file:
                data = json.load(file)
                print(f'Load from {path} successfully.')

            self.generate_table(__key, data)
        return self.tables[__key]

data_loader = DataLoader()
