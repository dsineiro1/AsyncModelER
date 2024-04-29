import asyncio
import httpx

from django.http import JsonResponse, StreamingHttpResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render

from .forms import PromptForm

async def stream_data():
    # Generate data in chunks
    for i in "Hi, I am here to help you model your E/R Diagram!$":
        yield f'data: {i}\n\n'
        # Simulate delay between chunks
        await asyncio.sleep(.05)

async def stream_http(request):
    response = StreamingHttpResponse(stream_data())
    response['Content-Type'] = 'text/event-stream'
    return response

class StreamView(TemplateView):
    template_name = "modeler/stream.html"

    async def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
        

class IndexView(TemplateView):
    template_name = "modeler/index.html"

    async def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

class ModelView(TemplateView):
    form_class = PromptForm
    initial = {"key": "value"}
    template_name = "modeler/model.html"

    async def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    async def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            print(form.cleaned_data)
            headers = {'ngrok-skip-browser-warning': 'true'}
            with httpx.stream("GET", "https://d731-34-125-194-209.ngrok-free.app/greet/", headers=headers) as r:
                for text in r.iter_text():
                    print(text)
            return JsonResponse({"prompt": prompt})