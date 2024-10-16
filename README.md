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

## Docker Usage
So you don't need to install the whole LaTeX package on your system
```shell
docker build . -t resume-to-pdf
```
Have a resume.json or a resume.toml file in your current directory and run
```shell
docker run \
    --rm \
    -v ./:/resume \
    resume-to-pdf 
```

Now you can pull a prebuilt image and run it:
```shell
docker run \
    --rm \
    -v ./:/resume \
    ghcr.io/calefrey/resume-to-pdf:master
```

If you have a github gist called `resume.json` (as per the jsonresume recommendations), you can pass the GITHUBUSER environmental variable rather than keeping a local copy of your json.
```shell
docker run \
    --rm \
    -v ./:/resume \
    -e GITHUBUSER={your gh username goes here} \
    ghcr.io/calefrey/resume-to-pdf:master
```

# NEW METHOD SINCE ADDING WEB API

The new version is built primarily for the web service (see https://resume.freyc.xyz/)
so as a result, building locally as a one-off resume is a bit tricker.

You need to do it in two parts. The first pass grabs your data from the github gist, and the second pass renders it into a PDF.

I'm planning to make this into a one-pass process so running it one-off is easier than running the web service, but that's the current state.

```shell
docker run \
    --pull=always \
    --rm \
    -v ./:/resume \
    -e GITHUBUSER=calefrey \
    ghcr.io/calefrey/resume-to-pdf:master \
    python3 /app/resume_to_latex.py

docker run \
    --pull=always \
    --rm \
    -v ./:/resume \
    -e GITHUBUSER=calefrey \
    ghcr.io/calefrey/resume-to-pdf:master \
    pdflatex -interaction=batchmode resume.tex

````
## TODO
- [x] Make a dockerfile to reduce the number of tools you need to install
- [x] Have github actions generate a container so you don't need to build latex every time
- [x] Let the image pull from a github gist for resume.json
- [x] Make this into a web service using flask to be deployed somewhere
  - https://resume.freyc.xyz
- [ ] Allow for easy one-off/static usage now that it's web-first
