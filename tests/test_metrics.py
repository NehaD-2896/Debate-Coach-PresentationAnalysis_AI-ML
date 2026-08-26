from app.services.presentation_audio import compute_presentation_metrics


def test_wpm_and_fillers():
    result = compute_presentation_metrics("Um this is like a test", 6)
    assert result.words_per_minute == 60
    assert result.pace_status == "Too Slow"
    assert result.filler_word_count == 2
    assert result.filler_words["um"] == 1
    assert result.filler_words["like"] == 1


def test_typed_mode_does_not_fabricate_wpm():
    result = compute_presentation_metrics("This is typed", None)
    assert result.words_per_minute is None
    assert result.pace_status == "N/A (no duration)"
