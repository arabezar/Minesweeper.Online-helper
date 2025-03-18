# Minesweeper.Online-helper
![Github last commit](https://img.shields.io/github/last-commit/arabezar/Minesweeper.Online-helper)
[![GitHub Stars](https://img.shields.io/github/stars/arabezar/Minesweeper.Online-helper?style=flat)](https://github.com/arabezar/xkeen-tg/stargazers)
[![License](https://img.shields.io/github/license/arabezar/Minesweeper.Online-helper.svg?style=flat&color=orange)](LICENSE)
[![YooMoney](https://img.shields.io/badge/donate-YooMoney-8037fd.svg?style=flat)](https://yoomoney.ru/to/410013875426872)
[![CloudTips](https://img.shields.io/badge/donate-CloudTips-598bd7.svg?style=flat)](https://pay.cloudtips.ru/p/6352cb45)

## Кратко
[Minesweeper.Online](https://minesweeper.online/) Helper - это проект на Python, предназначенный для помощи игрокам в решении головоломок Minesweeper. Он предоставляет инструменты и алгоритмы для улучшения игрового процесса.

Достаточно при открытой игре в браузере запустить скрипт, который сам найдёт игру и выполнит заложенные действия.

На данном этапе проект содержит всего один скрипт:
- `calc_cells`, подсчитывающий количество различных типов клеток на странице игры, что удобно для игр типа "без флагов", когда необходимо подсчитать, сколько неоткрытых клеток осталось
    <details>
        <summary>Пример</summary>
        Для вот такой игры<br>
        <img src="images/4396610651-hd-24-5150537.png"><br>
        скрипт выдаёт подсказку:

    ```
    Количество ненажатых клеток: 106, из них мин: 0, всего мин: 99, осталось открыть: 7
    ```
    </details>

> [!IMPORTANT]
> **Ограничения**
> - Проект требует установленного браузера Chrome (хотя может найти игру в любом браузере)
> - Поддерживается только русский язык (можно добавить и другие при необходимости, если люди пожелают)
> - Проект требует установленного Python (автор использовал 3.13, но, скорее всего, подойдёт и ≥3.9, не проверялось)

## Установка
Чтобы установить Minesweeper.Online Helper, выполните следующие шаги:
1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/arabezar/Minesweeper.Online-helper.git
    ```
2. Перейдите в каталог проекта:
    ```bash
    cd Minesweeper.Online-helper
    ```
3. Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv venv
    venv\Scripts\activate # Windows
    # venv/bin/activate # Linux
    ```
3. Установите необходимые зависимости:
    ```bash
    pip install -r requirements.txt
    ```
4. Пропишите пути к кастомному профилю Chrome в `settings.py`, если желаете, иначе будет использоваться профиль по умолчанию

## Использование
Чтобы использовать Minesweeper.Online Helper, откройте игру в браузере и в терминале выполните следующую команду:
```bash
python <script_name>.py
```

## Вклад
Все идеи, пожелания и замечания категорически приветствуются в разделах [Issues](https://github.com/arabezar/Minesweeper.Online-helper/issues) и [Discussions](https://github.com/arabezar/Minesweeper.Online-helper/discussions).

---
Поддержи автора, купив ему :beers: или :coffee: ([тынц](https://yoomoney.ru/to/410013875426872) или [тынц](https://pay.cloudtips.ru/p/6352cb45))
