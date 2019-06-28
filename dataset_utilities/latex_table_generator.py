class LatexTableGenerator:
    @staticmethod
    def generate_table_for_dataset(dataset_path: str):
        import re

        _category_regex = re.compile("[A-Za-z]+:")
        _document_regex = re.compile(".*,http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

        start = True

        with open(dataset_path, "r") as f:
            current_category = ""

            for line in f:
                if line[:2] == "//": #Ignore Comments
                    continue

                stripped_line = line.rstrip()
                if _category_regex.match(stripped_line):
                    if not start:
                        print("     \\hline")
                        print("     \\end{tabular}")
                        print("     }")
                        print("     \\caption{Documents for the test set category " + current_category[:-1] + "}")
                        print("\\end{table}")

                    current_category = stripped_line

                    print("\\begin{table}[H]")
                    print("     \\centerline")
                    print("     {")
                    print("     \\begin{tabular}{|l|l|}")
                    print("     \\hline")
                    print("     \\textbf{"+stripped_line+"} & \\\\")
                    print("     \\textbf{Device Name} & \\textbf{Url} \\\\ \\hline")


                    start = False

                elif _document_regex.match(stripped_line):
                    line_tokens = stripped_line.split(",")
                    document_name = line_tokens[0]
                    url = line_tokens[1]
                    if len(url) >= 60:
                        print("     "+document_name+" & \\url{" + url[:60] + "...} \\\\")
                    else:
                        print("     " + document_name + " & \\url{" + url + "} \\\\")

            print("     \\hline")
            print("     \\end{tabular}")
            print("     }")
            print("     \\caption{Documents for the test set category " + current_category[:-1] + "}")
            print("\\end{table}")



if __name__ == "__main__":
    import constants,os
    LatexTableGenerator.generate_table_for_dataset(os.path.join(constants.DATA_DIR,"dataset_urls.txt"))