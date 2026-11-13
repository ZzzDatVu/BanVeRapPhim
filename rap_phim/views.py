from django.shortcuts import render, redirect
from .models import Phim, PhongChieu, SuatChieu
from .storage import nap_du_lieu, luu_du_lieu

DANH_SACH_SUAT_CHIEU, ds_hoa_don = nap_du_lieu()
TEMP_BOOKING = {}

# Biến toàn cục lưu trữ tài khoản và người dùng đang đăng nhập hiện tại
DS_NGUOI_DUNG = {
    "admin": "1234"
}
CURRENT_USER = None


def trang_chu(request):
    global DANH_SACH_SUAT_CHIEU, CURRENT_USER
    context = {"ds_suat_chieu": DANH_SACH_SUAT_CHIEU, "current_user": CURRENT_USER}
    return render(request, "trang_chu.html", context)


def chon_ghe(request, ma_suat):
    global DANH_SACH_SUAT_CHIEU, TEMP_BOOKING, CURRENT_USER
    suat_hien_tai = next((sc for sc in DANH_SACH_SUAT_CHIEU if sc.ma_suat == ma_suat), None)

    if request.method == "POST":
        danh_sach_chon = request.POST.getlist("ghe_chon")
        if suat_hien_tai and danh_sach_chon:
            TEMP_BOOKING = {
                "ma_suat": ma_suat,
                "ds_ghe": danh_sach_chon,
                "tien_ghe": len(danh_sach_chon) * 50000,
                "ten_phim": suat_hien_tai.phim.ten_phim,
                "gio_chieu": suat_hien_tai.gio_chieu,
                "nguoi_dat": CURRENT_USER if CURRENT_USER else "Khách vãng lai"
            }
            return redirect('/chon-bap-nuoc/')

    context = {
        "suat": suat_hien_tai,
        "ghe_hop_le": suat_hien_tai.phong.lay_danh_sach_ghe_hop_le() if suat_hien_tai else [],
        "ghe_da_dat": list(suat_hien_tai.ds_ghe_dadat) if suat_hien_tai else [],
        "current_user": CURRENT_USER
    }
    return render(request, "chon_ghe.html", context)


def chon_bap_nuoc(request):
    global TEMP_BOOKING, CURRENT_USER
    if not TEMP_BOOKING:
        return redirect('/')

    if request.method == "POST":
        combo_raw = request.POST.get("combo", "khong|0|Không mua Combo")
        parts = combo_raw.split("|")
        TEMP_BOOKING['tien_bap_nuoc'] = int(parts[1])
        TEMP_BOOKING['ten_combo'] = parts[2]
        return redirect('/chon-uu-dai/')

    return render(request, "chon_bap_nuoc.html", {"booking": TEMP_BOOKING, "current_user": CURRENT_USER})


def chon_uu_dai(request):
    global DANH_SACH_SUAT_CHIEU, ds_hoa_don, TEMP_BOOKING, CURRENT_USER
    if not TEMP_BOOKING:
        return redirect('/')

    suat = next((sc for sc in DANH_SACH_SUAT_CHIEU if sc.ma_suat == TEMP_BOOKING['ma_suat']), None)

    if request.method == "POST":
        if "thanh_toan" in request.POST:
            if suat:
                for g in TEMP_BOOKING['ds_ghe']:
                    suat.ds_ghe_dadat.add(g)

            ds_hoa_don.append(dict(TEMP_BOOKING))
            luu_du_lieu(DANH_SACH_SUAT_CHIEU, ds_hoa_don)

            TEMP_BOOKING = {}
            return redirect('/lich-su-ve/')

        ma_giam = request.POST.get("ma_giam", "").strip().upper()
        giam_gia = 0
        if ma_giam == "GIAM10":
            giam_gia = 10000
        elif ma_giam == "GIAM20":
            giam_gia = 20000

        TEMP_BOOKING['ma_giam'] = ma_giam
        TEMP_BOOKING['giam_gia'] = giam_gia

    tien_ghe = TEMP_BOOKING.get('tien_ghe', 0)
    tien_bap_nuoc = TEMP_BOOKING.get('tien_bap_nuoc', 0)
    giam_gia = TEMP_BOOKING.get('giam_gia', 0)
    TEMP_BOOKING['tong_tien'] = max(0, tien_ghe + tien_bap_nuoc - giam_gia)

    return render(request, "chon_uu_dai.html", {"booking": TEMP_BOOKING, "current_user": CURRENT_USER})


def lich_su_ve(request):
    global ds_hoa_don, CURRENT_USER
    if not CURRENT_USER:
        return redirect('/dang-nhap/')

    ds_cua_toi = [hd for hd in ds_hoa_don if hd.get('nguoi_dat') == CURRENT_USER]
    return render(request, "lich_su_ve.html",
                  {"ds_hoa_don": ds_cua_toi, "username": CURRENT_USER, "current_user": CURRENT_USER})


def admin_quan_ly(request):
    global DANH_SACH_SUAT_CHIEU, ds_hoa_don, CURRENT_USER
    if CURRENT_USER != 'admin':
        return redirect('/dang-nhap/')

    if request.method == "POST" and request.POST.get("action"):
        action = request.POST.get("action")
        if action == "them":
            ten_phim = request.POST.get("ten_phim")
            thoi_luong = request.POST.get("thoi_luong")
            gio_chieu = request.POST.get("gio_chieu")

            ma_suat = f"SC{len(DANH_SACH_SUAT_CHIEU) + 1:02d}"
            phim_moi = Phim(f"P{len(DANH_SACH_SUAT_CHIEU) + 1:02d}", ten_phim, thoi_luong)
            phong_moi = PhongChieu("ROOM01", "Phòng 1")

            suat_moi = SuatChieu(ma_suat, phim_moi, phong_moi, gio_chieu)
            DANH_SACH_SUAT_CHIEU.append(suat_moi)
            luu_du_lieu(DANH_SACH_SUAT_CHIEU, ds_hoa_don)

        elif action == "xoa":
            ma_suat = request.POST.get("ma_suat")
            DANH_SACH_SUAT_CHIEU = [sc for sc in DANH_SACH_SUAT_CHIEU if sc.ma_suat != ma_suat]
            luu_du_lieu(DANH_SACH_SUAT_CHIEU, ds_hoa_don)

        return redirect("/admin-quan-ly/")

    context = {"ds_suat_chieu": DANH_SACH_SUAT_CHIEU, "ds_hoa_don": ds_hoa_don, "current_user": CURRENT_USER}
    return render(request, "admin.html", context)


def dang_nhap(request):
    global DS_NGUOI_DUNG, CURRENT_USER
    thong_bao = ""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if username in DS_NGUOI_DUNG and DS_NGUOI_DUNG[username] == password:
            CURRENT_USER = username
            if username == 'admin':
                return redirect('/admin-quan-ly/')  # Trỏ thẳng về trang quản lý tự thiết kế
            return redirect('/')
        else:
            thong_bao = "Tài khoản hoặc mật khẩu không chính xác!"
    return render(request, "dang_nhap.html", {"thong_bao": thong_bao, "current_user": CURRENT_USER})

def dang_ky(request):
    global DS_NGUOI_DUNG, CURRENT_USER
    thong_bao = ""
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if username in DS_NGUOI_DUNG:
            thong_bao = "Tài khoản này đã tồn tại, vui lòng chọn tên khác!"
        elif not username or not password:
            thong_bao = "Vui lòng điền đầy đủ thông tin!"
        else:
            DS_NGUOI_DUNG[username] = password
            thong_bao = "Đăng ký thành công! Bạn có thể đăng nhập ngay."

    return render(request, "dang_ky.html", {"thong_bao": thong_bao, "current_user": CURRENT_USER})


def dang_xuat(request):
    global CURRENT_USER
    CURRENT_USER = None
    return redirect('/')