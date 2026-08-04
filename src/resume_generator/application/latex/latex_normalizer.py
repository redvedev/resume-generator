import re


class LatexNormalizer:
    def __init__(self) -> None:
        pass

    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        if not text:
            return ""

        # Don't escape LaTeX commands
        if text.startswith("\\"):
            return text

        replacements = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }

        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        return text

    def normalize_text(self, text: str) -> str:
        """Normalize text for LaTeX and ATS extraction."""
        if not text:
            return ""

        text = text.replace("–", "--")
        text = text.replace("—", "---")
        text = re.sub(r"\s*--\s*", " -- ", text)
        return text

    def escape_and_normalize(self, text: str) -> str:
        """Normalize unicode punctuation before LaTeX escaping."""
        return self.escape_latex(self.normalize_text(text))

    def normalize_website(self, website: str) -> str:
        website = (website or "").strip()
        if website.startswith("https://"):
            return website[len("https://") :]
        if website.startswith("http://"):
            return website[len("http://") :]
        return website

    def format_header_dates(self, dates: str) -> str:
        """Wrap header dates so PDF text extraction keeps them separated."""
        return f"\\mbox{{~{dates}~}}"
