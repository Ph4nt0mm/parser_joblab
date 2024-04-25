# EbeyshiyParserJobLab


* Установите python 3.11
* Установите poetry
```
poetry shell
poetry install
```

Скопировать файл env.example, вставить в ту же папку, переименовав его в env

Прописать переменные как в примере

```
LOGURU_LEVEL=DEBUG
SLEEEP_BETWEEN_REQUESTS=1
MAX_NUM_PAGES_WITH_LINKS=3
```

`LOGURU_LEVEL` - вывод дополнительных логов. Имеет смысл прописать `DEBUG` для более подробной информации или `INFO` 
`SLEEEP_BETWEEN_REQUESTS` - время между запросами к сайту
`MAX_NUM_PAGES_WITH_LINKS` - 