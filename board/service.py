import math


class Pageinfo:

    def __init__(self):
        self.total_count = 0
        self.start = 0

        self.total_page_count = 0
        self.page = 1
        self.next_page = 0
        self.prev_page = 0

        self.display = 5
        self.page_num = 5

    def set_page(self, page=1):
        self.page = page
        self.start = (self.page - 1) * self.display

        self.prev_page = math.floor(self.page / (self.page_num + 1)) * self.page_num
        self.next_page = self.prev_page + self.page_num + 1

    def set_total_count(self, total_count):
        self.total_count = total_count
        self.total_page_count = math.floor((total_count - 1) / self.display) + 1

    def page_range(self):
        return range(self.prev_page + 1,
                     self.next_page if self.next_page <= self.total_page_count else self.total_page_count + 1)

    def board_num(self):
        return self.total_count - (self.page - 1) * self.display + 1


if __name__ == '__main__':
    print(list(range(0, 10)))
