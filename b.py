
from pathlib import Path

# Pfad zur CoNLL-U Datei
file_path = r'C:\Users\bashi\Downloads\UD_German-HDT-dev\de_hdt-ud-dev.conllu'
output_path = r'C:\Users\bashi\Downloads\UD_German-HDT-dev\de_hdt-ud-dev-transformed'

def parse_conllu(file_content):
    sätze = []
    satz = []
    for line in file_content.split('\n'):
        if line.strip() == '':
            if satz:
                sätze.append(satz)
                satz = []
        elif not line.startswith('#'):
            satz.append(line.split('\t'))
    return sätze

def transform_to_four_columns_format(satz):
    transformiert = []
    for token in satz:
        if len(token) < 10:
            continue  # Überspringe Tokens mit weniger als 10 Elementen
        if '-' in token[0] or '.' in token[0]:
            continue  # Überspringe Multi-Token-Wörter und Leerzeichen
        try:
            index = int(token[0]) - 1  # Konvertiere 1-basierten Index zu 0-basiert
            wort = token[1]
            kopf = int(token[6]) - 1  # Konvertiere 1-basierten Index zu 0-basiert, Wurzel wird -1
            kopf = -1 if kopf == -1 else kopf
            label = token[7]
            transformiert.append(f"{index}\t{wort}\t{kopf}\t{label}")
        except ValueError:
            continue  # Überspringe Tokens, bei denen die Konvertierung fehlschlägt
    return transformiert

def transform_conllu_to_custom_format(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    
    sätze = parse_conllu(file_content)
    transformierte_sätze = []
    for satz in sätze:
        transformierter_satz = transform_to_four_columns_format(satz)
        transformierte_sätze.append('\n'.join(transformierter_satz))
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write('\n\n'.join(transformierte_sätze))
        file.write('\n')  # Sicherstellen, dass die Datei mit einer neuen Zeile endet

# Transformation ausführen
transform_conllu_to_custom_format(file_path, output_path)

print(f"Transformation abgeschlossen. Transformierte Datei gespeichert unter: {output_path}")

