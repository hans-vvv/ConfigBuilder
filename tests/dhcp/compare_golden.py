from pathlib import Path
import sys, difflib

ROOT = Path(__file__).resolve().parents[2]  # repo root (two levels up from tests/dhcp)
sys.path.insert(0, str(ROOT))

from app.views.test_create_ftg_dhcp_server_cfg import merged_data, TEMPLATE_NAME, TEMPLATE_DIR
from app.printers.printer import Printer

# ---- config ----
SITE = "BRUSSELS"
HERE = Path(__file__).resolve().parent
GOLDEN_PATH = HERE / "golden" / f"{SITE}.conf"
# ---------------

def main() -> int:    
    accept = "--accept" in sys.argv    

    printer = Printer(
        config_tree=merged_data(),
        template_name=TEMPLATE_NAME,
        template_dir=str(Path(TEMPLATE_DIR).resolve()),
    )
    outputs = printer.render()

    if SITE not in outputs:
        print(f"[ERR] Site '{SITE}' not produced. Available: {list(outputs.keys())}")
        return 2

    got = _norm(outputs[SITE])    

    GOLDEN_PATH.parent.mkdir(parents=True, exist_ok=True)

    if accept or not GOLDEN_PATH.exists():
        GOLDEN_PATH.write_text(got, encoding="utf-8", newline="\n")
        tag = "[INIT]" if not GOLDEN_PATH.exists() else "[ACCEPT]"
        print(f"{tag} wrote {GOLDEN_PATH.relative_to(HERE.parent)}")
        return 0     

    exp = _norm(GOLDEN_PATH.read_text(encoding="utf-8"))
    if got == exp:
        print(f"[OK] matches golden: {GOLDEN_PATH.relative_to(HERE.parent)}")
        return 0  

    diff = difflib.unified_diff(
        exp.splitlines(keepends=True),
        got.splitlines(keepends=True),
        fromfile=str(GOLDEN_PATH),
        tofile=f"(current) {SITE}.conf",
    )
    print(f"[DIFF] {SITE} differs:\n{''.join(diff)}")
    return 1


def _norm(s: str) -> str:
    s = s.replace("\r\n", "\n")
    s = "\n".join(line.rstrip() for line in s.split("\n"))
    if not s.endswith("\n"):
        s += "\n"
    return s

if __name__ == "__main__":
    raise SystemExit(main())
