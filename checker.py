import json
import shutil
import subprocess
import os
from multiprocessing import Pool as ThreadPool

try:
    infoIn = open('/home/share/data.json', 'r')

except FileNotFoundError:
    infoOut = open('/home/share/result.json', 'w')
    result = {
        'status': 'error',
        'message': 'no json file'
    }
    json.dump(result, infoOut)
    infoOut.close()
    exit(0)

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
if language == 'C++' or language == 'Python2' or language == 'Python3' or language == 'C':
    solution = open('solution', 'w')
    solution.write(data['code'])
    solution.close()

elif language == 'Java':
    solution = open('Main.java', 'w')
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
subprocess.call('g++ checker.cpp', shell=True)

# Раскидываем тесты, testlib, исполнялку.
FROM = ['a.out', 'testlib.h']
TO = [filename, '/answer', 'checker', 'testlib.h']
for test in os.listdir(link_tests):
    if '.' not in os.path.basename(link_tests + '/' + test):
        answer = test + '.a'

        os.makedirs('/home/tests/' + str(test_number))

        FROM = [os.path.join(link_tests, test),
                os.path.join(link_tests, answer),
                os.path.join(os.getcwd(), 'a.out'),
                os.path.join(os.getcwd(), 'testlib.h')]

        TO = ['/home/tests/' + str(test_number) + '/' + filename + '.in',
              '/home/tests/' + str(test_number) + '/answer',
              '/home/tests/' + str(test_number) + '/checker',
              '/home/tests/' + str(test_number) + '/testlib.h']

        for i in range(0, 4):
            shutil.copy(FROM[i], TO[i])

        test_number = test_number + 1

# В зависимости от языка раскидываем исполнялку или само решение по папкам с тестами
# Сначала компилим и проверяем компиляцию
compilation_result = 'ok'
if language != 'Python3' and language != 'Python2':
    compilation = {'C++': 'g++ -x c++ solution > compilation.txt 2>&1',
                   'C': 'gcc -x c solution > compilation.txt 2>&1',
                   'Java': 'javac Main.java > compilation.txt 2>&1'}

    subprocess.call(compilation[language], shell=True)

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

    FROM = {'C': os.path.join(os.getcwd(), 'a.out'),
            'C++': os.path.join(os.getcwd(), 'a.out'),
            'Java': os.path.join(os.getcwd(), 'Main.class')}

    TO = {'C++': '/a.out', 'C': '/a.out', 'Java': '/Main.class'}

    for i in range(1, test_number):
        shutil.copy(FROM[language], '/home/tests/' + str(i) + TO[language])


else:
    for i in range(1, test_number):
        shutil.copyfile(os.path.join(os.getcwd(), 'solution'),
                        '/home/tests/' + str(i) + '/solution')

    # WorkCheck for Python
    os.chdir('/home/tests/1')
    if files == 1:
        try:
            if language == 'Python3':
                subprocess.call('python3 solution > workchecker.txt 2>&1', timeout=100, shell=True)

            else:
                subprocess.call('python solution > workchecker.txt 2>&1', timeout=100, shell=True)
        except:
            result['result']['verdict'] = 'TL'

    else:
        try:
            if language == 'Python3':
                command = 'python3 solution < ' + filename + '.in > ' + filename + '.out' + 'workchecker.txt 2>&1'
                subprocess.call(command, timeout=100, shell=True)

            else:
                command = 'python solution < ' + filename + '.in > ' + filename + '.out' + 'workchecker.txt 2>&1'
                subprocess.call(command, timeout=100, shell=True)
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

    commands_files = {'C++': './a.out',
                      'C': './a.out',
                      'Java': 'java Main',
                      'Python3': 'python3 solution',
                      'Python2': 'python solution'}

    commands_console = {'C++': './a.out < ' + filename + '.in > ' + filename + '.out',
                        'C': './a.out < ' + filename + '.in > ' + filename + '.out',
                        'Java': 'java Main < ' + filename + '.in > ' + filename + '.out',
                        'Python3': 'python3 < ' + filename + '.in > ' + filename + '.out',
                        'Python2': 'python < ' + filename + '.in > ' + filename + '.out'
                        }
    if files == 1:  # FILE
            try:
                subprocess.call(commands_files[language], timeout=time_limit, shell=True)

            except:
                return 'TL'

    else:  # CONSOLE
        try:
            subprocess.call(commands_console[language], timeout=time_limit, shell=True)

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

