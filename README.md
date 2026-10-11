<div align="center">

# 🗂️ MASTER MERGER

### دمج صور المانجا في ملفات PSD بطبقتين — Merge Manga Scans into Layered PSD

[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Windows-exe-0078D6?logo=windows&logoColor=white)](https://github.com/masterV00-hub/master-merger/releases/latest)

### ⬇️ [تحميل البرنامج — Download EXE](https://github.com/masterV00-hub/master-merger/releases/latest)

**ادمج مجلد الصور الأصلية مع مجلد التنظيف في ملفات PSD جاهزة للتلوين والتحرير.**

**Merge original + cleaned scan folders into layered PSD files ready for typesetting.**

</div>

---

<div align="center">

## 🌍 اختار اللغة — Choose Language

### [🇪🇬 العربية](#-النسخة-العربية) &nbsp;&nbsp;|&nbsp;&nbsp; [🇬🇧 English](#-english-version)

</div>

---

<a id="-النسخة-العربية"></a>

<div dir="rtl">

## 🇪🇬 النسخة العربية

### 📖 الفكرة

**MASTER MERGER** أداة ويندوز بواجهة عربية داكنة: تختار مجلد الصور الأصلية ومجلد التنظيف، والبرنامج يطابق الصور حسب رقمها ويطلع ملف `.psd` من طبقتين (`Original` تحت + `Cleaned` فوق) في مجلد `CBMV` — جاهز للتلوين والكتابة عليه في فوتوشوب.

### ✨ المميزات

- 🖼️ يدعم `png` / `jpg` / `jpeg` / `webp`
- 🔗 مطابقة تلقائية بالرقم + توحيد المقاس (LANCZOS)
- 🎚️ طبقتان + شفافية داخل كل PSD
- 📁 يلاقي مجلد التنظيف لوحده لو جنب المجلد الأصلي
- 🪟 نسخة exe لا تحتاج بايثون

### 🚀 التشغيل

**الأسهل:** حمّل `MASTER_MERGER.exe` من [صفحة الإصدارات](https://github.com/masterV00-hub/master-merger/releases/latest) وشغّله.

**من المصدر:**

```bash
pip install -r requirements.txt
python app.py
```

**إعادة بناء الـ exe:**

```bash
pyinstaller MASTER_MERGER.spec
```

### 📁 الهيكل

```
master-merger/
├── app.py                # البرنامج (الواجهة + الدمج)
├── icon.ico              # الأيقونة
├── MASTER_MERGER.spec    # إعداد PyInstaller
├── requirements.txt
└── README.md
```

</div>

---

<a id="-english-version"></a>

## 🇬🇧 English Version

### 📖 Overview

**MASTER MERGER** is a Windows tool with an Arabic dark UI: pick the originals folder and the cleaned folder, and it matches pages by number, producing 2-layer `.psd` files (`Original` bottom + `Cleaned` top) in a `CBMV` folder — ready for typesetting in Photoshop.

### ✨ Features

- 🖼️ Supports `png` / `jpg` / `jpeg` / `webp`
- 🔗 Auto number matching + resize to original (LANCZOS)
- 🎚️ Two layers + transparency per PSD
- 📁 Auto-detects the cleaned folder next to the originals
- 🪟 Standalone exe, no Python needed

### 🚀 Run

**Easiest:** download `MASTER_MERGER.exe` from [Releases](https://github.com/masterV00-hub/master-merger/releases/latest) and run it.

**From source:**

```bash
pip install -r requirements.txt
python app.py
```

**Rebuild the exe:**

```bash
pyinstaller MASTER_MERGER.spec
```

### 📁 Structure

```
master-merger/
├── app.py                # App (GUI + merging)
├── icon.ico              # Icon
├── MASTER_MERGER.spec    # PyInstaller config
├── requirements.txt
└── README.md
```

---

<div align="center">

### [⬆️ back to top / العودة للأعلى](#-master-merger)

MIT License.

</div>
