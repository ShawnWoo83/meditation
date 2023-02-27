function validatePhone(value) {
    const reg = /^(?:(?:\+|00)86)?1[3-9]\d{9}$/;
    return reg.test(value)
}

function validatePassword(value) {
    const reg = /^[a-zA-Z0-9_]{6,}$/;
    return reg.test(value)
}

function isNullOrEmpty(value) {
    return /^\s*$/.test(value);
}