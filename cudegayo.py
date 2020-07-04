import pymysql.cursors
import json

import flask
from flask import request, jsonify

class bar():
   
    def conexao(self):
        try:
            self.banco=pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='hackathondoscria',
                charset='utf8mb4',
                cursorclass = pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar com o bd')    

    def VerificaLoginBar(self,usuario,senha):
        autenticado = False
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('select * from bdbar')
                resultados = self.cursor.fetchall()
        except:
            return('erro ao fazer a consulta')
        for linha in resultados:
            if usuario == linha['strEmail'] and senha == linha['strSenha']:##Usuario e senha digitados
                autenticado = True
                break
            else:
                autenticado = False
        return autenticado
        
        ''' 
        if not autenticado:
            print("Dados errados fia da puta")
        if autenticado:
           for i in self.resultados:
               if i['strEmail']==self.usuario:
                   self.idBar = int(i['idBar'])
                   nomeBar = {'Nome:': i['strNome']}
                   fotoperfilBar= {'Foto:': i['strLogo']}
                   enderecoBar = {'Endereco:': i['strEndereco']}
                   cnpjBar =  {'Cnpj:': i['intCNPJ']}  

        dadosbar = [self.idBar, nomeBar, fotoperfilBar, enderecoBar, cnpjBar]
        self.dadosbar = json.dumps(dadosbar) #DADOS DO BAR AQUI APOS O LOGIN'''
        
    def VerificarEmail(self,email):

        #self.find = False
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('select * from bdbar')
                self.resultados = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta')
        for linha in self.resultados:
            if email == linha['strEmail']:
                return True
            else:
                return False                 
   
    def CadastrarBar(self,Email,Senha,Nome,cnpjbar,enderecobar,logo):
        '''self.Nome = input("Digite seu nome: ")
        self.Email = input("Digite seu email: ")
        self.VerificarEmail()
        while(self.find==True):
            print("Email já cadastrado")
            self.Email= input("Digite seu email novamente: ")
            self.VerificarEmail()
        self.Senha = input("Digite sua senha: ")
        self.enderecobar = input("Digite seu endereço: ")
        self.cnpjbar = int(input("Digite seu CNPJ: "))
        self.logo = input("Digite o logo: ")'''

        self.conexao()

        try:
            with self.banco.cursor() as self.cursor:
                sql = "INSERT INTO bdbar (strNome, strEndereco, strEmail, strSenha,intCNPJ, strLogo) values (%s,%s,%s,%s,%s,%s)"
                val = [Nome, enderecobar, Email, Senha, cnpjbar, logo]
                self.cursor.execute(sql, val)
                self.banco.commit()
                return True
                #self.VerificaLoginBar()
        except:
            return False
            #print("Erro ao fazer a inserção dos dados no bdbar")

    def InserirProduto(self):
        self.NomeProd = input("Digite o nome do produto: ")
        self.DescriProd = input("Digite a descrição do produto: ")
       # self.Ingredientes = input("Digite ingredientes: ")
        self.imagem = input("Insira imagem do produto: ")
        self.valor = input("Digite o valor do produto: ")
        self.tipo = int(input("Digite o tipo do produto: "))
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                sql = "INSERT INTO bdproduto (idBar,strTitulo, strDescricao, dblPreco, intTipo, strFoto) values (%s,%s,%s,%s,%s,%s)"
                val = [self.idBar,self.NomeProd, self.DescriProd,self.valor, self.tipo, self.imagem]
                self.cursor.execute(sql, val)
                self.banco.commit()
                print("Cadastrado")
            
        except:
            print("Erro ao fazer a inserção dos dados no bdproduto")

    def InserirEvento(self):
        self.NomeEv = input("Digite o nome do evento: ")
        self.DescriEv = input("Digite a descrição do evento: ")
        #self.Ingredientes = input("Digite ingredientes: ")
        self.imagemEv = input("Insira imagem do evento: ")
        #self.valor = input("Digite o valor do produto: ")
        self.Data = input("Digite a data do evento: ")
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                sql = "INSERT INTO bdevento (idBar,strTitulo, strDescricao, strFoto, dtData) values (%s,%s,%s,%s,%s)"
                val = [self.idBar,self.NomeEv, self.DescriEv, self.imagemEv, self.Data]
                self.cursor.execute(sql, val)
                self.banco.commit()
                print("Cadastrado")
            
        except:
            print("Erro ao fazer a inserção dos dados no bdevento")
      
    def Pedidos(self):##Salvação_do_grupo.png
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('SELECT * FROM bdpedido')
                self.pedidosBar = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta para os pedidos do bar')
         

        print('PRODUTO  |  CLIENTE   |  Tipo Entrega  |  Pagamento  |  Status')
        for i in self.pedidosBar:
            try:
                with self.banco.cursor() as self.cursor:
                    self.cursor.execute('SELECT strTitulo FROM bdproduto WHERE idProduto ={}'.format(int(i['idProduto'])))
                    self.produtoNome = self.cursor.fetchall()
            except:
                pass
            try:
                with self.banco.cursor() as self.cursor:
                    self.cursor.execute('SELECT strNome FROM bdcliente WHERE idCliente ={}'.format(int(i['idCliente'])))
                    self.clienteNome = self.cursor.fetchall()
            except:
                pass 
            
            if self.idBar==i['idBar']:
                print("{} {} {} {} {}".format(self.produtoNome[0]['strTitulo'], self.clienteNome[0]['strNome'], i['intTipoEntrega'], i['intTipoPagamento'], i['intStatus']))

        self.pedidosBar = json.dumps(self.pedidosBar) #DADOS DOS PEDIDOS

    def ListarProdutosBar(self):
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute("SELECT * FROM bdproduto WHERE idBar = {}". format(self.idBar))
                self.produtosBar = self.cursor.fetchall()
        except:
            print("erro ao fazer consulta bdprodutos - listarprodutosbar")
        
        self.produtosdoBar = json.dumps(self.produtosBar) #LISTA DOS PRODUTOS QUE O BAR POSSUI QUANDO ESTE ESTÁ LOGADO
        return self.produtosdoBar

    def ListarEventosBar(self):
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute("SELECT * FROM bdevento WHERE idBar = {}". format(self.idBar))
                self.eventosBar = self.cursor.fetchall()
        except:
            print("erro ao fazer consulta bdprodutos - listarprodutosbar")
        
        self.eventosdoBar = json.dumps(self.eventosBar) #LISTA DOS EVENTOS QUE O BAR POSSUI QUANDO ESTE ESTÁ LOGADO
        return self.eventosdoBar

    def menuBar(self):
        print('1- Lista Produtos \n')
        print('2- Lista Eventos \n')
        print('3- Cadastrar Produtos\n')
        print('4- Cadastrar Eventos\n')
        print('5- Pedidos\n')
        op = int(input('Escolha:'))
        if op==1:
            self.ListarProdutosBar()
        elif op==2:
            self.ListarEventosBar()
        elif op==3:
            self.InserirProduto()
        elif op==4:
            self.InserirEvento()
        else:
            self.Pedidos()
   
class tchola():

    def conexao(self):
        try:
            self.banco=pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='hackathondoscria',
                charset='utf8mb4',
                cursorclass = pymysql.cursors.DictCursor
            )
        except:
            print('erro ao conectar com o bd')    
    def CadastrarUsuario(self,Email,Senha,Nome,Persona,enderecoUsuario):
        '''self.Nome = input("Digite seu nome: ")
        self.Email = input("Digite seu email: ")
        self.VerificarEmail()
        while(self.find==True):
            print("Email já cadastrado")
            self.Email= input("Digite seu email novamente: ")
            self.VerificarEmail()
        self.Senha = input("Digite sua senha: ")
        self.Persona = int(input("Qual a sua persona 1-Cuzudo 0-Chupador:"))
        self.enderecoUsuario = input("Digite seu endereço: ")'''
        
        self.conexao()
        '''try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('select * from bdcliente')
                self.resultados = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta')
        '''
        try:
            with self.banco.cursor() as self.cursor:
                sql = "INSERT INTO bdcliente (strNome, intPersona,strEmail,strSenha,strEndereco) values (%s,%s,%s,%s,%s)"
                val = [Nome, Persona, Email, Senha, enderecoUsuario]
                self.cursor.execute(sql, val)
                self.banco.commit()
                return True
        except:
            return False
    def VerificaLogin(self,usuario,senha):
        autenticado = False
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('select * from bdcliente')
                self.resultados = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta')
        for linha in self.resultados:
            if usuario == linha['strEmail'] and senha == linha['strSenha']:##Usuario e senha digitados
                autenticado = True
                break
            else:
                autenticado = False
        return autenticado         
    def AddReview(self):
        self.review = input("Digite seu comentário: ")
        self.num_estrela = int(input("Número de estrelas: "))
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                sql = "INSERT INTO bdreview (idBar,idCliente, strReview,intEstrelas) values (%s,%s,%s,%s)"
                val = [self.idBar, self.idCliente, self.review, self.num_estrela]
                self.cursor.execute(sql, val)
                self.banco.commit()
                print("Cadastrado")
        except:
            print("Erro ao fazer a inserção dos dados")

    def VerificarEmail(self, email):

        self.find = False
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('select * from bdcliente')
                self.resultados = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta')
        for linha in self.resultados:
            if email == linha['strEmail']:
                ##self.find = True
                return True
            else:
                return False
    
    def ListarCervejas(self):
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('select * from bdcerveja')
                self.cervejas = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta')

        self.dadosCervejas = json.dumps(self.cervejas) #DADOS DAS CERVEJAS AQUI FIA DA PUTA te fode vagabundo
        return self.cervejas

    def Listarbar(self):
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('select * from bdbar')
                self.bares = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta - bdbar')
            
        self.dadosBares = json.dumps(self.bares) #DADOS DAS CERVEJAS AQUI FIA DA PUTA te fode vagabundo
        return self.bares
        
    def ListarFavoritos(self):
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('SELECT * FROM bdfavoritos WHERE idCliente ={}'.format(self.idCliente))
                self.favoritos = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta - bdfavoritos')

        self.dadosFavoritos = json.dumps(self.favoritos) #DADOS DAS CERVEJAS AQUI FIA DA PUTA te fode vagabundo
        print(self.dadosFavoritos)
        
    def ListarColecao(self):
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('SELECT * FROM bdfavoritoscol WHERE idCliente ={}'.format(self.idCliente))
                self.colecao = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta - bdfavoritoscol')

        self.dadosColecao = json.dumps(self.colecao) #DADOS DAS CERVEJAS AQUI FIA DA PUTA te fode vagabundo
        print(self.dadosColecao)

    def ListarPedidos(self):
        self.conexao()
        
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('SELECT * FROM bdpedido WHERE idCliente ={}'.format(self.idCliente))
                self.pedidos = self.cursor.fetchall()
        except:
            print('erro ao fazer a consulta - bdpedido')

        self.dadosPedidos = json.dumps(self.pedidos) #Pedidos realizados 
        print(self.dadosPedidos)
   
    def ListarEventos(self,idBar):
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('SELECT * FROM bdevento WHERE idBar ={}'.format(idBar))
                eventos = self.cursor.fetchall()
        except:
            return('erro ao fazer a consulta - bdevento')

        #self.dadosEventos = json.dumps(self.eventos) #Eventos disponíveis 
        return(eventos)

    def ListarProdutos(self,idBar):
        self.conexao()
        try:
            with self.banco.cursor() as self.cursor:
                self.cursor.execute('SELECT * FROM bdproduto WHERE idBar ={}'.format(idBar))
                produtos = self.cursor.fetchall()
        except:
            return ('erro ao fazer a consulta - bdproduto')

        return produtos
        

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Ambev club</h1><p>API do API do birubiru.</p>"

###CERVEJAS----------------------------------------------- FEITO
@app.route('/api/usuario/cervejas/all', methods=['GET'])
def api_all_cerveja():
    return jsonify(tchola().ListarCervejas())

@app.route('/api/usuario/cervejas', methods=['GET'])
def api_id_cerveja():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []
    for cerveja in tchola().ListarCervejas():
        print(cerveja)
        if cerveja['idCerveja'] == id:
            results.append(cerveja)

    return jsonify(results) 
###CERVEJAS-----------------------------------------------

###PRODUTOS----------------------------------------------- FEITO
@app.route('/api/usuario/produtos/all', methods=['GET'])
def api_all_produto():
    if 'idBar' in request.args:
        idBar = int(request.args['idBar'])
    else:
        return "Error: No idBar field provided. Please specify an id."

    return jsonify(tchola().ListarProdutos(idBar))

@app.route('/api/usuario/produtos', methods=['GET'])
def api_id_produto():
    if 'idBar' and 'id' in request.args:
        id = int(request.args['id'])
        idBar = int(request.args['idBar'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []
    for produto in tchola().ListarProdutos(idBar): #TESTAR
        print(produto)
        if produto['idProduto'] == id:
            results.append(produto)
    return jsonify(results)
###PRODUTOS----------------------------------------------

###EVENTOS DE UM BAR----------------------------------------------- FEITO
@app.route('/api/usuario/eventos/all', methods=['GET'])
def api_all_eventos():
    if 'idBar' in request.args:
        idBar = int(request.args['idBar'])
    else:
        return "Error: No idBar field provided. Please specify an id."

    return jsonify(tchola().ListarEventos(idBar))

@app.route('/api/usuario/eventos', methods=['GET'])
def api_id_eventos():
    if 'idBar' and 'id' in request.args:
        id = int(request.args['id'])
        idBar = int(request.args['idBar'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []
    for eventos in tchola().ListarEventos(idBar):
        print(eventos)
        if eventos['idEvento'] == id:
            results.append(eventos)

    return jsonify(results) 
###EVENTOS-----------------------------------------------

###BARES----------------------------------------------- FEITO
@app.route('/api/usuario/bares/all', methods=['GET'])
def api_all_bares():
    return jsonify(tchola().Listarbar())

@app.route('/api/usuario/bares', methods=['GET'])
def api_id_bares():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []
    for bar in tchola().Listarbar():
        print(bar)
        if bar['idBar'] == id:
            results.append(bar)

    return jsonify(results) 
###BARES-----------------------------------------------

###AUTENTICAÇÃO USUARIO-----------------------------------------------
@app.route('/api/usuario/autenticar', methods=['GET'])
def api_autenticar_usuario():
    if 'strEmail' in request.args and 'strSenha' in request.args:
        email = request.args['strEmail']
        senha = request.args['strSenha']
    else:
        return "Error: No strEmail or strSenha field provided. Please specify an id."

    return jsonify(tchola().VerificaLogin(email,senha))
###AUTENTICAÇÃO USUARIO-----------------------------------------------

###AUTENTICAÇÃO BAR-----------------------------------------------
@app.route('/api/bar/autenticar', methods=['GET'])
def api_autenticar_bar():
    if 'strEmail' in request.args and 'strSenha' in request.args:
        email = request.args['strEmail']
        senha = request.args['strSenha']
    else:
        return "Error: No strEmail or strSenha field provided. Please specify an id."

    return jsonify(bar().VerificaLoginBar(email,senha))
###AUTENTICAÇÃO BAR-----------------------------------------------


###CADASTRAR-----------------------------------------------
@app.route('/api/usuario/cadastrar/email', methods=['GET'])
def api_verificar_email_usuario():
    if 'strEmail' in request.args:
        email = request.args['strEmail']
    else:
        return "Error: No strEmail or field provided. Please specify an email."

    return jsonify(tchola().VerificarEmail(email))

@app.route('/api/usuario/cadastrar', methods=['GET'])
def api_cadastrar_usuario():
    if 'strEmail' and 'strSenha' and  'strNome' and 'intPersona' and 'strEndereco' in request.args:
        email= request.args['strEmail']
        senha= request.args['strSenha']
        nome= request.args['strNome']
        persona= int(request.args['intPersona'])
        endereco=request.args['strEndereco']
    else:  
        return "Error: missing fields on request."
    
    return jsonify(tchola().CadastrarUsuario(email,senha,nome,persona,endereco))

@app.route('/api/bar/cadastrar/email', methods=['GET'])
def api_verificar_email_bar():
    if 'strEmail' in request.args:
        email = request.args['strEmail']
    else:
        return "Error: No strEmail or field provided. Please specify an email."

    return jsonify(bar().VerificarEmail(email))
@app.route('/api/bar/cadastrar', methods=['GET'])
def api_cadastrar_bar():
    if 'strNome'and 'strEndereco'and 'strEmail'and 'strSenha'and'intCNPJ'and 'strLogo' in request.args:
        email= request.args['strEmail']
        senha= request.args['strSenha']
        nome= request.args['strNome']
        CNPJ= int(request.args['intCNPJ'])
        endereco=request.args['strEndereco']
        logo=request.args['strLogo']
    else:  
        return "Error: missing fields on request."
    
    return jsonify(bar().CadastrarBar(email,senha,nome,CNPJ,endereco,logo))

###CADASTRAR-----------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

app.run()

a = int(input("1 - Bar | 2 - Cliente "))
if a==1:
    bar()
else:
    tchola()