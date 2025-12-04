#!/usr/bin/env python3
"""
QR Code Generator with PDF Export
Tạo mã QR và xuất ra PDF chuẩn A4 để in
QR codes link to: https://farm.agribeacon.tech/product-traceability/{qrCode}
"""

import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
import secrets
from datetime import datetime

# Domain configuration
BASE_URL = "https://farm.agribeacon.tech/product-traceability/"

class QRCodePDFGenerator:
    def __init__(self):
        # Kích thước A4 trong points (1 inch = 72 points)
        self.page_width, self.page_height = A4

        # Kích thước QR code: 10cm x 10cm
        # 1 cm = 28.35 points (xấp xỉ)
        self.qr_size_cm = 10
        self.qr_size_points = self.qr_size_cm * 28.35

        # Số QR mỗi trang: 3 QR theo chiều dọc
        self.qr_per_page = 3

        print(f"📐 Kích thước trang A4: {self.page_width:.0f} x {self.page_height:.0f} points")
        print(f"📦 Kích thước QR: {self.qr_size_cm}cm x {self.qr_size_cm}cm ({self.qr_size_points:.0f} points)")
        print(f"📊 Mỗi trang in {self.qr_per_page} QR codes, căn giữa")

    def generate_qr(self, data, error_correction=qrcode.constants.ERROR_CORRECT_L):
        """Tạo một mã QR từ dữ liệu"""
        qr = qrcode.QRCode(
            version=1,  # Version 1 = 21x21 modules
            error_correction=error_correction,
            box_size=10,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # In ra thông tin matrix size
        print(f"  QR '{data}': Version {qr.version} = {qr.modules_count}x{qr.modules_count} modules")

        # Tạo ảnh QR
        img = qr.make_image(fill_color="black", back_color="white")

        # Resize về kích thước chuẩn (pixels)
        # Với DPI 300 cho in ấn chất lượng cao
        dpi = 300
        pixel_size = int(self.qr_size_cm * dpi / 2.54)  # 2.54 cm = 1 inch
        img = img.resize((pixel_size, pixel_size), Image.Resampling.LANCZOS)

        return img

    def create_pdf(self, qr_data_list, output_filename="qr_codes.pdf"):
        """Tạo PDF chứa các mã QR - 3 QR mỗi trang, căn giữa theo chiều ngang"""
        pdf = canvas.Canvas(output_filename, pagesize=A4)

        # Thêm metadata
        pdf.setTitle("QR Codes for Printing")
        pdf.setAuthor("QR Generator App")

        total_qrs = len(qr_data_list)

        # Tính khoảng cách giữa các QR theo chiều dọc
        # Chia đều chiều cao trang cho 3 QR
        vertical_spacing = self.page_height / self.qr_per_page

        for i, qr_data in enumerate(qr_data_list):
            # Vị trí QR trong trang (0, 1, hoặc 2)
            position_in_page = i % self.qr_per_page

            # Tạo QR code
            qr_img = self.generate_qr(qr_data)

            # Convert PIL image to bytes for ReportLab
            img_buffer = io.BytesIO()
            qr_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)

            # Căn giữa theo chiều ngang
            x = (self.page_width - self.qr_size_points) / 2

            # Tính y để căn giữa trong từng phần 1/3 trang
            # Từ trên xuống: phần 0, 1, 2
            section_center_y = self.page_height - (position_in_page * vertical_spacing) - (vertical_spacing / 2)
            y = section_center_y - (self.qr_size_points / 2)

            # Vẽ QR code vào PDF
            pdf.drawImage(ImageReader(img_buffer),
                        x, y,
                        width=self.qr_size_points,
                        height=self.qr_size_points,
                        preserveAspectRatio=True)

            # Thêm text bên dưới QR (optional)
            pdf.setFont("Helvetica", 10)
            text = qr_data
            if len(text) > 60:
                text = text[:57] + "..."
            text_width = pdf.stringWidth(text, "Helvetica", 10)
            pdf.drawString((self.page_width - text_width) / 2, y - 20, text)

            # Tạo trang mới sau mỗi 3 QR codes
            if (i + 1) % self.qr_per_page == 0 and i < total_qrs - 1:
                pdf.showPage()

        # Lưu PDF
        pdf.save()
        print(f"✅ Đã tạo file PDF: {output_filename}")
        print(f"📄 Tổng số trang: {pdf.getPageNumber()}")

        return output_filename

def generate_qr_code(num_bytes=8):
    """
    Generate QR code string (16 hex characters) - same as backend
    Backend uses: crypto.randomBytes(8).toString('hex')
    Python equivalent: secrets.token_hex(8)
    """
    return secrets.token_hex(num_bytes)


def generate_traceability_url(qr_code):
    """Generate full traceability URL"""
    return f"{BASE_URL}{qr_code}"


def main():
    """Hàm chính để demo"""
    print("🚀 QR Code Generator - Farm Traceability")
    print("-" * 50)
    print(f"🌐 Domain: {BASE_URL}")

    # Khởi tạo generator
    generator = QRCodePDFGenerator()

    # Số lượng QR codes cần tạo
    num_qr_codes = 100

    # Generate QR codes giống backend (16 hex chars = 8 random bytes)
    qr_codes = [generate_qr_code() for _ in range(num_qr_codes)]

    # Tạo full URLs
    sample_data = [generate_traceability_url(code) for code in qr_codes]

    print(f"\n📝 Tạo {len(sample_data)} mã QR...")
    print(f"📌 Ví dụ URL: {sample_data[0]}")

    # Tạo thư mục output nếu chưa có
    if not os.path.exists("output"):
        os.makedirs("output")

    # Tạo tên file với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/qr_codes_{timestamp}.pdf"

    # Tạo PDF
    generator.create_pdf(sample_data, output_file)

    # Lưu danh sách QR codes ra file CSV để import vào database
    csv_file = f"output/qr_codes_{timestamp}.csv"
    with open(csv_file, 'w') as f:
        f.write("qr_code,full_url\n")
        for code, url in zip(qr_codes, sample_data):
            f.write(f"{code},{url}\n")
    print(f"📋 Đã lưu danh sách QR codes: {csv_file}")

    print(f"\n✨ Hoàn thành! File PDF đã sẵn sàng để in.")
    print(f"📍 Vị trí file: {os.path.abspath(output_file)}")
    print(f"\n💡 Tips: Khi in, chọn 'Actual Size' hoặc '100%' để giữ đúng kích thước 10x10cm")
    print(f"\n📊 QR Code Format:")
    print(f"   - Length: 16 hex characters")
    print(f"   - Example: {qr_codes[0]}")
    print(f"   - Full URL: {sample_data[0]}")

if __name__ == "__main__":
    main()