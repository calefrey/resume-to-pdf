import json
import jinja2

try:
    data = json.load(open("resume.json", "r"))
    print("Using resume.json")
except FileNotFoundError:
    try:
        import tomllib
        data = tomllib.load(open("resume.toml", "rb"))
        print("Using resume.toml")
    except FileNotFoundError:
        pass
try:
    assert data
except NameError:
    print("Couldn't find any valid resume data files")
    print("Aborting")
    exit()

template_loader = jinja2.FileSystemLoader(searchpath="templates")
environment = jinja2.Environment(  # not using curly braces {} because that doesn't work well with latex
    block_start_string="((*",
    block_end_string="*))",
    variable_start_string="(((",
    variable_end_string=")))",
    comment_start_string="((#",
    comment_end_string="#))",
    lstrip_blocks=True,
    trim_blocks=True,
    loader=template_loader,
)
template = environment.get_template("resume.tex.j2")
with open("resume.tex", "w") as f:
    f.write(template.render(data=data))
