import json
import sys
from pathlib import Path
from typing import Any

RECORD_PATH = Path("justin_gamache_academic_record.json")
REQUIRED_KEYS = ["student", "academic_programs"]


def load_json(path: Path) -> dict[str, Any]:
    """Load and parse the JSON record."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid JSON in {path} at line {e.lineno}, column {e.colno}: {e.msg}"
        ) from e

    if not isinstance(data, dict):
        raise TypeError("Top-level JSON structure must be an object/dictionary.")

    return data


def validate_required_keys(data: dict[str, Any], required_keys: list[str]) -> None:
    """Ensure all required top-level keys are present."""
    missing = [key for key in required_keys if key not in data]
    if missing:
        raise KeyError(f"Missing required top-level keys: {', '.join(missing)}")


def validate_student_section(data: dict[str, Any]) -> None:
    """Validate the student section."""
    student = data.get("student")

    if not isinstance(student, dict):
        raise TypeError("'student' must be a JSON object.")

    required_student_keys = ["name"]
    missing = [key for key in required_student_keys if key not in student]
    if missing:
        raise KeyError(f"Missing required keys in 'student': {', '.join(missing)}")

    if not isinstance(student["name"], str) or not student["name"].strip():
        raise ValueError("'student.name' must be a non-empty string.")


def validate_academic_programs(data: dict[str, Any]) -> None:
    """Validate the academic_programs section."""
    programs = data.get("academic_programs")

    if not isinstance(programs, list):
        raise TypeError("'academic_programs' must be a list.")

    if not programs:
        raise ValueError("'academic_programs' must not be empty.")

    for index, program in enumerate(programs, start=1):
        if not isinstance(program, dict):
            raise TypeError(f"Program #{index} must be a JSON object.")

        required_program_keys = ["institution", "program_name"]
        missing = [key for key in required_program_keys if key not in program]
        if missing:
            raise KeyError(
                f"Program #{index} is missing required keys: {', '.join(missing)}"
            )

        if not isinstance(program["institution"], str) or not program["institution"].strip():
            raise ValueError(f"Program #{index} has an invalid 'institution' value.")

        if not isinstance(program["program_name"], str) or not program["program_name"].strip():
            raise ValueError(f"Program #{index} has an invalid 'program_name' value.")


def print_summary(data: dict[str, Any]) -> None:
    """Print a short validation summary."""
    student_name = data["student"]["name"]
    program_count = len(data["academic_programs"])
    top_keys = ", ".join(sorted(data.keys()))

    print("Validation successful.")
    print(f"Student: {student_name}")
    print(f"Academic programs: {program_count}")
    print(f"Top-level keys: {top_keys}")


def main() -> int:
    """Run all validation checks."""
    try:
        data = load_json(RECORD_PATH)
        validate_required_keys(data, REQUIRED_KEYS)
        validate_student_section(data)
        validate_academic_programs(data)
        print_summary(data)
        return 0

    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
