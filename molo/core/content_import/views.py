from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes)
from rest_framework.response import Response
from rest_framework.authentication import (
    SessionAuthentication, BasicAuthentication)
from rest_framework.permissions import IsAuthenticated

from molo.core.content_import import api
from unicore.content.models import Localisation


@api_view(['GET'])
def get_repos(request):
    return Response({'repos': api.get_repo_summaries()})


@api_view(['GET'])
def get_repo_languages(request):
    names = request.query_params.getlist('repo')
    repos = api.get_repos(names, models=(Localisation,))
    return Response(api.get_languages(repos))


@api_view(['PUT'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def import_content(request):
    data = request.data
    names, locales = data.getlist('repos'), data.getlist('locales')
    repos = api.get_repos(names)
    errors = api.validate_content(repos, locales)

    if errors:
        return Response(status=422, data={
            'type': 'validation_failure',
            'errors': errors
        })
    else:
        api.import_content(repos, locales)
        return Response(status=204)


@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def import_validate(request):
    data = request.data
    names, locales = data.getlist('repos'), data.getlist('locales')
    repos = api.get_repos(names)
    errors = api.validate_content(repos, locales)

    return Response(data={
        'repos': names,
        'locales': locales,
        'errors': errors
    })
