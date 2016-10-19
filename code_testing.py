import subprocess
import json

# EXERCICE 1
ex1 = ["import numpy as np\n",
		("print(f(42))", 42),
		("print(g(2))", 4)]


# Dictionary of functions to call
execPythonFunc =  {"/ex1" : ex1}

# Run the code of a certain exercice and return the std of JSON format
def submitTestCode(path, test_code):
	testResults = []
	testList = execPythonFunc[path]

	for k in range(1, len(testList)):
		# imports - submited code - custom tests
		testResults.append(runSubprocess(testList[0] + "\n\n" + test_code + "\n\n" + testList[k][0], testList[k][1]))

	return json.dumps(testResults)

# Run a single python test
def runSubprocess(full_code, expected_output):
	proc = subprocess.Popen(["python", "-c", full_code,], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	std = proc.communicate()
	stdout_value = std[0]
	stderr_value = std[1]

	stdout_value = stdout_value.replace("'", "");
	stderr_value = stderr_value.replace("'", "");
	stdout_value = stdout_value.replace('"', '');
	stderr_value = stderr_value.replace('"', '');
	stdout_value = stdout_value.replace("\n", "\\n");
	stderr_value = stderr_value.replace("\n", "\\n");

	is_success = (stderr_value == '')

	if is_success:
		# Test the output
		is_success = (stdout_value == str(expected_output)+'\\n')

		if not is_success:
			stderr_value = "The program returned " + stdout_value + "it should have been " + str(expected_output)

	return {"is_success" : is_success, "stdout" : stdout_value, "stderr" : stderr_value}
