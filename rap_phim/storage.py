import json
import os
from django.conf import settings
from .models import Phim, PhongChieu, SuatChieu

FILE_PATH = os.path.join(settings.BASE_DIR, "data", "database.json")


def luu_du_lieu(ds_suat_chieu, ds_hoa_don=None):
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    suat_data = []
    for sc in ds_suat_chieu:
        suat_data.append({
            "ma_suat": sc.ma_suat,
            "ma_phim": sc.phim.ma_phim,
            "ten_phim": sc.phim.ten_phim,
            "thoi_luong": sc.phim.thoi_luong,
            "ma_phong": sc.phong.ma_phong,
            "ten_phong": sc.phong.ten_phong,
            "gio_chieu": sc.gio_chieu,
            "ds_ghe_dadat": list(sc.ds_ghe_dadat)
        })

    data = {
        "suat_chieu": suat_data,
        "hoa_don": ds_hoa_don if ds_hoa_don else []
    }

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def nap_du_lieu():
    if not os.path.exists(FILE_PATH):
        p1 = Phim("P01", "Nhà ba tôi một phòng", "120 phút")
        phong1 = PhongChieu("ROOM01", "Phòng 1")
        sc_mau = SuatChieu("SC01", p1, phong1, "09:00")

        p2 = Phim("P02", "Thỏ ơi", "127 phút")
        sc_mau2 = SuatChieu("SC02", p2, phong1, "09:15")

        ds_suat = [sc_mau, sc_mau2]
        luu_du_lieu(ds_suat, [])
        return ds_suat, []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        ds_suat = []
        suat_list = data.get("suat_chieu", [])
        for item in suat_list:
            p = Phim(item["ma_phim"], item["ten_phim"], item["thoi_luong"])
            ph = PhongChieu(item["ma_phong"], item["ten_phong"])
            sc = SuatChieu(item["ma_suat"], p, ph, item["gio_chieu"])
            sc.ds_ghe_dadat = set(item.get("ds_ghe_dadat", []))
            ds_suat.append(sc)

        ds_hoa_don = data.get("hoa_don", [])
        return ds_suat, ds_hoa_don
    except Exception:
        p1 = Phim("P01", "Nhà ba tôi một phòng", "120 phút")
        phong1 = PhongChieu("ROOM01", "Phòng 1")
        sc_mau = SuatChieu("SC01", p1, phong1, "09:00")
        return [sc_mau], []