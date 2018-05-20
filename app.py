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

                if language == 'Java':
                    subprocess.call('java Main', timeout=time_limit, shell=True)


            except:
                result['result']['verdict'] = 'TL'
                break

        else:                    # CONSOLE
            if language == 'C++':
                command = './a.out < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)

            if language == 'Java':
                command = 'java Main < ' + filename + '.in > ' + filename + '.out'
                subprocess.call(command, timeout=time_limit, shell=True)




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