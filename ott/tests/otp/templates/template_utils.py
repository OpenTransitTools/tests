import os
import inspect
from mako.template import Template
from mako.lookup import TemplateLookup
from ott.utils import file_utils

import logging
log = logging.getLogger(__file__)


template_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def make_template(file, tl=None):
    ret_val = None
    try:
        if tl is None:
            tl = TemplateLookup(directories=[template_dir])  # TL needed for the template.defs inclde
        ret_val = Template(filename=file, lookup=tl)
    except Exception as e:
        pass
    return ret_val


def make_named_template(file_name, tl=None):
    ret_val = None
    if tl is None:
        tl = TemplateLookup(directories=[template_dir])  # TL needed for the template.defs include
    for t in file_utils.find_files(template_dir, ".mako"):
        if file_name in t:
            tmpl = make_template(t, tl)
            if tmpl:
                ret_val = tmpl
                break
    return ret_val


def make_templates(tl=None):
    ret_val = []
    if tl is None:
        tl = TemplateLookup(directories=[template_dir])  # TL needed for the template.defs include
    for t in file_utils.find_files(template_dir, ".mako"):
        if 'tora' in t: continue  # TODO: need to make other .mako templates work like tora and vis-vis
        tmpl = make_template(t, tl)
        if tmpl:
            ret_val.append(tmpl)
    return ret_val
