# Trình biên dịch C đơn giản bằng Python

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> Một trình biên dịch cơ bản cho một tập con của ngôn ngữ C, được xây dựng bằng Python. Dự án này chuyển đổi mã nguồn C thành tệp thực thi x86-64 trên môi trường Linux.

Đây là đồ án môn học "Lập trình hệ thống" tại Trường Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE).

---

## ✨ Tính năng chính

-   **Hỗ trợ cú pháp C cơ bản:**
    -   Khai báo biến: `int`, `char`, và `string`.
    -   Các phép toán số học: `+`, `-`, `*`, `/`.
    -   Cấu trúc điều khiển: `if`, `else`.
    -   Hàm I/O chuẩn: `printf`, `scanf`.
    -   Câu lệnh `return` trong hàm `main`.
-   **Sinh mã Hợp ngữ x86-64:** Tự động tạo mã assembly tương thích với cú pháp của NASM.
-   **Tự động hóa Build:** Tự động gọi `nasm` và `gcc` để tạo tệp thực thi cuối cùng.
-   **Giao diện đồ họa (GUI):** Tích hợp giao diện đơn giản bằng Tkinter để soạn thảo, mở tệp và biên dịch.

## 🏗️ Kiến trúc Trình biên dịch

Luồng xử lý của trình biên dịch được thiết kế theo các giai đoạn kinh điển:

```bash
+------------+ +---------+ +----------+ +----------------+
| Mã nguồn C |----->| Lexer |----->| Parser |----->| Code Generator |
+------------+ +---------+ +----------+ +----------------+
|
v
+--------------------+
| Mã Assembly |
| (output.asm) |
+--------------------+
|
v (Sử dụng nasm & gcc)
+--------------------+
| Tệp thực thi |
| (output) |
+--------------------+
```

## 🚀 Bắt đầu

### Yêu cầu hệ thống

-   **Hệ điều hành:** Linux (khuyến nghị Ubuntu/Debian)
-   **Ngôn ngữ:** Python 3.x
-   **Công cụ:** `nasm`, `gcc`, `python3-tk`

### Cài đặt

1.  Mở Terminal và cập nhật package list:
    ```bash
    sudo apt update
    ```

2.  Cài đặt các công cụ cần thiết:
    ```bash
    sudo apt install nasm gcc python3-tk
    ```

## 🛠️ Hướng dẫn sử dụng

1.  Clone repository này về máy của bạn (hoặc tải mã nguồn về).

2.  Di chuyển vào thư mục chứa mã nguồn:
    ```bash
    cd /path/to/your/sourcecode
    ```

3.  Chạy giao diện đồ họa:
    ```bash
    python3 UI_Compiler.py
    ```

4.  **Sử dụng chương trình:**
    -   Viết mã C trực tiếp vào trình soạn thảo hoặc mở một tệp `.c` có sẵn.
    -   Nhấn nút **"Compile"**.
    -   Quá trình biên dịch sẽ tự động thực hiện:
        1.  Phân tích mã nguồn và tạo tệp `output.asm`.
        2.  Sử dụng `nasm` để dịch `output.asm` thành `output.o`.
        3.  Sử dụng `gcc` để liên kết (link) `output.o` và tạo tệp thực thi `output`.

## 📁 Cấu trúc thư mục
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

sourcecode/
├── 📜 compiler.py # Lõi của trình biên dịch (Lexer, Parser, Code Generator)
├── 🎨 code_editer.py # Giao diện người dùng (Tkinter)
├── 📖 grammar.md # Mô tả cú pháp C được hỗ trợ
└── 🧪 program.c # Tệp mã nguồn C mẫu để kiểm thử

Generated code
## 📝 Ví dụ mã nguồn C

Đoạn mã dưới đây minh họa các tính năng mà trình biên dịch hiện đang hỗ trợ.

```c
int main() {
    printf("Nhap ten cua ban:\n");
    string name;
    scanf("%s", name);

    printf("Nhap tuoi cua ban:\n");
    int age;
    scanf("%d", &age);

    string hello = "Xin chao ";
    printf("%s%s, %d tuoi.\n", hello, name, age);

    int x = 20;
    int y = 10;
    int ketqua;

    if (x > y) {
        ketqua = x - y;
        printf("Hieu cua x va y la: %d\n", ketqua);
    } else {
        ketqua = y - x;
        printf("Hieu cua y va x la: %d\n", ketqua);
    }

    int tong = x + y;
    printf("Tong: %d\n", tong);

    return 0;
}
```
## ⚠️ Hạn chế

Trình biên dịch này được xây dựng cho mục đích học tập và có một số hạn chế:
-   Chỉ hỗ trợ hàm `main`, không hỗ trợ hàm do người dùng định nghĩa.
-   Chưa hỗ trợ vòng lặp (`for`, `while`).
-   Chưa hỗ trợ các kiểu dữ liệu phức tạp như con trỏ, mảng, `struct`.
-   Khả năng xử lý biểu thức lồng nhau còn hạn chế.
-   Hệ thống báo lỗi cú pháp còn ở mức cơ bản.

## ✍️ Tác giả

-   **Nguyễn Minh Tâm**
-   GitHub: [YShin044](https://github.com/YShin044)
