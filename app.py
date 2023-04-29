import sys
import yaml
import pathlib
from pathlib import Path
from docopt import docopt

USAGE = """
Build system.

Usage:
  app.py list builds
  app.py list tasks
  app.py get task <task_name>
  app.py get build <build_name>
  app.py (-h | --help)

Options:
  -h --help     Show this screen.
"""

def load_tasks(tasks_file):
    # loading a file with tasks and handling errors

    try:
        with open(tasks_file) as file:
            tasks = yaml.safe_load(file)["tasks"]
        if not tasks:
            raise ValueError(f"No tasks defined in tasks file '{tasks_file}'")
        tasks_names = set()
        tasks_dict = {}       
        for task in tasks:
            name = task.get('name')
            if not name:
                raise ValueError("Invalid task definition: missing 'name'")
            if name in tasks_names:
                raise ValueError(f"Duplicate task name '{name}' in tasks file '{tasks_file}'")
            tasks_names.add(name)
            dependencies = task.get("dependencies", [])
            tasks_dict[name] = dependencies
        return tasks_dict
    except FileNotFoundError:
        print(f"Error: {tasks_file} not found")
        sys.exit(1)
    except (yaml.parser.ParserError, yaml.parser.ScannerError):
        print(f"Error: Invalid YAML formatting in {tasks_file}")
        sys.exit(1)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        sys.exit(1)

def load_builds(builds_file):
    # loading a file with builds and handling errors

    try:
        with open(builds_file) as file:
            builds = yaml.safe_load(file)["builds"]
        if not builds:
            raise ValueError(f"No builds defined in tasks file '{builds_file}'")
        builds_names = set()
        builds_dict = {}
        for build in builds:
            name = build.get("name")
            if not name:
                raise ValueError("Invalid build definition: missing 'name'")
            if name in builds_names:
                raise ValueError(f"Duplicate build name '{name}' in builds file '{builds_file}'")
            builds_names.add(name)
            dependencies = build.get("tasks", [])
            builds_dict[name] = dependencies
        return builds_dict
    except FileNotFoundError:
        print(f"Error: {builds_file} not found")
        exit(1)
    except (yaml.parser.ParserError, yaml.parser.ScannerError):
        print(f"Error: Invalid YAML formatting in {builds_file}")
        exit(1)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        sys.exit(1)

def get_builds(builds_dict):
    # view names of loaded builds

    print(f"List of available builds:")
    for build in builds_dict:
        print(f" * {build}")

def get_tasks(tasks_dict):
    # view names of loaded tasks

    print(f"List of available tasks:")
    for task in tasks_dict:
        print(f" * {task}")

def get_task_info(task_name, tasks_dict):
    # displaying detailed information about the task and its dependencies
    try:
        dependencies = tasks_dict[task_name]
        print(f"Task info:\n * name: {task_name}\n * dependencies: {', '.join(dependencies)}")
    except KeyError:
        print(f"Task '{task_name}' not found")
        sys.exit(1)

def get_build_info(build_name, builds_dict, tasks_dict):
    # displaying detailed information about the build and its tasks and dependencies

    try:

        def recursion_dependencies(task_name, task_list, visited):
            # a recursive function to collect all the dependencies of a task
            if task_name not in tasks_dict:
                raise ValueError(f"Task '{task_name}' not found in tasks.yaml file")
            visited.add(task_name)
            for dependency in tasks_dict[task_name]:
                if dependency in visited:
                    raise ValueError(f"Cyclic dependency found: '{dependency}' depends on '{task_name}'")
                recursion_dependencies(dependency, task_list, visited)
            if task_name not in task_list:
                task_list.append(task_name)
            

        build_tasks = builds_dict[build_name]
        task_list = []
        visited = set()     # to check cyclic dependency

        # Collect all the tasks of the build and their dependencies
        for task_name in build_tasks:
            recursion_dependencies(task_name, task_list, visited)  
            if task_name not in task_list:
                task_list.append(task_name)

        task_info = []
        # Construct output string
        for task_name in task_list:
            task_info.append(f"{task_name}")
            task_info_str = ", ".join(task_info)
        return print(f"Build info:\n * name: {build_name}\n * tasks:{task_info_str}")
    except KeyError:
        print(f"Build '{build_name}' not found")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__== "__main__":
    arguments = docopt(USAGE)

     # Set default paths for files
    tasks_file = Path(pathlib.Path.cwd(), 'tasks.yaml')
    builds_file = Path(pathlib.Path.cwd(), 'builds.yaml')

    tasks_dict = load_tasks(tasks_file)
    builds_dict = load_builds(builds_file)

    if arguments["list"] and arguments["tasks"]:
        get_tasks(tasks_dict)
    elif arguments["list"] and arguments["builds"]:
        get_builds(builds_dict)
    elif arguments["get"] and arguments["task"]:
        get_task_info(arguments["<task_name>"], tasks_dict)
    elif arguments["get"] and arguments["build"]:
        get_build_info(arguments["<build_name>"], builds_dict, tasks_dict)
