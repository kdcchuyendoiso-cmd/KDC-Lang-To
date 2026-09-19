"""Lớp lưu trữ bằng file Excel.

- Ghi từng sheet (không ghi lại cả file) và có khoá luồng để nhiều người gửi form cùng lúc không mất dữ liệu.
- Tự sao lưu file .bak trước mỗi lần ghi.
- Không phụ thuộc Streamlit nên dễ kiểm thử.
"""
from __future__ import annotations

import io
import os
import shutil
import threading
from pathlib import Path

import openpyxl
import pandas as pd

DATA_FILE = Path(os.environ.get("LANGTO_DATA_FILE") or Path(__file__).resolve().parent / "dulieu_langto.xlsx")

DEFAULT_COLUMNS: dict[str, list[str]] = {
    "ThongBao": ["Tiêu Đề", "Nội Dung", "Phân Loại", "Ngày Đăng", "Người Đăng", "Ghim Nổi Bật"],
    "DanhBaThon": ["Họ Tên", "Chức Vụ", "Số Điện Thoại", "Cán Bộ"],
    "SuKien": ["Tên Sự Kiện", "Mô Tả", "Thời Gian Bắt Đầu", "Địa Điểm", "Tổng Số Hộ Tham Gia"],
    "DangKySuKien": ["Họ Tên", "Tên Sự Kiện", "Số Lượng", "Ghi Chú", "Ngày Đăng Ký"],
    "CongKhaiThuChi": ["Ngày", "Nội Dung", "Thu (VNĐ)", "Chi (VNĐ)", "Ghi Chú"],
    "PhanAnh": ["Người Gửi", "Lĩnh Vực", "Nội Dung", "Địa Điểm", "Ngày Gửi", "Trạng Thái"],
    "VinhDanh": ["Họ Tên", "Danh Hiệu", "Lý Do Khen Thưởng", "Năm"],
    "ChoQue": ["Tên Sản Phẩm", "Phân Loại", "Giá Bán", "Đơn Vị", "Số Điện Thoại", "Ngày Đăng"],
    "DatLichNhaVanHoa": ["Họ Tên", "Dịch Vụ", "Ngày Sử Dụng", "Mục Đích", "Trạng Thái"],
}

_LOCK = threading.RLock()  # module chỉ import một lần nên khoá này dùng chung cho mọi phiên


# ---------------------------------------------------------------- nội bộ
def _sheet_names() -> list[str]:
    wb = openpyxl.load_workbook(DATA_FILE, read_only=True)
    try:
        return list(wb.sheetnames)
    finally:
        wb.close()


def _actual_name(sheet: str) -> str | None:
    lookup = {n.lower(): n for n in _sheet_names()}
    return lookup.get(sheet.lower())


def _backup() -> None:
    if DATA_FILE.exists():
        shutil.copy2(DATA_FILE, DATA_FILE.with_name(DATA_FILE.name + ".bak"))


def clean_dataframe(df: pd.DataFrame | None, sheet: str) -> pd.DataFrame:
    """Đưa về đúng bộ cột chuẩn, mọi ô là chuỗi, bỏ cột rác 'Unnamed'."""
    if df is None:
        df = pd.DataFrame()
    df = df.rename(columns=lambda c: str(c).strip())
    keep = [c for c in df.columns if not str(c).lower().startswith("unnamed")]
    df = df[keep].dropna(how="all").copy()
    cols = DEFAULT_COLUMNS.get(sheet)
    if cols:
        for c in cols:
            if c not in df.columns:
                df[c] = ""
        df = df[cols]
    for c in df.columns:
        col = df[c]
        if pd.api.types.is_datetime64_any_dtype(col):
            col = col.dt.strftime("%Y-%m-%d")
        col = col.astype(object).where(col.notna(), "")
        df[c] = col.astype(str).replace({"nan": "", "None": "", "NaT": ""})
    return df.reset_index(drop=True)


def _drop_blank_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    mask = df.apply(lambda row: any(str(v).strip() for v in row), axis=1)
    return df[mask].reset_index(drop=True)


# ---------------------------------------------------------------- API công khai
def ensure_file() -> None:
    """Tạo file Excel nếu chưa có, và bổ sung sheet còn thiếu."""
    with _LOCK:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            with pd.ExcelWriter(DATA_FILE, engine="openpyxl") as writer:
                for sheet, cols in DEFAULT_COLUMNS.items():
                    pd.DataFrame(columns=cols).to_excel(writer, sheet_name=sheet, index=False)
            return
        existing = {n.lower() for n in _sheet_names()}
        missing = [s for s in DEFAULT_COLUMNS if s.lower() not in existing]
        if missing:
            _backup()
            with pd.ExcelWriter(DATA_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                for sheet in missing:
                    pd.DataFrame(columns=DEFAULT_COLUMNS[sheet]).to_excel(writer, sheet_name=sheet, index=False)


def file_stamp() -> tuple[int, int]:
    """Dấu vết thay đổi của file - dùng làm khoá cache để dữ liệu luôn mới."""
    try:
        st_ = DATA_FILE.stat()
        return (st_.st_mtime_ns, st_.st_size)
    except FileNotFoundError:
        return (0, 0)


def read_sheet(sheet: str) -> pd.DataFrame:
    with _LOCK:
        if not DATA_FILE.exists():
            ensure_file()
        try:
            real = _actual_name(sheet)
            if real is None:
                return clean_dataframe(None, sheet)
            df = pd.read_excel(DATA_FILE, sheet_name=real, dtype=str, engine="openpyxl")
        except Exception:
            return clean_dataframe(None, sheet)
    return clean_dataframe(df, sheet)


def write_sheet(sheet: str, df: pd.DataFrame) -> None:
    """Thay toàn bộ một sheet bằng df. Ném lỗi nếu không ghi được."""
    df = _drop_blank_rows(clean_dataframe(df, sheet))
    with _LOCK:
        ensure_file()
        real = _actual_name(sheet) or sheet
        _backup()
        with pd.ExcelWriter(DATA_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=real, index=False)


def append_row(sheet: str, row: dict) -> None:
    with _LOCK:
        df = read_sheet(sheet)
        df.loc[len(df)] = [str(row.get(c, "")) for c in DEFAULT_COLUMNS[sheet]]
        write_sheet(sheet, df)


def export_bytes() -> bytes:
    with _LOCK:
        ensure_file()
        return DATA_FILE.read_bytes()


def restore_from_bytes(data: bytes) -> None:
    """Thay toàn bộ dữ liệu bằng file Excel tải lên (đã kiểm tra hợp lệ)."""
    try:
        wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True)
        names = {n.lower() for n in wb.sheetnames}
        wb.close()
    except Exception as exc:
        raise ValueError("Đây không phải file Excel (.xlsx) hợp lệ.") from exc
    if not names & {s.lower() for s in DEFAULT_COLUMNS}:
        raise ValueError("File không có sheet nào của hệ thống (ThongBao, DanhBaThon, SuKien...).")
    with _LOCK:
        _backup()
        tmp = DATA_FILE.with_name(DATA_FILE.name + ".tmp")
        tmp.write_bytes(data)
        os.replace(tmp, DATA_FILE)
        ensure_file()
