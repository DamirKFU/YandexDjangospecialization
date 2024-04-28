from django.urls import path

import statistic.apps
import statistic.views

__all__ = []


app_name = statistic.apps.StatisticConfig.name

urlpatterns = [
    path(
        "",
        statistic.views.StatisticByUserTemplateView.as_view(),
        name="by-user",
    ),
    path(
        "items/graded/",
        statistic.views.StatisticGradedItemsListView.as_view(),
        name="graded-items",
    ),
    path(
        "items/",
        statistic.views.StatisticByItemsListView.as_view(),
        name="by-items",
    ),
]
