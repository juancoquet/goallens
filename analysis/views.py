from django.shortcuts import render # type: ignore


def m_and_a_view(request):
    return render(request, 'm_and_a.html')