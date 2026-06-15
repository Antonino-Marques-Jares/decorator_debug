import pytest
import sys
import tempfile
import os
from io import StringIO
from unittest.mock import patch, MagicMock
from datetime import datetime

# Assumindo que o código está em um módulo chamado 'debug_decorators'
from debug_decorators import debug_funcao, debug_oo, _tratar_excecao

# ==================== TESTES PARA @debug_funcao ====================

class TestDebugFuncao:
    
    def test_funcao_sem_argumentos(self, capsys):
        """Testa função sem argumentos que executa com sucesso"""
        
        @debug_funcao
        def saudacao():
            """Retorna uma saudação simples"""
            return "Olá mundo!"
        
        resultado = saudacao()
        
        assert resultado == "Olá mundo!"
        captured = capsys.readouterr()
        assert "FUNÇÃO: saudacao" in captured.out
        assert "RETORNO: 'Olá mundo!'" in captured.out
        assert "STATUS: SUCESSO" in captured.out
        assert "DOCSTRING: Retorna uma saudação simples" in captured.out
    
    def test_funcao_com_argumentos(self, capsys):
        """Testa função com múltiplos argumentos"""
        
        @debug_funcao
        def soma(a, b, c=0):
            """Soma três números"""
            return a + b + c
        
        resultado = soma(5, 3, c=2)
        
        assert resultado == 10
        captured = capsys.readouterr()
        assert "ASSINATURA RECEBIDA: soma(5, 3, c=2)" in captured.out
        assert "RETORNO: 10" in captured.out
    
    def test_funcao_sem_docstring(self, capsys):
        """Testa função sem documentação"""
        
        @debug_funcao
        def calcular(x, y):
            return x * y
        
        resultado = calcular(4, 5)
        
        assert resultado == 20
        captured = capsys.readouterr()
        assert "DOCSTRING: Sem documentação" in captured.out
    
    def test_type_error_na_funcao(self, capsys):
        """Testa tratamento de TypeError"""
        
        @debug_funcao
        def dividir(a, b):
            return a / b
        
        with pytest.raises(TypeError):
            dividir("10", 2)
        
        captured = capsys.readouterr()
        assert "STATUS: FALHA" in captured.out
        assert "ERRO em dividir: TypeError" in captured.out
        assert "Dica: Verifique os tipos dos argumentos" in captured.out
    
    def test_value_error_na_funcao(self, capsys):
        """Testa tratamento de ValueError"""
        
        @debug_funcao
        def converter_para_int(valor):
            return int(valor)
        
        with pytest.raises(ValueError):
            converter_para_int("abc")
        
        captured = capsys.readouterr()
        assert "Dica: Valor inválido fornecido" in captured.out
    
    def test_zero_division_error(self, capsys):
        """Testa tratamento de ZeroDivisionError"""
        
        @debug_funcao
        def dividir_por_zero(x):
            return x / 0
        
        with pytest.raises(ZeroDivisionError):
            dividir_por_zero(10)
        
        captured = capsys.readouterr()
        assert "Dica: Divisão por zero detectada" in captured.out
    
    def test_key_error(self, capsys):
        """Testa tratamento de KeyError"""
        
        @debug_funcao
        def acessar_dicionario(dicionario, chave):
            return dicionario[chave]
        
        with pytest.raises(KeyError):
            acessar_dicionario({"a": 1}, "b")
        
        captured = capsys.readouterr()
        assert "Dica: Chave não encontrada no dicionário" in captured.out
    
    def test_index_error(self, capsys):
        """Testa tratamento de IndexError"""
        
        @debug_funcao
        def acessar_lista(lista, indice):
            return lista[indice]
        
        with pytest.raises(IndexError):
            acessar_lista([1, 2, 3], 10)
        
        captured = capsys.readouterr()
        assert "Dica: Índice fora dos limites" in captured.out
    
    def test_attribute_error(self, capsys):
        """Testa tratamento de AttributeError"""
        
        @debug_funcao
        def chamar_metodo(objeto):
            return objeto.metodo_inexistente()
        
        with pytest.raises(AttributeError):
            chamar_metodo("string")
        
        captured = capsys.readouterr()
        assert "Dica: Objeto não possui o atributo/método solicitado" in captured.out
    
    def test_file_not_found_error(self, capsys):
        """Testa tratamento de FileNotFoundError"""
        
        @debug_funcao
        def ler_arquivo(caminho):
            with open(caminho, 'r') as f:
                return f.read()
        
        with pytest.raises(FileNotFoundError):
            ler_arquivo("/caminho/inexistente/arquivo.txt")
        
        captured = capsys.readouterr()
        assert "Dica: Arquivo ou diretório não encontrado" in captured.out
    
    def test_permission_error(self, capsys, tmp_path):
        """Testa tratamento de PermissionError"""
        
        arquivo = tmp_path / "protegido.txt"
        arquivo.write_text("conteúdo")
        os.chmod(arquivo, 0o000)  # Remove todas as permissões
        
        @debug_funcao
        def ler_arquivo_protegido(caminho):
            with open(caminho, 'r') as f:
                return f.read()
        
        with pytest.raises(PermissionError):
            ler_arquivo_protegido(arquivo)
        
        captured = capsys.readouterr()
        assert "Dica: Permissão negada para acessar o recurso" in captured.out
        
        # Restaura permissão para limpeza
        os.chmod(arquivo, 0o644)
    
    def test_recursion_error(self, capsys):
        """Testa tratamento de RecursionError"""
        
        @debug_funcao
        def recursao_infinita(n):
            return recursao_infinita(n + 1)
        
        with pytest.raises(RecursionError):
            recursao_infinita(0)
        
        captured = capsys.readouterr()
        assert "Dica: Possível recursão infinita ou muita profundidade" in captured.out
    
    def test_import_error(self, capsys):
        """Testa tratamento de ImportError"""
        
        @debug_funcao
        def importar_modulo():
            import modulo_inexistente_xyz_123
        
        with pytest.raises(ImportError):
            importar_modulo()
        
        captured = capsys.readouterr()
        assert "Dica: Falha ao importar módulo/pacote" in captured.out
    
    def test_module_not_found_error(self, capsys):
        """Testa tratamento de ModuleNotFoundError"""
        
        @debug_funcao
        def importar_modulo_especifico():
            import pacote_inexistente_xyz
        
        with pytest.raises(ModuleNotFoundError):
            importar_modulo_especifico()
        
        captured = capsys.readouterr()
        assert "Dica: Módulo específico não encontrado" in captured.out
    
    def test_not_implemented_error(self, capsys):
        """Testa tratamento de NotImplementedError"""
        
        @debug_funcao
        def metodo_nao_implementado():
            raise NotImplementedError("Este método precisa ser implementado")
        
        with pytest.raises(NotImplementedError):
            metodo_nao_implementado()
        
        captured = capsys.readouterr()
        assert "Dica: Método abstrato ou funcionalidade não implementada" in captured.out
    
    def test_timeout_error(self, capsys):
        """Testa tratamento de TimeoutError"""
        
        @debug_funcao
        def operacao_lenta():
            raise TimeoutError("Operação excedeu o tempo limite")
        
        with pytest.raises(TimeoutError):
            operacao_lenta()
        
        captured = capsys.readouterr()
        assert "Dica: Operação excedeu o tempo limite" in captured.out
    
    def test_assertion_error(self, capsys):
        """Testa tratamento de AssertionError"""
        
        @debug_funcao
        def verificar_valor(x):
            assert x > 0, "Valor deve ser positivo"
            return x
        
        with pytest.raises(AssertionError):
            verificar_valor(-5)
        
        captured = capsys.readouterr()
        assert "Dica: Falha em asserção (assert statement)" in captured.out
    
    def test_syntax_error_em_string(self, capsys):
        """Testa tratamento de SyntaxError (simulado)"""
        
        @debug_funcao
        def executar_codigo_invalido():
            raise SyntaxError("invalid syntax", ("<string>", 1, 5, "x = "))
        
        with pytest.raises(SyntaxError):
            executar_codigo_invalido()
        
        captured = capsys.readouterr()
        assert "Dica: Erro de sintaxe no código" in captured.out
    
    def test_keyboard_interrupt(self, capsys):
        """Testa tratamento de KeyboardInterrupt"""
        
        @debug_funcao
        def operacao_interrompida():
            raise KeyboardInterrupt()
        
        with pytest.raises(KeyboardInterrupt):
            operacao_interrompida()
        
        captured = capsys.readouterr()
        assert "Dica: Programa interrompido pelo usuário (Ctrl+C)" in captured.out
    
    def test_excecao_generica(self, capsys):
        """Testa tratamento de exceção genérica não mapeada"""
        
        class ExcecaoPersonalizada(Exception):
            pass
        
        @debug_funcao
        def funcao_com_excecao_personalizada():
            raise ExcecaoPersonalizada("Erro específico da aplicação")
        
        with pytest.raises(ExcecaoPersonalizada):
            funcao_com_excecao_personalizada()
        
        captured = capsys.readouterr()
        assert "Exceção não específica tratada genericamente" in captured.out
        assert "Tipo: ExcecaoPersonalizada" in captured.out
        assert "Considere adicionar tratamento específico" in captured.out


# ==================== TESTES PARA @debug_oo ====================

class TestDebugOO:
    
    def test_classe_com_str_corretamente(self, capsys):
        """Testa decorator em classe que implementa __str__ corretamente"""
        
        @debug_oo
        class Pessoa:
            def __init__(self, nome, idade):
                self.nome = nome
                self.idade = idade
            
            def __str__(self):
                return f"Pessoa(nome={self.nome}, idade={self.idade})"
            
            def envelhecer(self, anos=1):
                self.idade += anos
                return self.idade
            
            def trocar_nome(self, novo_nome):
                self.nome = novo_nome
        
        pessoa = Pessoa("João", 30)
        resultado = pessoa.envelhecer(5)
        
        assert resultado == 35
        assert pessoa.idade == 35
        
        captured = capsys.readouterr()
        assert "MÉTODO: envelhecer(5)" in captured.out
        assert "METODO EXECUTADO COM SUCESSO" in captured.out
        assert "NOVO ESTADO: Pessoa(nome=João, idade=35)" in captured.out
        assert "RETORNO: 35" in captured.out
    
    def test_metodo_sem_argumentos(self, capsys):
        """Testa método sem argumentos"""
        
        @debug_oo
        class Calculadora:
            def __init__(self, valor):
                self.valor = valor
            
            def __str__(self):
                return f"Calculadora(valor={self.valor})"
            
            def dobrar(self):
                self.valor *= 2
                return self.valor
        
        calc = Calculadora(10)
        resultado = calc.dobrar()
        
        assert resultado == 20
        captured = capsys.readouterr()
        assert "MÉTODO: dobrar()" in captured.out
        assert "NOVO ESTADO: Calculadora(valor=20)" in captured.out
    
    def test_metodo_com_kwargs(self, capsys):
        """Testa método com argumentos nomeados"""
        
        @debug_oo
        class Config:
            def __init__(self, **kwargs):
                self.config = kwargs
            
            def __str__(self):
                return f"Config({self.config})"
            
            def atualizar(self, **kwargs):
                self.config.update(kwargs)
                return self.config
        
        config = Config(host="localhost", port=8080)
        resultado = config.atualizar(port=9090, debug=True)
        
        assert resultado == {"host": "localhost", "port": 9090, "debug": True}
        captured = capsys.readouterr()
        assert "MÉTODO: atualizar(port=9090, debug=True)" in captured.out
    
    def test_metodo_que_retorna_none(self, capsys):
        """Testa método que não retorna valor explícito"""
        
        @debug_oo
        class Logger:
            def __init__(self):
                self.mensagens = []
            
            def __str__(self):
                return f"Logger(mensagens={len(self.mensagens)})"
            
            def adicionar(self, msg):
                self.mensagens.append(msg)
        
        logger = Logger()
        resultado = logger.adicionar("teste")
        
        assert resultado is None
        captured = capsys.readouterr()
        assert "EXECUTADO -> retorno: None" in captured.out
        assert "NOVO ESTADO:" in captured.out
    
    def test_metodo_que_nao_altera_estado(self, capsys):
        """Testa método que não altera o estado do objeto"""
        
        @debug_oo
        class Leitor:
            def __init__(self, dados):
                self.dados = dados
            
            def __str__(self):
                return f"Leitor({self.dados})"
            
            def ler(self, indice):
                return self.dados[indice]
        
        leitor = Leitor([1, 2, 3])
        resultado = leitor.ler(1)
        
        assert resultado == 2
        captured = capsys.readouterr()
        assert "EXECUTADO -> retorno: 2" in captured.out
        assert "NOVO ESTADO:" not in captured.out  # Estado não mudou
    
    def test_classe_sem_str(self):
        """Testa classe que não implementa __str__ - deve levantar NotImplementedError"""
        
        with pytest.raises(NotImplementedError) as exc_info:
            @debug_oo
            class ClasseSemStr:
                def __init__(self, x):
                    self.x = x
                
                def metodo(self):
                    return self.x
        
        assert "não implementa o método __str__()" in str(exc_info.value)
        assert "ClasseSemStr" in str(exc_info.value)
    
    def test_classe_com_str_herdado_de_object(self):
        """Testa classe que usa __str__ padrão do object"""
        
        class Pai:
            pass
        
        with pytest.raises(NotImplementedError) as exc_info:
            @debug_oo
            class Filho(Pai):
                def __init__(self, valor):
                    self.valor = valor
                
                def metodo(self):
                    return self.valor
        
        assert "não implementa o método __str__()" in str(exc_info.value)
    
    def test_str_retorna_string_muito_longa(self, capsys):
        """Testa quando __str__ retorna string muito longa (>80 chars)"""
        
        @debug_oo
        class TextoGrande:
            def __init__(self):
                self.texto = "a" * 100
            
            def __str__(self):
                return f"TextoGrande({self.texto})"
            
            def metodo(self):
                pass
        
        obj = TextoGrande()
        obj.metodo()
        
        captured = capsys.readouterr()
        # Verifica que a string foi truncada
        assert "..." in captured.out
        assert len(captured.out.split("ESTADO:")[1].split("\n")[0]) <= 90
    
    def test_excecao_no_metodo(self, capsys):
        """Testa tratamento de exceção dentro do método"""
        
        @debug_oo
        class ContaBancaria:
            def __init__(self, saldo):
                self.saldo = saldo
            
            def __str__(self):
                return f"Conta(saldo={self.saldo})"
            
            def sacar(self, valor):
                if valor > self.saldo:
                    raise ValueError("Saldo insuficiente")
                self.saldo -= valor
                return self.saldo
        
        conta = ContaBancaria(100)
        
        with pytest.raises(ValueError):
            conta.sacar(200)
        
        captured = capsys.readouterr()
        assert "ERRO em sacar: ValueError: Saldo insuficiente" in captured.out
        assert "Dica: Valor inválido fornecido" in captured.out
    
    def test_excecao_no_str_do_objeto(self):
        """Testa quando __str__ lança exceção"""
        
        class ObjetoComStrQuebrado:
            def __str__(self):
                raise RuntimeError("Erro ao gerar string")
        
        with pytest.raises(RuntimeError) as exc_info:
            @debug_oo
            class MinhaClasse:
                def __init__(self):
                    self.obj = ObjetoComStrQuebrado()
                
                def __str__(self):
                    return str(self.obj)
                
                def metodo(self):
                    pass
        
        # O erro ocorre quando tenta instanciar e chamar o método
        obj = MinhaClasse()
        with pytest.raises(RuntimeError):
            obj.metodo()
        
        assert "Erro ao chamar __str__()" in str(exc_info.value)
    
    def test_timestamp_no_output(self, capsys):
        """Testa se o timestamp está presente no output"""
        
        @debug_oo
        class TesteTimestamp:
            def __init__(self, valor):
                self.valor = valor
            
            def __str__(self):
                return f"Teste(valor={self.valor})"
            
            def metodo(self):
                pass
        
        obj = TesteTimestamp(42)
        obj.metodo()
        
        captured = capsys.readouterr()
        # Verifica formato de timestamp HH:MM:SS.mmm
        import re
        timestamp_pattern = r'\[\d{2}:\d{2}:\d{2}\.\d{3}\]'
        assert re.search(timestamp_pattern, captured.out)
    
    def test_multiplas_chamadas_no_mesmo_objeto(self, capsys):
        """Testa múltiplas chamadas no mesmo objeto"""
        
        @debug_oo
        class Contador:
            def __init__(self):
                self.count = 0
            
            def __str__(self):
                return f"Contador(count={self.count})"
            
            def incrementar(self):
                self.count += 1
        
        contador = Contador()
        
        for i in range(3):
            contador.incrementar()
        
        captured = capsys.readouterr()
        assert captured.out.count("MÉTODO: incrementar()") == 3
        assert "NOVO ESTADO: Contador(count=1)" in captured.out
        assert "NOVO ESTADO: Contador(count=2)" in captured.out
        assert "NOVO ESTADO: Contador(count=3)" in captured.out


# ==================== TESTES PARA _tratar_excecao ====================

class TestTratarExcecao:
    
    def test_tratar_excecao_generica(self, capsys):
        """Testa função _tratar_excecao diretamente com exceção genérica"""
        
        def func_teste():
            pass
        
        try:
            raise Exception("Erro genérico")
        except Exception as e:
            _tratar_excecao(func_teste, "args_teste", e)
        
        captured = capsys.readouterr()
        assert "ERRO em func_teste: Exception: Erro genérico" in captured.out
        assert "Stack trace:" in captured.out
    
    def test_tratar_stop_iteration(self, capsys):
        """Testa tratamento de StopIteration"""
        
        def func_teste():
            pass
        
        try:
            next(iter([]))
        except StopIteration as e:
            _tratar_excecao(func_teste, "", e)
        
        captured = capsys.readouterr()
        assert "Dica: Iterador não tem mais elementos" in captured.out
    
    def test_tratar_memory_error(self, capsys):
        """Testa tratamento de MemoryError"""
        
        def func_teste():
            pass
        
        try:
            raise MemoryError()
        except MemoryError as e:
            _tratar_excecao(func_teste, "", e)
        
        captured = capsys.readouterr()
        assert "Dica: Memória insuficiente para a operação" in captured.out
    
    def test_tratar_unicode_error(self, capsys):
        """Testa tratamento de UnicodeError"""
        
        def func_teste():
            pass
        
        try:
            "string".encode('ascii').decode('utf-8')
        except UnicodeDecodeError as e:
            _tratar_excecao(func_teste, "", e)
        
        captured = capsys.readouterr()
        assert "Dica: Erro relacionado a codificação Unicode" in captured.out
    
    def test_tratar_overflow_error(self, capsys):
        """Testa tratamento de OverflowError"""
        
        def func_teste():
            pass
        
        try:
            float(10**1000)
        except OverflowError as e:
            _tratar_excecao(func_teste, "", e)
        
        captured = capsys.readouterr()
        assert "Dica: Valor numérico muito grande para o tipo" in captured.out
    
    def test_tratar_broken_pipe_error(self, capsys):
        """Testa tratamento de BrokenPipeError"""
        
        def func_teste():
            pass
        
        try:
            raise BrokenPipeError()
        except BrokenPipeError as e:
            _tratar_excecao(func_teste, "", e)
        
        captured = capsys.readouterr()
        assert "Dica: Pipe quebrado" in captured.out
    
    def test_tratar_indentation_error(self, capsys):
        """Testa tratamento de IndentationError"""
        
        def func_teste():
            pass
        
        try:
            raise IndentationError("indentation error", ("<string>", 1, 0, "  x"))
        except IndentationError as e:
            _tratar_excecao(func_teste, "", e)
        
        captured = capsys.readouterr()
        assert "Dica: Erro de indentação no código" in captured.out
    
    def test_tratar_system_exit(self, capsys):
        """Testa tratamento de SystemExit"""
        
        def func_teste():
            pass
        
        try:
            sys.exit(1)
        except SystemExit as e:
            _tratar_excecao(func_teste, "", e)
        
        captured = capsys.readouterr()
        assert "Dica: Chamada explícita a sys.exit()" in captured.out
    
    def test_tratar_deprecation_warning(self, capsys):
        """Testa tratamento de DeprecationWarning"""
        
        def func_teste():
            pass
        
        try:
            raise DeprecationWarning("Esta função é obsoleta")
        except DeprecationWarning as e:
            _tratar_excecao(func_teste, "", e)
        
        captured = capsys.readouterr()
        assert "Dica: Uso de recurso/funcionalidade obsoleta" in captured.out


# ==================== TESTES DE INTEGRAÇÃO ====================

class TestIntegracao:
    
    def test_funcao_decorada_repassa_valores_corretamente(self):
        """Testa se o decorator não interfere no retorno da função"""
        
        @debug_funcao
        def multiplicar(a, b):
            return a * b
        
        assert multiplicar(3, 4) == 12
        assert multiplicar(-2, 5) == -10
        assert multiplicar(0, 100) == 0
    
    def test_metodo_decorado_mantem_comportamento(self):
        """Testa se o decorator não interfere no comportamento do método"""
        
        @debug_oo
        class Pilha:
            def __init__(self):
                self._itens = []
            
            def __str__(self):
                return f"Pilha({self._itens})"
            
            def push(self, item):
                self._itens.append(item)
            
            def pop(self):
                if not self._itens:
                    raise IndexError("Pilha vazia")
                return self._itens.pop()
            
            def top(self):
                if not self._itens:
                    return None
                return self._itens[-1]
        
        pilha = Pilha()
        pilha.push(1)
        pilha.push(2)
        
        assert pilha.top() == 2
        assert pilha.pop() == 2
        assert pilha.pop() == 1
        
        with pytest.raises(IndexError):
            pilha.pop()
    
    def test_decorators_aninhados_nao_interferem(self):
        """Testa múltiplos decorators (se houver outros decorators)"""
        
        def outro_decorator(func):
            def wrapper(*args, **kwargs):
                print("OUTRO")
                return func(*args, **kwargs)
            return wrapper
        
        @outro_decorator
        @debug_funcao
        def funcao_com_multiplos_decorators(x):
            return x * 2
        
        resultado = funcao_com_multiplos_decorators(5)
        assert resultado == 10


# ==================== TESTES DE PERFORMANCE ====================

class TestPerformance:
    
    def test_decorator_nao_adiciona_overhead_significativo(self, benchmark):
        """Testa performance do decorator"""
        
        @debug_funcao
        def operacao_simples(x, y):
            return x + y
        
        def executar():
            return operacao_simples(10, 20)
        
        resultado = benchmark(executar)
        assert resultado == 30
    
    def test_decorator_oo_nao_adiciona_overhead_significativo(self, benchmark):
        """Testa performance do decorator OO"""
        
        @debug_oo
        class ObjetoSimples:
            def __init__(self, valor):
                self.valor = valor
            
            def __str__(self):
                return f"Obj({self.valor})"
            
            def metodo(self):
                return self.valor * 2
        
        obj = ObjetoSimples(5)
        
        def executar():
            return obj.metodo()
        
        resultado = benchmark(executar)
        assert resultado == 10





if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
