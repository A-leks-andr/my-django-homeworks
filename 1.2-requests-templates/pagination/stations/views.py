import csv
import logging

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse

logger = logging.getLogger(__name__)


def load_bus_stations():
    """Загружает список остановок из CSV-файла, заданного в настройках.

    Возвращает кортеж (список остановок, сообщение об ошибке). Если файл
    недоступен или повреждён — возвращает пустой список и понятное
    пользователю сообщение, а также пишет предупреждение в лог.
    """
    csv_path = getattr(settings, "BUS_STATION_CSV", None)
    stations = []
    if not csv_path:
        message = "Данные остановок недоступны: настройка BUS_STATION_CSV не задана."
        logger.warning(message)
        return stations, message
    try:
        with open(csv_path, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stations.append(row)
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        # Файл отсутствует, недоступен или повреждён — работаем с пустым списком.
        message = (
            f"Данные остановок недоступны: не удалось прочитать файл "
            f"{csv_path} ({exc})."
        )
        logger.warning("Не удалось прочитать CSV-файл %s: %s", csv_path, exc)
        return stations, message
    return stations, None


BUS_STATIONS, CSV_WARNING = load_bus_stations()


def index(request):
    return redirect(reverse("bus_stations"))


def bus_stations(request):
    # Let Paginator handle invalid page values (e.g. non-numeric) via get_page()
    page_number = request.GET.get("page", 1)
    paginator = Paginator(BUS_STATIONS, 10)
    page = paginator.get_page(page_number)
    context = {
        "bus_stations": page,
        "page": page,
        "warning": CSV_WARNING,
    }
    return render(request, "stations/index.html", context)
