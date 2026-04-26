"""Extract all outputs from jigsaw_audit_analysis.ipynb into inference_outputs/."""
import base64
import json
import re
from pathlib import Path

NOTEBOOK = Path(__file__).parent / "jigsaw_audit_analysis.ipynb"
OUT_DIR = Path(__file__).parent / "inference_outputs"


def slugify(text: str, maxlen: int = 60) -> str:
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:maxlen] or "cell"


def cell_label(cell: dict, idx: int) -> str:
    src = "".join(cell.get("source", [])).strip()
    first = src.splitlines()[0] if src else ""
    first = re.sub(r"^#+\s*", "", first)
    return f"cell{idx:03d}_{slugify(first)}" if first else f"cell{idx:03d}"


def write_data(data: dict, prefix: Path) -> int:
    n = 0
    for mime, payload in data.items():
        text = payload if isinstance(payload, str) else "".join(payload) if isinstance(payload, list) else json.dumps(payload, indent=2)
        if mime == "image/png":
            prefix.with_suffix(".png").write_bytes(base64.b64decode(text))
        elif mime == "image/jpeg":
            prefix.with_suffix(".jpg").write_bytes(base64.b64decode(text))
        elif mime == "image/svg+xml":
            prefix.with_suffix(".svg").write_text(text, encoding="utf-8")
        elif mime == "text/html":
            prefix.with_suffix(".html").write_text(text, encoding="utf-8")
        elif mime == "text/plain":
            prefix.with_suffix(".txt").write_text(text, encoding="utf-8")
        elif mime == "application/json":
            prefix.with_suffix(".json").write_text(text, encoding="utf-8")
        else:
            ext = "." + mime.replace("/", "_").replace("+", "_") + ".bin"
            try:
                prefix.with_suffix(ext).write_bytes(base64.b64decode(text))
            except Exception:
                prefix.with_suffix(ext).write_text(text, encoding="utf-8")
        n += 1
    return n


def main() -> None:
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(exist_ok=True)

    files_written = 0
    for idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        outputs = cell.get("outputs", [])
        if not outputs:
            continue

        label = cell_label(cell, idx)
        stream_buf: dict[str, list[str]] = {}

        for out_i, out in enumerate(outputs):
            otype = out.get("output_type")
            if otype == "stream":
                name = out.get("name", "stdout")
                stream_buf.setdefault(name, []).append("".join(out.get("text", [])))
            elif otype in ("execute_result", "display_data"):
                prefix = OUT_DIR / f"{label}_out{out_i:02d}"
                files_written += write_data(out.get("data", {}), prefix)
            elif otype == "error":
                p = OUT_DIR / f"{label}_out{out_i:02d}_error.txt"
                p.write_text("\n".join(out.get("traceback", [])), encoding="utf-8")
                files_written += 1

        for name, chunks in stream_buf.items():
            p = OUT_DIR / f"{label}_{name}.txt"
            p.write_text("".join(chunks), encoding="utf-8")
            files_written += 1

    print(f"Wrote {files_written} files to {OUT_DIR}")


if __name__ == "__main__":
    main()
