# Test_SaberInteractive
Python version: 3.10.11
Установленные пакеты:
 - docopt: 0.6.2
 - pytest: 7.3.1
 - PyYAML: 6.0

Запуск программы с исходными файлами `builds.yaml` и `tasks.yaml`:

python3 app.py list tasks/builds
python3 app.py get build<build_name>/task<task_name>

Запуск тестов:
pytest tests_app.py

К программе прикладываю следующие тестовые файлы:
    - correct_builds.yaml - корректный файл с билдами
    - correct_tasks.yaml - корректный файл с задачами и зависимостями
    - cyclic_builds.yaml - проверка обработки исключения при циклической зависимости
    - duplicate_name_tasks.yaml - проверка уникальности имен задач
    - invalid_file.yaml - неверный формат данных файла .yaml
    - missing_name_tasks.yaml - пропущено слово 'name' в файле с задачами
    - no_builds.yaml - файл без билдов
    - no_tasks.yaml - файл без задач