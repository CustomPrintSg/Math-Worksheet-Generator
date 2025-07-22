# Math Worksheet Generator 🧮

A comprehensive web application built with Streamlit that generates professional math worksheets in PDF format. Perfect for teachers, parents, and tutors who need high-quality printable math practice materials.

## Features

### 🔢 Multiple Operations
- **Addition**: Numbers from 1 to 999 (user-configurable)
- **Subtraction**: Always positive results, user-configurable ranges
- **Multiplication**: 1-4 digit numbers for each factor
- **Division**: With or without remainders, or mixed

### 📄 Two Layout Formats
- **Format 1**: Grid layout (4×5 = 20 problems per page) with answer boxes
- **Format 2**: List layout with 1-3 columns and 10-15 questions per column

### 📋 Professional PDF Output
- High-quality PDF generation
- Name and date fields on each page
- Space for branding/logo
- Automatic answer key generation
- Multi-page support with ZIP downloads

## Installation & Setup

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/math-worksheet-generator.git
cd math-worksheet-generator
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
streamlit run app.py
```

5. **Open browser:**
Navigate to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Community Cloud](https://share.streamlit.io/)**

3. **Click "New app"**

4. **Connect your GitHub repository:**
   - Repository: `yourusername/math-worksheet-generator`
   - Branch: `