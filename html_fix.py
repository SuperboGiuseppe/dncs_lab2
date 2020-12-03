import os

def main(html_path):
    old_html = open(os.path.abspath(html_path), "r")
    lines = old_html.readlines()
    old_html_data = old_html.read()
    old_html.close()
    new_html = open(os.path.abspath("test3.html"), "w")
    for line in lines:
        if line.strip("\n") != "<center>" and line.strip("\n") != "<h1>None</h1>" and line.strip("\n") != "</center>":
            if line.strip("\n") == "            width: 500px;":
                new_html.write('            width: 1023px;\n')
                continue
            if line.strip("\n") == "            height: 500px;":
                new_html.write('            height: 600px;\n')
                continue
            if line.strip("\n") == "            position: relative;":
                new_html.write('            position: center;\n')
                continue
            if line.strip("\n") == "            border: 1px solid lightgray;":
                new_html.write("            border: 0px solid lightgray;\n")
            new_html.write(line)
    new_html.close()