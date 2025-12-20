# Конфиг-транслятор (Вариант №21)

Краткое описание
-----------------
Этот учебный инструмент переводит простой конфигурационный язык в XML.
Он читает входной `.conf` файл и генерирует соответствующий `.xml` файл.

Что поддерживается
-------------------
- Однострочные комментарии: `% ...`
- Многострочные комментарии: `=begin` ... `=end`
- Числа: целые и с плавающей точкой / экспонентой
- Массивы: `#( value value ... )`
- Имена: `[_a-zA-Z][_a-zA-Z0-9]*`
- Объявление константы: `global имя = значение;`
- Ссылка на константу: `.{имя}.` (подставляется при трансляции)

Структура проекта
------------------
- `config_tool/cli.py` — основной CLI (аргументы `-i`, `-o`, `--watch`).
- `config_tool/parser.py` — лексер, парсер, AST и генератор XML.
- `safe_run.py` — безопасный одноразовый запуск для Windows.
- `run_safe.bat` — helper для Windows (генерирует примеры и печатает результат).
- `generate_examples.py` — скрипт для генерации `examples/*.xml` из `examples/*.conf`.
- `examples/` — примеры входных `.conf` и сгенерированные `.xml`.
- `tests/test_parser.py` — автоматические тесты (pytest).

Как использовать
---------------
1) Однократная генерация (рекомендуется):

```powershell
python safe_run.py examples\physics.conf examples\physics.xml
Get-Content examples\physics.xml -Raw
```

2) Через CLI:

```powershell
python -m config_tool.cli -i examples\server.conf -o examples\server.xml
Get-Content examples\server.xml -Raw
```

3) Автоматически (watch — пересобирает при изменении входного файла):

```powershell
python -m config_tool.cli -i examples\physics.conf -o examples\physics.xml --watch
# остановка: Ctrl+C
```

4) Быстрый запуск в Windows (двойной клик):

Дважды щёлкните по `run_safe.bat` — он использует явный путь к `python.exe`, сгенерирует `examples/physics.xml` и `examples/server.xml` и покажет их содержимое.

Где править вход
----------------
Редактируйте файлы в каталоге `examples/` (например `examples/server.conf`). Измените числа, массивы `#(...)` или `global` объявления — затем запустите генерацию, и `*.xml` обновится.

Формат XML
-----------
- Число → `<number>...</number>`
- Массив → `<array>...</array>` (рекурсивно для вложенных массивов)
- Глобальная константа `global name = value;` → `<global name="name">...</global>`
- Весь документ обёрнут в `<config>...</config>`

Отладка и проблемы
-------------------
- Синтаксические ошибки и использование несуществующих констант приводят к `ParseError` с указанием строки.
- Если терминал в VS Code внезапно закрывается (код `-1073741510`), попробуйте:
  - запустить команды в внешнем PowerShell (Win -> PowerShell),
  - или запустить `run_safe.bat` двойным кликом,
  - убедиться, что антивирус не убивает python-процессы,
  - использовать явный путь к интерпретатору: `C:\Users\<you>\AppData\Local\Programs\Python\Python313\python.exe`.

Тесты
-----
Установите pytest и запустите:

```powershell
python -m pip install --user pytest
python -m pytest -q
```

Контакты / дополнения
---------------------
Если хотите расширить язык (строки, ключ-значение, вложенные объекты) — можно добавить новые токены и узлы AST в `config_tool/parser.py`.

Автор: Стальмаков Михаил (вариант №21)
"# dz-konfig2" 
"# dz-konfig2" 
