import re

date = re.compile(
    u"(?:(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?\s+(?:of\s+)?(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)|(?:jan\.?|january|feb\.?|february|mar\.?|march|apr\.?|april|may|jun\.?|june|jul\.?|july|aug\.?|august|sep\.?|september|oct\.?|october|nov\.?|november|dec\.?|december)\s+(?<!\:)(?<!\:\d)[0-3]?\d(?:st|nd|rd|th)?)(?:\,)?\s*(?:\d{4})?|[0-3]?\d[-\./][0-3]?\d[-\./]\d{2,4}",
    re.IGNORECASE,
)
time = re.compile(u"\d{1,2}:\d{2} ?(?:[ap]\.?m\.?)?|\d[ap]\.?m\.?", re.IGNORECASE)
phone = re.compile(
    u"""((?:(?<![\d-])(?:\+?\d{1,3}[-.\s*]?)?(?:\(?\d{3}\)?[-.\s*]?)?\d{3}[-.\s*]?\d{4}(?![\d-]))|(?:(?<![\d-])(?:(?:\(\+?\d{2}\))|(?:\+?\d{2}))\s*\d{2}\s*\d{3}\s*\d{4}(?![\d-])))"""
)
phones_with_exts = re.compile(
    u"((?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*(?:[2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|(?:[2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?(?:[2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?(?:[0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(?:\d+)?))",
    re.IGNORECASE,
)
email = re.compile(
    u"([a-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)",
    re.IGNORECASE,
)
ip = re.compile(
    u"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
    re.IGNORECASE,
)
ipv6 = re.compile(
    u"\s*(?!.*::.*::)(?:(?!:)|:(?=:))(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)){6}(?:[0-9a-f]{0,4}(?:(?<=::)|(?<!::):)[0-9a-f]{0,4}(?:(?<=::)|(?<!:)|(?<=:)(?<!::):)|(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)){3})\s*",
    re.VERBOSE | re.IGNORECASE | re.DOTALL,
)

credit_card = re.compile(u"((?:(?:\\d{4}[- ]?){3}\\d{4}|\\d{15,16}))(?![\\d])")
btc_address = re.compile(
    u"(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])"
)
street_address = re.compile(
    u"\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|park|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)",
    re.IGNORECASE,
)
zip_code = re.compile(r"\b\d{5}(?:[-\s]\d{4})?\b")
po_box = re.compile(r"P\.? ?O\.? Box \d+", re.IGNORECASE)

postcodes = re.compile("([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2})")
ukphones = re.compile("^\s*\(?(020[7,8]{1}\)?[ ]?[1-9]{1}[0-9{2}[ ]?[0-9]{4})|(0[1-8]{1}[0-9]{3}\)?[ ]?[1-9]{1}[0-9]{2}[ ]?[0-9]{3})\s*$")

medical_record_number = re.compile(
    r"\bMRN[ -]?\d{6,}\b",  # Example: MRN 123456 or MRN-123456
    re.IGNORECASE,
)
health_insurance_beneficiary_number = re.compile(
    r"\bHIBN[ -]?\d{9,}\b",  # Example: HIBN 123456789 or HIBN-123456789
    re.IGNORECASE,
)
social_security_number = re.compile(
    r"\b\d{3}-\d{2}-\d{4}\b"  # Example: 123-45-6789
)
nhs_number_uk = re.compile(
    r"\b\d{3}-\d{3}-\d{4}\b",  # Example: NHS number in the UK 123-456-7890
    re.IGNORECASE,
)
patient_id = re.compile(
    r"\bPID[ -]?\d{5,}\b",  # Example: PID 12345 or PID-12345
    re.IGNORECASE,
)
drug_prescription_number = re.compile(
    r"\bRx[ -]?\d{7,}\b",  # Example: Rx 1234567 or Rx-1234567
    re.IGNORECASE,
)

regexes = {
    "dates": date,
    "times": time,
    "phones": phone,
    "phones_with_exts": phones_with_exts,
    "emails": email,
    "ips": ip,
    "ipv6s": ipv6,
    "credit_cards": credit_card,
    "btc_addresses": btc_address,
    "street_addresses": street_address,
    "zip_codes": zip_code,
    "po_boxes": po_box,
    "postcodes": postcodes,
    "ukphones": ukphones,
    "medical_record_numbers": medical_record_number,
    "health_insurance_beneficiary_numbers": health_insurance_beneficiary_number,
    "social_security_numbers": social_security_number,
    "nhs_numbers_uk": nhs_number_uk,
    "patient_ids": patient_id,
    "drug_prescription_numbers": drug_prescription_number
}


class regex:
    def __init__(self, obj, regex):
        self.obj = obj
        self.regex = regex

    def __call__(self, *args):
        def regex_method(text=None):
            return [x for x
                    in self.regex.findall(text or self.obj.text)]

        return regex_method


class PiiRegex(object):
    def __init__(self, text=""):
        self.text = text

        # Build class attributes of callables.
        for k, v in regexes.items():
            setattr(self, k, regex(self, v)(self))

        if text:
            for key in regexes.keys():
                method = getattr(self, key)
                setattr(self, key, method())

    def any_match(self, text=""):
        """Scan through all available matches and try to match.
        """
        if text:
            self.text = text

            # Regenerate class attribute callables.
            for k, v in regexes.items():
                setattr(self, k, regex(self, v)(self))
            for key in regexes.keys():
                method = getattr(self, key)
                setattr(self, key, method())

        matches = []
        for match in regexes.keys():
            # If we've got a result, add it to matches.
            if getattr(self, match):
                matches.append(match)

        return True if matches else False
