import csv

# Pfad zur CSV-Datei angeben
csv_file = "   "

# Initialisierung der Zähler für die Kombinationen
correct_counts = {'0': 0, '1': 0, '2': 0, '3-5': 0, '5+': 0} # Korrekt erkannte Tiere pro Kategorie
extra_counts = {'0': 0, '1': 0, '2': 0, '3-5': 0, '5+': 0} # Zu viele erkannte Tiere pro Kategorie
total_counts = {'0': 0, '1': 0, '2': 0, '3-5': 0, '5+': 0} # Gesamtanzahl der Bilder pro Kategorie

# Schritt 1: CSV-Datei einlesen und Kombinationen zählen
with open(csv_file, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)

    for row in csv_reader:
        annotation_count = int(row[1]) # Anzahl der Annotationen aus der CSV
        chatgpt_count = int(row[2]) # Anzahl der von ChatGPT erkannten Tiere

        # Kategorie 0 (Annotation = 0)
        if annotation_count == 0:
            total_counts['0'] += 1
            correct_counts['0'] += min(annotation_count, chatgpt_count)
            if chatgpt_count > annotation_count:
                extra_counts['0'] += (chatgpt_count - annotation_count)

        # Kategorie 1 (Annotation = 1)
        elif annotation_count == 1:
            total_counts['1'] += 1
            correct_counts['1'] += min(annotation_count, chatgpt_count)
            if chatgpt_count > annotation_count:
                extra_counts['1'] += (chatgpt_count - annotation_count)

        # Kategorie 2 (Annotation = 2)
        elif annotation_count == 2:
            total_counts['2'] += 1
            correct_counts['2'] += min(annotation_count, chatgpt_count)
            if chatgpt_count > annotation_count:
                extra_counts['2'] += (chatgpt_count - annotation_count)

        # Kategorie 3-5 (Annotation 3-5)
        elif 3 <= annotation_count <= 5:
            total_counts['3-5'] += 1
            correct_counts['3-5'] += min(annotation_count, chatgpt_count)
            if chatgpt_count > annotation_count:
                extra_counts['3-5'] += (chatgpt_count - annotation_count)

        # Kategorie 5+ (Annotation > 5)
        elif annotation_count > 5:
            total_counts['5+'] += 1
            correct_counts['5+'] += min(annotation_count, chatgpt_count)
            if chatgpt_count > annotation_count:
                extra_counts['5+'] += (chatgpt_count - annotation_count)

# Schritt 2: Präzision berechnen und ausgeben
# Präzision für Kategorien 0, 1, 2, 3-5, und 5+
for category in ['0', '1', '2', '3-5', '5+']:
    total_images = total_counts[category]
    correct = correct_counts[category]
    extra = extra_counts[category]
    precision = (correct / total_images) * 100 if total_images > 0 else 0
    print(f"Kategorie {category}: {correct}/{total_images} korrekt, {extra} zu viel erkannt")
    print(f"Präzision: {precision:.2f}%")