"""
Scrape Google Scholar search results for references.
"""

import re
import hashlib
import random
import html.entities as htmlent
import optparse
import requests
import bibtexparser

GSCHOLAR_BASE_URL = "http://scholar.google.com"
GSCHOLAR_QUERY_PATH = "/scholar"

def _unescape_html_entities(html):
  # Author: Fredrik Lundh
  # http://effbot.org/zone/re-sub.htm#unescape-html
  def fixup(m):
    html = m.group(0)
    if html[:2] == "&#":
      # character reference
      try:
        if html[:3] == "&#x":
          return chr(int(html[3:-1], 16))
        else:
          return chr(int(html[2:-1]))
      except ValueError:
        pass
    else:
      # named entity9
      try:
        html = chr(htmlent.name2codepoint[html[1:-1]])
      except KeyError:
        pass
    return html # leave as is
  return re.sub("&#?\w+;", fixup, html)

def _gen_fake_google_id():
  return hashlib.md5(str(random.random()).encode("utf-8")).hexdigest()[:16]

def _extract_bib_links(html):
  return [_unescape_html_entities(m) for m in \
            re.compile(r'<a href="(/scholar\.bib\?[^"]*)').findall(html)]

def _do_gscholar_request(path, gid, params={}):
  return requests.get(GSCHOLAR_BASE_URL + path, params=params,
  headers={'User-Agent': 'Mozilla/5.0',
       'Cookie': 'GSP=ID=%s:CF=4' % gid})

def _extract_bib_from_link(link, gid):
  return _do_gscholar_request(link, gid).text

def _extract_bibtex_results(html, count, gid):
  links = _extract_bib_links(html)[:count]
  return [_extract_bib_from_link(link, gid) for link in links]

def _parse_bibtex(bib):
  return bibtexparser.loads(bib).entries

def get_results(query, count):
  gid = _gen_fake_google_id()
  html = _do_gscholar_request(GSCHOLAR_QUERY_PATH, gid, {"q": query}).text
  brs = _extract_bibtex_results(html, count, gid)
  return _parse_bibtex("\n".join(brs))

def get_result(query):
  rs = get_results(query, 1)
  if rs:
    return rs[0]

def _render_ref_as_xml(r):
  id = r.pop("id", "")
  return "<ref id=\"%s\">%s\n</ref>" % (id,
    "".join(["\n  <%s>%s</%s>" % (k, v, k) for (k, v) in r.items()]))

def get_results_as_xml(query, count):
  return [_render_ref_as_xml(r) for r in get_results(query, count)]

def get_result_as_xml(query):
  rs = get_results_as_xml(query, 1)
  if rs:
    return rs[0]

def main():
  parser = optparse.OptionParser('Usage: %prog [-n NUMBER] QUERY')
  parser.add_option("-n", "--number", type="int", dest="count",
    default=1, help="number of results to show")
  (options, args) = parser.parse_args()
  if len(args) != 1:
    parser.error("No query given, nothing to do.")
    sys.exit(1)
  query = args[0]
  results = get_results_as_xml(query, options.count)
  out = "\n\n".join(results)
  print(out)
