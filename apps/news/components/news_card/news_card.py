from django_components import component


@component.register("news_card")
class NewsCard(component.Component):
    template_name = "news_card/template.html"
