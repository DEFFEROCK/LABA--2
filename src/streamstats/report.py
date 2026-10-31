import json
def save_report(path,report) -> None:
    with open(report,"w", encoding="utf-8") as file:
        json.dump(path, file, ensure_ascii=False, indent=4)
