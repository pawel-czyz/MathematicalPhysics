from os.path import join
import time

LECTURE_NOTES_DIR = "../rawLectureNotes"
BOOK_TEX = "book.tex"
TEMPLATE = "template.tex"


def remove(s, *args):
    for i in args:
        s = s.replace(i, "")
    return s

def prepare_tex(content):
    date = time.strftime("%d.%m.%Y", time.gmtime())
    with open(TEMPLATE, "r") as f:
        t = f.read()
    t = t.replace("$DATE", date)
    t = t.replace("$CONTENT", content)
    return t

def cut_problems_from_file(filename):
    ret = ""
    in_prob = False
    with open(filename, "r") as f:
        for line in f:
            if "\\newcommand" in line or "\\renewcommand" in line:
                ret = ret + line
            if "\\section" in line or "\\chapter" in line or "\\subsection" in line:
                ret = ret + line
            if "\\begin{prob}" in line:
                in_prob = True
            elif "\\end{prob}" in line:
                ret += line
                in_prob = False

            if "PROBLEMS END" in line:
                break

            if in_prob:
                ret += line
    return ret


def main():
    book_tex_path = join(LECTURE_NOTES_DIR, BOOK_TEX)
    all_problems = cut_problems_from_file(book_tex_path)
    with open(book_tex_path, "r") as f:
        problems_start = False
        for line in f:
            if "PROBLEMS START" in line:
                problems_start = True
            elif "PROBLEMS END" in line:
                problems_start = False

            if "%" in line or not problems_start:
                continue

            if "include" in line:
                name = remove(line, "\include", "{", "}", "\n")
                name = join(LECTURE_NOTES_DIR, name + ".tex")
                all_problems += cut_problems_from_file(name)

        print(prepare_tex(all_problems))

if __name__ == "__main__":
    main()
