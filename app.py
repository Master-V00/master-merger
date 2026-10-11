import os
import re
import tkinter as tk

from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from PIL import Image
import numpy as np

from pytoshop.user import nested_layers
from pytoshop import enums


# ---------------- أدوات مساعدة ---------------- #

def select_folder(entry):

    path = filedialog.askdirectory()

    if path:

        entry.config(state=tk.NORMAL)

        entry.delete(0, tk.END)

        entry.insert(0, path)

        entry.config(state="readonly")

        # لو ده المجلد الرئيسي
        if entry == entry_main:

            auto_find_cleaned(path)
            
def auto_find_cleaned(folder_main):

    log_message("🔍 جاري البحث التلقائي عن Cleaned...")

    cleaned = find_cleaned_folder(folder_main)

    if cleaned:

        entry_cleaned.config(state=tk.NORMAL)

        entry_cleaned.delete(0, tk.END)

        entry_cleaned.insert(0, cleaned)

        entry_cleaned.config(state="readonly")

        log_message(f"✅ تم العثور تلقائياً على:\n{cleaned}")

    else:

        log_message("⚠️ لم يتم العثور على مجلد Cleaned")


def log_message(msg, tag="info"):
    log_text.config(state=tk.NORMAL)
    # نمرر الـ tag هنا ليتم تلوين السطر بناءً عليه
    log_text.insert(tk.END, msg + "\n", tag) 
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)
    root.update()


def extract_number(filename):

    match = re.search(r'\d+', filename)

    return int(match.group()) if match else None


# ---------------- البحث التلقائي ---------------- #

def find_cleaned_folder(folder_main):

    folder_main = os.path.abspath(folder_main)

    parent_dir = os.path.dirname(folder_main)

    # البحث جنب المجلد الرئيسي
    try:

        for item in os.listdir(parent_dir):

            item_path = os.path.join(parent_dir, item)

            if (
                os.path.isdir(item_path)
                and "cleaned" in item.lower()
                and os.path.abspath(item_path) != folder_main
            ):

                return item_path

    except Exception:
        pass

    # البحث داخل المجلد الرئيسي
    try:

        for item in os.listdir(folder_main):

            item_path = os.path.join(folder_main, item)

            if (
                os.path.isdir(item_path)
                and "cleaned" in item.lower()
            ):

                return item_path

    except Exception:
        pass

    return None


# ---------------- إنشاء Layer ---------------- #

def create_layer(img, name):

    arr = np.array(img)

    return nested_layers.Image(

        name=name,

        top=0,
        left=0,

        channels={

            enums.ChannelId.red:
                arr[:, :, 0],

            enums.ChannelId.green:
                arr[:, :, 1],

            enums.ChannelId.blue:
                arr[:, :, 2],

            enums.ChannelId.transparency:
                arr[:, :, 3],
        },

        color_mode=enums.ColorMode.rgb
    )


# ---------------- إنشاء PSD ---------------- #

def save_psd(img_original, img_cleaned, output_path):

    layer_original = create_layer(
        img_original,
        "Original"
    )

    layer_cleaned = create_layer(
        img_cleaned,
        "Cleaned"
    )

    # Original تحت - Cleaned فوق
    layers = [
        layer_cleaned,
        layer_original
    ]

    psd = nested_layers.nested_layers_to_psd(

        layers,

        color_mode=enums.ColorMode.rgb,

        compression=enums.Compression.raw
    )

    with open(output_path, "wb") as f:

        psd.write(f)


# ---------------- العملية الأساسية ---------------- #

def start_process():

    folder_main = entry_main.get().strip()

    folder_cleaned = entry_cleaned.get().strip()

    if not folder_main:

        messagebox.showerror(
            "خطأ",
            "اختر المجلد الرئيسي أولاً"
        )

        return

    if not os.path.isdir(folder_main):

        messagebox.showerror(
            "خطأ",
            "المجلد الرئيسي غير صالح"
        )

        return

    # تنظيف اللوج
    log_text.config(state=tk.NORMAL)

    log_text.delete(1.0, tk.END)

    log_text.config(state=tk.DISABLED)

    log_message("⏳ بدء العملية...")

    # البحث التلقائي
    if not folder_cleaned:

        log_message("🔍 جاري البحث التلقائي عن Cleaned...")

        folder_cleaned = find_cleaned_folder(folder_main)

        if folder_cleaned:

            entry_cleaned.config(state=tk.NORMAL)

            entry_cleaned.delete(0, tk.END)

            entry_cleaned.insert(0, folder_cleaned)

            entry_cleaned.config(state="readonly")

            log_message(f"✅ تم العثور على:\n{folder_cleaned}")

        else:

            log_message("❌ لم يتم العثور على مجلد Cleaned")

            messagebox.showerror(
                "خطأ",
                "لم يتم العثور على مجلد Cleaned تلقائياً"
            )

            return

    output_folder = os.path.join(
        folder_main,
        "CBMV"
    )

    os.makedirs(output_folder, exist_ok=True)

    valid_exts = (
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    )

    files_main = [

        f for f in os.listdir(folder_main)

        if f.lower().endswith(valid_exts)
    ]

    files_cleaned = [

        f for f in os.listdir(folder_cleaned)

        if f.lower().endswith(valid_exts)
    ]

    if not files_main:

        log_message("❌ لا توجد صور بالمجلد الرئيسي")

        return

    success = 0

    for file_main in files_main:

        num = extract_number(file_main)

        if num is None:
            continue

        matched = next(

            (
                f for f in files_cleaned
                if extract_number(f) == num
            ),

            None
        )

        if not matched:

            log_message(
                f"⚠️ لا يوجد ملف مطابق لـ {file_main}"
            )

            continue

        try:

            log_message(
                f"⚙️ دمج: {file_main} ➜ {matched}"
            )

            path_main = os.path.join(
                folder_main,
                file_main
            )

            path_cleaned = os.path.join(
                folder_cleaned,
                matched
            )

            img_original = Image.open(
                path_main
            ).convert("RGBA")

            img_cleaned = Image.open(
                path_cleaned
            ).convert("RGBA")

            # توحيد المقاس
            if img_original.size != img_cleaned.size:

                img_cleaned = img_cleaned.resize(

                    img_original.size,

                    Image.Resampling.LANCZOS
                )

            output_path = os.path.join(

                output_folder,

                f"{num}.psd"
            )

            save_psd(

                img_original,

                img_cleaned,

                output_path
            )

            success += 1

            log_message(
                f"✅ تم إنشاء {num}.psd"
            )

        except Exception as e:

            log_message(
                f"❌ خطأ في {file_main}"
            )

            log_message(str(e))

    log_message(
        f"\n🎉 انتهى! تم إنشاء {success} ملفات PSD"
    )

    messagebox.showinfo(

        "تم بنجاح",

        f"اكتملت العملية!\nتم دمج {success} صورة"
    )


# ---------------- الواجهة ---------------- #

root = tk.Tk()

root.title("MASTER MERGER - Pro Edition")

root.geometry("650x550")

root.configure(
    bg="#1e1e1e",
    padx=20,
    pady=20
)

style = ttk.Style()

style.theme_use('clam')

style.configure(
    '.',
    background='#1e1e1e',
    foreground='#ffffff'
)

style.configure(
    'TLabel',
    background='#1e1e1e',
    foreground='#e0e0e0',
    font=("Segoe UI", 10)
)

style.configure(
    'TEntry',
    fieldbackground='#2d2d2d',
    foreground='#ffffff',
    bordercolor='#3d3d3d'
)

style.configure(
    'TButton',
    background='#333333',
    foreground='#ffffff',
    font=("Segoe UI", 9, "bold")
)

style.map(
    'TButton',
    background=[('active', '#444444')]
)

lbl_title = tk.Label(

    root,

    text="MASTER MERGER",

    bg="#1e1e1e",

    fg="#00adb5",

    font=("Segoe UI", 18, "bold")
)

lbl_title.pack(pady=(0, 20))

# Main Folder

ttk.Label(
    root,
    text="المجلد الرئيسي (الصور الأصلية):"
).pack(anchor="w")

frame1 = ttk.Frame(root)

frame1.pack(fill="x", pady=5)

entry_main = ttk.Entry(
    frame1,
    state="readonly"
)

entry_main.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)

ttk.Button(
    frame1,
    text="تصفح",
    command=lambda: select_folder(entry_main)
).pack(side="right")

# Cleaned Folder

ttk.Label(
    root,
    text="مجلد التنظيف (اختياري - سيتم البحث التلقائي عنه):"
).pack(anchor="w", pady=(10, 0))

frame2 = ttk.Frame(root)

frame2.pack(fill="x", pady=5)

entry_cleaned = ttk.Entry(
    frame2,
    state="readonly"
)

entry_cleaned.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)

ttk.Button(
    frame2,
    text="تصفح",
    command=lambda: select_folder(entry_cleaned)
).pack(side="right")

# Start Button

btn_start = tk.Button(

    root,

    text="⚡ ابدأ دمج الصور الآن",

    command=start_process,

    bg="#00adb5",

    fg="#ffffff",

    activebackground="#007a80",

    font=("Segoe UI", 11, "bold"),

    relief="flat",

    cursor="hand2"
)

btn_start.pack(fill="x", pady=25)

# Logs

ttk.Label(
    root,
    text="حالة العمليات الحالية:"
).pack(anchor="w")

log_text = ScrolledText(
    root,
    height=12,
    state=tk.DISABLED,
    bg="#0f111a",
    fg="#d6deeb",
    insertbackground="#ffffff",
    # تغيير الخط ليكون أوضح مع اللغة العربية
    font=("Segoe UI", 11), 
    relief="flat",
    padx=10,
    pady=10
)

log_text.tag_config(
    "info",
    foreground="#4FC3F7"
)

log_text.tag_config(
    "success",
    foreground="#00E676"
)

log_text.tag_config(
    "warning",
    foreground="#FFD54F"
)

log_text.tag_config(
    "error",
    foreground="#FF5252"
)

log_text.pack(
    fill="both",
    expand=True,
    pady=5
)

root.mainloop()