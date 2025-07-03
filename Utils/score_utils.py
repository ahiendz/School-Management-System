def tinh_diem_trung_binh_nam_theo_mon( hk1, hk2):
    if hk1 is not None and hk2 is not None:
        return round((hk1 + hk2*2) / 3, 1)
    else:
        return None

# sau này làm lại sau
def xep_loai_hoc_sinh(year_averages):
    mon_count = 4 # là số lượng các môn học đang tính điểm
    if len(year_averages) < 4:
        return None

    overall_avg = sum(year_averages) / mon_count

    if overall_avg >= 9:
        return "Xuất sắc"
    elif overall_avg >= 8:
        return "Giỏi"
    elif overall_avg >= 6.5:
        return "Khá"
    elif overall_avg >= 5:
        return "Trung bình"
    else:
        return "Yếu"
