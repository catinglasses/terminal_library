from utils import Library, request_num

def main():
    library = Library()

    while True:
        print("Меню:")
        print("1. Отобразить все книги")
        print("2. Найти книгу(-и)")
        print("3. Добавить книгу")
        print("4. Удалить книгу")
        print("5. Изменить статус книги")
        print("6. Выйти\n")

        choice = input("Выберите опцию из меню, указав соотв. номер (1-6):  ")

        if choice == "1":
            library.display_books()

        elif choice == "2":
            result = library.find_books(search_condition=input("Введите название, автора или год для поиска:  "))
            if result:
                for book in result:
                    print(f"\nНайдена книга - ID: {book.book_id};\nНазвание: {book.title};\nАвтор: {book.author};\nГод: {book.year};\nСтатус: {book.status}\n")
            else:
                print("Ничего не найдено.\n")


        elif choice == "3":
            title = input("Введите название книги:  ")
            author = input("Введите автора книги:  ")
            year = request_num("Введите год издания книги:  ")
            library.add_book(title, author, year)

        elif choice == "4":
            book_id = request_num("Введите ID книги на удаление:  ")
            library.remove_book(book_id)

        elif choice == "5":
            book_id = request_num("Введите ID книги для изменения статуса:  ")
            library.change_status(book_id, new_status=input('Укажите статус (в наличии/выдана):  '))

        elif choice == "6":
            if input("Вы уверены? (y/n - Да/Нет)  ") in ["y", "Да", "да"]:
                print("Завершение программы...")
                break
            else:
                print()
                main()
        
        else:
            print("Пожалуйста, укажите корректный номер (1-6).\n")


if __name__ == "__main__":
    main()