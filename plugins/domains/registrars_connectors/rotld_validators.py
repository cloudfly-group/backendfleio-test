from datetime import datetime
from fleio.core.drf import validate_vat_id
from django.utils.translation import ugettext_lazy as _


class RotldValidators:
    @staticmethod
    def is_int_representable(s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_com_reg_no(reg_no: str) -> (bool, str):
        """Validate the company's Registry of Commerce number"""
        if ' ' in reg_no:
            reg_no = reg_no.replace(' ', '')
        reg_groups = reg_no.split('/')
        msg = _('Invalid registry of commerce number')
        if len(reg_groups) != 3:
            return False, msg
        first_group = reg_groups[0]
        if 'J' in first_group or 'F' in first_group or 'C' in first_group or '-' in first_group:
            first_group = first_group[1:]

        if (not RotldValidators.is_int_representable(first_group) or
                not RotldValidators.is_int_representable(reg_groups[1]) or
                not RotldValidators.is_int_representable(reg_groups[2])):
            return False, msg

        if not 0 < int(first_group) <= 52:
            return False, msg

        if not 0 < int(reg_groups[1]) < 999999999:
            return False, msg

        if not 1990 <= int(reg_groups[2]) <= datetime.now().year:
            return False, msg
        return True, reg_no

    @staticmethod
    def is_valid_fiscal_code(code: str) -> bool:
        """validates the ro fiscal code"""
        if ' ' in code:
            code = code.replace(' ', '')
        result, message = validate_vat_id(vat_id=code, country_code=code[:2])
        return result


class CNP:
    CITIES = {
        1: "Alba",
        2: "Arad",
        3: "Arges",
        4: "Bacau",
        5: "Bihor",
        6: "Bistrita-Nasaud",
        7: "Botosani",
        8: "Brasov",
        9: "Braila",
        10: "Buzau",
        11: "Caras-Severin",
        12: "Cluj",
        13: "Constanta",
        14: "Covasna",
        15: "Dambovita",
        16: "Dolj",
        17: "Galati",
        18: "Gorj",
        19: "Harghita",
        20: "Hunedoara",
        21: "Ialomita",
        22: "Iasi",
        23: "Ilfov",
        24: "Maramures",
        25: "Mehedinti",
        26: "Mures",
        27: "Neamt",
        28: "Olt",
        29: "Prahova",
        30: "Satu Mare",
        31: "Salaj",
        32: "Sibiu",
        33: "Suceava",
        34: "Teleorman",
        35: "Timis",
        36: "Tulcea",
        37: "Vaslui",
        38: "Valcea",
        39: "Vrancea",
        41: "Bucuresti/Sectorul 1",
        42: "Bucuresti/Sectorul 2",
        43: "Bucuresti/Sectorul 3",
        44: "Bucuresti/Sectorul 4",
        45: "Bucuresti/Sectorul 5",
        46: "Bucuresti/Sectorul 6",
        51: "Calarasi",
        52: "Giurgiu"
    }

    def __init__(self, cnp: str):
        self.cnp = cnp
        self.day = None
        self.month = None
        self.year = None
        self.genre = None
        self.city = None

    def is_valid(self) -> bool:
        if self._validate() is False:
            return False
        self.genre = int(self.cnp[:1])
        self.month = int(self.cnp[3:][:2])
        self.day = int(self.cnp[5:][:2])
        self.city = int(self.cnp[7:][:2])
        self.year = self.get_year()
        if 1 > self.month or 12 < self.month or 1 > self.day or 31 < self.day or self.city not in CNP.CITIES:
            return False
        return True

    def _validate(self) -> bool:
        if not RotldValidators.is_int_representable(self.cnp):
            return False
        key = '279146358279'
        if 13 != len(self.cnp):
            return False
        s = 0
        for x in range(0, 12):
            s += int(self.cnp[x]) * int(key[x])

        s = s % 11
        if (10 == s and '1' != self.cnp[12]) or (10 > s != int(self.cnp[12])):
            return False
        return True

    def get_year(self) -> int:
        """
        determine year based on cnp code
        :return: the year as an integer
        """
        if 0 < self.genre < 3:
            pre = 19
        elif 2 < self.genre < 5:
            pre = 18
        elif 4 < self.genre < 7:
            pre = 20
        else:
            raise Exception('Genre is not a valid value')
        year = (pre * 100) + int(self.cnp[1:][:2])
        return year

    def check_if_at_least_eighteen_years_old(self) -> bool:
        """
        method that checks age based on cnp of an individual
        :return: returns True if his age is greater or equal than 18 otherwise False
        """
        born = datetime(year=self.year, month=self.month, day=self.day)
        today = datetime.now().date()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        if age >= 18:
            return True
        return False
