import pandas as pd
import os
import re

# Укажите путь к вашему CSV-файлу
base_dir = r"C:\MGU_LAB\res_cap\test"
file_name = "Interface_1k-top-pos_old.csv"
file_path = os.path.join(base_dir, file_name)

# Чтение файла CSV
data = pd.read_csv(file_path)

# Функция для обновления значений в столбце 'Val' в зависимости от 'Package'
def update_val(row):
    package, val = row['Package'], row['Val']
    
    if re.search(r'R_\d{4}_\d{4}Metric', package):  # Условие для резисторов
        val = re.sub(r'(\d+)\.(\d+)', r'\1R\2', val)  # Заменяем точки на R
        val = val.replace("k", "k").replace("kR", "k")
    
    elif re.search(r'C_\d{4}_\d{4}Metric', package):  # Условие для конденсаторов
        if re.match(r'^\d+[un](?:\s.*)?$', val):  # Если формат корректный (например, "1n", "10n 2kV"), оставить без изменений
            pass
        elif val.startswith("0.") and "u" in val:  # Специальный случай для значений типа "0.1u"
            val = val.replace("u", "")  # Просто убираем символ "u"
        elif '.' in val and 'u' in val:  # Преобразуем значения типа "2.2u" → "2u2"
            val = val.replace('u', '')  # Убираем "u"
            val = val.replace('.', 'u', 1)  # Заменяем первую точку на "u"
        elif '.' in val and 'n' in val:  # Преобразуем значения типа "4.7n" → "4n7"
            val = val.replace('n', '')  # Убираем "n"
            val = val.replace('.', 'n', 1)  # Заменяем первую точку на "n"
        else:  # Для остальных случаев убираем символы "u" или "n"
            val = val.replace("u", "").replace("n", "")
    
    return val

# Применяем функцию к каждому ряду
data['Val'] = data.apply(update_val, axis=1)

# Укажите путь для сохранения нового файла
new_file_name = "Interface_1k-top-pos_old_Transformed_2.csv"
output_file_path = os.path.join(base_dir, new_file_name)

# Сохранение изменений в новый файл
data.to_csv(output_file_path, index=False)

print(f"The processed file is saved in {output_file_path}")
