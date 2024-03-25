## Python

- скачиваем дистрибутив с [официального сайта](https://www.python.org/downloads/windows/)
- запускаем установщик
    - ставим checkbox "Add python.exe to PATH"
    - прожимаем next/next для установки
- проверяем в cmd или powershell командой `python --version`
  ```shell
  C:\Users\alexigna> python --version
  Python 3.12.2
  ```
- создаем и переходим в папку с проектом
  ```shell
  C:\Users\alexigna> mkdir C:\Users\alexigna\Documents\projects\01-intro
  C:\Users\alexigna> cd C:\Users\alexigna\Documents\projects\01-intro
  ```
- создаем виртуальное окружение (что это такое - далее) командой `python -m venv venv`
  ```shell
  C:\Users\alexigna\Documents\projects\01-intro> python -m venv venv
  ```
- активируем виртуальное окружение командой `venv\Scripts\activate`
  ```shell
  C:\Users\alexigna\Documents\projects\01-intro> venv\Scripts\activate
  (venv) C:\Users\alexigna\Documents\projects\01-intro>
  ```
- устанавливаем ipython командой `pip install ipython`
  ```shell
  (venv) C:\Users\alexigna\Documents\projects\01-intro> pip install ipython
  Collecting ipython
    Using cached ipython-8.22.2-py3-none-any.whl.metadata (4.8 kB)
  ...
  Successfully installed ... ipython-8.22.2 ...
  ```
- запускаем ipython и пробуем любое действие
  ```shell
  (venv) C:\Users\alexigna\Documents\projects\01-intro> ipython
  Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 22:02:46) [MSC v.1937 64 bit (ARM64)]
  Type 'copyright', 'credits' or 'license' for more information
  IPython 8.22.2 -- An enhanced Interactive Python. Type '?' for help.

  In [1]: print("works")
  works

  In [2]:
  ```
- закрываем интерпретатор и даактивируем виртуальное окружение командой `venv\Scripts\deactivate`
  ```shell
  In [2]: exit

  (venv) C:\Users\alexigna\Documents\projects\01-intro> venv\Scripts\deactivate
  C:\Users\alexigna\Documents\projects\01-intro>
  ```