import os
import inspect
from mako.template import Template
from mako.lookup import TemplateLookup

import logging
log = logging.getLogger(__file__)

template_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


def make_named_template(file, tl=None):
    ret_val = None
    try:
        #import pdb; pdb.set_trace()
        if tl is None:
            tl = TemplateLookup(directories=[template_dir])  # TL needed for the template.defs include
        ret_val = Template(filename=file, lookup=tl)
    except Exception as e:
        log.error("{}\n template {}/{}".format(e, template_dir, file))
        pass
    return ret_val


def make_templates():
    ret_val = []
    tmpl_dir=os.path.join(misc.this_module_dir, 'templates')
    tl = TemplateLookup(directories=[tmpl_dir])  # TL needed for the template.defs include
    for t in file_utils.find_files(tmpl_dir, ".mako"):
        tmpl = make_named_template(t, tl)
        if tmpl:
            #print(t)
            ret_val.append(tmpl)
    return ret_val
