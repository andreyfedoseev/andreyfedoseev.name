import cssutils
import os
import logging


cssutils.log.setLevel(logging.ERROR)


def run():

    selectors = []

    styles_dir = os.path.join(os.path.dirname(__file__), "../media/LESS_CACHE/")

    for dirpath, diranames, filenames, in os.walk(styles_dir):
        for filename in filenames:
            if not filename.endswith(".css") or filename.startswith("ie"):
                continue

            print "Processing", filename

            filename = os.path.join(dirpath, filename)
            sheet = cssutils.parseFile(filename)

            for rule in sheet:
                if not isinstance(rule, cssutils.css.CSSStyleRule):
                    continue
                if rule.style.getPropertyValue("display") == "inline-block":
                    selectors.append(rule.selectorText)

    selectors.sort()
    print
    print
    print """%s {
    display: inline;
    zoom: 1;
}""" % ",\n".join(selectors)