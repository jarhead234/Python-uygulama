import random
from IPython.display import clear_output

def create_puzzle():
    # 1-8 arası sayılar ve bir boşluk içeren bir liste oluşturun
    puzzle = list(range(1, 9)) + [' ']
    # random.shuffle() kullanmadan özel karıştırma uygulaması
    for i in range(len(puzzle)-1, 0, -1):
        j = random.randint(0, i)
        puzzle[i], puzzle[j] = puzzle[j], puzzle[i]
    return puzzle

def print_puzzle(puzzle):
    clear_output(wait=True)
    for i in range(0, 9, 3):
        print('  '.join(str(x) for x in puzzle[i:i+3]))

def find_empty_position(puzzle):
    return puzzle.index(' ')

def is_valid_move(puzzle, move):
    empty_pos = find_empty_position(puzzle)
    if move == 'w':  # yukarı
        return empty_pos not in [0, 1, 2]
    elif move == 's':  # aşağı
        return empty_pos not in [6, 7, 8]
    elif move == 'a':  # sol
        return empty_pos not in [0, 3, 6]
    elif move == 'd':  # sağ
        return empty_pos not in [2, 5, 8]
    return False

def make_move(puzzle, move):
    empty_pos = find_empty_position(puzzle)
    if move == 'w':  # yukarı
        puzzle[empty_pos], puzzle[empty_pos-3] = puzzle[empty_pos-3], puzzle[empty_pos]
    elif move == 's':  # aşağı
        puzzle[empty_pos], puzzle[empty_pos+3] = puzzle[empty_pos+3], puzzle[empty_pos]
    elif move == 'a':  # sol
        puzzle[empty_pos], puzzle[empty_pos-1] = puzzle[empty_pos-1], puzzle[empty_pos]
    elif move == 'd':  # sağ
        puzzle[empty_pos], puzzle[empty_pos+1] = puzzle[empty_pos+1], puzzle[empty_pos]

def is_solved(puzzle):
    return puzzle == [1, 2, 3, 4, 5, 6, 7, 8, ' ']

def main():
    puzzle = create_puzzle()
    print("Kaydırma Bulmaca Oyununa Hoş Geldiniz!")
    print("Boş alanı hareket ettirmek için w (yukarı), s (aşağı), a (sol), d (sağ) tuşlarını kullanın")
    print("Sayıları 1'den 8'e kadar sıralamaya çalışın")
    
    while True:
        print_puzzle(puzzle)
        if is_solved(puzzle):
            print("Tebrikler puzzle çözüldü!")
            break
            
        move = input("Hareketinizi girin (w/a/s/d): ").lower()
        if move in ['w', 'a', 's', 'd']:
            if is_valid_move(puzzle, move):
                make_move(puzzle, move)
            else:
                print("Geçersiz hareket! Tekrar deneyin.")
        else:
            print("Geçersiz giriş! w, a, s veya d tuşlarını kullanın.")

if __name__ == "__main__":
    main()