"""Assemble the modular technical report into the repository-root report."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = Path(__file__).resolve().parent

SECTIONS = [
    "00_Front_Matter.md",
    "ABSTRACT.md",
    "TABLE_OF_CONTENTS.md",
    "LIST_OF_FIGURES.md",
    "LIST_OF_TABLES.md",
    "ABBREVIATIONS.md",
    "01_Introduction.md",
    "02_Objectives.md",
    "03_Scope.md",
    "04_Problem_Definition.md",
    "05_Benefits.md",
    "06_Main_Modules.md",
    "07_Technical_Overview.md",
    "08_System_Configuration.md",
    "09_Block_Diagram.md",
    "10_Data_Flow_Diagram.md",
    "11_ER_Diagram.md",
    "12_Project_Explanation.md",
    "13_Coding_Detailed_Explanation.md",
    "14_Results_and_Analysis.md",
    "15_Software_Testing.md",
    "16_Conclusion.md",
    "17_Bibliography.md",
]


def root_relative_links(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1)
        path, marker, fragment = target.partition("#")
        if not path or "://" in path:
            return match.group(0)
        resolved = (REPORT_DIR / path).resolve()
        try:
            relative = resolved.relative_to(ROOT).as_posix()
        except ValueError:
            return match.group(0)
        return f"](./{relative}{marker}{fragment})"

    return re.sub(r"\]\(([^)]+)\)", replace, text)


def build_report() -> None:
    sections = [
        root_relative_links((REPORT_DIR / name).read_text(encoding="utf-8").strip())
        for name in SECTIONS
    ]
    destination = ROOT / "PROJECT_REPORT.md"
    destination.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"Generated {destination}")


if __name__ == "__main__":
    build_report()
