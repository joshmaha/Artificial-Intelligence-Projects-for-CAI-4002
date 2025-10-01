import json
from hw3 import calcSentiment_test 

def evaluate_model_from_array(json_file_path):
    correct = 0
    total = 0

    with open(json_file_path, "r", encoding="utf-8") as f:
        reviews = json.load(f)

        for item in reviews:
            review_text = item["t"]
            actual_sentiment = bool(item["s"])
            prediction = calcSentiment_test(review_text)

            if prediction == actual_sentiment:
                correct += 1
            total += 1

            if total % 100 == 0:
                print(f"{total} reviews tested...")

            if total > 1000:
                break

    print(f"\nAccuracy: {correct}/{total} = {correct/total:.2%}")


file_path = r"C:\\Users\\jnmah\\OneDrive\\2025\\Spring 25\\CAI 4002\\Project 3\\reviews.json"
evaluate_model_from_array(file_path)
