from app import answer_question, load_chunks


def test_sample_question_returns_document_source():
    result = answer_question("What is the recommended coolant concentration for the TX-200 CNC turning centre?")
    assert "6-8 percent" in result["answer"]
    assert result["source"] == "03_tx200_maintenance.txt"


def test_alarm_question_returns_action():
    result = answer_question("The machine is showing alarm AL-104. What should the operator do?")
    assert "ISO VG 68" in result["answer"]
    assert "press RESET" in result["answer"]


def test_unknown_question_is_explicitly_not_found():
    result = answer_question("What is the cafeteria menu on Friday?")
    assert result["source"] is None
    assert "couldn't find" in result["answer"]


def test_outer_diameter_tolerance_is_retrieved():
    result = answer_question("What is the outer diameter tolerance for the BH-220 bearing housing?")
    assert "+/- 0.050" in result["answer"]


def test_documents_load():
    assert len(load_chunks()) >= 10
