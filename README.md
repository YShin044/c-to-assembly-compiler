# \# Simple C Compiler in Python

# 

# \## Tổng quan

# 

# Đây là một trình biên dịch đơn giản dành cho tập con của ngôn ngữ C, được phát triển bằng Python. Trình biên dịch này chuyển mã nguồn C thành mã hợp ngữ x86-64 theo cú pháp NASM, sau đó dùng NASM và GCC để tạo file thực thi. Dự án được thực hiện như đồ án cuối kỳ môn "Lập trình hệ thống" tại Trường Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE).

# 

# \## Tính năng

# 

# \- Hỗ trợ cú pháp C cơ bản:

# &nbsp; - Biến kiểu `int`, `char` và `string`

# &nbsp; - Biểu thức số học: `+`, `-`, `\*`, `/`

# &nbsp; - Câu lệnh điều kiện: `if`, `else`

# &nbsp; - Hàm I/O: `printf`, `scanf`

# &nbsp; - Lệnh `return`

# \- Sinh mã hợp ngữ x86-64 (NASM syntax)

# \- Tích hợp giao diện đồ họa Tkinter

# \- Gọi NASM và GCC tự động để tạo file thực thi

# 

# \## Kiến trúc Compiler

# 

# +-------------+ +-----------+ +-------------+ +--------------+

# | C Source | ---> | Lexer | ---> | Parser | ---> | CodeGen |

# +-------------+ +-----------+ +-------------+ +--------------+

# |

# v

# +------------------+

# | NASM Assembler |

# | GCC Linker |

# +------------------+

# 

# \## Cấu trúc thư mục

# 

# sourcecode/

# ├── compiler.py # Compiler chính: lexer, parser, codegen

# ├── code\_editer.py # Giao diện người dùng (Tkinter)

# ├── grammar.md # Cú pháp hỗ trợ

# └── program.c # File C mẫu để kiểm thử

# 

# \## Cách sử dụng

# 

# \### Yêu cầu

# 

# \- Python 3.x

# \- NASM

# \- GCC (trên Linux)

# 

# \### Các bước chạy

# 

# 1\. Cài đặt các công cụ cần thiết (trên Ubuntu/Debian):

# 

# &nbsp;  ```bash

# &nbsp;  sudo apt install nasm gcc python3

# 2\. Mở GUI:

# 3\. python3 UI\_Compiler.py

# 3\. Viết hoặc mở một file .c đơn giản → nhấn Compile

# Trình biên dịch sẽ:

# o	Phân tích mã nguồn

# o	Sinh file output.asm

# o	Gọi NASM → output.o

# o	Gọi GCC → file thực thi output

# Ví dụ mã C được hỗ trợ:



# int main() {

# 

# &nbsp;   int x = 10;

# &nbsp;   int y = 5;

# &nbsp;   

# &nbsp;   printf("Nhập tên của bạn:\\n");

# &nbsp;   string name;

# &nbsp;   scanf("%s", name); 

# &nbsp;   

# &nbsp;   printf("Nhập tuổi của bạn:\\n");

# &nbsp;   int age;

# &nbsp;   scanf("%d", \&age);

# &nbsp;   

# &nbsp;   string hello = "Xin chào\\n";

# &nbsp;   printf("In ra: %s", hello);

# &nbsp;   printf("\\nIn ra: %s", name);

# &nbsp;   printf("\\nIn ra: %d", age);

# &nbsp;   int hieu;

# &nbsp;   if (x > y) {

# &nbsp;       hieu = x - y;

# &nbsp;       printf("\\nHiệu của x và y là %d\\n", hieu);

# &nbsp;   }

# &nbsp;   else {

# &nbsp;	    hieu = y - x;

# &nbsp;       printf("\\nhiệu của y và x là %d\\n", hieu);

# &nbsp;   }

# &nbsp;   

# &nbsp;   int tong = x + y;

# &nbsp;   int tich = x \* y;

# &nbsp;   int thuong = x / y;

# &nbsp;   

# &nbsp;   printf("%d  ", tong);

# &nbsp;   printf("%d  ", tich);

# &nbsp;   printf("%d\\n", thuong);

# &nbsp;   

# &nbsp;   while (tong > 0) {

# &nbsp;       printf("%d > 0\\n", tong);

# &nbsp;       tong = tong - 1;

# &nbsp;   }

# &nbsp;   

# &nbsp;   return 0;

# }



# Hạn chế

# •	Không hỗ trợ:

# o	Hàm con ngoài main

# o	Vòng lặp (while, for)

# o	Con trỏ, mảng, struct

# o	Biểu thức phức tạp trong một dòng

# •	Báo lỗi cú pháp cơ bản

# &nbsp;Tác giả

# •	Nguyễn Minh Tâm – 22162039



