# QR Code Generator với PDF Export (A4)

Ứng dụng Python tạo mã QR và xuất ra file PDF chuẩn A4 để in ấn.

## Tính năng

- ✅ Tạo mã QR kích thước 10cm x 10cm
- ✅ Xuất PDF chuẩn A4 (210mm x 297mm)
- ✅ Tự động sắp xếp nhiều QR trên một trang
- ✅ Hỗ trợ in ấn chất lượng cao (300 DPI)

## Cài đặt

1. Tạo virtual environment:
```bash
python3 -m venv venv
```

2. Kích hoạt venv:
```bash
source venv/bin/activate  # macOS/Linux
# hoặc
venv\Scripts\activate  # Windows
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy demo:
```bash
python qr_generator.py
```

### Sử dụng trong code:
```python
from qr_generator import QRCodePDFGenerator

# Khởi tạo generator
generator = QRCodePDFGenerator()

# Danh sách dữ liệu cho QR codes
qr_data = [
    "https://example.com/tree/001",
    "TREE-ID-002",
    "Cây số 3",
    # Thêm nhiều dữ liệu...
]

# Tạo PDF
generator.create_pdf(qr_data, "output.pdf")
```

## Thông số kỹ thuật

- **Kích thước QR**: 10cm x 10cm
- **Trang PDF**: A4 (210mm x 297mm)
- **Số QR mỗi trang**: 2 QR codes (1 cột x 2 hàng)
- **Chất lượng**: 300 DPI cho in ấn

## Lưu ý khi in

⚠️ **QUAN TRỌNG**: Khi in file PDF, hãy chọn:
- Scale: **100%** hoặc **Actual Size**
- KHÔNG chọn "Fit to Page" hoặc "Shrink to Fit"

Điều này đảm bảo mã QR giữ đúng kích thước 10cm x 10cm.

## Output

File PDF được lưu trong thư mục `output/` với format:
```
output/qr_codes_YYYYMMDD_HHMMSS.pdf
```