import subprocess
import json

class CodeTester:
	def __init__(self):
		pass

	def submitTestCode(self, before_code, test_code, submited_code):
		assert len(test_code) % 2 == 0, "Wrong test code"
		testResults = []

		for k in range(int(len(test_code) / 2)):
			# imports - submited code - custom tests
			print(before_code + "\n\n")
			testResults.append(self.runSubprocess(before_code + "\n\n" + submited_code + "\n\n" + test_code[2 * k], test_code[2 * k + 1]))

		return json.dumps(testResults)

	# Run a single python test
	def runSubprocess(self, full_code, expected_output):
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
