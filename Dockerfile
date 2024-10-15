FROM alpine:3.19
RUN apk add --no-cache texlive texmf-dist-latexextra  py3-jinja2 py3-requests py3-flask
ENV TEMPLATES="/app/templates"
EXPOSE 5000/tcp
WORKDIR /app
# COPY resume-to-latex.py /app/
# COPY utils.py /app/
COPY . .
# COPY templates app/templates/
WORKDIR /resume
#CMD python3 /app/resume-to-latex.py && pdflatex -interaction=batchmode resume.tex > /dev/null && rm resume.out resume.aux resume.log resume.tex
CMD python3 /app/webapp.py