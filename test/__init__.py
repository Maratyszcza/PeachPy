def equal_codes(code, ref_code):
    assert isinstance(code, (str, list))
    assert isinstance(ref_code, (str, list))

    import string
    if isinstance(code, str):
        code = code.splitlines()
    if isinstance(ref_code, str):
        ref_code = ref_code.splitlines()
    code = map(string.strip, filter(len, code))
    ref_code = map(string.strip, filter(len, ref_code))
    return code == ref_code

