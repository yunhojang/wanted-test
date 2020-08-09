from typing import (
    List, Union, Mapping
)
from rest_api_service.api.common import error
from rest_api_service.api.common.enumeration import ErrorType
from rest_api_service.api.models import post_dao


@error.handle_exception_commonly
def get_autocompleted_companys(condition_params={}) -> Union[error.Error, Mapping]:
    import re
    word = condition_params.get('companyName', None)
    if word is None:
        return []

    regex_ = r".*" + rf'{word}' + r".*"
    results = []
    results_append = results.append
    for doc in post_dao.CompanyInfo.objects.values().raw({'company_ko': re.compile(regex_)}):
        doc.pop('_id', None)
        results_append(doc)
    limit = condition_params.get('limit', 0)
    result = {'totalCount': len(results), 'gettedCount': len(results[:limit]), 'results': results[:limit]}
    return result


@error.handle_exception_commonly
def get_company(condition_params={}) -> Union[error.Error, Mapping]:
    tag = condition_params.get('tagName', None)
    if tag is None:
        return []

    results = []
    results_append = results.append
    for doc in post_dao.CompanyInfo.objects.values().raw({'$text': {'$search': tag}}):
        doc.pop('_id', None)
        results_append(doc)
    result = {'totalCount': len(results), 'gettedCount': len(results), 'results': results}
    return result


@error.handle_exception_commonly
def add_company_tag(inputs={}) -> Union[error.Error, None]:
    return


@error.handle_exception_commonly
def remove_company_tag(condition_params={}) -> Union[error.Error, None]:
    return
