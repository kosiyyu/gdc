import os
import pytest
import subprocess

@pytest.fixture
def init_stage():
    """Fixture to set up the test environment."""

    if not os.path.exists("test_folder"):
        os.mkdir("test_folder")
    else:
        print("Directory should not exist")
        pytest.fail("Directory should not exist.")
    
    with open("test_folder/test_file.txt", "w") as file:
        pass
    
    yield None
    
    clean_stage()


def clean_stage() -> None:
    """Clean up the test folder and created ZIP file."""
    if os.path.exists("test_folder"):
        for item in os.listdir("test_folder"):
            item_path = os.path.join("test_folder", item)
            if os.path.isfile(item_path):
                os.remove(item_path)
        os.rmdir("test_folder")

    files = os.listdir()
    for item in files:
        if item.startswith("world") and item.endswith(".zip") and "44322739272" in item:
            os.remove(item)
            return


def correct_usage() -> bool:
    """Run the subprocess and check if the expected zip file is created."""
    result = subprocess.run(["python", "create_zip.py", "--id", "44322739272", "--path", "test_folder"])

    if result.returncode == 0:
        files = os.listdir()
        for item in files:
            if item.startswith("world") and item.endswith(".zip") and "44322739272" in item:
                return True
        
    return False

def incorrect_usage_1() -> bool:
    """Run with incorrect params."""
    result = subprocess.run(["python", "create_zip.py", "--path", "test_folder"])

    if result.returncode == 0:
        files = os.listdir()
        for item in files:
            if item.startswith("world") and item.endswith(".zip") and "44322739272" in item:
                return True
        
    return False

def incorrect_usage_2() -> bool:
    """Run with incorrect params."""
    result = subprocess.run(["python", "create_zip.py", "--id", "44322739272"])

    if result.returncode == 0:
        files = os.listdir()
        for item in files:
            if item.startswith("world") and item.endswith(".zip") and "44322739272" in item:
                return True
        
    return False

def test_correct_usage(init_stage):
    assert correct_usage()
 
def test_incorrect_usage_1(init_stage):
    assert not incorrect_usage_1()

def test_incorrect_usage_2(init_stage):
    assert not incorrect_usage_2()
