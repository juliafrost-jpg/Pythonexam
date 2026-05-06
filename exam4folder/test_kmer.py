from kmer_analyzer 
import validate_sequence, update_kmer_count,count_kmers_with_context, write_results_to_file

def test_validate():
    """Checks the DNA sequence to see if it is valid for the k-mer analysis. 
    If true the sequence is long enough and contains no numbers, if it does 
    contains numbers then it returns as false, test failed"""
    assert validate_sequence("ACGTACGT", 4) == True   #valid sequence
    assert validate_sequence("ACG1ACGT", 4) == False  #digit found
    assert validate_sequence("AC", 4) == False         #too short
def test_update():
    """Test that k-mers and thier following characters are recorded correctly
    If they are then it passes, if not then fails"""
    data = update_kmer_count({}, "ACGT", "A")
    assert "ACGT" in data                        #kmer was recorded
    assert data["ACGT"]["next_chars"]["A"] == 1  #"A" followed it once
def test_count():
    """Test that all k-mers and following characters are extracted from a sequence
    if they are then passes, if not then fails"""
    result = count_kmers_with_context("ACGTACGT", 4)
    assert "ACGT" in result                          #kmer found
    assert result["ACGT"]["next_chars"]["A"] == 1    #followed by "A" once

def test_write(tmp_path):
    """Tests that k-mer results are written to file in the correct format if 
    files are written correctly then passes, if not then fails"""
    f = tmp_path / "out.txt"
    write_results_to_file({"ACGT": {"count": 2, "next_chars": {"A": 1}}}, str(f))
    assert "ACGT A:1" in f.read_text()               #correct output format
