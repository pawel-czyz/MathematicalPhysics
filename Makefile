book:
	cd rawLectureNotes && pdflatex book.tex

problems:
	cd auxiliary && python prepare-problem-set.py > a.tex && pdflatex a.tex && rm a.tex a.aux a.log && mv a.pdf ../Problems.pdf

all: problems book

.PHONY: all book problems
