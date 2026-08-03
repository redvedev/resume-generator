"""Compile LaTeX to PDF - Simple version that works like manual compilation."""

import logging
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from src.application.config import TEMPLATE_DIR, OUTPUT_DIR

logger = logging.getLogger(__name__)


def _cleanup_latex_artifacts(tex_dir: Path, tex_stem: str) -> None:
    artifacts = [
        f"{tex_stem}.aux",
        f"{tex_stem}.log",
        f"{tex_stem}.out",
        f"{tex_stem}.toc",
        f"{tex_stem}.synctex.gz",
        "resume.cls",
    ]

    for artifact in artifacts:
        artifact_path = tex_dir / artifact
        if artifact_path.exists():
            try:
                artifact_path.unlink()
                logger.info("Removed LaTeX artifact: %s", artifact_path)
            except Exception as exc:
                logger.warning("Could not remove LaTeX artifact %s: %s", artifact_path, exc)


def compile_single_tex(tex_path: str):
    """Compile a single .tex file to PDF."""
    
    tex_file = Path(tex_path)
    
    if not tex_file.exists():
        logger.error("File not found: %s", tex_file)
        return False
    
    # Check if pdflatex is available
    pdflatex_path = shutil.which("pdflatex")
    if not pdflatex_path:
        logger.error("pdflatex not found. Please install MiKTeX.")
        return False
    
    # Get the directory containing the tex file
    tex_dir = tex_file.parent
    tex_name = tex_file.name
    
    logger.info("Using pdflatex: %s", pdflatex_path)
    logger.info("Compiling: %s", tex_name)
    logger.info("In directory: %s", tex_dir)
    
    # Make sure resume.cls is in the output directory
    cls_source = Path(TEMPLATE_DIR) / "resume.cls"
    if cls_source.exists():
        cls_dest = tex_dir / "resume.cls"
        if not cls_dest.exists():
            shutil.copy(cls_source, cls_dest)
            logger.info("Copied resume.cls to output directory")
    
    # Run pdflatex twice (for references) - exactly like manual
    try:
        for i in range(2):
            logger.info("Run %d/2", i + 1)
            # hide text output until error occurs, then show it
            result = subprocess.run(
                [pdflatex_path, tex_name],
                cwd=str(tex_dir),
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print("pdflatex failed:")
                print(result.stdout)
                print(result.stderr)
                raise subprocess.CalledProcessError(
                    result.returncode,
                    result.args,
                    output=result.stdout,
                    stderr=result.stderr,
                )
        
        # Check if PDF was created
        pdf_file = tex_dir / f"{tex_file.stem}.pdf"
        
        if pdf_file.exists():
            _cleanup_latex_artifacts(tex_dir, tex_file.stem)
            logger.info("PDF generated: %s", pdf_file)
            return str(pdf_file)
        else:
            logger.error("PDF not found at: %s", pdf_file)
            return False
            
    except Exception as e:
        logger.exception("Error: %s", e)
        return False


def main():
    """Main function."""
    output_dir = OUTPUT_DIR
    
    if not output_dir.exists():
        logger.error("Output directory not found: %s", output_dir)
        return
    
    # Find all generated tex files inside run directories
    tex_files = list(output_dir.glob("**/resume.tex"))
    
    if not tex_files:
        logger.error("No .tex files found in %s", output_dir)
        logger.info("Run main.py first to generate a .tex file")
        return
    
    # Show available files
    logger.info("Found %d .tex files", len(tex_files))
    for i, f in enumerate(tex_files, 1):
        # check if pdf exists, otherwise compile
        pdf_file = f.with_suffix(".pdf")
        if pdf_file.exists():
            continue  # Skip if PDF already exists
        file_time = f.stat().st_mtime
        time_str = datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
        logger.info("%d. %s (%s)", i, f.name, time_str)
        success = compile_single_tex(str(f))
        if success:
            logger.info("Compilation successful: %s", success)
        elif not pdf_file.exists():
            logger.error("Compilation failed for: %s", f.name)
            logger.info("Try manual compilation: cd %s", f.parent)
            logger.info("pdflatex %s", f.name)
            logger.info("pdflatex %s  # Run twice", f.name)


if __name__ == "__main__":
    main()