def write_content_to_file(content: str, path: str):
    if not file_exists(path):
        create_file(path)

    with open(path,"w+") as f:
        f.write(content)

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

