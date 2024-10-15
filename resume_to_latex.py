import jinja2
import os
from utils import get_json_from_files, get_json_from_github


def generate_latex(username=None, raise_exceptions=True):
    if username is None:
        # use github gist if GITHUBUSER is specified
        username = os.getenv("GITHUBUSER")
    if username:
        try:
            print(f"Pulling from {username}'s GitHub")
            data = get_json_from_github(username)
        except Exception as e:
            if raise_exceptions:
                raise e
            else:
                print(e)
                exit(1)
    else:
        try:
            data = get_json_from_files()
        except Exception as e:
            if raise_exceptions:
                raise e
            else:
                print(e)
                exit(1)
    print(f"Generating a resume for {data['basics']['name']}")
    template_path = os.getenv("TEMPLATES")
    if template_path:  # running in docker with environmental variable
        # print(f"Using {template_path} for templates")
        template_loader = jinja2.FileSystemLoader(searchpath=template_path)
    else:
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


if __name__ == "__main__":
    generate_latex(raise_exceptions=False)
