# VKStat

VKStat -- это набор скриптов, которые выполняют загрузку и обработку
социальных связей из социальной сети [Вконтакте](https://vk.com).
Данные, загружаемые посредством VK API, представляются в виде 
[социального графа]
(https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D1%86%D0%B8%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9_%D0%B3%D1%80%D0%B0%D1%84):

![Пример социального графа]
(https://github.com/budnyjj/vkstat/blob/master/doc/pic/clusterization.png)

## Установка

Чтобы запустить VKStat, нужно сначала **установить зависимости**,
а затем склонировать этот репозиторий.
Проверить работоспособность любого из скриптов можно следующим образом:

```bash
./get.py --help
```

Если запускается без ошибок, значит работает :)

### Зависимости

VKStat написан на **Python 3** со следующими внешними **зависимостями**:

#### Обязательные

* [vkontakte3](https://github.com/budnyjj/vkontakte3) --
VK API для Python 3
* [networkx](https://networkx.github.io/) --
создание и обработка графов

#### Необязательные

* [PyYAML](https://pypi.python.org/pypi/PyYAML) --
чтение/запись графа в формате YAML
* [PrettyTable](https://pypi.python.org/pypi/PrettyTable) --
вывод данных графа в табличном виде (info.py)
* [matplotlib](http://matplotlib.org/) -- визуализация графа средствами Python
(plot.py)
* [Gephi](http://gephi.github.io/) -- визуализация графа средствами Gephi

## Документация

* [Обзор функциональности](https://github.com/budnyjj/vkstat/blob/master/doc/overview.md)
* [Визуализация графов](https://github.com/budnyjj/vkstat/blob/master/doc/plot.md)
* [Примеры социальных графов](https://github.com/budnyjj/vkstat/blob/master/doc/examples.md)
