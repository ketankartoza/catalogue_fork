import tidy

# see http://tidy.sourceforge.net/docs/quickref.html
# for all options
options = dict(output_xhtml=False,
               add_xml_decl=False,
               doctype='strict',
               indent='auto',
               tidy_mark=False,
               hide_comments=True,
               wrap=100)


class PrettifyMiddleware(object):
  """Prettify middleware"""
  def process_response(self, request, response):
    if 'text/html' not in response['Content-Type'].lower(): 
      return response
    else:
      content = response.content
      content = str(tidy.parseString(content, **options))
      response.content = content
      return response

