from app import load_tasks, load_builds, get_builds, get_tasks, get_task_info, get_build_info
import pytest

def test_load_yaml_file():

    # Test missing file
    with pytest.raises(SystemExit) as e:
        load_tasks("nonexistent_file.yaml") 
    assert e.type == SystemExit
    assert e.value.code == 1


def test_invalid_yaml():
    
    # Test invalid file
    with pytest.raises(SystemExit) as e:
        load_builds("tests/invalid_file.yaml")
    assert e.type == SystemExit
    assert e.value.code == 1

def test_load_tasks():

    # Test correct tasks file
    tasks_dict = load_tasks("tests/correct_tasks.yaml")
    assert tasks_dict == {
        "task1": ["task2"],
        "task2": ["task5"],
        "task3": [],
        "task4": ["task1", "task3"],
        "task5": [],
        "task6": ["task7"],
        "task7": ["task6"],
    }

def test_load_builds():

    # Test correct buidls file
    builds_dict = load_builds("tests/correct_builds.yaml")
    assert builds_dict == {
        "build1": ["task1", "task2"],
        "build2": ["task3"],
        "build3": ["task4"],
    }

def test_get_tasks(capsys):

    # Test correct list tasks
    tasks_dict = load_tasks("tests/correct_tasks.yaml")
    get_tasks(tasks_dict)
    captured = capsys.readouterr()
    assert captured.out == "List of available tasks:\n * task1\n * task2\n * task3\n * task4\n * task5\n * task6\n * task7\n"

def test_get_builds(capsys):

    # Test correct list builds
    builds_dict = load_builds("tests/correct_builds.yaml")
    get_builds(builds_dict)
    captured = capsys.readouterr()
    assert captured.out == "List of available builds:\n * build1\n * build2\n * build3\n"

def test_get_task_info(capsys):

    # Test correct info tasks
    tasks_dict = load_tasks("tests/correct_tasks.yaml")
    get_task_info("task4", tasks_dict)
    captured = capsys.readouterr()
    assert captured.out == "Task info:\n * name: task4\n * dependencies: task1, task3\n"

def test_get_build_info(capsys):

    # Test correct info builds
    builds_dict = load_builds("tests/correct_builds.yaml")
    tasks_dict = load_tasks("tests/correct_tasks.yaml")
    get_build_info("build3", builds_dict, tasks_dict)
    captured = capsys.readouterr()
    assert captured.out == "Build info:\n * name: build3\n * tasks:task5, task2, task1, task3, task4\n"

def test_load_invalid_tasks():

    # Test invalid in tasks file
    with pytest.raises(SystemExit) as e:
        load_tasks("tests/no_tasks.yaml") 
    assert e.type == SystemExit
    assert e.value.code == 1

def test_load_invalid_tasks2():

    # Test duplicate 'name' in tasks file
    with pytest.raises(SystemExit) as e:
        load_tasks("tests/duplicate_name_tasks.yaml") 
    assert e.type == SystemExit
    assert e.value.code == 1

def test_load_invalid_tasks3():

    # Test missing 'name' in tasks file
    with pytest.raises(SystemExit) as e:
        load_tasks("tests/missing_name_tasks.yaml") 
    assert e.type == SystemExit
    assert e.value.code == 1

def test_load_invalid_tasks3():

    # Test missing 'name' in tasks file
    with pytest.raises(SystemExit) as e:
        load_tasks("tests/missing_name_tasks.yaml") 
    assert e.type == SystemExit
    assert e.value.code == 1

def test_invalid_info_task():

    # Test not found 'task_name' in tasks list
    tasks_dict = load_tasks("tests/correct_tasks.yaml")
    with pytest.raises(SystemExit) as e:
        get_task_info("task8", tasks_dict)
    assert e.type == SystemExit
    assert e.value.code == 1

def test_invalid_info_build():

    # Test not found 'build_name' in builds list
    tasks_dict = load_tasks("tests/correct_tasks.yaml")
    builds_dict = load_builds("tests/correct_builds.yaml")
    with pytest.raises(SystemExit) as e:
        get_build_info("build8", builds_dict, tasks_dict)
    assert e.type == SystemExit
    assert e.value.code == 1

def test_invalid_info_build2():

    # Test not found builds in builds file
    with pytest.raises(SystemExit) as e:
        load_builds("tests/no_builds.yaml")
    assert e.type == SystemExit
    assert e.value.code == 1

def test_cyclic_dependency():

    # Test cyclic dependencies in builds
    builds_dict = load_builds("tests/cyclic_builds.yaml")
    tasks_dict = load_tasks("tests/correct_tasks.yaml")
    with pytest.raises(SystemExit) as e:
        get_build_info("build4", builds_dict, tasks_dict)
    assert e.type == SystemExit
    assert e.value.code == 1
