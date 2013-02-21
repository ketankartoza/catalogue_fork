from django.conf.urls import patterns, url

from .views import (
    modifySearch,
    productIdSearch,
    searchResultMap,
    searchResultPage,
    downloadSearchResult,
    downloadSearchResultMetadata,
    getSensorDictionaries,
    search,
    renderSearchForm,
    renderSearchMap,
    renderSearchResultsPage
)


urlpatterns = patterns(
    '',
    url(r'^modifysearch/(?P<theGuid>[a-h0-9\-]{36})/$',
        modifySearch, name='modifySearch'),
    url(r'^productIdSearch/(?P<theGuid>[a-h0-9\-]{36})/$',
        productIdSearch, name='productIdSearch'),
    #show a single search map
    url(r'^searchresult/(?P<theGuid>[a-h0-9\-]{36})/$',
        searchResultMap, name='searchResultMap'),
    #show a single search page to insert into search result map
    url(r'^searchpage/(?P<theGuid>[a-h0-9\-]{36})/$',
        searchResultPage, name='searchResultPage'),
    # return the results of a search as a shapefile
    url(r'^downloadsearchresults/(?P<theGuid>[a-h0-9\-]{36})/$',
        downloadSearchResult, name='downloadSearchResult'),
    url(r'^downloadsearchmetadata/(?P<theGuid>[a-h0-9\-]{36})/$',
        downloadSearchResultMetadata, name='downloadSearchResultMetadata'),
    url(r'^sensordictionaries/$',
        getSensorDictionaries, name='getSensorDictionaries'),
    url(r'^search/$', search, name='search'),
    url(r'^rendersearchform/$', renderSearchForm, name='renderSearchForm'),
    url(r'^rendersearchmap/$', renderSearchMap, name='renderSearchMap'),
    url(r'^rendersearchresultspage/(?P<theGuid>[a-h0-9\-]{36})/$',
        renderSearchResultsPage, name='renderSearchResultsPage'),
)
