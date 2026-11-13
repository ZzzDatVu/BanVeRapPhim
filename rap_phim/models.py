class Phim:
    def __init__(self, ma_phim, ten_phim, thoi_luong):
        self.ma_phim = ma_phim
        self.ten_phim = ten_phim
        self.thoi_luong = thoi_luong

class PhongChieu:
    def __init__(self, ma_phong, ten_phong, so_hang=5, so_cot=5):
        self.ma_phong = ma_phong
        self.ten_phong = ten_phong
        self.so_hang = so_hang
        self.so_cot = so_cot

    def lay_danh_sach_ghe_hop_le(self):
        danh_sach = []
        for i in range(self.so_hang):
            hang_chu = chr(ord('A') + i)
            for j in range(1, self.so_cot + 1):
                danh_sach.append(f"{hang_chu}{j}")
        return danh_sach

class SuatChieu:
    def __init__(self, ma_suat, phim, phong, gio_chieu):
        self.ma_suat = ma_suat
        self.phim = phim
        self.phong = phong
        self.gio_chieu = gio_chieu
        self.ds_ghe_dadat = set()