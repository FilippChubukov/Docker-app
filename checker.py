import json
import shutil
import subprocess
import os
from multiprocessing import Pool as ThreadPool

infoIn = open('/home/share/data.json', 'r')
infoOut = open('/home/share/result.json', 'w')
data = json.load(infoIn)
infoIn.close()  # Open input & output files

language = data['language']
problems_dir = '/home/problems/'
link_task = os.path.join(problems_dir, data['path_to_task'])
link_tests = os.path.join(link_task, 'tests')
time_limit = float(data['time_limit'])
memory_limit = data['memory_limit']
filename = data['filename']
files = data['files']

tests = {}
test_number = 1
result = {
    'status': 'OK',
    'result': {
        'verdict': 'OK',
        'message': '',
        'tests': []
    }
}


# Write code to file
if language == 'C++':
    solution = open('solution.cpp', 'w')
    solution.write(data['code'])
    solution.close()

elif language == 'Java':
    solution = open('Main.java', 'w')
    solution.write(data['code'])
    solution.close()

elif language == 'Python2' or language == 'Python3':
    solution = open('solution.py', 'w')
    solution.write(data['code'])
    solution.close()

elif language == 'C':
    solution = open('solution.c', 'w')
    solution.write(data['code'])
    solution.close()

else:
    result = {
        'status': 'error',
        'message': 'no such language'
    }
    json.dump(result, infoOut)
    infoOut.close()
    exit(0)

# Получаем исполнялку чекера чтобы потом ее раскидать по папкам
shutil.copyfile('/home/problems/' + filename + '/' + 'check.cpp',
                        '/home/check/checker.cpp')
subprocess.call('g++ --std=c++17 checker.cpp', shell=True)




# Раскидываем тесты, testlib, исполнялку.
for test in os.listdir(link_tests):
    if '.' not in os.path.basename(link_tests + '/' + test):
        answer = test + '.a'

        os.makedirs('/home/tests/' + str(test_number))

        shutil.copyfile(os.path.join(link_tests, test),
                        '/home/tests/' + str(test_number) + '/' + filename + '.in')

        shutil.copyfile(os.path.join(link_tests, answer),
                        '/home/tests/' + str(test_number) + '/answer')

        shutil.copy(os.path.join(os.getcwd(), 'a.out'),
                        '/home/tests/' + str(test_number) + '/checker')

        shutil.copyfile(os.path.join(os.getcwd(), 'testlib.h'),
                        '/home/tests/' + str(test_number) + '/testlib.h')
        test_number = test_number + 1


# В зависимости от языка раскидываем исполнялку или само решение по папкам с тестами
# Сначала компилим и проверяем компиляцию
compilation_result = 'ok'

if language == 'C++':
    subprocess.call('g++ solution.cpp > compilation.txt 2>&1', shell=True)
    compilation = open('compilation.txt', 'r')
    compilation_result = compilation.read()
    compilation.close()

elif language == 'Java':
    subprocess.call('javac Main.java > compilation.txt 2>&1', shell=True)
    compilation = open('compilation.txt', 'r')
    compilation_result = compilation.read()
    compilation.close()

elif language == 'C':
    subprocess.call('gcc solution.c > compilation.txt 2>&1', shell=True)
    compilation = open('compilation.txt', 'r')
    compilation_result = compilation.read()
    compilation.close()


# Handle compilation error
if 'error' in compilation_result:
        result['result']['verdict'] = 'CE'
        result['result']['message'] = compilation_result
        json.dump(result, infoOut)
        infoOut.close()
        exit(0)

if language == 'C++':
    for i in range(1, test_number):
        shutil.copy(os.path.join(os.getcwd(), 'a.out'),
                        '/home/tests/' + str(i) + '/a.out')

elif language == 'C':
    for i in range(1, test_number):
        shutil.copyfile(os.path.join(os.getcwd(), 'a.out'),
                        '/home/tests/' + str(i) + '/a.out')

elif language == 'Java':
    for i in range(1, test_number):
        shutil.copyfile(os.path.join(os.getcwd(), 'Main.class'),
                        '/home/tests/' + str(i) + '/Main.class')

elif language == 'Python2' or language == 'Python3':
    for i in range(1, test_number):
        shutil.copyfile(os.path.join(os.getcwd(), 'solution.py'),
                        '/home/tests/' + str(i) + '/solution.py')

 # WorkCheck for Python
    if language == 'Python2' or language == 'Python3':
        os.chdir('/home/tests/1')
        if files == 1:
            try:
                if language == 'Python3':
                    subprocess.call('python3 solution.py > workchecker.txt 2>&1', timeout=100, shell=True)

                elif language == 'Python2':
                    subprocess.call('python solution.py > workchecker.txt 2>&1', timeout=100, shell=True)
            except:
                result['result']['verdict'] = 'TL'

        else:
            try:
                if language == 'Python3':
                    command = 'python3 < ' + filename + '.in > ' + filename + '.out' + 'workchecker.txt 2>&1'
                    subprocess.call(command, timeout=time_limit, shell=True)

                elif language == 'Python2':
                    command = 'python < ' + filename + '.in > ' + filename + '.out' + 'workchecker.txt 2>&1'
                    subprocess.call(command, timeout=time_limit, shell=True)
            except:
                result['result']['verdict'] = 'TL'


        work_check = open('workchecker.txt', 'r')
        work_result = work_check.read()
        work_check.close()


        if 'Traceback' in work_result:
            print(result['result']['verdict'])
            result['result']['verdict'] = 'CE'
            result['result']['message'] = work_result

            json.dump(result, infoOut)
            infoOut.close()
            exit(0)



# Функция для работы с каждым тестом

def check(number):

    os.chdir('/home/tests/' + str(number))

    if files == 1:  # FILE
            try:
                if language == 'C++':
                    subprocess.call('./a.out', timeout=time_limit, shell=True)

                elif language == 'Java':
                    subprocess.call('java Main', timeout=time_limit, shell=True)

                elif language == 'Python3':
                    subprocess.call('python3 solution.py', timeout=time_limit, shell=True)

                elif language == 'Python2':
                    subprocess.call('python solution.py ', timeout=time_limit, shell=True)

                elif language == 'C':
                    subprocess.call('./a.out', timeout=time_limit, shell=True)

            except:
                return 'TL'

    else:  # CONSOLE
        try:
            if language == 'C++':
                command = './a.out < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

            elif language == 'Java':
                command = 'java Main < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

            elif language == 'Python3':
                command = 'python3 < ' + filename + '.in > ' + filename + '.out' + 'workchecker.txt 2>&1'
                subprocess.call(command, timeout=time_limit, shell=True)

            elif language == 'Python2':
                command = 'python < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

            elif language == 'C++':
                command = './a.out < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

        except:
            return 'TL'

    # Run checker
    bash_command = './checker ' + filename + '.in ' + filename + '.out ' + 'answer > verdict.txt 2>&1'
    subprocess.call(bash_command, shell=True)

# Параллельно запускаем функцию check
pool = ThreadPool(3)

numbers = []
for i in range(1,test_number):
    numbers.append(i)

results = pool.map(check, numbers)

if 'TL' in results:
    result['result']['verdict'] = 'TL'
    json.dump(result, infoOut)
    infoOut.close()
    exit(0)

# Проверяем вердикты
for test in range(1,test_number):
    os.chdir('/home/tests/' + str(test))
    # Read result
    verdict_file = open('verdict.txt', 'r')
    verdict = verdict_file.read()
    verdict_file.close()

    # Save to result
    result['result']['tests'].append({
        'test_number': int(test),
        'checker_comment': verdict
    })

    if 'ok' not in verdict:
        result['result']['verdict'] = 'WA'
        break

json.dump(result, infoOut)
infoOut.close()

