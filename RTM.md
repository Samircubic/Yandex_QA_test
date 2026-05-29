# RTM


| Требование | ID | Сценарий | Автотест | Ожидаемый результат |
| --- | --- | --- | --- | --- |
| Проверить метод `PUT` | `TC-001` | Создание папки в `app:/` | `tests/test_positive_resources.py::test_tc001_create_folder` | API возвращает `201 Created`, созданный ресурс доступен через `GET`, тип ресурса `dir` |
| Проверить метод `GET` | `TC-002` | Получение метаинформации существующей папки | `tests/test_positive_resources.py::test_tc002_get_existing_folder` | API возвращает `200 OK`, ответ содержит данные созданной папки |
| Проверить обработку отсутствующего ресурса для `GET` | `TC-003` | Получение несуществующего ресурса | `tests/test_negative_resources.py::test_tc003_get_missing_resource` | API возвращает `404 Not Found` |
| Проверить метод `POST` | `TC-004` | Перемещение пустой папки | `tests/test_positive_resources.py::test_tc004_move_empty_folder` | API возвращает `201 Created`, старый путь недоступен, новый путь доступен |
| Проверить ошибку перемещения отсутствующего ресурса | `TC-005` | Перемещение несуществующего ресурса | `tests/test_negative_resources.py::test_tc005_move_missing_resource` | API возвращает `404 Not Found` |
| Проверить метод `DELETE` | `TC-006` | Удаление пустой папки | `tests/test_positive_resources.py::test_tc006_delete_empty_folder` | API возвращает `204 No Content`, последующий `GET` возвращает `404 Not Found` |
| Проверить ошибку удаления отсутствующего ресурса | `TC-007` | Удаление несуществующего ресурса | `tests/test_negative_resources.py::test_tc007_delete_missing_resource` | API возвращает `404 Not Found` |
| Проверить связку основных операций | `TC-008` | Жизненный цикл ресурса: создать, прочитать, переместить и удалить | `tests/test_resource_lifecycle.py::test_tc008_resource_lifecycle` | Состояние ресурса корректно меняется после каждой операции |
| Проверить обработку асинхронной операции | `TC-009` | Перемещение непустой папки | `tests/test_resource_lifecycle.py::test_tc009_move_non_empty_folder` | При `202 Accepted` статус операции завершается `success`; после завершения новый путь доступен |
| Проверить конфликт при перемещении в занятый путь | `TC-010` | Перемещение папки в путь существующей папки с `overwrite=false` | `tests/test_negative_resources.py::test_tc010_move_to_existing_folder_conflict` | API возвращает `409 Conflict`, исходная и целевая папки остаются доступными |
| Проверить повторяемость жизненного цикла ресурса | `TC-011` | Два независимых цикла создания, чтения, перемещения и удаления | `tests/test_resource_lifecycle.py::test_tc011_repeated_resource_lifecycle` | Оба цикла завершаются успешно, после удаления ресурсы недоступны через `GET` |
