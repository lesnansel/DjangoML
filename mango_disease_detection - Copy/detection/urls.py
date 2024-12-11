# from django.urls import path
# from . views import classify_leaf
# from . views import result

# urlpatterns = [
#     path('classify/', classify_leaf, name='classify_leaf'),  # Example URL for classification
#     path('result/', result, name='result'),        # Example URL for result display
# ]
from django.urls import path
from .views import classify_leaf, result

urlpatterns = [
    path('classify/', classify_leaf, name='classify_leaf'),  # URL for classification
    path('result/<str:prediction>/', result, name='result'),  # URL for result display with prediction
]
