from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import io
from typing import List, Dict
from datetime import datetime
# --- compatibility shim for old method name ---
if not hasattr(canvas.Canvas, "drawCentredText"):
    canvas.Canvas.drawCentredText = canvas.Canvas.drawCentredString
# ----------------------------------------------

class PDFCreator:
    """Creates PDF worksheets and answer keys."""
    
    def __init__(self, logo_path: str = "logo.png"):
        """Set up page geometry, styles, and optional branding image."""
        self.page_width, self.page_height = letter
        self.margin = 0.75 * inch
        self.styles = getSampleStyleSheet()
        self.logo_path = logo_path        # ← store once, reuse everywhere

    
    def create_grid_worksheet(self, problems: List[Dict], title: str, operation: str) -> bytes:
        """Create a grid format worksheet (4x5 layout)."""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        self._draw_header(c, "")             # pass empty string, prints nothing

        
        # Grid of problems (4 columns, 5 rows)
        start_x = self.margin
        start_y = self.page_height - 2.5 * inch
        
        col_width = (self.page_width - 2 * self.margin) / 4
        row_height = (start_y - self.margin) / 5
        
        for i, problem in enumerate(problems[:20]):  # Ensure max 20 problems
            row = i // 4
            col = i % 4
            
            x = start_x + col * col_width
            y = start_y - row * row_height
            
            # Draw problem box
            self._draw_grid_problem(c, problem, x, y, col_width, row_height)
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_grid_answer_key(self, problems: List[Dict], title: str, operation: str) -> bytes:
        """Create answer key for grid format."""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        self._draw_header(c, "")             # pass empty string, prints nothing

        
        # Grid of answers
        start_x = self.margin
        start_y = self.page_height - 2.5 * inch
        
        col_width = (self.page_width - 2 * self.margin) / 4
        row_height = (start_y - self.margin) / 5
        
        for i, problem in enumerate(problems[:20]):
            row = i // 4
            col = i % 4
            
            x = start_x + col * col_width
            y = start_y - row * row_height
            
            # Draw problem with answer
            self._draw_grid_answer(c, problem, x, y, col_width, row_height)
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_list_worksheet(self, problems: List[Dict], title: str, operation: str,
                            columns: int, questions_per_col: int) -> bytes:
        """Create a list format worksheet."""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        self._draw_header(c, "")             # pass empty string, prints nothing

        
        # Calculate layout
        start_x = self.margin
        start_y = self.page_height - 2.5 * inch
        col_width = (self.page_width - 2 * self.margin) / columns
        
        problem_idx = 0
        for col in range(columns):
            x = start_x + col * col_width
            y = start_y
            
            for row in range(min(questions_per_col, len(problems) - problem_idx)):
                if problem_idx >= len(problems):
                    break
                
                problem = problems[problem_idx]
                self._draw_list_problem(c, problem, problem_idx + 1, x, y)
                y -= 0.6 * inch
                problem_idx += 1
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def create_list_answer_key(self, problems: List[Dict], title: str, operation: str,
                             columns: int, questions_per_col: int) -> bytes:
        """Create answer key for list format."""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        self._draw_header(c, "")             # pass empty string, prints nothing

        
        # Calculate layout
        start_x = self.margin
        start_y = self.page_height - 2.5 * inch
        col_width = (self.page_width - 2 * self.margin) / columns
        
        problem_idx = 0
        for col in range(columns):
            x = start_x + col * col_width
            y = start_y
            
            for row in range(min(questions_per_col, len(problems) - problem_idx)):
                if problem_idx >= len(problems):
                    break
                
                problem = problems[problem_idx]
                self._draw_list_answer(c, problem, problem_idx + 1, x, y)
                y -= 0.6 * inch
                problem_idx += 1
        
        c.save()
        buffer.seek(0)
        return buffer.getvalue()
    
    def _draw_header(self, c: canvas.Canvas, title: str):
        """Draw page header with name/date fields and branding space."""
        # Branding space (placeholder)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredText(self.page_width / 2, self.page_height - 0.5 * inch, 
                         "Math Worksheet Generator")
        
        # Name and Date fields
        c.setFont("Helvetica", 12)
        name_x = self.margin
        date_x = self.page_width - 2.5 * inch
        y_pos = self.page_height - 1.2 * inch
        
        c.drawString(name_x, y_pos, "Name: " + "_" * 30)
        c.drawString(date_x, y_pos, "Date: " + "_" * 15)
        
        # Title
        #c.setFont("Helvetica-Bold", 14)
        #c.drawCentredText(self.page_width / 2, self.page_height - 1.8 * inch, title)
    
    def _draw_grid_problem(
        self,
        c: canvas.Canvas,
        problem: Dict,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        """Draw one problem (grid format)."""
        # Draw border
        c.rect(x + 5, y - height + 10, width - 10, height - 20)

        c.setFont("Helvetica", 14)

        # ─────────────────── division (long‑division house) ───────────────────
        if problem["operation"] == "÷":
            divisor, dividend = problem["num2"], problem["num1"]
            text = f"{divisor}){dividend}"

            # Draw the text centred
            c.drawCentredText(x + width / 2, y - height / 2 + 6, text)

            # Compute bar coordinates
            up_to_paren = f"{divisor})"
            full_text_width = c.stringWidth(text, "Helvetica", 14)
            offset_left = c.stringWidth(up_to_paren, "Helvetica", 14)

            bar_start_x = (x + width / 2) - full_text_width / 2 + offset_left
            bar_end_x   = (x + width / 2) + c.stringWidth(str(dividend), "Helvetica", 14) / 2
            bar_y       = y - height / 2 + 18      # tweak vertical offset here

            c.setLineWidth(0.5)
            c.line(bar_start_x - 3, bar_y, bar_end_x + 10, bar_y)
            return  # ← stop here so we don't reach the generic centering block
        # ───────────────────────────────────────────────────────────────────────

        # All other operations (+, −, ×)
        problem_text = problem["formatted_problem"]

        # Centre multi‑line text in the box
        text_lines = problem_text.split("\n")
        line_height = 16
        total_h = len(text_lines) * line_height
        start_y = y - (height - total_h) / 2 - 10
        current_y = start_y
        for i, line in enumerate(text_lines):
            c.drawCentredText(x + width / 2, current_y, line)

            # next baseline: use a tighter gap if the NEXT line is the underscore
            if i + 1 < len(text_lines) and set(text_lines[i + 1]) == {"_"}:
                current_y -= 5   # bar only 10 pt below the numbers
            else:
                current_y -= 16   # regular gap


    
    def _draw_grid_answer(self, c: canvas.Canvas, problem: Dict, x: float, y: float,
                         width: float, height: float):
        """Draw a problem with answer in grid format."""
        # Draw border
        c.rect(x + 5, y - height + 10, width - 10, height - 20)
        
        # Draw problem
        c.setFont("Helvetica", 12)
        problem_y = y - height / 3
        c.drawCentredText(x + width / 2, problem_y, problem["problem"])
        
        # Draw answer
        c.setFont("Helvetica-Bold", 14)
        answer_text = problem.get("answer_text", str(problem["answer"]))
        answer_y = y - 2 * height / 3
        c.drawCentredText(x + width / 2, answer_y, answer_text)
    
    def _draw_list_problem(self, c: canvas.Canvas, problem: Dict, number: int, x: float, y: float):
        """Draw a problem in list format."""
        c.setFont("Helvetica", 12)
        
        if problem["operation"] == "÷":
            problem_text = f"{number}. {problem['problem']} = ________"
        else:
            problem_text = f"{number}. {problem['problem']} = ________"
        
        c.drawString(x + 10, y, problem_text)
    
    def _draw_list_answer(self, c: canvas.Canvas, problem: Dict, number: int, x: float, y: float):
        """Draw a problem with answer in list format."""
        c.setFont("Helvetica", 12)
        answer_text = problem.get("answer_text", str(problem["answer"]))
        problem_text = f"{number}. {problem['problem']} = {answer_text}"
        c.drawString(x + 10, y, problem_text)
    
    def add_branding_image(self, c: canvas.Canvas, image_path: str):
        """Add branding image to the header (if available)."""
        try:
            from reportlab.lib.utils import ImageReader
            import os
            
            if os.path.exists(image_path):
                img = ImageReader(image_path)
                # Position image in top center
                img_width = 1 * inch
                img_height = 0.5 * inch
                x = (self.page_width - img_width) / 2
                y = self.page_height - 0.8 * inch
                
                c.drawImage(img, x, y, width=img_width, height=img_height)
        except Exception:
            # If image loading fails, continue without image
            pass
