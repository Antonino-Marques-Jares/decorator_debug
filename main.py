from functools import wraps
import traceback
import sys
from datetime import datetime
import inspect

def _tratar_excecao(func, assinatura, e):
    """Tratamento comum de exceções para funções e métodos."""
    import sys
    import traceback
    
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
    elif isinstance(e, ImportError):
        print(f"   Dica: Falha ao importar módulo/pacote")
        if hasattr(e, 'name') and e.name:
            print(f"   Módulo não encontrado: {e.name}")
        if hasattr(e, 'path') and e.path:
            print(f"   Caminho de busca: {e.path}")
            print(f"   Verifique se o módulo está instalado (pip install) e no PYTHONPATH")
    elif isinstance(e, ModuleNotFoundError):  # Subclasse de ImportError
        print(f"   Dica: Módulo específico não encontrado")
        print(f"   Nome do módulo: {e.name if hasattr(e, 'name') else 'N/A'}")
        print(f"   Dica: Execute 'pip install {e.name}' se for um pacote externo")
    elif isinstance(e, StopIteration):
        print(f"   Dica: Iterador não tem mais elementos")
        print(f"   Verifique se o iterador está vazio ou já foi consumido")
    elif isinstance(e, RuntimeError):
        print(f"   Dica: Erro genérico de execução")
        if "recursion" in str(e).lower():
            print(f"   Possível recursão infinita detectada")
            print(f"   Detalhes: {str(e)}")
    elif isinstance(e, NotImplementedError):
        print(f"   Dica: Método abstrato ou funcionalidade não implementada")
        print(f"   Implemente o método {func.__name__} na subclasse")
    elif isinstance(e, MemoryError):
        print(f"   Dica: Memória insuficiente para a operação")
        print(f"   Processe dados em lotes menores ou otimize estruturas")
    elif isinstance(e, OverflowError):
        print(f"   Dica: Valor numérico muito grande para o tipo")
        print(f"   Considere usar tipos com maior capacidade (ex: Decimal, int arbitrário)")
    elif isinstance(e, LookupError):
        print(f"   Dica: Erro de busca em coleção")
        print(f"   Verifique se o índice/chave existe no intervalo válido")
    elif isinstance(e, StopAsyncIteration):
        print(f"   Dica: Iterador assíncrono não tem mais elementos")
        print(f"   O loop async foi concluído naturalmente")
    elif isinstance(e, ConnectionError):
        print(f"   Dica: Erro de conexão de rede")
        if hasattr(e, 'errno'):
            print(f"   Código de erro: {e.errno}")
            print(f"   Verifique a conectividade e o servidor remoto")
    elif isinstance(e, TimeoutError):
        print(f"   Dica: Operação excedeu o tempo limite")
        print(f"   Aumente o timeout ou otimize a operação")
    elif isinstance(e, EOFError):
        print(f"   Dica: Fim de arquivo/entrada inesperado")
        print(f"   Verifique se há dados suficientes para leitura")
    elif isinstance(e, UnicodeError):
        print(f"   Dica: Erro relacionado a codificação Unicode")
        print(f"   Use encoding='utf-8' ou especifique a codificação correta")
        if hasattr(e, 'encoding'):
            print(f"   Encoding: {e.encoding}")
        if hasattr(e, 'reason'):
            print(f"   Razão: {e.reason}")
    elif isinstance(e, UnicodeEncodeError):
        print(f"   Dica: Falha ao codificar string para bytes")
        print(f"   Caractere problemático: {e.object[e.start:e.end] if hasattr(e, 'object') else 'N/A'}")
        print(f"   Posição: {e.start if hasattr(e, 'start') else 'N/A'}")
    elif isinstance(e, UnicodeDecodeError):
        print(f"   Dica: Falha ao decodificar bytes para string")
        print(f"   Posição do erro: {e.start if hasattr(e, 'start') else 'N/A'}")
        print(f"   Use errors='ignore' ou errors='replace' para contornar")
    elif isinstance(e, FloatingPointError):
        print(f"   Dica: Erro de ponto flutuante")
        print(f"   Verifique divisões por zero, overflow ou operações inválidas")
    elif isinstance(e, AssertionError):
        print(f"   Dica: Falha em asserção (assert statement)")
        print(f"   Expressão: {e.args[0] if e.args else 'N/A'}")
        print(f"   Verifique pré-condições ou invariantes")
    elif isinstance(e, BufferError):
        print(f"   Dica: Operação inválida em buffer")
        print(f"   Verifique o estado do buffer antes da operação")
    elif isinstance(e, BrokenPipeError):
        print(f"   Dica: Pipe quebrado - processo do outro lado fechou")
        print(f"   Verifique se o processo receptor ainda está ativo")
    elif isinstance(e, ChildProcessError):
        print(f"   Dica: Erro em processo filho")
        print(f"   Verifique o código de retorno do subprocesso")
    elif isinstance(e, IsADirectoryError):
        print(f"   Dica: Operação esperava arquivo mas recebeu diretório")
        print(f"   Caminho: {e.filename if hasattr(e, 'filename') else 'N/A'}")
    elif isinstance(e, NotADirectoryError):
        print(f"   Dica: Operação esperava diretório mas recebeu arquivo")
        print(f"   Caminho: {e.filename if hasattr(e, 'filename') else 'N/A'}")
    elif isinstance(e, BlockingIOError):
        print(f"   Dica: Recurso em modo não-bloqueante não está disponível")
        print(f"   Aguarde ou use operações assíncronas")
    elif isinstance(e, InterruptedError):
        print(f"   Dica: Chamada de sistema interrompida por sinal")
        print(f"   Pode ser necessário reexecutar a operação")
    elif isinstance(e, SystemError):
        print(f"   Dica: Erro interno do interpretador Python")
        print(f"   Considere reportar como bug")
    elif isinstance(e, IndentationError):
        print(f"   Dica: Erro de indentação no código")
        print(f"   Linha: {e.lineno if hasattr(e, 'lineno') else 'N/A'}")
        print(f"   Use espaços consistentemente (recomendado 4 espaços)")
    elif isinstance(e, TabError):
        print(f"   Dica: Mistura de tabs e espaços na indentação")
        print(f"   Use apenas espaços (recomendado 4 espaços)")
    elif isinstance(e, SyntaxError):
        print(f"   Dica: Erro de sintaxe no código")
        print(f"   Linha: {e.lineno if hasattr(e, 'lineno') else 'N/A'}")
        print(f"   Coluna: {e.offset if hasattr(e, 'offset') else 'N/A'}")
        if hasattr(e, 'text') and e.text:
            print(f"   Linha com erro: {e.text.strip()}")
    elif isinstance(e, SystemExit):
        print(f"   Dica: Chamada explícita a sys.exit()")
        print(f"   Código de saída: {e.code if hasattr(e, 'code') else 'N/A'}")
    elif isinstance(e, KeyboardInterrupt):
        print(f"   Dica: Programa interrompido pelo usuário (Ctrl+C)")
        print(f"   Finalizando operação atual...")
    elif isinstance(e, GeneratorExit):
        print(f"   Dica: Gerador fechado explicitamente")
        print(f"   Limpeza de recursos em progresso")
    elif isinstance(e, DeprecationWarning):
        print(f"   Dica: Uso de recurso/funcionalidade obsoleta")
        print(f"   Atualize o código para versão mais recente")
    else:
        print(f"   Exceção não específica tratada genericamente")
        print(f"   Tipo: {type(e).__name__}")
        print(f"   Considere adicionar tratamento específico para esta exceção em _tratar_excecao")
    
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
        
        # Verifica se a classe implementa o método __str__ (não herdado de object)
        if not hasattr(obj.__class__, '__str__') or obj.__class__.__str__ == object.__str__:
            nome_classe = obj.__class__.__name__
            raise NotImplementedError(
                f"A classe '{nome_classe}' não implementa o método __str__() de forma personalizada.\n"
                f"O decorator @debug_oo requer que a classe tenha uma representação textual própria.\n"
                f"Por favor, implemente o método __str__ na classe {nome_classe}.\n\n"
                f"Exemplo:\n"
                f"    class {nome_classe}:\n"
                f"        def __init__(self, atributo1):\n"
                f"            self.atributo1 = atributo1\n"
                f"        \n"
                f"        def __str__(self):\n"
                f"            return f'{nome_classe}(atributo1={{self.atributo1}})'"
            )
        
        try:
            obj_str = str(obj)
        except Exception as e:
            raise RuntimeError(
                f"Erro ao chamar __str__() no objeto {obj.__class__.__name__}: {type(e).__name__}: {str(e)}"
            ) from e
        
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
            
            try:
                estado_atual = str(obj)
            except Exception as e:
                print(f"   [{timestamp}]    AVISO: Não foi possível obter novo estado ({type(e).__name__})")
                estado_atual = "<erro ao obter estado>"
            
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
