from django.shortcuts import render, redirect
from .models import Url
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Url
from .serializers import UrlSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

class CreateShortLinkView(generics.CreateAPIView):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

class ListShortLinksView(generics.ListAPIView):
    serializer_class = UrlSerializer

    def get_queryset(self):
        user = self.request.user
        return Url.objects.filter(user=user)

class PageViewsCountView(generics.ListAPIView):
    serializer_class = UrlSerializer

    def get_queryset(self):
        user = self.request.user
        return Url.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page_views_count = {}
        for url in queryset:
            page_views_count[url.short_code] = url.pageviews.filter(created_at__gte=datetime.now()-timedelta(days=7)).count()
        return Response(page_views_count)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class LogoutView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
# Create your views here.
def index(request):
    context = {}
    if request.method == 'POST':
        original_url = request.POST['original_url']
        url = Url.objects.create(original_url=original_url)
        short_url = request.build_absolute_uri('/') + url.short_code
        context['short_url'] = short_url

    return render(request, 'index.html', context)

def redirect_to_original(request, short_code):
    url = Url.objects.get(short_code=short_code)
    return redirect(url.original_url)