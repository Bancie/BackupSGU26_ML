pdf:
	pdflatex -interaction=nonstopmode presentation.tex
	biber presentation
	pdflatex -interaction=nonstopmode presentation.tex
	pdflatex -interaction=nonstopmode presentation.tex

presentation.zip : 
	zip -r presentation.zip .gitignore presentation.tex sybila-logo/*.png

presentation-full.zip :
	zip -r presentation-full.zip fira-sans fira-mono sybila-logo .gitignore presentation.tex README.mk

fonts.zip :
	zip -r fonts.zip fira-sans fira-mono

clean :
	rm -f presentation.zip presentation-full.zip fonts.zip
	rm -f *.aux *.bbl *.bcf *.blg *.log *.nav *.out *.run.xml *.snm *.toc *.vrb

all : presentation.zip presentation-full.zip fonts.zip