# Resume.json to PDF
I love the idea of the [json-resume](https://jsonresume.org/) but most stuff I've seen turns the json into a website.

While the websites look nice, often you still need to submit a simple PDF resume.

The script and template included here takes your resume.json (or toml) and generate a simple PDF that looks decent to a human and readable to a robot - not something you could say about a website "print to PDF"

## Requirements
- A resume.json or a resume.toml file
 - the recommended vscode addons will help you configure it, but you can just follow my toml example
- Python 3.11 (required for the built in toml library)
  - `pip install jinja2`
- A LaTeX installation
  - Windows: you probably want [MiKTeX](https://miktex.org/)
  - Linux: install [TeX Live](https://tug.org/texlive/)
    - Should be available as `texlive` in your package manager
## Usage
This repo includes a task definition file for VSCode, so you can just start the build process (control-shift-b)
If you're not using VSCode that's fine, just run the two steps in sequence
- `python resume-to-latex.py` to build the latex
- `pdflatex resume.tex` to turn it into a PDF

## Docker Web Server

To make this easily usable by others, I have wrapped it into a flask app running in a docker container

If, per the jsonresume.org "standard", you have github gist called resume.json, the web server can generate the PDF on demand for a given username.

For example, if running at localhost:5000, visiting localhost:5000/calefrey.pdf would download resume.json from my github gists, render it to PDF, and then serve it to your web browser.

You can pull and run my prebuilt image with
```shell
docker run \
    -p 5000:5000 \
    ghcr.io/calefrey/resume-to-pdf:master
```

# Docker Local Mode

While the container can act as a web service, I originally made it a container to keep the LaTeX dependencies contained, and it can still work with local files instead of as a service.

Just mount the local folder to `/resume` and if you have local resume.json (or .toml) files, it will generate the PDF and exit.

```shell
docker run \
    --rm \
    -v ./:/resume \
    ghcr.io/calefrey/resume-to-pdf:master
```
Optionally if you want to pull from a specific github user you can do that as well with the environmental variables (though you'll still need to mount the directory to get output files).

```shell
docker run \
    --rm \
    -v ./:/resume \
    -e GITHUBUSER=calefrey \
    ghcr.io/calefrey/resume-to-pdf:master
```
## TODO
- [x] Make a dockerfile to reduce the number of tools you need to install
- [x] Have github actions generate a container so you don't need to build latex every time
- [x] Let the image pull from a github gist for resume.json
- [x] Make this into a web service using flask to be deployed somewhere
  - https://resume.freyc.xyz
- [x] Allow for easy one-off/static usage now that it's web-first
