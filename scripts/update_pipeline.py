import subprocess

steps = [
    "scripts/validate_csv.py",
    "scripts/clean_latest.py",
    "scripts/merge_database.py",
    "ml/preprocess.py",
    "ml/train_model.py"
]

for step in steps:
    print(f"\nRunning {step}...")
    result = subprocess.run(["python", step])

    if result.returncode != 0:
        print(f"\n Failed : {step}")
        exit()

print("\n Everything Updated Successfully")