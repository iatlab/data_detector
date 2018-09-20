import os
import csv
import re
import json
import xlrd
import mojimoji

class Spreadsheet(list):
    HYPHEN = re.compile("[—ー−ｰ]")
    WHITESPACE = re.compile("\s")

    def __init__(self, cells):
        super().__init__(cells)
    
    @classmethod
    def parse(cls, filepath, truncate_rows=None):
        """
        Read `filepath` and return a list of Spreadsheet
        """
        ext = os.path.splitext(filepath)[1]
        if ext == ".csv":
            return cls.parse_csv(filepath, truncate_rows)
        else:
            # use xlrd if the extension is not 'csv'
            return cls.parse_xl(filepath, truncate_rows)

    @classmethod
    def parse_csv(cls, filepath_or_fileobj, truncate_rows=None):
        """
        Use csv module
        """
        if isinstance(filepath_or_fileobj, str):
            with open(filepath_or_fileobj) as stream:
                return cls._parse_csv_stream(stream, truncate_rows)
        elif hasattr(filepath_or_fileobj, 'read'):
            return cls._parse_csv_stream(filepath_or_fileobj, truncate_rows)
        else:
            raise ValueError("The argument must be a filepath or fileobj with `read` function")

    @classmethod
    def _parse_csv_stream(cls, stream, truncate_rows):
        cells = []
        rows = csv.reader(stream)
        for row in rows:
            cells.append(row)
            if truncate_rows and len(cells) >= truncate_rows:
                break
        return [Spreadsheet(cells)]

    @classmethod
    def parse_xl(cls, filepath_or_fileobj, truncate_rows=None):
        """
        Use xlrd module
        """
        if isinstance(filepath_or_fileobj, str):
            wb = xlrd.open_workbook(filepath_or_fileobj, ragged_rows=True)
        elif hasattr(filepath_or_fileobj, 'read'):
            wb = xlrd.open_workbook(file_contents=filepath_or_fileobj.read(), ragged_rows=True)
        else:
            raise ValueError("The argument must be a filepath or fileobj with `read` function")
        return cls._parse_workbook(wb, truncate_rows)

    @classmethod
    def _parse_workbook(cls, workbook, truncate_rows):
        spreadsheets = []
        for sheet in workbook.sheets():
            cells = []
            for row in sheet.get_rows():
                vals = [cell.value for cell in row]
                cells.append(vals)
                if truncate_rows and len(cells) >= truncate_rows:
                    break
            spreadsheets.append(Spreadsheet(cells))
        return spreadsheets

    @classmethod
    def apply_all_cells(cls, func, spreadsheet):
        new_spreadsheet = []
        for row in spreadsheet:
            new_row = list(map(func, row))
            new_spreadsheet.append(new_row)
        return new_spreadsheet

    @classmethod
    def cell_normalization(cls, cell):
        cell = cell if isinstance(cell, str) else str(cell)
        # Zenkaku -> Hankaku
        cell = mojimoji.zen_to_han(cell, kana=False)
        # Normalize hyphen
        cell = cls.HYPHEN.sub("-", cell)
        # Remove whitespaces 
        cell = cls.WHITESPACE.sub("", cell)
        # Blank cell should be blank
        if cell == '-':
            cell = ""
        return cell
