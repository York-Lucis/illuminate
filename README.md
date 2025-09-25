# Illuminate - PDF Enhancement Tool

Illuminate is a powerful PDF enhancement application that uses AI super-resolution technology to restore and improve the quality of old, scanned, or damaged PDF documents. The tool automatically upscales all pages from a PDF while preserving the document's historical character and readability.

## ✨ Features

- **AI-Powered Super-Resolution**: Uses Real-ESRGAN models to enhance image quality with 2x, 4x, or 8x upscaling
- **OCR Text Extraction**: Automatically extracts text from scanned documents using Tesseract OCR
- **Multi-language Translation**: Translates extracted text from Latin to English (configurable)
- **Batch Processing**: Processes entire PDFs automatically, page by page
- **User-Friendly GUI**: Clean, modern interface built with ttkbootstrap
- **Command-Line Interface**: Full CLI support for automation and scripting
- **Progress Tracking**: Real-time progress monitoring during processing
- **Benchmarking Tools**: Built-in performance comparison utilities

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Tesseract OCR** (install from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki))
- **Poppler** (for PDF to image conversion)
- **CUDA-compatible GPU** (optional, for faster processing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/illuminate.git
   cd illuminate
   ```

2. **Install Python dependencies:**
   ```bash
   cd main
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR:**
   - **Windows**: Download from [UB-Mannheim releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **Install Poppler:**
   - **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows)
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils`

5. **Download AI Models:**
   The application will automatically download Real-ESRGAN model weights on first run, or you can manually place them in the `weights/` directory:
   - `RealESRGAN_x2.pth` (2x upscaling)
   - `RealESRGAN_x4.pth` (4x upscaling)
   - `RealESRGAN_x8.pth` (8x upscaling)

## 📖 Usage

### Graphical User Interface

Launch the application with the GUI:

```bash
cd main
python main.py
```

**GUI Features:**
- Browse and select your PDF file
- Choose output directory
- Click "Run" to start processing
- Monitor progress with the built-in progress bar

### Command Line Interface

For automation and batch processing:

```bash
cd main
python core.py --pdf "path/to/your/document.pdf" --output "path/to/output/directory"
```

**CLI Arguments:**
- `--pdf`: Path to the PDF file you want to enhance
- `--output`: Directory where the enhanced PDF will be saved

### Example Usage

```bash
# Enhance a single PDF
python core.py --pdf "old_book.pdf" --output "./enhanced_books/"

# The output will be saved as "Illuminate - old_book.pdf"
```

## 🔧 Configuration

### OCR Settings

Modify OCR parameters in `core.py`:

```python
self.ocr_path = 'C:\Program Files\Tesseract-OCR'  # Path to Tesseract installation
self.ocr_input_lang = 'lat'        # Input language (Latin)
self.ocr_output_lang = 'eng'       # Output language (English)
self.ocr_extra_params = '-c tessedit_do_invert=0'  # Additional Tesseract parameters
```

### Super-Resolution Settings

Adjust upscaling factor in `super_sampling.py`:

```python
IMAGE_SCALE = 2  # Options: 2, 4, or 8
```

### Translation Settings

Configure translation in `translation.py`:

```python
def translate_text(text, src_language, out_language='en'):
    # Change 'en' to your desired output language
```

## 📁 Project Structure

```
illuminate/
├── main/
│   ├── core.py              # Main processing logic
│   ├── main.py              # GUI application
│   ├── super_sampling.py    # AI upscaling functionality
│   ├── translation.py       # Text translation utilities
│   ├── requirements.txt     # Python dependencies
│   ├── weights/             # AI model weights
│   │   ├── RealESRGAN_x2.pth
│   │   ├── RealESRGAN_x4.pth
│   │   └── RealESRGAN_x8.pth
│   └── benchmark/           # Performance testing
│       ├── benchmark_input/ # Test images
│       └── benchmark_output/ # Results
├── LICENSE
└── README.md
```

## 🧪 Benchmarking

The application includes built-in benchmarking tools to compare processing performance:

```python
# Run benchmark comparison
from super_sampling import benchmark_results
benchmark_results()
```

This will process test images and compare the performance of different algorithms.

## 🔍 How It Works

1. **PDF Conversion**: Converts PDF pages to high-resolution PNG images
2. **AI Enhancement**: Applies Real-ESRGAN super-resolution to improve image quality
3. **OCR Processing**: Extracts text from enhanced images using Tesseract
4. **Translation**: Translates extracted text (configurable languages)
5. **Reassembly**: Combines enhanced images back into a new PDF

## 🛠️ Dependencies

- **chardet**: Character encoding detection
- **googletrans**: Google Translate API wrapper
- **img2pdf**: Image to PDF conversion
- **numpy**: Numerical computing
- **pdf2image**: PDF to image conversion
- **Pillow**: Python Imaging Library
- **PyPDF2**: PDF manipulation
- **RealESRGAN**: AI super-resolution models
- **torch**: PyTorch deep learning framework
- **ttkbootstrap**: Modern Tkinter themes

## 🐛 Troubleshooting

### Common Issues

1. **Tesseract not found**: Ensure Tesseract is installed and in your system PATH
2. **CUDA out of memory**: Reduce batch size or use CPU processing
3. **PDF conversion fails**: Install Poppler utilities
4. **Model download fails**: Check internet connection or manually download weights

### Performance Tips

- Use GPU acceleration for faster processing
- Process smaller PDFs for testing
- Adjust image scale based on your needs (2x is usually sufficient)
- Ensure sufficient disk space for temporary files

## 📄 License

This project is licensed under the terms specified in the LICENSE file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## ⚠️ Disclaimer

This tool is designed for research and educational purposes. Please ensure you have the right to process and enhance any documents you use with this tool. The AI models may not be suitable for all types of documents, and results may vary based on input quality.

## 🔮 Future Enhancements

- Support for additional file formats (TIFF, JPEG, etc.)
- More language options for OCR and translation
- Batch processing multiple PDFs
- Custom AI model training
- Web-based interface
- Cloud processing options

---

**Illuminate** - Bringing old documents back to life with AI-powered enhancement technology.