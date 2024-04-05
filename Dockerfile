FROM alpine:3.19
RUN apk add --no-cache texlive texmf-dist-latexextra  py3-jinja2 py3-requests
ENV TEMPLATES="/app/templates"
COPY resume-to-latex.py /app/
COPY utils.py /app/
COPY templates app/templates/
WORKDIR /resume
CMD python3 /app/resume-to-latex.py && pdflatex -interaction=batchmode resume.tex > /dev/null