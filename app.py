from flask import Flask, render_template, request

app = Flask(__name__)

TAXA_SHOPEE_PERCENTUAL = 14
TAXA_FRETE_GRATIS = 6
TAXA_FIXA = 4


# =====================
# CONTADOR DE ACESSOS
# =====================
def contar_acesso():

    if request.args.get("teste") == "1":
        return

    try:
        with open("contador.txt", "r") as f:
            total = int(f.read())
    except:
        total = 0

    total += 1

    with open("contador.txt", "w") as f:
        f.write(str(total))


# =====================
# HOME
# =====================
@app.route("/")
def home():
    # contar_acesso()  # desativado no Railway
    return render_template("home.html")


# =====================
# analise-vendas-shopee
# =====================
@app.route("/analise-vendas-shopee")
def analise_vendas_shopee():
    return render_template("analise_vendas_shopee.html")


# =====================
# CALCULADORA
# =====================
@app.route("/calculadorashopee", methods=["GET", "POST"])
def calculadora():

    # contar_acesso()  # desativado no Railway

    resultado1 = None
    resultado2 = None
    classe_lucro = ""
    status_texto = ""

    if request.method == "POST":

        modo = request.form.get("modo")

        # =====================
        # MODO 1
        # =====================
        if modo == "modo1":

            custo = float(request.form.get("custo"))
            preco_venda = float(request.form.get("preco_venda"))
            frete_gratis = request.form.get("frete_gratis")

            taxa_percentual = preco_venda * (TAXA_SHOPEE_PERCENTUAL / 100)

            taxa_frete = 0
            taxa_frete_num = 0

            if frete_gratis:
                taxa_frete = preco_venda * (TAXA_FRETE_GRATIS / 100)
                taxa_frete_num = TAXA_FRETE_GRATIS

            taxa_total = taxa_percentual + taxa_frete + TAXA_FIXA
            valor_recebido = preco_venda - taxa_total
            lucro = valor_recebido - custo

            margem_real = (lucro / preco_venda) * 100 if preco_venda > 0 else 0

            if margem_real > 20:
                classe_lucro = "verde"
                status_texto = "Lucro bom"
            elif margem_real >= 0:
                classe_lucro = "amarelo"
                status_texto = "Lucro médio"
            else:
                classe_lucro = "vermelho"
                status_texto = "Prejuízo"

            resultado1 = {
                "custo": f"{custo:.2f}",
                "preco_venda": f"{preco_venda:.2f}",
                "taxa_percentual": f"{taxa_percentual:.2f}",
                "taxa_frete": f"{taxa_frete:.2f}",
                "taxa_frete_num": taxa_frete_num,
                "taxa_fixa": f"{TAXA_FIXA:.2f}",
                "lucro": f"{lucro:.2f}",
                "margem_real": f"{margem_real:.2f}"
            }

        # =====================
        # MODO 2
        # =====================
        if modo == "modo2":

            custo = float(request.form.get("custo2"))

            margem_desejada = float(
                request.form.get("margem_desejada").replace(",", ".")
            )

            frete_gratis = request.form.get("frete_gratis2")

            taxa_total_percent = TAXA_SHOPEE_PERCENTUAL / 100

            taxa_frete_num = 0
            if frete_gratis:
                taxa_total_percent += TAXA_FRETE_GRATIS / 100
                taxa_frete_num = TAXA_FRETE_GRATIS

            preco_ideal = (custo + TAXA_FIXA) / (
                1 - taxa_total_percent - (margem_desejada / 100)
            )

            taxa_shopee = preco_ideal * (TAXA_SHOPEE_PERCENTUAL / 100)
            taxa_frete = preco_ideal * (TAXA_FRETE_GRATIS / 100) if frete_gratis else 0

            taxa_total = taxa_shopee + taxa_frete + TAXA_FIXA
            valor_recebido = preco_ideal - taxa_total
            lucro = valor_recebido - custo

            margem_real = (lucro / preco_ideal) * 100

            resultado2 = {
                "custo": f"{custo:.2f}",
                "preco_ideal": f"{preco_ideal:.2f}",
                "taxa_shopee": f"{taxa_shopee:.2f}",
                "taxa_frete": f"{taxa_frete:.2f}",
                "taxa_frete_num": taxa_frete_num,
                "taxa_fixa": f"{TAXA_FIXA:.2f}",
                "valor_recebido": f"{valor_recebido:.2f}",
                "lucro": f"{lucro:.2f}",
                "margem_real": f"{margem_real:.2f}"
            }

    return render_template(
        "index.html",
        resultado1=resultado1,
        resultado2=resultado2,
        classe_lucro=classe_lucro,
        status_texto=status_texto
    )


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)