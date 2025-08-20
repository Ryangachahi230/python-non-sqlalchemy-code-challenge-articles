# lib/classes/many_to_many.py

class Author:
    def __init__(self, name):
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Immutable after first assignment
        if hasattr(self, "_name"):
            return
        if not isinstance(value, str):
            raise Exception("Author name must be a string")
        if len(value) == 0:
            raise Exception("Author name cannot be empty")
        self._name = value

    def articles(self):
        """Return all Article instances written by this author"""
        return [article for article in Article.all if article.author == self]

    def add_article(self, magazine, title):
        """Create a new Article instance for this author"""
        return Article(self, magazine, title)

    def magazines(self):
        """Return all unique Magazine instances this author has written for"""
        return list({article.magazine for article in self.articles()})

    def topic_areas(self):
        """Return a list of unique categories for all magazines this author has written for"""
        mags = self.magazines()
        if not mags:
            return None
        return list({mag.category for mag in mags})


class Magazine:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Test expects invalid assignments to be ignored silently
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # Test expects invalid assignments to be ignored silently
        if isinstance(value, str) and len(value) > 0:
            self._category = value

    def articles(self):
        """Return all Article instances written for this magazine"""
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        """Return unique authors who wrote for this magazine"""
        return list({article.author for article in self.articles()})

    def article_titles(self):
        """Return a list of titles of all articles for this magazine"""
        articles = self.articles()
        if not articles:
            return None
        return [article.title for article in articles]

    def contributing_authors(self):
        """Return authors who wrote more than 2 articles for this magazine"""
        articles = self.articles()
        if not articles:
            return None
        author_count = {}
        for article in articles:
            author_count[article.author] = author_count.get(article.author, 0) + 1
        authors = [author for author, count in author_count.items() if count > 2]
        return authors if authors else None


class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if hasattr(self, "_title"):
            # immutable after being set once
            raise Exception("Title is immutable")
        if not isinstance(value, str):
            raise Exception("Title must be a string")
        if not (5 <= len(value) <= 50):
            raise Exception("Title must be between 5 and 50 characters")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("Author must be of type Author")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise Exception("Magazine must be of type Magazine")
        self._magazine = value
