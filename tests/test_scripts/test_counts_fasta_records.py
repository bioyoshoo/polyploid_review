import os
from subprocess import run, PIPE
import re


DIR = "./scripts/utils"
os.chdir(DIR)


def adjust_format(string: str) -> str:
    out = re.sub(r"\n$", "", string)
    out = re.sub(r'\s+', '\t', out)
    return out


def test_fasta_input():
    in_path = "../../tests/test_data/count_fasta_records/in/in_1.fasta"
    out_path = "../../tests/test_data/count_fasta_records/out/out_1.txt"

    result = run(["python", "count_fasta_records.py", 
                  "--fasta", in_path], 
                  capture_output=True, text=True)
    out = adjust_format(result.stdout)
    
    with open(out_path, "r") as f:
        expected = f.read()
        expected = adjust_format(expected)

    assert out == expected


def test_stdin_input():
    in_path = "../../tests/test_data/count_fasta_records/in/in_1.fasta"
    out_path = "../../tests/test_data/count_fasta_records/out/out_1.txt"
    
    cat = run(["cat", in_path], text=True, stdout=PIPE)
    result = run(["python", "count_fasta_records.py", 
                  "--fasta", "-"], 
                  capture_output=True, text=True, input=cat.stdout)
    out = adjust_format(result.stdout)
    
    with open(out_path, "r") as f:
        expected = f.read()
        expected = adjust_format(expected)
    
    assert out == expected


def test_bz2_input():
    in_path = "../../tests/test_data/count_fasta_records/in/in_2.fasta.bz2"
    out_path = "../../tests/test_data/count_fasta_records/out/out_2.txt"

    bzip = run(["bzip2", "-d", "-c", in_path],
               text=True, stdout=PIPE)
    result = run(["python", "count_fasta_records.py", 
                  "--fasta", "-"], 
                  capture_output=True, text=True, input=bzip.stdout)
    out = adjust_format(result.stdout)

    with open(out_path, "r") as f:
        expected = f.read()
        expected = adjust_format(expected)

    assert out == expected
    

    

