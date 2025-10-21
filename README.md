
2. **Создайте виртуальное окружение (необязательно, но рекомендуется):**
```bash
py -m venv venv
```

3. **Активируйте виртуальное окружение:**
*   В Windows:
```bash
venv\Scripts\Activate.ps1
```
*   В macOS/Linux:
```bash
source venv/bin/activate
```

4. **Установите необходимые зависимости:**
```bash
py -m pip install -r requirements.txt
```

4. **Запуск:**
```bash
py main.py
```

- __Удалите текущий (неверный) удаленный репозиторий `origin`:__

  ```bash
  git remote remove origin
  ```

- __Добавьте правильный удаленный репозиторий `origin`:__

  ```bash
  git remote add origin https://github.com/DemonDis/chat_fn.git
  ```

- __Установите основную ветку как `main`:__

  ```bash
  git branch -M main
  ```

- __Отправьте ваш код в удаленный репозиторий:__

  ```bash
  git push -u origin main
  ```
