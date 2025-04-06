def delete_row_col(matrix, row, col):
    """
    Verilen matristen belirtilen satır ve sütunu siler
    """
    return [[matrix[i][j] for j in range(len(matrix)) if j != col] 
            for i in range(len(matrix)) if i != row]

def determinant(matrix):
    """
    Kare matrisin determinantını cofaktör açılımı ile hesaplar
    """
    size = len(matrix)
    
    # Base case: 1x1 matris için
    if size == 1:
        return matrix[0][0]
    
    # Base case: 2x2 matris için
    if size == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    # İlk satır üzerinden cofaktör açılımı
    for j in range(size):
        cofactor = matrix[0][j] * ((-1) ** j) * determinant(delete_row_col(matrix, 0, j))
        det += cofactor
    
    return det

def get_valid_int(prompt):
    """
    Kullanıcıdan geçerli bir tam sayı alır
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Lütfen geçerli bir tam sayı giriniz!")

def main():
    # Matris boyutunu al
    while True:
        n = get_valid_int("Matrisin boyutunu giriniz (pozitif tam sayı): ")
        if n > 0:
            break
        print("Lütfen pozitif bir tam sayı giriniz!")
    
    # Matrisi oluştur
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            while True:
                value = get_valid_int(f"{i+1}. satır {j+1}. sütun elemanını giriniz: ")
                row.append(value)
                break
        matrix.append(row)
    
    # Matrisi göster
    print("\nGirilen matris:")
    for row in matrix:
        print(row)
    
    # Determinantı hesapla ve göster
    det = determinant(matrix)
    print(f"\nMatrisin determinantı: {det}")

if __name__ == "__main__":
    main() 