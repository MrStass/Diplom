import os
from radon.complexity import cc_visit
from radon.metrics import h_visit
from radon.raw import analyze

# Initialize metrics
metrics = {
    "Загальна кількість рядків коду у проекті": 0,
    "Середня кількість рядків коду у класі": 0,
    "Максимальна кількість рядків коду в одному класі": 0,
    "Середня кількість рядків коду в одному методі": 0,
    "Максимальна кількість рядків коду в одному методі": 0,
    "Максимальна глибина дерева наслідування": 0,
    "Середня цикломатична складність методів": 0,
    "Максимальна цикломатична складність методів": 0,
    "Коментування коду": 0,
    "Коментування коду у відсотках": 0,
    "Покриття коду модульними тестами": "N/A"
}

# Helper variables
total_classes = 0
total_methods = 0
total_lines = 0
total_methods_length = 0
total_complexity = 0
max_lines_class = 0
max_lines_method = 0
max_complexity = 0
total_comments = 0
class_lines = []
method_lines = []
inheritance_depths = []


# Function to count lines and comments for non-Python files
def count_lines_and_comments(file_path, file_extension):
    lines = 0
    comments = 0
    in_multiline_comment = False
    with open(file_path, 'r') as f:
        for line in f:
            stripped_line = line.strip()
            lines += 1
            if file_extension in ['js', 'css']:
                if stripped_line.startswith('//'):
                    comments += 1
                elif stripped_line.startswith('/*') and stripped_line.endswith('*/'):
                    comments += 1
                elif stripped_line.startswith('/*'):
                    comments += 1
                    in_multiline_comment = True
                elif in_multiline_comment:
                    comments += 1
                    if '*/' in stripped_line:
                        in_multiline_comment = False
            elif file_extension == 'html':
                if stripped_line.startswith('<!--') and stripped_line.endswith('-->'):
                    comments += 1
                elif stripped_line.startswith('<!--'):
                    comments += 1
                    in_multiline_comment = True
                elif in_multiline_comment:
                    comments += 1
                    if '-->' in stripped_line:
                        in_multiline_comment = False
    return lines, comments


# Traverse the repository files
for root, dirs, files in os.walk("."):
    # Skip excluded directories
    dirs[:] = [d for d in dirs if d not in {".venv", "venv", "__pycache__", ".git"}]

    for file in files:
        file_extension = file.split('.')[-1]
        if file_extension in ["py", "js", "html", "css"]:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")  # Log the file being processed
            try:
                if file_extension == "py":
                    with open(file_path, 'r') as f:
                        code = f.read()
                        raw_metrics = analyze(code)
                        metrics["Загальна кількість рядків коду у проекті"] += raw_metrics.loc
                        total_comments += raw_metrics.comments

                        # Cyclomatic complexity
                        complexities = cc_visit(code)
                        for c in complexities:
                            total_complexity += c.complexity
                            total_methods += 1
                            total_methods_length += c.lineno
                            method_lines.append(c.lineno)
                            max_complexity = max(max_complexity, c.complexity)

                        # Halstead metrics and class lines
                        halstead_metrics = h_visit(code)
                        for h in halstead_metrics:
                            total_classes += 1
                            class_lines.append(h.loc)
                            max_lines_class = max(max_lines_class, h.loc)

                else:
                    lines, comments = count_lines_and_comments(file_path, file_extension)
                    metrics["Загальна кількість рядків коду у проекті"] += lines
                    total_comments += comments
            except SyntaxError as e:
                print(f"SyntaxError in file {file_path}: {e}")
            except Exception as e:
                print(f"Error in file {file_path}: {e}")

# Calculate averages
if total_classes > 0:
    metrics["Середня кількість рядків коду у класі"] = sum(class_lines) / total_classes
if total_methods > 0:
    metrics["Середня кількість рядків коду в одному методі"] = sum(method_lines) / total_methods
    metrics["Середня цикломатична складність методів"] = total_complexity / total_methods

metrics["Максимальна кількість рядків коду в одному класі"] = max_lines_class
metrics["Максимальна кількість рядків коду в одному методі"] = max(method_lines, default=0)
metrics["Максимальна цикломатична складність методів"] = max_complexity
metrics["Коментування коду"] = total_comments

# Assuming we have a function to determine inheritance depth for each class
# This example does not implement it. Placeholder for demonstration:
inheritance_depths = [2]  # Replace with actual calculation
metrics["Максимальна глибина дерева наслідування"] = max(inheritance_depths, default=0)

# Calculate comment percentage
if metrics["Загальна кількість рядків коду у проекті"] > 0:
    metrics["Коментування коду у відсотках"] = (total_comments / metrics[
        "Загальна кількість рядків коду у проекті"]) * 100

# Print metrics
for metric, value in metrics.items():
    print(f"{metric}: {value}")