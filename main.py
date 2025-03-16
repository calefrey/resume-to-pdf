# dispatcher that decides whether to run the web service or convert local files
import subprocess
from webapp import app ## the flask application
from resume_to_latex import generate_latex

try: # if we have local files, generate them and exit
    generate_latex()
    subprocess.Popen("pdflatex -interaction=batchmode resume.tex", shell=True).wait()

except: # if not, run it as the service
    print("Running as web service instead")
    app.run("0.0.0.0")