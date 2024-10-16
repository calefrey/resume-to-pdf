# turn it into a flask function that takes the username as the url endpoint
import flask
import os, subprocess
from flask import make_response
from resume_to_latex import generate_latex
import platform  # really, I need to do all this work because windows cmd doesn't support rm?

if platform.system() == "Windows":
    rmcmd = "del"
else:
    rmcmd = "rm"
app = flask.Flask("Resume to PDF")

@app.route("/")
def index():
    return """
<h1>Welcome to the JSONResume PDF Generator!</h1>
If you have a json resume following <a href=https://jsonresume.org>the JSON Resume</a> standard and it's published as a gist on your github, we can convert it to a PDF.
<br>
You can find it at /{your-github-username}.pdf on this domain.
<br>
Service provided as-is with no warranty nor guarantee
"""

@app.route("/<username>.pdf", methods=["GET"])
def main(username: None):
    try:
        generate_latex(username,raise_exceptions=True)
    except Exception as e:
        print(e)
        return "<h1>Python error:</h1>"+str(e)
    # run pdflatex to turn it into a pdf
    subprocess.Popen("pdflatex -interaction=batchmode resume.tex", shell=True).wait()
    response = make_response(open("resume.pdf", "rb").read())
    subprocess.Popen(
        f"{rmcmd} resume.out resume.json resume.aux resume.log resume.tex resume.pdf",
        shell=True,
    )
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=resume.pdf"
    return response
# TODO add error handling to the frontend


if __name__ == "__main__":
    username = os.getenv("GITHUBUSER")
    if username:
        main(username)
        exit(0)
    app.run("0.0.0.0")
