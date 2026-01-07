from flask import Flask, render_template_string, request, session, redirect, url_for
import secrets
from urllib.parse import quote

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# --- LISTA DE PRODUTOS ---
PRODUTOS = [
    {'id': 1, 'nome': 'Lâmpada LED 12W', 'preco': 15.90, 'categoria': 'Iluminação', 'img': '💡'},
    {'id': 2, 'nome': 'Tomada 10A Padrão Novo', 'preco': 8.50, 'categoria': 'Tomadas', 'img': '🔌'},
    {'id': 3, 'nome': 'Disjuntor 20A Bifásico', 'preco': 35.00, 'categoria': 'Proteção', 'img': '⚡'},
    {'id': 4, 'nome': 'Fio Elétrico 2.5mm 100m', 'preco': 89.90, 'categoria': 'Cabos', 'img': '🔗'},
    {'id': 5, 'nome': 'Interruptor Simples', 'preco': 6.90, 'categoria': 'Interruptores', 'img': '💠'},
    {'id': 6, 'nome': 'Fita LED 5m Branco Frio', 'preco': 45.00, 'categoria': 'Iluminação', 'img': '✨'},
    {'id': 7, 'nome': 'Quadro de Distribuição 12D', 'preco': 125.00, 'categoria': 'Proteção', 'img': '📦'},
    {'id': 8, 'nome': 'Luminária Sobrepor LED 18W', 'preco': 68.00, 'categoria': 'Iluminação', 'img': '🔆'},
]

# --- ESTRUTURA BASE DO SITE (VISUAL CLEAN/BRANCO) ---
HTML_BASE = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nova Eletro - Soluções Elétricas</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        /* CORPO DO SITE: Fundo Branco e Texto Escuro */
        body { 
            font-family: 'Segoe UI', sans-serif; 
            background-color: #ffffff; 
            color: #333333; 
            min-height: 100vh; 
            display: flex; 
            flex-direction: column; 
        }
        
        /* CABEÇALHO: Preto e Amarelo */
        .header { 
            background: #000000; 
            border-bottom: 4px solid #ffd700; 
            padding: 1.5rem; 
            position: sticky; 
            top: 0; 
            z-index: 100; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
        }
        .header-content { 
            max-width: 1200px; 
            margin: 0 auto; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
        }
        .logo { display: flex; align-items: center; gap: 1rem; }
        .logo-icon { font-size: 2.5rem; color: #ffd700; }
        .logo h1 { color: #ffd700; font-size: 1.8rem; text-transform: uppercase; letter-spacing: 1px; margin: 0; }
        .logo p { color: #cccccc; font-size: 0.8rem; letter-spacing: 0.5px; margin: 0; }
        
        .cart-btn { 
            background: #ffd700; 
            color: #000; 
            padding: 0.8rem 1.5rem; 
            border: none; 
            border-radius: 8px; 
            font-weight: bold; 
            cursor: pointer; 
            display: flex; 
            align-items: center; 
            gap: 0.5rem; 
            text-decoration: none; 
            transition: all 0.3s; 
        }
        .cart-btn:hover { background: #ffed4e; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        
        /* CONTAINER PRINCIPAL */
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; flex: 1; width: 100%; }
        
        .page-title { 
            color: #000; 
            font-size: 2.2rem; 
            margin-bottom: 2rem; 
            display: flex; 
            align-items: center; 
            gap: 1rem; 
            border-bottom: 2px solid #ffd700;
            padding-bottom: 0.5rem;
            width: fit-content;
        }
        
        /* GRID DE PRODUTOS (Cartões Claros) */
        .produtos-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 3rem; }
        
        .produto-card { 
            background: #ffffff; 
            border-radius: 12px; 
            overflow: hidden; 
            border: 1px solid #e0e0e0; 
            transition: all 0.3s; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .produto-card:hover { 
            border-color: #ffd700; 
            transform: translateY(-5px); 
            box-shadow: 0 8px 20px rgba(0,0,0,0.1); 
        }
        
        .produto-img { 
            background: linear-gradient(135deg, #ffd700 0%, #fff0b3 100%); 
            height: 180px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 5rem; 
        }
        
        .produto-info { padding: 1.5rem; }
        .produto-categoria { color: #666; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; margin-bottom: 0.5rem; }
        .produto-nome { font-size: 1.2rem; margin: 0.5rem 0; color: #000; font-weight: 600; }
        .produto-preco { color: #000; font-size: 1.6rem; font-weight: bold; margin-bottom: 1rem; }
        
        .btn-adicionar { 
            width: 100%; 
            background: #000; 
            color: #ffd700; 
            border: none; 
            padding: 0.8rem; 
            border-radius: 6px; 
            font-weight: bold; 
            cursor: pointer; 
            transition: all 0.3s; 
        }
        .btn-adicionar:hover { background: #333; }

        /* RODAPÉ: Preto e Amarelo */
        .footer { background: #0a0a0a; border-top: 4px solid #ffd700; padding: 3rem 1rem; margin-top: auto; text-align: center; color: #fff; }
        .footer-logo { font-size: 1.5rem; color: #ffd700; font-weight: bold; margin-bottom: 0.5rem; }
        .footer-links { display: flex; gap: 2rem; flex-wrap: wrap; justify-content: center; margin-top: 1.5rem; }
        .footer-link { color: #fff; text-decoration: none; font-size: 1rem; display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; border: 1px solid #333; border-radius: 50px; transition: all 0.3s; }
        .footer-link:hover { border-color: #ffd700; color: #ffd700; background: rgba(255, 215, 0, 0.1); }
        .footer-phone { font-size: 1.1rem; color: #ccc; }
        .copyright { margin-top: 2rem; color: #555; font-size: 0.8rem; }

        /* CHECKOUT E CARRINHO (Ajustado para Fundo Claro) */
        .checkout-container { display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; }
        
        .form-section, .carrinho-section { 
            background: #f8f9fa; 
            padding: 2rem; 
            border-radius: 12px; 
            border: 1px solid #ddd; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .carrinho-section { border-top: 4px solid #ffd700; height: fit-content; position: sticky; top: 120px; }
        
        .form-title { color: #000; font-size: 1.5rem; margin-bottom: 1.5rem; border-bottom: 1px solid #ddd; padding-bottom: 0.5rem; }
        
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; color: #444; margin-bottom: 0.4rem; font-weight: bold; font-size: 0.9rem; }
        .form-group input { 
            width: 100%; 
            padding: 0.8rem; 
            background: #fff; 
            border: 1px solid #ccc; 
            border-radius: 6px; 
            color: #000; 
            font-size: 1rem; 
        }
        .form-group input:focus { outline: none; border-color: #ffd700; box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.2); }
        
        .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
        
        .carrinho-item { background: #fff; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid #eee; display: flex; flex-direction: column; gap: 0.5rem; }
        .carrinho-item-header { display: flex; justify-content: space-between; font-weight: bold; color: #000; }
        .carrinho-item-footer { display: flex; justify-content: space-between; align-items: center; }
        
        .quantidade-controls { display: flex; gap: 0.5rem; align-items: center; }
        .btn-qty { background: #e0e0e0; color: #000; border: none; width: 25px; height: 25px; border-radius: 4px; cursor: pointer; font-weight: bold; }
        .btn-qty:hover { background: #d0d0d0; }
        
        .btn-remover { background: #ffeded; color: #dc3545; border: 1px solid #ffcccc; padding: 0.2rem 0.6rem; border-radius: 4px; cursor: pointer; font-size: 0.8rem; }
        .btn-remover:hover { background: #ffcccc; }
        
        .total-section { border-top: 2px solid #ddd; padding-top: 1rem; margin-top: 1rem; }
        .total-row { display: flex; justify-content: space-between; font-size: 1.3rem; font-weight: bold; color: #000; }
        .total-valor { color: #000; }
        
        .btn-finalizar { 
            width: 100%; 
            background: #25d366; /* Verde WhatsApp */
            color: #fff; 
            border: none; 
            padding: 1rem; 
            border-radius: 8px; 
            font-weight: bold; 
            font-size: 1.1rem; 
            cursor: pointer; 
            margin-top: 1rem; 
            transition: all 0.3s; 
            box-shadow: 0 4px 6px rgba(37, 211, 102, 0.2);
        }
        .btn-finalizar:hover { background: #128c7e; transform: translateY(-2px); }
        
        .btn-voltar { display: inline-block; color: #000; text-decoration: none; margin-bottom: 1.5rem; font-weight: bold; }
        .btn-voltar:hover { color: #666; }
        
        .carrinho-vazio { text-align: center; color: #666; padding: 2rem; }
        .alert { background: #f8d7da; color: #721c24; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid #f5c6cb; }

        @media (max-width: 768px) {
            .checkout-container { grid-template-columns: 1fr; }
            .carrinho-section { position: static; }
            .form-row { grid-template-columns: 1fr; }
            .footer-links { flex-direction: column; width: 100%; }
            .footer-link { justify-content: center; }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <div class="logo-icon">⚡</div>
                <div>
                    <h1>NOVA ELETRO</h1>
                    <p>Materiais Elétricos & Soluções</p>
                </div>
            </div>
            <a href="{{ url_for('checkout') }}" class="cart-btn">
                🛒 <span id="cart-count">{{ carrinho|length }}</span> itens
            </a>
        </div>
    </div>
    
    <div class="container">
        CONTENT_PLACEHOLDER
    </div>

    <footer class="footer">
        <div class="footer-content">
            <div class="footer-logo">⚡ NOVA ELETRO</div>
            
            <p class="footer-phone">📞 Atendimento: (14) 99999-9999</p>
            
            <div class="footer-links">
                <a href="https://wa.me/5514999999999" target="_blank" class="footer-link">
                    📱 Falar no WhatsApp
                </a>
                
                <a href="https://instagram.com/novaeletro" target="_blank" class="footer-link">
                    📷 Siga no Instagram
                </a>
            </div>
            
            <div class="copyright">
                © 2025 Nova Eletro. Todos os direitos reservados.
            </div>
        </div>
    </footer>

</body>
</html>
'''

# --- CONTEÚDO DA PÁGINA DE PRODUTOS ---
PRODUTOS_CONTENT = '''
    <h2 class="page-title">⚡ Destaques da Loja</h2>
    <div class="produtos-grid">
        {% for produto in produtos %}
        <div class="produto-card">
            <div class="produto-img">{{ produto.img }}</div>
            <div class="produto-info">
                <div class="produto-categoria">{{ produto.categoria }}</div>
                <h3 class="produto-nome">{{ produto.nome }}</h3>
                <div class="produto-preco">R$ {{ "%.2f"|format(produto.preco) }}</div>
                <form method="POST" action="{{ url_for('adicionar_carrinho', produto_id=produto.id) }}">
                    <button type="submit" class="btn-adicionar">➕ Adicionar ao Carrinho</button>
                </form>
            </div>
        </div>
        {% endfor %}
    </div>
'''

# --- CONTEÚDO DA PÁGINA DE CHECKOUT ---
CHECKOUT_CONTENT = '''
    <a href="{{ url_for('index') }}" class="btn-voltar">← Voltar para a Loja</a>
    
    {% if erro %}
    <div class="alert">{{ erro }}</div>
    {% endif %}
    
    <div class="checkout-container">
        <div class="form-section">
            <h2 class="form-title">Dados para Entrega</h2>
            <form method="POST" action="{{ url_for('finalizar_pedido') }}" id="checkout-form">
                <div class="form-group">
                    <label>Nome Completo *</label>
                    <input type="text" name="nome" required placeholder="Ex: João da Silva">
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>CPF *</label>
                        <input type="text" name="cpf" required placeholder="000.000.000-00" maxlength="14">
                    </div>
                    <div class="form-group">
                        <label>Telefone *</label>
                        <input type="text" name="telefone" required placeholder="(14) 99999-9999" maxlength="15">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>Endereço *</label>
                        <input type="text" name="endereco" required placeholder="Rua, Avenida...">
                    </div>
                    <div class="form-group">
                        <label>Número *</label>
                        <input type="text" name="numero" required placeholder="123">
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Bairro *</label>
                    <input type="text" name="bairro" required placeholder="Centro">
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>Cidade *</label>
                        <input type="text" name="cidade" required placeholder="Bauru">
                    </div>
                    <div class="form-group">
                        <label>Estado *</label>
                        <input type="text" name="estado" required placeholder="SP" maxlength="2">
                    </div>
                </div>
            </form>
        </div>
        
        <div class="carrinho-section">
            <h2 class="form-title">Resumo do Pedido</h2>
            
            {% if carrinho|length == 0 %}
                <div class="carrinho-vazio">Seu carrinho está vazio 🛒</div>
            {% else %}
                {% for item in carrinho %}
                <div class="carrinho-item">
                    <div class="carrinho-item-header">
                        <span class="carrinho-item-nome">{{ item.nome }}</span>
                        <form method="POST" action="{{ url_for('remover_carrinho', produto_id=item.id) }}" style="display: inline;">
                            <button type="submit" class="btn-remover">🗑️</button>
                        </form>
                    </div>
                    <div class="carrinho-item-footer">
                        <div class="quantidade-controls">
                            <form method="POST" action="{{ url_for('alterar_quantidade', produto_id=item.id, acao='diminuir') }}" style="display: inline;">
                                <button type="submit" class="btn-qty">-</button>
                            </form>
                            <span style="font-weight: bold; color: #000;">{{ item.quantidade }}</span>
                            <form method="POST" action="{{ url_for('alterar_quantidade', produto_id=item.id, acao='aumentar') }}" style="display: inline;">
                                <button type="submit" class="btn-qty">+</button>
                            </form>
                        </div>
                        <span style="color: #000; font-weight: bold;">R$ {{ "%.2f"|format(item.preco * item.quantidade) }}</span>
                    </div>
                </div>
                {% endfor %}
                
                <div class="total-section">
                    <div class="total-row">
                        <span>TOTAL:</span>
                        <span class="total-valor">R$ {{ "%.2f"|format(total) }}</span>
                    </div>
                </div>
                
                <button type="button" class="btn-finalizar" onclick="document.getElementById('checkout-form').submit()">
                    💬 Finalizar no WhatsApp
                </button>
            {% endif %}
        </div>
    </div>
'''

# --- FUNÇÕES E ROTAS ---

def calcular_total():
    total = 0
    carrinho = session.get('carrinho', [])
    for item in carrinho:
        total += item['preco'] * item['quantidade']
    return total

@app.route('/')
def index():
    carrinho = session.get('carrinho', [])
    html = HTML_BASE.replace('CONTENT_PLACEHOLDER', PRODUTOS_CONTENT)
    return render_template_string(html, produtos=PRODUTOS, carrinho=carrinho)

@app.route('/adicionar/<int:produto_id>', methods=['POST'])
def adicionar_carrinho(produto_id):
    produto = next((p for p in PRODUTOS if p['id'] == produto_id), None)
    if produto:
        carrinho = session.get('carrinho', [])
        item_existente = next((item for item in carrinho if item['id'] == produto_id), None)
        
        if item_existente:
            item_existente['quantidade'] += 1
        else:
            carrinho.append({
                'id': produto['id'],
                'nome': produto['nome'],
                'preco': produto['preco'],
                'quantidade': 1
            })
        session['carrinho'] = carrinho
    return redirect(url_for('index'))

@app.route('/checkout')
def checkout():
    carrinho = session.get('carrinho', [])
    total = calcular_total()
    erro = request.args.get('erro')
    html = HTML_BASE.replace('CONTENT_PLACEHOLDER', CHECKOUT_CONTENT)
    return render_template_string(html, carrinho=carrinho, total=total, erro=erro)

@app.route('/remover/<int:produto_id>', methods=['POST'])
def remover_carrinho(produto_id):
    carrinho = session.get('carrinho', [])
    carrinho = [item for item in carrinho if item['id'] != produto_id]
    session['carrinho'] = carrinho
    return redirect(url_for('checkout'))

@app.route('/quantidade/<int:produto_id>/<acao>', methods=['POST'])
def alterar_quantidade(produto_id, acao):
    carrinho = session.get('carrinho', [])
    for item in carrinho:
        if item['id'] == produto_id:
            if acao == 'aumentar':
                item['quantidade'] += 1
            elif acao == 'diminuir':
                item['quantidade'] -= 1
                if item['quantidade'] <= 0:
                    carrinho.remove(item)
            break
    session['carrinho'] = carrinho
    return redirect(url_for('checkout'))

@app.route('/finalizar', methods=['POST'])
def finalizar_pedido():
    nome = request.form.get('nome', '').strip()
    cpf = request.form.get('cpf', '').strip()
    telefone = request.form.get('telefone', '').strip()
    endereco = request.form.get('endereco', '').strip()
    numero = request.form.get('numero', '').strip()
    bairro = request.form.get('bairro', '').strip()
    cidade = request.form.get('cidade', '').strip()
    estado = request.form.get('estado', '').strip()
    
    carrinho = session.get('carrinho', [])
    
    if not all([nome, cpf, telefone, endereco, numero, cidade, estado]):
        return redirect(url_for('checkout', erro='Preencha todos os campos para a entrega!'))
    
    if not carrinho:
        return redirect(url_for('checkout', erro='Seu carrinho está vazio!'))
    
    mensagem = f"*PEDIDO - NOVA ELETRO*\n\n"
    mensagem += f"*CLIENTE:*\nNome: {nome}\nCPF: {cpf}\nTel: {telefone}\n"
    mensagem += f"Local: {endereco}, {numero} - {bairro}\n{cidade}/{estado}\n\n"
    mensagem += f"*ITENS:*\n"
    
    for item in carrinho:
        valor_item = item['preco'] * item['quantidade']
        mensagem += f"{item['quantidade']}x {item['nome']} (R$ {valor_item:.2f})\n"
    
    total = calcular_total()
    mensagem += f"\n*TOTAL DO PEDIDO: R$ {total:.2f}*"
    
    # --- COLOQUE O NÚMERO DA LOJA AQUI ---
    numero_whatsapp_loja = '5514999999999'
    
    mensagem_encoded = quote(mensagem)
    url_whatsapp = f"https://wa.me/{numero_whatsapp_loja}?text={mensagem_encoded}"
    
    session['carrinho'] = []
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Enviando Pedido...</title>
        <meta charset="UTF-8">
        <style>
            body {{ background: #ffffff; color: #333; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
            .container {{ text-align: center; padding: 3rem; border: 2px solid #ffd700; border-radius: 12px; background: #f9f9f9; }}
            h1 {{ color: #000; }}
            a {{ color: #25d366; text-decoration: none; font-weight: bold; font-size: 1.2rem; }}
            a:hover {{ text-decoration: underline; }}
        </style>
        <script>
            window.onload = function() {{
                window.open("{url_whatsapp}", "_blank");
                setTimeout(function() {{ window.location.href = "/"; }}, 2000);
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <h1>✅ Pedido Gerado!</h1>
            <p>Estamos abrindo o WhatsApp...</p>
            <a href="{url_whatsapp}" target="_blank">Clique aqui se não abrir</a>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)