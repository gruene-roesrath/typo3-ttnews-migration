# coding: utf-8

import os
from datetime import datetime
import base64
from pprint import pprint

import xml.etree.ElementTree as ET
import yaml
import html2markdown

filename = 'testdata/news-export.xml'

content_files = {}
content_files_filename_to_id = {}

def main():
    tree = ET.parse(filename)
    root = tree.getroot()

    # collect files into memory
    for files in root.findall('files'):
        for f in files.findall('file'):
            print("Found file: %s" % f.attrib)
            if 'index' not in f.attrib:
                continue
            content_files[f.attrib['index']] = {}
            for child in f:
                content_files[f.attrib['index']][child.tag] = child.text

                # set reference from filename to ID
                if child.tag == 'filename':
                    content_files_filename_to_id[child.text] = f.attrib['index']

    # collect articles
    for child in root.iter('tablerow'):
        # looking for <tablerow index="tt_news:192240" type="array">
        table, news_id = child.attrib['index'].split(':')
        if table != 'tt_news':
            continue
        
        print("Found article: %s" % child.attrib)
        record = {
            "id": news_id
        }
        fieldlist = child.find('fieldlist')

        for field in fieldlist.iter('field'):
            if field.text is not None:
                record[field.attrib['index']] = field.text
        
        export_article(record)
    

def export_article(data):
    ts = int(data['datetime'])
    dt = datetime.utcfromtimestamp(ts)
    data['datetime'] = dt

    del_keys = ['l18n_diffsource']
    for key in del_keys:
        if key in data:
            del data[key]

    printdata = dict(data)
    if 'bodytext' in printdata:
        del printdata['bodytext']
    #pprint(printdata)
    
    frontmatter = {
        'title': data['title'],
        'summary': data.get('short'),
        'date': data['datetime'].isoformat(),
    }

    if data.get('author'):
        frontmatter['author'] = data.get('author')

    folder_path = 'export/%s-%s' % (dt.strftime('%Y-%m-%d'), data['id'])
    os.makedirs(folder_path, exist_ok=True)

    if data.get('image'):
        resources = []
        filenames = data.get('image').split(',')
        for fn in filenames:
            fid = None
            if fn not in content_files_filename_to_id:
                print("Error: Image %s not in content_files_filename_to_id" % fn)
                continue
            fid = content_files_filename_to_id[fn]
            res = {'src': fn, 'title': ''}
            resources.append(res)

            # store file
            res_path = folder_path + "/" + fn
            with open(res_path, 'wb') as resfile:
                content = base64.b64decode(content_files[fid]['content'])
                resfile.write(content)

        frontmatter['resources'] = resources

    file_path = folder_path + '/index.md'

    with open(file_path, 'w') as myfile:
        myfile.write('---\n')
        myfile.write(yaml.dump(frontmatter, default_flow_style=False))
        myfile.write('---\n\n')
        myfile.write(html2markdown.convert(data['bodytext']) + '\n')

if __name__ == "__main__":
    main()
