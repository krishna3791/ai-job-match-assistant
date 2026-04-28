from app.resume_documents import extract_text_from_upload


def test_extract_text_from_txt_upload() -> None:
    text = extract_text_from_upload("resume.txt", b"Python SQL Spark")

    assert text == "Python SQL Spark"


def test_extract_text_rejects_unsupported_format() -> None:
    try:
        extract_text_from_upload("resume.png", b"nope")
    except ValueError as exc:
        assert "Supported resume formats" in str(exc)
    else:
        raise AssertionError("Expected unsupported format error.")
