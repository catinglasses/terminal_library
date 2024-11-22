import json
import os

class Book:
    """Класс книги."""
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "В наличии"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """Конвертация данных в словарь"""
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

class BookRepository:
    """Класс для работы с хранилищем книг. Отвечает только за операции, связанные с манипуляциями объектом класса Book."""
    def __init__(self, filename: str):
        self.filename = filename
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.books = [Book(**book_data) for book_data in data]

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False)

    def add_book(self, new_book: Book):
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id: int):
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                self.save_books()
                return True
        return False

class BookSearcher:
    """Класс для поиска книг. Отвечает только за поиск книг."""
    def __init__(self, books: list):
        self.books = books

    def find_by_title(self, search_title: str) -> list:
        return [book for book in self.books if search_title.lower() in book.title.lower()]

    def find_by_author(self, search_author: str) -> list:
        return [book for book in self.books if search_author.lower() in book.author.lower()]

    def find_by_year(self, search_year: int) -> list:
        return [book for book in self.books if book.year == search_year]

class Library:
    """Основной класс приложения."""
    def __init__(self):
        self.repository = BookRepository("library.json")
        self.searcher = BookSearcher(self.repository.books)
        self.search_cache = {}

    def add_book(self, title: str, author: str, year: int):
        book_id = len(self.repository.books) + 1 # Автоинкремент ID для каждой добавляемой книги
        new_book = Book(book_id, title, author, year)
        self.repository.add_book(new_book)
        print(f"Книга {title} добавлена.\n")

    def remove_book(self, book_id: int):
        if self.repository.remove_book(book_id):
            print(f"Книга с ID {book_id} была удалена.\n")
        else:
            print(f"Книга с ID {book_id} не найдена.\n")

    def find_books(self, search_condition: str) -> list:
        if search_condition in self.search_cache:       # Проверка наличия в кэше
            return self.search_cache[search_condition]

        found_books = []

        if search_condition.isdigit():
            found_books.extend(self.searcher.find_by_year(int(search_condition)))

        found_books.extend(self.searcher.find_by_title(search_condition))
        found_books.extend(self.searcher.find_by_author(search_condition))

        unique_books = {book.book_id: book for book in found_books}.values()
        self.search_cache[search_condition] = list(unique_books)        # Простая реализация кэширования

        return list(unique_books)

    def display_books(self):
        print()
        if not self.repository.books:
            print("Библиотека пуста.\n")
            return
        for book in self.repository.books:
            print(f"ID: {book.book_id};\nНазвание: {book.title};\nАвтор: {book.author};\nГод: {book.year};\nСтатус: {book.status}")
            print()

    def change_status(self, book_id: int, new_status: str):
        STATUS_NAMES = ['в наличии', 'выдана']
        
        if new_status not in STATUS_NAMES:
            print('Указан неверный статус. Укажите статус "в наличии" или "выдана".\n')
            return
        
        for book in self.repository.books:
            if book.book_id == book_id:
                book.status = new_status
                self.repository.save_books()
                print(f"Статус книги {book.title} был изменен на {new_status}.\n")
                return
        print(f"Книга с ID {book_id} не найдена.\n")

def request_num(instruction):
    """Конвертация данных на входе в целочисленное и обработка ошибки."""
    while True:
        num = input(instruction)

        if not num.isdigit():
            print(
                "Ошибка: введенное значение не является числом."
            )
            return request_num("\nВведите новое число:  ")
        else:
            num = int(num)
            break

    return num
