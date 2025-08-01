int main() {
    int x = 10;
    int y = 5;
    
    printf("Nhập tên của bạn:\n");
    string name;
    scanf("%s", name); 
    
    printf("Nhập tuổi của bạn:\n");
    int age;
    scanf("%d", &age);
    
    string hello = "Xin chào\n";
    printf("In ra: %s", hello);
    printf("\nIn ra: %s", name);
    printf("\nIn ra: %d", age);
    int hieu;
    if (x > y) {
        hieu = x - y;
        printf("\nHiệu của x và y là %d\n", hieu);
    }
    else {
	    hieu = y - x;
        printf("\nhiệu của y và x là %d\n", hieu);
    }
    
    int tong = x + y;
    int tich = x * y;
    int thuong = x / y;
    
    printf("%d  ", tong);
    printf("%d  ", tich);
    printf("%d\n", thuong);
    
    while (tong > 0) {
        printf("%d > 0\n", tong);
        tong = tong - 1;
    }
    
    return 0;
}