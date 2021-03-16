import os
import subprocess
import json

with open(os.getcwd() + "/data/settings.json") as file:
    json_dict = json.load(file)
global ronadir
texdir = json_dict["texdir"]

in_path = os.path.join(os.getcwd(), texdir, "template.tex" )
out_path = os.path.join(os.getcwd(), texdir, "tmp.tex")


def writeTex(s):
    with open(os.path.join(os.getcwd(), in_path), 'r+') as f_in:
        test = f_in.read()
        tmp = test.replace('$equation$',s)
        with open(os.path.join(os.getcwd(), out_path), 'w')as f_out:
            f_out.write(tmp)
            f_out.close()
        f_in.close()
    subprocess.run("cd " + os.path.join(os.getcwd(), texdir) +  "; pdflatex -shell-escape tmp.tex", shell=True)

