

def equal_codes(code, ref_code):
    assert isinstance(code, list) or isinstance(code, str)
    assert isinstance(ref_code, list) or isinstance(code, str)

    if isinstance(code, str):
        code = code.splitlines()
    if isinstance(ref_code, str):
        ref_code = ref_code.splitlines()

    code = [line.strip() for line in code if len(line)]
    ref_code = [line.strip() for line in ref_code if len(line)]
    ref_code = [line.replace("\xC2\xB7", "\u00B7") for line in ref_code]
    return code == ref_code
