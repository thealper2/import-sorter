# Import Sorter

Import Sorter is a sophisticated command-line tool designed to automatically organize and standardize import statements in Python projects. It provides flexible sorting strategies and helps maintain clean, consistent import structures across your codebase.

## :dart: Features

- **Multiple Import Sorting Strategies**:
 - from-first: Prioritize 'from' imports
 - import-first: Prioritize standard 'import' statements
 - alphabetical: Sort imports alphabetically
 - structural: Sort by library type (system, third-party, local)
- **Flexible Processing**:
 - Process single files
 - Process entire directories
 - Dry-run mode for previewing changes

## :hammer_and_wrench: Installation

1. Clone the repository:

```bash
git clone https://github.com/thealper2/import-sorter.git
cd import-sorter
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## :handshake: Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature (git checkout -b feature/your-feature)
3. Commit your changes (git commit -am 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Create a new Pull Request

## :scroll: License

This project is licensed under the MIT License - see the LICENSE file for details.