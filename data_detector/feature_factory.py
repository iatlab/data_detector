import re
from .spreadsheet import Spreadsheet

class FeatureFactory(object):
    FEW  = 0.25
    HALF = 0.50
    MOST = 0.75
    NUM = re.compile("\d")
    NUMVAL_PATTERN = "(-?\d[\d,]*(\.\d+)?)"
    NUMVAL = re.compile("^[^\d]?{}[^\d]?$".format(NUMVAL_PATTERN))
    # http://www.us-metric.org/commonly-used-metric-system-units-symbols-and-prefixes/
    UNIT_PATTERN = r"((%)|(mm)|(cm)|(m)|(km)|(mg)|(g)|(kg)|(t)|"\
                    "(°c)|(m²)|(ha)|(km²)|(ml)|(cm³)|(l)|(m³)|(n)|"\
                    "(s)|(h)|(sec)|(seconds)|(min)|(minutes)|(hours)|"\
                    "(kpa)|(w)|(kw)|(kj)|(kwh)|(a)|(j)|(hpa)|(pa))[23]?"
    UNIT = re.compile("^{0}{1}([·/]{1})?$".format(NUMVAL_PATTERN, UNIT_PATTERN))

    FEATURE_LIST = [
        # per cell
        "cell_numval_num",
        "cell_numval_frac",
        "cell_natural_num",
        "cell_natural_frac",
        "cell_uniq_numval_num",
        "cell_uniq_numval_frac",
        "cell_unit_num",
        "cell_unit_frac",
        # per char
        "char_num_num",
        "char_num_frac",
        "char_zero_num",
        "char_zero_frac",
        # per line
        "line_few_numerical_num",
        "line_few_numerical_frac",
        "line_half_numerical_num",
        "line_half_numerical_frac",
        "line_most_numerical_num",
        "line_most_numerical_frac",
        # per adj
        "uniq_adj_diff_num",
        "uniq_adj_diff_frac",
    ]

    @classmethod
    def extract_features(cls, spreadsheet):
        feature = {feature_name: None for feature_name in cls.FEATURE_LIST}
        ss = Spreadsheet.apply_all_cells(Spreadsheet.cell_normalization, spreadsheet)
        feature.update(cls.extract_independent_features(ss))
        feature.update(cls.extract_dependent_features(ss))

        assert(all([v is not None for v in feature.values()]))
        return feature

    @classmethod
    def extract_independent_features(cls, normalized_spreadsheet):
        # per cell
        cell_num = 0
        cell_numval_num = 0
        cell_natural_num = 0
        cell_numval_list = []
        cell_unit_num = 0

        # per char
        char_num = 0
        char_num_num = 0
        char_zero_num = 0

        for row in normalized_spreadsheet:
            for cell in row:
                if cell == "":
                    # exclude empty cells
                    continue
                cell_num += 1
                
                # per cell
                if cls.is_numval_with_unit(cell):
                    cell_unit_num += 1
                numval = cls.extract_numval(cell)
                if numval is not None:
                    cell_numval_num += 1
                    cell_numval_list.append(numval)
                    if cls.does_look_like_natural(numval):
                        cell_natural_num += 1
                
                # per char
                char_num += len(cell)
                char_num_num += len(cls.NUM.findall(cell))
                char_zero_num += cell.count("0")

        uniq_numval_num = len(set(cell_numval_list))

        feature = {}
        feature["cell_numval_num"]       = cell_numval_num
        feature["cell_numval_frac"]      = 0 if cell_num == 0\
                                           else cell_numval_num  / cell_num
        feature["cell_natural_num"]      = cell_natural_num
        feature["cell_natural_frac"]     = 0 if cell_num == 0\
                                           else cell_natural_num / cell_num
        feature["cell_uniq_numval_num"]  = uniq_numval_num
        feature["cell_uniq_numval_frac"] = 0 if cell_num == 0\
                                           else uniq_numval_num  / cell_num
        feature["cell_unit_num"]  =        cell_unit_num
        feature["cell_unit_frac"] =        0 if cell_num == 0\
                                           else cell_unit_num    / cell_num
        feature["char_num_num"]          = char_num_num
        feature["char_num_frac"]         = 0 if char_num == 0\
                                           else char_num_num     / char_num
        feature["char_zero_num"]         = char_zero_num
        feature["char_zero_frac"]        = 0 if char_num == 0\
                                           else char_zero_num    / char_num
        return feature

    @classmethod
    def extract_dependent_features(cls, normalized_spreadsheet):
        line_num = 0
        line_few_numerical_num = 0
        line_half_numerical_num = 0
        line_most_numerical_num = 0
        adj_diffs = []

        iters = [cls.iter, cls.transpose_iter]
        for it in iters:
            for line in it(normalized_spreadsheet):
                non_empty_cells = [cell for cell in line if len(cell) > 0]
                if len(non_empty_cells) == 0:
                    continue
                line_num += 1
                numvals = list(filter(lambda x: x is not None,
                                      map(cls.extract_numval, non_empty_cells)))
                numval_frac = len(numvals) / len(non_empty_cells)
                if numval_frac >= cls.FEW:
                    line_few_numerical_num += 1
                if numval_frac >= cls.HALF:
                    line_half_numerical_num += 1
                if numval_frac >= cls.MOST:
                    line_most_numerical_num += 1
                for i in range(len(numvals)-1):
                    adj = numvals[i:i+2]
                    diff = float(adj[1]) - float(adj[0])
                    adj_diffs.append(diff)

        uniq_adj_diff_num = len(set(adj_diffs))

        feature = {}
        feature["line_few_numerical_num"]   = line_few_numerical_num
        feature["line_few_numerical_frac"]  = 0 if line_num == 0\
                                              else line_few_numerical_num  / line_num
        feature["line_half_numerical_num"]  = line_half_numerical_num
        feature["line_half_numerical_frac"] = 0 if line_num == 0\
                                              else line_half_numerical_num / line_num
        feature["line_most_numerical_num"]  = line_most_numerical_num
        feature["line_most_numerical_frac"] = 0 if line_num == 0\
                                              else line_most_numerical_num / line_num
        feature["uniq_adj_diff_num"]        = uniq_adj_diff_num
        feature["uniq_adj_diff_frac"]       = 0 if len(adj_diffs) == 0\
                                              else uniq_adj_diff_num       / len(adj_diffs)
        return feature

    @classmethod
    def iter(cls, spreadsheet):
        for row in spreadsheet:
            yield row

    @classmethod
    def transpose_iter(cls, spreadsheet):
        col_idx = 0
        while True:
            col = []
            for row in spreadsheet:
                if col_idx < len(row):
                    col.append(row[col_idx])
                else:
                    col.append(None)
            if all([cell is None for cell in col]):
                break
            col = [cell if cell is not None else "" for cell in col]
            col_idx += 1
            yield col

    @classmethod
    def extract_numval(cls, normalized_cell):
        # e.g. -10.5
        # Allow one-char non-digit prefix and suffix:
        #   e.g. $ -10.5
        #   e.g. Disallow 111-222, AB4352, or 13:00
        match = cls.NUMVAL.match(normalized_cell)
        if match:
            match = match.group(1)
            match = match.replace(",", "")
            try:
                _ = float(match)
            except ValueError:
                match = None
        return match

    @classmethod
    def does_look_like_natural(cls, numval):
        return not "." in numval and not numval.startswith("-")

    @classmethod
    def is_numval_with_unit(cls, normalized_cell):
        match = cls.UNIT.match(normalized_cell.lower())
        return match is not None
