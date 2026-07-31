from viscomm import CATEGORICAL, contrast_ink


def test_categorical_palette_has_eight_distinct_hues():
    assert len(CATEGORICAL) == 8
    assert len(set(CATEGORICAL)) == 8


def test_contrast_ink_picks_dark_on_light_and_white_on_dark():
    assert contrast_ink("#fcfcfb") == "#0b0b0b"
    assert contrast_ink("#0b0b0b") == "#ffffff"
