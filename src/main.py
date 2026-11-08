from models import Phim, Phong_Chieu, Suat_Chieu, Combo, Ve, Hoa_Don
from storage import nap_du_lieu, luu_du_lieu


def dat_ve(ds_suat, ds_hoa_don):
    # 2. Chọn suất chiếu (Chống gõ lố số hoặc gõ chữ)
    print("\n=== DANH SACH SUAT CHIEU ===")
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
    # Tự động sinh mã hóa đơn tăng dần (VD: HD01, HD02...)
    hd.ma_hd = f"HD{len(ds_hoa_don) + 1:02d}"

    while True:
        nhap_ghe = input("\nNhap cac ghe muon dat (VD: A1 A2 hoac A1,A2): ").strip()
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
        print(f"1. Bap + Nuoc (65000đ)")
        c = input("Chon (1 de lay combo, enter de bo qua): ").strip()
        if c == "1":
            cb1 = Combo("CB1", "Bap + Nuoc", 65000)
            hd.them_combo(cb1)

    # 5. In sơ đồ sau đặt và xuất hóa đơn
    print("\n--- SO DO SAU DAT ---")
    suat_chon.in_so_do()
    hd.in_hoa_don()
    hd.trang_thai = "DA_THANH_TOAN"

    # Thêm vào danh sách và lưu ngay lập tức vào file JSON
    ds_hoa_don.append(hd)
    luu_du_lieu(ds_suat, ds_hoa_don)
    print(f"💾 Đã lưu vé thành công! Mã hóa đơn của bạn là: {hd.ma_hd}")


def huy_ve(ds_hoa_don, ds_suat_chieu):
    """Thực hiện hủy hóa đơn, nhả lại ghế trống cho suất chiếu và cập nhật file."""
    print("\n--- KHO HỦY VÉ ---")
    if not ds_hoa_don:
        print("❌ Hiện tại chưa có hóa đơn nào trong hệ thống!")
        return

    ma_can_huy = input("Nhập mã hóa đơn cần hủy (VD: HD01): ").strip()

    # 1. Tìm hóa đơn trong danh sách
    hoa_don_tim_thay = None
    for hd in ds_hoa_don:
        if getattr(hd, 'ma_hd', '') == ma_can_huy:
            hoa_don_tim_thay = hd
            break

    if not hoa_don_tim_thay:
        print("❌ Không tìm thấy mã hóa đơn này trong hệ thống!")
        return

    # Kiểm tra xem hóa đơn đã hủy trước đó chưa
    if getattr(hoa_don_tim_thay, 'trang_thai', '') == "DA_HUY":
        print("⚠️ Hóa đơn này đã được hủy từ trước đó rồi.")
        return

    # 2. Lấy suất chiếu an toàn từ vé đầu tiên trong hóa đơn
    if not hasattr(hoa_don_tim_thay, 'ds_ve') or not hoa_don_tim_thay.ds_ve:
        print("❌ Hóa đơn không có thông tin vé!")
        return

    suat_chieu = hoa_don_tim_thay.ds_ve[0].suat

    # 3. Nhả lại ghế cho Suất Chiếu tương ứng
    for ve in hoa_don_tim_thay.ds_ve:
        ten_ghe = ve.ghe.ten()
        if ten_ghe in suat_chieu.ds_ghe_dadat:
            suat_chieu.ds_ghe_dadat.remove(ten_ghe)  # Xóa tên ghế khỏi set đã đặt

    # 4. Đổi trạng thái hóa đơn thành đã hủy & lưu lại file JSON
    hoa_don_tim_thay.trang_thai = "DA_HUY"
    luu_du_lieu(ds_suat_chieu, ds_hoa_don)

    print(f"✅ Hủy hóa đơn [{ma_can_huy}] thành công! Các ghế đã được mở khóa trở lại trên sơ đồ.")
def main():
    # 1. Khởi tạo dữ liệu rạp mặc định
    p1 = Phim("P01", "Doraemon", 110)
    p2 = Phim("P02", "Conan", 120)
    phong1 = Phong_Chieu("Phong 01", 5, 5, 80000)

    ds_suat = [
        Suat_Chieu(p1, "09:00", phong1),
        Suat_Chieu(p2, "14:00", phong1)
    ]

    # Nạp dữ liệu cũ từ file JSON (khôi phục ghế đã đặt và danh sách hóa đơn)
    ds_hoa_don = nap_du_lieu(ds_suat)

    # Menu vòng lặp chính
    while True:
        print("\n==============================")
        print("    HỆ THỐNG ĐẶT VÉ RẠP PHIM   ")
        print("==============================")
        print("1. Xem danh sách phim & Đặt vé")
        print("2. Hủy vé")
        print("3. Thoát chương trình")

        choice = input("Chọn chức năng (1-3): ").strip()

        if choice == "1":
            dat_ve(ds_suat, ds_hoa_don)
        elif choice == "2":
            huy_ve(ds_hoa_don, ds_suat)
        elif choice == "3":
            # Đồng bộ lần cuối trước khi thoát
            luu_du_lieu(ds_suat, ds_hoa_don)
            print("👋 Cảm ơn bạn đã sử dụng hệ thống. Hẹn gặp lại!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ, vui lòng nhập từ 1 đến 3!")


if __name__ == "__main__":
    main()