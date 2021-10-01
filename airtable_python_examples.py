'''
presents example methods for basic Airtable API integrations in Python
'''
import os
import time
import pathlib
import urllib
from airtable import Airtable
from pprint import pprint

def download_file(airtable_attachment_url, destination_filepath):
    '''
    download resource at url to dest_filepath
    returns True if success, False if HTTP/URL error
    '''
    try:
        response = urllib.request.urlretrieve(airtable_attachment_url,destination_filepath)
        return True
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        print('HTTPError: {}'.format(e.code))
        return False
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        print('URLError: {}'.format(e.reason))
        return False
    except Exception as e:
        print(e)
        return False

def build_upload_url(file_fullpath, server_root_path, hostname_url):
    '''
    builds a URL for file_fullpath, located in server_root_path, addressed at hostname_url
    hostname_url must contains http:// or https://
    '''
    pprint("http server address: " + hostname_url)
    pprint("root folder for server: " + server_root_path)
    pprint("preparing upload for: " + file_fullpath)
    _file_fullpath = pathlib.Path(file_fullpath)
    _server_root_path = pathlib.Path(server_root_path)
    file_in_subdirs_path = str(_file_fullpath.relative_to(_server_root_path))
    try:
        subdirs = _file_fullpath.relative_to(_server_root_path)
        file_upload_url_path = urllib.parse.urljoin(hostname_url, file_in_subdirs_path)
    except:
        file_upload_url_path = urllib.parse.urljoin(hostname_url, _file_fullpath.name)
    return file_upload_url_path

def upload_file(file_upload_url, record_id, field, airtable_connection):
    '''
    airtable requires uploads be hosted on public web
    we use http_server below + filepath here to do that
    --you'll need to set up a URL for yourself
    --and link it to the computer's public IP address
    uploads file_fullpath to field of record_id
    '''
    try:
        airtable_record = {field:[{"url":file_upload_url}]}
        start, stop = http_server(server_root_path)
        start()
        time.sleep(5)
        pprint("actually sending update request to Airtable")
        response = airtable_connection.update(record_id, airtable_record)
        pprint("waiting for upload to complete")
        time.sleep(8)
        stop()
        return True
    except Exception as e:
        pprint("there was an error uploading that file")
        pprint(e)
        return False

def http_server(path):
    '''
    initalizes a simple http server for sending files to Airtable
    '''
    port = 8000
    host = ""
    server = http.server.HTTPServer((host, port), http.server.SimpleHTTPRequestHandler)
    daemon = threading.Thread(target=server.serve_forever)
    daemon.setDaemon(True)
    def start():
        os.chdir(path)
        daemon.start()
        pprint("server started")
    def stop():
        os.chdir(path)
        server.shutdown()
        server.socket.close()
        pprint("server stopped")
    return start, stop

def calculate_number_of_unique_entries_in_linked_field(linked_field, view, airtable_connection):
    '''
    given a linked field in a table (other fields have GUI for unique entries)
    calculates the number of unique entries in the linked field
    '''
    pprint("getting every record in table")
    records = airtable_connection.get_all(view=view,fields=[linked_field])
    try:
        pprint("number of unique values in field " + linked_field + ": " + str(len(set(records))))
        return len(set(records))
    except:
        pprint("record set is list of lists")
        a_list = []
        for record in records:
            try:
                if isinstance(record['fields'][linked_field],list):
                    for instance in record['fields'][linked_field]:
                        a_list.append(instance)
            except:
                continue
            else:
                try:
                    a_list.append(record[0])
                except:
                    continue
        if a_list:
            pprint("number of unique values in field " + linked_field + ": " + str(len(set(a_list))))
            return len(set(a_list))

def search_field_for_value(field, value, airtable_connection):
    '''
    searches a field for a value
    returns list of results (list of Airtable record objects)
    '''
    formula_str = "FIND('" + value + "',{" + field + "})=1"
    results = airtable_connection.get_all(formula=formula_str)
    return results
