import fitz
PDF_FILE = "Б2 2 этаж.pdf"
doc = fitz.open(PDF_FILE)
page =doc[0]

drawings = page.get_drawings()

print(f"Всего объектов: {len(drawings)}")

stats={}
for d in drawings:
    obj_type = d.get("type")
    width = d.get("width")
    if width is None:
        width_key = None
    else:
        width_key = round(width, 2)
    key = (obj_type, width_key)
    stats[key] = stats.get(key, 0) + 1

# <-- БЕЗ отступа, вне цикла
print("\n=== СТАТИСТИКА ПО ТИПУ И ТОЛЩИНЕ ===")
for key in sorted(stats.keys(), key=lambda k: (str(k[0]), k[1] if k[1] is not None else -1)):
    obj_type, width = key
    print(f"  тип='{obj_type}' | толщина={width} | количество={stats[key]}")
lines = [d for d in drawings if d.get("type") == "s"]
print(f"\nЛиний (type='s') всего: {len(lines)}")

# Разделяем линии по толщине
thin_lines = []     # тонкие — размеры, выноски
medium_lines = []   # средние — перегородки
thick_lines = []    # толстые — стены

for d in lines:
    w = d.get("width")
    if w is None:
        continue
    if w < 0.6:
        thin_lines.append(d)
    elif w < 1.0:
        medium_lines.append(d)
    else:
        thick_lines.append(d)

print(f"  Тонких (< 0.6): {len(thin_lines)}")
print(f"  Средних (0.6–1.0): {len(medium_lines)}")
print(f"  Толстых (>= 1.0): {len(thick_lines)}")

print("\nГОТОВО")