from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import make_aware
from django.views.decorators.http import require_http_methods
from fpdf import FPDF

from core.decorators import admin_required
from stock.models import Ingredient, Product

from .models import Movement
from .services import create_inflow, create_outflow


@login_required
@require_http_methods(["GET", "POST"])
def movement_create(request: HttpRequest) -> HttpResponse:
    """Renderiza a página de criação de movimentação e processa o registro.

    Args:
        request (HttpRequest): Objeto de requisição do Django.

    GET:
        Renderiza a tela de registro de movimentação com ingredientes e produtos a serem transacionados.

    POST:
        Valida os campos fornecidos de acordo com o tipo de movimentação:
            - Se válida redireciona para a lista de movimentações e exibe uma mensagem de sucesso.
            - Se Inválida redireciona para a crição novamente e exibe uma mensagem de erro.

    Returns:
        HttpResponse: Página de criar movimentação (GET ou POST com dados inválidos).
        HttpResponseRedirect: Redirecionamento para a lista de movimentações (POST válido).

    """

    context = {
        "products": Product.objects.all(),
        "ingredients": Ingredient.objects.all(),
        "type_choices": Movement._meta.get_field("type").choices,
    }

    if request.method == "GET":
        return render(request, "movement_create.html", context)

    try:
        user = request.user
        username = f"{user.first_name} {user.last_name}"
        transaction_type = request.POST.get("type")

        match transaction_type:
            case "in":
                create_inflow(request.POST, username)
            case "out":
                create_outflow(request.POST, username)

        messages.success(request, "Movimentação registrada com sucesso!")
        return redirect("movement_list")

    except ValidationError as e:
        for msg in e.messages:
            messages.error(request, msg)
        return render(request, "movement_create.html", context)


@login_required
@require_http_methods(["GET"])
def movement_list(request: HttpRequest) -> HttpResponse:
    """Exibe uma lista com as movimentações do sistema.

    Args:
        request (HttpRequest): Objeto de requisição do Django.

    GET:
        renderiza a tela de movimentações com o filtro de data vazio.
            - Se tiver filtro, retorna as movimentações correspondentes ao período.
            - Se não tiver filtro, retorna as movimentações de acordo com a página.

    Returns:
        HttpResponse: Listando as movimentações
    """

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        # Pegando as datas e formatando
        start_dt = datetime.strptime(str(start_date), "%Y-%m-%d")
        end_dt = datetime.strptime(str(end_date) + " 23:59:59", "%Y-%m-%d %H:%M:%S")

        # Adicionando o timezone
        start_dt = make_aware(start_dt)
        end_dt = make_aware(end_dt)

        movements = Movement.objects.filter(date__range=(start_dt, end_dt)).order_by("-date")
    else:
        movements = Movement.objects.all().order_by("-date")

    page_number = request.GET.get("page") or 1
    paginator = Paginator(movements, 10)

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "Paginator": paginator,
        "is_paginated": page_obj.has_other_pages(),
    }
    return render(request, "movement_list.html", context)


@login_required
@require_http_methods(["GET"])
def movement_detail(request: HttpRequest, id: int) -> HttpResponse:
    """Renderiza uma página com detalhes da movimentação.

    Args:
        request (HttpRequest): Objeto de requisição do Django.
        id (int): Identificador único da movimentação.

    GET:
        Renderiza a tela com os dados da movimentação.

    Returns:
        HttpResponse: Página de detalhamento.

    """

    movement = get_object_or_404(Movement, id=id)

    context = {"movement": movement}
    return render(request, "movement_detail.html", context)


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def movement_delete(request: HttpRequest, id: int) -> HttpResponse:
    """Exibe e processa a exclusão da movimentação.

    Args:
        request (HttpRequest): Objeto de requisição do Django.
        id (int): identificador único da movimentação.

    GET:
        Renderiza a tela de deletar movimentação solicitando senha.

    POST:
        Valida a senha:
            - Se válida, deleta movimentação do do banco de dados com uma mensagem de sucesso.
            - Se inválido, redireciona para a página de insersão de senha com uma mensagem de erro.

    Returns:
        HttpResponse: Página de deletar movimentação (senha inválida).
        HttpResponseRedirect: Redirecionamento para a página a lista de movimentações (POST válido).
    """

    movement = get_object_or_404(Movement, id=id)
    context = {"movement": movement}

    if request.method == "GET":
        return render(request, "movement_delete.html", context)

    password = request.POST.get("password")

    if not request.user.check_password(password):
        messages.error(request, "A senha que você inseriu está incorreta!")
        return render(request, "movement_delete.html", context)

    movement.delete()

    messages.success(request, "Movimentação deletada com sucesso!")
    return redirect("movement_list")


@login_required
@admin_required
@require_http_methods(["GET", "POST"])
def report(request: HttpRequest) -> HttpResponse:
    """Cria um relatório de movimentações de acordo com um período específico.

    Args:
        request (HttpRequest): Objeto de requisição do django.

    GET:
        Renderiza a página de relatório.

    POST:
        Valida o período inserido:
            - Se válido, gera um relatório com base em um período específico.
            - Se inválido, retorna para a página de relatório com uma mensagem de erro.

    Returns:
        HttpRequest: Página de geração de relatório (data inválida).
        HttpsResponseRedirect: PDF do relatório (POST válido).
    """

    if request.method == "GET":
        return render(request, "report.html")

    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    if not (start_date and end_date):
        messages.error(request, "Insira uma data válida!")
        return redirect("report")

    start_dt = make_aware(datetime.strptime(str(start_date), "%Y-%m-%d"))
    end_dt = make_aware(datetime.strptime(str(end_date) + " 23:59:59", "%Y-%m-%d %H:%M:%S"))

    # prefetch_related para realizar apenas uma busca por todos os dados que atendem ao filtro
    movements = (
        Movement.objects.filter(date__range=(start_dt, end_dt))
        .prefetch_related("ingredients", "products")
        .order_by("-date")
    )

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Relatório de Movimentações", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, f"Período: {start_date} até {end_date}", ln=True, align="C")
    pdf.ln(5)

    total_in = 0
    total_out = 0

    for movement in movements:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{movement.get_type_display()} - {movement.date.strftime('%d/%m/%Y %H:%M')}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 8, f"Responsável: {movement.user}", ln=True)
        pdf.cell(
            0,
            8,
            f"Valor total: R$ {movement.value:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            ln=True,
        )

        pdf.ln(2)
        if movement.type == "in":
            total_in += movement.value
            pdf.set_font("Arial", "B", 10)
            pdf.cell(60, 8, "Nome", border=1)
            pdf.cell(40, 8, "Quantidade", border=1)
            pdf.cell(30, 8, "Medida", border=1)
            pdf.cell(40, 8, "Preço (R$)", border=1)
            pdf.ln()

            for ing in movement.ingredients.all():
                pdf.set_font("Arial", size=10)
                pdf.cell(60, 8, ing.name, border=1)
                pdf.cell(40, 8, f"{ing.quantity}", border=1)
                pdf.cell(30, 8, ing.get_measure_display(), border=1)
                pdf.cell(40, 8, f"{ing.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), border=1)
                pdf.ln()
        else:
            total_out += movement.value
            pdf.set_font("Arial", "B", 10)
            pdf.cell(60, 8, "Nome", border=1)
            pdf.cell(40, 8, "Quantidade", border=1)
            pdf.cell(40, 8, "Preço (R$)", border=1)
            pdf.ln()

            for prod in movement.products.all():
                pdf.set_font("Arial", size=10)
                pdf.cell(60, 8, prod.name, border=1)
                pdf.cell(40, 8, f"{prod.quantity}", border=1)
                pdf.cell(40, 8, f"{prod.price:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), border=1)
                pdf.ln()

        pdf.ln(5)  # espaço entre movimentos

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Resumo Financeiro", ln=True)

    pdf.set_font("Arial", size=10)
    pdf.cell(
        0, 8, f"Total de Entradas: R$ {total_in:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True
    )
    pdf.cell(
        0, 8, f"Total de Saídas:   R$ {total_out:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True
    )

    # Retornando o pdf como resposta HTTP
    response = HttpResponse(bytes(pdf.output(dest="S")), content_type="application/pdf")
    response["Content-Disposition"] = "inline; filename='relatorio.pdf'"
    return response
