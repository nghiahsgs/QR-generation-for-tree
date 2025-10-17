#!/usr/bin/env python3
"""
QR Code Generator with PDF Export
Tạo mã QR và xuất ra PDF chuẩn A4 để in
"""

import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io
import os
from datetime import datetime

class QRCodePDFGenerator:
    def __init__(self):
        # Kích thước A4 trong points (1 inch = 72 points)
        self.page_width, self.page_height = A4

        # Kích thước QR code: 10cm x 10cm
        # 1 cm = 28.35 points (xấp xỉ)
        self.qr_size_cm = 10
        self.qr_size_points = self.qr_size_cm * 28.35

        # Margin cho trang
        self.margin = 30  # points

        # Tính số QR code trên một hàng và một cột
        self.qr_per_row = int((self.page_width - 2 * self.margin) / self.qr_size_points)
        self.qr_per_col = int((self.page_height - 2 * self.margin) / self.qr_size_points)

        print(f"📐 Kích thước trang A4: {self.page_width:.0f} x {self.page_height:.0f} points")
        print(f"📦 Kích thước QR: {self.qr_size_cm}cm x {self.qr_size_cm}cm ({self.qr_size_points:.0f} points)")
        print(f"📊 Số QR mỗi trang: {self.qr_per_row} x {self.qr_per_col} = {self.qr_per_row * self.qr_per_col} QR codes")

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
        """Tạo PDF chứa các mã QR"""
        pdf = canvas.Canvas(output_filename, pagesize=A4)

        # Thêm metadata
        pdf.setTitle("QR Codes for Printing")
        pdf.setAuthor("QR Generator App")

        current_qr = 0
        total_qrs = len(qr_data_list)

        while current_qr < total_qrs:
            # Vẽ QR codes cho trang hiện tại
            for row in range(self.qr_per_col):
                for col in range(self.qr_per_row):
                    if current_qr >= total_qrs:
                        break

                    # Tạo QR code
                    qr_img = self.generate_qr(qr_data_list[current_qr])

                    # Convert PIL image to bytes for ReportLab
                    img_buffer = io.BytesIO()
                    qr_img.save(img_buffer, format='PNG')
                    img_buffer.seek(0)

                    # Tính vị trí x, y cho QR code
                    x = self.margin + col * self.qr_size_points
                    # Tọa độ y trong PDF tính từ bottom lên
                    y = self.page_height - self.margin - (row + 1) * self.qr_size_points

                    # Vẽ QR code vào PDF
                    pdf.drawImage(ImageReader(img_buffer),
                                x, y,
                                width=self.qr_size_points,
                                height=self.qr_size_points,
                                preserveAspectRatio=True)

                    # Thêm text bên dưới QR (optional)
                    pdf.setFont("Helvetica", 8)
                    text = qr_data_list[current_qr]
                    if len(text) > 20:
                        text = text[:17] + "..."
                    pdf.drawString(x + 5, y - 10, text)

                    current_qr += 1

            # Thêm số trang
            pdf.setFont("Helvetica", 10)
            page_num = pdf.getPageNumber()
            pdf.drawString(self.page_width / 2 - 20, 20, f"Trang {page_num}")

            # Tạo trang mới nếu còn QR codes
            if current_qr < total_qrs:
                pdf.showPage()

        # Lưu PDF
        pdf.save()
        print(f"✅ Đã tạo file PDF: {output_filename}")
        print(f"📄 Tổng số trang: {pdf.getPageNumber()}")

        return output_filename

def main():
    """Hàm chính để demo"""
    print("🚀 QR Code Generator - PDF A4 Export")
    print("-" * 50)

    # Khởi tạo generator
    generator = QRCodePDFGenerator()

    # Dữ liệu mẫu cho QR codes
    # Bạn có thể thay đổi hoặc thêm dữ liệu tùy ý
    sample_data = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        # Thêm nhiều hơn nếu muốn test nhiều trang
    ]

    print(f"\n📝 Tạo {len(sample_data)} mã QR...")

    # Tạo thư mục output nếu chưa có
    if not os.path.exists("output"):
        os.makedirs("output")

    # Tạo tên file với timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output/qr_codes_{timestamp}.pdf"

    # Tạo PDF
    generator.create_pdf(sample_data, output_file)

    print(f"\n✨ Hoàn thành! File PDF đã sẵn sàng để in.")
    print(f"📍 Vị trí file: {os.path.abspath(output_file)}")
    print(f"\n💡 Tips: Khi in, chọn 'Actual Size' hoặc '100%' để giữ đúng kích thước 10x10cm")

if __name__ == "__main__":
    main()