import sys

TODO_FILE = 'todo.txt'
ARCHIVE_FILE = 'done.txt'

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

ADICIONAR = 'a'
REMOVER = 'r'
FAZER = 'f'
PRIORIZAR = 'p'
LISTAR = 'l'

# Imprime texto com cores. Por exemplo, para imprimir "Oi mundo!" em vermelho, basta usar
#
# printCores('Oi mundo!', RED)
# printCores('Texto amarelo e negrito', YELLOW + BOLD)

def printCores(texto, cor) :
  print(cor + texto + RESET)
  

# Adiciona um compromisso aa agenda. Um compromisso tem no minimo
# uma descrição. Adicionalmente, pode ter, em caráter opcional, uma
# data (formato DDMMAAAA), um horário (formato HHMM), uma prioridade de A a Z, 
# um contexto onde a atividade será realizada (precedido pelo caractere
# '@') e um projeto do qual faz parte (precedido pelo caractere '+'). Esses
# itens opcionais são os elementos da tupla "extras", o segundo parâmetro da
# função.
#
# extras ~ (data, hora, prioridade, contexto, projeto)
#
# Qualquer elemento da tupla que contenha um string vazio ('') não
# deve ser levado em consideração. 
def adicionar(descricao, extras):

  # não é possível adicionar uma atividade que não possui descrição. 
  if descricao  == '' :
    print('Esse compromisso não possui descrição, por isso não foi adicionado na sua agenda')
    return False

  else:
    novaAtividade = ''

    if dataValida(extras[0]):
        novaAtividade += extras[0] + ' '

    if horaValida(extras[1]):
      novaAtividade += extras[1] + ' '

    novaAtividade += descricao + ' '

    if contextoValido(extras[2]):
      novaAtividade += extras[2] + ' '

    if projetoValido(extras[3]):
      novaAtividade += extras[3]

  # Escreve no TODO_FILE. 
  try: 
    fp = open(TODO_FILE, 'a')
    fp.write(novaAtividade + "\n")
    fp.close()
  except IOError as err:
    print("Não foi possível escrever para o arquivo " + TODO_FILE)
    print(err)
    return False

  return True


# Valida a prioridade.
def prioridadeValida(pri):

  if pri[0] == '(' and pri[2] == ')' and 'A' <= pri[1] <= 'Z':
    return True
  
  return False


# Valida a hora. Consideramos que o dia tem 24 horas, como no Brasil, ao invés
# de dois blocos de 12 (AM e PM), como nos EUA.
def horaValida(horaMin) :
  if len(horaMin) != 4 or not soDigitos(horaMin):
    return False
  else:
    if (horaMin[0]+horaMin[1] > '23' or horaMin[0]+horaMin[1] < '00') or (horaMin[2]+horaMin[3] > '59' or horaMin[2]+horaMin[3] < '00'):
      return False
    return True

# Valida datas. Verificar inclusive se não estamos tentando
# colocar 31 dias em fevereiro. Não precisamos nos certificar, porém,
# de que um ano é bissexto. 
def dataValida(data) :
  if len(data) != 8 or not soDigitos(data):
    return False
  
  else:
    if data[2]+data[3] > '12' or data[2]+data[3] < '01':
      return False
    else:
      if data[2]+data[3] == '01' or data[2]+data[3] == '03' or data[2]+data[3] == '05' or data[2]+data[3] == '07' or data[2]+data[3] == '08' or data[2]+data[3] == '10' or data[2]+data[3] == '12':
        if data[0]+data[1] > '31' or data[0]+data[1] < '01':
          return False
      
      elif data[2]+data[3] == '02':
        if data[0]+data[1] > '29':
          return False

      elif data[2]+data[3] == '04' or data[2]+data[3] == '06' or data[2]+data[3] == '09' or data[2]+data[3] == '11':
        if data[0]+data[1] > '30':
          return False
  return True

# Valida que o string do projeto está no formato correto. 
def projetoValido(proj):
  if proj == '':
    return False
  
  elif proj[0] == '+' and len(proj) >= 2:
    return True

  return False

# Valida que o string do contexto está no formato correto. 
def contextoValido(cont):
  if cont == '':
    return False

  elif cont[0] == '@' and len(cont) >= 2:
    return True

  return False

# Valida que a data ou a hora contém apenas dígitos, desprezando espaços
# extras no início e no fim.
def soDigitos(numero) :
  if type(numero) != str :
    return False
  for x in numero :
    if x < '0' or x > '9' :
      return False
  return True

# Função que, dada um caractere inicial, vai continuar concatenando
# até encontrar um espaço vazio


# Dadas as linhas de texto obtidas a partir do arquivo texto todo.txt, devolve
# uma lista de tuplas contendo os pedaços de cada linha, conforme o seguinte
# formato:
#
# (descrição, prioridade, (data, hora, contexto, projeto))
#
# É importante lembrar que linhas do arquivo todo.txt devem estar organizadas de acordo com o
# seguinte formato:
#
# #DDMMAAAA &HHMM (P) DESC @CONTEXT +PROJ
#
# Todos os itens menos DESC são opcionais. Se qualquer um deles estiver fora do formato, por exemplo,
# data que não tem todos os componentes ou prioridade com mais de um caractere (além dos parênteses),
# tudo que vier depois será considerado parte da descrição.  
def organizar(linhas):

  itens = []

  cont = 1

  for l in linhas:    
    data = ''  
    hora = ''
    pri = ''
    desc = ''
    contexto = ''
    projeto = ''
    
    l = l.strip() # remove espaços em branco e quebras de linha do começo e do fim
    tokens = l.split() # quebra o string em palavras
        
    # Processa os tokens um a um, verificando se são as partes da atividade.
    # Por exemplo, se o primeiro token é uma data válida, deve ser guardado
    # na variável data e posteriormente removido a lista de tokens. Feito isso,
    # é só repetir o processo verificando se o primeiro token é uma hora. Depois,
    # faz-se o mesmo para prioridade. Neste ponto, verifica-se os últimos tokens
    # para saber se são contexto e/ou projeto. Quando isso terminar, o que sobrar
    # corresponde à descrição. É só transformar a lista de tokens em um string e
    # construir a tupla com as informações disponíveis. 
    if tokens == []:
      continue
    else:
      if dataValida(tokens[0]):
        data += tokens[0]
        tokens.pop(0)

      if horaValida(tokens[0]):
        hora += tokens[0]
        tokens.pop(0)
      
      if prioridadeValida(tokens[0]):
        pri += tokens[0]
        tokens.pop(0)

      if contextoValido(tokens[len(tokens)-2]):
        contexto += tokens[len(tokens)-2]
        tokens.pop(len(tokens)-2)

      if projetoValido(tokens[len(tokens)-1]):
        projeto += tokens[len(tokens)-1]
        tokens.pop(len(tokens)-1)

      desc = ' '.join(tokens)

    itens.append((desc, (data, hora, pri, contexto, projeto), cont))
    cont += 1
    
  return itens

# Datas e horas são armazenadas nos formatos DDMMAAAA e HHMM, mas são exibidas
# como se espera (com os separadores apropridados). 
#
# Uma extensão possível é listar com base em diversos critérios: (i) atividades com certa prioridade;
# (ii) atividades a ser realizadas em certo contexto; (iii) atividades associadas com
# determinado projeto; (vi) atividades de determinado dia (data específica, hoje ou amanhã). Isso não
# é uma das tarefas básicas do projeto, porém. 
def listar():

  arquivo = open(TODO_FILE, 'r')
  linhas = arquivo.readlines()
  arquivo.close()

  todasAtividades = organizar(linhas)

  return todasAtividades

def listarOrdenado():
  
  itens = ordenarPorPrioridade(ordenarPorDataHora(listar()))
  
  for i in itens:
    atividadePrintada = ''

    if i[1][0] != '':
      atividadePrintada += i[1][0][0:2] + '/' + i[1][0][2:4] + '/' + i[1][0][4:] + ' '

    if i[1][1] != '':
      atividadePrintada += i[1][1][0:2] + 'h' + i[1][1][2:4] + 'm '

    if i[1][2] != '':
      atividadePrintada += i[1][2] + ' '

    atividadePrintada += i[0] + ' '

    if i[1][3] != '':
      atividadePrintada += i[1][3] + ' '

    if i[1][4] != '':
      atividadePrintada += i[1][4]

    if i[1][2] == '(A)':
      print(RED + str(i[2]),end = ' ')
      printCores(atividadePrintada, RED)

    elif i[1][2] == '(B)':
      print(YELLOW+str(i[2]),end = ' ')
      printCores(atividadePrintada, YELLOW)

    elif i[1][2] == '(C)':
      print(GREEN+str(i[2]),end = ' ')
      printCores(atividadePrintada, GREEN)

    elif i[1][2] == '(D)':
      print(CYAN + str(i[2]), end = ' ')
      printCores(atividadePrintada, CYAN)
      
    else:
      print(i[2], atividadePrintada)

  return itens

def ordenarPorDataHora(itens):
  
  itens = ordenaPorData(itens)
  cont = 0
  aux = len(itens)
  while cont < aux:
    for i in range(aux-1):
      
      if itens[i][1][0] == itens[i+1][1][0]:
        if itens[i][1][1] == '' and itens[i+1][1][1] != '':
          temp = itens[i]
          itens[i] = itens[i+1]
          itens[i+1] = temp

        elif itens[i][1][1] != '' and itens[i+1][1][1] != '' and itens[i][1][1] > itens[i+1][1][1]:
          temp = itens[i]
          itens[i] = itens[i+1]
          itens[i+1] = temp
          
    cont += 1

  return itens

def ordenaPorData(itens):
  aux = len(itens)  
  cont = 0
  
  while cont < len(itens):
    for i in range(len(itens)-1):
      if itens[i][1][0][4:] + itens[i][1][0][2:4] + itens[i][1][0][0:2] > itens[i+1][1][0][4:] + itens[i+1][1][0][2:4] + itens[i+1][1][0][0:2]:
        temp = itens[i]
        itens[i] = itens[i+1]
        itens[i+1] = temp
    cont += 1
    
  for i in range(aux-1):
    if itens[i][1][0] == '':
      ultimo = itens.pop(0)
      itens.append(ultimo)

  return itens

def transformaData(elemento):

  data = elemento[1][0]
  data = data[4:] + data[2:4] + data[0:2]

  return data
   
def ordenarPorPrioridade(itens):

  itens = ordenarPorDataHora(itens)
  aux = len(itens)
  cont = 0
  
  while cont < aux:
    for i in range(aux-1):
      
      if itens[i][1][2] != '' and itens[i+1][1][2] != '':
        if itens[i][1][2] > itens[i+1][1][2]:
          temp = itens[i]
          itens[i] = itens[i+1]
          itens[i+1] = temp

      elif itens[i][1][2] == '' and itens[i+1][1][2] != '':
        temp = itens[i]
        itens[i] = itens[i+1]
        itens[i+1] = temp
          
    cont += 1
  
  return itens

def fazer(num):

  atividades = listar()

  if num > len(atividades) or num < 1:
    print('Tá trollando o esquema querendo tirar coisa que não existe né carai')
  
  else:
    feito = atividades.pop(num-1)

    arquivo = open(TODO_FILE, 'w')

    for i in atividades:
      linha = ''

      if i[1][0] != '':
        linha += i[1][0] + ' '
      
      if i[1][1] != '':
        linha += i[1][1] + ' '
      
      if i[1][2] != '':
        linha += i[1][2] + ' '
      
      linha += i[0] + ' '

      if i[1][3] != '':
        linha += i[1][3] + ' '
      
      if i[1][4] != '':
        linha += i[1][4]
      
      arquivo.write(linha + '\n')

    arquivo.close()

    arquivo = open('done.txt','a')

    linha = ''

    if feito[1][0] != '':
      linha += feito[1][0] + ' '
    
    if feito[1][1] != '':
      linha += feito[1][1] + ' '
    
    if feito[1][2] != '':
      linha += feito[1][2] + ' '
    
    linha += feito[0] + ' '

    if feito[1][3] != '':
      linha += feito[1][3] + ' '
    
    if feito[1][4] != '':
      linha += feito[1][4]

    arquivo.write(linha + '\n')
    arquivo.close()


def remover(num):

  atividades = listar()
  if num > len(atividades) or num < 1:
    print('Tá trollando o esquema querendo tirar coisa que não existe né carai')
  
  else:
    atividades.pop(num-1)

    arquivo = open(TODO_FILE, 'w')

    for i in atividades:
      linha = ''

      if i[1][0] != '':
        linha += i[1][0] + ' '
      
      if i[1][1] != '':
        linha += i[1][1] + ' '
      
      if i[1][2] != '':
        linha += i[1][2] + ' '
      
      linha += i[0] + ' '

      if i[1][3] != '':
        linha += i[1][3] + ' '
      
      if i[1][4] != '':
        linha += i[1][4]
      
      arquivo.write(linha + '\n')
      
    arquivo.close()

# prioridade é uma letra entre A a Z, onde A é a mais alta e Z a mais baixa.
# num é o número da atividade cuja prioridade se planeja modificar, conforme
# exibido pelo comando 'l'. 
def priorizar(num, prioridade):

  atividades = listar()

  if 'A' <= prioridade <= 'Z' or 'a' <= prioridade <= 'z':
    prioridade = prioridade.upper()
    mudança = atividades.pop(num-1)

    mudança = (mudança[0],(mudança[1][0],mudança[1][1],'(%s)'%prioridade,mudança[1][3],mudança[1][4]),mudança[2])
    atividades.insert(num-1, mudança)

    arquivo = open(TODO_FILE, 'w')

    for i in atividades:
      linha = ''

      if i[1][0] != '':
        linha += i[1][0] + ' '
      
      if i[1][1] != '':
        linha += i[1][1] + ' '
      
      if i[1][2] != '':
        linha += i[1][2] + ' '
      
      linha += i[0] + ' '

      if i[1][3] != '':
        linha += i[1][3] + ' '
      
      if i[1][4] != '':
        linha += i[1][4]
      
      arquivo.write(linha + '\n')
    
    arquivo.close()
  
  else:
    print('Tá trollando o esquema querendo tirar coisa que não existe né carai')


# Esta função processa os comandos e informações passados através da linha de comando e identifica
# que função do programa deve ser invocada. Por exemplo, se o comando 'adicionar' foi usado,
# isso significa que a função adicionar() deve ser invocada para registrar a nova atividade.
# O bloco principal fica responsável também por tirar espaços em branco no início e fim dos strings
# usando o método strip(). Além disso, realiza a validação de horas, datas, prioridades, contextos e
# projetos. 
def processarComandos(comandos) :
  if comandos[1] == ADICIONAR:
    comandos.pop(0) # remove 'agenda.py'
    comandos.pop(0) # remove 'adicionar'
    itemParaAdicionar = organizar([' '.join(comandos)])[0]
    # itemParaAdicionar = (descricao, (prioridade, data, hora, contexto, projeto))
    adicionar(itemParaAdicionar[0], itemParaAdicionar[1]) # novos itens não têm prioridade

  elif comandos[1] == LISTAR:
    atividades = listarOrdenado()
    
    return atividades

  elif comandos[1] == REMOVER:
    comandos[2] = int(comandos[2])
    remover(comandos[2]-1)
      
  elif comandos[1] == FAZER:
    comandos[2] = int(comandos[2])
    fazer(comandos[2])

  elif comandos[1] == PRIORIZAR:
    comandos[2] = int(comandos[2])
    priorizar(comandos[2], comandos[3])

  else :
    print("Comando inválido.")
    
  
# sys.argv é uma lista de strings onde o primeiro elemento é o nome do programa
# invocado a partir da linha de comando e os elementos restantes são tudo que
# foi fornecido em sequência. Por exemplo, se o programa foi invocado como
#
# python3 agenda.py a Mudar de nome.
#
# sys.argv terá como conteúdo
#
# ['agenda.py', 'a', 'Mudar', 'de', 'nome']
processarComandos(sys.argv)
