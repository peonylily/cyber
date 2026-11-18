from model import train_and_evaluate

if __name__ == "__main__":
    _, m = train_and_evaluate()
    print("Cyber Mentor — synthetic-data evaluation")
    for key in ("accuracy", "precision", "recall"):
        print(f"{key}: {m[key]:.4f}")
    print("labels:", m["labels"])
    print("confusion matrix:\n", m["confusion_matrix"])
    print(f"records={m['total_size']} train={m['train_size']} test={m['test_size']}")
    print("NOTE: These results describe synthetic data only.")
