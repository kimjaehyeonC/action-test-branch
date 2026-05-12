import json
import sys
from pathlib import Path

def zpln_to_ipynb(src: Path, dst: Path):
    zpln = json.loads(src.read_text(encoding="utf-8"))
    paragraphs = zpln.get("paragraphs", [])
    
    cells = []
    for para in paragraphs:
        text = para.get("text", "") or ""
        text = text.strip()
        if not text:
            continue
        
        lines = text.split("\n")
        
        # 첫 줄 인터프리터 선언 처리
        if lines[0].startswith("%"):
            interp = lines[0]           # ex) %python
            code = "\n".join(lines[1:]).strip()
            source = f"# {interp}\n{code}"
        else:
            source = text
        
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": source.splitlines(keepends=True)
        })
    
    ipynb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {"name": "python", "version": "3.11.14"},
            "zeppelin_note_name": zpln.get("name", src.stem),
        },
        "cells": cells,
    }
    
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(ipynb, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[변환완료] {src.name} → {dst.name}")

if __name__ == "__main__":
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    zpln_to_ipynb(src, dst)