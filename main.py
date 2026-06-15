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
        print(f"   Assinatura esperada: {func.__name__}{func.__signature__ if hasattr(func, '__signature__') else '(...)'}")
    elif isinstance(e, ValueError):
        print(f"   Dica: Valor inválido fornecido")
        print(f"   Valor problemático: {e.args[0] if e.args else 'N/A'}")
    elif isinstance(e, ZeroDivisionError):
        print(f"   Dica: Divisão por zero detectada")
        print(f"   Verifique se o divisor não é zero")
    elif isinstance(e, KeyError):
        print(f"   Dica: Chave não encontrada no dicionário")
        print(f"   Chave procurada: {e.args[0] if e.args else 'N/A'}")
    elif isinstance(e, IndexError):
        print(f"   Dica: Índice fora dos limites")
        print(f"   Índice problemático: {e.args[0] if e.args else 'N/A'}")
    elif isinstance(e, AttributeError):
        print(f"   Dica: Objeto não possui o atributo/método solicitado")
        print(f"   Objeto: {repr(e.args[0]) if len(e.args) > 0 else 'N/A'}")
        print(f"   Atributo: {e.args[1] if len(e.args) > 1 else 'N/A'}")
    elif isinstance(e, FileNotFoundError):
        print(f"   Dica: Arquivo ou diretório não encontrado")
        print(f"   Caminho: {e.filename if hasattr(e, 'filename') else 'N/A'}")
    elif isinstance(e, PermissionError):
        print(f"   Dica: Permissão negada para acessar o recurso")
        print(f"   Recurso: {e.filename if hasattr(e, 'filename') else 'N/A'}")
    elif isinstance(e, RecursionError):
        print(f"   Dica: Possível recursão infinita ou muita profundidade")
        print(f"   Limite de recursão atual: {sys.getrecursionlimit()}")
    else:
        print(f"   Exceção não específica tratada genericamente")
    
    print(f"\n   Stack trace:")
    traceback.print_exc(limit=3, file=sys.stdout)
    print(f"{'='*60}")

def debug_funcao(func):
    """Mostra entrada, saída e tratamento detalhado de exceções da função."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Obtém a assinatura da função
        sig = inspect.signature(func)
        
        # Formata os argumentos recebidos
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        assinatura_recebida = ", ".join(args_repr + kwargs_repr)
        
        # Cabeçalho com nome da função e assinatura esperada
        print(f"\n{'='*60}")
        print(f"FUNÇÃO: {func.__name__}")
        print(f"ASSINATURA ESPERADA: {func.__name__}{sig}")
        print(f"ASSINATURA RECEBIDA: {func.__name__}({assinatura_recebida})")
        print(f"DOCSTRING: {func.__doc__.strip() if func.__doc__ else 'Sem documentação'}")
        print(f"{'-'*60}")
        
        try:
            resultado = func(*args, **kwargs)
            print(f"RETORNO: {resultado!r}")
            print(f"STATUS: SUCESSO")
            print(f"{'='*60}")
            return resultado
        except Exception as e:
            print(f"STATUS: FALHA")
            _tratar_excecao(func, assinatura_recebida, e)
            raise
    return wrapper

def debug_oo(metodo):
    @wraps(metodo)
    def wrapper(*args, **kwargs):
        if not args or not hasattr(args[0], '__class__'):
            raise TypeError(
                f"@debug_oo só pode ser usado em métodos de instância. "
                f"'{metodo.__name__}' não é um método de objeto."
            )
        
        obj = args[0]
        obj_str = str(obj)
        if len(obj_str) > 80:
            obj_str = obj_str[:77] + "..."
        
        args_repr = [repr(a) for a in args[1:]]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        assinatura = ", ".join(args_repr + kwargs_repr)
        
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        print(f"\n{'='*70}")
        print(f"   [{timestamp}] OBJETO: {obj.__class__.__name__}")
        print(f"   [{timestamp}] ESTADO: {obj_str}")
        print(f"   [{timestamp}] MÉTODO: {metodo.__name__}({assinatura})")
        
        estado_anterior = obj_str
        
        try:
            resultado = metodo(*args, **kwargs)
            
            estado_atual = str(obj)
            if len(estado_atual) > 80:
                estado_atual = estado_atual[:77] + "..."
            
            if estado_anterior != estado_atual:
                print(f"   [{timestamp}]    METODO EXECUTADO COM SUCESSO")
                print(f"   [{timestamp}]    NOVO ESTADO: {estado_atual}")
                if resultado is not None:
                    print(f"   [{timestamp}]    RETORNO: {resultado!r}")
            else:
                print(f"   [{timestamp}]    EXECUTADO -> retorno: {resultado!r}")
            
            print(f"{'='*70}")
            return resultado
        except Exception as e:
            _tratar_excecao(metodo, assinatura, e)
            raise
    return wrapper


# ==================== TESTES ====================

print("=" * 80)
print("TESTES DO DECORATOR debug_funcao")
print("=" * 80)

print("\n[Teste 1] Funcao normal com assinatura clara")
@debug_funcao
def soma(a, b, multiplicador=1):
    """Soma dois números e multiplica o resultado."""
    return (a + b) * multiplicador

try:
    resultado = soma(3, 5, multiplicador=2)
    print(f"Resultado final: {resultado}")
except:
    pass

print("\n[Teste 2] Funcao com multiplos parametros")
@debug_funcao
def criar_usuario(nome, idade, email=None, ativo=True):
    """Cria um novo usuário no sistema."""
    return {
        'nome': nome,
        'idade': idade,
        'email': email,
        'ativo': ativo
    }

try:
    usuario = criar_usuario("João", 30, email="joao@email.com", ativo=True)
    print(f"Usuario criado: {usuario['nome']}")
except:
    pass

print("\n[Teste 3] TypeError (argumento invalido)")
@debug_funcao
def dividir(a, b):
    """Divide a por b."""
    return a / b

try:
    dividir(10, "2")
except Exception as e:
    print(f"Excecao capturada: {type(e).__name__}")

print("\n[Teste 4] ZeroDivisionError")
try:
    dividir(10, 0)
except Exception as e:
    print(f"Excecao capturada: {type(e).__name__}")

print("\n[Teste 5] Funcao sem documentacao")
@debug_funcao
def sem_doc(x, y):
    return x * y

try:
    sem_doc(4, 5)
except:
    pass

print("\n[Teste 6] ValueError")
@debug_funcao
def raiz_quadrada(numero):
    """Calcula a raiz quadrada de um número."""
    if numero < 0:
        raise ValueError(f"Não é possível calcular raiz de {numero}")
    return numero ** 0.5

try:
    raiz_quadrada(-9)
except Exception as e:
    print(f"Excecao capturada: {type(e).__name__}")


# ==================== TESTES DO debug_oo ====================

print("\n" + "=" * 80)
print("TESTES DO DECORATOR debug_oo")
print("=" * 80)

print("\n[Teste 7] Classe com metodos")
class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.saldo = 0
    
    def __str__(self):
        return f"Banco {self.nome}: R${self.saldo:.2f}"
    
    @debug_oo
    def depositar(self, valor):
        """Deposita valor na conta."""
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        self.saldo += valor
        return self.saldo
    
    @debug_oo
    def sacar(self, valor):
        """Saca valor da conta."""
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= valor
        return self.saldo

banco = Banco("Meu Banco")
print("\n--- Operacoes com sucesso ---")
banco.depositar(1000)
banco.sacar(300)

print("\n--- Operacoes com erro ---")
try:
    banco.depositar(-50)
except Exception as e:
    print(f"Erro esperado: {type(e).__name__}")

try:
    banco.sacar(10000)
except Exception as e:
    print(f"Erro esperado: {type(e).__name__}")

print("\n[Teste 8] Metodo com retorno complexo")
class Processador:
    def __init__(self):
        self.dados = []
    
    def __str__(self):
        return f"Processador ({len(self.dados)} itens)"
    
    @debug_oo
    def processar_lista(self, lista, multiplicador=2):
        """Processa uma lista multiplicando cada elemento."""
        self.dados = [x * multiplicador for x in lista]
        return self.dados

proc = Processador()
resultado = proc.processar_lista([1, 2, 3, 4], multiplicador=3)
print(f"Resultado processado: {resultado}")

print("\n" + "=" * 80)
print("TODOS OS TESTES CONCLUIDOS")
print("=" * 80)
