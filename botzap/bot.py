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
    xpath_contato_origem = '//*[@id="pane-side"]/div[1]/div/div/div[5]/div/div/div[2]/div[1]/div[1]/div/span/span'
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


    @classmethod 
    def reinicia(self):
        self.driver.refresh()
        bot.abre_conversa(self.contato_origem)  # Passando o numero ou o nome do contato

        x = False
        while x != True:
            self.repassar_msg()
            time.sleep(0.5)

    @staticmethod
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
                #menu = self.driver.find_elements_by_css_selector("span[data-icon='menu']")
                #menu[1].click()
                #time.sleep(0.4)
                #selecionar_msg = self.driver.find_elements_by_css_selector("li[data-animate-dropdown-item='true']")
                #selecionar_msg[1].click()
                #time.sleep(1)
                
                time.sleep(1)
                self.abrir_menu(self)
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
                    '''self.driver.refresh()
                    bot.abre_conversa(self.contato_origem)  # Passando o numero ou o nome do contato

                    x = False
                    while x != True:
                        self.repassar_msg()
                        time.sleep(0.5)'''

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

    x = False
    while x != True:
        bot.repassar_msg()
        time.sleep(0.5)
