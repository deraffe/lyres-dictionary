import src.evolutor.language.oe_orthography as orthography
import src.utils.helpers as helpers
from src.utils.logging import Logger

# Returns any prefix matching the given written form
def get_prefix(form):
    prefixes = {
        "a": "a",
        "ā": "a",
        "biġ": "by",
        "bī": "by",
        "be": "be",
        "for": "for",
        "ġe": "", # TODO: Allow this to be rendered as /a/, /e/, or /i/ in some cases (as in 'afford', 'enough', 'handiwork')
        "on": "a" # TODO: Maybe add a probability to this
    }

    if form in prefixes:
        return prefixes[form]

def get_derivational(form_tail):
    suffixes = {
        "ard": "ard",
        "els": "els",
        "else": "els",
        "elsi": "els",
        "en": "en",
        "iġ": "iġ",
        "t": "þ",
        "þ": "þ"
    }

    raw_value = "".join(form_tail).split("+")[0].split("|")[0]
    if raw_value in suffixes:
        return suffixes[raw_value]

# Get a pseudo-past-participle form for the given form, treating it as the given verb class
#
# NOTE: this does *not* produce historical Old English participles. Rather, it produces
# an alternative form that should convert properly into a modern-style participle.
#
# Specifically, it does not produce changes in consonants due to Verner's law, as in cases like
# 'frēosan' (freeze) -> 'fruron', or 'ċēosan' choose -> 'curon', as PDE does not include
# these sound changes, using the forms 'frozen' and 'chosen'
#
# That said, Verner's law does apply in cases like 'forlese' -> 'forlorn', or 'sodden' (from 'sēoþan'),
# so I should probably add handling from it at some point. There are also some cases of literary use,
# e.g. 'frore' in Milton
# TODO: Support Verner's law sound changes in past participles.
def get_strong_pseudoparticiple(form, verb_class, drop_suffix=False):
    # If this is a contract form, call the separate function for that
    if form[-2:] in ["on", "ōn"]:
        return get_strong_pseudoparticiple_contracted(form, verb_class, drop_suffix)

    if not drop_suffix:
        suffix = "+en"
    else:
        suffix = ""

    # Remove inflectional ending, if any}
    form = form.split("|")[0]

    if verb_class == "weak":
        # TODO: handle class 3 weak verbs (should work for 2 as well)
        return form
    elif verb_class == 7:
        return form + suffix

    vowel_map = {
        1: { "ī": "i" },
        2: { "ēo": "o", "ū": "o" },
        3: { "e": "o", "eo": "o", "i": "u", "ie": "o" },
        4: { "e": "o", "i": "u", "u": "u" },
        5: { "e": "e", "i": "e", "ie": "e"},
        6: { "a": "a", "e": "a", "ē": "aġ", "ea": "a", "ie": "a"}, # 'ie' as in 'hliehhan'. 'a', 'ie' can also go to 'æ". 'ē' -> 'aġ' as in 'slēan', 'flēan'. TODO: Figure out cases like 'swerian' -> 'sworen' that have 'e' -> 'o'
        7: {}
    }

    if not verb_class in vowel_map:
        print("VERB CLASS NOT IN VOWEL MAP! HAVE: " + str(verb_class))

    cluster_indices = []
    for i in range(0, len(form)):
        if form[i] in orthography.vowels:
            cluster_indices = [i]
            for j in range(i, len(form)):
                if form[j] not in orthography.vowels:
                    cluster_indices += [j]
                    break

            if len(cluster_indices) == 2:
                break
            elif len(cluster_indices) == 1:
                cluster_indices += [len(form)]

    if not len(cluster_indices) == 2:
        print("DIDN'T GET PROPER INDICES! HAVE: " + str(cluster_indices))

    vowels = form[cluster_indices[0]: cluster_indices[1]]
    if vowels not in vowel_map[verb_class]:
        print("VOWELS NOT FOUND IN VOWEL MAP! Have " + str(vowels) + " FOR CLASS " + str(verb_class))

    return form[0:cluster_indices[0]] + vowel_map[verb_class][vowels] + form[cluster_indices[1]:] + suffix

# Get a pseudoparticiple for a verb in a contracted form (e.g. 'lēon', 'þēon')
def get_strong_pseudoparticiple_contracted(form, verb_class, drop_suffix=False):
    if not drop_suffix:
        suffix = "+en"
    else:
        suffix = ""

    if verb_class == "weak":
        return form[0:-2]
    else:
        if form[-4:] == "ē|on":
            stem = form[0:-4]
        elif form[-2:] == "ōn":
            stem = form[0:-3]

        if verb_class == 1:
            # TODO: Handle cases where class 1 verbs are given class 2-style endings, as in 'tēon' -> 'togen'
            return stem + "iġ" + suffix
        elif verb_class == 2:
            return stem + "og" + suffix
        elif verb_class == 7:
            # Also appeared as '-ongen' in OE
            # HACK: '-æng' spelling is constructed, with intent of consistently giving '-ang' forms in MnE.
            # TODO: Find a more elegant way to do this.
            return stem + "æng" + suffix
        else:
            Logger.error("ERROR: NO CONTRACTED VERB PARTICIPLE BEHAVIOR FOR CLASS " + str(verb_class) + ", requested for '" + form + "'")
