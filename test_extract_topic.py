"""
Unit tests for extract_topic() and _strip_lecture_suffix().

Run:  python test_extract_topic.py
"""
import re
import sys
import unittest

# ── inline copy of the two functions so tests run standalone ─────────────────

def _strip_lecture_suffix(text: str) -> str:
    cleaned = re.sub(
        r'\s*[-–]?\s*(?:lec(?:ture)?|class)\s*[-–]?\s*\d+\s*$',
        '',
        text,
        flags=re.IGNORECASE
    ).strip()
    return cleaned if cleaned else text


def extract_topic(original_title: str) -> str:
    title = original_title.strip()

    bracket_match = re.match(r'^[\[\(]([^\]\)]+)[\]\)]', title)
    if bracket_match:
        bracket_content = bracket_match.group(1).strip()
        if bracket_content.lower().startswith('by '):
            parts = re.split(r'\|', title, maxsplit=1)
            if len(parts) > 1:
                rest = parts[1].strip()
                rest = re.split(r'\|\|', rest)[0].strip()
                rest = re.sub(r'\s*Lecture\s*\d+.*', '', rest, flags=re.IGNORECASE).strip()
                rest = re.sub(r'^Class\s*[-–]?\s*\d+\s*\|?\s*', '', rest, flags=re.IGNORECASE).strip()
                rest = re.sub(r'\s*by\s+.*', '', rest, flags=re.IGNORECASE).strip()
                rest = _strip_lecture_suffix(rest)
                return rest if rest else bracket_content
            return bracket_content
        else:
            return bracket_content

    if '||' in title:
        after_double_pipe = title.split('||', 1)[1].strip()
        topic = re.sub(r'\s*by\s+.*', '', after_double_pipe, flags=re.IGNORECASE).strip()
        topic = re.sub(r'^Maths\s*$', '', topic, flags=re.IGNORECASE).strip()
        topic = _strip_lecture_suffix(topic)
        if topic:
            return topic

    snake_match = re.match(r'^(.+?)_[Cc]lass[-_]?\d*', title)
    if snake_match:
        return snake_match.group(1).replace('_', ' ').strip()

    fallback = re.split(r'[:|]', title)[0].strip()
    fallback = _strip_lecture_suffix(fallback)
    return fallback if fallback else title


# ── tests ────────────────────────────────────────────────────────────────────

class TestStripLectureSuffix(unittest.TestCase):
    def test_lec_space_hyphen_n(self):
        self.assertEqual(_strip_lecture_suffix("English Pronoun lec -1"), "English Pronoun")

    def test_lec_hyphen_n(self):
        self.assertEqual(_strip_lecture_suffix("English Pronoun lec-2"), "English Pronoun")

    def test_class_space_hyphen_n(self):
        self.assertEqual(_strip_lecture_suffix("English Pronoun class -1"), "English Pronoun")

    def test_class_hyphen_n(self):
        self.assertEqual(_strip_lecture_suffix("English Pronoun class-8"), "English Pronoun")

    def test_lecture_full_word(self):
        self.assertEqual(_strip_lecture_suffix("Maths Lecture 3"), "Maths")

    def test_no_suffix(self):
        self.assertEqual(_strip_lecture_suffix("Percentage"), "Percentage")

    def test_no_suffix_unchanged(self):
        self.assertEqual(_strip_lecture_suffix("English Pronoun"), "English Pronoun")


class TestExtractTopicLecSuffix(unittest.TestCase):
    """
    Core issue: titles from 'by Teacher' bracket format that contain
    'English Pronoun lec -N' should return 'English Pronoun'.
    """

    def test_pronoun_lec1(self):
        title = "[by Aman Sir] Class -8 | English Pronoun lec -1 || by Aman Sir"
        self.assertEqual(extract_topic(title), "English Pronoun")

    def test_pronoun_lec2(self):
        title = "[by Aman Sir] Class -9 | English Pronoun lec -2 || by Aman Sir"
        self.assertEqual(extract_topic(title), "English Pronoun")

    def test_pronoun_class1(self):
        title = "[by Aman Sir] Class -8 | English Pronoun class -1 || by Aman Sir"
        self.assertEqual(extract_topic(title), "English Pronoun")

    def test_pronoun_class_no_space(self):
        title = "[by Aman Sir] Class -8 | English Pronoun class-1 || by Aman Sir"
        self.assertEqual(extract_topic(title), "English Pronoun")


class TestExtractTopicExistingBehaviour(unittest.TestCase):
    """
    Make sure existing valid topics are NOT broken.
    """

    def test_bracket_topic(self):
        # [Arithmetic] Class-03 | Percentage  → Arithmetic
        self.assertEqual(extract_topic("[Arithmetic] Class-03 | Percentage"), "Arithmetic")

    def test_by_teacher_simple(self):
        # [by Aman Sir] Class -3 | English Basics || by Aman Sir  → English Basics
        self.assertEqual(
            extract_topic("[by Aman Sir] Class -3 | English Basics || by Aman Sir"),
            "English Basics"
        )

    def test_double_pipe_format(self):
        # Class - 03 || Percentage by Gagan sir  → Percentage
        self.assertEqual(
            extract_topic("Class - 03 || Percentage by Gagan sir"),
            "Percentage"
        )

    def test_snake_case(self):
        # Profit_Loss_Class_3  → Profit Loss
        self.assertEqual(extract_topic("Profit_Loss_Class_3"), "Profit Loss")

    def test_plain_subject(self):
        # No pattern → fallback to first segment
        self.assertEqual(extract_topic("Percentage"), "Percentage")


if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestStripLectureSuffix))
    suite.addTests(loader.loadTestsFromTestCase(TestExtractTopicLecSuffix))
    suite.addTests(loader.loadTestsFromTestCase(TestExtractTopicExistingBehaviour))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
