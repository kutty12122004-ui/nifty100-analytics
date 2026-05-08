import os
import pandas as pd

RAW_DIR = os.path.join('data', 'raw')


def find_excel_files(root_dir=RAW_DIR):
    """Yield all .xlsx files inside root_dir and its subfolders."""
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.xlsx'):
                yield os.path.join(dirpath, filename)


def build_output_name(input_path, root_dir=RAW_DIR, existing_names=None):
    """Create a unique CSV filename in the root raw directory."""
    if existing_names is None:
        existing_names = set()

    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_name = f'{base_name}.csv'

    if output_name in existing_names:
        rel_dir = os.path.relpath(os.path.dirname(input_path), root_dir)
        rel_dir = rel_dir.replace(os.sep, '_') if rel_dir != '.' else 'nested'
        output_name = f'{rel_dir}_{base_name}.csv'

    counter = 1
    while output_name in existing_names:
        output_name = f'{base_name}_{counter}.csv'
        counter += 1

    existing_names.add(output_name)
    return output_name


def extract_excel_to_csv():
    excel_paths = list(find_excel_files())
    if not excel_paths:
        print(f'No .xlsx files found under {RAW_DIR}')
        return

    existing_names = set()
    for excel_path in excel_paths:
        print(f'Reading {excel_path}...')
        try:
            df = pd.read_excel(excel_path)
        except Exception as exc:
            print(f'Failed to read {excel_path}: {exc}')
            continue

        output_filename = build_output_name(excel_path, existing_names=existing_names)
        output_path = os.path.join(RAW_DIR, output_filename)

        try:
            df.to_csv(output_path, index=False)
            print(f'Successfully converted {excel_path} to {output_path}')
        except Exception as exc:
            print(f'Failed to write CSV for {excel_path}: {exc}')


if __name__ == '__main__':
    extract_excel_to_csv()