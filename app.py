import json
import shutil
import subprocess
import os

infoIn = open('/home/filipp/share/data.json', 'r')
infoOut = open('/home/filipp/share/result.json', 'w')
data = json.load(infoIn)
infoIn.close()  # Open input & output files

language = data['language']
problems_dir = '/home/filipp/problems/'
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

for test in os.listdir(link_tests):  # Add test file, compile, check
    if '.' not in os.path.basename(link_tests + '/' + test):
        answer = test + '.a'

        shutil.copyfile(os.path.join(link_tests, test),
                        os.path.join(os.getcwd(), test))
        shutil.copyfile(os.path.join(link_tests, answer),
                        os.path.join(os.getcwd(), answer))
        shutil.copyfile(os.path.join(link_task, 'check.cpp'),
                        os.path.join(os.getcwd(), 'check.cpp'))

        os.rename(test, filename + '.in')
        os.rename(answer, 'answer')


        # Compile solution

        if language == 'C++':
         subprocess.call('g++ solution.cpp > compilation.txt 2>&1', shell=True)

        elif language == 'Java':
            subprocess.call('javac Main.java > compilation.txt 2>&1', shell=True)

        elif language == 'C':
            subprocess.call('gcc solution.c > compilation.txt 2>&1', shell=True)




        compilation = open('compilation.txt', 'r')
        compilation_result = compilation.read()
        compilation.close()

        # Handle compilation error
        if 'error' in compilation_result:
            result['result']['verdict'] = 'CE'
            result['result']['message'] = compilation_result
            break

        # Run code
        if files == 1:          # FILE
            try:
                if language == 'C++':
                    subprocess.call('./a.out', timeout=time_limit, shell=True)

                elif language == 'Java':
                    subprocess.call('java Main', timeout=time_limit, shell=True)

                elif language == 'Python3':
                    subprocess.call('python3 solution.py > workchecker.txt 2>&1', timeout=time_limit, shell=True)

                elif language == 'Python':
                    subprocess.call('python solution.py > workchecker.txt 2>&1', timeout=time_limit, shell=True)

                elif language == 'C':
                    subprocess.call('./a.out', timeout=time_limit, shell=True)

            except:
                result['result']['verdict'] = 'TL'
                break

        else:                    # CONSOLE
            if language == 'C++':
                command = './a.out < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

            elif language == 'Java':
                command = 'java Main < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

            elif language == 'Python3':
                command = 'python3 < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

            elif language == 'Python2':
                command = 'python < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

            elif language == 'C++':
                command = './a.out < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)
                
        # WorkCheck for Python
        if language == 'Python2' or language == 'Python3':
            work_check = open('workchecker.txt', 'r')

            if 'Traceback' in work_check.read():
                result['result']['verdict'] = 'CE'
                result['result']['message'] = compilation_result
                work_check.close()
                break

        # Run checker
        subprocess.call('g++ --std=c++17 check.cpp', shell=True)
        bash_command = './a.out ' + filename + '.in ' + filename + '.out ' + 'answer > verdict.txt 2>&1'
        subprocess.call(bash_command, shell=True)

        # Read result
        verdict_file = open('verdict.txt', 'r')
        verdict = verdict_file.read()
        verdict_file.close()

        # Save to result
        result['result']['tests'].append({
            'test_number': int(test),
            'checker_comment': verdict
        })

        test_number += 1
        if 'ok' not in verdict:
            result['result']['verdict'] = 'WA'
            break

json.dump(result, infoOut)
infoOut.close()