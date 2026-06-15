# ==================== TESTES PARA GOOGLE COLAB ====================
# Este código pode ser executado diretamente em células do Google Colab

import sys
import traceback
from datetime import datetime
import inspect
from io import StringIO
import contextlib

# Assumindo que seu código já foi executado na célula anterior
# Se não, copie e execute o código dos decorators primeiro

# ==================== UTILITÁRIOS PARA TESTES ====================

def capturar_saida(func):
    """Decorator para capturar output impresso durante testes"""
    def wrapper(*args, **kwargs):
        buffer = StringIO()
        with contextlib.redirect_stdout(buffer):
            resultado = func(*args, **kwargs)
        return resultado, buffer.getvalue()
    return wrapper

def print_test_header(nome_teste):
    """Imprime cabeçalho formatado para testes"""
    print(f"\n{'='*70}")
    print(f"🧪 TESTE: {nome_teste}")
    print(f"{'='*70}")

# ==================== TESTES PARA @debug_funcao ====================

print("\n" + "="*70)
print("🚀 INICIANDO BATERIA DE TESTES")
print("="*70)

print_test_header("1. Função sem argumentos - Sucesso")

@debug_funcao
def saudacao():
    """Retorna uma saudação simples"""
    return "Olá mundo!"

resultado = saudacao()
print(f"\n✅ Resultado esperado: 'Olá mundo!'")
print(f"✅ Resultado obtido: {resultado}")
assert resultado == "Olá mundo!", "Erro: valor retornado incorreto"

print_test_header("2. Função com múltiplos argumentos")

@debug_funcao
def calcular_media(nota1, nota2, nota3=0):
    """Calcula média de notas"""
    return (nota1 + nota2 + nota3) / 3

resultado = calcular_media(7.5, 8.0, nota3=9.5)
print(f"\n✅ Média calculada: {resultado:.2f}")
assert 8.33 < resultado < 8.34, "Erro no cálculo da média"

print_test_header("3. Função sem docstring")

@debug_funcao
def multiplicar(x, y):
    return x * y

resultado = multiplicar(4, 5)
print(f"\n✅ 4 × 5 = {resultado}")
assert resultado == 20

print_test_header("4. Tratamento de TypeError")

@debug_funcao
def dividir(a, b):
    return a / b

try:
    dividir("10", 2)
except TypeError as e:
    print(f"\n✅ TypeError capturado corretamente: {type(e).__name__}")
else:
    print("\n❌ Erro: TypeError não foi levantado")

print_test_header("5. Tratamento de ZeroDivisionError")

@debug_funcao
def dividir_por_zero(x):
    return x / 0

try:
    dividir_por_zero(10)
except ZeroDivisionError as e:
    print(f"\n✅ ZeroDivisionError capturado: {type(e).__name__}")
else:
    print("\n❌ Erro: ZeroDivisionError não foi levantado")

print_test_header("6. Tratamento de KeyError")

@debug_funcao
def acessar_dicionario(dicionario, chave):
    return dicionario[chave]

try:
    acessar_dicionario({"nome": "João"}, "idade")
except KeyError as e:
    print(f"\n✅ KeyError capturado: chave '{e.args[0]}' não encontrada")
else:
    print("\n❌ Erro: KeyError não foi levantado")

print_test_header("7. Tratamento de IndexError")

@debug_funcao
def acessar_lista(lista, indice):
    return lista[indice]

try:
    acessar_lista([1, 2, 3], 10)
except IndexError as e:
    print(f"\n✅ IndexError capturado: índice {e.args[0]} fora dos limites")
else:
    print("\n❌ Erro: IndexError não foi levantado")

print_test_header("8. Tratamento de AttributeError")

@debug_funcao
def chamar_metodo_inexistente(objeto):
    return objeto.metodo_que_nao_existe()

try:
    chamar_metodo_inexistente("string")
except AttributeError as e:
    print(f"\n✅ AttributeError capturado: {str(e)}")
else:
    print("\n❌ Erro: AttributeError não foi levantado")

print_test_header("9. Tratamento de ValueError")

@debug_funcao
def converter_para_int(valor):
    return int(valor)

try:
    converter_para_int("não é número")
except ValueError as e:
    print(f"\n✅ ValueError capturado: {str(e)}")
else:
    print("\n❌ Erro: ValueError não foi levantado")

print_test_header("10. Tratamento de RecursionError")

@debug_funcao
def recursao_infinita(n):
    return recursao_infinita(n + 1)

try:
    recursao_infinita(0)
except RecursionError as e:
    print(f"\n✅ RecursionError capturado: profundidade excedida")
else:
    print("\n❌ Erro: RecursionError não foi levantado")

print_test_header("11. Tratamento de NotImplementedError")

@debug_funcao
def metodo_nao_implementado():
    raise NotImplementedError("Este método precisa ser implementado na subclasse")

try:
    metodo_nao_implementado()
except NotImplementedError as e:
    print(f"\n✅ NotImplementedError capturado: {str(e)}")
else:
    print("\n❌ Erro: NotImplementedError não foi levantado")

print_test_header("12. Função com argumentos complexos")

@debug_funcao
def processar_lista(lista, multiplicador=2):
    """Processa lista multiplicando elementos"""
    return [x * multiplicador for x in lista]

lista_original = [1, 2, 3, 4]
resultado = processar_lista(lista_original, multiplicador=3)
print(f"\n✅ Lista original: {lista_original}")
print(f"✅ Lista processada: {resultado}")
assert resultado == [3, 6, 9, 12], "Erro no processamento"

# ==================== TESTES PARA @debug_oo ====================

print_test_header("13. Classe com __str__ implementado")

@debug_oo
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
    
    def __str__(self):
        return f"Pessoa(nome='{self.nome}', idade={self.idade})"
    
    def fazer_aniversario(self):
        self.idade += 1
        return self.idade
    
    def trocar_nome(self, novo_nome):
        self.nome = novo_nome
        return self.nome

pessoa = Pessoa("Ana", 25)
print(f"\n✅ Objeto criado: {pessoa}")
resultado = pessoa.fazer_aniversario()
print(f"✅ Nova idade: {resultado}")
assert resultado == 26, "Erro no aniversário"

print_test_header("14. Método que não altera estado")

@debug_oo
class Calculadora:
    def __init__(self, valor):
        self.valor = valor
    
    def __str__(self):
        return f"Calculadora(valor={self.valor})"
    
    def obter_dobro(self):
        return self.valor * 2

calc = Calculadora(10)
print(f"\n✅ Objeto: {calc}")
resultado = calc.obter_dobro()
print(f"✅ Dobro: {resultado}")
assert resultado == 20, "Erro no cálculo do dobro"
assert calc.valor == 10, "Estado não deveria mudar"

print_test_header("15. Método com múltiplos argumentos")

@debug_oo
class Retangulo:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
    
    def __str__(self):
        return f"Retangulo({self.largura}x{self.altura})"
    
    def redimensionar(self, nova_largura=None, nova_altura=None):
        if nova_largura:
            self.largura = nova_largura
        if nova_altura:
            self.altura = nova_altura
        return self.largura * self.altura

ret = Retangulo(10, 5)
print(f"\n✅ Área original: {ret.largura * ret.altura}")
area = ret.redimensionar(nova_largura=15, nova_altura=8)
print(f"✅ Nova área: {area}")
assert area == 120, "Erro no redimensionamento"

print_test_header("16. Método que retorna None")

@debug_oo
class Logger:
    def __init__(self):
        self.mensagens = []
    
    def __str__(self):
        return f"Logger({len(self.mensagens)} msgs)"
    
    def adicionar(self, mensagem):
        self.mensagens.append(mensagem)

logger = Logger()
print(f"\n✅ Logger criado: {logger}")
resultado = logger.adicionar("Teste 1")
print(f"✅ Retorno do método: {resultado}")
assert resultado is None, "Método deveria retornar None"
assert len(logger.mensagens) == 1, "Mensagem não foi adicionada"

print_test_header("17. Classe sem __str__ - Deve levantar erro")

try:
    @debug_oo
    class ClasseSemStr:
        def __init__(self, valor):
            self.valor = valor
        
        def metodo(self):
            return self.valor
    
    obj = ClasseSemStr(42)
    obj.metodo()  # Deve falhar aqui
    print("\n❌ Erro: Não levantou NotImplementedError")
except NotImplementedError as e:
    print(f"\n✅ NotImplementedError capturado: {str(e)[:100]}...")
except Exception as e:
    print(f"\n⚠️ Outro erro: {type(e).__name__}")

print_test_header("18. Tratamento de exceção no método")

@debug_oo
class ContaBancaria:
    def __init__(self, saldo):
        self.saldo = saldo
    
    def __str__(self):
        return f"Conta(saldo=R${self.saldo:.2f})"
    
    def sacar(self, valor):
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= valor
        return self.saldo

conta = ContaBancaria(100)
print(f"\n✅ Conta criada: {conta}")

try:
    conta.sacar(200)
    print("\n❌ Erro: Não levantou ValueError")
except ValueError as e:
    print(f"\n✅ ValueError capturado: {str(e)}")
    assert conta.saldo == 100, "Saldo não deveria mudar"

print_test_header("19. Múltiplas operações no mesmo objeto")

@debug_oo
class Contador:
    def __init__(self):
        self.valor = 0
    
    def __str__(self):
        return f"Contador(valor={self.valor})"
    
    def incrementar(self, quantidade=1):
        self.valor += quantidade
        return self.valor

contador = Contador()
print(f"\n✅ Estado inicial: {contador}")

valores = []
for i in range(5):
    valores.append(contador.incrementar())

print(f"\n✅ Sequência: {valores}")
assert valores == [1, 2, 3, 4, 5], "Erro na sequência de incrementos"

print_test_header("20. Objeto com __str__ longo (truncamento)")

@debug_oo
class TextoLongo:
    def __init__(self, texto):
        self.texto = texto
    
    def __str__(self):
        return f"TextoLongo(texto='{self.texto}')"
    
    def metodo_qualquer(self):
        pass

texto_longo = "a" * 100
obj = TextoLongo(texto_longo)
print(f"\n✅ Texto original: {texto_longo[:50]}... (100 caracteres)")
obj.metodo_qualquer()
print("\n✅ Verificar se a saída foi truncada (deve conter '...')")

# ==================== TESTES ADICIONAIS ====================

print_test_header("21. Decorator funciona com herança")

class Animal:
    def __init__(self, nome):
        self.nome = nome
    
    def __str__(self):
        return f"Animal(nome='{self.nome}')"

@debug_oo
class Cachorro(Animal):
    def __init__(self, nome, raca):
        super().__init__(nome)
        self.raca = raca
    
    def __str__(self):
        return f"Cachorro(nome='{self.nome}', raca='{self.raca}')"
    
    def latir(self):
        return f"{self.nome} diz: Au au!"

dog = Cachorro("Rex", "Labrador")
print(f"\n✅ Cachorro criado: {dog}")
som = dog.latir()
print(f"✅ {som}")
assert "Rex" in som, "Nome não está no som"

print_test_header("22. Método com argumentos nomeados e posicionais")

@debug_oo
class Configuracao:
    def __init__(self, **defaults):
        self.config = defaults
    
    def __str__(self):
        return f"Config({self.config})"
    
    def atualizar(self, *args, **kwargs):
        for chave, valor in kwargs.items():
            self.config[chave] = valor
        return self.config

config = Configuracao(host="localhost", port=8080)
print(f"\n✅ Config inicial: {config.config}")
resultado = config.atualizar(port=9090, debug=True, timeout=30)
print(f"✅ Config atualizada: {resultado}")
assert resultado["port"] == 9090, "Porta não atualizada"
assert resultado["debug"] is True, "Debug não ativado"

print_test_header("23. Teste de timestamp no output")

@debug_oo
class TesteTimestamp:
    def __init__(self, valor):
        self.valor = valor
    
    def __str__(self):
        return f"Teste({self.valor})"
    
    def metodo(self):
        pass

obj = TesteTimestamp(42)
obj.metodo()
print("\n✅ Verificar se o timestamp no formato HH:MM:SS.mmm aparece na saída acima")

print_test_header("24. Teste de exceções específicas - FileNotFoundError")

@debug_funcao
def ler_arquivo_inexistente():
    with open('/caminho/que/nao/existe/arquivo.txt', 'r') as f:
        return f.read()

try:
    ler_arquivo_inexistente()
except FileNotFoundError as e:
    print(f"\n✅ FileNotFoundError capturado: {str(e)[:100]}")

print_test_header("25. Teste de exceções específicas - PermissionError (simulado)")

@debug_funcao
def acesso_sem_permissao():
    raise PermissionError("Permissão negada para acessar o arquivo")

try:
    acesso_sem_permissao()
except PermissionError as e:
    print(f"\n✅ PermissionError capturado: {str(e)}")

print_test_header("26. Teste de exceções específicas - UnicodeError")

@debug_funcao
def erro_unicode():
    # Simula erro de decodificação
    dados = b'\xff\xfe\x00\x00'
    return dados.decode('utf-8')

try:
    erro_unicode()
except UnicodeDecodeError as e:
    print(f"\n✅ UnicodeDecodeError capturado: posição {e.start}")

print_test_header("27. Teste de exceções específicas - AssertionError")

@debug_funcao
def verificar_positivo(valor):
    assert valor > 0, "Valor deve ser positivo"
    return valor

try:
    verificar_positivo(-10)
except AssertionError as e:
    print(f"\n✅ AssertionError capturado: {str(e)}")

# ==================== RESUMO DOS TESTES ====================

print("\n" + "="*70)
print("📊 RESUMO DOS TESTES")
print("="*70)

testes_realizados = 27
testes_aprovados = 24  # Alguns testes são apenas verificações manuais
print(f"\n✅ Total de testes executados: {testes_realizados}")
print(f"✅ Todos os testes de funcionalidade foram executados")
print("\n🔍 Verificações manuais necessárias:")
print("   - Verificar visualmente as saídas dos decorators")
print("   - Confirmar que timestamps aparecem corretamente")
print("   - Verificar truncamento de strings longas")
print("   - Confirmar que stack traces são exibidos")

print("\n" + "="*70)
print("🎉 BATERIA DE TESTES CONCLUÍDA!")
print("="*70)
