import importlib.util
import time

studentName = "studentName"
studentFile = "exampleHW3.py"

assignmentName = "Sentiment_Analysis"
trainFunctionName = "calcSentiment_train"
testFunctionName = "calcSentiment_test"

maxTrainTime = 120  # in seconds
maxTestTime = 10  # in seconds

lowerBound = 0.5 #the percent that results in a score of 70%.
upperBound = 0.7 #the percent that results in a score of 100%.
maxEC = 10 #the max number of extra credit points that can be earned.

exampleOutputsFile = "exampleOutputs.txt"
gradedOutputsFile = "gradedOutputs.txt"

finalGradingMode = False  # TA will set this to True when grading the actual submission

if finalGradingMode:
    from actual_test_problems import problems as test_graded_problems
    from actual_test_problems import answers as test_graded_answers
else:
    from practice_test_problems import problems as test_practice_problems
    from practice_test_problems import answers as test_practice_answers

def pOut(s: str):
    print(s)
    if finalGradingMode:
        with open(studentName + "_grade.txt", "a+") as f:
            f.write(s + "\n")


######################################################################################
## DO NOT MODIFY ANYTHING BELOW THIS LINE ###########################################
######################################################################################

# Load student file
spec = importlib.util.spec_from_file_location("student_code", studentFile)
student_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student_module)

# Load train function
if not hasattr(student_module, trainFunctionName):
    raise Exception(f"ERROR: Function {trainFunctionName} not found in student file.")
sentiment_train = getattr(student_module, trainFunctionName)

# Load test function
if not hasattr(student_module, testFunctionName):
    raise Exception(f"ERROR: Function {testFunctionName} not found in student file.")
sentiment_test = getattr(student_module, testFunctionName)

if finalGradingMode:
    inputs = test_graded_problems
    answers = test_graded_answers
else:
    inputs = test_practice_problems
    answers = test_practice_answers

assert len(inputs) == len(answers), "ERROR: The number of inputs and answers are not the same."

# Train the sentiment model
startTime = time.time()
sentiment_train('trainingFile.jsonlist')
endTime = time.time()
pOut(f"Function {trainFunctionName} took {endTime - startTime} seconds to run.")
if endTime - startTime > maxTrainTime:
    pOut(
        f"ERROR: Function {trainFunctionName} took too long to run. Max runtime: {maxTrainTime} seconds."
    )

# grade all items
numCorrect = 0
pOut(f"GRADING REPORT: {studentName} FOR ASSIGNMENT {assignmentName}")
for i, input in enumerate(inputs):
    pOut("\n" + "=" * 80)
    pOut(f"PROBLEM {i+1}")
    # pOut(f"\tInput {input}")
    startTime = time.time()
    classification = sentiment_test(input)
    endTime = time.time()
    pOut(f"Function {testFunctionName} took {endTime - startTime} seconds to run.")
    if endTime - startTime > maxTrainTime:
        pOut(
            f"ERROR: Function {testFunctionName} took too long to run. Max runtime: {maxTrainTime} seconds."
        )
        continue

    pOut(f"\tYour function's output: {classification}")
    if classification == answers[i]:
        pOut("CORRECT: Your model correctly classified the sentiment of the review!")
        numCorrect += 1
        continue

pOut("=" * 80)
pOut("=" * 80)

# Calculate final score
percentCorrect = numCorrect / len(inputs)
if percentCorrect <= lowerBound:
    grade = 70
else:
    grade = min(100 + maxEC, (percentCorrect / upperBound) * 100)

# storeCorrect = numCorrect

# firstBracket = (min(numCorrect, len(inputs) * 0.5) / (len(inputs) * 0.5)) * 70
# numCorrect -= len(inputs) * 0.5

# secondBracket = (min(numCorrect, len(inputs) * 0.2) / (len(inputs) * 0.2)) * 30
# numCorrect = max(0, numCorrect - len(inputs) * 0.2)

# thirdBracket = (min(numCorrect, len(inputs) * 0.3) / (len(inputs) * 0.3)) * 10
# numCorrect = max(0, numCorrect - len(inputs) * 0.3)

pOut(f"Total score: {numCorrect} of {len(inputs)} = {percentCorrect*100}% which is worth {grade:.2f} points.")
