import importlib.util
import json
import time

studentName = "studentName"
studentFile = "studentFile.py"

assignmentName = "assignmentName"
gradedFunctionName = "solveSlider"
maxruntime = 1  # in seconds

exampleInputsFile = "exampleInputs.jsonlist"
exampleOutputsFile = "exampleOutputs.txt"
gradedInputsFile = "gradedInputs.jsonlist"
gradedOutputsFile = "gradedOutputs.txt"

finalGradingMode = False  # TA will set this to True when grading the actual submission


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

# load inputs
if finalGradingMode:
    with open(gradedInputsFile) as f:
        inputs = [json.loads(l) for l in f.readlines()]
    with open(gradedOutputsFile) as f:
        outputs = [json.loads(l)["ans"] for l in f.readlines()]
else:
    with open(exampleInputsFile) as f:
        inputs = [json.loads(l) for l in f.readlines()]
    with open(exampleOutputsFile) as f:
        outputs = [json.loads(l)["ans"] for l in f.readlines()]

assert len(inputs) == len(outputs)
if not hasattr(student_module, gradedFunctionName):
    raise Exception(f"ERROR: Function {gradedFunctionName} not found in student file.")
studentFn = getattr(student_module, gradedFunctionName)

# grade all items
numCorrect = 0
pOut(f"GRADING REPORT: {studentName} FOR ASSIGNMENT {assignmentName}")
for i in range(len(inputs)):
    pOut("\n" + "=" * 80)
    pOut(f"PROBLEM {i+1}")
    for k, v in inputs[i].items():
        pOut(f"\tInput {k}: {v}")
    startTime = time.time()
    thisOutput = studentFn(**inputs[i])
    endTime = time.time()
    pOut(f"Function {gradedFunctionName} took {endTime - startTime} seconds to run.")
    if endTime - startTime > maxruntime:
        pOut(
            f"ERROR: Function {gradedFunctionName} took too long to run. Max runtime: {maxruntime} seconds."
        )
        continue
    pOut(f"\tYour function's output: {thisOutput}")

    #################################################################
    ############# evaluate student answer  ##########################
    #################################################################
    # apply their answer to the board
    moveSequence = thisOutput
    boardSize = inputs[i]["size"]
    grid_flat = inputs[i]["grid"]
    if not isinstance(moveSequence, list):
        pOut("ERROR: Your function must return a list of moves.")
        continue
    if not all(isinstance(m, int) for m in moveSequence) or not all(
        m in range(boardSize * boardSize) for m in moveSequence
    ):
        pOut(
            "ERROR: Your function must return a list of integers no greater than boardSize*boardSize."
        )
        continue
    for m in moveSequence:
        # Find the index of the piece to move
        m = grid_flat.index(m)
        if m not in grid_flat:
            pOut(
                "ERROR: Your function said to move a piece that was not in the grid: "
                + str(m)
            )
            continue
        # is 0 to the left?
        if m % boardSize > 0 and grid_flat[m - 1] == 0:
            grid_flat[m - 1] = grid_flat[m]
            grid_flat[m] = 0
        # is 0 to the right?
        elif m % boardSize < boardSize - 1 and grid_flat[m + 1] == 0:
            grid_flat[m + 1] = grid_flat[m]
            grid_flat[m] = 0
        # is 0 above?
        elif m >= boardSize and grid_flat[m - boardSize] == 0:
            grid_flat[m - boardSize] = grid_flat[m]
            grid_flat[m] = 0
        # is 0 below?
        elif m < boardSize * (boardSize - 1) and grid_flat[m + boardSize] == 0:
            grid_flat[m + boardSize] = grid_flat[m]
            grid_flat[m] = 0
        else:
            pOut(
                "ERROR: Your function said to move a piece that was not next to an empty space: "
                + str(m)
            )
            continue
    if grid_flat == list(range(boardSize * boardSize)):
        pOut("CORRECT: Your solution returned a sequence that solved the puzzle!")
        numCorrect += 1
        continue

pOut("=" * 80)
pOut("=" * 80)
percentCorrect = numCorrect / len(inputs)
pOut(f"Percentage correct: {numCorrect}/{len(inputs)} = {percentCorrect}")
pOut(f"Points awarded: {percentCorrect*50} of 50")
