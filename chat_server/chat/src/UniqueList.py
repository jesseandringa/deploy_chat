class UniqueList:
    def __init__(self, lst: list):
        self.lst = lst

    def append(self, item: any):
        if item not in self.lst:
            self.lst.append(item)

    def __getitem__(self, index: int):
        return self.lst[index]

    def __contains__(self, item: any):
        return item in self.lst

    def __len__(self):
        return len(self.lst)

    def __str__(self):
        return str(self.lst)

    def extend(self, lst: list):
        for item in lst:
            self.append(item)

    def remove(self, item: any):
        self.lst.remove(item)
