from models import Phim, Phong_Chieu, Suat_Chieu, Combo, Ve, Hoa_Don


def main():
    # 1. Dữ liệu rạp
    p1 = Phim("P01", "Doraemon", 110)
    p2 = Phim("P02", "Conan", 120)
    phong1 = Phong_Chieu("Phong 01", 5, 5, 80000)

    ds_suat = [
        Suat_Chieu(p1, "09:00", phong1),
        Suat_Chieu(p2, "14:00", phong1)
    ]
    cb1 = Combo("CB1", "Bap + Nuoc", 65000)

    # 2. Chọn suất chiếu (Chống gõ lố số hoặc gõ chữ)
    print("=== DANH SACH SUAT CHIEU ===")
    for i, s in enumerate(ds_suat, start=1):
        print(f"{i}. {s}")

    while True:
        nhap = input(f"Chon suat (1 hoac {len(ds_suat)}): ").strip()
        if nhap.isdigit() and 1 <= int(nhap) <= len(ds_suat):
            suat_chon = ds_suat[int(nhap) - 1]
            break
        print("Lua chon khong hop le, vui long nhap lai!")

    # 3. Chọn ghế (Xử lý cả dấu phẩy lẫn dấu cách)
    suat_chon.in_so_do()
    hd = Hoa_Don()

    while True:
        nhap_ghe = input("\nNhap cac ghe muon dat (VD: A1 A2 hoac A1,A2): ").strip()
        # Chuyển dấu phẩy thành dấu cách rồi tách chuỗi
        ds_ten = nhap_ghe.replace(",", " ").upper().split()
        if not ds_ten:
            print("Vui long nhap it nhat mot ghe!")
            continue

        dem_thanh_cong = 0
        for ten in ds_ten:
            ghe, kq = suat_chon.chon_ghe(ten)
            if kq == "ok":
                hd.them_ve(Ve(suat_chon, ghe))
                print(f"-> Chon thanh cong ghe {ten}")
                dem_thanh_cong += 1
            elif kq == "da_dat":
                print(f"-> Ghe {ten} da co nguoi dat roi!")
            else:
                print(f"-> Ghe {ten} khong ton tai tren so do!")

        if dem_thanh_cong > 0:
            break
        print("Chua dat duoc ghe nao hop le, vui long chon lai!")

    # 4. Mua bắp nước (Bắt buộc chỉ nhập y hoặc n)
    while True:
        hoi_cb = input("\nMua bap nuoc khong? (y/n): ").strip().lower()
        if hoi_cb in ['y', 'n']:
            break
        print("Vui long chi nhap 'y' (dong y) hoac 'n' (khong)!")

    if hoi_cb == 'y':
        print(f"1. {cb1}")
        c = input("Chon (1 de lay combo, enter de bo qua): ").strip()
        if c == "1":
            hd.them_combo(cb1)

    # 5. In sơ đồ sau đặt và xuất hóa đơn
    print("\n--- SO DO SAU DAT ---")
    suat_chon.in_so_do()
    hd.in_hoa_don()


if __name__ == "__main__":
    main()
