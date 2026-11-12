import inspect
import json
from functools import wraps


def inspect_object(obj):
    """Return detailed information about an object's type and class hierarchy."""

    obj_type = type(obj)

    # Get methods and filter out dunder methods
    methods = [
        name
        for name in dir(obj)
        if callable(getattr(obj, name, None))
        and not name.startswith("__")
    ]

    # Get class hierarchy
    hierarchy = [
        cls.__name__
        for cls in inspect.getmro(obj_type)
    ]

    return {
        "object": repr(obj),
        "type": obj_type.__name__,
        "module": obj_type.__module__,
        "is_primitive": isinstance(
            obj, (int, float, str, bool, bytes)
        ),
        "methods": sorted(methods),
        "class_hierarchy": hierarchy
    }


def type_check(**expected_types):
    """Validate function arguments using a decorator."""

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            signature = inspect.signature(function)
            bound_arguments = signature.bind(*args, **kwargs)

            for name, expected_type in expected_types.items():
                if name in bound_arguments.arguments:
                    value = bound_arguments.arguments[name]

                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Argument '{name}' must be "
                            f"{expected_type.__name__}, "
                            f"but received {type(value).__name__}."
                        )

            return function(*args, **kwargs)

        return wrapper

    return decorator


@type_check(name=str, age=int)
def introduce(name, age):
    """Return a short introduction."""
    return f"Hello {name}! You are {age} years old."


class Student:
    """Example custom class for testing introspection."""

    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def get_grade(self):
        """Return a grade based on marks."""
        if self.marks >= 90:
            return "A"
        elif self.marks >= 75:
            return "B"
        elif self.marks >= 50:
            return "C"
        return "D"


def recursive_inspect(obj, depth=0, max_depth=2):
    """Recursively inspect attributes of custom objects."""

    result = inspect_object(obj)

    if depth >= max_depth:
        return result

    if hasattr(obj, "__dict__"):
        attributes = {}

        for name, value in vars(obj).items():
            if not name.startswith("_"):
                if isinstance(
                    value,
                    (str, int, float, bool, list, tuple, dict, type(None))
                ):
                    attributes[name] = repr(value)
                else:
                    attributes[name] = recursive_inspect(
                        value,
                        depth + 1,
                        max_depth
                    )

        result["attributes"] = attributes

    return result


def main():
    """Run the interactive Type Utility Tool."""

    print("=" * 60)
    print("        INTERACTIVE TYPE UTILITY TOOL")
    print("=" * 60)

    while True:
        print("\nChoose an option:")
        print("1. Inspect an object")
        print("2. Test type validation")
        print("3. Inspect a custom class")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            user_input = input(
                "Enter a value to inspect: "
            )

            # Try to identify common Python types
            if user_input.lower() == "none":
                value = None
            elif user_input.isdigit():
                value = int(user_input)
            elif user_input.lower() in ("true", "false"):
                value = user_input.lower() == "true"
            else:
                value = user_input

            result = inspect_object(value)

            print("\n--- Inspection Result ---")
            print(json.dumps(result, indent=4))

        elif choice == "2":
            print("\n--- Type Validation Test ---")

            name = input("Enter your name: ")
            age_input = input("Enter your age: ")

            try:
                age = int(age_input)

                result = introduce(name, age)

                print(result)

            except ValueError:
                print("Error: Age must be a number.")

            except TypeError as error:
                print(f"Type Error: {error}")

        elif choice == "3":
            print("\n--- Custom Class Inspection ---")

            name = input("Enter student name: ")

            try:
                marks = float(input("Enter marks: "))

                student = Student(name, marks)

                result = recursive_inspect(student)

                print("\n--- Student Information ---")
                print(json.dumps(result, indent=4))

                print(
                    f"\nGrade: {student.get_grade()}"
                )

            except ValueError:
                print("Error: Marks must be a number.")

        elif choice == "4":
            print("\nThank you for using the Type Utility Tool!")
            break

        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()