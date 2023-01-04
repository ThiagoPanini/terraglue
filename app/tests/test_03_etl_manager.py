"""
SCRIPT: test_etl_manager.py

CONTEXTO:
---------
Script de testes criado para validar elementos e
funcionalidades presentes na classe GlueETLManager do
módulo terraglue como forma de garantir que todos os
insumos necessários para execução da aplicação Spark
se fazem presentes.

OBJETIVO:
---------
Consoldar uma suíte de testes capaz de testar e validar
todos os insumos presentes na classe GlueETLManager que
podem comprometer o funcionamento da aplicação.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando módulos para uso
from pytest import mark


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@mark.etl_manager
def test_conversao_de_data_no_metodo_de_extracao_de_atributos_de_data(
    etl_manager, fake_dataframe):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método date_attributes_extraction() da classe
       GlueETLManager for executado em uma coluna de data com
       date_col_type="date" e convert_string_to_date=True
    T: então o DataFrame resultante deve conter a mesma coluna de data
       porém com o tipo primitivo DateType
    """