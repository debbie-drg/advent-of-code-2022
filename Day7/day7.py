import sys

TOTAL_SPACE = 70000000
FREE_NEEDED = 30000000


class Folder:
    def __init__(self, name, parent):
        self.name = name
        self.files = dict()
        self.children = []
        self.size = 0
        self.parent = parent

    def __repr__(self) -> str:
        return (
            f"Folder {self.get_location()} of size {self.compute_size()}"
        )

    def get_location(self) -> str:
        try:
            if self.parent.name == "/":
                return f"/{self.name}"
            else:
                return f"{self.parent.get_location()}/{self.name}"
        except AttributeError:
            return "/"

    def add_file(self, name: str, size: int):
        self.files[name] = size
        if self.size is not None:
            self.size += size

    def add_subfolder(self, subfolder):
        self.children.append(subfolder)
        self.size = None

    def get_subfolder_names(self) -> list[str]:
        return [children.name for children in self.children]

    def get_subfolder(self, name: str | list[str]):
        if isinstance(name, list):
            if len(name) > 1:
                next_child = name[0]
                for child in self.children:
                    if child.name == next_child:
                        return child.get_subfolder(name[1:])
                print("Folder does not exist.")
                return None
            else:
                name = name[0]
        for child in self.children:
            if child.name == name:
                return child
        print("Folder does not exist.")
        return None

    def get_sizes(self):
        sizes = [self.compute_size()]
        for child in self.children:
            sizes += child.get_sizes()
        return sizes

    def get_subfolders(self):
        subfolders = [self]
        for child in self.children:
            subfolders += child.get_subfolders()
        return subfolders

    def folder_attributes(self, depth: int = 0) -> str:
        attributes = (
            f"{2 * depth * ' '}- {self.name} (dir, size={self.compute_size()})\n"
        )
        for file in self.files:
            attributes += (
                f"{2 * (depth + 1) * ' '}- {file} (file, size={self.files[file]})\n"
            )
        for subfolder in self.children:
            attributes += subfolder.folder_attributes(depth=depth + 1)
        return attributes

    def compute_size(self) -> int:
        if self.size is not None:
            return self.size
        size = 0
        for file in self.files:
            size += self.files[file]
        for children in self.children:
            size += children.compute_size()
        self.size = size
        return size


class FileSystem:
    def __init__(self):
        self.root = Folder(name="/", parent=None)

    def __repr__(self) -> str:
        return self.root.folder_attributes()

    def get_folders(self) -> list[Folder]:
        return self.root.get_subfolders()

    def get_folder_sizes(self) -> list[int]:
        return self.root.get_sizes()

    def total_space_used(self) -> int:
        return self.root.compute_size()

    def get_folder(self, path: str) -> Folder:
        path = path.removeprefix("/")
        split_path = path.split("/")
        return self.root.get_subfolder(split_path)


def parse_command(line: str, current_folder: Folder) -> Folder:
    split_line = line.split(" ")
    if split_line[0] == "$":
        if split_line[1] == "cd":
            return command_cd(split_line[2], current_folder)
        return current_folder
    if split_line[0] != "dir":
        current_folder.add_file(name=split_line[1], size=int(split_line[0]))
    return current_folder


def command_cd(folder_name: str, current_folder: Folder) -> Folder:
    if folder_name == "..":
        if current_folder.parent is not None:
            return current_folder.parent
        return current_folder
    if folder_name == "/":
        return current_folder
    if folder_name not in current_folder.get_subfolder_names():
        new_folder = Folder(name=folder_name, parent=current_folder)
        current_folder.add_subfolder(new_folder)
        return new_folder
    return current_folder.get_subfolder(folder_name)


# These two are the functions that solve the tasks


def sum_folder_size_at_most(folder_sizes: list[int], max_size: int = 100000):
    return sum(filter(lambda x: x < max_size, folder_sizes))


def folder_to_delete(
    folder_sizes: list[int], total_used: int, total_size: int, free_size_needed: int
):
    need_to_free = free_size_needed - (total_size - total_used)
    assert need_to_free > 0, "There already is enough space available."
    return min(filter(lambda x: x > need_to_free, folder_sizes))


if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except IndexError:
        file_name = "input.txt"
    size_count = 0
    commands = open(file_name).read().split(sep="\n")
    commands.remove("")

    file_system = FileSystem()
    current_folder = file_system.root

    for line in commands:
        current_folder = parse_command(line, current_folder)

    print("This is what the file system looks like.\n")
    print(file_system)

    # To solve the task we need the sizes of all folders.
    folder_sizes = file_system.get_folder_sizes()

    folders_less_than_100000 = sum_folder_size_at_most(folder_sizes, max_size=100000)
    smallest_directory_to_remove = folder_to_delete(
        folder_sizes,
        total_used=file_system.total_space_used(),
        total_size=TOTAL_SPACE,
        free_size_needed=FREE_NEEDED,
    )

    print(
        f"The total size of the folders of less than 100000 is {folders_less_than_100000}."
    )
    print(f"The size of the directory to delete is {smallest_directory_to_remove}.")
