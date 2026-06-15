from functools import wraps
import traceback
import sys
from datetime import datetime
import inspect

def _tratar_excecao(func, assinatura, e):
    """Tratamento comum de exceções para funções e métodos."""
    print(f"ERRO em {func.__name__}: {type(e).__name__}: {str(e)}")
    
    if isinstance(e, TypeError):
        print(f"   Dica: Verifique os tipos dos argumentos")
        print(f"   Argumentos recebidos: {assinatura}")
    elif isinstance(e, ValueError):
        print(f"   Dica: Valor inválido fornecido")
        print(f"   Valor problemático: {e.args[0] if e.args else 'N/A'}")
    elif isinstance(e, ZeroDivisionError):
        print(f"   Dica: Divisão por zero detectada")
    elif isinstance(e, KeyError):
        print(f"   Dica: Chave não encontrada no dicionário")
        print(f"   Chave procurada: {e.args[0] if e.args else 'N/A'}")
    elif isinstance(e, IndexError):
        print(f"   Dica: Índice fora dos limites")
    elif isinstance(e, AttributeError):
        print(f"   Dica: Objeto não possui o atributo/método solicitado")
    elif isinstance(e, RecursionError):
        print(f"   Dica: Possível recursão infinita ou muita profundidade")
    else:
        print(f"   Exceção não específica tratada genericamente")
    
    print(f"\n   Stack trace:")
    traceback.print_exc(limit=3, file=sys.stdout)
    print(f"{'='*60}")

def debug_oo(metodo):
    """Decorador genérico para depuração de métodos - SEM regras de negócio."""
    @wraps(metodo)
    def wrapper(self, *args, **kwargs):
        # Validação genérica (apenas para garantir que é método de instância)
        if not hasattr(self, '__class__'):
            raise TypeError(f"@debug_oo só pode ser usado em métodos de instância")
        
        # Prepara informações de depuração
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        assinatura = ", ".join(args_repr + kwargs_repr)
        
        # Captura estado anterior (genérico)
        estado_anterior = str(self) if hasattr(self, '__str__') else repr(self)
        
        # Cabeçalho de depuração
        print(f"\n{'='*70}")
        print(f"[{timestamp}] DEBUG: Chamando {self.__class__.__name__}.{metodo.__name__}({assinatura})")
        print(f"[{timestamp}] ESTADO INICIAL: {estado_anterior}")
        
        try:
            # EXECUTA O MÉTODO (as regras de negócio estão DENTRO do método)
            resultado = metodo(self, *args, **kwargs)
            
            # Captura estado posterior
            estado_atual = str(self) if hasattr(self, '__str__') else repr(self)
            
            # Log de sucesso (genérico)
            print(f"[{timestamp}] ESTADO FINAL: {estado_atual}")
            print(f"[{timestamp}] RETORNO: {resultado!r}")
            print(f"[{timestamp}] STATUS: SUCESSO")
            print(f"{'='*70}")
            
            return resultado
            
        except Exception as e:
            # Tratamento de exceções (genérico)
            print(f"[{timestamp}] STATUS: FALHA")
            _tratar_excecao(metodo, assinatura, e)
            raise
    
    return wrapper


# ==================== AS REGRAS DE NEGÓCIO FICAM NA CLASSE ====================

class ContaBancaria:
    """Classe que contém TODAS as regras de negócio."""
    
    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self.saldo = saldo_inicial
        self.historico = []
        self._limite_especial = 500  # Regra de negócio: limite de cheque especial
    
    def __str__(self):
        return f"Conta[{self.titular}]: R${self.saldo:.2f}"
    
    @debug_oo  # Apenas instrumentação, sem regras de negócio
    def depositar(self, valor):
        """REGRAS DE NEGÓCIO: valor positivo, atualiza saldo, registra histórico."""
        # Regra 1: Valor deve ser positivo
        if valor <= 0:
            raise ValueError("Depósito deve ser maior que zero")
        
        # Regra 2: Atualiza saldo
        self.saldo += valor
        
        # Regra 3: Registra no histórico
        self.historico.append(f"Depósito de R${valor:.2f}")
        
        # Regra 4: Bônus para depósitos grandes (regra de negócio específica)
        if valor > 10000:
            self.saldo += 50  # Bônus de R$50
            self.historico.append(f"Bônus de R$50.00 por depósito superior a R$10.000")
        
        return self.saldo
    
    @debug_oo
    def sacar(self, valor):
        """REGRAS DE NEGÓCIO: valor positivo, saldo suficiente (incluindo limite especial)."""
        # Regra 1: Valor deve ser positivo
        if valor <= 0:
            raise ValueError("Saque deve ser maior que zero")
        
        # Regra 2: Verifica saldo disponível (incluindo limite especial)
        saldo_disponivel = self.saldo + self._limite_especial
        if valor > saldo_disponivel:
            raise ValueError(f"Saldo insuficiente. Disponível: R${saldo_disponivel:.2f}")
        
        # Regra 3: Atualiza saldo (pode ficar negativo até o limite especial)
        self.saldo -= valor
        
        # Regra 4: Registra no histórico
        self.historico.append(f"Saque de R${valor:.2f}")
        
        # Regra 5: Aplica taxa se ficar negativo (regra de negócio)
        if self.saldo < 0:
            taxa = abs(self.saldo) * 0.01  # Taxa de 1% sobre valor negativo
            self.saldo -= taxa
            self.historico.append(f"Taxa de cheque especial: R${taxa:.2f}")
        
        return self.saldo
    
    @debug_oo
    def transferir(self, destino, valor):
        """REGRAS DE NEGÓCIO: conta destino válida, valor dentro do limite."""
        # Regra 1: Conta destino deve existir
        if not isinstance(destino, ContaBancaria):
            raise TypeError("Destino deve ser uma ContaBancaria")
        
        # Regra 2: Não transferir para si mesmo
        if destino is self:
            raise ValueError("Não é possível transferir para a mesma conta")
        
        # Regra 3: Valor positivo
        if valor <= 0:
            raise ValueError("Valor da transferência deve ser positivo")
        
        # Regra 4: Executa saque na origem (reutiliza regras de saque)
        self.sacar(valor)
        
        # Regra 5: Executa depósito no destino (reutiliza regras de depósito)
        destino.depositar(valor)
        
        # Regra 6: Registra no histórico
        self.historico.append(f"Transferência de R${valor:.2f} para {destino.titular}")
        
        return True
    
    @debug_oo
    def extrato(self):
        """REGRAS DE NEGÓCIO: Formatação do extrato."""
        print(f"\n--- EXTRATO BANCÁRIO - {self.titular} ---")
        print(f"Saldo atual: R${self.saldo:.2f}")
        print(f"Limite especial: R${self._limite_especial:.2f}")
        print(f"Saldo total disponível: R${self.saldo + self._limite_especial:.2f}")
        print("\nHISTÓRICO DE TRANSAÇÕES:")
        for i, transacao in enumerate(self.historico[-10:], 1):  # Últimas 10
            print(f"  {i}. {transacao}")
        return self.historico


class Pedido:
    """Outra classe com regras de negócio completamente diferentes."""
    
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = []
        self.desconto = 0
        self.status = "aberto"
    
    def __str__(self):
        return f"Pedido[{self.cliente}]: {len(self.itens)} itens, total R${self.total():.2f}, {self.status}"
    
    @debug_oo
    def adicionar_item(self, produto, preco, quantidade=1):
        """REGRAS DE NEGÓCIO: valida produto, preço e quantidade."""
        if not produto or not isinstance(produto, str):
            raise ValueError("Produto inválido")
        if preco <= 0:
            raise ValueError("Preço deve ser positivo")
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        if self.status != "aberto":
            raise ValueError(f"Pedido está {self.status}, não é possível adicionar itens")
        
        self.itens.append({
            'produto': produto,
            'preco': preco,
            'quantidade': quantidade,
            'subtotal': preco * quantidade
        })
        return len(self.itens)
    
    @debug_oo
    def aplicar_desconto(self, percentual):
        """REGRAS DE NEGÓCIO: percentual entre 0 e 50, apenas para pedidos abertos."""
        if not 0 <= percentual <= 50:
            raise ValueError("Desconto deve ser entre 0% e 50%")
        if self.status != "aberto":
            raise ValueError(f"Pedido está {self.status}, não é possível aplicar desconto")
        
        self.desconto = percentual
        return self.desconto
    
    def total(self):
        """REGRAS DE NEGÓCIO: calcula total com desconto."""
        subtotal = sum(item['subtotal'] for item in self.itens)
        desconto_valor = subtotal * (self.desconto / 100)
        return subtotal - desconto_valor
    
    @debug_oo
    def finalizar(self):
        """REGRAS DE NEGÓCIO: pedido só pode ser finalizado se tiver itens."""
        if len(self.itens) == 0:
            raise ValueError("Não é possível finalizar pedido sem itens")
        if self.status != "aberto":
            raise ValueError(f"Pedido já está {self.status}")
        
        self.status = "fechado"
        return self.status


# ==================== DEMONSTRAÇÃO ====================

print("=" * 80)
print("DEMONSTRAÇÃO: debug_oo é GENÉRICO, regras de negócio ficam nas CLASSES")
print("=" * 80)

print("\n[CENÁRIO 1] Conta Bancária com regras de negócio específicas")
conta = ContaBancaria("João", 1000)

print("\n--- Depósito normal ---")
conta.depositar(500)

print("\n--- Depósito grande (regra de bônus) ---")
conta.depositar(15000)

print("\n--- Saque com limite especial ---")
conta.sacar(2000)  # Saldo: 16500 - 2000 = 14500

print("\n--- Saque que ativa taxa de cheque especial ---")
conta.sacar(15000)  # Saldo fica negativo, aplica taxa

print("\n--- Tentativa de saque inválido (regra de negócio) ---")
try:
    conta.sacar(-50)
except Exception as e:
    print(f"  Erro capturado (esperado): {e}")

print("\n--- Transferência entre contas ---")
conta2 = ContaBancaria("Maria", 500)
conta.transferir(conta2, 1000)

print("\n--- Extrato final ---")
conta.extrato()

print("\n[CENÁRIO 2] Pedido com regras de negócio completamente diferentes")
pedido = Pedido("Carlos")

print("\n--- Adicionando itens ---")
pedido.adicionar_item("Notebook", 3500, 1)
pedido.adicionar_item("Mouse", 150, 2)
pedido.adicionar_item("Teclado", 250, 1)

print("\n--- Aplicando desconto (regra: máximo 50%) ---")
pedido.aplicar_desconto(10)

print(f"Total do pedido com 10% de desconto: R${pedido.total():.2f}")

print("\n--- Tentativa de desconto inválido ---")
try:
    pedido.aplicar_desconto(75)  # Acima do limite
except Exception as e:
    print(f"  Erro capturado (esperado): {e}")

print("\n--- Finalizando pedido ---")
pedido.finalizar()

print("\n--- Tentativa de adicionar item ao pedido fechado ---")
try:
    pedido.adicionar_item("Monitor", 1200, 1)
except Exception as e:
    print(f"  Erro capturado (esperado): {e}")

print("\n" + "=" * 80)
print("CONCLUSÃO: debug_oo é 100% genérico e reutilizável")
print("Todas as regras de negócio estão encapsuladas nas classes")
print("=" * 80)
