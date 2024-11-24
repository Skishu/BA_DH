#pip install matplotlib

import json
import csv
import matplotlib.pyplot as plt
from collections import Counter

# Pfade zu Ihren Dateien  
annotations_file = "   "  # Pfad zur COCO-Annotationsdatei (JSON)
responses_file = "   "  # Pfad zum ChatGPT-Response (JSON)
output_csv = "   "  # Pfad zur Ausgabedatei (CSV)

# COCO-Annotationsdatei einlesen
with open(annotations_file, 'r') as f:
    coco_data = json.load(f)

# Erstellen eines Mappings von image_id zum file_name
image_id_to_file = {image['id']: image['file_name'] for image in coco_data['images']}

# Zählen der Annotationen pro Bild
annotations_per_image = {}
for annotation in coco_data['annotations']:
    image_id = annotation['image_id']
    file_name = image_id_to_file[image_id]
    annotations_per_image[file_name] = annotations_per_image.get(file_name, 0) + 1

# ChatGPT-Antworten einlesen
with open(responses_file, 'r') as f:
    chatgpt_data = json.load(f)

# Extrahieren der Anzahl der Tiere pro Bild aus den Antworten
animals_per_image_chatgpt = {}
for item in chatgpt_data:
    image_file = item['image_file']
    response = item['response']
    if "No, 0" in response:
        count = 0
    else:
        try:
            count = int(response.split(',')[1].strip().rstrip('.'))
        except ValueError:
            count = 0
    animals_per_image_chatgpt[image_file] = count

# Präzision und Statistiken berechnen
total_annotations = 0
total_chatgpt_annotations = 0
precision_sum = 0
matching_results = []

# Zähler für die neuen Statistiken
exact_match_0 = 0
exact_match_1 = 0
exact_match_2 = 0
exact_match_3_5 = 0
exact_match_5_plus = 0
total_images = 0

all_files = set(annotations_per_image.keys()) | set(animals_per_image_chatgpt.keys())

# Liste zur Speicherung der ChatGPT-Annotationszahlen
chatgpt_annotation_counts = []

for file_name in all_files:
    annotations_count = annotations_per_image.get(file_name, 0)
    chatgpt_count = animals_per_image_chatgpt.get(file_name, 0)

    # Hinzufügen zur Gesamtsumme
    total_annotations += annotations_count
    total_chatgpt_annotations += chatgpt_count

    # Berechnung der Präzision für das aktuelle Bild
    if annotations_count == 0 and chatgpt_count == 0:
        precision = 100.0
    elif annotations_count == 0 or chatgpt_count == 0:
        precision = 0.0
    else:
        precision = (min(annotations_count, chatgpt_count) / max(annotations_count, chatgpt_count)) * 100

    precision_sum += precision
    total_images += 1

    # Speichern der ChatGPT-Anzahl für das Balkendiagramm
    chatgpt_annotation_counts.append(chatgpt_count)

    matching_results.append({
        'Datei': file_name,
        'Anzahl der Annotationen': annotations_count,
        'Anzahl der Animals durch ChatGPT': chatgpt_count,
        'Präzision (%)': precision
    })

# Ergebnisse in CSV schreiben
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Datei', 'Anzahl der Annotationen', 'Anzahl der Animals durch ChatGPT', 'Präzision (%)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for result in matching_results:
        writer.writerow(result)

# Balkendiagramm erstellen
# Zählen, wie oft eine bestimmte Anzahl von Tieren durch ChatGPT erkannt wurde
chatgpt_count_distribution = Counter(chatgpt_annotation_counts)

# X-Werte: Die Anzahl der Annotationen, aufsteigend sortiert, ab 1 (0 wird ausgeschlossen)
x_values = sorted([x for x in chatgpt_count_distribution.keys() if x > 0])

# Y-Werte: Die Häufigkeit der jeweiligen Annotationen
y_values = [chatgpt_count_distribution[x] for x in x_values]

# Balkendiagramm erstellen und anzeigen
plt.figure(figsize=(10, 6))
plt.bar(x_values, y_values, color='blue')  # Balkendiagramm mit blauen Balken
plt.title('ChatGPT-Annotationen - high')  # Titel des Diagramms
plt.xlabel('Anzahl der Annotationen durch ChatGPT')  # X-Achsenbeschriftung
plt.ylabel('Häufigkeit')  # Y-Achsenbeschriftung
plt.grid(axis='y')  # Gitterlinien auf der Y-Achse
plt.xticks(x_values)  # X-Achse entsprechend den eindeutigen Werten
plt.tight_layout()

# Balkendiagramm anzeigen
plt.show()

# Durchschnittliche Präzision berechnen
average_precision = precision_sum / total_images

# Ausgabe der Gesamtsummen und der durchschnittlichen Präzision
print(f"Gesamtzahl der Annotationen: {total_annotations}")  # Ausgabe der Gesamtzahl der Annotationen
print(f"Gesamtzahl der von ChatGPT erkannten Annotationen: {total_chatgpt_annotations}")  # Ausgabe der Gesamtzahl
print(f"Durchschnittliche Präzision: {average_precision:.2f}%")  # Ausgabe der durchschnittlichen Präzision