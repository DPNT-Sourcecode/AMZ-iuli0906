import sys
import io
import builtins

# Import the legacy code as a module
import importlib.util
import os

# Dynamically import the amazing.py legacy code as a module
LEGACY_PATH = os.path.join(os.path.dirname(__file__), "amazing.py")
spec = importlib.util.spec_from_file_location("amazing_legacy", LEGACY_PATH)
amazing_legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(amazing_legacy)

class AmazingSolution:
    def amazing_maze(self, rows, columns, maze_generation_options):
        """
        Invokes the legacy amazing.py code, passing columns and rows to stdin,
        captures the output, and returns the ASCII maze as a string (without the prompt).
        """
        # Prepare the input: columns then rows, each on a new line
        # The legacy code expects input() for width (columns) and length (rows)
        input_values = [str(columns), str(rows)]
        input_iter = iter(input_values)

        # Patch input() to return our values
        orig_input = builtins.input
        def fake_input(prompt=None):
            try:
                return next(input_iter)
            except StopIteration:
                raise EOFError("No more input values provided.")

        # Capture stdout
        buf = io.StringIO()
        orig_stdout = sys.stdout
        try:
            builtins.input = fake_input
            sys.stdout = buf
            amazing_legacy.run()
        finally:
            builtins.input = orig_input
            sys.stdout = orig_stdout

        # Get output and remove the legacy prompt
        output = buf.getvalue()
        # Remove the prompt line ("WHAT ARE YOUR WIDTH AND LENGTH\n")
        lines = output.splitlines()
        maze_lines = []
        prompt_found = False
        for line in lines:
            # The prompt is always "WHAT ARE YOUR WIDTH AND LENGTH"
            if not prompt_found and "WHAT ARE YOUR WIDTH AND LENGTH" in line:
                prompt_found = True
                continue
            # Skip empty lines before the maze
            if not prompt_found:
                continue
            # Skip any lines that are just empty after the prompt
            if prompt_found and not line.strip() and not maze_lines:
                continue
            maze_lines.append(line)
        # Return the maze as a string
        return "\n".join(maze_lines).rstrip()
