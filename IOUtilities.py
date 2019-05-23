def write_content_to_file(content: str, path: str):
    if not file_exists(path):
        create_file(path)

    with open(path,"w+") as f:
        f.write(content)

def read_content_from_file(path: str) -> str:
    lines = ""

    with open(path,"r") as f:
        for line in f:
            lines += line

    return lines

def create_path(path: str):
    import os
    if not os.path.exists(path):
        os.makedirs(path)

def create_file(path: str):
    f = open(path, "w+")
    f.close()

def file_exists(path: str):
    import os
    return os.path.exists(path)