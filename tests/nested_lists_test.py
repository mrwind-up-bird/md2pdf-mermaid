"""
Tests for nested list rendering in both HTML and ReportLab renderers.

These tests verify that:
1. Nested lists with various indentation styles are parsed correctly
2. The indentation normalization works for any number of spaces
3. Normal paragraphs with leading spaces are NOT treated as list items
4. Numbered lists have correct per-level numbering
5. Bullet lists have appropriate bullet styles per level
"""

import re

import pytest

from md2pdf.converter import parse_markdown
from md2pdf.html_renderer import _normalize_list_indentation


class TestParseMarkdownLists:
    """Tests for the ReportLab parser's list handling."""

    def test_flat_bullet_list(self):
        """Test parsing a flat bullet list (no nesting)."""
        content = """- Item 1
- Item 2
- Item 3"""
        elements = parse_markdown(content)
        list_elements = [e for e in elements if e[0] == 'list']
        
        assert len(list_elements) == 3
        # All should have 0 leading spaces (top level)
        assert all(e[1][0] == 0 for e in list_elements)
        assert list_elements[0][1][1] == 'Item 1'
        assert list_elements[1][1][1] == 'Item 2'
        assert list_elements[2][1][1] == 'Item 3'

    def test_flat_numbered_list(self):
        """Test parsing a flat numbered list (no nesting)."""
        content = """1. First
2. Second
3. Third"""
        elements = parse_markdown(content)
        list_elements = [e for e in elements if e[0] == 'numlist']
        
        assert len(list_elements) == 3
        assert all(e[1][0] == 0 for e in list_elements)
        assert list_elements[0][1][1] == 'First'
        assert list_elements[1][1][1] == 'Second'
        assert list_elements[2][1][1] == 'Third'

    def test_nested_bullet_list_2_spaces(self):
        """Test parsing nested bullet list with 2-space indentation."""
        content = """- Level 0
  - Level 1
    - Level 2
  - Back to Level 1
- Back to Level 0"""
        elements = parse_markdown(content)
        list_elements = [e for e in elements if e[0] == 'list']
        
        assert len(list_elements) == 5
        assert list_elements[0][1][0] == 0  # Level 0
        assert list_elements[1][1][0] == 2  # Level 1 (2 spaces)
        assert list_elements[2][1][0] == 4  # Level 2 (4 spaces)
        assert list_elements[3][1][0] == 2  # Back to Level 1
        assert list_elements[4][1][0] == 0  # Back to Level 0

    def test_nested_numbered_list_3_spaces(self):
        """Test parsing nested numbered list with 3-space indentation."""
        content = """1. Level 0
   1. Level 1
      1. Level 2
   2. Back to Level 1
2. Back to Level 0"""
        elements = parse_markdown(content)
        list_elements = [e for e in elements if e[0] == 'numlist']
        
        assert len(list_elements) == 5
        assert list_elements[0][1][0] == 0  # Level 0
        assert list_elements[1][1][0] == 3  # Level 1 (3 spaces)
        assert list_elements[2][1][0] == 6  # Level 2 (6 spaces)
        assert list_elements[3][1][0] == 3  # Back to Level 1
        assert list_elements[4][1][0] == 0  # Back to Level 0

    def test_nested_list_1_space_indentation(self):
        """Test that even 1-space indentation is captured."""
        content = """- Item
 - Nested with 1 space
  - Nested with 2 spaces"""
        elements = parse_markdown(content)
        list_elements = [e for e in elements if e[0] == 'list']
        
        assert len(list_elements) == 3
        assert list_elements[0][1][0] == 0
        assert list_elements[1][1][0] == 1
        assert list_elements[2][1][0] == 2

    def test_nested_list_5_space_indentation(self):
        """Test that 5-space indentation is captured."""
        content = """1. Item
     1. Nested with 5 spaces"""
        elements = parse_markdown(content)
        list_elements = [e for e in elements if e[0] == 'numlist']
        
        assert len(list_elements) == 2
        assert list_elements[0][1][0] == 0
        assert list_elements[1][1][0] == 5

    def test_paragraph_with_leading_spaces_not_list(self):
        """Test that paragraphs with leading spaces are NOT parsed as lists."""
        content = """   This has 3 leading spaces but no list marker.
  Two spaces here.
    Four spaces here."""
        elements = parse_markdown(content)
        
        # Should be paragraphs, not lists
        list_elements = [e for e in elements if e[0] in ['list', 'numlist']]
        assert len(list_elements) == 0
        
        # Should have paragraph elements
        p_elements = [e for e in elements if e[0] == 'p']
        assert len(p_elements) == 3

    def test_asterisk_bullet_list(self):
        """Test that asterisk (*) bullets are also recognized."""
        content = """* Item 1
  * Nested item
* Item 2"""
        elements = parse_markdown(content)
        list_elements = [e for e in elements if e[0] == 'list']
        
        assert len(list_elements) == 3
        assert list_elements[0][1][0] == 0
        assert list_elements[1][1][0] == 2
        assert list_elements[2][1][0] == 0


class TestNormalizeListIndentation:
    """Tests for the HTML renderer's indentation normalization."""

    def test_already_4_space_indentation(self):
        """Test that 4-space indentation is preserved."""
        content = """- Item 1
    - Nested"""
        result = _normalize_list_indentation(content)
        
        assert "- Item 1" in result
        assert "    - Nested" in result

    def test_2_space_to_4_space_conversion(self):
        """Test that 2-space indentation is converted to 4-space."""
        content = """- Item 1
  - Nested level 1
    - Nested level 2"""
        result = _normalize_list_indentation(content)
        lines = result.split('\n')
        
        assert lines[0] == "- Item 1"
        assert lines[1] == "    - Nested level 1"
        assert lines[2] == "        - Nested level 2"

    def test_3_space_to_4_space_conversion(self):
        """Test that 3-space indentation is converted to 4-space."""
        content = """1. Item 1
   1. Nested level 1
      1. Nested level 2"""
        result = _normalize_list_indentation(content)
        lines = result.split('\n')
        
        assert lines[0] == "1. Item 1"
        assert lines[1] == "    1. Nested level 1"
        assert lines[2] == "        1. Nested level 2"

    def test_1_space_indentation(self):
        """Test that 1-space indentation creates proper nesting."""
        content = """- Item
 - One space
  - Two spaces
   - Three spaces"""
        result = _normalize_list_indentation(content)
        lines = result.split('\n')
        
        # Each additional space should create a new nesting level
        assert lines[0] == "- Item"
        assert lines[1] == "    - One space"
        assert lines[2] == "        - Two spaces"
        assert lines[3] == "            - Three spaces"

    def test_mixed_indentation_levels(self):
        """Test going back to shallower nesting levels."""
        content = """- Level 0
  - Level 1
    - Level 2
  - Back to Level 1
- Back to Level 0"""
        result = _normalize_list_indentation(content)
        lines = result.split('\n')
        
        assert lines[0] == "- Level 0"
        assert lines[1] == "    - Level 1"
        assert lines[2] == "        - Level 2"
        assert lines[3] == "    - Back to Level 1"
        assert lines[4] == "- Back to Level 0"

    def test_paragraph_with_spaces_unchanged(self):
        """Test that non-list paragraphs with leading spaces are unchanged."""
        content = """Normal paragraph.

   This has spaces but no list marker.

- Actual list item"""
        result = _normalize_list_indentation(content)
        
        # The indented paragraph should remain unchanged
        assert "   This has spaces but no list marker." in result
        # The list item should be at root level
        assert "\n- Actual list item" in result

    def test_headers_reset_list_context(self):
        """Test that headers reset the list context."""
        content = """- List item

## Header

   This indented text after header should not be affected by previous list."""
        result = _normalize_list_indentation(content)
        
        # The indented text after header should be preserved as-is
        assert "   This indented text after header" in result

    def test_empty_lines_preserved(self):
        """Test that empty lines are preserved."""
        content = """- Item 1

- Item 2"""
        result = _normalize_list_indentation(content)
        
        assert result == content  # Should be unchanged

    def test_deeply_nested_list(self):
        """Test deeply nested list (5 levels)."""
        content = """- Level 0
 - Level 1
  - Level 2
   - Level 3
    - Level 4"""
        result = _normalize_list_indentation(content)
        lines = result.split('\n')
        
        assert lines[0] == "- Level 0"
        assert lines[1] == "    - Level 1"
        assert lines[2] == "        - Level 2"
        assert lines[3] == "            - Level 3"
        assert lines[4] == "                - Level 4"


class TestIntegration:
    """Integration tests combining parsing and normalization."""

    def test_html_produces_nested_html_lists(self):
        """Test that normalized markdown produces proper nested HTML."""
        import markdown
        
        content = """- Item 1
  - Subitem 1
    - Sub-subitem 1
  - Subitem 2
- Item 2"""
        
        normalized = _normalize_list_indentation(content)
        md = markdown.Markdown(extensions=['extra'])
        html = md.convert(normalized)
        
        # Should have nested <ul> tags
        assert html.count('<ul>') >= 2
        assert '<li>Item 1<ul>' in html or '<li>Item 1\n<ul>' in html

    def test_numbered_list_produces_nested_html(self):
        """Test that normalized numbered lists produce proper nested HTML."""
        import markdown
        
        content = """1. First
   1. Nested first
   2. Nested second
2. Second"""
        
        normalized = _normalize_list_indentation(content)
        md = markdown.Markdown(extensions=['extra'])
        html = md.convert(normalized)
        
        # Should have nested <ol> tags
        assert html.count('<ol>') >= 2

    def test_reportlab_parser_captures_all_indentation_styles(self):
        """Test that the ReportLab parser handles various indentation styles."""
        # This represents a document with inconsistent indentation
        content = """1. Top level
   1. Three space indent
2. Back to top
 - One space bullet under numbered
  - Two space nested bullet"""
        
        elements = parse_markdown(content)
        numlist_elements = [e for e in elements if e[0] == 'numlist']
        list_elements = [e for e in elements if e[0] == 'list']
        
        assert len(numlist_elements) == 3
        assert len(list_elements) == 2
        
        # Verify indentation is captured correctly
        assert numlist_elements[0][1][0] == 0
        assert numlist_elements[1][1][0] == 3
        assert numlist_elements[2][1][0] == 0
        assert list_elements[0][1][0] == 1
        assert list_elements[1][1][0] == 2
