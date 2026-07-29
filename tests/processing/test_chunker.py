from src.models.paper import Page, Paper, PaperMetadata
from src.processing.chunker import flatten_paper


def make_paper(*texts: str) -> Paper:
    return Paper(
        filename="test",
        filepath="a/b/test.pdf",
        metadata=PaperMetadata(title="Test Paper", author="Test Author"),
        num_pages=len(texts),
        pages=[Page(page_number=i + 1, text=text) for i, text in enumerate(texts)],
    )


def test_flatten_single_page():
    paper = make_paper("Hello World")
    text, index = flatten_paper(paper)

    assert text == "Hello World"
    assert index[0].page_number == 1
    assert index[0].global_start_idx == 0
    assert index[0].global_end_idx == 11


def test_flatten_multiple_pages():
    paper = make_paper("ABC", "DEFG", "HI")
    text, indices = flatten_paper(paper)

    assert text == "ABCDEFGHI"
    assert len(indices) == 3
    assert indices[0].page_number == 1
    assert indices[0].global_start_idx == 0
    assert indices[0].global_end_idx == 3

    assert indices[1].page_number == 2
    assert indices[1].global_start_idx == 3
    assert indices[1].global_end_idx == 7

    assert indices[2].page_number == 3
    assert indices[2].global_start_idx == 7
    assert indices[2].global_end_idx == 9


def test_flatten_empty_page():
    paper = make_paper("")
    text, index = flatten_paper(paper)

    assert text == ""
    assert len(index) == 1

    assert index[0].page_number == 1
    assert index[0].global_start_idx == 0
    assert index[0].global_end_idx == 0


def test_flatten_empty_paper():
    paper = make_paper()
    text, index = flatten_paper(paper)

    assert text == ""
    assert index == []


def test_flatten_preserves_empty_pages():
    paper = make_paper("ABC", "", "DEF")

    text, indices = flatten_paper(paper)

    assert text == "ABCDEF"
    assert len(indices) == 3

    assert indices[0].page_number == 1
    assert indices[0].global_start_idx == 0
    assert indices[0].global_end_idx == 3

    assert indices[1].page_number == 2
    assert indices[1].global_start_idx == 3
    assert indices[1].global_end_idx == 3

    assert indices[2].page_number == 3
    assert indices[2].global_start_idx == 3
    assert indices[2].global_end_idx == 6


def test_flatten_preserves_page_numbers():
    paper = make_paper("ABC", "DEF")
    paper.pages[0].page_number = 5
    paper.pages[1].page_number = 8

    text, indices = flatten_paper(paper)
    assert text == "ABCDEF"
    assert indices[0].page_number == 5
    assert indices[1].page_number == 8


def test_flatten_does_not_modify_paper():
    paper = make_paper("ABC", "DEF")
    original = [page.text for page in paper.pages]
    flatten_paper(paper)
    assert [page.text for page in paper.pages] == original


def test_flatten_unicode():
    paper = make_paper(
        "αβγ",
        "ΔΣΩ",
    )
    text, index = flatten_paper(paper)

    assert text == "αβγΔΣΩ"

    assert index[0].global_end_idx == 3
    assert index[1].global_start_idx == 3


def test_flatten_large_pages():

    p1 = "A" * 1000
    p2 = "B" * 500

    paper = make_paper(p1, p2)

    text, index = flatten_paper(paper)

    assert len(text) == 1500

    assert index[0].global_end_idx == 1000
    assert index[1].global_start_idx == 1000
    assert index[1].global_end_idx == 1500
