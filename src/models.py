class Phim:
    def __init__(self,ma_phim,ten_phim,thoi_luong):
        self.ma_phim = ma_phim
        self.ten_phim = ten_phim
        self.thoi_luong = thoi_luong
    def __str__(self):
        return f"{self.ma_phim} {self.ten_phim} {self.thoi_luong}"

class Combo:
    def __init__(self, ma_combo, ten_combo, gia):
        self.ma_combo = ma_combo
        self.ten_combo = ten_combo
        self.gia = gia
    def __str__(self):
        return f"{self.ma_combo} - {self.ten_combo}: {self.gia:,} d"


class Hoa_Don:
    def __init__(self):
        self.ds_ve = []
        self.ds_combo = []

    def them_ve(self, ve):
        self.ds_ve.append(ve)

    def them_combo(self, combo):
        self.ds_combo.append(combo)

    def tinh_tong(self):
        # v.gia() là hàm lấy giá vé, c.gia là thuộc tính lấy giá combo
        tien_ve = sum(v.gia() for v in self.ds_ve)
        tien_combo = sum(c.gia for c in self.ds_combo)
        return tien_ve + tien_combo

    def in_hoa_don(self):
        print("\n" + "=" * 20 + " HOA DON " + "=" * 20)
        if self.ds_ve:
            print("--- VE XEM PHIM ---")
            for v in self.ds_ve:
                print(v)
        if self.ds_combo:
            print("--- COMBO BAP NUOC ---")
            for c in self.ds_combo:
                print(c)
        print("-" * 49)
        print(f"TONG CONG: {self.tinh_tong():,} d")
        print("=" * 49 + "\n")

class Ghe:
    def __init__(self, hang, so, gia):
        self.hang = hang
        self.so = so
        self.gia = gia
    def ten(self):
        return f"{self.hang}{self.so}"

class Suat_Chieu:
    def __init__(self,phim,gio_chieu,phong):
        self.phim = phim
        self.gio_chieu = gio_chieu
        self.phong = phong
        self.ds_ghe_dadat=set()
    def in_so_do(self):
        print(f"\n----So do ghe {self.phong.ten_phong}| Gio: {self.gio_chieu}----")
        for hang in self.phong.ds_ghe:
            dong=[]
            for ghe in hang:
                if ghe.ten() in self.ds_ghe_dadat:
                    dong.append("XX")
                else:
                    dong.append(f"[{ghe.ten():^4}]")
            print(" ".join(dong))
    def chon_ghe(self,ten_ghe):
        ten_ghe = ten_ghe.strip().upper()
        ghe = self.phong.tim_ghe(ten_ghe)
        if ghe is None:
            return None, "sai_ghe"
        if ten_ghe in self.ds_ghe_dadat:
            return None, "da_dat"
        self.ds_ghe_dadat.add(ten_ghe)
        return ghe, "ok"
    def __str__(self):
        return f"{self.phim.ten_phim}|Gio:{self.gio_chieu}|{self.phong.ten_phong}"

class Phong_Chieu:
    def __init__(self, ten_phong, so_hang, so_cot, gia_co_ban):
        self.ten_phong = ten_phong
        self.so_hang = so_hang
        self.so_cot = so_cot
        self.ds_ghe = []
        for i in range(so_hang):
            hang = chr(ord("A") + i)
            hang_ghe = []
            for j in range(so_cot):
                hang_ghe.append(Ghe(hang, j + 1, gia_co_ban))
            self.ds_ghe.append(hang_ghe)

    def tim_ghe(self, ten_ghe):
        for hang in self.ds_ghe:
            for ghe in hang:
                if ghe.ten() == ten_ghe:
                    return ghe

        return None

class Ve:
    def __init__(self, suat, ghe):
        self.suat = suat
        self.ghe = ghe

    def gia(self):
        return self.ghe.gia

    def __str__(self):
        return f"{self.suat.phim.ten_phim} | Suat: {self.suat.gio_chieu} | Phong: {self.suat.phong.ten_phong} | Ghe: {self.ghe.ten()} | Gia: {self.gia():,} d"

class Hoa_Don:
    def __init__(self):
        self.ds_ve = []
        self.ds_combo = []

    def them_ve(self, ve):
        self.ds_ve.append(ve)

    def them_combo(self, combo):
        self.ds_combo.append(combo)

    def tinh_tong(self):
        # v.gia() là hàm lấy giá vé, c.gia là thuộc tính lấy giá combo
        tien_ve = sum(v.gia() for v in self.ds_ve)
        tien_combo = sum(c.gia for c in self.ds_combo)
        return tien_ve + tien_combo

    def in_hoa_don(self):
        print("\n" + "=" * 20 + " HOA DON " + "=" * 20)
        if self.ds_ve:
            print("--- VE XEM PHIM ---")
            for v in self.ds_ve:
                print(v)
        if self.ds_combo:
            print("--- COMBO BAP NUOC ---")
            for c in self.ds_combo:
                print(c)
        print("-" * 49)
        print(f"TONG CONG: {self.tinh_tong():,} d")
        print("=" * 49 + "\n")
