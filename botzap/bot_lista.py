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
    getTotalMensagens = 0


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
            except:
                Exception


    def seleciona_mensagem(self, faltantes):
        self.getTotalMensagens = self.getTotalMensagens + 1
        for i in self.faltantes:
            choices = self.driver.find_elements_by_xpath("//div[contains(@data-id,'{}')]/span/div/div".format(i))
            #print(f'Choices[0]: {choices[0]}')
            time.sleep(0.2)
            try:
                choices[0].click()
                self.lista_enviados.append(i)
            except:
                Exception
        

    def verifica_mensagens(self):
        if len(self.lista_enviados) > 35:
            while len(self.lista_enviados) > 35:
                self.lista_enviados.pop(0)
        self._id = []
        self.id_msg = []
        id_msg = self.driver.find_elements_by_css_selector("div[class*='_2hqOq']")
        x = 1
        for i in id_msg:
            try:
                ultimo_id_msg = id_msg[x].get_attribute("data-id")
                self._id.append(ultimo_id_msg)
                x=x+1
            except:
                Exception
        for i in self._id:
            if i is None:
                self._id.remove(i)
            elif 'grouped-sticker' in i:
                self._id.remove(i)
            elif 'album' in i:
                self._id.remove(i)
            else:
                pass
        for i in self._id:
            if i in self.lista_enviados:
                self._id.remove(i)
        self.ultimos_5 = []
        self.ultimos_5 = self._id
        self.ultimos_5.reverse()
        self.ultimos_5 = self.ultimos_5[:5]
        #print(f'ultimos 5: {self.ultimos_5}')
        #print(f'ultimos 5: {self.ultimos_5}')
        self.encaminhando(self.ultimos_5)


    def encaminhando(self, ultimos_5):
        ##self.ids_chaves = self.lista_enviados[]
        self.faltantes = []
        for i in self.ultimos_5:
            if i not in self.lista_enviados:
                self.faltantes.append(i)
        #print(f'Lista_enviados: {self.lista_enviados}')
        print(f'Faltantes: {self.faltantes}')
        print(f'Bot já reiniciou: {self.getReiniciou}')
        print(f'Foram enviadas: {self.getTotalMensagens} mensagens')
        if self.faltantes:
            if None in self.faltantes:
                self.faltantes.remove(None)
            else:
                self.abrir_menu()
                self.seleciona_mensagem(self.faltantes)
                self.encaminha_mensagem()


    def encaminha_mensagem(self):
        try:
            self.driver.find_element_by_css_selector("span[data-icon='forward']").click()
        except:
            Exception
            #zapbot.reinicia()
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
        try:
            menu[1].click()
        except:
            Exception
        time.sleep(0.4)
        try:
            selecionar_msg = self.driver.find_elements_by_css_selector("li[data-animate-dropdown-item='true']")
            selecionar_msg[1].click()
            time.sleep(1)
        except:
            Exception


if __name__ == '__main__':
    bot = zapbot()  # Inicia o objeto zapbot
    bot.abre_conversa(bot.contato_origem)  # Passando o numero ou o nome do contato
 
    while True:
        bot.verifica_mensagens()
        time.sleep(0.5)
