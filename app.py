import json
import shutil
import subprocess
import os


info = "app.json"
file_info = open(info, 'r')
file = open("result.json", 'w')
data = json.load(file_info)  # Parse JSON


link_solve = data['solve']
link_checker = data['checker']
link_tests = data['tests']

# Getting files

shutil.copyfile(link_solve, os.path.join(os.getcwd(),  "solution.cpp"))

shutil.copyfile(link_checker, os.path.join(os.getcwd(),  "check.cpp"))


flag = "ok"

for test in os.listdir(link_tests):  # add test file, compile, check

        if(len(test) == 2):

            answer = test + ".a"

            shutil.copyfile(os.path.join(link_tests, test), os.path.join(os.getcwd(), test))
            shutil.copyfile(os.path.join(link_tests, answer), os.path.join(os.getcwd(), answer))

            os.rename(test, "sum.in")
            os.rename(answer, "answer")


            subprocess.call('g++ solution.cpp', shell=True)

            subprocess.call('./a.out', shell=True)

            subprocess.call('g++ check.cpp', shell=True)


            process = subprocess.Popen('./a.out sum.in sum.out answer', shell=True)

            # Checker {}


if (flag == "ok"):

    answer = {'result' : "ok OK"}
    json.dump(answer, file)

else:

    json.dump(answer, file)











# Compile and Check

