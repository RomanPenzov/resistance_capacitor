import pandas as pd
import os
import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Функция для обновления значений в столбце 'Val' в зависимости от 'Package'
def update_val(row):
    package, val = row['Package'], row['Val']
    
    if re.search(r'R_\d{4}_\d{4}Metric', package):  # Условие для резисторов
        if '.' in val and not val.endswith('k'):  # Преобразуем значения типа "0.5" → "0R5"
            val = val.replace('.', 'R', 1)  # Заменяем первую точку на "R"
        elif '.' in val and 'k' in val:  # Преобразуем значения типа "3.3k" → "3k3"
            val = val.replace('k', '')  # Убираем "k"
            val = val.replace('.', 'k', 1)  # Заменяем первую точку на "k"
    
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

# Функция для преобразования значений в столбце Package
def transform_package(value):
    match = re.match(r'([RC])_(\d{4})_\d{4}Metric', value)
    if match:
        prefix = 'RES' if match.group(1) == 'R' else 'CAP'
        size = match.group(2)
        return f"{prefix}{size}"
    return value  # Если значение не подходит под шаблон, оставить без изменений

def replace_value(value):
    replacements = [
        (r'^D_SMA', 'SMA'),
        #(r'^LED_\d{4}', lambda m: m.group(0).split('_')[0]),
        (r'^LED_\d{4}', lambda m: m.group(0)),
        (r'^Crystal_SMD_HC49-SD', 'HC49SM'),
        (r'^SOT-89-3', 'SOT-89'),
        (r'^L_\d{4}', lambda m: 'IND' + m.group(0).split('_')[1]),
        (r'^LQFP-48_', 'LQFP-48'),
        (r'^SOT-353_SC-70-5', 'SOT-353'),
        (r'^SOP-16_', 'SOP-16'),
        (r'^SOT-252-2', 'DPAK'),
        (r'^SOIC-8_', 'SO8'),
        (r'^DX-BT18', 'SOIC-16W'),
        (r'^SOIC-20W', 'so-20'),
        (r'^Wide_SOIC-8', 'SO8-veryWIDE'),
        (r'^wide_SOIC-8', 'SO8-veryWIDE'),
        (r'^Transformer_TSHT5\.8-01', 'tsht5_8_01'),
        (r'^CP_EIA-6032-28_Keme', 'C-type'),
    ] 

    for pattern, replacement in replacements:
        match = re.match(pattern, value)
        if match:
            return replacement(match) if callable(replacement) else replacement

    return value

def main():
    # Открытие диалогового окна выбора файла
    root = Tk()
    root.withdraw()  # Скрыть главное окно Tkinter
    file_path = askopenfilename(
        title="Select a CSV file to process",
        filetypes=[("CSV files", "*.csv")],
    )

    if not file_path:
        print("No file was selected. Terminating program.")
        return

    # Чтение файла CSV
    data = pd.read_csv(file_path)

    # Применение обработки значений столбца 'Val'
    data['Val'] = data.apply(update_val, axis=1)

    # Применение обработки значений столбца 'Package' по компонентам RES и CAP
    data['Package'] = data['Package'].apply(transform_package)
    
    # Применение обработки значений столбца 'Package' по ДРУГИМ компонентам (кроме RES и CAP)
    data['Package'] = data['Package'].apply(replace_value)
    
    

    # Формирование пути для сохранения нового файла
    base_dir, original_name = os.path.split(file_path)
    new_file_name = os.path.splitext(original_name)[0] + "_Transformed.csv"
    output_file_path = os.path.join(base_dir, new_file_name)

    # Сохранение результата в новый файл
    data.to_csv(output_file_path, index=False)
    print(f"Processing completed. Result saved in: {output_file_path}")

if __name__ == "__main__":
    main()
