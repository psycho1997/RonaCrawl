import os
import subprocess

in_path = "/data/template.tex"
out_path = "/data/tmp.tex"


def writeTex(s):
    with open(os.getcwd()+in_path, 'r+') as f_in:
        test = f_in.read()
        tmp = test.replace('$equation$',s)
        with open(os.getcwd()+out_path, 'w')as f_out:
            f_out.write(tmp)
            f_out.close()
        f_in.close()
    subprocess.run("cd /data; pwd", shell=True)

