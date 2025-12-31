"""
Bild-Optimierungs-Script für Ruby Vandomme Website
===================================================
Erstellt web-optimierte Versionen der Kunstwerk-Bilder.

Vorher: 12-15 MB pro Bild (zu groß für Web!)
Nachher: ~100-300 KB pro Bild (perfekt für schnelles Laden)
"""

from PIL import Image
import os
from pathlib import Path

# Konfiguration
SOURCE_FOLDER = "prints"
OUTPUT_FOLDER = "prints_web"  # Optimierte Bilder hier
MAX_WIDTH = 1200  # Maximale Breite in Pixeln (gut für Web)
JPEG_QUALITY = 85  # Qualität 1-100 (85 ist guter Kompromiss)

def optimize_image(input_path, output_path):
    """Optimiert ein einzelnes Bild für Web-Nutzung."""
    
    with Image.open(input_path) as img:
        # Originalgröße merken
        original_size = os.path.getsize(input_path)
        original_dimensions = img.size
        
        # In RGB konvertieren (für JPEG, falls PNG mit Transparenz)
        if img.mode in ('RGBA', 'P'):
            # Weißer Hintergrund für transparente Bereiche
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Größe anpassen wenn nötig
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
        
        # Als optimiertes JPEG speichern
        img.save(output_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        
        # Neue Größe
        new_size = os.path.getsize(output_path)
        new_dimensions = img.size
        
        return {
            'original_size': original_size,
            'new_size': new_size,
            'original_dimensions': original_dimensions,
            'new_dimensions': new_dimensions,
            'reduction': (1 - new_size / original_size) * 100
        }

def format_size(bytes):
    """Formatiert Bytes in lesbare Größe."""
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1024 * 1024:
        return f"{bytes / 1024:.1f} KB"
    else:
        return f"{bytes / (1024 * 1024):.1f} MB"

def main():
    print("🎨 Ruby Vandomme - Bild-Optimierung")
    print("=" * 50)
    
    # Output-Ordner erstellen
    output_path = Path(OUTPUT_FOLDER)
    output_path.mkdir(exist_ok=True)
    
    # Alle PNG-Dateien im Source-Ordner finden
    source_path = Path(SOURCE_FOLDER)
    images = list(source_path.glob("*.png")) + list(source_path.glob("*.PNG"))
    
    if not images:
        print(f"❌ Keine Bilder in '{SOURCE_FOLDER}' gefunden!")
        return
    
    print(f"📁 Gefunden: {len(images)} Bilder")
    print(f"📂 Output: {OUTPUT_FOLDER}/")
    print()
    
    total_original = 0
    total_new = 0
    
    for img_path in images:
        # Neuer Dateiname (PNG -> JPG)
        new_name = img_path.stem + ".jpg"
        out_path = output_path / new_name
        
        print(f"🖼️  {img_path.name}")
        
        try:
            stats = optimize_image(str(img_path), str(out_path))
            
            total_original += stats['original_size']
            total_new += stats['new_size']
            
            print(f"   {stats['original_dimensions'][0]}x{stats['original_dimensions'][1]} → {stats['new_dimensions'][0]}x{stats['new_dimensions'][1]}")
            print(f"   {format_size(stats['original_size'])} → {format_size(stats['new_size'])} ({stats['reduction']:.1f}% kleiner)")
            print()
            
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            print()
    
    print("=" * 50)
    print(f"✅ Fertig!")
    print(f"📊 Gesamt: {format_size(total_original)} → {format_size(total_new)}")
    print(f"💾 Ersparnis: {format_size(total_original - total_new)} ({(1 - total_new / total_original) * 100:.1f}%)")
    print()
    print(f"👉 Die optimierten Bilder sind in '{OUTPUT_FOLDER}/'")
    print("👉 Kopiere sie nach 'prints/' um sie zu verwenden")
    print("   (oder ich kann die HTML-Dateien anpassen)")

if __name__ == "__main__":
    main()
