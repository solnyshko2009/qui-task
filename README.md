# FASTQ File Analyzer

Профессиональное приложение для анализа файлов формата FASTQ с графическим интерфейсом. Предоставляет статистику и визуализацию данных секвенирования в стиле FastQC.


## Требования

### Системные требования
- **ОС**: Windows 10+, macOS 10.14+, или Linux (Ubuntu 16.04+)
- **Память**: 4 GB RAM (рекомендуется 8 GB для больших файлов)
- **Место на диске**: 500 MB свободного места

### Программные требования
- **Python**: версия 3.7 или выше
- **Установленные пакеты**:
  - `matplotlib >= 3.3.0`
  - `numpy >= 1.19.0`
  - `pandas >= 1.3.0`
  - `seaborn >= 0.11.0`

## Установка

### Способ 1: Установка из исходного кода

1. **Скачайте приложение**:
   ```bash
   git clone https://github.com/your-username/fastq-analyzer.git
   cd fastq-analyzer


2. **Установите зависимости:**
  `bash
  pip install -r requirements.txt `

3. **Проверьте установку:**
 `bash
  python fastq_analyzer.py --help `
### Способ 2: Прямая установка
1. **Скачайте файлы:**

 - fastq_analyzer.py

 - fastq_reader.py

 - fastq_gui.py

2. **Установите зависимости:**
`bash
pip install matplotlib numpy pandas seaborn`

## Запуск
`python fastq_analyzer.py`


