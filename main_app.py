import streamlit as st
import io
import zipfile
from datetime import datetime
from worksheet_generator import WorksheetGenerator
from pdf_creator import PDFCreator
import base64

def main():
    st.set_page_config(
        page_title="Math Worksheet Generator",
        page_icon="🧮",
        layout="wide"
    )
    
    # Header with branding space
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🧮 Math Worksheet Generator")
        st.markdown("*Create professional math worksheets in seconds*")
    
    # Sidebar for main controls
    with st.sidebar:
        st.header("Worksheet Settings")
        
        # Operation Selection
        operation = st.selectbox(
            "Select Operation",
            ["Addition", "Subtraction", "Multiplication", "Division"]
        )
        
        # Difficulty Settings based on operation
        st.subheader("Difficulty Settings")
        
        difficulty_settings = {}
        
        if operation == "Addition":
            max_num = st.slider("Maximum number", 1, 999, 100)
            difficulty_settings = {"max_num": max_num}
            
        elif operation == "Subtraction":
            max_num = st.slider("Maximum number", 1, 999, 100)
            difficulty_settings = {"max_num": max_num}
            
        elif operation == "Multiplication":
            digits_1 = st.slider("First number digits", 1, 4, 1)
            digits_2 = st.slider("Second number digits", 1, 4, 1)
            difficulty_settings = {"digits_1": digits_1, "digits_2": digits_2}
            
        elif operation == "Division":
            max_dividend = st.slider("Maximum dividend", 10, 999, 100)
            max_divisor = st.slider("Maximum divisor", 2, 20, 10)
            remainder_type = st.radio(
                "Remainder type",
                ["No remainders", "With remainders", "Mixed"]
            )
            difficulty_settings = {
                "max_dividend": max_dividend,
                "max_divisor": max_divisor,
                "remainder_type": remainder_type
            }
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Layout Options")
        
        # Format 1 settings
        st.write("**Format 1: Grid Layout (4×5 = 20 problems per page)**")
        format1_pages = st.number_input(
            "Pages of Format 1",
            min_value=0,
            max_value=50,
            value=1,
            key="format1"
        )
        
        # Format 2 settings
        st.write("**Format 2: List Layout**")
        format2_pages = st.number_input(
            "Pages of Format 2",
            min_value=0,
            max_value=50,
            value=0,
            key="format2"
        )
        
        if format2_pages > 0:
            columns = st.radio(
                "Number of columns for Format 2",
                [1, 2, 3],
                index=1
            )
            questions_per_col = st.slider(
                "Questions per column",
                10, 15, 12
            )
        else:
            columns = 2
            questions_per_col = 12
    
    with col2:
        st.subheader("Preview & Generate")
        
        # Show preview of selected settings
        total_pages = format1_pages + format2_pages
        
        if total_pages > 0:
            st.info(f"""
            **Worksheet Summary:**
            - Operation: {operation}
            - Total pages: {total_pages}
            - Format 1 pages: {format1_pages}
            - Format 2 pages: {format2_pages}
            """)
            
            # Generate worksheets button
            if st.button("🔄 Generate Worksheets", type="primary"):
                with st.spinner("Generating worksheets..."):
                    try:
                        # Initialize generator and PDF creator
                        generator = WorksheetGenerator()
                        pdf_creator = PDFCreator()
                        
                        # Generate worksheets and answer keys
                        worksheet_files = []
                        answer_files = []
                        
                        # Generate Format 1 worksheets
                        for page in range(format1_pages):
                            problems = generator.generate_problems(
                                operation.lower(),
                                20,  # 4x5 grid
                                difficulty_settings
                            )
                            
                            # Create worksheet PDF
                            worksheet_pdf = pdf_creator.create_grid_worksheet(
                                problems,
                                f"Worksheet - Page {page + 1}",
                                operation
                            )
                            worksheet_files.append((f"worksheet_grid_{page + 1}.pdf", worksheet_pdf))
                            
                            # Create answer key PDF
                            answer_pdf = pdf_creator.create_grid_answer_key(
                                problems,
                                f"Answer Key - Page {page + 1}",
                                operation
                            )
                            answer_files.append((f"answers_grid_{page + 1}.pdf", answer_pdf))
                        
                        # Generate Format 2 worksheets
                        questions_total = columns * questions_per_col
                        for page in range(format2_pages):
                            problems = generator.generate_problems(
                                operation.lower(),
                                questions_total,
                                difficulty_settings
                            )
                            
                            # Create worksheet PDF
                            worksheet_pdf = pdf_creator.create_list_worksheet(
                                problems,
                                f"Worksheet - List Page {page + 1}",
                                operation,
                                columns,
                                questions_per_col
                            )
                            worksheet_files.append((f"worksheet_list_{page + 1}.pdf", worksheet_pdf))
                            
                            # Create answer key PDF
                            answer_pdf = pdf_creator.create_list_answer_key(
                                problems,
                                f"Answer Key - List Page {page + 1}",
                                operation,
                                columns,
                                questions_per_col
                            )
                            answer_files.append((f"answers_list_{page + 1}.pdf", answer_pdf))
                        
                        # Create download options
                        if total_pages == 1:
                            # Single file downloads
                            st.success("✅ Worksheets generated successfully!")
                            
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                st.download_button(
                                    "📄 Download Worksheet",
                                    worksheet_files[0][1],
                                    file_name=worksheet_files[0][0],
                                    mime="application/pdf"
                                )
                            
                            with col_b:
                                st.download_button(
                                    "📋 Download Answer Key",
                                    answer_files[0][1],
                                    file_name=answer_files[0][0],
                                    mime="application/pdf"
                                )
                        
                        else:
                            # Multiple files - create ZIP
                            worksheet_zip = create_zip_file(worksheet_files, "worksheets")
                            answer_zip = create_zip_file(answer_files, "answer_keys")
                            
                            st.success("✅ Worksheets generated successfully!")
                            
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                st.download_button(
                                    "📦 Download All Worksheets (ZIP)",
                                    worksheet_zip,
                                    file_name=f"math_worksheets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                                    mime="application/zip"
                                )
                            
                            with col_b:
                                st.download_button(
                                    "📦 Download All Answer Keys (ZIP)",
                                    answer_zip,
                                    file_name=f"answer_keys_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                                    mime="application/zip"
                                )
                    
                    except Exception as e:
                        st.error(f"Error generating worksheets: {str(e)}")
                        st.error("Please check your settings and try again.")
        
        else:
            st.warning("Please select at least one page to generate.")

def create_zip_file(files, folder_name):
    """Create a ZIP file containing multiple PDF files."""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filename, file_data in files:
            zip_file.writestr(filename, file_data)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

if __name__ == "__main__":
    main()
