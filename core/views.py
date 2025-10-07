from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render
from django.utils.timezone import now, timedelta

from movements.models import Movement
from stock.models import Category, Ingredient, Product


@login_required
def home(request):
    today = now().date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    def get_net(start_date):
        entradas = (
            Movement.objects.filter(date__date__gte=start_date, type="in").aggregate(Sum("value"))["value__sum"] or 0
        )
        saidas = (
            Movement.objects.filter(date__date__gte=start_date, type="out").aggregate(Sum("value"))["value__sum"] or 0
        )
        return saidas - entradas

    context = {
        "total_movements": Movement.objects.count(),
        "total_products": Product.objects.count(),
        "low_stock_count": Ingredient.objects.filter(qte__lt=F("min_qte")).count(),
        "total_categories": Category.objects.count(),
        "recent_movements": Movement.objects.order_by("-date")[:5],
        "low_stock_alerts": Ingredient.objects.filter(qte__lt=F("min_qte")),
        "daily_net": get_net(today),
        "weekly_net": get_net(week_start),
        "monthly_net": get_net(month_start),
    }

    return render(request, "home.html", context)
