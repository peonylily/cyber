from model import train_and_evaluate, predict_topic

def test_training_and_prediction():
    model, metrics = train_and_evaluate()
    assert metrics["total_size"] == 900
    assert metrics["train_size"] + metrics["test_size"] == 900
    assert metrics["confusion_matrix"].shape == (3, 3)
    topic, confidence = predict_topic(model, {"phishing": 30, "privacy": 80, "password": 75}, 5)
    assert topic in metrics["labels"]
    assert 0 <= confidence <= 1
