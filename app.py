import json
import shutil
import subprocess
import os


infoIn = open("app.json", 'r')
infoOut = open("result.json", 'w')
data = json.load(infoIn)
infoIn.close()   # Открыли json, распарсили входящий, закрыли.

language = data["language"]

solution = open("solution.cpp",'w')
solution.write(data["code"])
solution.close()  # Записываем код программы в файл.

link_tests = data["path_to_tests"]

time_limit = data["time_limit"]
memory_limit = data["ml"]

tests = {}
test_number = 0

flag = "OK"

for test in os.listdir(link_tests):  # add test file, compile, check

        if(len(test)==2):

            answer = test + ".a"

            shutil.copyfile(os.path.join(link_tests, test), os.path.join(os.getcwd(), test))
            shutil.copyfile(os.path.join(link_tests, answer), os.path.join(os.getcwd(), answer))

            os.rename(test, "sum.in")
            os.rename(answer, "answer")


            subprocess.call("g++ solution.cpp > compilation.txt 2>&1", shell=True)  #Компилируем решение.

            compilation = open("compilation.txt", "r")
            compilation_result = compilation.read()
            compilation.close()




            if "error" in compilation_result:
                flag = "CE"
                break

            subprocess.call("./a.out", shell=True)

            subprocess.call("g++ check.cpp", shell=True)


            subprocess.call("./a.out sum.in sum.out answer > result.txt 2>&1", shell=True)

            result = open("result.txt", "r")
            res = result.read()
            result.close()

            test_number = test_number+1
            tests.update({str(test_number): res})



            if "ok" not in res:
                flag = "WA"





if (flag == "OK"):
    json.dump({"verdict": "OK", "tests": tests}, infoOut)

elif (flag == "CE"):
    json.dump({"verdict": "CE"}, infoOut)

else:
    json.dump({"verdict": "WA", "tests": tests}, infoOut)


infoOut.close()

subprocess.call("cat result.json", shell=True)
