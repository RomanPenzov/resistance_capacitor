import pandas as pd
import re
import os

# Загрузка файла
base_dir = r"C:\MGU_LAB\res_cap\test" # Укажите путь к вашему CSV-файлу
file_name = "Interface_1k-top-pos_old.csv"
file_path = os.path.join(base_dir, file_name)
data = pd.read_csv(file_path)

# Функция для преобразования значений в столбце Package
def transform_package(value):
    match = re.match(r'([RC])_(\d{4})_\d{4}Metric', value)
    if match:
        prefix = 'RES' if match.group(1) == 'R' else 'CAP'
        size = match.group(2)
        return f"{prefix}{size}"
    return value  # Если значение не подходит под шаблон, оставить без изменений

# Применение функции ко всем значениям в столбце Package
data['Package'] = data['Package'].apply(transform_package)

# Сохранение изменений в новый файл
new_file_name = "Interface_1k-top-pos_old_Transformed.csv"
output_file_path = os.path.join(base_dir, new_file_name)

data.to_csv(output_file_path, index=False)

print(f"The processed file is saved in {output_file_path}")
