# VKStat

VKStat -- это набор из скриптов, которые выполняют загрузку и обработку
социальных связей из популярной социальной сети [Вконтакте](https://vk.com).
Данные, загружаемые посредством VK API, представляются в виде 
[социального графа](https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B3%D1%80%D0%B0%D1%84):
![Пример социального графа]
(https://github.com/budnyjj/vkstat/blob/master/examples/with_gephi.png)

## установка

Эти скрипты написаны на **Python 3** со следующими внешними зависимостями:
* [vkontakte3](https://github.com/budnyjj/vkontakte3) --
VK API для Python 3 (обязательно)
* [networkx](https://networkx.github.io/) --
создание и обработка графов (обязательно)
* [PyYAML](https://pypi.python.org/pypi/PyYAML) --
чтение/запись графа в формате YAML (опционально)
* [PrettyTable](https://pypi.python.org/pypi/PrettyTable) --
печать данных графа в табличном виде (опционально)
* [matplotlib](http://matplotlib.org/) -- визуализация графа средствами Python
(опционально)
* [gephi](http://gephi.github.io/) -- визуализация графа средствами Gephi
(опционально)

## обзор функциональности

```bash
get.py --> process.py ---> plot.py
                       |
                       --> info.py
```

* [get.py](https://github.com/budnyjj/vkstat/blob/master/get.py) --
  используется для получения данных через VK API.
  Вы можете указать **несколько UID-ов пользователей**
  и установить **уровень рекурсии** (чтобы получать друзей друзей). 
  Для ускорения процесса загрузки можно использовать **мультипроцессинг**.

  Загруженный граф может быть сохранен в форматах  **Pickle** или **YAML**.

* [process.py](https://github.com/budnyjj/vkstat/blob/master/process.py) --
  используется для фильтрации узлов графа по различным признакам,
  а также конвертации графа между различными форматами.

* [info.py](https://github.com/budnyjj/vkstat/blob/master/info.py) --
  используется для табличного анализа содержимого графа.
  На данный момент, этот скрипт предоставляет данные о
  **радиусе** и **диаметре** графа,
  а также **число друзей**, **число фолловеров**, **pagerank**,
  и т. д.

* [plot.py](https://github.com/budnyjj/vkstat/blob/master/plot.py) --
  используется для отображения графа средствами matplotlib.
  Построенный граф может быть исследован интерактивно или сохранения
  в виде форматах png или pdf. 
  По причинам низкой производительности рекомендуется
  **строить графы размером не более 500 узлов**.