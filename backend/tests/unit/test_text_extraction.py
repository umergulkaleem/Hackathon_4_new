import unittest
import tempfile
import os
from src.services.text_extraction import TextExtractionService
from src.models.markdown_content import MarkdownContent

class TestTextExtractionService(unittest.TestCase):
    """
    Unit tests for TextExtractionService
    """

    def setUp(self):
        """Set up test fixtures"""
        self.service = TextExtractionService()

    def test_extract_from_file(self):
        """Test extracting content from a markdown file"""
        # Create a temporary markdown file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Title\n\nThis is test content.\n\n## Subsection\n\nMore content here.")
            temp_file_path = f.name

        try:
            # Extract content
            content = self.service.extract_from_file(temp_file_path)

            # Verify the extracted content
            self.assertIsInstance(content, MarkdownContent)
            self.assertEqual(content.title, "Test Title")
            self.assertIn("# Test Title", content.content)
            self.assertIn("This is test content.", content.content)
            self.assertGreater(len(content.headers), 0)
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_extract_title(self):
        """Test title extraction from markdown content"""
        content = "# Main Title\n\nSome content here\n\n## Subtitle\n\nMore content"
        title = self.service._extract_title(content)
        self.assertEqual(title, "Main Title")

    def test_extract_headers(self):
        """Test header extraction from markdown content"""
        content = "# Header 1\n\nContent\n\n## Header 2\n\nMore content\n\n### Header 3\n\nEven more"
        headers = self.service._extract_headers(content)

        self.assertIn("# Header 1", headers)
        self.assertIn("## Header 2", headers)
        self.assertIn("### Header 3", headers)
        self.assertEqual(len(headers), 3)


if __name__ == '__main__':
    unittest.main()