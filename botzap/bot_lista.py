import random
import time

from selenium import webdriver
import os
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


class zapbot:
    #variaveis de funcionamento
    contato_origem = 'PanelaTI'
    contato_destino = 'grupo que envia a msg'
    class_caixa_de_pesquisa = '.\_3FRCZ'
    xpath_contato_origem = '//*[@id="pane-side"]/div[1]/div/div/div[5]/div/div/div[2]/div[1]'
    class_contato_destino = '_3ko75'

    # O local de execução do nosso script
    dir_path = os.getcwd()
    # O caminho do chromedriver
    opts = webdriver.ChromeOptions()
    opts.add_argument("start-maximized")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option('useAutomationExtension', False)
    opts.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=opts)
    driver.set_window_position(0, 0)
    driver.set_window_size(800, 800)
    chromedriver = os.path.join(dir_path, "chromedriver.exe")
    # Caminho onde será criada pasta profile
    profile = os.path.join(dir_path, "profile", "wpp")
    action = ActionChains(driver)
    ultimamsg_id = ""
    ultimamsg_looping = ""
    lista_enviados = []
    faltantes = []
    getReiniciou = 0


    def __init__(self):
        # Abre o whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        # Aguarda alguns segundos para validação manual do QrCode
        self.driver.implicitly_wait(15)
       
    
    def abre_conversa(self, contato):
        """ Abre a conversa com um contato especifico """
        try:
            # Seleciona a caixa de pesquisa de conversa
            
            #self.caixa_de_pesquisa = self.driver.find_element_by_css_selector("span[data-testid='search']")
            self.caixa_de_pesquisa = self.driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
            # Digita o nome ou numero do contato
            self.caixa_de_pesquisa.send_keys(contato)
            
            sleep(2)
            # Seleciona o contato 
            #self.contato = self.driver.find_element_by_xpath("span[.='{}']".format(contato))
            self.contato = self.driver.find_element_by_xpath(self.xpath_contato_origem)
            #self.action.moveByOffset(xCoordinate, yCoordinate).click().build().perform();

            # Entra na conversa
            self.contato.click()
            self.caixa_de_pesquisa.clear()
            time.sleep(1)
        except:
            try:
                self.caixa_de_pesquisa = self.driver.find_element_by_css_selector(".\_3FRCZ")
                self.caixa_de_pesquisa.send_keys(contato)
                sleep(2)
                self.contato = self.driver.find_element_by_xpath(self.xpath_contato_origem)
                self.contato.click()
                self.caixa_de_pesquisa.clear()
                time.sleep(1)
            except Exception as e:
                zapbot.reinicia()


    def get10MsgPrimeiraVez(self):
        id_msg = self.driver.find_elements_by_css_selector("div[class*='_2hqOq']")
        x = 1
        try:
            for i in id_msg:
                if i is None:
                    break
                else:
                    try:
                        ultimo_id_msg = id_msg[len(id_msg)-x].get_attribute("data-id")
                        self.lista_enviados.append(ultimo_id_msg)
                    except:
                        pass
                x=x+1
        except:
            raise
        for i in self.lista_enviados:
            if i is None:
                self.lista_enviados.remove(i)
            elif 'grouped-sticker' in i:
                self.lista_enviados.remove(i)
            elif 'album' in i:
                self.lista_enviados.remove(i)
        for i in self.lista_enviados:
            if i is None:
                self.lista_enviados.remove(i)
             
        self.abrir_menu()
        time.sleep(2)
        print(self.lista_enviados[-1])
        self.seleciona_mensagem(self.lista_enviados[0])
        
        self.encaminha_mensagem()


    def seleciona_mensagem(self, id):
        choices = self.driver.find_elements_by_xpath("//div[contains(@data-id,'{}')]/span/div/div".format(id))
        #print(f'Choices[0]: {choices[0]}')
        time.sleep(0.5)
        try:
            choices[0].click()
        except:
            self.reinicia()
        self.lista_enviados.append(id)
        

    def verifica_mensagens(self):
        if len(self.lista_enviados) > 35:
            while len(self.lista_enviados) > 35:
                self.lista_enviados.pop(0)
        x = 1
        self._id = []
        self.id_msg = None
        id_msg = self.driver.find_elements_by_css_selector("div[class*='_2hqOq']")
        try:
            for i in id_msg:
                if i is None:
                    break
                else:
                    ultimo_id_msg = id_msg[len(id_msg)-x].get_attribute("data-id")
                    self._id.append(ultimo_id_msg)
                x=x+1
        except Exception:
            #self.reinicia()
            print(Exception.__getattribute__)
        for i in self._id:
            if i is None:
                break
            elif 'grouped-sticker' in i:
                self._id.remove(i)
            elif 'album' in i:
                self._id.remove(i)
        self.ultimos_5 = []
        self.ultimos_5 = list(set(self._id))
        self.ultimos_5.reverse()
        self.ultimos_5 = self.ultimos_5[:5]
        #print(f'ultimos 5: {self.ultimos_5}')
        #print(f'ultimos 5: {self.ultimos_5}')
        self.encaminhando(self.ultimos_5)


    def encaminhando(self, ultimos_5):
        ##self.ids_chaves = self.lista_enviados[]
        for i in self.ultimos_5:
            if i in self.lista_enviados:
                pass
            elif i not in self.faltantes:
                self.faltantes.append(i)
        #print(f'Lista_enviados: {self.lista_enviados}')
        print(f'Faltantes: {self.faltantes}')
        print(f'Bot já reiniciou: {self.getReiniciou}')
        if not self.faltantes:
            #se for vazio
            print(f'self.faltantes está vazio')
            pass
        else:
            self.abrir_menu()
            for i in self.faltantes:
                self.seleciona_mensagem(i)
                self.faltantes.remove(i)
            self.encaminha_mensagem()


    def encaminha_mensagem(self):
        try:
            self.driver.find_element_by_css_selector("span[data-icon='forward']").click()
        except:
            zapbot.reinicia()
        time.sleep(1)
        #para quem vai a mensagem
        self.driver.find_elements_by_css_selector("div[contenteditable='true']")[0].send_keys(self.contato_destino)
        time.sleep(1)
        self.driver.find_element_by_class_name(self.class_contato_destino).click() #_3ko75 _5h6Y_ _3Whw5
        self.driver.find_element_by_css_selector("span[data-icon='send']").click()
        time.sleep(0.5)
        self.abre_conversa(self.contato_origem)
    
    @classmethod 
    def reinicia(self):
        self.getReiniciou = self.getReiniciou + 1
        self.driver.refresh()
        bot.abre_conversa(self.contato_origem)  # Passando o numero ou o nome do contato
        bot.get10MsgPrimeiraVez()
        while True:
            bot.verifica_mensagens()
            time.sleep(0.5)


    def abrir_menu(self):
        menu = self.driver.find_elements_by_css_selector("span[data-icon='menu']")
        menu[1].click()
        time.sleep(0.4)
        try:
            selecionar_msg = self.driver.find_elements_by_css_selector("li[data-animate-dropdown-item='true']")
            selecionar_msg[1].click()
            time.sleep(1)
        except:
            self.abrir_menu()


    @classmethod
    def repassar_msg(self):
        id_msg = self.driver.find_elements_by_css_selector("div[class*='_2hqOq']")
        
        try:
            ultima_id_msg = id_msg[len(id_msg) - 1].get_attribute("data-id")
        except:
            zapbot.reinicia()

        while self.ultimamsg_looping != ultima_id_msg:
            id_msg = self.driver.find_elements_by_css_selector("div[class*='_2hqOq']")
            try:
                ultima_id_msg = id_msg[len(id_msg) - 1].get_attribute("data-id")
            except:
                zapbot.reinicia()
            if ultima_id_msg != self.ultimamsg_id:
                time.sleep(1)
                self.abrir_menu()
                x = 1
                for c in range(len(id_msg)):
                    if self.ultimamsg_id != "":
                        try:
                            while id_msg[len(id_msg) - x].get_attribute("data-id") != self.ultimamsg_id:
                                try:
                                    if id_msg[len(id_msg) - x].get_attribute("data-id").startswith("album"):
                                        break
                                    elif id_msg[len(id_msg) - x].get_attribute("data-id").startswith("grouped-sticker"):
                                        break
                                    else:
                                        botao_pra_enviar = self.driver.find_elements_by_class_name("_2XWkx")
                                        botao_pra_enviar[len(botao_pra_enviar) - x].click()
                                        x += 1
                                except:
                                    break
                                
                                
                                self.ultimamsg_looping = id_msg[len(id_msg) - 1].get_attribute("data-id")
                        except:
                            pass
                    else:
                        botao_pra_enviar = self.driver.find_elements_by_class_name("_2XWkx")
                        botao_pra_enviar[len(botao_pra_enviar) - 1].click()
                        self.ultimamsg_looping = id_msg[len(id_msg) - 1].get_attribute("data-id")
                        break
                time.sleep(1)
                print(self.ultimamsg_looping,ultima_id_msg)
                if self.ultimamsg_looping != ultima_id_msg:
                    self.driver.find_element_by_css_selector("span[data-icon='x']").click()
                    print('entrou nesse if estranho na linha 156')
                    bot.repassar_msg()
                try:
                    self.driver.find_element_by_css_selector("span[data-icon='forward']").click()
                except:
                    zapbot.reinicia()

                time.sleep(1)
                self.driver.find_elements_by_css_selector("div[contenteditable='true']")[0].send_keys(self.contato_destino)# para quem vai a mensagem
                time.sleep(1)
                self.driver.find_element_by_class_name(self.class_contato_destino).click() #_3ko75 _5h6Y_ _3Whw5
                self.driver.find_element_by_css_selector("span[data-icon='send']").click()
                self.ultimamsg_id = ultima_id_msg
                """ Abre a conversa com um contato especifico """
                time.sleep(0.5)
                try:
                    # Seleciona a caixa de pesquisa de conversa
                    self.caixa_de_pesquisa = self.driver.find_element_by_css_selector(self.class_caixa_de_pesquisa)
                    # Digita o nome ou numero do contato
                    self.caixa_de_pesquisa.send_keys(self.contato_origem)
                    sleep(1)
                    # Seleciona o contato
                    self.contato = self.driver.find_element_by_xpath(self.xpath_contato_origem)

                    # Entra na conversa
                    self.contato.click()
                    self.caixa_de_pesquisa.clear()
                except Exception as e:
                    zapbot.reinicia()


if __name__ == '__main__':
    bot = zapbot()  # Inicia o objeto zapbot
    bot.abre_conversa(bot.contato_origem)  # Passando o numero ou o nome do contato
    bot.get10MsgPrimeiraVez() #pega os 10 primeiros
    # primeiro ciclo concluído
    while True:
        bot.verifica_mensagens()
        time.sleep(0.5)
