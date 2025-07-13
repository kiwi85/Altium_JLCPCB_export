# Altium JLCPCB Export

This repository provides scripts to facilitate the export of PCB design files from Altium Designer for manufacturing with JLCPCB. The scripts automate the generation and formatting of required files, ensuring compatibility with JLCPCB's submission requirements.

## Features

- Automated export of Gerber files, BOM, and Pick & Place files from Altium projects.
- File renaming and formatting to match JLCPCB standards.
- Easy-to-use scripts for batch processing multiple projects.

## Scripts

### `export_gerber.py`
Exports Gerber files from Altium projects and organizes them into the required folder structure.

### `format_bom.py`
Processes the Bill of Materials (BOM) file, ensuring correct formatting and part numbering for JLCPCB assembly.

### `export_pick_place.py`
Generates and formats the Pick & Place file for SMT assembly, compatible with JLCPCB requirements.

### `batch_export.sh`
Shell script for batch processing multiple Altium projects, automating the export and formatting steps.

## Usage

1. Place your Altium project files in the designated input folder.
2. Run the provided scripts in sequence or use the batch script for automation.
3. Upload the generated files to JLCPCB for manufacturing.

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.