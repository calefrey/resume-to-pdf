rm resume.json
python resume_to_latex.py
docker run --rm -v ./:/resume pdflatex pdflatex -interaction=batchmode resume.tex
