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
    def parse(cls, filepath):
        """
        Read `filepath` and return a list of Spreadsheet
        """
        ext = os.path.splitext(filepath)[1]
        if ext == ".csv":
            return cls.parse_csv(filepath)
        else:
            # use xlrd if the extension is not 'csv'
            return cls.parse_xl(filepath)

    @classmethod
    def parse_csv(cls, filepath):
        """
        Use csv module
        """
        cells = []
        with open(filepath) as f:
            rows = csv.reader(f)
            for row in rows:
                cells.append(row)
        return [Spreadsheet(cells)]

    @classmethod
    def parse_xl(cls, filepath):
        """
        Use xlrd module
        """
        wb = xlrd.open_workbook(filepath)
        spreadsheets = []
        for sheet in wb.sheets():
            cells = []
            for row in sheet.get_rows():
                vals = [cell.value for cell in row]
                cells.append(vals)
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
