import transliterate


# Файл, который служит для добавления книг
out = transliterate.translit("Pushkin_'SKAZKA_O_TsARE_SALTANE,_O_SYNE_EGO_SLAVNOM_I_MOGUChEM_BOGATYRE_KNJaZE_GVIDONE_SALTANOVIChE_I_O_PREKRASNOJ_TsAREVNE_LEBEDI'", reversed=True)
print(out.replace(' ', '_'))
