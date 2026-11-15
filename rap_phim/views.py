from django.shortcuts import render, redirect
from .models import Phim, PhongChieu, SuatChieu
from .storage import nap_du_lieu, luu_du_lieu
import qrcode
import os
import re

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


def tao_qr_code(ma_ve, thong_tin_chi_tiet):
    qr_data = f"VE_RAP_PHIM: {ma_ve}\n{thong_tin_chi_tiet}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    os.makedirs("rap_phim/static/images", exist_ok=True)
    duong_dan_luu = f"rap_phim/static/images/qr_{ma_ve}.png"
    img.save(duong_dan_luu)

    return f"/static/images/qr_{ma_ve}.png"


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

            ma_ve = f"VE{len(ds_hoa_don) + 1:03d}"
            thong_tin_qr = f"{TEMP_BOOKING['ten_phim']} - Suất: {TEMP_BOOKING['gio_chieu']} - Ghế: {', '.join(TEMP_BOOKING['ds_ghe'])}"
            duong_dan_qr = tao_qr_code(ma_ve, thong_tin_qr)

            hoa_don_moi = dict(TEMP_BOOKING)
            hoa_don_moi['ma_ve'] = ma_ve
            hoa_don_moi['qr_code'] = duong_dan_qr

            ds_hoa_don.append(hoa_don_moi)
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
    return render(request, "lich_su_ve.html", {
        "ds_hoa_don": ds_cua_toi,
        "username": CURRENT_USER,
        "current_user": CURRENT_USER
    })


def doi_gio_ra_phut(chuoi_gio):
    try:
        h, m = map(int, chuoi_gio.split(':'))
        return h * 60 + m
    except:
        return 0


def lay_so_phut_thoi_luong(chuoi_thoi_luong):
    so = re.findall(r'\d+', str(chuoi_thoi_luong))
    return int(so[0]) if so else 120


def admin_quan_ly(request):
    global DANH_SACH_SUAT_CHIEU, ds_hoa_don, CURRENT_USER
    if CURRENT_USER != 'admin':
        return redirect('/dang-nhap/')

    thong_bao = ""
    if request.method == "POST" and request.POST.get("action"):
        action = request.POST.get("action")

        if action == "them":
            ten_phim = request.POST.get("ten_phim")
            thoi_luong_str = request.POST.get("thoi_luong", "120 phút")
            phong_chieu = request.POST.get("phong_chieu")
            gio_chieu = request.POST.get("gio_chieu")

            phut_moi_bat_dau = doi_gio_ra_phut(gio_chieu)
            thoi_luong_moi_phut = lay_so_phut_thoi_luong(thoi_luong_str)
            phut_moi_ket_thuc = phut_moi_bat_dau + thoi_luong_moi_phut

            trung_lich = False
            for suat in DANH_SACH_SUAT_CHIEU:
                if suat.phong.ten_phong == phong_chieu:
                    phut_cu_bat_dau = doi_gio_ra_phut(suat.gio_chieu)
                    thoi_luong_cu_phut = lay_so_phut_thoi_luong(suat.phim.thoi_luong)
                    phut_cu_ket_thuc = phut_cu_bat_dau + thoi_luong_cu_phut

                    if phut_moi_bat_dau < phut_cu_ket_thuc and phut_cu_bat_dau < phut_moi_ket_thuc:
                        trung_lich = True
                        break

            if trung_lich:
                thong_bao = f"❌ Phòng '{phong_chieu}' đang có suất chiếu trong khung giờ này (trùng khoảng thời gian phim đang chiếu)!"
            else:
                ma_suat = f"SC{len(DANH_SACH_SUAT_CHIEU) + 1:02d}"
                ma_phim_moi = f"P{len(DANH_SACH_SUAT_CHIEU) + 1:02d}"

                phim_moi = Phim(ma_phim=ma_phim_moi, ten_phim=ten_phim, thoi_luong=thoi_luong_str)
                phong_moi = PhongChieu(ma_phong="ROOM_CUSTOM", ten_phong=phong_chieu)

                suat_moi = SuatChieu(ma_suat, phim_moi, phong_moi, gio_chieu)
                DANH_SACH_SUAT_CHIEU.append(suat_moi)
                luu_du_lieu(DANH_SACH_SUAT_CHIEU, ds_hoa_don)
                thong_bao = "✅ Thêm suất chiếu thành công!"

        elif action == "xoa":
            ma_suat = request.POST.get("ma_suat")
            DANH_SACH_SUAT_CHIEU = [sc for sc in DANH_SACH_SUAT_CHIEU if sc.ma_suat != ma_suat]
            luu_du_lieu(DANH_SACH_SUAT_CHIEU, ds_hoa_don)
            thong_bao = "✅ Xóa suất chiếu thành công!"

    context = {
        "ds_suat_chieu": DANH_SACH_SUAT_CHIEU,
        "ds_hoa_don": ds_hoa_don,
        "current_user": CURRENT_USER,
        "thong_bao": thong_bao
    }
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
                return redirect('/admin-quan-ly/')
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