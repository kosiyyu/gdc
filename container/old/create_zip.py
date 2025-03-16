import argparse
import shutil as sh
import datetime as dt

def create_zip(user_id: str, dir_path: str) -> None:
    date_string = str(dt.datetime.now().timestamp()).replace(".", "")
    filename = f"world_{user_id}_{date_string}"
    sh.make_archive(base_name=filename, format='zip', root_dir=".", base_dir=dir_path)

def main():
    try:
        parser = argparse.ArgumentParser("creates a ZIP archive of a directory, naming it with your user identifier and current timestamp")

        parser.add_argument('--id', type=str, required=True, help='user identifier of container rental')
        parser.add_argument('--path', type=str, required=True, help='directory path to be zipped')

        args = parser.parse_args()

        create_zip(args.id, args.path)
        exit(0)
    except Exception as e:
        print(e)
        exit(1)

if __name__ == "__main__":
    main()

# Usage exampe python create_zip.py --id "44322739272" --path "test_folder"