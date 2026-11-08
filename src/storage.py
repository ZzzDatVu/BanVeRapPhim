import json
import os

# Trỏ thẳng ra thư mục data ở gốc project (ngoài thư mục src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, "data", "database.json")


def luu_du_lieu(ds_suat_chieu, ds_hoa_don):
    """Lưu danh sách suất chiếu (ghế đã đặt) và hóa đơn ra file JSON."""
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    hoa_don_data = []
    for hd in ds_hoa_don:
        suat_hd = hd.ds_ve[0].suat if hasattr(hd, 'ds_ve') and hd.ds_ve else None

        hoa_don_data.append({
            "ma_hd": getattr(hd, 'ma_hd', 'HD01'),
            "ten_phim": suat_hd.phim.ten_phim if suat_hd else "Unknown",
            "gio_chieu": suat_hd.gio_chieu if suat_hd else "00:00",
            "ds_ghe": [ve.ghe.ten() for ve in hd.ds_ve] if hasattr(hd, 'ds_ve') else [],
            "tong_tien": hd.tinh_tong() if hasattr(hd, 'tinh_tong') else 0,
            "trang_thai": getattr(hd, 'trang_thai', 'DA_THANH_TOAN')
        })

    data = {
        "suat_chieu": [
            {
                "ma_phim": sc.phim.ma_phim,
                "gio_chieu": sc.gio_chieu,
                "phong": sc.phong.ten_phong,
                "ds_ghe_dadat": list(sc.ds_ghe_dadat)
            }
            for sc in ds_suat_chieu
        ],
        "hoa_don": hoa_don_data
    }

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def nap_du_lieu(ds_suat_chieu):
    """Khởi động ứng dụng: Đọc file JSON để khôi phục lại trạng thái ghế."""
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Nạp lại các ghế đã đặt vào từng suất chiếu tương ứng
        for sc_data in data.get("suat_chieu", []):
            for sc in ds_suat_chieu:
                if sc.phim.ma_phim == sc_data["ma_phim"] and sc.gio_chieu == sc_data["gio_chieu"]:
                    sc.ds_ghe_dadat = set(sc_data["ds_ghe_dadat"])

        return data.get("hoa_don", [])
    except (json.JSONDecodeError, Exception):
        return []