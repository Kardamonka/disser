import fitz #PyMuPDF

PDF_FILE = "Б2 2 этаж.pdf"

#Открытие ПДФ файла
doc=fitz.open(PDF_FILE)
print(f"Открыть файл: {PDF_FILE}")
print(f"Всего страниц: {len(doc)}")

page =doc[0] #first pages
print(f"\n Размер страницы: {page.rect}")

# ===== 1. ТЕКСТ =====
print ("\n"+"="*60) #Что делает эта строка?
print ("ТЕКСТ (ПЕРВЫЕ 30 БЛОКОВ)")
print ("="*60)

text_blocks = page.get_text("dict")["blocks"]
text_count=0
for block in text_blocks:
    if block.get("type")==0:
        for line in block.get("lines",[]):
            for span in line.get("spans",[]):
                text=span["text"].strip()
                if text:
                    bbox=span["bbox"]
                    print (f"'{text}' | коорд: ({bbox[0]:.0f}, {bbox[1]:.0f}) | размер: {span['size']:.1f}")
                    text_count+=1
                    if text_count>=30:
                        break
                if text_count>=30:
                    break
            if text_count>=30:
                break

print (f"\n(всего текстовых блоков на странице: {sum(1 for b in text_blocks if b.get('type')==0)})")

# ===== 2. ГРАФИЧЕСКИЕ ОБЪЕКТЫ =====
print("\n" + "="*60)
print("ГРАФИЧЕСКИЕ ОБЪЕКТЫ")
print("="*60)

drawings = page.get_drawings()
print(f"Всего объектов: {len(drawings)}")
widths = {}
for d in drawings:
    w=d.get("width",0)
    if w:
        widths[round(w,2)]=widths.get(round(w,2),0)+1
print("\nРаспределение по толщине линии (толщина: количество):")
for w in sorted(widths.keys()):
    print (f"   {w}:: {widths[w]}")

# Первые 10 объектов — подробно
print("\nПервые 10 объектов:")
for i, d in enumerate(drawings[:10]):
    print(f"\n--- Объект {i} ---")
    print(f"  Тип: {d['type']}")
    print(f"  Кол-во элементов: {len(d['items'])}")
    print(f"  Толщина: {d.get('width')}")
    print(f"  Цвет: {d.get('color')}")
    print(f"  Заливка: {d.get('fill')}")
    print(f"  Bbox: {d['rect']}")
    for j, item in enumerate(d['items'][:3]):
        print(f"    Элемент {j}: {item[0]} -> {item[1:]}")

# ===== 3. ИЗОБРАЖЕНИЯ =====
print("\n" + "="*60)
print("ИЗОБРАЖЕНИЯ")
print("="*60)
images = page.get_images()
print(f"Всего изображений: {len(images)}")

print("\n" + "="*60)
print("ГОТОВО")
print("="*60)