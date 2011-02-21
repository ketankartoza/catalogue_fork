"""This is a decorator that when used will always pass the RequestContext
   over to the template. This is needed in tandem with the authentication 
   stuff so that the templates can know who the logged in users is 
   and perform conditional rendering based on that. 
   
   example useage in your view:

   from catalogue.renderDecorator import renderWithContext

   @renderWithContext('demo.html')  
   def demo(request):
       return {}

   The template will then have the RequestContext passed to it along 
   automatically,  along with any other parameters your view defines.
   """
from django.shortcuts import render_to_response
from django.template import RequestContext
from pdfReport import render_to_pdf

class renderWithContext(object):
  def __init__(self, template_name, ajax_template_name=None):
    self.template_name = template_name
    self.ajax_template_name = ajax_template_name

  def __call__(self, func):
    def rendered_func(request, *args, **kwargs):
      if request.is_ajax():
        render_template = self.ajax_template_name
      else:
        render_template = self.template_name

      items = func(request, *args, **kwargs)
      #check for PDF arg
      if request.GET.has_key('pdf'):
        tmp_template_name = '/'.join(['pdf',self.template_name])
        return render_to_pdf(tmp_template_name,items)

      return render_to_response(render_template, items, context_instance=RequestContext(request))

    return rendered_func
