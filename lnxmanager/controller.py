import os


def change_directory() -> None:
    pass



if __name__ == "__main__":
    folder = '.'
    filepaths = [os.path.join(folder, i) for i in os.listdir(folder)]

    print(os.getcwd())
    os.chdir(str(os.path.abspath(os.sep)))
    print(os.getcwd())