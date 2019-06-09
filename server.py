import Pyro4
pessoas = {"1":{"vinculo":"funcionario"},"2":{"vinculo":"visitante"}}
print(pessoas.get("1"))
locais= {"bloco5,andar3":{"limite":1,"atual":0}}

@Pyro4.expose
class mestre(object):
    def consulta_pessoa(self,id_pessoa):
        return pessoas.get(id_pessoa)
    def solicita_acesso(self,local,id_pessoa,sentido):
        if local not in locais:
            return False
        else:
            if id_pessoa in pessoas :
                if pessoas.get(id_pessoa).get("vinculo")=="funcionario":
                    return True
                else:
                    if sentido == "entrar" :
                        if locais.get(local).get("atual") < locais.get(local).get("limite"):
                            return True
                        else :
                            return False
            else:
                return False

    def registra_passagem(self,local,sentido):
        if local not in locais:
            return False
        else:
            if sentido == "entrar":
                locais[local]["atual"]=locais[local]["atual"]+1
                print(locais[local])
            elif sentido == "sair":
                locais[local]["atual"] = locais[local]["atual"] - 1
                print(locais[local])
        return False




def Main():
    print("servidor central")
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(mestre)
    ns.register("mestre",uri)
    print(uri)
    print("pronto")
    daemon.requestLoop()
if __name__ == "__main__":
    Main()