FROM alpine
RUN apk add --no-cache texlive texmf-dist-latexextra  py3-jinja2 py3-requests py3-flask
ENV TEMPLATES="/app/templates"
EXPOSE 5000/tcp
WORKDIR /app
COPY . .
WORKDIR /resume
CMD ["python3", "/app/main.py"]