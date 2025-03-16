import json
import requests
import platform  # really, I need to do all this work because windows cmd doesn't support rm?

class CustomException(Exception):
    pass

if platform.system() == "Windows":
    rmcmd = "del"
else:
    rmcmd = "rm"

def get_json_from_github(username):
    r = requests.get(f"https://api.github.com/users/{username}/gists")
    if r.status_code == 404:
        raise CustomException("GitHub user not found")
    gists = json.loads(r.text)

    resume_gists = [
        gist["files"]["resume.json"] for gist in gists if "resume.json" in gist["files"]
    ]
    if len(resume_gists) == 0:
        raise CustomException(f"Cannot find any gists called resume.json for user {username}")
    else:
        print("Found resume.json gist")
    resume_gist = resume_gists[0]
    raw_file_url = resume_gist["raw_url"]
    resume_json = json.loads(requests.get(raw_file_url).text)
    return resume_json


def get_json_from_files():
    try:
        data = json.load(open("resume.json", "r"))
        print("Using resume.json")
    except FileNotFoundError:
        try:
            import tomllib
            data = tomllib.load(open("resume.toml", "rb"))
            print("Using resume.toml")
            # also write out a json
            print("Writing resume.json")
            json.dump(data,open("resume.json",'w'))
        except FileNotFoundError as e:
            print("Couldn't find any valid resume data files")
            raise e
    return data
