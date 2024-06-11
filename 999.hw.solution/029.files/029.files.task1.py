from pathlib import Path

with open(Path(Path.cwd(), "029.config.txt"), "r") as f:
    for line in f:
        if line.strip() == "!":
            continue
        print(line.rstrip())
