from models import Phim, PhongChieu, SuatChieu, NguoiDung
from storage import nap_du_lieu, luu_du_lieu
from admin import menu_admin
from views import menu_viewer


def main():
    # 1. Khởi tạo danh sách đối tượng mẫu (Khung dữ liệu chuẩn OOP)
    p1 = Phim("P01", "Avengers: Endgame", "180 phút")
    p2 = Phim("P02", "Doraemon: Nobita", "90 phút")

    phong1 = PhongChieu("ROOM01", "Phòng 1", so_hang=5, so_cot=5)  # Ma trận ghế A1..E5
    phong2 = PhongChieu("ROOM02", "Phòng 2", so_hang=5, so_cot=5)

    ds_suat_chieu = [
        SuatChieu("SC01", p1, phong1, "19:00"),
        SuatChieu("SC02", p2, phong2, "15:00"),
    ]

    # Khai báo người dùng mẫu (Đạt chuẩn 7 OOP Classes)
    admin_user = NguoiDung("U01", "Admin_Manager", "ADMIN")
    viewer_user = NguoiDung("U02", "Khach_Hang", "VIEWER")

    # 2. Nạp dữ liệu cũ từ JSON
    ds_hoa_don = nap_du_lieu(ds_suat_chieu)

    # 3. Vòng lặp giao diện Console
    while True:
        print("\n==========================================")
        print("    HỆ THỐNG ĐẶT VÉ RẠP PHIM CONSOLE OOP  ")
        print("==========================================")
        print("1. Khách hàng (Viewer)")
        print("2. Quản trị viên (Admin)")
        print("3. Lưu dữ liệu & Thoát")

        chon = input("Vui lòng chọn vai trò (1-3): ").strip()

        if chon == "1":
            print(f"\n👋 Xin chào Khách hàng ({viewer_user.ten_user})")
            menu_viewer(ds_suat_chieu, ds_hoa_don)
        elif chon == "2":
            pass_admin = input("Nhập mật khẩu Admin: ").strip()
            if pass_admin == "admin123":
                print(
                    f"\n🔑 Đăng nhập thành công! Quản trị viên: {admin_user.ten_user}"
                )
                menu_admin(ds_suat_chieu, ds_hoa_don)
            else:
                print("❌ Mật khẩu Admin sai!")
        elif chon == "3":
            luu_du_lieu(ds_suat_chieu, ds_hoa_don)
            print("💾 Đã ghi nhận toàn bộ dữ liệu vào `data/database.json`. Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ, vui lòng chọn lại!")


if __name__ == "__main__":
    main()
