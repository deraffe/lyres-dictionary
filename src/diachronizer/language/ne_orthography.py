import random
from src.diachronizer.engine.helpers import often, even, occ

def from_me_phonemes(phonemes, overrides=[]):
    result = []
    insert_lengthening_e = False
    skip_next = 0

    last_stressed_vowel = None

    for i in range(0, len(phonemes)):
        if skip_next > 0:
            skip_next -= 1
            continue

        phone = phonemes[i]

        prev2 = None
        prev = None
        next1 = None
        next2 = None
        next3 = None
         
        if i > 1:
            prev2 = phonemes[i - 2]
        if i > 0:
            prev = phonemes[i - 1]
        if i < len(phonemes) - 1:
            next1 = phonemes[i + 1]
        if i < len(phonemes) - 2:
            next2 = phonemes[i + 2]
        if i < len(phonemes) - 3:
            next3 = phonemes[i + 3]

        if insert_lengthening_e and phone.is_vowel():
            insert_lengthening_e = False

        # Diphthongs
        if phone.value == "uː" and "vocalized-g" in phone.history:
            result += random.choose("ow", "ough")
        elif next1 and phone.value + next1.value == "aux":
            result += "augh"
            skip_next = True
        elif next1 and phone.value + next1.value == "ɛix":
            result += "aigh"
            skip_next = True
        elif next1 and phone.value + next1.value == "iːx":
            result += "igh"
            skip_next = True
        elif next1 and phone.value + next1.value == "ɔux":
            result += "ough"
            skip_next = True
        elif next1 and phone.value + next1.value == "uːx":
            result += "ough"
            skip_next = True
        elif phone.value == "ai":
            if not next1:
                result += "ay"
            elif next1 and next1.is_vowel():
                if (even() and not "aiV->ay" in overrides) or "aiV->ai" in overrides:
                    result += "ai"
                    skip_next = True
                else:
                    result += "ay"
            else:
                result += "ai"
        elif phone.value == "au":
            result += "aw"
        elif phone.value in ["ɛu", "iu"]:
            if next1:
                result += random.choice(["ew", "ue", "u"])
            else:
                result += random.choice(["ew", "ue"])
        elif phone.value == "ɔu":
            result += "ow"

        # Monophthongs
        elif phone.value == "a":
            result += "a"
        elif phone.value == "aː":
            result += "a"
            if next1 and not (next1.is_geminate() or (next2 and next2.is_consonant()) or next1.value in ["ʃ"]):
                insert_lengthening_e = True
        elif phone.value == "e":
            if next1 and next1.value == "r":
                # These cases seem ambiguous. 
                # "ea" may be more common when descending from "eo" spelling?
                if "orth_e+r->ea" in overrides:
                    result += "ea"
                    overrides.remove("orth_e+r->ea")
                elif "orth_e+r->a" in overrides:
                    result += "a"
                    overrides.remove("orth_e+r->a")
                elif "orth_e+r->e" in overrides:
                    result += "e"
                    overrides.remove("orth_e+r->e")
                else:
                    if often():
                        result += "ea"
                    elif often():
                        result += "a"
                    else:
                        result += "e"
            else:
                result += "e"
        elif phone.value == "ɛː":
            if "orth_ɛː->ea" in overrides:
                result += "ea"
            elif "orth_ɛː->eCV" in overrides:
                result += "e"
                insert_lengthening_e = True
            elif often():
                result += "ea"
            else:
                result += "e"
                insert_lengthening_e = True
        elif phone.value == "i":
            result += "i"
        elif phone.value == "iː" and next1 and next1.is_consonant() and next2 and next2.is_consonant():
            result += "i"
        elif phone.value == "iː":
            if next1:
                result += "i"
                insert_lengthening_e = True
            else:
                if prev2 and prev2 and prev.is_consonant() and prev2.is_consonant():
                    result += "y"
                else:
                    if "iː#->ie#" in overrides:
                        result += "ie"
                    elif "iː#->ye#" in overrides:
                        result += "ye"
                    else:
                        result += random.choice(["ie", "ye"])
        elif phone.value == "eː" and next1 and next2 and next1.value + next2.value in ["nd", "ld"]:
            result += "ie"
        elif phone.value == "eː":
            result += "ee"
        elif phone.value == "o":
            result += "o"
        elif phone.value == "ɔː":
            if "orth_ɔː->oa" in overrides:
                result += "oa"
            elif "orth_ɔː->oCV" in overrides:
                result += "o"
                insert_lengthening_e = True
            elif often():
                result += "oa"
            else:
                result += "o"
                insert_lengthening_e = True
        elif phone.value == "oː":
            result += "oo"
        elif phone.value == "u" and prev and prev.value == "w" and next1 and next1.value == "r":
            result += "o"
        elif phone.value == "u" and next1 and next1.value == "r":
            result += "u"
        elif phone.value == "u" and next1 and next1.value == "v":
            result += "o"
            insert_lengthening_e = True
        elif phone.value == "u":
            result += "u"
        elif phone.value == "uː":
            if next1:
                result += "ou"
        elif phone.value == "ə":
            if not next2:
                if next1.value in ["m", "w"]:
                    result += "o"
                elif next1.value in ["l"]:
                    result += "i"
                else:
                    result += "e"
            else:
                result += "e"

        # Consonants
        elif phone.value == "f":
            if next1 \
                or (prev and prev.is_consonant()) \
                or (prev and prev.is_vowel() and prev.is_long()):
                result += "f"
            else:
                result += "ff"
        elif phone.value == "l":
            if next1 != None \
                or (prev and prev.is_vowel() and prev.is_long()) \
                or (prev and prev.is_consonant()):
                result += "l"
            elif not next1 and prev and prev.value == "ə" \
                and prev2 and prev2.is_consonant() \
                and not prev2.value in ["dʒ"]:
                if last_stressed_vowel and last_stressed_vowel.is_long():
                    result += "l"
                else:
                    result = result[:-1] + ["le"]
            elif prev.is_vowel() and (not prev.stressed or prev.is_diphthong()):
                result += "l"
            else:
                result += "ll"
        elif phone.value == "s":
            if next1:
                if next1.value == "c":
                    result += "sh"
                    skip_next = True
                else:
                    result += "s"
            else:
                if prev and prev.is_vowel() and prev.is_short():
                    result += "ss"
                elif prev and prev.value == "r":
                    result += "se"
                elif prev and prev.value == "iː":
                    result += "c"
                elif prev and prev.is_vowel() and prev.is_long() and not insert_lengthening_e:
                    result += "se"
                else:
                    result += "s"
        elif phone.value == "z":
            if prev and prev.is_vowel() and prev.is_short():
                result += "zz"
            else:
                if not next1 and prev and prev.value == "r":
                    result += "se"
                else:
                    result += "s"
        elif phone.value in ["θ", "ð"]:
            result += "th"
        elif phone.value in ["x", "xx"]:
            if prev == None:
                result += "h"
            else:
                result += "gh"
        elif phone.value == "k":
            if not next1 and prev and prev.is_vowel() and prev.is_short():
                result += "ck"
            elif next1 and next1.value == "w":
                    result += "qu"
                    skip_next = True
            elif not prev and not (next1 and next1.value == "n") and not (next1 and next1.value in ["e", "i"]):
                result += "c"
            else:
                result += "k"
        elif phone.value == "ks":
            result += "x"
            skip_next = True
        elif phone.value == "ʃ":
            result += "sh"
        elif phone.value == "tʃ":
            if not next1:
                result += "tch"
            else:
                result += "ch"
        elif phone.value == "dʒ":
            if prev == None:
                result += "j"
            else:
                result += "dg"
                if next1 == None:
                    result += "e"
        elif phone.value == "w":
            if prev and prev.value == "x" and not prev2:
                result = "wh" 
            else:
                result += "w"
        elif phone.value == "j":
            if prev and prev.value == "ə":
                result = result[:-1]
            result += "y"
        elif phone.value == "y":
            result += "u"
        else:
            result += phone.value

        # Various word-end adjustments
        if phone.is_consonant() and insert_lengthening_e and (not next1 or not next1.is_vowel()):
            # Insert lengthening 'e'
            result += "e"
            insert_lengthening_e = False
        elif phone.is_consonant() and not phone.is_geminate() \
            and prev and prev.is_vowel() and prev.is_short() \
            and next1 and next1.is_vowel() \
            and phone.value not in ["v", "j", "θ", "ð", "ʃ", "dʒ"]:
            # Double non-final consonant after short vowel
            if phone.value == "k":
                result = result[:-1] + ["ck"]
            else:
                result += result[-1]
        elif not next1 and phone.value in ["v", "z"] and result[-1] != "e":
            # Makes sure certain voiced fricatives don't end a word
            result += "e"
        
        if phone.is_vowel() and phone.stressed:
            last_stressed_vowel = phone
        
    return "".join(result)
