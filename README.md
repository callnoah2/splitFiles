# splitFiles

## Overview

This Python script allows you to split a large zip file into smaller parts based on a specified maximum size. It preserves the original compression and creates new zip files with the split content.

## Usage

python fileSplitter.py <input_zip_file> [max_size_in_MB]

- <input_zip_file>: The path to the input zip file you want to split.
- [max_size_in_MB] (optional): The maximum size for each split part in megabytes. If not provided, the default is set to 50 MB.
