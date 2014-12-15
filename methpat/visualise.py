import json
import logging
from pkg_resources import resource_filename
import os
from doc_template import DOC_TEMPLATE

def make_asset_paths(asset_names):
    return [resource_filename('methpat', os.path.join('data', asset))
               for asset in asset_names]

def web_assets(args):
    script_link = '<script type="text/javascript" src="{}"></script>'
    css_link = '<link rel="stylesheet" href="{}">'
    css_asset_names = [ 'bootstrap.min.css' ]
    js_asset_names = [ 'd3.v3.min.js'
                     , 'jquery.min.js'
                     , 'bootstrap.min.js'
                     , 'saveSvgAsPng.js'
                     ]
    if args.webassets == 'package':
        js_asset_paths = make_asset_paths(js_asset_names) 
        css_asset_paths = make_asset_paths(css_asset_names) 
    elif args.webassets == 'online':
        js_asset_paths = [ 'http://d3js.org/d3.v3.min.js'
                         , 'http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js'
                         , 'http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js'
                         , 'http://bjpop.github.io/saveSvgAsPng/saveSvgAsPng.js']
        css_asset_paths = [ 'http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css' ]
    else: #args.webassets == 'local':
        js_asset_paths = js_asset_names
        js_asset_paths = css_asset_names
    js_asset_links = [ script_link.format(path) for path in js_asset_paths ]
    css_asset_links = [ css_link.format(path) for path in css_asset_paths ]
    return '\n'.join(css_asset_links + js_asset_links)

def make_html(args, amplicon_names, json_dict):
    js_strings = []
    for amplicon_name in amplicon_names:
        try:
            amplicon_dict = json_dict[amplicon_name]
        except KeyError:
            logging.info("No methylation patterns found for {}".format(amplicon_name))
            continue
        # sort patterns on count in descending order
        amplicon_dict['patterns'].sort(key=lambda x:x['count'], reverse=True)
        json_str = json.dumps(amplicon_dict)
        js_strings.append('create_matrix({});'.format(json_str))
    doc = DOC_TEMPLATE % (web_assets(args), args.title, '\n'.join(js_strings))
    with open(args.html, 'w') as html_file:
        html_file.write(doc)
