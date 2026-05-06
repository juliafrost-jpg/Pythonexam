from kmer_analyzer import validate_sequence, update_kmer_count, count_kmers_with_context, write_results_to_file

def test_validate():
    """Checks the DNA sequence is valid for k-mer analysis."""
    assert validate_sequence("ACGTACGT", 4) == True
    assert validate_sequence("ACG1ACGT", 4) == False
    assert validate_sequence("AC", 4) == False

def test_update():
    """Tests k-mers and following characters are recorded correctly."""
    data = update_kmer_count({}, "ACGT", "A")
    assert "ACGT" in data
    assert data["ACGT"]["next_chars"]["A"] == 1

def test_update_count_is_correct():
    """Count should be 1 after seeing a k-mer once - FAILS due to bug."""
    data = update_kmer_count({}, "ACGT", "A")
    assert data["ACGT"]["count"] == 1

def test_count():
    """Tests k-mers and following characters are extracted from a sequence."""
    result = count_kmers_with_context("ACGTACGT", 4)
    assert "ACGT" in result
    assert result["ACGT"]["next_chars"]["A"] == 1

def test_write(tmp_path):
    """Tests k-mer results are written to file in correct format."""
    f = tmp_path / "out.txt"
    write_results_to_file({"ACGT": {"count": 2, "next_chars": {"A": 1}}}, str(f))
    assert "ACGT A:1" in f.read_text()

def test_main_multiple_sequences(tmp_path):
    """All sequences should appear in output - FAILS due to bug."""
    import sys
    input_file = tmp_path / "input.txt"
    input_file.write_text("ACGTACGT
TTTTGGGG
")
    output_file = tmp_path / "output.txt"
    sys.argv = ["kmer_analyzer.py", str(input_file), "4", str(output_file)]
    from kmer_analyzer import main
    main()
    content = output_file.read_text()
    assert "ACGT" in content
    assert "TTTT" in content
