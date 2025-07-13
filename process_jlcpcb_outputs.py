import os
import csv
import sys
import shutil
from zipfile import ZipFile

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def read_csv_with_fallback(path):
    try:
        with open(path, newline='', encoding='utf-8-sig') as f:
            return list(csv.reader(f))
    except UnicodeDecodeError:
        with open(path, newline='', encoding='latin1') as f:
            return list(csv.reader(f))

def process_bom(project_dir, output_dir):
    import csv

    bom_dir = os.path.join(project_dir, "BOM")
    bom_file = next((f for f in os.listdir(bom_dir) if f.endswith(".csv")), None)
    if not bom_file:
        print("⚠️ No BOM CSV found")
        return

    input_path = os.path.join(bom_dir, bom_file)
    rows = read_csv_with_fallback(input_path)

    header = [h.strip().lower() for h in rows[0]]
    data = rows[1:]

    try:
        idx_comment    = header.index("comment")
        idx_designator = header.index("designator")
        idx_footprint  = header.index("footprint")
        # description optional
    except ValueError as e:
        print(f"❌ BOM headers not matched: {e}")
        return

    output_path = os.path.join(output_dir, "BOM.csv")
    with open(output_path, 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(["Comment", "Designator", "Footprint", "JLCPCB Part #"])

        for row in data:
            if len(row) <= max(idx_comment, idx_designator, idx_footprint):
                continue  # Zeile unvollständig → überspringen

            comment    = row[idx_comment].strip()
            designator = row[idx_designator].strip()
            footprint  = row[idx_footprint].strip()
            partnum    = comment  # oder ""

            writer.writerow([comment, designator, footprint, partnum])
    print(f"✅ BOM written: {output_path}")

def read_csv_dict_fallback(path):
    import csv
    try:
        with open(path, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            raw_header = next(reader)
            header = [h.strip().strip('"') for h in raw_header]
            return [dict(zip(header, [cell.strip() for cell in row])) for row in reader]
    except UnicodeDecodeError:
        with open(path, newline='', encoding='latin1') as f:
            reader = csv.reader(f)
            raw_header = next(reader)
            header = [h.strip().strip('"') for h in raw_header]
            return [dict(zip(header, [cell.strip() for cell in row])) for row in reader]


def process_pick_place(project_dir, output_dir):
    import csv

    pp_dir = os.path.join(project_dir, "Pick Place")
    pp_file = next((f for f in os.listdir(pp_dir) if f.lower().endswith(".csv")), None)
    if not pp_file:
        print("⚠️ No Pick & Place CSV found")
        return

    input_path = os.path.join(pp_dir, pp_file)

    # Datei komplett einlesen
    with open(input_path, encoding='utf-8-sig', errors='replace') as f:
        lines = f.readlines()

    # Suche nach gültiger Headerzeile mit mindestens 5 Spalten
    data_start_index = None
    for i, line in enumerate(lines):
        if "Designator" in line and "Center-X" in line and "Rotation" in line:
            try:
                test = next(csv.reader([line]))
                if len(test) >= 5:
                    data_start_index = i
                    break
            except Exception:
                continue

    if data_start_index is None:
        print("❌ Keine gültige Datenzeile in Pick&Place-Datei gefunden.")
        return

    # Ab Headerzeile lesen
    csv_lines = lines[data_start_index:]
    reader = csv.reader(csv_lines)
    header = next(reader)
    header = [h.strip().strip('"') for h in header]

    try:
        i_designator = header.index("Designator")
        i_mid_x = header.index("Center-X(mm)")
        i_mid_y = header.index("Center-Y(mm)")
        i_layer = header.index("Layer")
        i_rotation = header.index("Rotation")
    except ValueError as e:
        print(f"❌ Spalten nicht gefunden: {e}")
        print(f"Header erkannt als: {header}")
        return

    output_path = os.path.join(output_dir, "PickAndPlace.csv")
    with open(output_path, 'w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(["Designator", "Mid X", "Mid Y", "Layer", "Rotation"])

        for row in reader:
            if len(row) <= max(i_designator, i_mid_x, i_mid_y, i_layer, i_rotation):
                continue
            writer.writerow([
                row[i_designator].strip(),
                row[i_mid_x].strip(),
                row[i_mid_y].strip(),
                row[i_layer].strip(),
                row[i_rotation].strip()
            ])

    print(f"✅ Pick & Place geschrieben: {output_path}")

def zip_gerber(project_dir, output_dir):
    gerber_dir = os.path.join(project_dir, "Gerber")
    drill_dir = os.path.join(project_dir, "NC Drill")
    zip_path = os.path.join(output_dir, "jlcpcb_gerber.zip")

    with ZipFile(zip_path, 'w') as zipf:
        for folder in [gerber_dir, drill_dir]:
            if os.path.isdir(folder):
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    zipf.write(file_path, arcname=file)
    print(f"✅ Gerber + Drill zipped: {zip_path}")

def main():
    if len(sys.argv) < 2:
        print("❌ Please provide project path")
        sys.exit(1)

    project_dir = sys.argv[1]
    output_dir = os.path.join(project_dir, "JLCPCB")
    ensure_dir(output_dir)

    process_bom(project_dir, output_dir)
    process_pick_place(project_dir, output_dir)
    zip_gerber(project_dir, output_dir)

if __name__ == "__main__":
    main()
